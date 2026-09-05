import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Request Upgrade' in line:
        print(repr(line))

    if 'st.markdown("## ₹' in line:
        print(repr(line))

