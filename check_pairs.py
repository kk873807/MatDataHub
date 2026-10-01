import os
import json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

pairs_to_check = [
    [782, 72], # Alumina 99.5
    [238, 615], # Alumina 99
    [923, 104], # Boron Carbide
    [988, 106], # Borosilicate Glass
    [604, 242], # Concrete M20
    [608, 243], # Concrete M40
    [241, 1015], # Fused Silica
    [1010, 103], # Silicon Nitride
    [239, 102] # Zirconia
]

def dump_row(id):
    res = supabase.table("materials").select("*").eq("id", id).execute()
    if res.data:
        r = res.data[0]
        print(f"[{r['id']}] {r['name']} | Ext: {r.get('extraction_method')} | Desc: {r.get('description')}")

for pair in pairs_to_check:
    print("-" * 40)
    for id in pair:
        dump_row(id)
