import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(670, 710):
    if "def api_get" in lines[i]:
        for j in range(i, i+15):
            print(f"Line {j}: {lines[j].strip()}")
        break
