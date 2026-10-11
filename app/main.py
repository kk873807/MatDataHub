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

# ── Track DB readiness (used by /health) ──────────────────────────
_db_ready = False
_db_error: str | None = None


def _init_db():
    """Run DB table creation in a background thread so it never blocks
    Uvicorn from binding the port.  Render's health-check sees the open
    port immediately and marks the deploy as successful."""
    global _db_ready, _db_error
    try:
        print("Background thread: connecting to DB and creating tables...", flush=True)
        Base.metadata.create_all(bind=engine)
        _db_ready = True
        print("Background thread: tables created successfully.", flush=True)
    except Exception as e:
        _db_error = str(e)
        print(f"Background thread: DB init error: {e}", file=sys.stderr, flush=True)


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
    t = threading.Thread(target=_init_db, daemon=True)
    t.start()


# ── Rate limiting ─────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address, default_limits=["2000/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


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
def health():
    """Detailed health check for monitoring and Render zero-downtime deploys."""
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
