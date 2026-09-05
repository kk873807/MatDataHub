import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "st.button" in line.lower() or "button" in line.lower() or "primary" in line.lower():
        if "<style>" in "".join(lines[max(0, i-50):i+50]):
            pass # just a heuristic
for i, line in enumerate(lines[:300]):
    if "button" in line.lower():
        print(f"Line {i}: {line.strip()}")
