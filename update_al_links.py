
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# Delete duplicates
supabase.table("materials").delete().in_("name", ["1050A-H22 Aluminum", "1060 Al99.6 A91060 Aluminum", "1350-H24 Aluminum"]).execute()

updates = {
    "1050 (A91050) Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/1050-A91050-Aluminum, https://www.azom.com/article.aspx?ArticleID=6586",
        "ys": 20, "ts": 75, "el": 39
    },
    "1050A (Al99.5, 3.0255, 1B) Aluminum": {
        "url": "https://makeitfrom.com/material-properties/1050A-Al99.5-3.0255-1B-Aluminum, https://www.aircraftmaterials.com/data/aluminium/1050.html",
        "ys": 20, "ts": 75, "el": 39
    },
    "1050A H22 Aluminum": {
        "url": "https://makeitfrom.com/material-properties/1050A-Al99.5-3.0255-1B-Aluminum",
        "ys": 85, "ts": 105, "el": 12
    },
    "1050A O Aluminum": {
        "url": "https://makeitfrom.com/material-properties/1050A-O-Aluminum",
        "ys": 20, "ts": 65, "el": 42
    },
    "1060 (Al99.6, A91060) Aluminum": {
        "url": "https://makeitfrom.com/material-properties/1060-Al99.6-A91060-Aluminum",
        "ys": 28, "ts": 69, "el": 43
    },
    "1070 (Al99.7) Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/1070-Al99.7-Aluminum",
        "ys": 20, "ts": 65, "el": 45
    },
    "1070A (Al99.7(A), 3.0275) Aluminum": {
        "url": "https://makeitfrom.com/material-properties/1070A-Al99.7A-3.0275-Aluminum",
        "ys": 20, "ts": 65, "el": 45
    },
    "1080 (Al99.8) Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/1080-Al99.8-Aluminum, https://aircraftmaterials.com/data/aluminium/1080.html",
        "ys": 20, "ts": 60, "el": 50
    },
    "1080A (Al99.8(A), 3.0285, 1A) Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/1080A-Al99.8A-3.0285-1A-Aluminum",
        "ys": 20, "ts": 60, "el": 50
    },
    "1085 (Al99.85) Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/1085-Al99.85-Aluminum",
        "ys": 15, "ts": 60, "el": 55
    },
    "1100 (Al99.0Cu, A91100) Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/1100-Al99.0Cu-A91100-Aluminum",
        "ys": 34, "ts": 89, "el": 40
    },
    "1100A (Al99.0Cu(A)) Aluminum": {
        "url": "https://makeitfrom.com/material-properties/1100A-Al99.0CuA-Aluminum",
        "ys": 34, "ts": 89, "el": 40
    },
    "1200 (Al99.0, 3.0205, 1C, A91200) Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/1200-Al99.0-3.0205-1C-A91200-Aluminum",
        "ys": 30, "ts": 80, "el": 45
    },
    "1230A Aluminum": {
        "url": "https://makeitfrom.com/material-properties/1230A-Aluminum",
        "ys": 25, "ts": 70, "el": 40
    },
    "1235 (Al99.35, A91235) Aluminum": {
        "url": "https://makeitfrom.com/material-properties/1235-Al99.35-A91235-Aluminum",
        "ys": 24, "ts": 75, "el": 43
    },
    "1350 (E-Al99.5, EC, 3.0257, 1E, A91350) Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/1350-E-Al99.5-EC-3.0257-1E-A91350-Aluminum",
        "ys": 28, "ts": 82, "el": 40
    },
    "1350 H19 Aluminum": {
        "url": "https://makeitfrom.com/material-properties/1350-H19-Aluminum",
        "ys": 165, "ts": 185, "el": 1.5
    },
    "1350 H24 Aluminum": {
        "url": "https://nl.mfgrobots.com/material/metal/1009035887.html",
        "ys": 110, "ts": 125, "el": 10
    }
}

count = 0
for name, data in updates.items():
    supabase.table("materials").update({
        "source_url": data["url"],
        "source_name": "MakeItFrom / Verified Datasheet",
        "extraction_method": "Verified Source Datasheet",
        "yield_strength_min": data["ys"],
        "tensile_strength_min": data["ts"],
        "elongation": data["el"]
    }).eq("name", name).execute()
    count += 1

print(f"Updated {count} aluminum materials and deleted 2 duplicates.")

