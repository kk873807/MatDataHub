import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Frequently Asked Questions" in line or "Support Center" in line or "Help Center & Contact Support" in line:
        print(f"Line {i}: {line.strip()}")
