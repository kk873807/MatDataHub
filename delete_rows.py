
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

to_delete = [
    "Stainless Steel Tube",
    "Carbon Black (Polymer Additive)",
    "Glycol Modified Polyethylene Terephthalate PETG PET G"
]

for name in to_delete:
    res = supabase.table("materials").delete().eq("name", name).execute()
    print(f"Deleted {name}: {len(res.data)} rows affected")

