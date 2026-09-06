import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    text = f.read().split("PRO FEATURE: SMART SUBSTITUTE")[1]
    
# Remove emojis to print to terminal safely
text = text.encode("ascii", "ignore").decode()
print(text)
