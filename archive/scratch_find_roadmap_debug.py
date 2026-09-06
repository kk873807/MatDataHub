with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Simulation &" in line:
        print(f"Found Simulation at {i}")
    if "<!-- wrapper -->" in line:
        print(f"Found wrapper at {i}")
