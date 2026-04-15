# VoiceFlow AI – Smart Voice Intelligence Platform

VoiceFlow AI is a SaaS-ready Flask startup project that transforms raw audio into actionable intelligence: transcription, summaries, and keyword insights. It includes user auth, pricing plans, usage limits, multilingual support (English + Hindi), and dashboard history.

## Project Overview

The project evolves a basic speech-to-text utility into a monetizable startup foundation:

- **AI voice transcription** using SpeechRecognition + Google Web Speech API
- **Summary generation** for quick understanding
- **Keyword/task-like extraction** for actionability
- **SaaS plans** with usage restrictions and premium feature gating
- **Business-ready architecture** with APIs and persistent storage

## Features

### Product Features
- Landing page with startup positioning and CTA: **“Turn Voice into Actionable Intelligence”**
- User auth system (Signup/Login/Logout)
- Dashboard for transcription workflow and history
- English and Hindi transcription (`en-IN`, `hi-IN`)
- WAV upload + browser microphone recording
- AI summary generation and keyword extraction
- Download transcript as TXT (Pro/Business)
- Transcription history per user

### SaaS Monetization Features
- **Free**: 10 minutes/day transcription, basic transcription only
- **Pro ($9/month)**: Unlimited transcription + summaries + TXT downloads
- **Business ($29/month)**: Pro features + API/bulk access endpoint
- Daily usage tracking and automatic free-tier limit enforcement
- Stripe Checkout + Stripe Customer Portal integration for self-serve billing

## Tech Stack

- **Backend**: Python, Flask, Flask-Login, Flask-SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **AI**: SpeechRecognition (Google Web Speech API)
- **Database**: SQLite (`database.db`)

## Screenshots

> Placeholder: add screenshots after running locally.

- `![Landing Page](docs/screenshots/landing-placeholder.png)`
- `![Dashboard](docs/screenshots/dashboard-placeholder.png)`

## Installation & Local Run

```bash
git clone <your-repo-url>
cd Ai_Defense_Driving_Project
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open: `http://127.0.0.1:5000`

### Stripe Billing Environment Variables

Set these before running to enable paid upgrades and billing management:

```bash
export STRIPE_SECRET_KEY=sk_test_xxx
export STRIPE_PRICE_PRO=price_xxx
export STRIPE_PRICE_BUSINESS=price_xxx
```

## API Endpoints

- `POST /api/transcribe` — upload WAV and get transcript + keywords
- `POST /api/summarize` — generate summary from transcript text or transcript ID
- `GET /api/history` — fetch user transcript history
- `POST /api/transcribe/bulk` — Business-only bulk upload placeholder endpoint
- `POST /create-checkout-session` — create Stripe checkout session for Pro/Business
- `POST /create-portal-session` — open Stripe Customer Portal for active customer

## Monetization Logic (Implemented)

- Usage tracked on `User.daily_seconds_used` with `usage_reset_date`
- Free plan blocked when projected usage exceeds 600 seconds/day
- Premium-only actions (summarize/download) gated for Pro/Business plans
- Signup starts on Free plan; paid upgrades are completed via Stripe Checkout

## Stripe Customer Portal Setup

1. Open **Stripe Dashboard → Settings → Billing → Customer portal**.
2. Enable features:
   - Subscription cancellation
   - Payment method updates
   - Invoice history
   - Plan switching (optional)
3. Configure your default return URL (e.g. `http://127.0.0.1:5000/dashboard`).
4. Create recurring prices for Pro and Business products and copy `price_...` IDs.
5. Set `STRIPE_SECRET_KEY`, `STRIPE_PRICE_PRO`, `STRIPE_PRICE_BUSINESS` in your environment.
6. In VoiceFlow dashboard, click:
   - **Upgrade to Pro/Business** for checkout
   - **Manage Billing** to open hosted Stripe portal

> Note: Production plan syncing should use Stripe webhooks (`checkout.session.completed`, `customer.subscription.updated`) for reliability.

## Future Scope

- Stripe integration for real subscription billing
- Team workspaces and role management
- Async transcription queue (Celery/RQ)
- Whisper integration for higher-accuracy offline inference
- Analytics dashboard (retention, transcription minutes, ARR)

## Project Structure

```text
voiceflow-ai/
├── app.py
├── models.py
├── database.db
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── dashboard.html
├── static/
│   └── style.css
├── pitch.md
├── requirements.txt
└── README.md
```
