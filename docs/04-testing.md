# 4. Testing

## 4.1 Testing Strategy
Testing is layered to match the CI pipeline's gates: fast, isolated unit/API
tests run on every commit before any image is built, so a broken change
never reaches a container image.

## 4.2 Backend Test Suite (`backend/tests/test_api.py`)
Runs against an **in-memory SQLite database** (not MySQL) so tests are fast,
require no external services, and are fully reproducible in CI runners.

| Test | Verifies |
|---|---|
| `test_health_check` | `/api/health` returns `200` and `status: ok` |
| `test_register_first_user_becomes_admin` | Registration succeeds and the first user is auto-promoted to `admin` |
| `test_login_and_create_post` | JWT login works and an authenticated admin can create a post |
| `test_list_posts_is_public` | Post listing is accessible without authentication |
| `test_duplicate_registration_fails` | Duplicate username/email is rejected with `400` |
| `test_long_password_is_hashed_without_truncation` | A 186-character passphrase still logs in — passwords are SHA-256 pre-hashed so bcrypt's 72-byte cap never silently truncates |
| `test_passwords_are_not_stored_in_plaintext` | Stored hashes are bcrypt (`$2b$`), never the raw password, and a wrong password does not verify |
| `test_role_permissions_are_enforced` | A `reader` receives `403` when trying to create a post |
| `test_draft_posts_are_hidden_from_public_list` | Unpublished drafts never leak into the public feed |

Current status: **9 passed**.

Run locally:
```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

### 4.2.1 Password hashing note
Passwords are hashed with `bcrypt` used directly (not via `passlib`, which is
unmaintained and breaks against `bcrypt >= 5.x`). Because bcrypt ignores
everything past 72 bytes, the plaintext is first SHA-256 hashed and
base64-encoded, which yields a fixed 44-byte input — so two long passphrases
that share a prefix still produce different hashes instead of colliding.

## 4.3 Manual / Exploratory Test Cases

| # | Scenario | Steps | Expected Result |
|---|---|---|---|
| 1 | Registration | Register a new user | User created, redirected/logged in, role = reader (unless first user) |
| 2 | Login with wrong password | Submit incorrect password | `401 Unauthorized`, error shown in UI |
| 3 | Unauthorized post creation | Reader tries to POST `/api/posts` | `403 Forbidden` |
| 4 | Post ownership | Author A tries to edit Author B's post | `403 Forbidden` (unless requester is admin) |
| 5 | Draft visibility | Create a draft post (published=false) | Not shown in the public post list |
| 6 | Category filter | Filter posts by an existing category slug | Only matching posts returned |
| 7 | Comment as guest | Attempt to comment while logged out | UI prompts login; API returns `401` |
| 8 | Health check under DB outage | Stop the `db` container, hit `/api/health` | Returns `status: ok`, `database: unreachable` (app stays up) |

## 4.4 Container-Level Testing
- **Build test:** `docker compose build` must complete for all three services
  with zero errors.
- **Startup test:** `docker compose up` brings all containers to a healthy
  state (`docker compose ps` shows `healthy` for `db` and `backend`).
- **Integration smoke test:** after `docker compose up`, visiting
  `http://localhost` loads the app, and `http://localhost:8000/api/health`
  reports `database: connected`.

## 4.5 CI Pipeline as a Test Gate
The GitHub Actions pipeline enforces:
1. Lint must pass (backend flake8, frontend ESLint) before tests run.
2. Backend tests (pytest) must pass before any Docker image is built.
3. Frontend must build successfully (`vite build`) before any Docker image is built.
4. Only after both test/build jobs succeed does the pipeline build and push
   Docker images — guaranteeing every pushed image corresponds to a
   passing test run.

## 4.6 Known Limitations
- No automated frontend component tests (e.g., React Testing Library) are
  included in this version — manual test cases above cover the UI instead.
  This is a natural extension for future iterations.
- Load/performance testing was not conducted; NFR3 (~500ms response) was
  observed informally during local development, not benchmarked formally.
- The `deploy` job calls a provider deploy hook, but that hook is not part of
  this repository — it lives in your Render/Railway/Fly account and is reached
  through the `DEPLOY_HOOK_URL` repository secret. With no secret configured
  the job logs a notice and still succeeds, so forks and contributors can
  run the whole pipeline without access to your infrastructure.
- The pipeline pushes to GitHub Container Registry. Image vulnerability
  scanning (e.g. Trivy) is not yet part of the build.
