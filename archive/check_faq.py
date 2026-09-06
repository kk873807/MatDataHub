import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(2895, 2915):
    print(f"Line {i}: {repr(lines[i])}")
