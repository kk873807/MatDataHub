import json

with open("backend/data/materials.json", "r", encoding="utf-8") as f:
    data = json.load(f)

nonzero = 0
for m in data:
    c = m.get("embodied_carbon")
    if c and float(c) > 0:
        nonzero += 1
print(f"Total mats: {len(data)}")
print(f"Mats with embodied_carbon > 0: {nonzero}")
