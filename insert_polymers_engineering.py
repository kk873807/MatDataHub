
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials_to_insert = [
    {
        "name": "PA 11 (Nylon 11)",
        "url": "https://www.goodfellow.com/usa/rilsan-bmntld-nylon-11-rod-group, https://hpp.arkema.com/assets/arkema/TDS_RILSAN%C2%AE%20PA11%20T%20GREY%207310%20AC_ko_WW.pdf"
    },
    {
        "name": "PA 12 (Nylon 12)",
        "url": "https://www.bopla.de/fileadmin/product_data/00_Materialdatenblaetter/PA_12_LR7MHI_Vestamid/PA_DB_12_LR7MHI_Vestamid.pdf, https://hpp.arkema.com/assets/arkema/TDS_RILSAMID%C2%AE%20AESNO%20MED_en_WW.pdf"
    },
    {
        "name": "PA 46 (Nylon 46)",
        "url": "https://plasticsfinder.envalior.com/api/document/tech/Stanyl%C2%AE%20HGR3-W/O4uVuqP5d/en"
    },
    {
        "name": "PC/ABS (Polycarbonate/ABS Blend)",
        "url": "https://plasticker.de/docs/recybase/4089_1768399051.pdf, https://plasticker.de/docs/recybase/31599_1724311132.pdf"
    },
    {
        "name": "PPE/PS (Polyphenylene Ether / Noryl)",
        "url": "https://www.protolabs.com/media/ipwe0ehh/2026-026-cnc-material-data-sheet_ppe-ps-noryl-265.pdf"
    },
    {
        "name": "POM-H (Acetal Homopolymer / Delrin)",
        "url": "https://www.protolabs.com/media/zlknjwmd/2026-026-cnc-material-data-sheet_pom-h.pdf, https://www.curbellplastics.com/wp-content/uploads/2022/11/Acetal-Data-Sheet.pdf"
    },
    {
        "name": "POM-C (Acetal Copolymer / Celcon)",
        "url": "https://www.scribd.com/document/437515969/Polyacetal"
    },
    {
        "name": "SAN (Styrene Acrylonitrile)",
        "url": "https://www.kkpc.com/download/?seq=7273"
    },
    {
        "name": "ASA (Acrylonitrile Styrene Acrylate)",
        "url": "https://www.makeitfrom.com/material-properties/Acrylonitrile-Styrene-Acrylate-ASA"
    },
    {
        "name": "MABS (Methyl Methacrylate ABS)",
        "url": "https://www.uniboxinfo.com/datasheets/terlux.pdf"
    }
]

count = 0
for m in materials_to_insert:
    res = supabase.table("materials").select("id").eq("name", m["name"]).execute()
    
    payload = {
        "name": m["name"],
        "category": "Polymer",
        "subcategory": "Engineering Thermoplastics",
        "source_url": m["url"],
        "source_name": "Verified Sources",
        "extraction_method": "Verified Source Datasheet"
    }
        
    if len(res.data) > 0:
        supabase.table("materials").update(payload).eq("name", m["name"]).execute()
    else:
        supabase.table("materials").insert(payload).execute()
    count += 1

print(f"Inserted/Updated {count} engineering polymers!")

