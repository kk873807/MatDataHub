"""
MatDataHub API — Main application entry point.
Run with:
    uvicorn app.main:app --reload
Then open:
    http://127.0.0.1:8000        -> Welcome message
    http://127.0.0.1:8000/docs   -> Interactive API documentation (Swagger UI)
"""
import os
import sys
import threading

# Fix for "python app/main.py" causing ModuleNotFoundError
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("--- APP MODULE LOADING ---", flush=True)

from fastapi import FastAPI, Request, Depends, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.database import engine, Base, get_db
from app.auth import get_current_user
from app.models import User
from sqlalchemy.orm import Session

print("--- IMPORTS COMPLETE ---", flush=True)

# ── Track DB readiness & keep-alive (used by /health) ─────────────
import time as _time
from sqlalchemy import text as _sql_text

_db_ready = False
_db_error: str | None = None
_last_db_ping_ts: float = 0.0
_MIN_DB_PING_INTERVAL: float = 60.0  # At most 1 real SELECT 1 query per 60 seconds
_ping_lock = threading.Lock()


def _ping_db(force: bool = False) -> bool:
    """Execute a lightweight SELECT 1 query so Supabase registers active DB traffic
    and never auto-pauses on the free tier. Throttled to at most once per 60s
    so public callers of /health?ping_db=true cannot hammer the database."""
    global _db_ready, _db_error, _last_db_ping_ts
    now = _time.time()
    if not force and _db_ready and (now - _last_db_ping_ts) < _MIN_DB_PING_INTERVAL:
        return True
    with _ping_lock:
        now = _time.time()
        if not force and _db_ready and (now - _last_db_ping_ts) < _MIN_DB_PING_INTERVAL:
            return True
        try:
            with engine.connect() as conn:
                conn.execute(_sql_text("SELECT 1"))
            _db_ready = True
            _db_error = None
            _last_db_ping_ts = _time.time()
            return True
        except Exception as e:
            _db_error = str(e)
            return False


def _init_db():
    """Run DB table creation in a background thread so it never blocks
    Uvicorn from binding the port.  Render's health-check sees the open
    port immediately and marks the deploy as successful."""
    global _db_ready, _db_error, _last_db_ping_ts
    for attempt in range(1, 4):
        try:
            print(f"Background thread: connecting to DB and creating tables (attempt {attempt}/3)...", flush=True)
            Base.metadata.create_all(bind=engine)
            _db_ready = True
            _db_error = None
            _last_db_ping_ts = _time.time()
            print("Background thread: tables created successfully.", flush=True)
            return
        except Exception as e:
            _db_error = str(e)
            print(f"Background thread: DB init error (attempt {attempt}/3): {e}", file=sys.stderr, flush=True)
            if attempt < 3:
                _time.sleep(2 * attempt)


# ── Build the FastAPI app ─────────────────────────────────────────
app = FastAPI(
    title="MatDataHub API",
    description="Engineering Material Data API - Search, filter, and compare 1000+ engineering materials.",
    version="2.0.0",
    contact={"name": "MatDataHub"},
)


@app.on_event("startup")
def startup_event():
    """Fire-and-forget DB init so the ASGI server can start accepting
    connections without waiting for a potentially slow remote DB."""
    print("--- STARTUP EVENT: launching DB init thread ---", flush=True)
    threading.Thread(target=_init_db, daemon=True).start()


# ── Rate limiting & DB error handling ─────────────────────────────
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

