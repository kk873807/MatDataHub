import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace using regex to avoid spacing issues
content = re.sub(
    r'\.compact-admin \{[^\}]+\}', 
    '.compact-admin {\n                            background-color: var(--secondary-background-color);\n                            border: 1px solid var(--faded-text-20);\n                            border-left: 3px solid #00f0ff;\n                            border-radius: 5px;\n                            padding: 10px;\n                            margin-top: 10px;\n                            font-size: 0.85em;\n                            color: var(--text-color);\n                        }', 
    content
)

content = content.replace('<strong style="color:#00ffcc">✅ Verified Admin Response:</strong>', '<strong style="color: #00f0ff;">✅ Verified Admin Response:</strong>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("CSS Regex updated.")
