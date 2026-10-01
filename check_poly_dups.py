
import os
import json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

pairs = [
    ["ABS", "ABS (Acrylonitrile Butadiene Styrene)"],
    ["HDPE (High Density PE)", "HDPE (High-Density Polyethylene)"],
    ["Natural Rubber (NR)", "Natural Rubber (Polyisoprene)"],
    ["Neoprene (CR)", "Neoprene (Polychloroprene)"],
    ["Nylon 6/6", "Nylon 66"],
    ["PEEK (Polyether Ether Ketone)", "PEEK (Polyetheretherketone)", "PEEK (Unfilled)"],
    ["Polycarbonate", "Polycarbonate (PC)"],
    ["Polypropylene", "Polypropylene (PP Homopolymer)"],
    ["Silicone Rubber", "Silicone Rubber (VMQ)"]
]

all_names = [name for group in pairs for name in group]

res = supabase.table("materials").select("name, yield_strength_min, tensile_strength_min, elongation, source_name, extraction_method").in_("name", all_names).execute()

data_by_name = {m["name"]: m for m in res.data}

for group in pairs:
    print("--------------------")
    for name in group:
        if name in data_by_name:
            m = data_by_name[name]
            print(f"{name}: YS={m.get('yield_strength_min')}, TS={m.get('tensile_strength_min')}, Ext={m.get('extraction_method')}")
        else:
            print(f"{name}: NOT FOUND")

