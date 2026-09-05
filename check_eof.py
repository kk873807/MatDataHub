import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(len(lines)-60, len(lines)):
    print(f"Line {i}: {repr(lines[i])}")
