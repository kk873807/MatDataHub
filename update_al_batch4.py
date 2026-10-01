
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

updates = {
    "Aluminium Alloy 4015 H14 Sheet_60": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-4015-H14-Sheet_60.ashx",
        "ys": 120, "ts": 150, "el": 5
    },
    "Aluminium Alloy 4925 H12 Sheet_136": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-4925-H12-Sheet_136.ashx",
        "ys": 110, "ts": 140, "el": 6
    },
    "Aluminium Alloy 5005 H34 Sheet_137": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-5005-H34-Sheet_137.ashx",
        "ys": 110, "ts": 135, "el": 5
    },
    "Aluminium Alloy 5052 H32 Sheet and Treadplate_138": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-5052-H32-Sheet-and-Treadplate_138.ashx",
        "ys": 193, "ts": 228, "el": 12
    },
    "Aluminium Alloy 5052 H32 Triple Grip Treadplate_47": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-5052-H32-Triple-Grip-Treadplate_47.ashx",
        "ys": 193, "ts": 228, "el": 12
    },
    "Aluminium Alloy 5083 0 H111 Sheet and Plate_149": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-5083-0-H111-Sheet-and-Plate_149.ashx",
        "ys": 145, "ts": 290, "el": 16
    },
    "Aluminium Alloy 5083 H32 Sheet_140": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-5083-H32-Sheet_140.ashx",
        "ys": 228, "ts": 303, "el": 9
    },
    "Aluminium Alloy 5251 0 Sheet and Plate_141": {
        "url": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-5251-0-Sheet-and-Plate_141.pdf.ashx",
        "ys": 60, "ts": 160, "el": 18
    },
    "Aluminium Alloy 5251 H22 Sheet and Plate_150": {
        "url": "https://www.rightonblackburns.co.uk/datasheets/view/Righton-Blackburns-Ltd_Aluminium-Alloy-5251-H22-Sheet-Plate_150.pdf",
        "ys": 130, "ts": 190, "el": 7
    },
    "Aluminium Alloy 5251 H24 Sheet and Plate_151": {
        "url": "https://mail.aircraftmaterials.com/data/aluminium/5251.html",
        "ys": 175, "ts": 225, "el": 6
    },
    "Aluminium Alloy 5251 H26 Sheet_152": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-5251-H26-Sheet_152.ashx",
        "ys": 190, "ts": 250, "el": 5
    },
    "Aluminium Alloy 5454 H22 and H32 Sheet_237": {
        "url": "https://aircraftmaterials.com/data/aluminium/5454.html, https://www.referansmetal.com/alasimli-aluminyum/product/40/genel-endustri/astm-b209-almg3mn-5454-h32?lang=en",
        "ys": 179, "ts": 248, "el": 10
    },
    "Aluminium Alloy 5454 O and H111 Sheet_238": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-5454-O-and-H111-Sheet_238.ashx",
        "ys": 83, "ts": 214, "el": 18
    },
    "Aluminium Alloy 5754 H111 Treadplate_142": {
        "url": "https://www.rightonblackburns.co.uk/datasheets/view/aluminium-alloy-5754-h111-sheet-plate, https://www.dinco.ae/files/aluminium-alloy-5754-data-sheet.pdf",
        "ys": 130, "ts": 220, "el": 12
    },
    "Aluminium Alloy 5754 H114 Sheet_299": {
        "url": "https://www.rightonblackburns.co.uk/datasheets/view/Righton-Blackburns-Ltd_Aluminium-Alloy-5754-H114-Sheet-Plate_299.pdf",
        "ys": 130, "ts": 220, "el": 12
    },
    "Aluminium Alloy 5754 H22 Sheet and Plate_153": {
        "url": "https://www.rightonblackburns.co.uk/datasheets/view/Righton-Blackburns-Ltd_Aluminium-Alloy-5754-H22-Sheet-Plate_153.pdf",
        "ys": 190, "ts": 260, "el": 7
    },
    "Aluminium Alloy 5754 H24 Sheet and Plate_340": {
        "url": "https://www.rightonblackburns.co.uk/datasheets/view/Righton-Blackburns-Ltd_Aluminium-Alloy-5754-H24-Sheet-Plate_340.pdf",
        "ys": 220, "ts": 280, "el": 5
    },
    "Aluminium Alloy 5754 H26 Sheet_341": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-5754-H26-Sheet_341.ashx",
        "ys": 240, "ts": 300, "el": 4
    },
    "Aluminium Alloy 6005A T6 Extrusion_157": {
        "url": "https://www.rightonblackburns.co.uk/datasheets/render/righton-blackburns-ltd_aluminium-alloy-6005a-t6-bar-extrusion_157, https://ucpcdn.thyssenkrupp.com/_legacy/UCPthyssenkruppBAMXUK/assets.files/material-data-sheets/aluminium/6005a-t6-extrusion.pdf",
        "ys": 215, "ts": 255, "el": 8
    },
    "Aluminium Alloy 6026 T9 Rod and Bar_143": {
        "url": "https://aalco.co.uk/datasheets/Aluminium-Alloy-6026-T9-Rod-and-Bar_143.ashx",
        "ys": 360, "ts": 390, "el": 6
    }
}

count = 0
for name, data in updates.items():
    supabase.table("materials").update({
        "source_url": data["url"],
        "source_name": "Aalco / Verified Datasheet",
        "extraction_method": "Verified Source Datasheet",
        "yield_strength_min": data["ys"],
        "tensile_strength_min": data["ts"],
        "elongation": data["el"]
    }).eq("name", name).execute()
    count += 1
    
# Fix description/notes for 5754 H22/H24 since Aalco copy-pasted aerospace text
bad_note = "Copy-pasted aerospace description removed."
supabase.table("materials").update({"description": bad_note}).eq("name", "Aluminium Alloy 5754 H22 Sheet and Plate_153").execute()
supabase.table("materials").update({"description": bad_note}).eq("name", "Aluminium Alloy 5754 H24 Sheet and Plate_340").execute()

print(f"Updated {count} Aalco batch materials.")

