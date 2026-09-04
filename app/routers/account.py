from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Transaction, User
from app.auth import get_current_user
from app.schemas import TransactionOut

router = APIRouter(prefix="/account", tags=["Account & Settings"])

@router.get("/transactions", response_model=List[TransactionOut])
def get_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetch the payment history / transactions for the currently logged-in user."""
    return db.query(Transaction).filter(Transaction.user_id == current_user.id).order_by(Transaction.created_at.desc()).all()


import secrets

@router.post("/generate-api-key")
def generate_api_key(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.tier != "advanced":
        raise HTTPException(status_code=403, detail="API Keys are strictly reserved for the Advanced (Enterprise) tier.")
        
    new_key = "mdh_" + secrets.token_hex(24)
    current_user.api_key = new_key
    db.commit()
    return {"ok": True, "api_key": new_key, "message": "New API Key generated successfully!"}
