import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Let's write a small separate script that uses the existing api functions
test_script = """
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
"""
with open("test_api.py", "w") as f:
    f.write(test_script)
