import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\payments.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_imports = 'from app.models import User'
good_imports = 'from app.models import User, Transaction'

bad_req = '''class CreateLinkRequest(BaseModel):
    tier: str'''
good_req = '''from typing import Optional

class CreateLinkRequest(BaseModel):
    tier: str
    callback_url: Optional[str] = None'''

bad_link = '''        payment_link_data = {
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
            # "callback_url": "https://matdataapp-x5gof2igdr7cmiwucho22n.next.js.app/", # Optional redirect
            # "callback_method": "get"
        }'''

good_link = '''        payment_link_data = {
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
            }
        }
        
        if req.callback_url:
            payment_link_data["callback_url"] = req.callback_url
            payment_link_data["callback_method"] = "get"'''

bad_webhook = '''            if user_id_str and tier:
                user_id = int(user_id_str)
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user.tier = tier
                    user.upgrade_status = None
                    user.requested_tier = None
                    db.commit()'''

good_webhook = '''            if user_id_str and tier:
                user_id = int(user_id_str)
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user.tier = tier
                    user.upgrade_status = None
                    user.requested_tier = None
                    
                    # Record transaction securely
                    payment_id = data["payload"].get("payment", {}).get("entity", {}).get("id") or entity.get("id")
                    amount_paid = entity.get("amount", 0) / 100.0  # Convert paise to INR
                    
                    new_txn = Transaction(
                        user_id=user.id,
                        amount=amount_paid,
                        currency=entity.get("currency", "INR"),
                        tier_purchased=tier,
                        status="completed",
                        payment_id=payment_id
                    )
                    db.add(new_txn)
                    db.commit()'''

if bad_imports in content: content = content.replace(bad_imports, good_imports)
if bad_req in content: content = content.replace(bad_req, good_req)
if bad_link in content: content = content.replace(bad_link, good_link)
if bad_webhook in content: content = content.replace(bad_webhook, good_webhook)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Payments router updated")
