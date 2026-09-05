import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any lingering 1499/mo with 499/mo
content = content.replace("1499/mo", "499/mo")
# Replace any lingering 149,999/mo with 49,999/mo
content = content.replace("149,999/mo", "49,999/mo")
content = content.replace("11499/mo", "49,999/mo")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated lingering prices.")
