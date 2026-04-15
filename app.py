import os
import re
import tempfile
import wave
from collections import Counter
from datetime import date

import speech_recognition as sr
import stripe
from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from models import Transcript, User, db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["STRIPE_SECRET_KEY"] = os.getenv("STRIPE_SECRET_KEY", "")
app.config["STRIPE_PRICE_PRO"] = os.getenv("STRIPE_PRICE_PRO", "")
app.config["STRIPE_PRICE_BUSINESS"] = os.getenv("STRIPE_PRICE_BUSINESS", "")

FREE_PLAN_DAILY_LIMIT_SECONDS = 600
PLAN_PRICING = {
    "free": "$0/month",
    "pro": "$9/month",
    "business": "$29/month",
}
PLAN_PRICE_LOOKUP = {
    "pro": app.config["STRIPE_PRICE_PRO"],
    "business": app.config["STRIPE_PRICE_BUSINESS"],
}

STOP_WORDS = {
    "the", "a", "an", "and", "or", "to", "of", "for", "in", "on", "at", "is", "are", "it", "this", "that",
    "with", "as", "by", "from", "be", "was", "were", "will", "can", "could", "should", "i", "you", "we", "they",
    "he", "she", "them", "our", "your", "my", "me", "us", "but", "if", "then", "so", "than", "very", "just",
    "hai", "ki", "ka", "ke", "ko", "aur", "mein", "main", "se", "par", "ye", "woh", "ek", "kya", "kyon", "jab",
}


db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
stripe.api_key = app.config["STRIPE_SECRET_KEY"]


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()
    user_columns = [row[1] for row in db.session.execute(db.text("PRAGMA table_info(user)")).fetchall()]
    if "stripe_customer_id" not in user_columns:
        db.session.execute(db.text("ALTER TABLE user ADD COLUMN stripe_customer_id VARCHAR(255)"))
        db.session.commit()


def reset_usage_if_needed(user: User) -> None:
    today = date.today()
    if user.usage_reset_date != today:
        user.usage_reset_date = today
        user.daily_seconds_used = 0
        db.session.commit()


def summarize_text(text: str, sentence_count: int = 2) -> str:
    if not text.strip():
        return ""

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    if len(sentences) <= sentence_count:
        return text.strip()

    words = re.findall(r"[A-Za-z\u0900-\u097F']+", text.lower())
    freq = Counter(word for word in words if word not in STOP_WORDS and len(word) > 2)

    scored = []
    for sentence in sentences:
        sentence_words = re.findall(r"[A-Za-z\u0900-\u097F']+", sentence.lower())
        score = sum(freq.get(word, 0) for word in sentence_words)
        scored.append((score, sentence))

    top_sentences = [s for _, s in sorted(scored, key=lambda item: item[0], reverse=True)[:sentence_count]]
    return " ".join(top_sentences)


def extract_keywords(text: str, keyword_count: int = 8) -> list[str]:
    words = re.findall(r"[A-Za-z\u0900-\u097F']+", text.lower())
    filtered = [word for word in words if word not in STOP_WORDS and len(word) > 2]
    keyword_freq = Counter(filtered)
    return [word for word, _ in keyword_freq.most_common(keyword_count)]


def calculate_wav_duration_seconds(path: str) -> float:
    with wave.open(path, "rb") as wf:
        frames = wf.getnframes()
        framerate = wf.getframerate()
        if framerate == 0:
            return 0.0
        return frames / float(framerate)


def require_paid_features():
    if current_user.plan == "free":
        return jsonify({"error": "Upgrade to Pro to use summaries and downloads."}), 403
    return None


def create_or_get_stripe_customer(user: User) -> str:
    if user.stripe_customer_id:
        return user.stripe_customer_id

    customer = stripe.Customer.create(email=user.email, metadata={"user_id": str(user.id)})
    user.stripe_customer_id = customer.id
    db.session.commit()
    return customer.id


def sync_plan_from_checkout_session(user: User, session_id: str) -> None:
    if not app.config["STRIPE_SECRET_KEY"]:
        return

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.get("payment_status") != "paid":
            return

        target_plan = session.get("metadata", {}).get("target_plan")
        customer_id = session.get("customer")
        if target_plan in {"pro", "business"} and customer_id == user.stripe_customer_id:
            user.plan = target_plan
            db.session.commit()
    except Exception:
        return


