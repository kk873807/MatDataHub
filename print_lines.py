import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(1350, 1370):
    print(f"{i}: {repr(lines[i])}")
