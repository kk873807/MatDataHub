
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials_to_insert = [
    {
        "name": "1145 Aluminum",
        "url": "https://www.matweb.com/search/datasheettext.aspx?matid=8761, https://www.azom.com/article.aspx?ArticleID=6621",
        "ys": 165, "ts": 185, "el": 1.5, "desc": "Values typical of H19 temper."
    },
    {
        "name": "1199 Aluminum",
        "url": "https://en.wikipedia.org/wiki/1199_aluminium_alloy, https://aircraftmaterials.com/data/aluminium/1199.html",
        "ys": None, "ts": None, "el": None, "desc": "Composition only (99.99% Al min). Mechanical properties pending reliable open source."
    },
    {
        "name": "2017 Aluminum",
        "url": "https://www.azom.com/article.aspx?ArticleID=8721, https://www.suppliersonline.com/propertypages/2017.asp",
        "ys": 105, "ts": 180, "el": 22, "desc": "Values typical of Annealed (O) temper."
    },
    {
        "name": "2024 T351 Aluminum",
        "url": "https://makeitfrom.com/material-properties/2024-T351-Aluminum, https://www.gabrian.com/wp-content/uploads/2018/10/2024-Aluminum-Alloy-Properties.pdf, https://en.wikipedia.org/wiki/2024_aluminium_alloy",
        "ys": 324, "ts": 470, "el": 19, "desc": ""
    },
    {
        "name": "2090 Aluminum",
        "url": "https://www.azom.com/article.aspx?ArticleID=8715, http://www.matweb.com/search/datasheet.aspx?matguid=a8a1d8e79fee4c01962b764e7cedf18a",
        "ys": 480, "ts": 550, "el": 7, "desc": "Values typical of T8 temper."
    },
    {
        "name": "2099 T83 Aluminum",
        "url": "https://www.smithmetal.com/pdf/lithium/2099-lithium.pdf, https://dl.asminternational.org/alloy-digest/article/54/12/Al-398/6849/2099-T83-T8E67High-Strength-Low-Density-Aluminum",
        "ys": 510, "ts": 545, "el": 10, "desc": "Aluminum-Lithium alloy."
    },
    {
        "name": "2124 T851 Aluminum",
        "url": "https://www.makeitfrom.com/material-properties/2124-2124-T851-AlCu4Mg1A-3.1354-Aluminum, https://dl.asminternational.org/alloy-digest/article/55/7/Al-399/6904/ALCOA-2124-PLATEAerospace-Aluminum-Alloy",
        "ys": 410, "ts": 460, "el": 8, "desc": ""
    },
    {
        "name": "2324 T39 Aluminum",
        "url": "https://dl.asminternational.org/alloy-digest/article/6342/ALCOA-2324-T39-PLATEHigh-Strength-Aerospace-Plate, https://metals.ulprospector.com/datasheet/e272680/alcoa-2324-t39",
        "ys": None, "ts": None, "el": None, "desc": "Open property table not available (abstract only)."
    },
    {
        "name": "3005 H14 Aluminum",
        "url": "https://www.makeitfrom.com/compare/1200-H14-Aluminum/3005-H14-Aluminum, https://www.delta-trading.de/en/product-overview/aluminium-heavy-metals/alloy-30525-en-aw-3005-aluminium/",
        "ys": 170, "ts": 190, "el": 8, "desc": ""
    },
    {
        "name": "3105 H14 Aluminum",
        "url": "https://www.mfgrobots.com/Article/material/metal/38876.html, https://www.kloecknermetals.com/?p=14224",
        "ys": 150, "ts": 170, "el": 6, "desc": ""
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

print(f"Inserted {count} missing alloys!")

