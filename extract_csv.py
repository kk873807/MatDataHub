
import json

lines = []
with open(r"C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\.system_generated\logs\transcript_full.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        lines.append(json.loads(line))

for msg in reversed(lines):
    if msg.get("type") == "USER_INPUT":
        content = msg.get("content", "")
        if "ZrZn3" in content:
            print("Message starts with:", repr(content[:100]))
            break

