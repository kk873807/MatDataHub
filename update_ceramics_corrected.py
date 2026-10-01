
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

updates = [
    {
        "name": "Alumina (99.5% Al2O3)",
        "url": "https://ipsceramics.com/technical-ceramics/alumina/, https://www.ipsceramics.com/wp-content/uploads/2015/09/Technical-Datasheet-Alumina1.pdf, https://matweb.com/search/datasheettext.aspx?matid=143, https://coorstek.com/media/4244/ceramic-material-properties.pdf"
    },
    {
        "name": "Alumina (Al2O3) 99%",
        "url": "https://ipsceramics.com/technical-ceramics/alumina/, https://www.ipsceramics.com/wp-content/uploads/2015/09/Technical-Datasheet-Alumina1.pdf, https://coorstek.com/media/4244/ceramic-material-properties.pdf"
    },
    {
        "name": "Silicon Nitride (Si3N4)",
        "url": "https://www.makeitfrom.com/material-properties/Silicon-Nitride-Si3N4, https://coorstek.com/media/4244/ceramic-material-properties.pdf"
    },
    {
        "name": "Engineering Porcelain",
        "url": "https://www.engineeringtoolbox.com/ceramics-properties-d_1227.html, https://www.ceramicindustry.com/ceramic-materials-properties-charts/, https://ceramics.net/wp-content/uploads/stc-material-property-chart-individual-silicates-mullite-01052021.pdf"
    }
]

count = 0
for u in updates:
    res = supabase.table("materials").update({"source_url": u["url"]}).eq("name", u["name"]).execute()
    if len(res.data) > 0:
        count += 1

print(f"Updated {count} material records with corrected URLs!")

