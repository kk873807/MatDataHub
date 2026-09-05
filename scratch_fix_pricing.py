import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the price rendering
content = re.sub(r'st\.markdown\("## .*?114999 / mo"\)', 'st.markdown("## ₹14999 / mo")', content)
content = re.sub(r'st\.markdown\("## .*?1999 / mo"\)', 'st.markdown("## ₹14999 / mo")', content)
content = re.sub(r'st\.markdown\("## ₹14999 / mo"\)', 'st.markdown("## ₹14,999 / mo")', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed pricing text formatting.")
