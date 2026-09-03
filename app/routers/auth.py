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
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address), Request

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

import os
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.responses import RedirectResponse
from fastapi import Request
from app.auth import create_access_token

# ─── OAuth Setup ───
oauth_config = Config(environ=os.environ)
oauth = OAuth(oauth_config)
oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", ""),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)
oauth.register(
    name='apple',
    client_id=os.environ.get("APPLE_CLIENT_ID", ""),
    client_secret=os.environ.get("APPLE_CLIENT_SECRET", ""),
    access_token_url='https://appleid.apple.com/auth/token',
    authorize_url='https://appleid.apple.com/auth/authorize',
    client_kwargs={
        'scope': 'name email',
        'response_type': 'code id_token',
        'response_mode': 'form_post',
    }
)

@router.get("/google")
async def login_google(request: Request):
    if not oauth.google.client_id:
        return {"ok": False, "error": "Google Client ID is missing. Please configure backend environment variables."}
    redirect_uri = str(request.url).split('?')[0].rstrip('/') + '/callback'
    redirect_uri = str(redirect_uri).replace("http://", "https://") if "onrender" in str(redirect_uri) else str(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def auth_google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to fetch user info from Google")
            
        email = user_info.get("email")
        name = user_info.get("name")
        google_id = user_info.get("sub")
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                name=name,
                hashed_password="OAUTH_USER_NO_PASSWORD",
                auth_provider="google",
                provider_id=google_id,
                tier="free"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            if user.auth_provider != "google":
                user.auth_provider = "google"
                user.provider_id = google_id
                db.commit()

        access_token = create_access_token(data={"sub": user.email})
        
        frontend_url = os.environ.get("FRONTEND_URL", "https://matdatahub.streamlit.app")
        if "localhost" in str(request.url):
            frontend_url = "http://localhost:8501"
            
        return RedirectResponse(url=f"{frontend_url}/?t={access_token}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/apple")
async def login_apple(request: Request):
    return {"ok": False, "error": "Apple OAuth requires an Apple Developer account ($99/yr) and custom Private Key generation. We have scaffolded the route but need keys."}

@router.get("/sms")
async def login_sms(request: Request):
    return {"ok": False, "error": "SMS OTP requires a Twilio account. Please provide Twilio SID and Auth Token."}


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

    # Basic bot protection
    if "test.com" in req.email.lower() or len(req.name) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email domain or name. Please use a real email address."
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
    if user.is_blocked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been blocked. Please contact support.",
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
