import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

pairs = [
    ("Aluminum Nitride", "Aluminum Nitride (AlN)"),
    ("Concrete M20", "Concrete M20 (C16/20)"),
    ("Concrete M40", "Concrete M40 (C32/40)"),
    ("Fused Silica", "Fused Silica (Quartz Glass)"),
    ("Silicon Nitride", "Silicon Nitride (Si3N4)"),
    ("Zirconia (Y-TZP)", "Zirconia (Yttria-Stabilized ZrO2)")
]

for p1, p2 in pairs:
    res = supabase.table("materials").select("id, name, extraction_method, created_at").in_("name", [p1, p2]).execute()
    print(f"--- {p1} vs {p2} ---")
    for row in res.data:
        print(f"ID: {row['id']} | Name: {row['name']} | Ext: {row.get('extraction_method')} | Date: {row['created_at']}")
