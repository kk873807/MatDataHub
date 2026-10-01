
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

updates = {
    "Upper Bainitic Steel": {
        "name": "precidur HBS 600",
        "urls": "https://www.thyssenkrupp-steel.com/media/content_1/publikationen/precision_steel/produktinformationen_1/bainitischer_stahl/thyssenkrupp_precidur_hbs_600_pr_624_precision_steel_en.pdf, https://www.thyssenkrupp-steel.com/en/products/precision-strip/product-details/bainitic-steel/Bainitic-steel.html",
        "ys": 440, "ts": 580, "el": 14
    },
    "Lower Bainitic Steel": {
        "name": "precidur HBS 800",
        "urls": "https://www.thyssenkrupp-steel.com/media/content_1/publikationen/precision_steel/produktinformationen_1/bainitischer_stahl/thyssenkrupp_hbs-800_product_information_precision_steel_en.pdf, https://www.thyssenkrupp-steel.com/media/content_1/publikationen/precision_steel/thyssenkrupp_precidur_bainitic_steels_en_precision_steel.pdf",
        "ys": 680, "ts": 780, "el": 10
    },
    "HSLA Bainitic Steel": {
        "name": "FB-W 300Y450T",
        "urls": "https://www.thyssenkrupp-steel.com/media/content_1/publikationen/produktinformationen/fb_w/thyssenkrupp_fb-w_product_information_steel_en_08-2016_01.pdf, https://www.thyssenkrupp-steel.com/en/products/hot-strip/multiphase-steel/ferrite-bainite-phase-steel/ferrite-bainite-phase-steel.html",
        "ys": 300, "ts": 450, "el": 24
    },
    "Bainitic Forging Steel": {
        "name": "Bainidur 7980 CN",
        "urls": "https://www.dew-powder.com/fileadmin/files/metallpulver.de/documents/Publikationen/Deutsch/2020-05-07_Bainidur_7980_CN_DE.pdf, https://matmatch.com/materials/destbainidur1301-bainidur-7980-cn",
        "ys": 790, "ts": 980, "el": 12
    },
    "Creep-Resistant Bainitic Steel (2.25Cr-1Mo)": {
        "name": "T24 / 7CrMoVTiB10-10",
        "urls": "https://www.czasopisma.pan.pl//Content/87592/PDF/10172%20Volume%2058%20Issue%203-6%20paper.pdf.pdf, https://mdr.nims.go.jp/datasets/8b8b55a8-4e72-4d8d-a101-3491de52b44f, https://dl.asminternational.org/alloy-digest/article/50/2/SA-508/6391/V-amp-M-T24High-Temperature-Ferritic-Steel",
        "ys": 450, "ts": 580, "el": 20
    }
}

res = supabase.table("materials").select("id, name").ilike("subcategory", "%Bainitic%").execute()

for m in res.data:
    old_name = m["name"]
    if old_name in updates:
        info = updates[old_name]
        supabase.table("materials").update({
            "name": info["name"],
            "source_url": info["urls"],
            "source_name": "Manufacturer PDF / Literature",
            "yield_strength_min": info["ys"],
            "tensile_strength_min": info["ts"],
            "elongation": info["el"]
        }).eq("id", m["id"]).execute()

print("Database updated!")

