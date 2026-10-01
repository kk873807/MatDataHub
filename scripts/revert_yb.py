import os
import csv
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

def safe_float(val):
    try:
        return float(val) if val else None
    except ValueError:
        return None

def restore_clobbered():
    print("=" * 60)
    print("RESTORING CLOBBERED YB COMPOUNDS")
    print("=" * 60)
    
    targets = ['Yb', 'Yb2PdRh', 'Yb2TlPb', 'YbGaPt']
    found = {}
    
    with open('batch2_materials_project.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('material_name') in targets:
                found[row['material_name']] = row
                
    for name, row in found.items():
        comp_props = {
            "formula_pretty": row.get("formula_pretty"),
            "mp_id": row.get("mp_id"),
            "band_gap": safe_float(row.get("band_gap")),
            "formation_energy_per_atom": safe_float(row.get("formation_energy_per_atom")),
            "energy_above_hull": safe_float(row.get("energy_above_hull")),
            "volume": safe_float(row.get("volume")),
            "crystal_system": row.get("crystal_system"),
            "spacegroup": row.get("spacegroup"),
            "is_stable": row.get("is_stable") == "True",
            "theoretical": row.get("theoretical") == "True",
            "mp_id_alts": row.get("mp_id_alts", "").split(";") if row.get("mp_id_alts") else []
        }
        
        ehull = safe_float(row.get("energy_above_hull"))
        if not comp_props["theoretical"]:
            comp_props["confidence_tier"] = "experimentally_synthesized"
        elif comp_props["is_stable"]:
            comp_props["confidence_tier"] = "hypothetical_dft_stable"
            comp_props["display_warning"] = "Computationally predicted — not yet experimentally verified"
        elif ehull is not None and ehull <= 0.1:
            comp_props["confidence_tier"] = "hypothetical_metastable"
            comp_props["display_warning"] = "Metastable — DFT predicts this compound exists but is not the ground-state phase"
        else:
            comp_props["confidence_tier"] = "provisional"
            
        update_data = {
            "source_url": row["source_url"],
            "computational_properties": comp_props
        }
        
        density = safe_float(row.get("density"))
        if density is not None:
            update_data["density"] = density
            
        res = supabase.table("materials").update(update_data).eq("name", name).eq("source_name", "Materials Project").execute()
        if res.data:
            print(f"✅ Restored {name} -> {row['mp_id']}")
        else:
            print(f"❌ Failed to restore {name}")

def null_missing_targets():
    print("\n" + "=" * 60)
    print("NULLING OUT PENDING YB COMPOUNDS")
    print("=" * 60)
    
    missing_targets = ['Yb2AlGe3', 'YbMgCu4', 'YbMoClO4', 'YbSiPt2']
    
    for name in missing_targets:
        res = supabase.table("materials").select("id, computational_properties").eq("name", name).eq("source_name", "Materials Project").execute()
        
        if res.data:
            mat_id = res.data[0]["id"]
            comp = res.data[0].get("computational_properties") or {}
            if isinstance(comp, str): comp = json.loads(comp)
            
            comp["mp_id"] = None
            comp["link_status"] = "pending-mp-recompute"
            comp["display_warning"] = "Data temporarily unavailable — MP pseudopotential recompute in progress"
            
            update_data = {
                "source_url": "", # Null out source URL
                "computational_properties": comp
            }
            
            supabase.table("materials").update(update_data).eq("id", mat_id).execute()
            print(f"✅ Nulled {name} (pending recompute)")
        else:
            print(f"⚠️ {name} not found in DB")

if __name__ == "__main__":
    restore_clobbered()
    null_missing_targets()
