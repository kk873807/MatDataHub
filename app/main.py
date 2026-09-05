"""
MatDataHub API â€” Main application entry point.
Run with:
    uvicorn app.main:app --reload
Then open:
    http://127.0.0.1:8000        -> Welcome message
    http://127.0.0.1:8000/docs   -> Interactive API documentation (Swagger UI)
"""
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.database import engine, Base
from app.routers import materials, auth, admin, feedback, payments, ai, projects, account, calculators
from sqlalchemy.orm import Session
from app.database import get_db   # <-- added payments


# Create tables on startup (safe to call multiple times)
Base.metadata.create_all(bind=engine)

# Quick and dirty auto-migration for MVP
from sqlalchemy import text
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN is_blocked BOOLEAN DEFAULT FALSE;"))
        conn.commit()
    except Exception:
        conn.rollback() # Clear the aborted transaction state
        
    try:
        conn.execute(text("ALTER TABLE projects ADD COLUMN blueprint_data TEXT;"))
        conn.commit()
    except Exception:
        conn.rollback()
        
    try:
        conn.execute(text("ALTER TABLE feedback ADD COLUMN helpful_votes INTEGER DEFAULT 0;"))
        conn.commit()
    except Exception:
        conn.rollback()
        
    try:
        conn.execute(text("ALTER TABLE feedback ADD COLUMN parent_id INTEGER REFERENCES feedback(id);"))
        conn.commit()
    except Exception:
        conn.rollback()

    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN auth_provider VARCHAR(50) DEFAULT 'email' NOT NULL;"))
        conn.commit()
    except Exception:
        conn.rollback()

    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN provider_id VARCHAR(255);"))
        conn.commit()
    except Exception:
        conn.rollback()

    try:
        # Create transactions table manually if Base.metadata.create_all doesn't catch it
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount FLOAT NOT NULL,
            currency VARCHAR(10) DEFAULT 'INR',
            tier_purchased VARCHAR(50) NOT NULL,
            status VARCHAR(20) DEFAULT 'completed',
            payment_id VARCHAR(100),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """))
        conn.commit()
    except Exception as e:
        print(f"Transaction migration skipped/failed: {e}")
        conn.rollback()




app = FastAPI(
    title="MatDataHub API",
    description="Engineering Material Data API - Search, filter, and compare 1000+ engineering materials.",
    version="2.0.0",
    contact={
        "name": "MatDataHub",
    },
)

# --- RATE LIMITING IMPLEMENTATION ---
limiter = Limiter(key_func=get_remote_address, default_limits=["2000/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Register route modules
app.include_router(materials.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(feedback.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(account.router, prefix="/api/v1")       # <-- added payments
app.include_router(calculators.router, prefix="/api/v1")

# Allow cross-origin requests (so Streamlit Cloud can call Render-hosted API)

# Required by Authlib for OAuth flows (saves state between redirect and callback)
import os
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("OAUTH_SESSION_SECRET", "super-secret-oauth-key-change-me"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Tighten this to your Streamlit URL in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Health check / welcome endpoint."""
    return {
        "app": "MatDataHub API",
        "version": "0.2.0",
        "docs": "/docs",
        "status": "running",
    }




@app.get("/api/v1/admin/seed-demo")
def seed_demo_data():
    """
    Hidden endpoint to seed Render database without SSH access.
    """
    try:
        from scripts.seed_professor_materials import run_seed
        added = run_seed()
        return {"ok": True, "message": f"Successfully seeded {added} materials for the demo!"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
