import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "fig = go.Figure()" in line and i > 2500:
        for j in range(i-5, i+30):
            print(f"Line {j}: {lines[j].strip()}")
        break
