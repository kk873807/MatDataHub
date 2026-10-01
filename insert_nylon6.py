
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# 1. Insert PA 6
payload = {
    "name": "PA 6 (Nylon 6)",
    "category": "Polymer",
    "subcategory": "Engineering Thermoplastics",
    "source_url": "https://www.directplastics.co.uk/pub/pdf/datasheets/Nylon%20Extruded%206%20Black%20Data%20Sheet.pdf",
    "source_name": "Verified Sources",
    "extraction_method": "Verified Source Datasheet"
}

res = supabase.table("materials").select("id").eq("name", "PA 6 (Nylon 6)").execute()
if len(res.data) > 0:
    supabase.table("materials").update(payload).eq("name", "PA 6 (Nylon 6)").execute()
else:
    supabase.table("materials").insert(payload).execute()

# 2. Flag Xometry links
res_xo = supabase.table("materials").select("id, name, description, source_url").ilike("source_url", "%xometry%").execute()
flag_count = 0
for m in res_xo.data:
    desc = m.get("description") or ""
    if "Xometry links should be periodically verified" not in desc:
        new_desc = (desc + "\n[Note: Xometry links should be periodically verified due to periodic path restructuring.]").strip()
        supabase.table("materials").update({"description": new_desc}).eq("id", m["id"]).execute()
        flag_count += 1

print(f"Inserted PA 6 and flagged {flag_count} Xometry links.")

