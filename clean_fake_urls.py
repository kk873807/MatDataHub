
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("id, name, source_url").eq("category", "Composite").execute()

cleaned = 0
for m in res.data:
    url = m.get("source_url") or ""
    if url == "https://materialsproject.org" or url == "https://materialsproject.org, ":
        supabase.table("materials").update({"source_url": None}).eq("id", m["id"]).execute()
        cleaned += 1

print(f"Removed fake/generic Material Project URLs from {cleaned} composite materials.")

