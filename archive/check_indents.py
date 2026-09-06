import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(3090, 3105):
    print(f"Line {i}: {lines[i].encode('ascii', 'backslashreplace').decode().strip('\n')}")
