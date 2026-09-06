with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
with open("out_pricing_safe.txt", "w", encoding="utf-8") as out:
    for i, line in enumerate(lines):
        if "def render_pricing_page" in line:
            for j in range(i, i+120):
                if j < len(lines):
                    out.write(lines[j])
            break
