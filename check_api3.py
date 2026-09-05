import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "def api_get(" in line:
        for j in range(i, i+15):
            print(f"Line {j}: {lines[j].strip()}")
        break
