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


from app.auth import get_current_user, generate_api_credentials

@router.post("/generate-api-key")
def generate_api_key(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.tier != "advanced":
        raise HTTPException(status_code=403, detail="API Keys are strictly reserved for the Advanced (Enterprise) tier.")
        
    # Generate API credentials matching the rest of the application
    raw_key, raw_secret = generate_api_credentials()
    
    current_user.api_key = raw_key
    current_user.api_secret = raw_secret
    db.commit()
    
    return {
        "ok": True, 
        "api_key_id": raw_key,
        "api_secret": raw_secret,
        "message": "API Key generated successfully!"
    }
