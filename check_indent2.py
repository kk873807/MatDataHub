import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(2985, 3015):
    try:
        print(f"{i+1}: {lines[i].encode('ascii', 'backslashreplace').decode()}")
    except Exception:
        pass
