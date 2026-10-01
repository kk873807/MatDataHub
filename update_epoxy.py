
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

up = {
    "source_url": "https://acpcomposites.com/wp-content/uploads/2023/12/Mechanical-Properties-of-Carbon-Fiber-Composite-Materials.pdf, https://swh.princeton.edu/~maelabs/mae324/glos324/carbonfibercomposite.htm",
    "extraction_method": "Verified Source Datasheet",
    "density": 1.6,
    "tensile_strength_max": 1400.0,
    "elastic_modulus": 135.0,
    "shear_modulus": 5.0,
    "thermal_expansion_coefficient": -0.2,
    "description": "Standard Modulus Carbon Fiber UD / Epoxy composite (Vf = 60%). High longitudinal stiffness, low transverse stiffness."
}
supabase.table("materials").update(up).eq("name", "Epoxy (60% Carbon Fiber UD)").execute()
print("Updated Epoxy UD!")

