import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\payments.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''                user_id = int(user_id_str)
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user.tier = tier
                    user.upgrade_status = None
                    user.requested_tier = None
                    
                    # Record transaction
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

good = '''                user_id = int(user_id_str)
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user.tier = tier
                    user.upgrade_status = None
                    user.requested_tier = None
                    
                # Always record transaction for audit trail, even if user was deleted mid-payment
                amount_paid = entity.get("amount", 0) / 100.0  # Convert paise to INR
                
                new_txn = Transaction(
                    user_id=user_id,
                    amount=amount_paid,
                    currency=entity.get("currency", "INR"),
                    tier_purchased=tier,
                    status="completed",
                    payment_id=payment_id
                )
                db.add(new_txn)
                db.commit()'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed audit trail logic")
else:
    print("Could not find block")
