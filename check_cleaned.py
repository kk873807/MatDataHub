import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "Average Rating" in line or "Helpful" in line or "Reply" in line or "Admin" in line:
        if "Community" in "".join(lines[max(0, i-50):i]): # Roughly within the community block
            print(line.strip())
