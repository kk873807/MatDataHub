import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in [3002, 3003]:
    print(f"Line {i}: {lines[i].encode('ascii', 'backslashreplace').decode().strip()}")
