import os
import hmac
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
import razorpay

from app.database import get_db
from app.models import User, Transaction
from app.auth import get_current_user, generate_api_credentials
from pydantic import BaseModel

router = APIRouter(prefix="/payments", tags=["Payments"])

limiter = Limiter(key_func=get_remote_address)

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")

# Initialize razorpay client only if keys are present
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)) if RAZORPAY_KEY_ID else None

from typing import Optional

class CreateLinkRequest(BaseModel):
    tier: str
    callback_url: Optional[str] = None

@router.post("/create-link")
@limiter.limit("5/minute")
def create_payment_link(request: Request, req: CreateLinkRequest, current_user: User = Depends(get_current_user)):
    if not client:
        raise HTTPException(status_code=500, detail="Razorpay is not configured on the server.")
        
    tier = req.tier.lower()
    if tier not in ["pro", "advanced"]:
        raise HTTPException(status_code=400, detail="Invalid tier.")
        
    if current_user.tier == tier:
        raise HTTPException(status_code=400, detail=f"You are already on the {tier.capitalize()} tier.")
        
    if current_user.tier == "advanced" and tier == "pro":
        raise HTTPException(status_code=400, detail="You are currently on the Advanced tier. Downgrading to Pro requires contacting support.")
        
    amount = 49900 if tier == "pro" else 1999900  # Amount in paise (multiply INR by 100)
    
    # Generate payment link
    try:
        payment_link_data = {
            "amount": amount,
            "currency": "INR",
            "accept_partial": False,
            "description": f"Upgrade to {tier.capitalize()} Tier",
            "customer": {
                "name": current_user.name or "MatDataHub User",
                "email": current_user.email
            },
            "notify": {
                "sms": False,
                "email": True
            },
            "reminder_enable": False,
            "notes": {
                "user_id": str(current_user.id),
                "tier": tier
            },
            "options": {
                "checkout": {
                    "name": "MatDataHub"
                }
            }
        }
        
        if req.callback_url:
            if not req.callback_url.startswith(("http://", "https://")):
                raise HTTPException(status_code=400, detail="Invalid callback URL.")
            payment_link_data["callback_url"] = req.callback_url
            payment_link_data["callback_method"] = "get"
        
        response = client.payment_link.create(payment_link_data)
        return {"payment_url": response.get("short_url")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create payment link: {str(e)}")

@router.post("/webhook")
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Razorpay sends a webhook when payment succeeds.
    Verifies HMAC-SHA256 signature, upgrades user tier, and logs the transaction.
    """
    import json
    
    webhook_signature = request.headers.get("X-Razorpay-Signature")
    if not webhook_signature:
        raise HTTPException(status_code=400, detail="Missing signature")
        
    if not RAZORPAY_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured on server")
        
    body = await request.body()
    
    # Verify HMAC-SHA256 signature
    expected_sig = hmac.HMAC(
        key=RAZORPAY_WEBHOOK_SECRET.encode('utf-8'),
        msg=body,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(expected_sig, webhook_signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
        
    try:
        # Parse JSON from the already-consumed body bytes (not request.json())
        data = json.loads(body)
        event = data.get("event")
        
        if event in ("payment_link.paid", "payment.captured"):
            # Payment link payloads store notes in data.payload.payment_link.entity.notes
            # or data.payload.payment.entity.notes depending on the event
            payload = data.get("payload", {})
            entity = (payload.get("payment_link") or payload.get("payment", {})).get("entity", {})
            notes = entity.get("notes", {})
            
            user_id_str = notes.get("user_id")
            tier = notes.get("tier")
            
            # Extract payment_id for idempotency
            payment_entity = payload.get("payment", {}).get("entity", {})
            payment_id = payment_entity.get("id") or entity.get("id")
            
            if user_id_str and tier:
                # Idempotency: skip if this payment_id was already processed
                if payment_id:
                    existing_txn = db.query(Transaction).filter(Transaction.payment_id == payment_id).first()
                    if existing_txn:
                        return {"status": "ok", "detail": "Already processed"}
                
                user_id = int(user_id_str)
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    # Protect against unauthorized downgrades via webhook
                    if not (user.tier == "advanced" and tier == "pro"):
                        user.tier = tier
                        user.upgrade_status = None
                        user.requested_tier = None
                        
                        # Generate API credentials for Advanced users if they don't have them
                        if tier == "advanced" and not user.api_key:
                            raw_key, raw_secret = generate_api_credentials()
                            user.api_key = raw_key
                            user.api_secret = raw_secret
                    
                # Always record transaction for audit trail, even if user was deleted mid-payment
                amount_paid = (entity.get("amount") or 0) / 100.0  # Convert paise to INR
                
                new_txn = Transaction(
                    user_id=user_id,
                    amount=amount_paid,
                    currency=entity.get("currency", "INR"),
                    tier_purchased=tier,
                    status="completed",
                    payment_id=payment_id
                )
                db.add(new_txn)
                db.commit()
                    
        return {"status": "ok"}
    except Exception as e:
        # Raise 500 so Razorpay properly retries the webhook in case of database downtime
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
