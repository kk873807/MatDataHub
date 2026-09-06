with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
with open("scratch_roadmap.txt", "w", encoding="utf-8") as out:
    in_roadmap = False
    for i, line in enumerate(lines):
        if 'class="roadmap-wrapper"' in line:
            in_roadmap = True
        if in_roadmap:
            out.write(line)
        if in_roadmap and '</div> <!-- wrapper -->' in line:
            break
