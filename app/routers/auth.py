"""
Auth API routes.

Endpoints:
    POST /auth/register  - Create a new account
    POST /auth/login     - Login and get JWT token
    GET  /auth/me        - Get current user profile (requires auth)
    POST /auth/upgrade   - Request a tier upgrade (requires auth; NOT instant —
                            an admin must approve it via /admin/upgrade-requests)
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status, Request

# --- Rate Limiting for Security ---
import time
from collections import defaultdict
from fastapi import Request

# IP -> list of timestamps
_auth_attempts: dict[str, list[float]] = defaultdict(list)
AUTH_COOLDOWN = 1.0  # 1 second between attempts
MAX_AUTH_PER_HOUR = 20

def _get_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

def _check_auth_rate_limit(request: Request):
    ip = _get_ip(request)
    now = time.time()
    timestamps = _auth_attempts[ip]
    
    # Remove attempts older than 1 hour (3600 seconds)
    timestamps[:] = [t for t in timestamps if now - t < 3600]
    
    if timestamps and (now - timestamps[-1]) < AUTH_COOLDOWN:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Please wait a moment before trying again.")
        
    if len(timestamps) >= MAX_AUTH_PER_HOUR:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Too many login attempts. Please try again later.")
        
    timestamps.append(now)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    generate_api_key,
    get_current_user,
)
from app.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserProfile,
    UpgradeRequest,
    UpgradeRequestResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

VALID_TIERS = {"pro", "advanced"}


# ──────────────────────────────────────────────
# POST /auth/register
# ──────────────────────────────────────────────
@router.post("/register", response_model=TokenResponse, status_code=201)
def register(req: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    _check_auth_rate_limit(request)
    """
    Create a new user account.

    Returns a JWT access token on success.
    All new users start on the 'free' tier.

    Example:
        POST /auth/register
        {"email": "kishan@example.com", "password": "securepass123", "name": "Kishan"}
    """
    # Check if email already exists
    existing = db.query(User).filter(User.email == req.email.lower().strip()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists. Please login instead.",
        )

    # Create user
    user = User(
        email=req.email.lower().strip(),
        hashed_password=hash_password(req.password),
        name=req.name,
        tier="free",
        api_key=generate_api_key(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate JWT token
    token = create_access_token(user.id, user.email, user.tier)

    return TokenResponse(
        access_token=token,
        tier=user.tier,
        name=user.name,
    )


# ──────────────────────────────────────────────
# POST /auth/login
# ──────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, request: Request, db: Session = Depends(get_db)):
    _check_auth_rate_limit(request)
    """
    Login with email and password.

    Returns a JWT access token on success.

    Example:
        POST /auth/login
        {"email": "kishan@example.com", "password": "securepass123"}
    """
    user = db.query(User).filter(User.email == req.email.lower().strip()).first()

    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Please contact support.",
        )

    # Generate JWT token
    token = create_access_token(user.id, user.email, user.tier)

    return TokenResponse(
        access_token=token,
        tier=user.tier,
        name=user.name,
    )


# ──────────────────────────────────────────────
# GET /auth/me
# ──────────────────────────────────────────────
@router.get("/me", response_model=UserProfile)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get the current user's profile.

    Requires a valid JWT token in the Authorization header:
        Authorization: Bearer <token>
    """
    return current_user


# ──────────────────────────────────────────────
# POST /auth/upgrade
# ──────────────────────────────────────────────
@router.post("/upgrade", response_model=UpgradeRequestResponse)
def request_upgrade(
    payload: UpgradeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Submit a request to upgrade to 'pro' or 'advanced'.

    This does NOT change the user's tier. It only records the request
    (requested_tier + upgrade_status="pending") for an admin to review.
    The tier is updated only when an admin approves it via
    POST /admin/upgrade-requests/{user_id}/approve.
    """
    tier = payload.tier.lower()
    if tier not in VALID_TIERS:
        raise HTTPException(status_code=400, detail="tier must be 'pro' or 'advanced'")

    # Prevent same-tier or downgrade requests
    TIER_ORDER = {"free": 0, "pro": 1, "advanced": 2}
    if TIER_ORDER.get(tier, 0) <= TIER_ORDER.get(current_user.tier, 0):
        raise HTTPException(status_code=400, detail=f"You're already on the '{current_user.tier}' tier. Only upgrades are allowed.")

    if current_user.upgrade_status == "pending":
        raise HTTPException(
            status_code=400,
            detail=f"You already have a pending request to upgrade to {current_user.requested_tier}.",
        )

    current_user.requested_tier = tier
    current_user.upgrade_status = "pending"
    current_user.requested_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(current_user)

    return UpgradeRequestResponse(
        message=f"Upgrade request to {tier} submitted! We'll review it shortly.",
        upgrade_status=current_user.upgrade_status,
        requested_tier=current_user.requested_tier,
    )
