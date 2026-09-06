import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "Engineering AI Advisor" in line:
        print(f"Line {i}: {line.encode('ascii', 'backslashreplace').decode().strip()}")
