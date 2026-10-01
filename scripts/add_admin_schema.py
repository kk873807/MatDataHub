import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\schemas.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_schema = '''class TransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    tier_purchased: str
    status: str
    payment_id: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class AdminTransactionOut(TransactionOut):
    user_email: str
'''

if 'class AdminTransactionOut' not in content:
    content = content.replace('''class TransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    tier_purchased: str
    status: str
    payment_id: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}''', new_schema)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added AdminTransactionOut schema")
else:
    print("Already exists")
