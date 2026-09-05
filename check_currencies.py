import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

for i, line in enumerate(content.split("\n")):
    if "cbam" in line.lower() and ("€" in line or "$" in line or "eur" in line.lower() or "usd" in line.lower()):
        print(f"Line {i}: {line.encode('ascii', 'backslashreplace').decode().strip()}")
