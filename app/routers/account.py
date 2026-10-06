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

from app.models import BOMAnalysis

@router.get("/bom-history")
def get_bom_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetch the CBAM/ESG BOM analysis history for the logged-in user."""
    history = db.query(BOMAnalysis).filter(BOMAnalysis.user_id == current_user.id).order_by(BOMAnalysis.created_at.desc()).all()
    
    return [
        {
            "id": item.id,
            "filename": item.filename,
            "strict_mode": item.strict_mode,
            "total_co2_tonnes": item.total_co2_tonnes,
            "cbam_cost_eur": item.cbam_cost_eur,
            "total_rows": item.total_rows,
            "quarantined_rows": item.quarantined_rows,
            "created_at": item.created_at
        }
        for item in history
    ]

import json

@router.get("/bom-history/{bom_id}")
def get_bom_history_detail(bom_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetch the detailed results (JSON) for a specific BOM analysis."""
    bom = db.query(BOMAnalysis).filter(BOMAnalysis.id == bom_id, BOMAnalysis.user_id == current_user.id).first()
    if not bom:
        raise HTTPException(status_code=404, detail="BOM analysis not found")
        
    results_data = []
    if bom.results_json:
        try:
            results_data = json.loads(bom.results_json)
        except json.JSONDecodeError:
            pass
            
    return {
        "id": bom.id,
        "filename": bom.filename,
        "strict_mode": bom.strict_mode,
        "total_co2_tonnes": bom.total_co2_tonnes,
        "cbam_cost_eur": bom.cbam_cost_eur,
        "total_rows": bom.total_rows,
        "quarantined_rows": bom.quarantined_rows,
        "created_at": bom.created_at,
        "results_data": results_data
    }
