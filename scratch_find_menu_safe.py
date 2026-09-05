import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open("scratch_lines.txt", 'w', encoding='utf-8') as out:
    for i, line in enumerate(lines):
        if "account_menu = st.radio" in line:
            out.write(f"{i}: {line}")
        if "Payment History" in line:
            out.write(f"{i}: {line}")
        if "Find Materials Similar" in line:
            out.write(f"{i}: {line}")
