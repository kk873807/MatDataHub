"""
Auth API routes.

Endpoints:
    POST /auth/register  - Create a new account
    POST /auth/login     - Login and get JWT token
    GET  /auth/me        - Get current user profile (requires auth)
    POST /auth/upgrade   - Upgrade current user's tier (requires auth)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    generate_api_key,
    get_current_user,
    TIER_LIMITS,
)
from app.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserProfile,
    UpgradeRequest,
    UpgradeResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

VALID_TIERS = {"pro", "advanced"}


# ──────────────────────────────────────────────
# POST /auth/register
# ──────────────────────────────────────────────
@router.post("/register", response_model=TokenResponse, status_code=201)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email.lower().strip()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists. Please login instead.",
        )

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

    token = create_access_token(user.id, user.email, user.tier)

    return TokenResponse(access_token=token, tier=user.tier, name=user.name)


# ──────────────────────────────────────────────
# POST /auth/login
# ──────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
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

    token = create_access_token(user.id, user.email, user.tier)

    return TokenResponse(access_token=token, tier=user.tier, name=user.name)


# ──────────────────────────────────────────────
# GET /auth/me
# ──────────────────────────────────────────────
@router.get("/me", response_model=UserProfile)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


# ──────────────────────────────────────────────
# POST /auth/upgrade
# ──────────────────────────────────────────────
@router.post("/upgrade", response_model=UpgradeResponse)
def upgrade_tier(
    payload: UpgradeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tier = payload.tier.lower()
    if tier not in VALID_TIERS:
        raise HTTPException(status_code=400, detail="tier must be 'pro' or 'advanced'")

    current_user.tier = tier

    if tier == "advanced" and not current_user.api_key:
        current_user.api_key = generate_api_key()

    db.commit()
    db.refresh(current_user)

    # Same 3-arg call signature as /login and /register use
    new_token = create_access_token(current_user.id, current_user.email, current_user.tier)

    return UpgradeResponse(
        message=f"Upgraded to {tier}! 🎉",
        tier=current_user.tier,
        api_key=current_user.api_key,
        token=new_token,
    )
