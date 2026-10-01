import os
import csv
import re
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

print("Fetching existing database to prevent duplicates...")
existing_names = []
page = 0
while True:
    res = supabase.table('materials').select('name').range(page*1000, (page+1)*1000 - 1).execute()
    if not res.data: break
    existing_names.extend([m['name'].lower() for m in res.data if m.get('name')])
    if len(res.data) < 1000: break
    page += 1

alloys = []

# --- COMMERCIALLY PURE TITANIUM ---
ti_cp = [
    ("Titanium Grade 1", "Commercially Pure Titanium", ["titanium grade 1", "ti grade 1", "cp1", "r50250"]),
    ("Titanium Grade 2", "Commercially Pure Titanium", ["titanium grade 2", "ti grade 2", "cp2", "r50400"]),
    ("Titanium Grade 3", "Commercially Pure Titanium", ["titanium grade 3", "ti grade 3", "cp3", "r50550"]),
    ("Titanium Grade 4", "Commercially Pure Titanium", ["titanium grade 4", "ti grade 4", "cp4", "r50700"]),
    ("Titanium Grade 7 (Pd-enhanced)", "Commercially Pure Titanium", ["titanium grade 7", "ti grade 7", "cp7", "ti-0.2pd", "r52400"]),
    ("Titanium Grade 11 (Pd-enhanced)", "Commercially Pure Titanium", ["titanium grade 11", "ti grade 11", "cp11", "r52250"]),
]
for n, sub, s in ti_cp:
    alloys.append({"name": n, "cat": "Titanium", "sub": sub, "search": s})

# --- MAGNESIUM ALLOYS ---
mg_grades = [
    ("AZ31B Magnesium Alloy", "Wrought Magnesium", ["az31", "az31b"]),
    ("AZ91D Magnesium Alloy", "Cast Magnesium", ["az91", "az91d"]),
    ("AM60B Magnesium Alloy", "Cast Magnesium", ["am60", "am60b"]),
    ("ZK60A Magnesium Alloy", "Wrought Magnesium", ["zk60", "zk60a"]),
    ("AZ80A Magnesium Alloy", "Wrought Magnesium", ["az80", "az80a"]),
    ("AS41B Magnesium Alloy", "Cast Magnesium", ["as41", "as41b"]),
    ("WE43 Magnesium Alloy", "High-Temp Magnesium", ["we43", "elektron we43"]),
    ("Elektron 21 Magnesium Alloy", "High-Temp Magnesium", ["elektron 21", "elektron21"]),
    ("Pure Magnesium (99.8%)", "Pure Magnesium", ["pure magnesium", "mg 99.8%"]),
]
for n, sub, s in mg_grades:
    alloys.append({"name": n, "cat": "Magnesium", "sub": sub, "search": s})

# --- BERYLLIUM MATERIALS ---
be_grades = [
    ("Pure Beryllium (S-65 Structural Grade)", "Pure Beryllium", ["s-65", "s65 beryllium", "structural beryllium"]),
    ("Pure Beryllium (I-70 Instrument Grade)", "Pure Beryllium", ["i-70", "i70 beryllium", "instrument beryllium"]),
    ("Beryllium-Aluminum Alloy (AlBeMet 162)", "Beryllium-Aluminum Alloy", ["albemet", "albemet 162", "be-al alloy"]),
]
for n, sub, s in be_grades:
    alloys.append({"name": n, "cat": "Beryllium", "sub": sub, "search": s})

print("Cross-referencing to find missing grades...")
missing_materials = []

def is_duplicate(search_terms, existing_db_names):
    for term in search_terms:
        pattern = r'\b' + re.escape(term.lower()) + r'\b'
        for ex in existing_db_names:
            if re.search(pattern, ex):
                return True
    return False

for mat in alloys:
    if not is_duplicate(mat['search'], existing_names):
        missing_materials.append({
            "category": mat['cat'],
            "subcategory": mat['sub'],
            "name": mat['name'],
            "density": "",
            "tensile_strength_min": "",
            "yield_strength_min": "",
            "elongation": "",
            "hardness": "",
            "elastic_modulus": "",
            "thermal_conductivity": "",
            "specific_heat": "",
            "melting_point_min": "",
            "composition": "",
            "description": "Please manually fill data for this grade."
        })

from collections import Counter
cat_counts = Counter(m['category'] for m in missing_materials)
print(f"\nOut of {len(alloys)} total standard grades checked, {len(missing_materials)} are currently missing from your database:")
for cat, cnt in sorted(cat_counts.items()):
    print(f"  {cat}: {cnt} missing")

headers = ['category', 'subcategory', 'name', 'density', 'tensile_strength_min', 'yield_strength_min', 
           'elongation', 'hardness', 'elastic_modulus', 'thermal_conductivity', 'specific_heat', 
           'melting_point_min', 'composition', 'description']

output_file = 'Missing_CPTi_Mg_Be_Alloys_Template.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(missing_materials)

print(f"\nTemplate saved successfully to {output_file}!")
