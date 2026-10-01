import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials_to_insert = [
    {
        "name": "6463 T6 Aluminum",
        "url": "https://www.makeitfrom.com/material-properties/6463-T6-Aluminum, https://makeitfrom.com/material-properties/6463-AlMg0.7SiB-A96463-Aluminum",
        "ys": 200, "ts": 230, "el": 8, "desc": ""
    },
    {
        "name": "7005 T6 Aluminum",
        "url": "https://www.makeitfrom.com/material-properties/7005-T6-Aluminum, https://www.bluescopedistribution.com.au/wp-content/uploads/2022/10/Aluminium-7005-Data-Sheet-BlueScope-Distribution.pdf",
        "ys": 310, "ts": 380, "el": 10, "desc": ""
    },
    {
        "name": "7039 Aluminum",
        "url": "https://www.azom.com/article.aspx?ArticleID=8764, https://en.wikipedia.org/wiki/7039_aluminium_alloy",
        "ys": 380, "ts": 450, "el": 10, "desc": "Armor plate alloy (MIL-DTL-46063H)."
    },
    {
        "name": "7049 T73 Aluminum",
        "url": "https://makeitfrom.com/material-properties/7049-T73-Aluminum, https://www.azom.com/article.aspx?ArticleID=6662",
        "ys": 450, "ts": 530, "el": 9, "desc": ""
    },
    {
        "name": "7050 T7451 Aluminum",
        "url": "https://www.makeitfrom.com/material-properties/7050-T7451-Aluminum, https://en.wikipedia.org/wiki/7050_aluminium_alloy",
        "ys": 480, "ts": 540, "el": 9, "desc": ""
    },
    {
        "name": "7068 T6511 Aluminum",
        "url": "https://www.smithmetal.com/pdf/aluminium/7xxx/7068.pdf, https://en.wikipedia.org/wiki/7068_aluminium_alloy",
        "ys": 683, "ts": 710, "el": 5, "desc": "Ultra-high strength aerospace alloy (AMS 4331)."
    },
    {
        "name": "7150 T7751 Aluminum",
        "url": "https://saemobilus.sae.org/standards/ams4252c-aluminum-alloy-plate-64zn-24mg-22cu-012zr-7150-t7751-solution-heat-treated-stress-relieved-overaged, https://icme.hpc.msstate.edu/mediawiki/index.php/Al_7150-T7751_Stress-Strain_and_Fatigue_Life_Data.html",
        "ys": None, "ts": None, "el": None, "desc": "Open property table unavailable (paywalled or reference data only). Caution: Do not use Referansmetal composition for this alloy."
    },
    {
        "name": "7175 T7352 Aluminum",
        "url": "https://www.aubertduval.com/wp-content/uploads/2024/12/7175_GB.pdf, https://www.aubertduval.com/en/products/7175-aluminum-alloys/",
        "ys": 370, "ts": 455, "el": 7, "desc": "Values typical of T7352/T7354 tempers."
    },
    {
        "name": "7475 T7351 Aluminum",
        "url": "https://www.makeitfrom.com/material-properties/7475-T7351-Aluminum, https://www.mfgrobots.com/Article/material/metal/40536.html",
        "ys": 400, "ts": 470, "el": 10, "desc": ""
    },
    {
        "name": "8006 H18 Aluminum",
        "url": "https://www.mfgrobots.com/Article/material/metal/37378.html, https://en.wikipedia.org/wiki/8006_aluminium_alloy",
        "ys": 160, "ts": 190, "el": 3, "desc": "Properties typical of strip/sheet/foil."
    },
    {
        "name": "8090 Aluminum",
        "url": "https://www.makeitfrom.com/material-properties/8090-AlLi2.5Cu1.5Mg1-Aluminum, https://www.smithshp.com/assets/pdf/aluminium/aluminium-lithium/8090-aluminium-lithium-english.pdf",
        "ys": 370, "ts": 450, "el": 6, "desc": "Aluminum-Lithium alloy. Values are typical."
    }
]

count = 0
for m in materials_to_insert:
    res = supabase.table("materials").select("id").eq("name", m["name"]).execute()
    
    payload = {
        "name": m["name"],
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "source_url": m["url"],
        "source_name": "Verified Sources",
        "extraction_method": "Verified Source Datasheet",
        "yield_strength_min": m["ys"],
        "tensile_strength_min": m["ts"],
        "elongation": m["el"]
    }
    if m["desc"]:
        payload["description"] = m["desc"]
        
    if len(res.data) > 0:
        supabase.table("materials").update(payload).eq("name", m["name"]).execute()
    else:
        supabase.table("materials").insert(payload).execute()
    count += 1

print(f"Inserted/Updated {count} missing alloys!")