limiter = Limiter(key_func=get_remote_address, default_limits=["2000/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(OperationalError)
async def db_operational_error_handler(request: Request, exc: OperationalError):
    """Return a handled 503 so CORSMiddleware attaches Access-Control-Allow-Origin headers
    instead of letting an unhandled 500 trigger browser TypeError: Failed to fetch."""
    return JSONResponse(
        status_code=503,
        content={"detail": "Database is temporarily unavailable. Please check that the Supabase instance is active."},
    )


# ── Register route modules ────────────────────────────────────────
from app.routers import materials, auth, admin, feedback, payments, ai, projects, account, calculators, blogs

app.include_router(materials.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(feedback.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(account.router, prefix="/api/v1")
app.include_router(calculators.router, prefix="/api/v1")
app.include_router(blogs.router, prefix="/api/v1")


# ── Middleware ─────────────────────────────────────────────────────
_DEV_SESSION_SECRET = "super-secret-oauth-key-change-me"
_session_secret = os.environ.get("OAUTH_SESSION_SECRET", _DEV_SESSION_SECRET)
if os.environ.get("RENDER") and _session_secret == _DEV_SESSION_SECRET:
    # Refuse to start in production with a publicly known signing secret.
    raise RuntimeError("OAUTH_SESSION_SECRET is not set; refusing to start with the development default.")
app.add_middleware(
    SessionMiddleware,
    secret_key=_session_secret,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "https://matdatahub.com",
        "https://www.matdatahub.com",
        "https://mat-data-hub.vercel.app",
        *([os.environ["FRONTEND_URL"].rstrip("/")] if os.environ.get("FRONTEND_URL") else []),
        *[o.strip() for o in os.environ.get("CORS_EXTRA_ORIGINS", "").split(",") if o.strip()],
    ],
    # The old pattern r"https://.*\.vercel\.app" allowed credentialed requests from ANY site hosted on Vercel.
    # Preview deployments are opt-in: set CORS_ALLOW_ORIGIN_REGEX to a pattern you control.
    allow_origin_regex=os.environ.get("CORS_ALLOW_ORIGIN_REGEX") or None,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-CBAM-Defaults-Count", "X-CBAM-Defaults-Version", "X-CBAM-History-Saved", "X-CBAM-Mode", "X-CBAM-Reference-Price", "Content-Disposition"],
)

# Custom Middleware for Security Headers (Gap 2)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"
    return response


# ── Core endpoints ────────────────────────────────────────────────
@app.get("/")
def root():
    """Health check / welcome endpoint."""
    return {
        "app": "MatDataHub API",
        "version": "2.0.0",
        "docs": "/docs",
        "status": "running",
        "db_ready": _db_ready,
    }


@app.get("/health")
def health(ping_db: bool = False):
    """Detailed health check for monitoring, Render zero-downtime deploys, and Supabase keep-alive."""
    now = _time.time()
    if ping_db or (not _db_ready and _last_db_ping_ts > 0) or (now - _last_db_ping_ts > 3600):
        _ping_db()
    return {
        "status": "healthy",
        "db_ready": _db_ready,
        "db_error": bool(_db_error),   # detail is in the server log, not in a public response
    }


# ── Seed endpoints (admin-only, no SSH on Render) ─────────────────
def _require_admin(user: User):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required.")


@app.get("/api/v1/admin/seed-demo")
def seed_demo_data(current_user: User = Depends(get_current_user)):
    """Seed the demo materials. Admin only (this endpoint used to be callable by anyone)."""
    _require_admin(current_user)
    try:
        from scripts.seed_professor_materials import run_seed
        added = run_seed()
        return {"ok": True, "message": f"Successfully seeded {added} materials for the demo!"}
    except Exception as e:
        print(f"seed-demo failed: {e}", file=sys.stderr, flush=True)
        return {"ok": False, "error": "Seeding failed; see server logs."}


@app.get("/api/v1/admin/seed-aa1000")
def seed_aa1000_data(current_user: User = Depends(get_current_user)):
    """Seed the AA 1000 series. Admin only."""
    _require_admin(current_user)
    try:
        from scripts.seed_aa1000_series import run_seed
        added = run_seed()
        return {"ok": True, "message": f"Successfully seeded {added} AA 1000 series materials!"}
    except Exception as e:
        print(f"seed-aa1000 failed: {e}", file=sys.stderr, flush=True)
        return {"ok": False, "error": "Seeding failed; see server logs."}


print("--- APP MODULE LOADED ---", flush=True)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
