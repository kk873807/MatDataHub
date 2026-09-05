import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

bom_fetch_old = 'bom_mat_options = {m["id"]: m["name"] for m in all_mats["data"].get("materials", [])} if all_mats["ok"] else {}'

bom_fetch_new = """
                                    bom_mat_options = {m["id"]: m["name"] for m in all_mats["data"].get("materials", [])} if all_mats["ok"] else {}
                                    
                                    # Fetch custom materials if advanced
                                    if user_tier == "advanced":
                                        cust_mats = api_get("/materials/custom/mine")
                                        if cust_mats["ok"] and cust_mats["data"]:
                                            for cm in cust_mats["data"]:
                                                # Use negative IDs to distinguish custom materials in the UI
                                                bom_mat_options[-cm["id"]] = f"🔒 {cm['name']}"
"""

content = content.replace(bom_fetch_old, bom_fetch_new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated BOM Synthesizer to fetch custom materials.")