@app.route("/")
def landing_page():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("index.html", plan_pricing=PLAN_PRICING)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            return render_template("signup.html", error="Email and password are required."), 400
        if User.query.filter_by(email=email).first():
            return render_template("signup.html", error="Account already exists. Please log in."), 409

        user = User(email=email, plan="free")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return render_template("login.html", error="Invalid credentials."), 401

        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("landing_page"))


@app.route("/dashboard")
@login_required
def dashboard():
    reset_usage_if_needed(current_user)

    checkout_session_id = request.args.get("session_id")
    if checkout_session_id:
        sync_plan_from_checkout_session(current_user, checkout_session_id)

    remaining = None
    if current_user.plan == "free":
        remaining = max(FREE_PLAN_DAILY_LIMIT_SECONDS - current_user.daily_seconds_used, 0)

    return render_template(
        "dashboard.html",
        user=current_user,
        remaining_seconds=remaining,
        has_stripe_config=bool(app.config["STRIPE_SECRET_KEY"]),
    )


@app.route("/create-checkout-session", methods=["POST"])
@login_required
def create_checkout_session():
    if not app.config["STRIPE_SECRET_KEY"]:
        return jsonify({"error": "Stripe is not configured. Add STRIPE_SECRET_KEY and Stripe price IDs."}), 500

    payload = request.get_json(silent=True) or {}
    target_plan = payload.get("plan")
    if target_plan not in {"pro", "business"}:
        return jsonify({"error": "Invalid paid plan selection."}), 400

    stripe_price_id = PLAN_PRICE_LOOKUP.get(target_plan)
    if not stripe_price_id:
        return jsonify({"error": f"Missing Stripe price id for {target_plan} plan."}), 500

    customer_id = create_or_get_stripe_customer(current_user)

    checkout = stripe.checkout.Session.create(
        mode="subscription",
        customer=customer_id,
        customer_email=current_user.email,
        line_items=[{"price": stripe_price_id, "quantity": 1}],
        success_url=url_for("dashboard", _external=True) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=url_for("dashboard", _external=True),
        metadata={"target_plan": target_plan, "user_id": str(current_user.id)},
    )

    return jsonify({"url": checkout.url})


@app.route("/create-portal-session", methods=["POST"])
@login_required
def create_portal_session():
    if not app.config["STRIPE_SECRET_KEY"]:
        return jsonify({"error": "Stripe is not configured."}), 500

    if not current_user.stripe_customer_id:
        return jsonify({"error": "No Stripe customer found. Please subscribe first."}), 400

    portal_session = stripe.billing_portal.Session.create(
        customer=current_user.stripe_customer_id,
        return_url=url_for("dashboard", _external=True),
    )

    return jsonify({"url": portal_session.url})


@app.route("/api/history")
@login_required
def api_history():
    history = Transcript.query.filter_by(user_id=current_user.id).order_by(Transcript.created_at.desc()).all()
    rows = [
        {
            "id": item.id,
            "filename": item.filename,
            "language": item.language,
            "duration_seconds": round(item.duration_seconds, 2),
            "transcript_text": item.transcript_text,
            "summary_text": item.summary_text,
            "keywords": item.keywords.split(",") if item.keywords else [],
            "created_at": item.created_at.strftime("%Y-%m-%d %H:%M") if item.created_at else "",
        }
        for item in history
    ]
    return jsonify({"history": rows})


