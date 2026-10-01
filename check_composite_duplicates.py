import os
from dotenv import load_dotenv
from supabase import create_client
from collections import defaultdict

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("id, name, extraction_method").eq("category", "Composite").execute()
materials = res.data

print(f"Found {len(materials)} composites.")

groups = defaultdict(list)
for m in materials:
    groups[m["name"].lower().strip()].append(m)

duplicates = {k: v for k, v in groups.items() if len(v) > 1}
if duplicates:
    print("\nExact Name Duplicates:")
    for k, v in duplicates.items():
        print(f"Name: {k}")
        for m in v:
            print(f"  - ID: {m['id']} (Extraction: {m['extraction_method']})")
else:
    print("\nNo exact name duplicates found. Listing all to check for near matches:")
    names = sorted([m["name"] for m in materials])
    for n in names:
        print(n)
