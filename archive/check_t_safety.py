import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
start = -1
for i, line in enumerate(lines):
    if "with t_safety:" in line:
        start = i
        break
if start != -1:
    for i in range(start, start+30):
        if i < len(lines):
            print(f"Line {i}: {lines[i].encode('ascii', 'backslashreplace').decode().strip('\n')}")
