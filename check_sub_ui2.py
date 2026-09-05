import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(3045, 3075):
    try:
        print(f"Line {i}: {lines[i].encode('ascii', 'backslashreplace').decode().strip()}")
    except:
        pass
