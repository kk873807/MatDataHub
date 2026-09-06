with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "def render_pricing_page" in line:
        for j in range(i, i+50):
            print(lines[j].strip())
        break
