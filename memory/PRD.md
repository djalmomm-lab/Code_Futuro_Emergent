# CodeFuturo — PRD

## Original Problem Statement
Pixel-perfect clone of Coddy.tech focused on coding tracks (Python, JS, HTML, etc.) with the visual identity of "CodeFuturo". Multi-language, LGPD-compliant onboarding (parental consent for <13), Stripe subscription model (monthly/yearly/lifetime), interactive code editor with real Python execution. Frontend React/Tailwind, Backend FastAPI/MongoDB, Pyodide for Python in the browser, Stripe payments, automated lesson content generation via LLM.

User language preference: **Portuguese (pt-BR)**.

## Tech Stack
- Frontend: React, Tailwind CSS, Shadcn UI, Pyodide (CDN), Sonner toasts, Lucide icons.
- Backend: FastAPI, MongoDB (Motor), JWT auth, passlib/bcrypt, reportlab (PDF certs).
- Integrations: Stripe (test mode), Emergent LLM key (GPT for lesson generation, Nano Banana for product image), LinkedIn share/profile-add (no SDK; URL-based deep links).

## Core Architecture
- `frontend/src/pages/`: Home, Login, Register, Onboard, Dashboard, Lesson, JourneyPage, LeaderboardPage, Catalog, Profile, Plans, PaymentSuccess, Certificates, VerifyCertificate, **Schools, ClassDetail**.
- `frontend/src/components/`: Navbar, Footer, Paywall, UpgradeCelebration, LanguagesSection, etc.
- `frontend/src/lib/runners.js`: JS sandbox runner + HTML preview/normalization.
- `backend/server.py`: Auth, onboarding, progress, energy, leaderboard, tracks/paths, lessons, paywall enforcement, certificates, public verify endpoint, LGPD endpoints.
- **`backend/classes_routes.py`: B2B Escolas — create/list/join/detail/remove/delete classes.**
- `backend/subscription_routes.py`: Stripe checkout/portal/webhook.
- `backend/certificates.py`: reportlab-based PDF generator (rendered via `asyncio.to_thread`).
- `backend/seed_lessons.py`: LLM-driven lesson seeder.

## DB Collections
- `users`, `paths`, `lessons`, `progress`, `lesson_completions`, `payment_transactions`, `profiles`, `certificates`,
- **`classes` `{id, slug, name, school_name, owner_id, invite_code (unique), seats, created_at}`**
- **`class_memberships` `{id, class_id, user_id, role: 'teacher'|'student', joined_at}` (compound unique on class_id+user_id)**

## Paywall, Conversion Popup, Live Execution, Certificates, Public Verify
(Same as iteration 2 — see prior changelog.)

## CodeFuturo Escolas (B2B) — NEW
Any authenticated user can create a class (becomes teacher). Students join via 6-character invite code (omits look-alikes O/0/I/1).
- **Endpoints (`/api/classes`)**: `POST /` (create), `GET /mine` (list), `POST /join`, `GET /{id}`, `DELETE /{id}/students/{user_id}`, `DELETE /{id}`.
- **Teacher dashboard** (`/escolas/{id}`): invite code with copy button, full students table with progress bars, XP, streak, and remove-student / delete-class actions.
- **Student view**: confirms membership, CTA to `/catalogo`.
- Seat enforcement on join (`409 Conflict` when full); idempotent re-join.

## LinkedIn Integration (URL-based, no API key)
- **Add to LinkedIn profile** button (rich): builds the LinkedIn `profile/add?startTask=CERTIFICATION_NAME&...` URL with name, organizationName=CodeFuturo, issueYear/Month, certUrl=`/verificar/{cert_id}`, certId.
- **Share post** button: standard `linkedin.com/sharing/share-offsite/?url=...`.
- **Copy link** button: clipboard.
- Surfaces: `/verificar/:certId` card and `/certificados` list (only when cert is ready).

## Implemented (Changelog)
- 2026-04: CodeFuturo identity, multi-language UI, LGPD onboarding, Stripe subscriptions, 76 lessons via LLM, Pyodide Python execution, paywall backend.
- 2026-05-01 (am): Paywall frontend, PDF certificates backend + `/certificados` page.
- 2026-05-01 (pm-1): UpgradeCelebration popup, JS live exec + HTML preview, public `/api/verify/{cert_id}` + `/verificar` page, cert auto-issuance on track completion.
- **2026-05-01 (pm-2): CodeFuturo Escolas (full B2B classroom layer). LinkedIn add-to-profile + share-post + copy-link buttons on verified cert + cert list. `cert_id` exposed in `/api/certificates`. PDF rendering wrapped in `asyncio.to_thread`.**

## Test Coverage
- Backend regression: 36/36 (17 classes + 16 paywall/cert + 3 verify).
- Frontend e2e: 100% on all critical flows across 3 iterations.

## Roadmap

### P2 — Remaining
- Refactor: split `server.py` (~593 lines) into routers under `/app/backend/routes/` (auth, lessons, progress, certificates, verify) — `classes_routes.py` already followed the pattern.
- Production hardening: pin `runJavaScript` postMessage origin; explicit allow-list projection on verify response.
- Cleanup: prune orphan free-test users created during automated tests.

### P3 (new ideas)
- Class bulk invoicing / Stripe Connect for schools.
- Aggregate `_student_progress_summary` into a single `$lookup` pipeline (perf at scale).
- LinkedIn deep-share for completing each chapter (not just full track).
- Inline form errors (a11y) in addition to toasts in the Schools modals.

## Critical Info
- Stripe runs in TEST mode with real test keys in `backend/.env`.
- Pro test user (also owner of "Turma 8A"): `cert.test@codefuturo.app / TestPro123!` (invite code `8H4M5J`).
- Student test user: `aluno.teste@cf.app / Aluno12345!` (member of Turma 8A).
- Public verify URL example: `/verificar/CF-FD26B52ECDE6`.
- Always speak with the user in Portuguese (pt-BR).
