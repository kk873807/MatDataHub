import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\payments.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Webhook Secret Vulnerability
bad_sig = '''    webhook_signature = request.headers.get("X-Razorpay-Signature")
    if not webhook_signature:
        raise HTTPException(status_code=400, detail="Missing signature")
        
    body = await request.body()'''

good_sig = '''    webhook_signature = request.headers.get("X-Razorpay-Signature")
    if not webhook_signature:
        raise HTTPException(status_code=400, detail="Missing signature")
        
    if not RAZORPAY_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured on server")
        
    body = await request.body()'''

if bad_sig in content:
    content = content.replace(bad_sig, good_sig)
    print("Fixed empty webhook secret vulnerability")

# 2. NoneType safe division
bad_amount = '''                amount_paid = entity.get("amount", 0) / 100.0  # Convert paise to INR'''
good_amount = '''                amount_paid = (entity.get("amount") or 0) / 100.0  # Convert paise to INR'''

if bad_amount in content:
    content = content.replace(bad_amount, good_amount)
    print("Fixed NoneType division vulnerability")

# 3. Proper Exception Handling to allow Razorpay Retries
bad_except = '''        return {"status": "ok"}
    except Exception as e:
        # Return 200 so Razorpay doesn't endlessly retry on our logic errors
        return {"status": "error", "detail": str(e)}'''

good_except = '''        return {"status": "ok"}
    except Exception as e:
        # Raise 500 so Razorpay properly retries the webhook in case of database downtime
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))'''

if bad_except in content:
    content = content.replace(bad_except, good_except)
    print("Fixed webhook retry mechanism")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
