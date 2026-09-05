import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "st.markdown(\"### \U0001f916 Engineering AI Advisor\")" in line.encode('ascii', 'backslashreplace').decode():
        print(f"Line {i}")
