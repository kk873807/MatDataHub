import sys

with open("app/routers/materials.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "def get_materials" in line or "@router.get(" in line:
        print(f"Line {i}: {line.strip()}")
