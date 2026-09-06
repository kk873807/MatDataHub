import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "Community Reviews & Discussion" in line:
        print(f"Found at line {i}")
