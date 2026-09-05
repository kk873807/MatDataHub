with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "Platform Mastery Roadmap" in line:
        print(f"Found at {i}")
        break
for j in range(i, i+50):
    print(lines[j].strip())
