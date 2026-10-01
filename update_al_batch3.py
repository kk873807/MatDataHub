
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# Delete duplicates
dups = ["6101-T65 Aluminum", "7020-T651 Aluminum", "7075-T7351 Aluminum", "8011A-H16 Aluminum"]
supabase.table("materials").delete().in_("name", dups).execute()

updates = {
    "6101 T65 Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/6101-T65-Aluminum",
        "ys": 170, "ts": 220, "el": 12
    },
    "7020 T651 Aluminum": {
        "url": "https://makeitfrom.com/material-properties/7020-T651-Aluminum",
        "ys": 280, "ts": 350, "el": 10
    },
    "7075 T7351 Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/7075-T7351-Aluminum",
        "ys": 435, "ts": 505, "el": 11
    },
    "8011A H16 Aluminum": {
        "url": "https://www.makeitfrom.com/material-properties/8011A-H16-Aluminum",
        "ys": 125, "ts": 140, "el": 4
    },
    "Alumina (99.5% Al2O3)": {
        "url": "https://matweb.com/search/datasheettext.aspx?matid=143",
        "ys": 280, "ts": 280, "el": 0
    },
    "Alumina (Al2O3) 99%": {
        "url": "https://www.ipsceramics.com/wp-content/uploads/2024/11/IPS-Ceramics-Technical-Datasheet-Technical-Alumina.pdf",
        "ys": 320, "ts": 320, "el": 0
    },
    "Alumina (Aluminium Oxide 99.5%)": {
        "url": "https://www.ipsceramics.com/wp-content/uploads/2024/11/IPS-Ceramics-Technical-Datasheet-Technical-Alumina.pdf, https://www.kyocera-fineceramics.de/fileadmin/user_upload/Download/werkstoffdatenblaetter/aluminiumoxid/KFEG_Data_sheets_EN_2025_DD57.pdf",
        "ys": 300, "ts": 300, "el": 0
    },
    "Alumina 99%": {
        "url": "https://www.ipsceramics.com/wp-content/uploads/2024/11/IPS-Ceramics-Technical-Datasheet-Technical-Alumina.pdf",
        "ys": 320, "ts": 320, "el": 0
    },
    "Aluminium Alloy 1050 0 Sheet_58": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-1050-0-Sheet_58.ashx",
        "ys": 20, "ts": 70, "el": 40
    },
    "Aluminium Alloy 1050A H14 Sheet_57": {
        "url": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-1050A-H14-Sheet_57.pdf.ashx",
        "ys": 105, "ts": 115, "el": 8
    },
    "Aluminium Alloy 2011 T3 Rod and Bar_3": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-2011-T3-Rod-and-Bar_3.ashx",
        "ys": 295, "ts": 380, "el": 15
    },
    "Aluminium Alloy 2011 T6 Extruded Rod and Bar_56": {
        "url": "https://www.rightonblackburns.co.uk/datasheets/view/Righton-Blackburns-Ltd_Aluminium-Alloy-2011-T6-Bar_56.pdf, https://referansmetal.com/alasimli-aluminyum/product/367/uzay-havacilik-savunma/cubuk-lama/2011/astm-b211-alcu6bipb-2011-t6?lang=zh",
        "ys": 295, "ts": 395, "el": 10
    },
    "Aluminium Alloy 2014A T651 Sheet and Plate_295": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-2014A-T651-Sheet-and-Plate_295.ashx",
        "ys": 415, "ts": 460, "el": 8
    },
    "Aluminium Alloy 2014A T6511 Extrusion_342": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-2014A-T6511-Extrusion_342.ashx",
        "ys": 400, "ts": 460, "el": 7
    },
    "Aluminium Alloy 3003 0 Sheet_59": {
        "url": "https://www.aalco.co.uk/datasheets/Aluminium-Alloy-3003-0-Sheet_59.ashx, https://aircraftmaterials.com/data/aluminium/3003.html",
        "ys": 40, "ts": 110, "el": 30
    },
    "Aluminium Alloy 3103 H14 Sheet_298": {
        "url": "https://www.aalco.co.uk/datasheets/Aalco-Metals-Ltd_Aluminium-Alloy-3103-H14-Sheet_298.pdf.ashx",
        "ys": 120, "ts": 150, "el": 5
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
    
# Retro-update 3003 H14
supabase.table("materials").update({
    "source_url": "https://www.referansmetal.com/alasimli-aluminyum/product/454/sac/ams-4008-almn1cu-3003-h14?lang=en, https://aircraftmaterials.com/data/aluminium/3003.html",
    "yield_strength_min": 117,
    "tensile_strength_min": 138,
    "elongation": 5
}).eq("name", "3003 H14 Aluminum").execute()

print(f"Updated {count} batch 3 materials and deleted 4 duplicates.")

