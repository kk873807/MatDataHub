import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '\u0393' in line or '\u2261' in line or '\xc9' in line or 'Γ' in line:
        print(f"Line {i}: {line.encode('ascii', 'backslashreplace').decode().strip()}")
