"""
Basic API test suite. Runs against an in-memory SQLite DB so it
needs no external database - this is what the CI pipeline's
'test' stage executes before building/pushing any image.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine, StaticPool  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# The client is instantiated without a `with` block, so Starlette never fires
# the lifespan handler -- meaning the real MySQL DB-retry boot hook is skipped
# and the in-memory SQLite schema created above is used as-is.
client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_first_user_becomes_admin():
    response = client.post(
        "/api/auth/register",
        json={"username": "admin1", "email": "admin1@example.com", "password": "supersecret"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "admin1"
    assert data["role"] == "admin"


def test_login_and_create_post():
    login = client.post(
        "/api/auth/login", json={"username": "admin1", "password": "supersecret"}
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    response = client.post(
        "/api/posts",
        json={"title": "Hello World", "content": "My first post", "published": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Hello World"


def test_list_posts_is_public():
    response = client.get("/api/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_duplicate_registration_fails():
    response = client.post(
        "/api/auth/register",
        json={"username": "admin1", "email": "admin1@example.com", "password": "supersecret"},
    )
    assert response.status_code == 400


def test_long_password_is_hashed_without_truncation():
    """bcrypt caps input at 72 bytes; we pre-hash so long passphrases still work."""
    long_password = "correct-horse-battery-staple-" * 6  # 186 chars, well over 72
    assert len(long_password) > 72

    register = client.post(
        "/api/auth/register",
        json={"username": "longpw", "email": "longpw@example.com", "password": long_password},
    )
    assert register.status_code == 201

    login = client.post(
        "/api/auth/login", json={"username": "longpw", "password": long_password}
    )
    assert login.status_code == 200

    wrong = client.post(
        "/api/auth/login",
        json={"username": "longpw", "password": long_password[:-1] + "X"},
    )
    assert wrong.status_code == 401


def test_passwords_are_not_stored_in_plaintext():
    """NFR2 - verify bcrypt (never plain text) is what lands in the DB."""
    from app import auth as auth_module

    hashed = auth_module.get_password_hash("supersecret")
    assert hashed != "supersecret"
    assert hashed.startswith("$2b$")
    assert auth_module.verify_password("supersecret", hashed)
    assert not auth_module.verify_password("wrongpassword", hashed)


def test_role_permissions_are_enforced():
    """A reader must not be able to create posts (403)."""
    client.post(
        "/api/auth/register",
        json={"username": "reader1", "email": "reader1@example.com", "password": "supersecret"},
    )
    login = client.post(
        "/api/auth/login", json={"username": "reader1", "password": "supersecret"}
    )
    token = login.json()["access_token"]

    response = client.post(
        "/api/posts",
        json={"title": "Reader Post", "content": "should be rejected", "published": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_draft_posts_are_hidden_from_public_list():
    """FR-drafts - unpublished posts must not appear in the public feed."""
    login = client.post(
        "/api/auth/login", json={"username": "admin1", "password": "supersecret"}
    )
    token = login.json()["access_token"]

    client.post(
        "/api/posts",
        json={"title": "Secret Draft", "content": "not public yet", "published": False},
        headers={"Authorization": f"Bearer {token}"},
    )

    public = client.get("/api/posts")
    assert public.status_code == 200
    assert all(p["title"] != "Secret Draft" for p in public.json())
