import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in [2903, 2936]:
    print(f"Line {i}: {lines[i].encode('ascii', 'backslashreplace').decode().strip()}")
