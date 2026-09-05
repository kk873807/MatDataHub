import sys
with open("app/routers/materials.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "def get_materials(" in line:
        for j in range(i, i+15):
            print(f"Line {j}: {lines[j].strip()}")
        break
