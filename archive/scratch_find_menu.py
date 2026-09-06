import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "account_menu = st.radio" in line:
        print(f"{i}: {line.strip()}")
    if "Payment History" in line:
        print(f"{i}: {line.strip()}")
