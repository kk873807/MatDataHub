import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "st.markdown(\"## " in line or "st.header(" in line or "st.markdown('## " in line:
        print(f"Line {i}: {line.encode('ascii', 'backslashreplace').decode().strip()}")
