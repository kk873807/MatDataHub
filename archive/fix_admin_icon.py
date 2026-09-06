import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("\u0393\xa3\xe0 Verified Admin Response", "✅ Verified Admin Response")

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced Verified Admin Response icon!")
