import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\payments.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add slowapi imports
if 'from slowapi import Limiter' not in content:
    content = content.replace('from fastapi import APIRouter, Depends, HTTPException, Request', 'from fastapi import APIRouter, Depends, HTTPException, Request\nfrom slowapi import Limiter\nfrom slowapi.util import get_remote_address')
    content = content.replace('router = APIRouter(prefix="/payments", tags=["Payments"])', 'router = APIRouter(prefix="/payments", tags=["Payments"])\n\nlimiter = Limiter(key_func=get_remote_address)')

# Add rate limit to create-link
bad = '''@router.post("/create-link")
def create_payment_link(req: CreateLinkRequest, current_user: User = Depends(get_current_user)):'''

good = '''@router.post("/create-link")
@limiter.limit("5/minute")
def create_payment_link(request: Request, req: CreateLinkRequest, current_user: User = Depends(get_current_user)):'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added rate limit to create-link")
else:
    print("Could not find create-link block")
