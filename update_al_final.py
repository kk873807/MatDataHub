
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

name = "EN AC 47100 47100 F AISi12Cu1Fe Cast Aluminum"
urls = "https://www.makeitfrom.com/material-properties/EN-AC-47100-47100-F-AISi12Cu1Fe-Cast-Aluminum, https://matmatch.com/materials/minfm17131-en-1706-grade-ac-47100-f, http://www.steelnumber.com/en/steel_alloy_composition_eu.php?name_id=1252, https://www.raffmetal.com/wp-content/uploads/sites/4/EN-47100-AlSi12Cu1Fe-1.pdf"

res = supabase.table("materials").update({
    "source_url": urls,
    "source_name": "MakeItFrom / Raffmetal Datasheet",
    "extraction_method": "Verified Source Datasheet",
    "yield_strength_min": 140,
    "tensile_strength_min": 240,
    "elongation": 1
}).eq("name", name).execute()

print(f"Updated EN AC 47100")

