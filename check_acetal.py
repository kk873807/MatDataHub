import requests

API_BASE = "https://matdatahub-api.onrender.com/api/v1"
res = requests.get(f"{API_BASE}/materials/", params={"per_page": 1000})
if res.status_code == 200:
    data = res.json()
    mats = data.get("materials", [])
    
    target = None
    for m in mats:
        if "acetal" in m.get("name", "").lower():
            target = m
            break
            
    if target:
        print("Found Material:")
        print(f"Name: {target.get('name')}")
        print(f"embodied_carbon: {target.get('embodied_carbon')}")
        print(f"cost_per_kg_min: {target.get('cost_per_kg_min')}")
        print(f"cost_per_kg_max: {target.get('cost_per_kg_max')}")
    else:
        print("Acetal not found.")
else:
    print("API fetch failed")
