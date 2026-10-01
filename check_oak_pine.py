import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("id, name, extraction_method, source_url, density").in_("name", ["Oak Wood", "Oak Wood (Dry)", "Oak Wood (Green)", "Pine Wood", "Pine Wood (Dry)", "Pine Wood (Green)"]).execute()

for m in res.data:
    print(m)
