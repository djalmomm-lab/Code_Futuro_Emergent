# CodeFuturo — PRD

## Original Problem Statement
Pixel-perfect clone of Coddy.tech focused on coding tracks (Python, JS, HTML, etc.) with the visual identity of "CodeFuturo". Multi-language, LGPD-compliant onboarding (parental consent for <13), Stripe subscription model (monthly/yearly/lifetime), interactive code editor with real Python execution. Frontend React/Tailwind, Backend FastAPI/MongoDB, Pyodide for Python in the browser, Stripe payments, automated lesson content generation via LLM.

User language preference: **Portuguese (pt-BR)**.

## Tech Stack
- Frontend: React, Tailwind CSS, Shadcn UI, Pyodide (CDN), Sonner toasts, Lucide icons.
- Backend: FastAPI, MongoDB (Motor), JWT auth, passlib/bcrypt, reportlab (PDF certs).
- Integrations: Stripe (test mode), Emergent LLM key (GPT for lesson generation, Nano Banana for product image).

## Core Architecture
- `frontend/src/pages/`: Home, Login, Register, Onboard, Dashboard, Lesson, JourneyPage, LeaderboardPage, Catalog, Profile, Plans, PaymentSuccess, Certificates, **VerifyCertificate**.
- `frontend/src/components/`: Navbar, Footer, Paywall, **UpgradeCelebration**, LanguagesSection, etc.
- `frontend/src/lib/runners.js`: JS sandbox runner + HTML preview/normalization.
- `backend/server.py`: Auth, onboarding, progress, energy, leaderboard, tracks/paths, lessons, paywall enforcement, certificates, **public verify endpoint**, LGPD endpoints.
- `backend/subscription_routes.py`: Stripe checkout/portal/webhook.
- `backend/certificates.py`: reportlab-based PDF generator.
- `backend/seed_lessons.py`: LLM-driven lesson seeder.

## DB Collections
- `users`, `paths`, `lessons`, `progress`, `lesson_completions`, `payment_transactions`, `profiles`,
- **`certificates` `{cert_id (unique), user_id, path_slug, track_name, student_name, total_lessons, xp_earned, issued_at}`** — issued idempotently on track completion (Pro users).

## Paywall Rules
- `FREE_LESSONS_PER_PATH = 3`. Backend enforces in `/api/paths/{slug}`, `/api/lessons/{slug}`, `/api/progress/complete`.
- Frontend: `Paywall.jsx` modal + lock icons + PRO badges + Journey upgrade banner.

## Conversion Popup (UpgradeCelebration)
- Triggered when an authenticated **non-Pro** user completes the **3rd** (last free) lesson of any track.
- Celebrates the milestone, previews 4 of the upcoming locked lessons, offers Pro CTA.
- Suppressed for Pro users and skipped on idempotent re-completes.

## Certificates (Pro feature)
- `GET /api/certificates` → list of all tracks with completion stats + `is_pro`
- `GET /api/certificates/{path_slug}` → 200 PDF (Pro + completed) | 402 (free) | 403 (incomplete)
- **`GET /api/verify/{cert_id}` → 200 public verification** (no auth) | 404 if invalid.
- Certificate auto-issued on `/api/progress/complete` when Pro user finishes the last lesson — verifiable instantly without needing to download.
- Stable cert ID: `CF-` + sha1(user_id:path_slug)[:12].
- Frontend pages: `/certificados` (private, listing + download) and `/verificar`, `/verificar/:certId` (public).

## Live Code Execution
- **Python**: Pyodide WASM in browser (real exec).
- **JavaScript**: sandboxed iframe + postMessage capture of `console.log` (`runJavaScript()`).
- **HTML/CSS**: live iframe preview pane with normalized HTML comparison for tests.
- Other languages (SQL, TS, Java, etc.): textual validation mode (fallback).

## Implemented (Changelog)
- 2026-04: CodeFuturo identity, multi-language UI, LGPD onboarding, Stripe subscriptions (checkout + portal + webhooks), 76 lessons across 9 tracks via LLM, Pyodide Python execution, paywall backend.
- 2026-05-01: Paywall frontend (Lesson.jsx, JourneyPage.jsx, Paywall.jsx).
- 2026-05-01: PDF Certificate generation. Backend `/api/certificates` endpoints + frontend `/certificados`.
- **2026-05-01 (later): UpgradeCelebration popup. JS live execution + HTML preview pane in Lesson page. Public certificate verification endpoint `/api/verify/{cert_id}` + page `/verificar/:certId`. Auto-issuance of cert on track completion.**

## Test Coverage
- Backend regression: `/app/backend/tests/test_paywall_certs.py` + `test_verify_endpoint.py` (**19/19 100%**).
- E2E frontend: 4/4 new flows + 8/8 paywall flows green via Playwright.

## Roadmap

### P1 — Next
- (none of the original P1 items remain; all delivered)
- Bonus polish: cert auto-issue confirmation toast in Lesson page when track is fully completed.

### P2 — Later
- B2B "CodeFuturo Escolas" panel (teacher dashboard, classes, bulk invoices).
- Refactor: split `server.py` (~580 lines) into routers under `/app/backend/routes/` (auth, lessons, progress, certificates, verify).
- Wrap `render_certificate` in `asyncio.to_thread` if PDFs grow heavy.
- Production hardening: pin postMessage origin in `runJavaScript`, switch to allow-list projection on verify response.
- Cleanup: prune orphan free-test users created during automated tests.

## Critical Info
- Stripe runs in TEST mode with real test keys in `backend/.env`.
- Pro test user (with all Python lessons completed): `cert.test@codefuturo.app / TestPro123!`
- Public verify URL example: `/verificar/CF-FD26B52ECDE6`
- Always speak with the user in Portuguese (pt-BR).
