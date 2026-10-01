
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("id, name, extraction_method").eq("category", "Ceramic").execute()
candidates = [r for r in res.data if r.get("extraction_method") != "Verified Source Datasheet"]
print(f"Total candidates: {len(candidates)}")
for r in candidates[:5]:
    print(r)

