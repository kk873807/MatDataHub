import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "elif st.session_state.current_page ==" in line or "Footer" in line:
        print(f"Line {i}: {line.strip()}")
