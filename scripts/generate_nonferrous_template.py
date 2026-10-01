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

# --- ALUMINUM ALLOYS ---
al_grades = [
    ("1100", "Pure Aluminum"), ("1050", "Pure Aluminum"), ("1199", "Pure Aluminum"),
    ("2011", "Aluminum-Copper"), ("2014", "Aluminum-Copper"), ("2024", "Aluminum-Copper"),
    ("3003", "Aluminum-Manganese"), ("3004", "Aluminum-Manganese"),
    ("4032", "Aluminum-Silicon"), ("4043", "Aluminum-Silicon"),
    ("5052", "Aluminum-Magnesium"), ("5083", "Aluminum-Magnesium"), ("5086", "Aluminum-Magnesium"), ("5454", "Aluminum-Magnesium"),
    ("6061", "Aluminum-Magnesium-Silicon"), ("6063", "Aluminum-Magnesium-Silicon"), ("6082", "Aluminum-Magnesium-Silicon"),
    ("7050", "Aluminum-Zinc"), ("7075", "Aluminum-Zinc"), ("7475", "Aluminum-Zinc")
]
for g, sub in al_grades:
    alloys.append({"name": f"Aluminum {g} Alloy", "cat": "Aluminum", "sub": sub, "search": [g]})

al_cast = [
    ("A356", "Cast Aluminum", ["a356", "356.0"]),
    ("319.0", "Cast Aluminum", ["319", "319.0"]),
    ("380.0", "Cast Aluminum", ["380", "380.0", "a380"]),
    ("390.0", "Cast Aluminum", ["390", "390.0"]),
]
for n, sub, s in al_cast:
    alloys.append({"name": f"Aluminum {n} Cast Alloy", "cat": "Aluminum", "sub": sub, "search": s})

# --- COPPER ALLOYS ---
cu_grades = [
    ("C10100", "Oxygen-Free Electronic (OFE) Copper", "Pure Copper", ["c10100", "c101", "ofe copper"]),
    ("C11000", "Electrolytic Tough Pitch (ETP) Copper", "Pure Copper", ["c11000", "c110", "etp copper"]),
    ("C12200", "Phosphorus-Deoxidized (DHP) Copper", "Pure Copper", ["c12200", "c122", "dhp copper"]),
    ("C14500", "Tellurium Copper", "Free-Machining Copper", ["c14500", "c145", "tellurium copper"]),
    ("C17200", "Beryllium Copper", "Beryllium Copper", ["c17200", "c172", "beryllium copper"]),
    ("C26000", "Cartridge Brass (70/30)", "Brass", ["c26000", "c260", "cartridge brass"]),
    ("C28000", "Muntz Metal (60/40 Brass)", "Brass", ["c28000", "c280", "muntz metal"]),
    ("C36000", "Free-Cutting Brass", "Brass", ["c36000", "c360", "free-cutting brass"]),
    ("C46400", "Naval Brass", "Brass", ["c46400", "c464", "naval brass"]),
    ("C51000", "Phosphor Bronze", "Bronze", ["c51000", "c510", "phosphor bronze"]),
    ("C61400", "Aluminum Bronze", "Bronze", ["c61400", "c614", "aluminum bronze"]),
    ("C63000", "Nickel Aluminum Bronze", "Bronze", ["c63000", "c630", "nickel aluminum bronze"]),
    ("C65500", "High Silicon Bronze", "Bronze", ["c65500", "c655", "silicon bronze"]),
    ("C70600", "Copper-Nickel 90/10", "Cupronickel", ["c70600", "c706", "cupronickel 90/10", "90/10 copper-nickel"]),
    ("C71500", "Copper-Nickel 70/30", "Cupronickel", ["c71500", "c715", "cupronickel 70/30", "70/30 copper-nickel"]),
    ("C75200", "Nickel Silver (65-18)", "Nickel Silver", ["c75200", "c752", "nickel silver"]),
    ("C93200", "Bearing Bronze (SAE 660)", "Cast Bronze", ["c93200", "c932", "sae 660", "bearing bronze"])
]
for g, n, sub, s in cu_grades:
    alloys.append({"name": f"{n} (UNS {g})", "cat": "Copper", "sub": sub, "search": s})

# --- ZINC ALLOYS ---
zn_grades = [
    ("Zamak 3", "Zinc Die Cast Alloy", ["zamak 3", "zinc alloy 3", "astm ag40a"]),
    ("Zamak 5", "Zinc Die Cast Alloy", ["zamak 5", "zinc alloy 5", "astm ac41a"]),
    ("Zamak 2", "Zinc Die Cast Alloy", ["zamak 2", "zinc alloy 2"]),
    ("Zamak 7", "Zinc Die Cast Alloy", ["zamak 7", "zinc alloy 7"]),
    ("ZA-8", "Zinc-Aluminum Alloy", ["za-8", "za8"]),
    ("ZA-12", "Zinc-Aluminum Alloy", ["za-12", "za12"]),
    ("ZA-27", "Zinc-Aluminum Alloy", ["za-27", "za27"])
]
for n, sub, s in zn_grades:
    alloys.append({"name": n, "cat": "Zinc", "sub": sub, "search": s})

# --- LEAD ALLOYS ---
pb_grades = [
    ("Chemical Lead (Pure Lead)", "Pure Lead", ["chemical lead", "corroding lead", "pure lead"]),
    ("Antimonial Lead (4% Sb)", "Antimonial Lead", ["antimonial lead", "lead-antimony", "hard lead"]),
    ("Antimonial Lead (6% Sb)", "Antimonial Lead", ["6% sb"]),
    ("Lead Babbitt (ASTM B23 Grade 7)", "Babbitt Metal", ["lead babbitt", "grade 7 babbitt", "astm b23"]),
    ("Lead-Calcium-Tin Alloy", "Lead-Calcium Alloy", ["lead-calcium", "pb-ca-sn"])
]
for n, sub, s in pb_grades:
    alloys.append({"name": n, "cat": "Lead", "sub": sub, "search": s})

# 3. Deduplicate
print("Cross-referencing to find missing non-ferrous grades...")
missing_materials = []

def is_duplicate(search_terms, existing_db_names):
    for term in search_terms:
        # Require word boundaries for alphanumeric strings to avoid false matches (e.g. '304' matching '3040')
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

print(f"Out of {len(alloys)} total standard industrial non-ferrous alloys checked, {len(missing_materials)} are currently missing from your database.")

# 4. Generate CSV
headers = ['category', 'subcategory', 'name', 'density', 'tensile_strength_min', 'yield_strength_min', 
           'elongation', 'hardness', 'elastic_modulus', 'thermal_conductivity', 'specific_heat', 
           'melting_point_min', 'composition', 'description']

output_file = 'Missing_NonFerrous_Alloys_Template.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(missing_materials)

print(f"Template saved successfully to {output_file}!")
