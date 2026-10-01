import csv
import json
import os
from collections import defaultdict
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

def safe_float(val):
    if not val: return None
    try:
        if "to" in val:
            parts = [float(p.strip()) for p in val.split("to")]
            return sum(parts) / len(parts)
        return float(val)
    except:
        return None

def parse_range(val):
    if not val: return None, None
    if "to" in val:
        parts = [float(p.strip()) for p in val.split("to")]
        return parts[0], parts[1]
    try:
        f = float(val)
        return f, f
    except:
        return None, None

def build_composition(rows):
    comp = []
    for r in rows:
        if r['category'] == 'Alloy Composition':
            name = r['property'].split('(')[0].strip()
            comp.append(f"{name}: {r['value']}%")
    return ", ".join(comp)

def build_hardness(rows):
    h = []
    for r in rows:
        if 'Hardness' in r['property']:
            h.append(f"{r['value']} {r['property'].replace(' Hardness', '')}")
    return ", ".join(h)

def main():
    print("=" * 60)
    print("INGESTING MAKEITFROM EXTRACTED DATA")
    print("=" * 60)

    data = defaultdict(list)
    with open('extracted_properties.csv', 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            data[row['material_name']].append(row)

    prop_map = {
        "Density": "density",
        "Elastic (Young's, Tensile) Modulus": "elastic_modulus",
        "Elongation at Break": "elongation",
        "Fatigue Strength": "fatigue_strength",
        "Poisson's Ratio": "poissons_ratio",
        "Shear Modulus": "shear_modulus",
        "Specific Heat Capacity": "specific_heat",
        "Thermal Conductivity": "thermal_conductivity",
        "Thermal Expansion": "thermal_expansion_coefficient",
        "Embodied Carbon": "embodied_carbon",
    }

    success = 0
    failed = 0

    for mat_name, rows in data.items():
        record = {}
        
        comp = build_composition(rows)
        if comp: record["composition"] = comp
        
        hard = build_hardness(rows)
        if hard: record["hardness"] = hard

        for r in rows:
            prop = r['property']
            val = r['value']
            
            if prop == "Tensile Strength: Ultimate (UTS)":
                vmin, vmax = parse_range(val)
                record["tensile_strength_min"] = vmin
                record["tensile_strength_max"] = vmax
            elif prop == "Tensile Strength: Yield (Proof)":
                vmin, vmax = parse_range(val)
                record["yield_strength_min"] = vmin
                record["yield_strength_max"] = vmax
            elif prop == "Melting Onset (Solidus)":
                record["melting_point_min"] = safe_float(val)
            elif prop == "Melting Completion (Liquidus)":
                record["melting_point_max"] = safe_float(val)
            elif prop == "Maximum Temperature: Mechanical":
                record["max_service_temp"] = safe_float(val)
            elif prop in prop_map:
                record[prop_map[prop]] = safe_float(val)

        # Update the database
        try:
            # We match strictly by name. We update fields that are part of record.
            # We also set data_type and extraction_method if we want, but let's just update properties.
            res = supabase.table("materials").update(record).eq("name", mat_name).execute()
            if res.data:
                success += 1
            else:
                print(f"⚠️ Could not find {mat_name} in DB.")
                failed += 1
        except Exception as e:
            print(f"❌ Error updating {mat_name}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)
    print(f"✅ Successfully updated: {success}")
    print(f"❌ Failed / Not found: {failed}")

if __name__ == "__main__":
    main()
