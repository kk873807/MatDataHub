import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "with tab_home:" in line:
        print(f"tab_home at {i}")
    if "with tab_browse_main:" in line:
        print(f"tab_browse_main at {i}")
