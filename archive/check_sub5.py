import sys
with open("app/routers/materials.py", "r", encoding="utf-8") as f:
    content = f.read()
if "/substitute" in content or "def substitute" in content:
    print("Substitute endpoint exists!")
else:
    print("Substitute endpoint missing!")
