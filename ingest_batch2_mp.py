
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

def main():
    updated = 0
    errors = 0
    with open("batch2_materials_project.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mat_name = row["material_name"]
            
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
            
            update_data = {
                "source_url": row["source_url"],
                "source_name": "Materials Project",
                "computational_properties": comp_props
            }
            
            density = safe_float(row.get("density"))
            if density is not None:
                update_data["density"] = density

            try:
                res = supabase.table("materials").update(update_data).eq("name", mat_name).execute()
                if len(res.data) > 0:
                    updated += 1
                else:
                    print(f"Warning: {mat_name} not found in DB")
            except Exception as e:
                print(f"Error updating {mat_name}: {e}")
                errors += 1
                
    print(f"\nIngestion Complete: {updated} rows updated successfully. {errors} errors.")

if __name__ == "__main__":
    main()

