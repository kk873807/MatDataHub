import sys

file_path = 'app/routers/admin.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Regex to remove the test_smtp_connection function and its route
content = re.sub(r'@router\.get\("/test-smtp"\)[\s\S]*?(?=\n@router|\Z)', '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content.strip() + '\n')
print("Removed /test-smtp from admin.py")
