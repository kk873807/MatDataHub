
import json

lines = []
with open(r"C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\.system_generated\logs\transcript_full.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        lines.append(json.loads(line))

for msg in reversed(lines):
    if msg.get("type") == "USER_INPUT":
        content = msg.get("content", "")
        if "recover_yb.py" in content and "batch3_mp_enriched.csv" in content:
            # find recover_yb.py
            py_start = content.find("#!/usr/bin/env python3")
            py_end = content.find("material_name,formula_pretty,mp_id", py_start)
            if py_start != -1 and py_end != -1:
                py_code = content[py_start:py_end].strip()
                with open("recover_yb.py", "w", encoding="utf-8") as f:
                    f.write(py_code)
                print("Wrote recover_yb.py")

            # find csv
            csv_start = content.find("material_name,formula_pretty,mp_id")
            if csv_start != -1:
                csv_code = content[csv_start:].strip()
                with open("batch3_mp_enriched.csv", "w", encoding="utf-8") as f:
                    f.write(csv_code)
                print("Wrote batch3_mp_enriched.csv")
            break

