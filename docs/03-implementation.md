# 3. Implementation

## 3.1 Backend Implementation
- **Framework:** FastAPI, organized into routers (`auth`, `posts`,
  `categories`, `comments`) mounted on a single `FastAPI()` app in `main.py`.
- **ORM:** SQLAlchemy models (`models.py`) define `User`, `Post`, `Category`,
  `Comment`, and the `post_category` association table for the many-to-many
  relationship.
- **Validation:** Pydantic schemas (`schemas.py`) separate input models
  (`*Create`, `*Update`) from output models (`*Out`), so internal fields
  (like `hashed_password`) are never serialized in responses.
- **Auth:** `auth.py` implements password hashing (bcrypt), JWT issuance and
  verification, and two dependency helpers — `get_current_user` and
  `require_role(*roles)` — used throughout the routers to enforce access
  control declaratively.
- **Startup resilience:** `init_db_with_retry()` retries table creation for
  up to 30 seconds, because in Docker Compose the backend container can
  start before MySQL finishes initializing.

## 3.2 Frontend Implementation
- **Framework:** React 18 with Vite for fast builds and HMR during development.
- **Routing:** `react-router-dom` with a `ProtectedRoute` wrapper that
  redirects unauthenticated users and enforces role checks for the post
  editor routes.
- **State:** `AuthContext` (React Context) holds the current user and token,
  persisted in `localStorage`, and exposes `login`/`register`/`logout`.
- **API layer:** a single Axios instance (`api/client.js`) attaches the JWT
  bearer token to every outgoing request via an interceptor.
- **Pages:** `Home` (listing + search/filter), `Login`, `Register`,
  `PostDetail` (with comments), `PostEditor` (shared create/edit form).

## 3.3 Containerization
- **Backend Dockerfile:** installs system build dependencies for
  `mysqlclient`/`cryptography`, installs pinned Python dependencies, copies
  the app, creates and switches to a non-root `appuser`, and defines a
  `HEALTHCHECK` against `/api/health`.
- **Frontend Dockerfile:** two-stage build — `node:20-alpine` compiles the
  Vite production bundle, then `nginx:1.27-alpine` serves the static files
  and proxies `/api/*` to the backend container by its Compose service name
  (`backend`), so no hard-coded IPs or ports are needed.

## 3.4 Orchestration
- `docker-compose.yml` wires together `db`, `backend`, and `frontend` on a
  shared bridge network (`blog-net`), with `depends_on: condition:
  service_healthy` so the backend waits for MySQL's health check to pass
  before starting.
- `docker-compose.dev.yml` is an optional override that mounts source
  directories as volumes and runs the dev servers (`uvicorn --reload`,
  `npm run dev`) for fast local iteration without rebuilding images.

## 3.5 Version Control Strategy
- `main` branch is the deployable branch; the CI/CD pipeline triggers on
  every push and pull request targeting it.
- Feature work should branch off `main` and merge via pull request, so the
  lint/test stages run as a gate before merge (recommended, not enforced by
  this template — enable branch protection rules in GitHub repo settings to
  require the CI checks to pass before merging).

## 3.6 Configuration Management
- All secrets/config (DB credentials, JWT secret) are injected via
  environment variables, never hard-coded — following the twelve-factor app
  principle of config/code separation.
- `.env.example` files document required variables without exposing real
  secrets in version control.
