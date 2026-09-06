import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_community = False
for i, line in enumerate(lines):
    if "## Community Reviews & Discussion" in line:
        in_community = True
    if in_community and "st.divider()" in line: # Or end of community block
        pass
    if in_community:
        print(f"{i}: {repr(line)}")
    if in_community and "    with tab_feedback:" in line:
        break
