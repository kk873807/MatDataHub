import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(1350, 1375):
    line = lines[i]
    print(f"{i}: {line.encode('ascii', 'backslashreplace').decode()}")
