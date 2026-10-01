
import os
import requests
import urllib3
from dotenv import load_dotenv
from supabase import create_client

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials_to_check = [
    "Ash Wood (Dry)", "Ash Wood (Green)",
    "Balsa Wood (Dry)", "Balsa Wood (Green)",
    "Birch Wood (Dry)", "Birch Wood (Green)",
    "Cedar Wood (Dry)", "Cedar Wood (Green)",
    "Cherry Wood (Dry)", "Cherry Wood (Green)",
    "Cypress Wood (Dry)", "Cypress Wood (Green)",
    "Ebony Wood (Dry)", "Ebony Wood (Green)",
    "Epoxy (50% Glass Fiber Woven)", "Epoxy (60% Carbon Fiber UD)",
    "Hickory Wood (Dry)", "Hickory Wood (Green)",
    "Lignum Vitae Wood (Dry)", "Lignum Vitae Wood (Green)",
    "Mahogany Wood (Dry)", "Mahogany Wood (Green)",
    "Maple Wood (Dry)", "Maple Wood (Green)"
]

res = supabase.table("materials").select("name, source_url").in_("name", materials_to_check).execute()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

print("Verifying URLs...")
for m in res.data:
    name = m["name"]
    url_str = m.get("source_url")
    if not url_str:
        print(f"[{name}] No URLs to verify.")
        continue
        
    urls = [u.strip() for u in url_str.split(",") if u.strip()]
    for u in urls:
        try:
            r = requests.get(u, headers=headers, timeout=10, verify=False)
            if r.status_code == 200:
                print(f"[{name}] [OK 200] {u}")
            elif r.status_code in [403, 405]:
                # USDA FPL, VT, Dspace MIT often block bots
                print(f"[{name}] [WARN {r.status_code}] {u} (Likely Bot Blocked)")
            else:
                print(f"[{name}] [FAIL {r.status_code}] {u}")
        except Exception as e:
            print(f"[{name}] [ERROR] {u}: {e}")

print("Verification complete.")

