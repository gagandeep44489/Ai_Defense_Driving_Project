from datetime import date

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    plan = db.Column(db.String(20), default="free", nullable=False)
    stripe_customer_id = db.Column(db.String(255), nullable=True)
    daily_seconds_used = db.Column(db.Float, default=0.0, nullable=False)
    usage_reset_date = db.Column(db.Date, default=date.today, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    transcripts = db.relationship("Transcript", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)


class Transcript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(10), default="en-IN", nullable=False)
    duration_seconds = db.Column(db.Float, default=0.0, nullable=False)
    transcript_text = db.Column(db.Text, nullable=False)
    summary_text = db.Column(db.Text, nullable=True)
    keywords = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
