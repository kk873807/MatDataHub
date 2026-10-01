
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("name, extraction_method, source_url").eq("category", "Composite").execute()
unverified = []
for m in res.data:
    if m.get("extraction_method") != "Verified Source Datasheet":
        unverified.append(m)

for m in unverified:
    print(m)
print(f"Total unverified remaining: {len(unverified)}")

