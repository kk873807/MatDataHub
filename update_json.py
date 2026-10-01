
import os, json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

with open("payload.json", "r") as f:
    data = json.load(f)

for item in data["materials"]:
    name = item["name"]
    
    comp_parts = []
    for k, v in item["chemical_composition_wt_pct"].items():
        comp_parts.append(f"{k}: {v}%")
    comp_str = ", ".join(comp_parts)

    urls = ", ".join([link["url"] for link in item["source_links"]])
    
    ys = None
    ts = None
    el = None

    cond = item["conditions"][0]["mechanical_properties"]
    
    if "yield_strength_MPa" in cond:
        ys = cond["yield_strength_MPa"].get("min")
    elif "yield_strength_MPa_Rp0_2" in cond:
        ys = cond["yield_strength_MPa_Rp0_2"].get("min")
        
    if "tensile_strength_MPa" in cond:
        if isinstance(cond["tensile_strength_MPa"], dict):
            ts = cond["tensile_strength_MPa"].get("typical") or cond["tensile_strength_MPa"].get("min")
        else:
            ts = cond["tensile_strength_MPa"]
    elif "tensile_strength_MPa_Rm" in cond:
        ts = cond["tensile_strength_MPa_Rm"].get("min")
        
    if "elongation_at_fracture_pct_A5" in cond:
        el = cond["elongation_at_fracture_pct_A5"].get("min")
    elif "total_elongation_pct" in cond:
        el = cond["total_elongation_pct"].get("min")

    desc = item.get("steel_class", "")

    # Upsert logic based on name
    res = supabase.table("materials").select("id").eq("name", name).execute()
    
    payload = {
        "name": name,
        "category": "Metal",
        "subcategory": "Bainitic Steel",
        "composition": comp_str,
        "source_url": urls,
        "source_name": "Valid Manufacturer/Research Source",
        "description": desc,
        "extraction_method": "JSON Import",
        "yield_strength_min": ys,
        "tensile_strength_min": ts,
        "elongation": el
    }
    
    if res.data:
        # Update
        supabase.table("materials").update(payload).eq("id", res.data[0]["id"]).execute()
        print(f"Updated {name}")
    else:
        # Insert
        supabase.table("materials").insert(payload).execute()
        print(f"Inserted {name}")

print("Done!")

