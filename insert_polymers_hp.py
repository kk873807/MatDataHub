
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials_to_insert = [
    {
        "name": "PEI (Polyetherimide / Ultem)",
        "url": "https://ca.electro-wind.com/web-files/Sabic/ultem-datasheet.pdf"
    },
    {
        "name": "PPS (Polyphenylene Sulfide / Ryton)",
        "url": "https://protolabs.com/media/g3ehzag1/ryton-r-4-200na.pdf"
    },
    {
        "name": "PAI (Polyamide-imide / Torlon)",
        "url": "https://drakeplastics.com/wp-content/uploads/2016/01/Torlon-4203L.pdf"
    },
    {
        "name": "PI (Polyimide / Kapton / Vespel)",
        "url": "https://www.synflex.com/tr/insulate/syntherm-isolierstoffe/ayrinti/datasheets/kaptonr-hn-polyimidfolie-46/, https://docs.rs-online.com/f265/A700000014060820.pdf"
    },
    {
        "name": "LCP (Liquid Crystal Polymer)",
        "url": "https://www.makeitfrom.com/material-properties/Liquid-Crystal-Polymer-LCP"
    },
    {
        "name": "PES (Polyethersulfone)",
        "url": "https://download.basf.com/p1/8a8081c57fd4b609017fd664c4583e10/de/ULTRASON%25C2%25AE_E2010_NATURAL"
    },
    {
        "name": "PSU (Polysulfone)",
        "url": "https://protolabs.com/media/b2rj51rq/udel-p1700.pdf"
    },
    {
        "name": "PPSU (Polyphenylsulfone / Radel)",
        "url": "https://plasticker.de/docs/recybase/943_1756291360.pdf"
    },
    {
        "name": "PEKK (Polyetherketoneketone)",
        "url": "https://hpp.arkema.com/assets/arkema/TDS%20ARKEMA%20KEPSTAN%20serie%206000.pdf"
    },
    {
        "name": "PPA (Polyphthalamide)",
        "url": "https://www.makeitfrom.com/material-properties/Polyphthalamide-PPA"
    },
    {
        "name": "FEP (Fluorinated Ethylene Propylene)",
        "url": "https://www.professionalplastics.com/professionalplastics/content/downloads/PTFE_FEP_PFA.pdf"
    },
    {
        "name": "PFA (Perfluoroalkoxy)",
        "url": "https://www.professionalplastics.com/professionalplastics/content/downloads/PTFE_FEP_PFA.pdf, https://wkfluidhandling.com/wp-content/media/materials/pfa-perfluoroalkoxy.pdf"
    },
    {
        "name": "PVDF (Polyvinylidene Fluoride / Kynar)",
        "url": "https://www.makeitfrom.com/material-properties/Polyvinylidene-Fluoride-PVDF"
    },
    {
        "name": "ETFE (Ethylene Tetrafluoroethylene / Tefzel)",
        "url": "https://www.makeitfrom.com/compare/Ethylene-Tetrafluoroethylene-ETFE/Polyvinyl-Fluoride-PVF, https://betaplastics.ulprospector.com/plastics/zh-cn/datasheet/436530/tefzel-etfe-ht-2162"
    }
]

count = 0
for m in materials_to_insert:
    res = supabase.table("materials").select("id").eq("name", m["name"]).execute()
    
    payload = {
        "name": m["name"],
        "category": "Polymer",
        "subcategory": "High-Performance Polymers",
        "source_url": m["url"],
        "source_name": "Verified Sources",
        "extraction_method": "Verified Source Datasheet"
    }
        
    if len(res.data) > 0:
        supabase.table("materials").update(payload).eq("name", m["name"]).execute()
    else:
        supabase.table("materials").insert(payload).execute()
    count += 1

print(f"Inserted/Updated {count} high-performance polymers!")

