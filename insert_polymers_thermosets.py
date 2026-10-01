
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials_to_insert = [
    {
        "name": "Epoxy (Unfilled)",
        "url": "https://www.makeitfrom.com/material-properties/Epoxy, http://www.matweb.com/search/datasheettext.aspx?matguid=1c74545c91874b13a3e44f400cedfe39, https://www.matweb.com/search/datasheettext.aspx?matguid=956da5edc80f4c62a72c15ca2b923494",
        "sub": "Thermosets"
    },
    {
        "name": "Epoxy (Glass Fiber Reinforced / FR4)",
        "url": "https://en.wikipedia.org/wiki/FR-4, https://www.plasticsintl.com/products/laminate-g-10fr-4-glass-epoxy, https://www.ulprospector.com/plastics/en/datasheet/112876/acculam-epoxyglas-g10-fr4, https://www.makeitfrom.com/material-properties/NEMA-Industrial-Laminate, https://www.matweb.com/search/DataSheet.aspx?MatGUID=035d2130b7f34d918e8d590659b85cb7",
        "sub": "Thermosets"
    },
    {
        "name": "Epoxy (Carbon Fiber Reinforced)",
        "url": "http://www.performance-composites.com/carbonfibre/mechanicalproperties_2.asp, https://acpcomposites.com/wp-content/uploads/2024/05/Mechanical-Properties-of-Carbon-Fiber-Composite-Materials.pdf, https://assets.rs-online.com/v1699614257/Datasheets/94dbd134a6050eb5ac2e6e0ad5307516.pdf",
        "sub": "Thermosets"
    },
    {
        "name": "PUR (Polyurethane, Rigid)",
        "url": "https://www.makeitfrom.com/material-properties/Rigid-Thermoset-Polyurethane-RPU, https://sawbones.com/solid-rigid-polyurethane-foam-properties/, https://dragonplate.com/Images/uploaded/PDFs/FR-3706-TDS%20LASTAFOAM%20technical%20data%20sheet.pdf, https://cdn.shopify.com/s/files/1/0076/1856/0097/files/U150-ENG_1.pdf",
        "sub": "Thermosets"
    },
    {
        "name": "PUR (Polyurethane, Flexible)",
        "url": "https://www.makeitfrom.com/material-properties/Polyurethane-Rubber-AU-EU",
        "sub": "Elastomers & Rubbers",
        "desc": "Cast PU elastomer (AU/EU). Note: flexible slabstock/moulded foam properties are highly density/formulation dependent."
    },
    {
        "name": "Melamine Formaldehyde (MF)",
        "url": "https://www.makeitfrom.com/material-properties/Melamine-Formaldehyde-MF, https://www.makeitfrom.com/material-properties/Melamine-Formaldehyde-Moulding-Compound, https://www.britannica.com/technology/melamine-formaldehyde-resin",
        "sub": "Thermosets"
    },
    {
        "name": "Urea Formaldehyde (UF)",
        "url": "https://www.makeitfrom.com/material-properties/Urea-Formaldehyde-UF, https://www.bpf.co.uk/plastipedia/polymers/Default.aspx",
        "sub": "Thermosets"
    },
    {
        "name": "Vinyl Ester",
        "url": "https://romar-voss.nl/downloads/tds/tds-derakane-signia-411-resin.pdf, https://www.freemansupply.com/datasheets/derakane.pdf, https://www.ulprospector.com/plastics/en/datasheet/7516/derakane-411-45",
        "sub": "Thermosets"
    },
    {
        "name": "Unsaturated Polyester (UP)",
        "url": "https://www.makeitfrom.com/material-properties/Unsaturated-Polyester-UP, https://omnexus.specialchem.com/product-categories/thermosets-upr-unsaturated-polyester-resin",
        "sub": "Thermosets"
    }
]

count = 0
for m in materials_to_insert:
    res = supabase.table("materials").select("id").eq("name", m["name"]).execute()
    
    payload = {
        "name": m["name"],
        "category": "Polymer",
        "subcategory": m["sub"],
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

print(f"Inserted/Updated {count} thermoset polymers!")

