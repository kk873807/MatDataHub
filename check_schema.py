import sys
with open("app/schemas.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "class MaterialListResponse" in line:
        for j in range(i, i+10):
            print(f"Line {j}: {lines[j].strip()}")
        break