@app.route("/api/transcribe", methods=["POST"])
@login_required
def api_transcribe():
    reset_usage_if_needed(current_user)
    recognizer = sr.Recognizer()
    temp_path = None

    try:
        audio_file = request.files.get("audio")
        language = request.form.get("language", "en-IN")
        if language not in {"en-IN", "hi-IN"}:
            return jsonify({"error": "Unsupported language. Use English or Hindi."}), 400

        if not audio_file:
            return jsonify({"error": "No audio file provided."}), 400

        filename = (audio_file.filename or "recording.wav").strip()
        if not filename.lower().endswith(".wav"):
            return jsonify({"error": "Only WAV audio files are supported."}), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            audio_file.save(tmp_file)
            temp_path = tmp_file.name

        with wave.open(temp_path, "rb"):
            pass

        duration_seconds = calculate_wav_duration_seconds(temp_path)

        if current_user.plan == "free":
            projected = current_user.daily_seconds_used + duration_seconds
            if projected > FREE_PLAN_DAILY_LIMIT_SECONDS:
                return jsonify({
                    "error": "Daily free limit reached (10 minutes). Upgrade to Pro for unlimited transcription.",
                    "used_seconds": round(current_user.daily_seconds_used, 2),
                    "limit_seconds": FREE_PLAN_DAILY_LIMIT_SECONDS,
                }), 403

        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)

        transcript_text = recognizer.recognize_google(audio_data, language=language)
        keywords = extract_keywords(transcript_text)

        saved = Transcript(
            user_id=current_user.id,
            filename=filename,
            language=language,
            duration_seconds=duration_seconds,
            transcript_text=transcript_text,
            keywords=",".join(keywords),
        )

        current_user.daily_seconds_used += duration_seconds
        db.session.add(saved)
        db.session.commit()

        return jsonify({
            "id": saved.id,
            "text": transcript_text,
            "keywords": keywords,
            "duration_seconds": round(duration_seconds, 2),
            "plan": current_user.plan,
        })

    except wave.Error:
        return jsonify({"error": "Invalid WAV file."}), 400
    except sr.UnknownValueError:
        return jsonify({"error": "Speech could not be recognized. Please upload clearer audio."}), 422
    except sr.RequestError:
        return jsonify({"error": "Google speech service is unavailable right now."}), 503
    except Exception as exc:
        return jsonify({"error": f"Unexpected error: {exc}"}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.route("/api/summarize", methods=["POST"])
@login_required
def api_summarize():
    paid_check = require_paid_features()
    if paid_check:
        return paid_check

    payload = request.get_json(silent=True) or {}
    transcript_id = payload.get("transcript_id")
    raw_text = payload.get("text", "").strip()

    transcript = None
    if transcript_id:
        transcript = Transcript.query.filter_by(id=transcript_id, user_id=current_user.id).first()
        if not transcript:
            return jsonify({"error": "Transcript not found."}), 404
        source_text = transcript.transcript_text
    else:
        source_text = raw_text

    if not source_text:
        return jsonify({"error": "No text available to summarize."}), 400

    summary = summarize_text(source_text)
    keywords = extract_keywords(source_text)

    if transcript:
        transcript.summary_text = summary
        transcript.keywords = ",".join(keywords)
        db.session.commit()

    return jsonify({"summary": summary, "keywords": keywords})


@app.route("/download/<int:transcript_id>")
@login_required
def download_transcript(transcript_id: int):
    paid_check = require_paid_features()
    if paid_check:
        return paid_check

    transcript = Transcript.query.filter_by(id=transcript_id, user_id=current_user.id).first_or_404()

    content = (
        f"VoiceFlow AI Transcript\n"
        f"Generated for: {current_user.email}\n"
        f"Language: {transcript.language}\n"
        f"Duration: {round(transcript.duration_seconds, 2)} seconds\n\n"
        f"Transcript:\n{transcript.transcript_text}\n\n"
        f"Summary:\n{transcript.summary_text or 'Not generated yet'}\n\n"
        f"Keywords:\n{transcript.keywords or 'Not generated yet'}\n"
    )

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmp.write(content.encode("utf-8"))
    tmp.close()

    return send_file(
        tmp.name,
        as_attachment=True,
        download_name=f"transcript_{transcript_id}.txt",
        mimetype="text/plain",
    )


@app.route("/api/transcribe/bulk", methods=["POST"])
@login_required
def api_transcribe_bulk():
    if current_user.plan != "business":
        return jsonify({"error": "Bulk uploads are available on Business plan only."}), 403

    files = request.files.getlist("audio")
    if not files:
        return jsonify({"error": "No files provided for bulk transcription."}), 400

    results = [{"filename": file.filename} for file in files]

    return jsonify({
        "message": "Business bulk upload endpoint is ready. Integrate queue worker for production-scale async processing.",
        "files_received": results,
    })


if __name__ == "__main__":
    app.run(debug=True)
