import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace button backgrounds to be theme adaptive (gray transparent)
content = content.replace("background: rgba(255, 255, 255, 0.05);", "background: rgba(128, 128, 128, 0.1);")
content = content.replace("border: 1px solid rgba(255, 255, 255, 0.1);", "border: 1px solid rgba(128, 128, 128, 0.2);")

# Replace input box backgrounds
content = content.replace("background: rgba(255, 255, 255, 0.02) !important;", "background: rgba(128, 128, 128, 0.05) !important;")
content = content.replace("border: 1px solid rgba(255, 255, 255, 0.1) !important;", "border: 1px solid rgba(128, 128, 128, 0.2) !important;")

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("CSS updated for full Light Mode compatibility!")
