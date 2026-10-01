
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

mat = {
    "name": "C/SiC (Ceramic Matrix Composite)",
    "category": "Composite",
    "subcategory": "Ceramic Matrix Composite",
    "source_url": "https://ntrs.nasa.gov/api/citations/20020072848/downloads/20020072848.pdf, https://elib.dlr.de/92428, https://tf.uns.ac.rs/publikacije/PAC/pdf/PAC%2066%2001.pdf",
    "extraction_method": "Verified Source Datasheet",
    "density": 1.99,
    "tensile_strength_max": 413.0, # ~60 ksi from NASA CVI T-300
    "thermal_conductivity": 135.0, # avg of 110-160 from SIGRASIC
    "description": "Carbon fiber reinforced Silicon Carbide (e.g. 2D CVI C/SiC or SGL SIGRASIC). Liquid silicon infiltrated for automotive brake discs (e.g. Porsche PCCB) due to thermal stability, low wear, and high thermal conductivity.",
    "computational_properties": {
        "thermal_conductivity_range_W_mK": "110 - 160",
        "application": "Automotive brake discs, high-temperature structural components"
    }
}

name = mat["name"]
res = supabase.table("materials").update(mat).eq("name", name).execute()
print(f"Updated {name}")

