
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("name, subcategory").eq("category", "Ceramic").execute()
current_names = [m["name"] for m in res.data]
current_names.sort()

with open("current_ceramics.md", "w", encoding="utf-8") as f:
    f.write("# Current Ceramic Materials in Database\n\n")
    for name in current_names:
        f.write(f"- {name}\n")

master_list = [
    "Silicon Carbide (SiC)",
    "Tungsten Carbide (WC)",
    "Titanium Carbide (TiC)",
    "Beryllium Oxide (BeO)",
    "Steatite",
    "Cordierite",
    "Mullite",
    "Sialon",
    "Macor (Machinable Glass Ceramic)",
    "Boron Nitride (Hexagonal / h-BN)",
    "Boron Nitride (Cubic / c-BN)",
    "Titanium Dioxide (Titania / TiO2)",
    "Barium Titanate (BaTiO3)",
    "Lead Zirconate Titanate (PZT)",
    "Hafnium Carbide (HfC)",
    "Tantalum Carbide (TaC)",
    "Zirconium Diboride (ZrB2)",
    "Hafnium Diboride (HfB2)",
    "Titanium Silicon Carbide (MAX Phase Ti3SiC2)",
    "Spinel (MgAl2O4)",
    "Aluminum Titanate (Al2TiO5)",
    "Yttrium Barium Copper Oxide (YBCO - Superconductor)",
    "Bismuth Strontium Calcium Copper Oxide (BSCCO - Superconductor)",
    "Zerodur (Low Expansion Glass Ceramic)"
]

missing = []
current_lower = [n.lower() for n in current_names]

for m in master_list:
    # Check if a close match exists
    found = False
    for c in current_lower:
        base_m = m.lower().split("(")[0].strip()
        if base_m in c or c in base_m:
            found = True
            break
    if not found:
        missing.append(m)
        
with open("missing_ceramics.md", "w", encoding="utf-8") as f:
    f.write("# Missing Engineering, Advanced & Futuristic Ceramics\n\n")
    for name in missing:
        f.write(f"- {name}\n")

print(f"Generated lists! Current: {len(current_names)}, Missing: {len(missing)}")

