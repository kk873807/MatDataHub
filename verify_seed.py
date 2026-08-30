"""Quick verification that seeded data is being served by the API."""
import requests

BASE = "http://127.0.0.1:8000/api/v1"

# 1. List all
r = requests.get(f"{BASE}/materials/", params={"per_page": 30})
d = r.json()
print(f"Total materials in DB: {d['total']}\n")

print("=== ALL MATERIALS ===\n")
for m in d["materials"]:
    cost = f"Rs.{m['cost_per_kg_min']}-{m['cost_per_kg_max']}/kg" if m["cost_per_kg_min"] else "N/A"
    print(f"  {m['id']:2d}. {m['name']:45s} {m['category']:10s} {cost}")

# 2. Search test
print("\n=== SEARCH: 'corrosion' ===\n")
r = requests.get(f"{BASE}/materials/search", params={"q": "corrosion"})
d = r.json()
for m in d["materials"]:
    print(f"  {m['name']} - {m['applications'][:70]}")

# 3. Filter: cheapest metals under Rs.100/kg
print("\n=== FILTER: Metals under Rs.100/kg ===\n")
r = requests.get(f"{BASE}/materials/", params={"category": "Metal", "max_cost": 100})
d = r.json()
for m in d["materials"]:
    print(f"  {m['name']:40s} Rs.{m['cost_per_kg_min']}-{m['cost_per_kg_max']}/kg")

# 4. Filter: High tensile > 500 MPa
print("\n=== FILTER: Tensile strength > 500 MPa ===\n")
r = requests.get(f"{BASE}/materials/", params={"min_tensile": 500})
d = r.json()
for m in d["materials"]:
    print(f"  {m['name']:45s} {m['tensile_strength_min']}-{m['tensile_strength_max']} MPa")
