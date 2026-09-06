
import sys
sys.path.append("frontend")
from app import fetch_all_materials
res = fetch_all_materials()
if res.get("ok"):
    mats = res["data"]["materials"]
    for m in mats[:2]:
        print(f"Name: {m.get('name')}")
        print(f"cost_per_kg: {m.get('cost_per_kg')}")
        print(f"cost_per_kg_min: {m.get('cost_per_kg_min')}")
        print(f"cost_per_kg_max: {m.get('cost_per_kg_max')}")
