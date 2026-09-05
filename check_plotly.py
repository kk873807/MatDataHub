import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "import plotly.graph_objects as go" in line:
        for j in range(i, i+30):
            print(f"Line {j}: {lines[j].strip()}")
        break
