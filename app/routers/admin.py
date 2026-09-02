"""
Admin routes — approve/reject tier upgrade requests.
Gated by a shared secret (ADMIN_SECRET env var) sent as X-Admin-Secret header.
This is a single-operator gate, not full RBAC.
"""
import os
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth import generate_api_key
from app.schemas import PendingRequestOut, AdminActionResponse

router = APIRouter(prefix="/admin", tags=["Admin"])
ADMIN_SECRET = os.getenv("ADMIN_SECRET")


def verify_admin(x_admin_secret: str = Header(...)):
    if not ADMIN_SECRET:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Admin access not configured.")
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid admin credentials.")
    return True


@router.get("/upgrade-requests", response_model=list[PendingRequestOut])
def list_pending_requests(_: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    users = db.query(User).filter(User.upgrade_status == "pending").order_by(User.requested_at.asc()).all()
    return [
        PendingRequestOut(
            id=u.id, email=u.email, name=u.name, current_tier=u.tier,
            requested_tier=u.requested_tier, requested_at=u.requested_at,
        ) for u in users
    ]


@router.post("/upgrade-requests/{user_id}/approve", response_model=AdminActionResponse)
def approve_request(user_id: int, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found.")
    if user.upgrade_status != "pending":
        raise HTTPException(400, "This user has no pending request.")

    new_tier = user.requested_tier
    user.tier = new_tier
    if new_tier == "advanced" and not user.api_key:
        user.api_key = generate_api_key()
    user.requested_tier = None
    user.upgrade_status = None
    user.requested_at = None
    db.commit()
    db.refresh(user)

    return AdminActionResponse(message=f"Approved. {user.email} is now on {new_tier}.", user_email=user.email, tier=user.tier)


@router.post("/upgrade-requests/{user_id}/reject", response_model=AdminActionResponse)
def reject_request(user_id: int, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found.")
    if user.upgrade_status != "pending":
        raise HTTPException(400, "This user has no pending request.")

    rejected = user.requested_tier
    user.requested_tier = None
    user.upgrade_status = None
    user.requested_at = None
    db.commit()

    return AdminActionResponse(message=f"Rejected {user.email}'s request for {rejected}.", user_email=user.email, tier=user.tier)

@router.post("/users/{user_id}/block")
def block_user(user_id: int, _: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    """Admin-only: block a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found.")
    user.is_blocked = True
    db.commit()
    return {"message": f"User {user.email} blocked."}
