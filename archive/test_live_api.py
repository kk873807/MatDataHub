import requests
API_BASE = "https://matdatahub-api.onrender.com/api/v1"
res = requests.get(f"{API_BASE}/materials/")
if res.status_code == 200:
    data = res.json()
    mats = data.get("materials", [])
    if mats:
        print("First material keys:")
        for k, v in mats[0].items():
            print(f"{k}: {v}")
    else:
        print("No materials found in response")
else:
    print(f"Failed to fetch: {res.status_code}")
