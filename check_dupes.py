import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "## \u2753 Frequently Asked Questions" in line.encode('ascii', 'backslashreplace').decode():
        print(f"Line {i}: FAQ Header")
    if "## \U0001f4ac Support Center" in line.encode('ascii', 'backslashreplace').decode():
        print(f"Line {i}: Support Header")
    if "## \U0001f4ac Help Center & Contact Support" in line.encode('ascii', 'backslashreplace').decode():
        print(f"Line {i}: Support Header 2")
