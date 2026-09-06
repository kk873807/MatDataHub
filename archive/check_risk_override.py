import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
start = -1
for i, line in enumerate(lines):
    if "raw_carbon = selected_mat.get" in line and "tab_risk" in "".join(lines[max(0, i-50):i]):
        start = i
        break
if start != -1:
    for i in range(start, start+25):
        if i < len(lines):
            print(f"Line {i}: {lines[i].encode('ascii', 'backslashreplace').decode().strip('\n')}")
