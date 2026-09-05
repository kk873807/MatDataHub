import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "tab_compare, tab_substitute =" in line:
        for j in range(i-5, i+2):
            print(f"Line {j}: {lines[j].encode('ascii', 'backslashreplace').decode().strip('\n')}")
        break
