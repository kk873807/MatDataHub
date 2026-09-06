import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "with tab_guide:" in line:
        print(f"tab_guide at {i}")
