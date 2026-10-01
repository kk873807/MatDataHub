
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

mat = {
    "name": "AlSiC-8 (Al-SiC Metal Matrix Composite)",
    "category": "Composite",
    "subcategory": "Metal Matrix Composite",
    "source_url": "https://www.lookpolymers.com/polymer_CPS-Technologies-AlSiC-8-Metal-Matrix-Composite.php",
    "extraction_method": "Verified Source Datasheet",
    "density": 2.99,
    "elastic_modulus": 217.5,
    "shear_modulus": 94.2,
    "thermal_conductivity": 180.0,
    "description": "AlSiC-8 (70 vol% SiC). Widely used in thermal management and electronic packaging applications due to its high thermal conductivity, low density, and tailored CTE.",
    "computational_properties": {
        "poissons_ratio": 0.154,
        "fracture_toughness_MPa_m_half": 11.67,
        "hermeticity_atm_cc_s_He": "< 1x10^-9",
        "sic_volume_fraction_pct": 70
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

