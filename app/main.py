"""
MatDataHub API â€” Main application entry point.
Run with:
    uvicorn app.main:app --reload
Then open:
    http://127.0.0.1:8000        -> Welcome message
    http://127.0.0.1:8000/docs   -> Interactive API documentation (Swagger UI)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import materials, auth, admin, feedback, payments, ai, projects
from sqlalchemy.orm import Session
from app.database import get_db   # <-- added payments


# Create tables on startup (safe to call multiple times)
Base.metadata.create_all(bind=engine)

# Quick and dirty auto-migration for MVP
from sqlalchemy import text
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN is_blocked BOOLEAN DEFAULT FALSE;"))
        try:
            conn.execute(text("ALTER TABLE projects ADD COLUMN blueprint_data TEXT;"))
            conn.commit()
        except Exception:
            pass
        conn.commit()
    except Exception:
        pass # Probably already exists
        
    try:
        conn.execute(text("ALTER TABLE feedback ADD COLUMN helpful_votes INTEGER DEFAULT 0;"))
        conn.commit()
    except Exception:
        pass # Probably already exists


app = FastAPI(
    title="MatDataHub API",
    description="Engineering Material Data API - Search, filter, and compare 500+ engineering materials.",
    version="0.2.0",
    contact={
        "name": "MatDataHub",
    },
)

# Register route modules
app.include_router(materials.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(feedback.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")       # <-- added payments

# Allow cross-origin requests (so Streamlit Cloud can call Render-hosted API)
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


