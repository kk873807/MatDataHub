import json

with open("backend/data/materials.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for m in data[:3]:
    print(f"Name: {m.get('name')}")
    print(f"cost_per_kg: {m.get('cost_per_kg')}")
    print(f"cost_per_kg_min: {m.get('cost_per_kg_min')}")
    print(f"cost_per_kg_max: {m.get('cost_per_kg_max')}")
    print("---")
