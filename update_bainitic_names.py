
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

updates = {
    "Nanostructured Bainitic Steel (Super Bainite)": {
        "new_name": "Bainidur 1300",
        "new_url": "https://www.swisssteel-group.com/en/products/engineering-steel/bainitic-steels",
        "source_name": "Swiss Steel Group"
    },
    "Upper Bainitic Steel": {
        "new_name": "precidur HBS 600 (Bainitic Steel)",
        "new_url": "https://www.thyssenkrupp-steel.com/en/products/precision-steel-strip/hot-rolled-precision-strip/bainitic-steels.html",
        "source_name": "ThyssenKrupp"
    },
    "Lower Bainitic Steel": {
        "new_name": "precidur HBS 800 (Bainitic Steel)",
        "new_url": "https://www.thyssenkrupp-steel.com/en/products/precision-steel-strip/hot-rolled-precision-strip/bainitic-steels.html",
        "source_name": "ThyssenKrupp"
    },
    "Carbide-Free Bainitic Steel": {
        "new_name": "Swissbain-7MnB8",
        "new_url": "https://www.swisssteel-group.com/en/products/engineering-steel/bainitic-steels",
        "source_name": "Swiss Steel Group"
    },
    "HSLA Bainitic Steel": {
        "new_name": "FB-W 300Y450T (Ferritic-Bainitic)",
        "new_url": "https://www.thyssenkrupp-steel.com/en/products/hot-strip/multiphase-steels/ferrite-bainite-phase-steel.html",
        "source_name": "ThyssenKrupp"
    },
    "Bainitic Forging Steel": {
        "new_name": "Bainidur 7980 CN",
        "new_url": "https://www.swisssteel-group.com/en/products/engineering-steel/bainitic-steels",
        "source_name": "Swiss Steel Group"
    },
    "Creep-Resistant Bainitic Steel (2.25Cr-1Mo)": {
        "new_name": "ASTM A387 Grade 22 (2.25Cr-1Mo)",
        "new_url": "https://www.azom.com/article.aspx?ArticleID=6022",
        "source_name": "ASTM / AZoM"
    }
}

res = supabase.table("materials").select("id, name").ilike("subcategory", "%Bainitic%").execute()

for m in res.data:
    old_name = m["name"]
    if old_name in updates:
        info = updates[old_name]
        supabase.table("materials").update({
            "name": info["new_name"],
            "source_url": info["new_url"],
            "source_name": info["source_name"]
        }).eq("id", m["id"]).execute()

print("Done!")

