"""
Authentication utilities for MatDataHub.

Provides:
    - Password hashing (bcrypt via passlib)
    - JWT token creation and validation
    - FastAPI dependencies for protected routes
    - API key generation
"""
import os
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

# ── Config ──
# Secret key for JWT signing — read from env or generate a default for dev
JWT_SECRET = os.getenv("JWT_SECRET", "matdatahub-dev-secret-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24

# ── Password hashing (bcrypt directly) ──


def hash_password(plain_password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    pwd_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ── JWT Tokens ──
def create_access_token(user_id: int, email: str, tier: str) -> str:
    """Create a JWT access token with user info embedded."""
    payload = {
        "sub": str(user_id),
        "email": email,
        "tier": tier,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token. Raises HTTPException on failure."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please login again.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )


# ── API Key generation ──
def generate_api_key() -> str:
    """Generate a secure 32-character hex API key prefixed with 'mdh_'."""
    return f"mdh_{secrets.token_hex(16)}"


# ── Tier constants ──
TIER_LIMITS = {
    "free":     {"compare_max": 2,  "api_daily": 0,     "export": False, "find_similar": False},
    "pro":      {"compare_max": 5,  "api_daily": 0,     "export": True,  "find_similar": True},
    "advanced": {"compare_max": 99, "api_daily": 10000, "export": True,  "find_similar": True},
}


# ── FastAPI Dependencies ──
# This enables the "Authorization: Bearer <token>" header extraction
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    api_key = request.headers.get("X-API-Key")
    if api_key:
        user = db.query(User).filter(User.api_key == api_key, User.is_active == True).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid API Key")
        if getattr(user, "is_blocked", False):
            raise HTTPException(status_code=403, detail="Account blocked.")
        return user

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please login or register.",
        )

    payload = decode_token(credentials.credentials)
    user_id = int(payload["sub"])

    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or deactivated.",
        )
    if getattr(user, 'is_blocked', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been blocked.",
        )
    return user


def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    """
    FastAPI dependency: OPTIONALLY extracts user from JWT token.
    Returns None if no token provided (anonymous access).
    Use this for endpoints that work for everyone but behave differently for logged-in users.
    """
    if credentials is None:
        return None

    try:
        payload = decode_token(credentials.credentials)
        user_id = int(payload["sub"])
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        return user
    except HTTPException:
        return None
