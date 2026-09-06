import sys
with open("app/routers/materials.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(101, 115):
    print(f"Line {i}: {lines[i].strip()}")
