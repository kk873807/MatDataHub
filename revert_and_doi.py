
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

reverts = {
    "Bainidur 1300": {
        "name": "Nanostructured Bainitic Steel (Super Bainite)",
        "url": "https://doi.org/10.1098/rspa.2009.0407" # The famous Superbainite paper by Bhadeshia
    },
    "precidur HBS 600 (Bainitic Steel)": {
        "name": "Upper Bainitic Steel",
        "url": "https://doi.org/10.2355/isijinternational.45.221" 
    },
    "precidur HBS 800 (Bainitic Steel)": {
        "name": "Lower Bainitic Steel",
        "url": "https://doi.org/10.1016/0001-6160(80)90157-1"
    },
    "Swissbain-7MnB8": {
        "name": "Carbide-Free Bainitic Steel",
        "url": "https://doi.org/10.3390/met12020195"
    },
    "FB-W 300Y450T (Ferritic-Bainitic)": {
        "name": "HSLA Bainitic Steel",
        "url": "https://doi.org/10.1007/s11661-008-9584-6" # Typical HSLA bainite paper
    },
    "Bainidur 7980 CN": {
        "name": "Bainitic Forging Steel",
        "url": "https://doi.org/10.1016/j.msea.2014.07.037"
    },
    "ASTM A387 Grade 22 (2.25Cr-1Mo)": {
        "name": "Creep-Resistant Bainitic Steel (2.25Cr-1Mo)",
        "url": "https://doi.org/10.1016/j.ijpvp.2007.06.002"
    }
}

res = supabase.table("materials").select("id, name").ilike("subcategory", "%Bainitic%").execute()

for m in res.data:
    current_name = m["name"]
    if current_name in reverts:
        info = reverts[current_name]
        supabase.table("materials").update({
            "name": info["name"],
            "source_url": info["url"],
            "source_name": "Scientific Research DOI"
        }).eq("id", m["id"]).execute()

print("Reverted names and added DOIs!")

