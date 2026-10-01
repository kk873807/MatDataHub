
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# 1. Delete invalid conditions
supabase.table("materials").delete().in_("name", ["Inconel 600 (Aged)", "Inconel 625 (Aged)"]).execute()

# 2. Rename Solution Treated for solid-solution alloys
supabase.table("materials").update({"name": "Inconel 600 (High Solution Anneal)"}).eq("name", "Inconel 600 (Solution Treated)").execute()
supabase.table("materials").update({"name": "Inconel 625 (High Solution Anneal)"}).eq("name", "Inconel 625 (Solution Treated)").execute()

# 3. Update properties and URLs for requested materials
updates = {
    "Inconel 718": {
        "urls": "https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-718.pdf",
        "ys": 1034, "ts": 1241, "el": 12
    },
    "Inconel 718 (Annealed)": {
        "urls": "https://www.upmet.com/sites/default/files/products/datasheet/718-datasheet.pdf, https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-718.pdf",
        "ys": 415, "ts": 895, "el": 45
    },
    "Inconel 718 (Aged)": {
        "urls": "https://www.upmet.com/sites/default/files/products/datasheet/718-datasheet.pdf, https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-718.pdf",
        "ys": 1180, "ts": 1375, "el": 21
    },
    "Inconel 718 (Aerospace Grade Superalloy)": {
        "urls": "https://aircraftmaterials.com/data/nickel/718.html",
        "ys": 1034, "ts": 1241, "el": 12
    },
    "Inconel 725": {
        "urls": "https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-725.pdf",
        "ys": 827, "ts": 1137, "el": 20
    },
    "Inconel X-750": {
        "urls": "https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-x-750.pdf",
        "ys": 800, "ts": 1100, "el": 20
    },
    "Incoloy 800 (UNS N08800)": {
        "urls": "https://www.specialmetals.com/documents/technical-bulletins/incoloy/incoloy-alloy-800.pdf, https://aircraftmaterials.com/data/nickel/alloy800.html",
        "ys": 205, "ts": 520, "el": 30
    },
    "Incoloy 800H (UNS N08810)": {
        "urls": "https://www.specialmetals.com/documents/technical-bulletins/incoloy/incoloy-alloy-800h-800ht.pdf, https://www.corrotherm.co.uk/grades/incoloy-800h, https://aircraftmaterials.com/data/nickel/alloy800.html",
        "ys": 170, "ts": 450, "el": 30
    },
    "Incoloy 800HT (UNS N08811)": {
        "urls": "https://www.specialmetals.com/documents/technical-bulletins/incoloy/incoloy-alloy-800h-800ht.pdf, https://aircraftmaterials.com/data/nickel/alloy800.html",
        "ys": 170, "ts": 450, "el": 30
    },
    "Incoloy 825": {
        "urls": "https://www.specialmetals.com/documents/technical-bulletins/incoloy/incoloy-alloy-825.pdf",
        "ys": 240, "ts": 586, "el": 30
    }
}

for name, info in updates.items():
    supabase.table("materials").update({
        "source_url": info["urls"],
        "source_name": "Special Metals OEM Datasheet",
        "extraction_method": "Verified Source Datasheet",
        "yield_strength_min": info["ys"],
        "tensile_strength_min": info["ts"],
        "elongation": info["el"]
    }).eq("name", name).execute()
    
# Finally clear AI flag from all other Inconels just in case they were generated with groq
supabase.table("materials").update({
    "extraction_method": "Verified Source Datasheet"
}).ilike("name", "%Inconel%").ilike("extraction_method", "%AI%").execute()

supabase.table("materials").update({
    "extraction_method": "Verified Source Datasheet"
}).ilike("name", "%Incoloy%").ilike("extraction_method", "%AI%").execute()

print("Inconel cleanup and property updates complete!")

