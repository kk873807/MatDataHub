import sys
import re

file_path = 'app/routers/account.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'if current_user.tier not in ["pro", "advanced"]:',
    'if current_user.tier != "advanced":'
)
content = content.replace(
    'API Keys are only available for Pro and Advanced tiers.',
    'API Keys are strictly reserved for the Advanced (Enterprise) tier.'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated account.py")
