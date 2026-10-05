# Social Lens — AI-Driven Social Media Analytics Framework

**Organization:** National Technical Research Organisation (NTRO)  
**UI/UX Specification:** Government of India UX4G Design System ([https://ux4g.gov.in/](https://ux4g.gov.in/))  

---

## 📌 Executive Overview

**Social Lens** is an enterprise AI-driven social media analytics platform engineered for multi-platform intelligence ingestion (Telegram, X/Twitter, Instagram, Facebook, Reddit, YouTube). It delivers four real-time intelligence vectors on a single unified dashboard:
1. **Multilingual Sentiment & Shift Detection** (English, Hindi, Hinglish, Sarcasm, Emotions, CUSUM Z-score shift detection).
2. **Demographic Profiling & Privacy** (Age, Geography, Language, Professional Interests, Differential Privacy with <20 bucket suppression).
3. **Trend Detection & Volume Forecasting** (BERTopic clustering, burst detection, growth % ranking, 1-6 hr volume prediction band).
4. **Link Analysis & Virality Time Slider** (Directed interaction graph, Louvain community detection, influence scores 0-100, 12 PM - 4 PM time slider cascade replay).

---

## 🎨 UI/UX & UX4G Design Tokens

The user interface follows the official **UX4G (Government of India)** design system:
- **Primary Navy:** `#002B49`
- **Saffron Accent:** `#FF9933`
- **Green Accent:** `#138808`
- **Background / Surface:** `#F4F6F8` / `#FFFFFF`
- **Accessibility:** High Contrast Mode toggle, WCAG 2.1 AA keyboard navigation, visible focus indicators, skip link, ARIA attributes.
- **Classification Banner:** `RESTRICTED / INTERNAL USE ONLY — GOVT OF INDIA`
- **Formatting:** Indian digit grouping (e.g., `1,24,560` total posts, `38,420` active users).

---

## 🚀 Key System Features

- **Pluggable Connector Architecture:** `TelegramConnector`, `XConnector`, `MetaConnector`, `RedditConnector`, `YouTubeConnector`, `ReplayConnector`.
- **Seeded Dataset:** Pre-loaded with 125,000+ posts, 38,000+ user profiles, 3 viral topics (`AI Regulation`, `New Product`, `Data Privacy`), and top influencers (`User A`, `User B`, `User C`).
- **REST API & Live Socket Stream:** FastAPI-compatible standard endpoints with JWT role-based access control (`admin`, `analyst`, `viewer`).
- **Export Engine:** Formatted CSV and PDF report generation.

---

## 🛠️ Quick Start & Execution

### 1. Run Automated Test Suite (42/42 Tests Pass)
```bash
python3 tests/test_suite.py
```

### 2. Run Demo Script
```bash
./demo_script.sh
```

### 3. Start Backend & Open Web Dashboard
```bash
python3 backend/main.py 8000
```
Then open `http://localhost:8000` or load `frontend/index.html` directly in any standard browser.

---

## 📊 API Endpoints Contract

- `POST /auth/login` — Issue JWT token for roles (`admin`, `analyst`, `viewer`).
- `GET /summary` — KPI summary cards, sentiment split, platform filter.
- `GET /sentiment/timeline` — Polarity time series, emotions, CUSUM shift detection with evidence posts.
- `GET /demographics` — Age, geography, language, interest distributions with bucket suppression.
- `GET /trends` — Topic growth % ranking, burst status, volume forecast band.
- `GET /influencers` — Top ranked users with 0-100 influence score.
- `GET /network` — Directed interaction topology graph, Louvain communities, time slider filter.
- `GET /timeline/{topic_id}` — Chronological event rail with original evidence posts.
- `GET /export?format=csv|pdf` — Download intelligence summary report.
- `GET /health` — Service & connector status report.

---

## 📜 Compliance & Test Report
For full verification details, inspect [TEST_REPORT.md](TEST_REPORT.md) detailing all 42 passed test IDs (A1-A8, B1-B6, C1-C4, D1-D5, E1-E5, U1-U7, S1-S3, P1-P2, X1-X2).
