
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# Delete invalid cast variants
dups = ["Aluminum Bronze C95400 (Cold Drawn)", "Aluminum Bronze C95400 (Hot Rolled)"]
supabase.table("materials").delete().in_("name", dups).execute()

updates = {
    "Aluminium Alloy GAL C250 Precision Milled Plate_457": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-GAL-C250-Precision-Milled-Plate_457.ashx",
        "ys": 125, "ts": 275, "el": 15
    },
    "Aluminium Alloy J57S Anodising Quality Aluminium Sheet Sheet_418": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-J57S-Anodising-Quality-Aluminium-Sheet-Sheet_418.ashx",
        "ys": 115, "ts": 145, "el": 6
    },
    "Aluminium Alloy PLANCAST PLUS PLATE 5754_456": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-PLANCAST-PLUS-PLATE-5754_456.ashx",
        "ys": 130, "ts": 220, "el": 12
    },
    "Aluminium Alloy Transition Joint_55": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-Transition-Joint_55.ashx",
        "ys": None, "ts": None, "el": None, "desc": "Tri-Plate aluminium/steel marine joint, Lloyds approved."
    },
    "Aluminosilicate Glass": {
        "url": "https://www.makeitfrom.com/material-properties/Aluminosilicate-Glass, https://matmatch.com/learn/material/aluminosilicate-glass",
        "ys": None, "ts": 70, "el": 0
    },
    "Aluminosilicate Glass (Sheet)": {
        "url": "https://www.americanelements.com/aluminosilicate-glass-sheet",
        "ys": None, "ts": 70, "el": 0
    },
    "Aluminosilicate Glass (Tube)": {
        "url": "https://www.goodfellow.com/usa/aluminosilicate-glass-tube-group, https://www.samaterials.com/al6109-aluminosilicate-glass-tube.html",
        "ys": None, "ts": 70, "el": 0
    },
    "Aluminum Bronze C95400": {
        "url": "https://www.azom.com/article.aspx?ArticleID=6291, https://www.matweb.com/search/datasheet.aspx?matguid=b950d0d72b5b467689f2d9c5d9030ae8",
        "ys": 220, "ts": 515, "el": 12
    },
    "Aluminum Bronze C95400 (Annealed)": {
        "url": "https://www.azom.com/article.aspx?ArticleID=6291",
        "ys": None, "ts": None, "el": None, "desc": "Process Only (Source provides annealing procedure but no explicit annealed mechanicals)"
    },
    "Aluminum Bronze C95400 (Quenched & Tempered)": {
        "url": "https://www.azom.com/article.aspx?ArticleID=6291, https://diversifiedbronze.com/resources/bronze-alloys/c95400-aluminum-bronze.html",
        "ys": 310, "ts": 620, "el": 8
    }
}

count = 0
for name, data in updates.items():
    payload = {
        "source_url": data["url"],
        "source_name": "Verified Source",
        "extraction_method": "Verified Source Datasheet",
        "yield_strength_min": data.get("ys"),
        "tensile_strength_min": data.get("ts"),
        "elongation": data.get("el")
    }
    if "desc" in data:
        payload["description"] = data["desc"]
        
    supabase.table("materials").update(payload).eq("name", name).execute()
    count += 1

guides = [
    ("Aluminium Alloy EN Standards for Aluminium Extrusions_48", "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-EN-Standards-for-Aluminium-Extrusions_48.ashx", "Standards guide"),
    ("Aluminium Alloy EN Standards for Rolled Aluminium_51", "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-EN-Standards-for-Rolled-Aluminium_51.ashx", "Standards guide (plate and sheet)"),
    ("Aluminium Alloy Fabrication of Aluminium_53", "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-Fabrication-of-Aluminium_53.ashx", "Fabrication guide"),
    ("Aluminium Alloy Introduction to Aluminium and its alloys_9", "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-Introduction-to-Aluminium-and-its-alloys_9.ashx", "Introductory guide"),
    ("Aluminium Alloy Material Safety Aluminium_251", "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-Material-Safety-Aluminium_251.ashx", "Safety guide"),
    ("Aluminium Alloy R0HS Aluminium_123", "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-R0HS-Aluminium_123.ashx", "RoHS compliance information"),
    ("Aluminium Alloy Specifications_42", "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-Specifications_42.ashx", "Specifications guide"),
    ("Aluminium Alloy Temper Designations_93", "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-Temper-Designations_93.ashx", "Temper reference guide")
]

for name, url, desc in guides:
    supabase.table("materials").update({
        "source_url": url,
        "source_name": "Aalco Reference Guide",
        "extraction_method": "Verified Source Datasheet",
        "yield_strength_min": None,
        "tensile_strength_min": None,
        "elongation": None,
        "subcategory": "Information Guide",
        "description": desc
    }).eq("name", name).execute()
    count += 1

print(f"Processed final batch of {count} items.")

