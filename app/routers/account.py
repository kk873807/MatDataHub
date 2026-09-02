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
