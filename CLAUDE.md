# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

DrobnaPomoc.pl — a university (PZSP2) web platform for ordering small local services (shopping, minor repairs, dog walking, etc.), aimed mainly at seniors and people ordering on behalf of relatives. Requirements, glossary (zlecenie, oferta, zleceniodawca, wykonawca, konsultant…) and use cases are in Polish in [docs/dokumentacja.md](docs/dokumentacja.md). User-facing UI text and many log messages are in Polish.

Monorepo: `backend/` (Django + DRF, Python 3.13, managed with `uv`) and `frontend/` (React 19 + Vite, plain JSX, no TypeScript), PostgreSQL 15.

## Commands

Full stack (Postgres + backend on :8000 + frontend on :5173, both with source mounted for live reload):
```
docker compose up --build
```

Backend (run from `backend/`; needs a running Postgres — copy `.env.example` to `.env`, it is loaded by `config/settings.py`):
```
uv sync --dev
uv run python manage.py migrate
uv run python manage.py runserver
uv run python manage.py test                                   # all tests
uv run python manage.py test accounts.tests.AccountsApiTests.test_register   # single test
uv run black .            # format (CI runs black --check)
uv run ruff check .       # lint (rules E4,E7,E9,F,I — includes import sorting)
uv run python manage.py makemigrations   # CI fails if models change without a migration
```
There is no SQLite fallback — tests also require Postgres.

Frontend (run from `frontend/`):
```
npm ci
npm run dev          # Vite dev server, proxies /api -> VITE_PROXY_TARGET (default http://localhost:8000)
npm run lint
npm test             # vitest run (jsdom)
npx vitest run src/features/home/pages/HomePage.test.jsx   # single test file
npm run build
npm run format       # prettier: 4-space indent, double quotes, semicolons, no trailing commas, width 100
```

CI (`.github/workflows/`) runs black/ruff/makemigrations --check/tests for the backend, lint/test/build for the frontend, plus CodeQL, gitleaks and a dependency audit.

## Architecture

**Backend.** `config/` is the Django project; domain code lives in apps:
- `accounts` — custom `AUTH_USER_MODEL = "accounts.User"` (`AbstractUser` with unique email), JWT auth and password management.
- `orders` — `ServiceCategory` (seeded with 6 default categories via data migration) and `Order` (statuses, channels, address split into fields with `city` as the only pre-acceptance location field, optional photo under `MEDIA_URL`/`MEDIA_ROOT`, and recipient consent DB constraint).
- `offers` — `Offer` (positive price check, at most one `ACCEPTED` offer per order and one non-withdrawn offer per contractor/order) and `Visit` (auto-generated 4-digit code via `secrets`, `cancel_reason` required when `CANCELLED`, timestamp ordering check, at most one active visit per offer).

DRF defaults are JWT auth (simplejwt) and `IsAuthenticated` for every view — public endpoints must explicitly set `permission_classes = [AllowAny]`. Rate limiting uses `ScopedRateThrottle` with scopes defined in `REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]`; tests call `cache.clear()` in `setUp` to reset throttles. Refresh tokens rotate and are blacklisted after rotation/logout (`token_blacklist` app).

API routes: `/api/token/`, `/api/token/refresh/`, `/api/token/verify/` (simplejwt), and `/api/accounts/{register,login,logout,me,change-password}/`. Login returns `{access, refresh}`; logout blacklists the posted refresh token.

**Frontend.** Feature-sliced layout under `src/`: `app/` (root `App`), `features/<name>/{api,components,pages}`, `layouts/`, `shared/` (axios client, common components), `styles/`. There is no router yet — `App.jsx` renders `AuthPage` or `AppLayout`+`HomePage` based on `useAuth().isAuthenticated`.

Auth flow: `shared/api/api.js` is a single axios instance with `baseURL = VITE_API_URL || "/api"`. A request interceptor attaches `accessToken` from `localStorage`; a response interceptor on 401 calls `/token/refresh/` once (via a separate axios instance), stores the rotated tokens and retries, or clears tokens on failure. `features/auth/AuthContext.jsx` (`AuthProvider`) restores the session on mount via `/accounts/me/`, and exposes `login`/`register`/`logout`; consume it with `useAuth()`. The context object lives in `context.js` and the hook in `useAuth.js`, separate from the provider component.
