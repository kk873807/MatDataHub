import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "def fetch_all_materials" in line or "requests.get(f\"{API_BASE}/materials" in line:
        for j in range(i, i+15):
            print(f"Line {j}: {lines[j].strip()}")
        break
