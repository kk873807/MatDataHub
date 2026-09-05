from backend.services.material_service import fetch_all_materials
mats = fetch_all_materials()
data = mats.get("data", {}).get("materials", [])
print(f"Total mats: {len(data)}")
nonzero = 0
for m in data:
    c = m.get("embodied_carbon")
    if c and float(c) > 0:
        nonzero += 1
print(f"Mats with embodied_carbon > 0: {nonzero}")
