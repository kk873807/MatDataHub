
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# Delete duplicates
dups = ["1350-H24 Aluminum", "3004-H19 Aluminum", "5042-H18 Aluminum", "5083-H36 Aluminum", "6060-T6 Aluminum", "6061-O Aluminum", "6061-T6 Aluminum"]
supabase.table("materials").delete().in_("name", dups).execute()

updates = {
    "1435 (A91435) Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/1435-A91435-Aluminum",
        "ys": 30, "ts": 80, "el": 40
    },
    "2219 T87 Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/2219-T87-Aluminum, https://www.referansmetal.com/alasimli-aluminyum/product/109/uzay-havacilik-savunma/levha-plaka/ams-qq-a-25030-alcu6mn-2219-t87?lang=en",
        "ys": 395, "ts": 475, "el": 10
    },
    "3003 H14 Aluminum": {
        "url": "https://www.referansmetal.com/alasimli-aluminyum/product/454/sac/ams-4008-almn1cu-3003-h14?lang=en, https://speedymetals.com/information/material21.html",
        "ys": 145, "ts": 150, "el": 16
    },
    "3004 H19 Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/3004-H19-Aluminum",
        "ys": 275, "ts": 305, "el": 3
    },
    "5042 H18 Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/5042-H18-Aluminum",
        "ys": 320, "ts": 350, "el": 4
    },
    "5059 H321 Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/5059-H321-Aluminum",
        "ys": 270, "ts": 360, "el": 10
    },
    "5083 H36 Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/5083-H36-Aluminum, https://www.mfgrobots.com/Article/material/metal/37392.html",
        "ys": 310, "ts": 360, "el": 6
    },
    "5086 H112 Aluminum": {
        "url": "https://makeitfrom.com/material-properties/5086-H112-Aluminum",
        "ys": 130, "ts": 260, "el": 14
    },
    "6060 T6 Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/6060-T6-Aluminum",
        "ys": 150, "ts": 190, "el": 12
    },
    "6061 O Aluminum": {
        "url": "https://makeitfrom.com/material-properties/6061-O-Aluminum",
        "ys": 55, "ts": 125, "el": 30
    },
    "6061 T6 Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/6061-T6-Aluminum",
        "ys": 276, "ts": 310, "el": 17
    },
    "6063 T6 Aluminum": {
        "url": "https://makeitfrom.com/material-properties/6063-T6-Aluminum",
        "ys": 214, "ts": 241, "el": 12
    },
    "6065 T6 Aluminum": {
        "url": "https://makeitfrom.com/material-properties/6065-T6-Aluminum",
        "ys": 260, "ts": 310, "el": 10
    }
}

count = 0
for name, data in updates.items():
    supabase.table("materials").update({
        "source_url": data["url"],
        "source_name": "Verified Datasheet",
        "extraction_method": "Verified Source Datasheet",
        "yield_strength_min": data["ys"],
        "tensile_strength_min": data["ts"],
        "elongation": data["el"]
    }).eq("name", name).execute()
    count += 1

print(f"Updated {count} aluminum materials and deleted 6 duplicates.")

