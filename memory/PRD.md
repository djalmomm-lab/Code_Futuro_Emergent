# CodeFuturo — PRD

## Original Problem Statement
Pixel-perfect clone of Coddy.tech focused on coding tracks (Python, JS, HTML, etc.) with the visual identity of "CodeFuturo". Multi-language, LGPD-compliant onboarding (parental consent for <13), Stripe subscription model (monthly/yearly/lifetime), interactive code editor with real Python execution. Frontend React/Tailwind, Backend FastAPI/MongoDB, Pyodide for Python in the browser, Stripe payments, automated lesson content generation via LLM.

User language preference: **Portuguese (pt-BR)**.

## Tech Stack
- Frontend: React, Tailwind CSS, Shadcn UI, Pyodide (CDN), Sonner toasts, Lucide icons.
- Backend: FastAPI, MongoDB (Motor), JWT auth, passlib/bcrypt, reportlab (PDF certs).
- Integrations: Stripe (test mode), Emergent LLM key (GPT for lesson generation, Nano Banana for product image).

## Core Architecture
- `frontend/src/pages/`: Home, Login, Register, Onboard, Dashboard, Lesson, JourneyPage, LeaderboardPage, Catalog, Profile, Plans, PaymentSuccess, **Certificates**.
- `frontend/src/components/`: Navbar, Footer, Paywall, LanguagesSection, etc.
- `backend/server.py`: Auth, onboarding, progress, energy, leaderboard, tracks/paths, lessons, paywall enforcement, **certificates**, LGPD endpoints.
- `backend/subscription_routes.py`: Stripe checkout/portal/webhook.
- `backend/certificates.py`: reportlab-based PDF generator.
- `backend/seed_lessons.py`: LLM-driven lesson seeder.

## DB Collections
- `users` `{id, email, password_hash, name, age, is_pro, plan, tier, stripe_customer_id, subscription_status, subscription_ends_at}`
- `paths` `{slug, name, language, color, desc, total_lessons}`
- `lessons` `{id, slug, path_slug, chapter, order, title, instruction_pt, starter_code, tests, language}`
- `progress` `{user_id, xp_total, streak, energy, level, ...}`
- `lesson_completions` `{user_id, lesson_slug, completed_at}` (unique compound index)
- `payment_transactions` `{user_id, stripe_session_id, amount, status, ...}`

## Paywall Rules
- `FREE_LESSONS_PER_PATH = 3` (first 3 lessons free per track)
- Backend enforces:
  - `GET /api/paths/{slug}` → tags each lesson with `requires_pro` (order > 3 AND not is_pro)
  - `GET /api/lessons/{slug}` → returns minimal payload `{requires_pro: true}` for locked lessons
  - `POST /api/progress/complete` → 402 for locked lessons
- Frontend: `Paywall.jsx` component + lock icons + PRO badges + upgrade banner.

## Certificates (Pro feature)
- `GET /api/certificates` → list of all tracks with completion stats + `is_pro`
- `GET /api/certificates/{path_slug}` → 200 PDF (Pro + completed) | 402 (free) | 403 (incomplete)
- Frontend `/certificados` page with download flow (blob → trigger save).
- Stable cert ID: `CF-` + sha1(user_id:path_slug)[:12]

## Implemented (Changelog)
- 2026-04: CodeFuturo identity, multi-language UI, LGPD onboarding, Stripe subscriptions (checkout + portal + webhooks), 76 lessons across 9 tracks via LLM, Pyodide Python execution, paywall backend.
- **2026-05-01: Paywall frontend (Lesson.jsx, JourneyPage.jsx, Paywall.jsx). Beautiful Pro upgrade modal with 4 benefit bullets, lock icons + PRO pills on locked lessons, contextual upgrade banner on Journey page.**
- **2026-05-01: PDF Certificate generation. Backend `/api/certificates` endpoints with reportlab-rendered A4 landscape PDF. Frontend `/certificados` page with grid + progress bars + download buttons. Navbar dropdown link added.**

## Test Coverage
- Backend regression: `/app/backend/tests/test_paywall_certs.py` (16 cases, 100%).
- E2E frontend: 8/8 flows green via Playwright (anonymous + free + Pro).

## Roadmap

### P1 — Next
- Live code execution / advanced validation for JavaScript and HTML/CSS (currently only Python via Pyodide).
- "Verify certificate" public endpoint (lookup by cert_id) — UI placeholder already mentions `codefuturo.app/verificar`.

### P2 — Later
- B2B "CodeFuturo Escolas" panel (teacher dashboard, classes, bulk invoices).
- Refactor: split `server.py` (~530 lines) into routers under `/app/backend/routes/` (auth, lessons, progress, certificates).
- Wrap `render_certificate` in `asyncio.to_thread` if PDFs grow heavy.
- Cleanup: prune orphan free-test users created during automated tests.

## Critical Info
- Stripe runs in TEST mode with real test keys in `backend/.env`.
- Pro test user (with all Python lessons completed): `cert.test@codefuturo.app / TestPro123!`
- Always speak with the user in Portuguese (pt-BR).
