import os
import time
from dotenv import load_dotenv
from supabase import create_client
from mp_api.client import MPRester

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
mp_key = os.environ.get("MP_API_KEY")

print("Fetching candidates...")
res = supabase.table("materials").select("id, name").eq("category", "Ceramic").is_("extraction_method", "null").execute()
candidates = res.data
print(f"Found {len(candidates)} candidates.")

# Extract valid formulas (assuming they match standard chemical formulas)
formula_to_id = {}
for c in candidates:
    formula = c["name"].strip()
    # Replace anything in parens, but wait: the MP API might just need the basic formula.
    # If the user named them exactly as formula:
    # We will just test if it's alphanumeric
    if " " not in formula and "(" not in formula: 
        formula_to_id[formula] = c["id"]

formulas_to_search = list(formula_to_id.keys())
print(f"Found {len(formulas_to_search)} pure formulas to search via MP.")

results_found = {}

with MPRester(mp_key) as mpr:
    batch_size = 30
    for i in range(0, len(formulas_to_search), batch_size):
        batch = formulas_to_search[i:i+batch_size]
        print(f"Searching batch {i} to {i+batch_size}...")
        try:
            docs = mpr.summary.search(formula=batch)
            for doc in docs:
                f = doc.formula_pretty
                if f in formula_to_id:
                    # If multiple polymorphs, pick lowest energy_above_hull
                    if f not in results_found or doc.energy_above_hull < results_found[f]["energy_above_hull"]:
                        results_found[f] = {
                            "mp_id": str(doc.material_id),
                            "energy_above_hull": float(doc.energy_above_hull),
                            "band_gap": float(doc.band_gap) if doc.band_gap is not None else None,
                            "density": float(doc.density) if doc.density is not None else None,
                            "volume": float(doc.volume) if doc.volume is not None else None,
                            "formation_energy_per_atom": float(doc.formation_energy_per_atom) if doc.formation_energy_per_atom is not None else None,
                            "crystal_system": str(doc.symmetry.crystal_system) if doc.symmetry else None,
                            "space_group": str(doc.symmetry.symbol) if doc.symmetry else None
                        }
        except Exception as e:
            print(f"Error on batch: {e}")
        time.sleep(0.5)

print(f"Found MP data for {len(results_found)} formulas. Updating database...")

count = 0
for f, data in results_found.items():
    mat_id = formula_to_id[f]
    payload = {
        "data_source_type": "computational_dft",
        "source_name": "Materials Project",
        "source_url": f"https://next-gen.materialsproject.org/materials/{data['mp_id']}",
        "computational_properties": data,
        "density": data["density"]
    }
    
    supabase.table("materials").update(payload).eq("id", mat_id).execute()
    count += 1

print(f"Successfully backfilled {count} materials with DFT data!")
