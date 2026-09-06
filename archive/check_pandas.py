import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "import pandas as pd" in line:
        print("pandas imported")
        break
