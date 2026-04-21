# CodeFuturo — Backend Integration Contracts

## Stack
- FastAPI (Python) + Motor (async MongoDB driver)
- JWT auth (python-jose) + bcrypt (passlib) for password hashing
- All routes prefixed with `/api` per ingress rules

## Collections (MongoDB)

### users
```
{
  _id: UUID,
  email: str (unique),
  password_hash: str,
  name: str,
  created_at: ISO datetime
}
```

### profiles
```
{
  _id: UUID,
  user_id: UUID (FK users),
  birth_date: str (YYYY-MM-DD),
  age: int,
  parent_name: str | null,
  parent_email: str | null,
  consent_data: bool | null,      # LGPD mandatory for <13
  consent_comm: bool | null,      # LGPD optional
  consent_ip: str | null,         # for audit
  consent_at: ISO | null,
  interest: str,
  diagnostic_score: int,
  recommendation: { type: 'module'|'track', id: str, reason: str },
  onboarded_at: ISO
}
```

### progress
```
{
  _id: UUID,
  user_id: UUID (unique),
  xp_total: int,
  xp_today: int,
  daily_goal: int,
  level: int,
  streak: int,
  last_streak_date: str (YYYY-MM-DD),
  energy: int,
  max_energy: int,
  last_energy_reset: ISO,
  tokens: int,
  updated_at: ISO
}
```

### lesson_completions
```
{
  _id: UUID,
  user_id: UUID,
  lesson_slug: str,
  path_slug: str,
  xp_earned: int,
  completed_at: ISO
}
```

## Endpoints

### Auth
- `POST /api/auth/register` → body: `{email, password, name}` → returns `{token, user}`
- `POST /api/auth/login` → body: `{email, password}` → returns `{token, user}`
- `GET /api/auth/me` (auth) → returns `{user, profile, progress}`

### Onboarding
- `POST /api/onboard` (auth) → body: full profile incl. consent → creates profile + initial progress

### Progress
- `GET /api/progress` (auth) → returns current stats
- `POST /api/progress/complete` (auth) → body: `{lesson_slug, path_slug}` → awards XP, updates streak, returns updated progress
- `POST /api/energy/consume` (auth) → decrements energy, returns new value

### Leaderboard
- `GET /api/leaderboard?period=week` → returns top 20 users by XP

### Tracks (public, seed data)
- `GET /api/tracks` → returns list of all tracks/modules

## Frontend integration
- Replace `localStorage.setItem('cf_user')` with real API calls in:
  - `Login.jsx` → POST /api/auth/login → save token
  - `Register.jsx` → POST /api/auth/register → save token
  - `Onboard.jsx` → POST /api/onboard with full profile
  - `Dashboard.jsx` → GET /api/auth/me for user+progress
  - `Lesson.jsx` → POST /api/progress/complete when all tests pass
  - `LeaderboardPage.jsx` → GET /api/leaderboard

- Create `src/lib/api.js` axios instance with `Authorization: Bearer <token>` interceptor
- Store token in `localStorage.cf_token`

## Business rules
- Streak: increment only once per day, reset if missed (unless streak freeze)
- XP per lesson: 50 XP (can vary per lesson later)
- Daily energy: 5 for free users, resets every 24h
- LGPD: consent + IP + timestamp stored for audit; mandatory for <13
- Passwords: bcrypt, min 8 chars
- JWT: 7-day expiry, HS256
