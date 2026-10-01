
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("*").eq("name", "Fir Wood (Dry)").execute()
print(res.data[0].keys() if res.data else "No data")

