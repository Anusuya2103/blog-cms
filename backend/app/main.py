import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.database import Base, engine
from app import schemas
from app.routers import auth, posts, categories, comments


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create tables once the DB is reachable (MySQL needs a moment on boot).
    init_db_with_retry()
    yield


app = FastAPI(
    title="Blog CMS API",
    description="A DevOps-ready full-stack Blog / CMS backend built with FastAPI, MySQL and JWT auth.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production via env-based allow-list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(categories.router)
app.include_router(comments.router)


def init_db_with_retry(retries: int = 10, delay: int = 3):
    """Wait for the DB container to be ready before creating tables."""
    for attempt in range(1, retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            if attempt == retries:
                raise
            time.sleep(delay)


@app.get("/api/health", response_model=schemas.HealthOut, tags=["Health"])
def health_check():
    db_status = "unknown"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "unreachable"
    return schemas.HealthOut(status="ok", database=db_status)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Blog CMS API is running. See /docs for the OpenAPI UI."}
