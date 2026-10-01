"""
cleanup_mp_materials.py
========================
1. Classify all 564 Materials Project materials by confidence tier.
2. DELETE the ~133 "predicted not to exist" (energy_above_hull > 0.1 eV/atom, theoretical=True).
3. Tag remaining materials with confidence_tier in computational_properties JSONB.
4. Attempt to recover Yb compounds via the MP API (phase-space search).
"""

import os
import csv
import json
import time
import requests
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
MP_API_KEY = os.environ.get("MP_API_KEY", "")

def safe_float(val):
    try:
        return float(val) if val else None
    except ValueError:
        return None


def classify_tier(theoretical_str, is_stable_str, ehull):
    """Classify a material into a confidence tier."""
    theoretical = theoretical_str == "True"
    is_stable = is_stable_str == "True"
    
    if not theoretical:
        return "experimentally_synthesized"
    elif is_stable:
        return "hypothetical_dft_stable"
    elif ehull is not None and ehull <= 0.1:
        return "hypothetical_metastable"
    elif ehull is not None and ehull > 0.1:
        return "predicted_not_to_exist"
    else:
        return "provisional"


def step1_classify_and_delete():
    """Read the CSV, classify each material, and delete the ones above hull."""
    print("=" * 60)
    print("STEP 1: Classify MP materials and delete unstable compounds")
    print("=" * 60)
    
    to_delete = []
    to_tag = []
    
    with open("batch2_materials_project.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ehull = safe_float(row.get("energy_above_hull"))
            tier = classify_tier(
                row.get("theoretical", ""),
                row.get("is_stable", ""),
                ehull
            )
            
            if tier == "predicted_not_to_exist":
                to_delete.append(row["material_name"])
            else:
                to_tag.append({
                    "name": row["material_name"],
                    "tier": tier,
                    "ehull": ehull
                })
    
    print(f"\n📊 Classification results:")
    from collections import Counter
    tier_counts = Counter(m["tier"] for m in to_tag)
    tier_counts["predicted_not_to_exist"] = len(to_delete)
    for tier, count in sorted(tier_counts.items()):
        print(f"  {tier}: {count}")
    
    # Delete unstable materials
    print(f"\n🗑️  Deleting {len(to_delete)} 'predicted not to exist' materials...")
    deleted = 0
    errors = 0
    for name in to_delete:
        try:
            res = supabase.table("materials").delete().eq("name", name).eq("source_name", "Materials Project").execute()
            if res.data:
                deleted += 1
            else:
                # Might not exist or might have a different source_name
                pass
        except Exception as e:
            print(f"  ❌ Error deleting {name}: {e}")
            errors += 1
    
    print(f"  ✅ Deleted {deleted} materials. {errors} errors.")
    
    # Tag remaining materials with confidence tier
    print(f"\n🏷️  Tagging {len(to_tag)} materials with confidence_tier...")
    tagged = 0
    for mat in to_tag:
        try:
            # Fetch current computational_properties
            existing = supabase.table("materials").select("id, computational_properties").eq("name", mat["name"]).eq("source_name", "Materials Project").execute()
            if not existing.data:
                continue
            
            row = existing.data[0]
            comp_props = row.get("computational_properties") or {}
            if isinstance(comp_props, str):
                comp_props = json.loads(comp_props)
            
            comp_props["confidence_tier"] = mat["tier"]
            if mat["tier"] == "hypothetical_metastable":
                comp_props["display_warning"] = "Metastable — DFT predicts this compound exists but is not the ground-state phase"
            elif mat["tier"] == "hypothetical_dft_stable":
                comp_props["display_warning"] = "Computationally predicted — not yet experimentally verified"
            elif mat["tier"] == "provisional":
                comp_props["display_warning"] = "Provisional — data may be incomplete due to ongoing recomputation"
            
            supabase.table("materials").update({
                "computational_properties": comp_props
            }).eq("id", row["id"]).execute()
            tagged += 1
            
        except Exception as e:
            print(f"  ❌ Error tagging {mat['name']}: {e}")
    
    print(f"  ✅ Tagged {tagged} materials with confidence_tier.")
    return to_delete, to_tag


def step2_recover_yb():
    """
    Attempt to recover Yb compounds by searching the MP API
    for the Yb-containing phase space instead of exact formula match.
    """
    print("\n" + "=" * 60)
    print("STEP 2: Recover Ytterbium (Yb) compounds")
    print("=" * 60)
    
    if not MP_API_KEY:
        print("⚠️  MP_API_KEY not set. Skipping Yb recovery.")
        return
    
    # Known Yb material names from the database that have null/incomplete data
    yb_names = []
    res = supabase.table("materials").select("name, computational_properties").eq("source_name", "Materials Project").execute()
    for mat in res.data:
        comp = mat.get("computational_properties") or {}
        if isinstance(comp, str):
            comp = json.loads(comp)
        
        formula = comp.get("formula_pretty", "")
        if formula and "Yb" in formula:
            yb_names.append({
                "name": mat["name"],
                "formula": formula,
                "mp_id": comp.get("mp_id", ""),
                "ehull": comp.get("energy_above_hull")
            })
    
    print(f"Found {len(yb_names)} Yb compounds in database:")
    for yb in yb_names:
        print(f"  {yb['name']} ({yb['formula']}) — mp_id: {yb['mp_id']}, ehull: {yb['ehull']}")
    
    if not yb_names:
        print("No Yb compounds found. Nothing to recover.")
        return
    
    # Search MP API for Yb compounds
    headers = {"X-API-KEY": MP_API_KEY}
    base_url = "https://api.materialsproject.org/materials/summary"
    
    recovered = 0
    for yb in yb_names:
        formula = yb["formula"]
        print(f"\n🔍 Searching MP API for {formula}...")
        
        try:
            # Search by formula
            params = {
                "formula": formula,
                "fields": "material_id,formula_pretty,energy_above_hull,formation_energy_per_atom,is_stable,theoretical,density",
                "_limit": 5
            }
            resp = requests.get(base_url, headers=headers, params=params, timeout=30)
            
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                if data:
                    best = data[0]  # Take the most stable entry
                    print(f"  ✅ Found {len(data)} entries. Best: {best.get('material_id')}")
                    
                    # Update the database
                    comp = {"formula_pretty": formula, "mp_id": best.get("material_id")}
                    ehull = best.get("energy_above_hull")
                    fe = best.get("formation_energy_per_atom")
                    
                    if ehull is not None:
                        comp["energy_above_hull"] = ehull
                    if fe is not None:
                        comp["formation_energy_per_atom"] = fe
                    comp["is_stable"] = best.get("is_stable", False)
                    comp["theoretical"] = best.get("theoretical", True)
                    comp["confidence_tier"] = "provisional"
                    comp["display_warning"] = "Yb compound — data may be affected by ongoing MP pseudopotential recomputation"
                    
                    update_data = {"computational_properties": comp}
                    density = best.get("density")
                    if density:
                        update_data["density"] = density
                    
                    source_url = f"https://next-gen.materialsproject.org/materials/{best.get('material_id')}"
                    update_data["source_url"] = source_url
                    
                    supabase.table("materials").update(update_data).eq("name", yb["name"]).eq("source_name", "Materials Project").execute()
                    recovered += 1
                    print(f"  ✅ Updated {yb['name']} with fresh data from {best.get('material_id')}")
                else:
                    print(f"  ⚠️  No entries found for {formula} — likely still mid-recompute")
            elif resp.status_code == 403:
                print(f"  ⚠️  403 Forbidden for {formula} — MP may be blocking formula queries")
            else:
                print(f"  ❌ HTTP {resp.status_code}: {resp.text[:200]}")
            
            time.sleep(2)  # Rate limit
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n✅ Yb recovery complete. Recovered {recovered}/{len(yb_names)} compounds.")


def main():
    print("🚀 Materials Project Cleanup & Recovery Pipeline")
    print("=" * 60)
    
    deleted, tagged = step1_classify_and_delete()
    step2_recover_yb()
    
    print("\n" + "=" * 60)
    print("🏁 PIPELINE COMPLETE")
    print("=" * 60)
    print(f"  Deleted: {len(deleted)} unstable hypothetical materials")
    print(f"  Tagged:  {len(tagged)} materials with confidence_tier")
    print("  Yb recovery attempted")


if __name__ == "__main__":
    main()
