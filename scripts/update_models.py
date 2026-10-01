import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\models.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = "payment_id = Column(String(100), nullable=True)  # e.g., razorpay_payment_id or stripe_id"
good = "payment_id = Column(String(100), nullable=True, unique=True)  # e.g., razorpay_payment_id or stripe_id"

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added unique constraint to models.py")
else:
    print("Could not find payment_id block")
