import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old_code = """                # Fetch materials for dropdown
                import requests
                try:
                    res = requests.get(f"{API_BASE}/materials?skip=0&limit=500")
                    if res.status_code == 200:
                        mats = res.json()
                        mat_options = {m["name"]: m["id"] for m in mats}"""

new_code = """                # Fetch materials for dropdown
                import requests
                try:
                    res = fetch_all_materials()
                    if res.get("ok") and res.get("data"):
                        data = res["data"]
                        mats = data.get("materials", []) if isinstance(data, dict) else data
                        mat_options = {m["name"]: m["id"] for m in mats if isinstance(m, dict) and "name" in m}"""

if old_code in content:
    content = content.replace(old_code, new_code)
    # Also fix the exception handler to print the error
    content = content.replace('st.error("Failed to connect to API.")', 'st.error(f"API Error: {e}")')
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed!")
else:
    print("Could not find the exact code block to replace.")
