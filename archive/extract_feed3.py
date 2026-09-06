import sys

with open("old_app.py", "r", encoding="utf-16") as f:
    content = f.read()

start = content.find("Community Reviews & Discussion")
if start != -1:
    text = content[start-100:start+1000]
    print(text.encode("ascii", "ignore").decode())
else:
    print("NOT FOUND IN old_app.py")
