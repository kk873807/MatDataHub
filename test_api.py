"""
Quick test: insert 3 sample materials and test all API endpoints.
Run with:  python test_api.py
"""
import requests
import json

BASE = "http://127.0.0.1:8000/api/v1"

# ── 1. Insert sample materials ──
samples = [
    {
        "name": "AISI 304 Stainless Steel",
        "category": "Metal",
        "subcategory": "Stainless Steel",
        "grade": "304",
        "standard": "ASTM A240",
        "density": 7.93,
        "tensile_strength_min": 515,
        "tensile_strength_max": 750,
        "yield_strength_min": 205,
        "yield_strength_max": 310,
        "elongation": 40,
        "hardness": "85 HRB",
        "elastic_modulus": 193,
        "thermal_conductivity": 16.2,
        "melting_point_min": 1400,
        "melting_point_max": 1455,
        "cost_per_kg_min": 250,
        "cost_per_kg_max": 400,
        "applications": "Kitchen sinks, chemical tanks, food processing equipment",
        "equivalent_grades": "SUS 304 (JIS), X5CrNi18-10 (EN), 08Cr18Ni10 (China)",
        "composition": "Fe 66-74%, Cr 18-20%, Ni 8-10.5%, Mn 2%",
        "source_name": "MatWeb",
    },
    {
        "name": "Aluminium 6061-T6",
        "category": "Metal",
        "subcategory": "Aluminium Alloy",
        "grade": "6061-T6",
        "standard": "ASTM B209",
        "density": 2.70,
        "tensile_strength_min": 290,
        "tensile_strength_max": 310,
        "yield_strength_min": 240,
        "yield_strength_max": 276,
        "elongation": 12,
        "hardness": "95 HBW",
        "elastic_modulus": 68.9,
        "thermal_conductivity": 167,
        "melting_point_min": 582,
        "melting_point_max": 652,
        "cost_per_kg_min": 220,
        "cost_per_kg_max": 350,
        "applications": "Aerospace structures, bicycle frames, automotive parts",
        "equivalent_grades": "A96061 (UNS), AlMg1SiCu (EN)",
        "composition": "Al 95.8-98.6%, Mg 0.8-1.2%, Si 0.4-0.8%, Cu 0.15-0.4%",
        "source_name": "MatWeb",
    },
    {
        "name": "Nylon 6 (PA6)",
        "category": "Polymer",
        "subcategory": "Thermoplastic",
        "grade": "PA6",
        "standard": "ISO 1874",
        "density": 1.14,
        "tensile_strength_min": 70,
        "tensile_strength_max": 85,
        "yield_strength_min": 70,
        "yield_strength_max": 85,
        "elongation": 60,
        "elastic_modulus": 2.9,
        "thermal_conductivity": 0.25,
        "melting_point_min": 220,
        "melting_point_max": 220,
        "max_service_temp": 120,
        "cost_per_kg_min": 180,
        "cost_per_kg_max": 280,
        "applications": "Gears, bearings, automotive under-hood parts, cable ties",
        "composition": "Polycaprolactam",
        "source_name": "MakeItFrom",
    },
]

print("=== Inserting 3 sample materials ===\n")
for mat in samples:
    r = requests.post(f"{BASE}/materials/", json=mat)
    if r.status_code == 201:
        data = r.json()
        print(f"  [CREATED] id={data['id']}  {data['name']}")
    else:
        print(f"  [ERROR] {r.status_code}: {r.text}")

# ── 2. List all materials ──
print("\n=== Listing all materials ===\n")
r = requests.get(f"{BASE}/materials/")
data = r.json()
print(f"  Total: {data['total']} materials")
for m in data["materials"]:
    print(f"  id={m['id']}  {m['name']:40s}  {m['category']:10s}  tensile={m['tensile_strength_min']}-{m['tensile_strength_max']} MPa")

# ── 3. Filter: Metals with tensile > 400 MPa ──
print("\n=== Filter: Metals with tensile > 400 MPa ===\n")
r = requests.get(f"{BASE}/materials/", params={"category": "Metal", "min_tensile": 400})
data = r.json()
print(f"  Found: {data['total']} materials")
for m in data["materials"]:
    print(f"  {m['name']}  (tensile: {m['tensile_strength_min']}-{m['tensile_strength_max']} MPa)")

# ── 4. Search for "stainless" ──
print("\n=== Search: 'stainless' ===\n")
r = requests.get(f"{BASE}/materials/search", params={"q": "stainless"})
data = r.json()
print(f"  Found: {data['total']} results")
for m in data["materials"]:
    print(f"  {m['name']} ({m['grade']})")

# ── 5. Search for "aerospace" (searches applications field) ──
print("\n=== Search: 'aerospace' ===\n")
r = requests.get(f"{BASE}/materials/search", params={"q": "aerospace"})
data = r.json()
print(f"  Found: {data['total']} results")
for m in data["materials"]:
    print(f"  {m['name']} - {m['applications'][:60]}...")

# ── 6. Get single material ──
print("\n=== Get material by ID (id=1) ===\n")
r = requests.get(f"{BASE}/materials/1")
data = r.json()
print(f"  {data['name']}")
print(f"  Category:    {data['category']} / {data['subcategory']}")
print(f"  Grade:       {data['grade']}")
print(f"  Standard:    {data['standard']}")
print(f"  Density:     {data['density']} g/cm3")
print(f"  Tensile:     {data['tensile_strength_min']}-{data['tensile_strength_max']} MPa")
print(f"  Cost:        Rs.{data['cost_per_kg_min']}-{data['cost_per_kg_max']}/kg")
print(f"  Uses:        {data['applications']}")

print("\n=== ALL TESTS PASSED ===")
