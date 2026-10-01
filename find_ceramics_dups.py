import os
from dotenv import load_dotenv
from supabase import create_client
import re

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("id, name").eq("category", "Ceramic").execute()

names = sorted([(m["name"], m["id"]) for m in res.data])

for i in range(len(names)):
    for j in range(i+1, len(names)):
        n1, id1 = names[i]
        n2, id2 = names[j]
        # Ignore things like "(Sheet)" vs "(Tube)"
        base1 = re.sub(r' \(.*?\)', '', n1).strip()
        base2 = re.sub(r' \(.*?\)', '', n2).strip()
        if base1 == base2 and n1 != n2:
            print(f"Possible dup: '{n1}' ({id1}) vs '{n2}' ({id2})")
