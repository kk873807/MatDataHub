import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\auth.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''from fastapi import APIRouter, Depends, HTTPException, status, Request'''
good = '''from fastapi import APIRouter, Depends, HTTPException, status, Request, Header'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added Header import to auth.py")
else:
    print("Could not find block")
