
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

mat = {
    "name": "B4C-Al (Metamic / Neutron Absorber Composite)",
    "category": "Composite",
    "subcategory": "Metal Matrix Composite",
    "source_url": "https://ww2.nrc.gov/docs/ML1307/ML13079A685.pdf, https://holtecinternational.com/products-and-services/innovative-technologies/neutronabsorbermaterial/",
    "extraction_method": "Verified Source Datasheet",
    "tensile_strength_max": 250.0,
    "description": "Al-B4C Metal Matrix Composite (e.g. Metamic, Boralyn). Al-6061 powder matrix with nuclear-grade B4C. Specifically used for neutron shielding in dry-cask nuclear storage.",
    "computational_properties": {
        "tensile_strength_range_MPa": "227 - 276",
        "yield_strength_range_MPa": "138 - 227",
        "yield_strength_MPa": 180,
        "b4c_loading_pct": "10 - 33"
    }
}

name = mat["name"]
existing = supabase.table("materials").select("id").eq("name", name).execute()
if existing.data:
    supabase.table("materials").update(mat).eq("name", name).execute()
    print(f"Updated {name}")
else:
    supabase.table("materials").insert(mat).execute()
    print(f"Inserted {name}")

