import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_community = False
for i, line in enumerate(lines):
    if "## Community Reviews & Discussion" in line:
        in_community = True
    if in_community:
        print(f"{i}: {line.encode('ascii', 'backslashreplace').decode()}")
    if in_community and "    with tab_feedback:" in line:
        break
