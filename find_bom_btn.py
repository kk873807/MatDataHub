import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "Run advanced optimization" in line or "Run Advanced Optimization" in line:
        print(f"Line {i}: {line.strip()}")
