
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials_to_insert = [
    {
        "name": "EPDM Rubber",
        "url": "https://www.makeitfrom.com/material-properties/Ethylene-Propylene-Diene-Rubber-EPDM-EPT, https://o-ring.info/en/o-ring/technical%20handbook/06%20-%20eriks%20nv%20-%20o-ring%20technical%20handbook%20-%20basic%20elastomers.pdf, https://allsealsinc.com/pdfs/dichtomatik_oring_handbook.pdf, https://en.wikipedia.org/wiki/EPDM_rubber"
    },
    {
        "name": "Nitrile Rubber (NBR)",
        "url": "https://www.makeitfrom.com/material-properties/Acrylonitrile-Nitrile-Butadiene-Rubber-NBR-Buna-N, https://en.wikipedia.org/wiki/Nitrile_rubber, http://allsealsinc.com/03_Elastomers-Materials.pdf"
    },
    {
        "name": "HNBR (Hydrogenated Nitrile Butadiene Rubber)",
        "url": "https://www.makeitfrom.com/material-properties/Hydrogenated-Acrylonitrile-Butadiene-Rubber-HNBR-HSN, https://o-ring.info/en/o-ring/technical%20handbook/06%20-%20eriks%20nv%20-%20o-ring%20technical%20handbook%20-%20basic%20elastomers.pdf, https://trp.co.uk/materials/datasheets/"
    },
    {
        "name": "SBR (Styrene-Butadiene Rubber)",
        "url": "https://www.makeitfrom.com/material-properties/Styrene-Butadiene-Rubber-SBR-Buna-S, http://allsealsinc.com/03_Elastomers-Materials.pdf"
    },
    {
        "name": "FKM (Viton / Fluoroelastomer)",
        "url": "https://www.makeitfrom.com/material-properties/Fluorocarbon-Rubber-FKM-FPM, https://www.viton.com/en/-/media/files/viton/viton-selection-guide.pdf, https://www.parker.com/us/en/divisions/o-ring-and-engineered-seals-division/resources/oring-ehandbook/oring-elastomers/material-selection-guide.html"
    },
    {
        "name": "FFKM (Perfluoroelastomer / Kalrez)",
        "url": "https://www.makeitfrom.com/material-properties/Perfluoroelastomer-FFKM, https://www.dymseal.com/pdf/Kalrez%20Physical%20Properties%20&%20Compound%20Comparisons.pdf, https://www.parrinst.com/wp-content/uploads/downloads/2011/07/Parr_DuPont-Kalrez-O-ring-Materials-Corrosion-Info.pdf"
    },
    {
        "name": "IIR (Butyl Rubber)",
        "url": "https://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=93, https://www.parker.com/us/en/divisions/o-ring-and-engineered-seals-division/resources/oring-ehandbook/oring-elastomers/material-selection-guide.html, https://allsealsinc.com/pdfs/dichtomatik_oring_handbook.pdf"
    },
    {
        "name": "CSM (Chlorosulfonated Polyethylene / Hypalon)",
        "url": "https://www.makeitfrom.com/material-properties/Chlorosulfonated-Polyethylene-Rubber-CSM, https://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=93, http://allsealsinc.com/03_Elastomers-Materials.pdf"
    },
    {
        "name": "ACM (Polyacrylate Rubber)",
        "url": "https://www.makeitfrom.com/material-properties/Polyacrylate-Rubber-ACM, https://www.parker.com/us/en/divisions/o-ring-and-engineered-seals-division/resources/oring-ehandbook/oring-elastomers/material-selection-guide.html"
    },
    {
        "name": "TPU (Thermoplastic Polyurethane)",
        "url": "https://download.basf.com/p1/8a8082587fd4b608017fd6411cdd6d63/en/Elastollan%3Csup%3E%C2%AE%3Csup%3E_%E2%80%93_Thermoplastic_Polyurethane_Elastomers_%28TPU%29_-_Product_Range_Range_Chart_English.pdf, https://omnexus.specialchem.com/product-categories/tpes-tpvs-tpu-or-tpe-u-thermoplastic-polyurethane-tpu-ester-ether, https://www.americanchemistry.com/content/download/4863/file/Thermoplastic-Polyurethanes-Bridge-The-Gap-Between-Rubber-and-Plastics.pdf"
    },
    {
        "name": "TPE (Thermoplastic Elastomer)",
        "url": "https://www.hexpol.com/tpe/?p=3884, https://business.specialchem.com/blog/top-25-most-popular-plastics-and-elastomers-on-specialchem"
    },
    {
        "name": "TPV (Thermoplastic Vulcanizate / Santoprene)",
        "url": "https://upmold.com/wp-content/uploads/data-sheet/TPV-Santoprene_101-73.pdf, https://www.phmolds.com/wp-content/uploads/2016/09/TPV-ExxonMobil-Santoprene-101-80-Black.pdf, https://www.phmolds.com/wp-content/uploads/2016/09/TPV-ExxonMobil-Santoprene-101-64-Black.pdf, https://en.wikipedia.org/wiki/Thermoplastic_vulcanizates",
        "desc": "[Caution: Santoprene/TPV TDS values are typically for fan-gated injection-moulded plaques measured across flow direction (compression set at 25% deflection). Do not directly compare numeric values against thermoset rubbers measured per ASTM D412/D395 without standardizing test conditions.]"
    }
]

count = 0
for m in materials_to_insert:
    res = supabase.table("materials").select("id, description").eq("name", m["name"]).execute()
    
    desc = m.get("desc", "")
    desc += "\n[Note: Ensure PDFs hosted by distributors are periodically archived as URLs may rot if distributors update their directories.]"
    desc = desc.strip()
    
    payload = {
        "name": m["name"],
        "category": "Polymer",
        "subcategory": "Elastomers & Rubbers",
        "source_url": m["url"],
        "source_name": "Verified Sources",
        "extraction_method": "Verified Source Datasheet",
        "description": desc
    }
        
    if len(res.data) > 0:
        supabase.table("materials").update(payload).eq("name", m["name"]).execute()
    else:
        supabase.table("materials").insert(payload).execute()
    count += 1

print(f"Inserted/Updated {count} elastomer polymers!")

