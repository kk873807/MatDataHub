"""
MatDataHub API — Main application entry point.
Run with:
    uvicorn app.main:app --reload
Then open:
    http://127.0.0.1:8000        -> Welcome message
    http://127.0.0.1:8000/docs   -> Interactive API documentation (Swagger UI)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import materials, auth, admin, feedback, payments   # <-- added payments

# Create tables on startup (safe to call multiple times)
Base.metadata.create_all(bind=engine)

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
app.include_router(payments.router, prefix="/api/v1")       # <-- added payments

# Allow cross-origin requests (so Streamlit Cloud can call Render-hosted API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Tighten this to your Streamlit URL in production
    allow_credentials=True,
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
