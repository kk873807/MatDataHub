import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "with tab_projects:" in line or "with tab_enterprise:" in line:
        print(f"Line {i}: {line.strip()}")
