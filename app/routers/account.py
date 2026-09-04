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
        
    import hashlib
    import base64
    # Generate an API Key ID and a Secret
    key_id = "mdh_key_" + secrets.token_hex(8)
    raw_secret = "mdh_secret_" + secrets.token_hex(24)
    
    # We only store the hash of the secret for authentication.
    hashed_secret = hashlib.sha256(raw_secret.encode('utf-8')).hexdigest()
    current_user.api_key = hashed_secret
    db.commit()
    
    return {
        "ok": True, 
        "api_key_id": key_id,
        "api_secret": raw_secret,
        "message": "API Key generated successfully!"
    }
