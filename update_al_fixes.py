
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# 1. Update J57S properties to None, change to Info Guide, update to direct PDF URL
supabase.table("materials").update({
    "yield_strength_min": None,
    "tensile_strength_min": None,
    "elongation": None,
    "subcategory": "Information Guide",
    "description": "Stock range datasheet only. Property data nullified.",
    "source_url": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-J57S-Anodising-Quality-Aluminium-Sheet-Sheet_418.pdf.ashx"
}).eq("name", "Aluminium Alloy J57S Anodising Quality Aluminium Sheet Sheet_418").execute()

# 2. Wipe properties for 356 and 358, append Righton Blackburns fallbacks
supabase.table("materials").update({
    "yield_strength_min": None,
    "tensile_strength_min": None,
    "elongation": None,
    "description": "Properties pending import from 6101A",
    "source_url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6101-T6-Extrusions-Bar_356.ashx, https://www.rightonblackburns.co.uk/datasheets/view/Righton-Blackburns-Ltd_Aluminium-Alloy-6101-T6-Extrusions-Bar_356.pdf"
}).eq("name", "Aluminium Alloy 6101 T6 Extrusions Bar_356").execute()

supabase.table("materials").update({
    "yield_strength_min": None,
    "tensile_strength_min": None,
    "elongation": None,
    "description": "Properties pending import from 6101A",
    "source_url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6101B-T6-Extrusions_358.ashx, https://www.rightonblackburns.co.uk/datasheets/view/Righton-Blackburns-Ltd_Aluminium-Alloy-6101B-T6-Extrusions_358.pdf"
}).eq("name", "Aluminium Alloy 6101B T6 Extrusions_358").execute()

# 3. Append Righton Blackburns fallbacks for 147, 338, 339
fallbacks = {
    "Aluminium Alloy 6082 T4 Extrusions_147": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6082-T4-Extrusions_147.ashx, https://www.rightonblackburns.co.uk/datasheets/view/Righton-Blackburns-Ltd_Aluminium-Alloy-6082-T4-Extrusions_147.pdf",
    "Aluminium Alloy 6082 T6 Extrusions_338": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6082-T6-Extrusions_338.ashx, https://www.rightonblackburns.co.uk/datasheets/view/Righton-Blackburns-Ltd_Aluminium-Alloy-6082-T6-Extrusions_338.pdf",
    "Aluminium Alloy 6063A T6 Extrusions_339": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-6063A-T6-Extrusions_339.ashx, https://www.rightonblackburns.co.uk/datasheets/view/Righton-Blackburns-Ltd_Aluminium-Alloy-6063A-T6-Extrusions_339.pdf"
}
for name, url in fallbacks.items():
    supabase.table("materials").update({"source_url": url}).eq("name", name).execute()

# 4. Update Direct PDF Links for the verified 8 (excluding 418 which was done)
pdf_links = {
    "Aluminium Alloy 6060 T5  Extrusions_144": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-6060-T5--Extrusions_144.pdf.ashx",
    "Aluminium Alloy 6061 T6 Extrusions_145": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-6061-T6-Extrusions_145.pdf.ashx",
    "Aluminium Alloy 6106 T6 Extrusions_154": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-6106-T6-Extrusions_154.pdf.ashx",
    "Aluminium Alloy 6063 T6 Extrusions_158": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-6063-T6-Extrusions_158.pdf.ashx",
    "Aluminium Alloy 6063 0 Extrusions_160": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-6063-0-Extrusions_160.pdf.ashx",
    "Aluminium Alloy DNV Certified Marine Extrusions Extrusions_419": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-DNV-Certified-Marine-Extrusions-Extrusions_419.pdf.ashx",
    "Aluminium Alloy PLANCAST PLUS PLATE 5754_456": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-PLANCAST-PLUS-PLATE-5754_456.pdf.ashx",
    "Aluminium Alloy GAL C250 Precision Milled Plate_457": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-GAL-C250-Precision-Milled-Plate_457.pdf.ashx"
}
for name, url in pdf_links.items():
    supabase.table("materials").update({"source_url": url}).eq("name", name).execute()

print("Finetuning completed!")

