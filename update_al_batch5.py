
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

updates = {
    "Aluminium Alloy 6060 T5  Extrusions_144": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6060-T5--Extrusions_144.ashx",
        "ys": 120, "ts": 160, "el": 8
    },
    "Aluminium Alloy 6061 T6 Extrusions_145": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6061-T6-Extrusions_145.ashx",
        "ys": 240, "ts": 260, "el": 8
    },
    "Aluminium Alloy 6063 0 Extrusions_160": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6063-0-Extrusions_160.ashx",
        "ys": 50, "ts": 130, "el": 18
    },
    "Aluminium Alloy 6063 T4 Extruded Rod and Bar_159": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6063-T4-Extruded-Rod-and-Bar_159.ashx",
        "ys": 90, "ts": 130, "el": 14
    },
    "Aluminium Alloy 6063 T6 Extrusions_158": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6063-T6-Extrusions_158.ashx",
        "ys": 170, "ts": 215, "el": 8
    },
    "Aluminium Alloy 6063A T4 Extrusions_161": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6063A-T4-Extrusions_161.ashx",
        "ys": 90, "ts": 150, "el": 12
    },
    "Aluminium Alloy 6063A T6 Extrusions_339": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6063A-T6-Extrusions_339.ashx",
        "ys": 190, "ts": 230, "el": 6
    },
    "Aluminium Alloy 6082 0 Sheet_146": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6082-0-Sheet_146.ashx",
        "ys": 85, "ts": 130, "el": 14
    },
    "Aluminium Alloy 6082 T4 Extrusions_147": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6082-T4-Extrusions_147.ashx",
        "ys": 110, "ts": 205, "el": 14
    },
    "Aluminium Alloy 6082 T6 Extrusions_338": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6082-T6-Extrusions_338.ashx",
        "ys": 250, "ts": 290, "el": 8
    },
    "Aluminium Alloy 6082 T6T651 Plate_148": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6082-T6T651-Plate_148.ashx",
        "ys": 240, "ts": 295, "el": 8
    },
    "Aluminium Alloy 6082 T6T651 Sheet_335": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6082-T6T651-Sheet_335.ashx",
        "ys": 255, "ts": 310, "el": 8
    },
    "Aluminium Alloy 6101 T6 Extrusions Bar_356": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6101-T6-Extrusions-Bar_356.ashx",
        "ys": 170, "ts": 200, "el": 8
    },
    "Aluminium Alloy 6101A T6 Extrusions Bar_357": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6101A-T6-Extrusions-Bar_357.ashx",
        "ys": 170, "ts": 200, "el": 8
    },
    "Aluminium Alloy 6101B T6 Extrusions_358": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6101B-T6-Extrusions_358.ashx",
        "ys": 160, "ts": 200, "el": 8
    },
    "Aluminium Alloy 6106 T6 Extrusions_154": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6106-T6-Extrusions_154.ashx",
        "ys": 200, "ts": 250, "el": 8
    },
    "Aluminium Alloy 6262 T6 Extrusions_156": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6262-T6-Extrusions_156.ashx",
        "ys": 240, "ts": 260, "el": 10
    },
    "Aluminium Alloy Aalcopanel Composite Panels_258": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-Aalcopanel-Composite-Panels_258.ashx",
        "ys": None, "ts": None, "el": None, "desc": "Product data for aluminium composite panels, not a standard alloy. Data is indicative only; consult full specifications."
    },
    "Aluminium Alloy Cleaning Aluminium_52": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-Cleaning-Aluminium_52.ashx",
        "ys": None, "ts": None, "el": None, "desc": "General cleaning guide, no property table. Data is indicative only."
    },
    "Aluminium Alloy DNV Certified Marine Extrusions Extrusions_419": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-DNV-Certified-Marine-Extrusions-Extrusions_419.ashx",
        "ys": None, "ts": None, "el": None, "desc": "Stock range for 6082 T6 marine extrusions. Data is indicative only; consult full specifications."
    }
}

count = 0
for name, data in updates.items():
    payload = {
        "source_url": data["url"],
        "source_name": "Aalco Verified Source",
        "extraction_method": "Verified Source Datasheet",
        "yield_strength_min": data["ys"],
        "tensile_strength_min": data["ts"],
        "elongation": data["el"]
    }
    
    if "desc" in data:
        payload["description"] = data["desc"]
        payload["subcategory"] = "Information Guide"
        
    res = supabase.table("materials").update(payload).eq("name", name).execute()
    count += 1
    
print(f"Updated {count} materials in batch 5.")

