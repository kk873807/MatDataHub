
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

pairs = [
    ("ABS", "ABS (Acrylonitrile Butadiene Styrene)"),
    ("HDPE (High Density PE)", "HDPE (High-Density Polyethylene)"),
    ("Natural Rubber (NR)", "Natural Rubber (Polyisoprene)"),
    ("Neoprene (CR)", "Neoprene (Polychloroprene)"),
    ("Nylon 66", "Nylon 6/6"),
    ("PEEK (Polyether Ether Ketone)", "PEEK (Polyetheretherketone)"),
    ("PEEK (Unfilled)", "PEEK (Polyetheretherketone)"),
    ("Polycarbonate", "Polycarbonate (PC)"),
    ("Polypropylene", "Polypropylene (PP Homopolymer)"),
    ("Silicone Rubber", "Silicone Rubber (VMQ)")
]

for to_delete, to_keep in pairs:
    del_res = supabase.table("materials").select("id").eq("name", to_delete).execute()
    keep_res = supabase.table("materials").select("id").eq("name", to_keep).execute()
    
    if del_res.data and keep_res.data:
        del_id = del_res.data[0]["id"]
        keep_id = keep_res.data[0]["id"]
        
        # update project items
        supabase.table("project_items").update({"material_id": keep_id}).eq("material_id", del_id).execute()
        
        # now delete
        supabase.table("materials").delete().eq("id", del_id).execute()
        print(f"Merged {to_delete} -> {to_keep}")

# Update Silicone Rubber (VMQ) with sane values since the old one had YS=199
supabase.table("materials").update({
    "yield_strength_min": 10,
    "tensile_strength_min": 10,
}).eq("name", "Silicone Rubber (VMQ)").execute()

# Also ensure Polycarbonate (PC) has the 65 MPa values that the deleted Polycarbonate had
supabase.table("materials").update({
    "yield_strength_min": 65,
    "tensile_strength_min": 65,
}).eq("name", "Polycarbonate (PC)").execute()

print("Duplication merge complete.")

