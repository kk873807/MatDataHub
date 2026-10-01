
import os, urllib.parse
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

print("Fixing Bainitic Steels...")
res = supabase.table("materials").select("id, name").ilike("subcategory", "%Bainitic%").execute()
for m in res.data:
    name_enc = urllib.parse.quote(m["name"])
    new_url = f"https://www.matweb.com/search/QuickText.aspx?SearchText={name_enc}, https://www.sciencedirect.com/search?qs={name_enc}"
    supabase.table("materials").update({"source_url": new_url}).eq("id", m["id"]).execute()

print("Fixing MIDHANI materials...")
res = supabase.table("materials").select("id, name, source_url").eq("source_name", "MIDHANI").execute()
for m in res.data:
    name_enc = urllib.parse.quote(m["name"])
    old_url = m["source_url"] or ""
    if ", https://www.matweb.com" in old_url:
        old_url = old_url.split(", https://www.matweb.com")[0]
    new_url = f"{old_url}, https://www.matweb.com/search/QuickText.aspx?SearchText={name_enc}, https://www.azom.com/search.aspx?q={name_enc}"
    supabase.table("materials").update({"source_url": new_url}).eq("id", m["id"]).execute()

print("Done!")

