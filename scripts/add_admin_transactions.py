import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\admin.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add models import
if 'Transaction' not in content:
    content = content.replace('from app.models import User', 'from app.models import User, Transaction')

# Add schema import
if 'AdminTransactionOut' not in content:
    content = content.replace('from app.schemas import PendingRequestOut, AdminActionResponse', 'from app.schemas import PendingRequestOut, AdminActionResponse, AdminTransactionOut')

# Add route
new_route = '''
@router.get("/transactions", response_model=list[AdminTransactionOut])
def get_all_transactions(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Fetch all platform transactions with user emails for the admin dashboard."""
    txns = db.query(Transaction, User.email).join(User, Transaction.user_id == User.id).order_by(Transaction.created_at.desc()).all()
    
    result = []
    for txn, email in txns:
        txn_dict = {
            "id": txn.id,
            "user_id": txn.user_id,
            "amount": txn.amount,
            "currency": txn.currency,
            "tier_purchased": txn.tier_purchased,
            "status": txn.status,
            "payment_id": txn.payment_id,
            "created_at": txn.created_at,
            "user_email": email
        }
        result.append(txn_dict)
    return result
'''

if 'get_all_transactions' not in content:
    content += new_route

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added /transactions route to admin")
