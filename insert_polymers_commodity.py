
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials_to_insert = [
    {
        "name": "LDPE (Low-Density Polyethylene)",
        "url": "https://xometry.asia/wp-content/uploads/2021/03/LDPE.pdf"
    },
    {
        "name": "LLDPE (Linear Low-Density Polyethylene)",
        "url": "https://productsandsolutions.pttgcgroup.com/customer-support/files/LL6420A-BROCHURE-TH.pdf, https://media.knowde.com/image/upload/v1697541389/production/Collateral/516351/SLL118-21-enUS-ASTM.pdf"
    },
    {
        "name": "MDPE (Medium-Density Polyethylene)",
        "url": "https://www.makeitfrom.com/material-properties/Medium-Density-Polyethylene-MDPE"
    },
    {
        "name": "UHMWPE (Ultra-High-Molecular-Weight Polyethylene)",
        "url": "https://quickparts.com/wp-content/uploads/2024/05/UHMW-PE.pdf, https://www.tse-industries.com/wp-content/uploads/Plastics-Material-Properties-UHMW.pdf"
    },
    {
        "name": "PET (Polyethylene Terephthalate)",
        "url": "https://apm.matweb.com/reference/polyester.aspx, https://www.specialchem.com/plastics/document/arnite-a08-100-unreinforced-polyethylene-terephthalate"
    },
    {
        "name": "PBT (Polybutylene Terephthalate)",
        "url": "https://datasheets.globalspec.com/ds/polyplastics-usa/209aw-ef2001-iso/4b2c758b-c3f7-4046-8f93-bbfc86ecd0ba"
    },
    {
        "name": "PS (Polystyrene, General Purpose)",
        "url": "https://www.makeitfrom.com/material-properties/General-Purpose-Polystyrene-GPPS"
    },
    {
        "name": "HIPS (High Impact Polystyrene)",
        "url": "https://modernplastics.com//wp-content/uploads/2015/05/HIPS.pdf"
    },
    {
        "name": "EPS (Expanded Polystyrene)",
        "url": "https://xometry.pro/wp-content/uploads/2025/07/EPS-Expanded-Polystyrene.pdf",
        "desc": "Reference density 30 kg/m3 basis."
    },
    {
        "name": "PVC (Polyvinyl Chloride, Flexible)",
        "url": "https://en.wikipedia.org/wiki/Polyvinyl_chloride",
        "desc": "Flexible PVC."
    },
    {
        "name": "CPVC (Chlorinated Polyvinyl Chloride)",
        "url": "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-CPVC.pdf"
    },
    {
        "name": "EVA (Ethylene Vinyl Acetate)",
        "url": "https://www.exxonmobilchemical.com/en/chemicals/webapi/dps/v1/datasheets/150000000144/0/en"
    },
    {
        "name": "PLA (Polylactic Acid)",
        "url": "https://3dp.seas.harvard.edu/files/2023/01/PLAMDS.pdf"
    }
]

count = 0
for m in materials_to_insert:
    res = supabase.table("materials").select("id").eq("name", m["name"]).execute()
    
    payload = {
        "name": m["name"],
        "category": "Polymer",
        "subcategory": "Commodity Thermoplastics",
        "source_url": m["url"],
        "source_name": "Verified Sources",
        "extraction_method": "Verified Source Datasheet"
    }
    if "desc" in m:
        payload["description"] = m["desc"]
        
    if len(res.data) > 0:
        supabase.table("materials").update(payload).eq("name", m["name"]).execute()
    else:
        supabase.table("materials").insert(payload).execute()
    count += 1

print(f"Inserted/Updated {count} commodity polymers!")

