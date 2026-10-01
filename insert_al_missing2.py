
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials_to_insert = [
    {
        "name": "4032 T6 Aluminum",
        "url": "https://www.makeitfrom.com/material-properties/4032-4032-T6-AlSi12.5MgCuNi-Aluminum, https://www.smithshp.com/assets/pdf/aluminium/high-performance-aluminium/4032-aluminium-english.pdf",
        "ys": 320, "ts": 390, "el": 5, "desc": ""
    },
    {
        "name": "4043 Aluminum",
        "url": "https://www.azom.com/article.aspx?ArticleID=8685, https://en.wikipedia.org/wiki/4043_aluminium_alloy",
        "ys": None, "ts": None, "el": None, "desc": "Welding filler alloy. Properties reflect composition and typical weld metal data."
    },
    {
        "name": "4047 Aluminum",
        "url": "https://www.makeitfrom.com/compare/4047-BAlSi-4-Aluminum/4343-BAlSi-2-AlSi7.5-Aluminum",
        "ys": 64, "ts": 120, "el": None, "desc": "Brazing filler alloy. Liquidus 580 C, brazing 580-600 C."
    },
    {
        "name": "4145 Aluminum",
        "url": "https://aircraftmaterials.com/data/weld/4145.html, https://dl.asminternational.org/alloy-digest/article/51/12/Al-383/6554/ALCOTEC-WELD-FILLER-WIRE-4145Aluminum-Welding-and",
        "ys": None, "ts": None, "el": None, "desc": "Welding filler alloy. Composition and process data only."
    },
    {
        "name": "4643 Aluminum",
        "url": "https://dl.asminternational.org/alloy-digest/article/51/3/Al-324/6484/ALCOTEC-WELD-FILLER-WIRE-4643Silicon-Magnesium, https://saemobilus.sae.org/content/AMS4189K/",
        "ys": None, "ts": None, "el": None, "desc": "Welding filler alloy. Open property table not available."
    },
    {
        "name": "5154 H14 Aluminum",
        "url": "https://www.makeitfrom.com/material-properties/5154-H14-Aluminum, https://en.wikipedia.org/wiki/5154_aluminium_alloy",
        "ys": 230, "ts": 300, "el": 8, "desc": ""
    },
    {
        "name": "5182 H19 Aluminum",
        "url": "https://makeitfrom.com/material-properties/5182-H19-Aluminum, https://en.wikipedia.org/wiki/5182_aluminium_alloy",
        "ys": 360, "ts": 420, "el": 4, "desc": "Can-end temper."
    },
    {
        "name": "5356 Aluminum",
        "url": "https://en.wikipedia.org/wiki/5356_aluminium_alloy, https://airgas.com/product/Welding-Products/Filler-Metal/MIG-Wire-%28GMAW-%26-SAW%29/MIG-Wire---Aluminum/p/HOB535603504",
        "ys": None, "ts": 260, "el": None, "desc": "Welding filler alloy. Properties reflect typical weld metal data (approx 38 ksi tensile)."
    },
    {
        "name": "5456 H112 Aluminum",
        "url": "https://makeitfrom.com/material-properties/5456-H112-Aluminum, https://www.mfgrobots.com/Article/material/metal/39859.html",
        "ys": 165, "ts": 290, "el": 12, "desc": ""
    },
    {
        "name": "6013 T6 Aluminum",
        "url": "https://makeitfrom.com/material-properties/6013-T6-Aluminum, https://en.wikipedia.org/wiki/6013_aluminium_alloy",
        "ys": 350, "ts": 410, "el": 8, "desc": ""
    }
]

count = 0
for m in materials_to_insert:
    res = supabase.table("materials").select("id").eq("name", m["name"]).execute()
    
    payload = {
        "name": m["name"],
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "source_url": m["url"],
        "source_name": "Verified Sources",
        "extraction_method": "Verified Source Datasheet",
        "yield_strength_min": m["ys"],
        "tensile_strength_min": m["ts"],
        "elongation": m["el"]
    }
    if m["desc"]:
        payload["description"] = m["desc"]
        
    if len(res.data) > 0:
        supabase.table("materials").update(payload).eq("name", m["name"]).execute()
    else:
        supabase.table("materials").insert(payload).execute()
    count += 1

print(f"Inserted/Updated {count} missing alloys!")

