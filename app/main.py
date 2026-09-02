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
from app.routers import materials, auth, admin, feedback, payments, ai
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
app.include_router(ai.router, prefix="/api/v1")       # <-- added payments

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


@app.get("/api/v1/debug_db")
def debug_db():
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE feedback ADD COLUMN helpful_votes INTEGER DEFAULT 0;"))
            conn.commit()
            return {"status": "success added helpful_votes"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/debug2")
def debug2(db: Session = Depends(get_db)):
    from app.models import Feedback
    try:
        fb = db.query(Feedback).filter(Feedback.rating != None).order_by(Feedback.helpful_votes.desc()).all()
        return {"status": "ok", "count": len(fb)}
    except Exception as e:
        import traceback
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}
