import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(2998, 3035):
    print(f"Line {i}: {lines[i].strip()}")
