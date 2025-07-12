# TIMEPUSH API

A production-ready FastAPI backend for the TimePush platform, supporting manual and OAuth (Google, Facebook) authentication, JWT access tokens, and secure refresh tokens via HTTP-only cookies.

## Features

- FastAPI + async PostgreSQL (psycopg)
- User signup/login (manual, Google, Facebook)
- JWT access tokens for authentication
- Secure refresh token flow using HTTP-only cookies
- Modular code structure (features/auth, features/users, etc.)
- CORS enabled for frontend integration

## Endpoints

### Auth

- `POST /auth/signup` — Manual signup
- `POST /auth/login` — Manual login (returns JWT, sets refresh cookie)
- `POST /auth/oauth` — Google/Facebook login/signup (returns JWT, sets refresh cookie)
- `POST /auth/refresh` — Get new JWT using refresh cookie

## Auth Flow

1. **Login/Signup:**
   - On success, backend returns JWT access token and sets refresh token as HTTP-only cookie.
2. **Frontend:**
   - Store access token in memory (not localStorage).
   - On page reload or token expiry, call `/auth/refresh` (browser sends cookie automatically).
   - Use new access token for API requests.

## Setup

1. **Install dependencies:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. **Configure environment:**
   - Set environment variables (see docker-compose.yml for required keys).
3. **Start the server (local):**
   ```sh
   uvicorn app.main:app --reload
   ```
4. **Start with Docker Compose (production):**
   ```sh
   docker compose --env-file .env up -d
   ```
