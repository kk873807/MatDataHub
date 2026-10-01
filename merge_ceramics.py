import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

merges = [
    {"keep": 782, "old": 72, "desc": None},
    {"keep": 238, "old": 615, "desc": None},
    {"keep": 104, "old": 923, "desc": "Third hardest known material (after diamond & cubic BN). Authentic energy-critical material. Applications: Extreme hardness. Used in body armor plating, tank armor, and nuclear reactor control rods (absorbs neutrons)."},
    {"keep": 106, "old": 988, "desc": "Excellent thermal shock resistance. Authentic electrical/magnetic/ionic material. Applications: Low thermal expansion glass used as an electrical insulator, laboratory glassware, and telescope mirrors."},
    {"keep": 242, "old": 604, "desc": None},
    {"keep": 243, "old": 608, "desc": None},
    {"keep": 1015, "old": 241, "desc": None},
    {"keep": 103, "old": 1010, "desc": "Best thermal shock resistance of any ceramic. Authentic advanced ceramic / glass material. Applications: Outstanding thermal shock resistance and fracture toughness. Used in high-performance engine bearings, turbocharger rotors, and space shuttle thrusters."},
    {"keep": 102, "old": 239, "desc": None}
]

count = 0
for m in merges:
    # 1. Update project_items
    supabase.table("project_items").update({"material_id": m["keep"]}).eq("material_id", m["old"]).execute()
    
    # 2. Update keeper description if provided
    if m["desc"]:
        supabase.table("materials").update({"description": m["desc"]}).eq("id", m["keep"]).execute()
        
    # 3. Delete old material
    supabase.table("materials").delete().eq("id", m["old"]).execute()
    print(f"Merged {m['old']} into {m['keep']}")
    count += 1
    
print(f"Successfully deduplicated {count} ceramic materials!")
