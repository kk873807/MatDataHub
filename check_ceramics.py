
import os
import json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("id, name, category, subcategory").eq("category", "Ceramic").execute()
names = [m["name"] for m in res.data]
names.sort()

print(f"Total Ceramics: {len(names)}")
print(json.dumps(names, indent=2))

