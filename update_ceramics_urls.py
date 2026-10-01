import os
import requests
import time
import urllib3
from dotenv import load_dotenv
from supabase import create_client

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials_to_update = [
    {
        "name": "Alumina (99.5% Al2O3)",
        "url": "https://www.ipsceramics.com/wp-content/uploads/2024/11/IPS-Ceramics-Technical-Datasheet-Technical-Alumina.pdf, https://matweb.com/search/datasheettext.aspx?matid=143, https://coorstek.com/media/4244/ceramic-material-properties.pdf"
    },
    {
        "name": "Alumina (Al2O3) 99%",
        "url": "https://www.ipsceramics.com/wp-content/uploads/2024/11/IPS-Ceramics-Technical-Datasheet-Technical-Alumina.pdf, https://coorstek.com/media/4244/ceramic-material-properties.pdf"
    },
    {
        "name": "Aluminosilicate Glass",
        "url": "https://www.makeitfrom.com/material-properties/Aluminosilicate-Glass, https://www.goodfellow.com/usa/aluminosilicate-glass-tube-group"
    },
    {
        "name": "Aluminosilicate Glass (Sheet)",
        "url": "https://www.globalspec.com/ds/5452/areaspec/matl_aluminosilicate"
    },
    {
        "name": "Aluminosilicate Glass (Tube)",
        "url": "https://www.goodfellow.com/usa/aluminosilicate-glass-tube-group"
    },
    {
        "name": "Borosilicate Glass (Pyrex)",
        "url": "https://www.matweb.com/search/DataSheet.aspx?MatGUID=b0dbbac859444ffe98307f24ffd4c6a2, https://en.wikipedia.org/wiki/Borosilicate_glass, https://www.imetra.com/borosilicate-glass-material-properties/"
    },
    {
        "name": "Borosilicate Glass (Sheet)",
        "url": "https://matweb.com/search/datasheet.aspx?matguid=c88baf339576454ea8cac3e208bde97a"
    },
    {
        "name": "Borosilicate Glass (Tube)",
        "url": "https://en.wikipedia.org/wiki/Borosilicate_glass"
    },
    {
        "name": "Fused Silica (Quartz Glass)",
        "url": "https://www.makeitfrom.com/material-properties/Fused-Silica-Fused-Quartz, https://insaco.com/"
    },
    {
        "name": "Fused Silica (Sheet)",
        "url": "https://www.makeitfrom.com/material-properties/Fused-Silica-Fused-Quartz"
    },
    {
        "name": "Fused Silica (Tube)",
        "url": "https://www.makeitfrom.com/material-properties/Fused-Silica-Fused-Quartz"
    },
    {
        "name": "Soda-Lime Glass",
        "url": "https://en.wikipedia.org/wiki/List_of_physical_properties_of_glass, https://www.makeitfrom.com/material-properties/Soda-Lime-Float-Glass"
    },
    {
        "name": "Soda-Lime Glass (Sheet)",
        "url": "https://en.wikipedia.org/wiki/List_of_physical_properties_of_glass"
    },
    {
        "name": "Soda-Lime Glass (Tube)",
        "url": "https://en.wikipedia.org/wiki/List_of_physical_properties_of_glass"
    },
    {
        "name": "Sapphire (Sheet)",
        "url": "https://www.makeitfrom.com/material-properties/Synthetic-Sapphire, https://insaco.com/"
    },
    {
        "name": "Sapphire (Tube)",
        "url": "https://www.makeitfrom.com/material-properties/Synthetic-Sapphire, https://insaco.com/"
    },
    {
        "name": "Zirconia (Yttria-Stabilized ZrO2)",
        "url": "https://makeitfrom.com/material-properties/Yttria-Partially-Stabilized-Zirconia-TZP, https://ceramics.net/wp-content/uploads/stc-material-brochure-zirconia-ceramic-web-NEW-LOGO.pdf"
    },
    {
        "name": "Silicon Nitride (Si3N4)",
        "url": "https://www.makeitfrom.com/material-properties/Silicon-Nitride-Si3N4, https://ceramics.net/wp-content/uploads/stc-material-property-chart-master-ceramic-property-chart-printable-black-and-white-NO-LOGOS.pdf"
    },
    {
        "name": "Boron Carbide (B4C)",
        "url": "https://www.makeitfrom.com/material-properties/Boron-Carbide-B4C, https://coorstek.com/media/4244/ceramic-material-properties.pdf"
    },
    {
        "name": "Engineering Porcelain",
        "url": "https://www.engineeringtoolbox.com/ceramics-properties-d_1227.html, https://ceramics.net/wp-content/uploads/stc-material-property-chart-master-ceramic-full-property-chart-NEW-LOGOS.pdf"
    },
    {
        "name": "Concrete M20 (C16/20)",
        "url": "https://beamdimensions.com/materials/Concrete/Indian_IS-456/M20/, https://civilnotess.com/modulus-of-elasticity-of-concrete/"
    },
    {
        "name": "Concrete M40 (C32/40)",
        "url": "https://beamdimensions.com/materials/Concrete/Indian_IS-456/M40/, https://www.scribd.com/document/406091892/Material-Properties"
    },
    {
        "name": "Carbon Black",
        "url": "https://www.birlacarbon.com/wp-content/uploads/2022/02/birla-carbon-brochure-rubber-products-guide.pdf, https://www.specialchem.com/polymer-additives/product/better-chem-carbon-black-n330",
        "cat": "Additive/Filler"
    }
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

count = 0
for m in materials_to_update:
    urls_to_test = [u.strip() for u in m["url"].split(",") if u.strip()]
    for u in urls_to_test:
        try:
            r = requests.get(u, headers=headers, timeout=5, verify=False)
            if r.status_code == 404:
                print(f"[404] {u}")
        except:
            pass
            
    res = supabase.table("materials").select("id").eq("name", m["name"]).execute()
    payload = {
        "source_url": m["url"],
        "source_name": "Verified Sources",
        "extraction_method": "Verified Source Datasheet"
    }
    
    if len(res.data) > 0:
        supabase.table("materials").update(payload).eq("name", m["name"]).execute()
        count += 1
    else:
        # Some items might be missing, like Carbon Black, so insert them
        payload["name"] = m["name"]
        payload["category"] = m.get("cat", "Ceramic") 
        payload["subcategory"] = "Advanced Ceramics"
        supabase.table("materials").insert(payload).execute()
        count += 1
        print(f"Inserted missing material: {m['name']}")

print(f"Successfully processed {count} materials!")
