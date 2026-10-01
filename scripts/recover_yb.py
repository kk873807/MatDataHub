import os
import json
import requests
from supabase import create_client
from dotenv import load_dotenv
import re

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
MP_API_KEY = os.environ.get("MP_API_KEY", "")

def get_chemsys(formula):
    elements = re.findall(r"[A-Z][a-z]?", formula)
    return "-".join(sorted(list(set(elements))))

def recover_yb():
    # The actual 4 targets the user wanted
    target_names = ["Yb2AlGe3", "YbMgCu4", "YbMoClO4", "YbSiPt2"]
    
    yb_names = []
    res = supabase.table("materials").select("id, name, computational_properties").in_("name", target_names).eq("source_name", "Materials Project").execute()
    
    for mat in res.data:
        # Since computational_properties is None, we just use the material name as the formula
        yb_names.append({
            "id": mat["id"],
            "name": mat["name"],
            "formula": mat["name"]
        })
            
    headers = {"X-API-KEY": MP_API_KEY}
    base_url = "https://api.materialsproject.org/materials/summary"
    
    recovered = 0
    for yb in yb_names:
        chemsys = get_chemsys(yb["formula"])
        print(f"\n🔍 Searching MP API for {yb['formula']} (chemsys: {chemsys})...")
        
        try:
            params = {
                "chemsys": chemsys,
                "_fields": "material_id,formula_pretty,energy_above_hull,formation_energy_per_atom,is_stable,theoretical,density",
                "_limit": 10
            }
            resp = requests.get(base_url, headers=headers, params=params, timeout=30)
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                exact_matches = [d for d in data if d.get("formula_pretty") == yb["formula"]]
                
                if exact_matches:
                    best = exact_matches[0]
                    for match in exact_matches:
                        if match.get("energy_above_hull") is not None:
                            best = match
                            break
                            
                    print(f"  ✅ Found new ID: {best.get('material_id')} with ehull: {best.get('energy_above_hull')}")
                    
                    comp = {"formula_pretty": yb["formula"], "mp_id": best.get("material_id")}
                    ehull = best.get("energy_above_hull")
                    fe = best.get("formation_energy_per_atom")
                    
                    if ehull is not None: comp["energy_above_hull"] = ehull
                    if fe is not None: comp["formation_energy_per_atom"] = fe
                    comp["is_stable"] = best.get("is_stable", False)
                    comp["theoretical"] = best.get("theoretical", True)
                    comp["confidence_tier"] = "provisional"
                    comp["display_warning"] = "Yb compound — data may be affected by ongoing MP pseudopotential recomputation"
                    
                    update_data = {"computational_properties": comp}
                    density = best.get("density")
                    if density: update_data["density"] = density
                    
                    source_url = f"https://next-gen.materialsproject.org/materials/{best.get('material_id')}"
                    update_data["source_url"] = source_url
                    
                    supabase.table("materials").update(update_data).eq("id", yb["id"]).execute()
                    recovered += 1
                else:
                    print(f"  ⚠️  No exact formula match in chemsys {chemsys}")
            else:
                print(f"  ❌ HTTP {resp.status_code}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            
    print(f"\n✅ Recovered {recovered} Yb compounds.")

if __name__ == "__main__":
    recover_yb()
