import os
import csv
import re
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# 1. Fetch all existing material names to check for duplicates
print("Fetching existing database to prevent duplicates...")
existing_names = []
page = 0
while True:
    res = supabase.table('materials').select('name').range(page*1000, (page+1)*1000 - 1).execute()
    if not res.data: break
    existing_names.extend([m['name'].lower() for m in res.data if m.get('name')])
    if len(res.data) < 1000: break
    page += 1

# 2. Comprehensive Master List of Industrial Ferrous Alloys
alloys = []

# Carbon Steels (10xx series)
for grade in ["1005", "1006", "1008", "1010", "1015", "1018", "1020", "1022", "1025", "1030", "1035", "1040", "1045", "1050", "1055", "1060", "1070", "1080", "1090", "1095"]:
    sub = "Low Carbon Steel" if int(grade) <= 1030 else ("Medium Carbon Steel" if int(grade) <= 1050 else "High Carbon Steel")
    alloys.append({"name": f"AISI {grade} Carbon Steel", "cat": "Steel", "sub": sub, "search": [grade]})

# Free Machining Steels
for grade in ["1117", "1141", "1144", "1215", "12L14"]:
    alloys.append({"name": f"AISI {grade} Free Machining Steel", "cat": "Steel", "sub": "Free Machining Steel", "search": [grade.lower()]})

# Alloy Steels
for grade in ["1330", "4130", "4140", "4150", "4320", "4340", "5160", "52100", "6150", "8620", "9310"]:
    alloys.append({"name": f"AISI {grade} Alloy Steel", "cat": "Steel", "sub": "Low Alloy Steel", "search": [grade]})

# Structural / Weathering / Specialty
specials = [
    ("ASTM A36 Structural Steel", "Structural Steel", ["a36"]),
    ("ASTM A514 High Yield Strength Steel", "Structural Steel", ["a514"]),
    ("ASTM A572 High-Strength Low-Alloy Steel", "HSLA Steel", ["a572"]),
    ("ASTM A588 Weathering Steel", "Weathering Steel", ["a588", "corten"]),
    ("Hy-100 High-Yield Steel", "HSLA Steel", ["hy-100", "hy100"]),
    ("Hy-80 High-Yield Steel", "HSLA Steel", ["hy-80", "hy80"]),
    ("Maraging Steel 250", "Maraging Steel", ["maraging 250", "vascomax 250"]),
    ("Maraging Steel 300", "Maraging Steel", ["maraging 300", "vascomax 300"]),
    ("Maraging Steel 350", "Maraging Steel", ["maraging 350", "vascomax 350"]),
    ("Invar 36 (Fe-Ni Alloy)", "Low Expansion Alloy", ["invar", "nilo 36"]),
    ("Kovar (Fe-Ni-Co Alloy)", "Controlled Expansion Alloy", ["kovar"]),
    ("Hadfield Manganese Steel", "Manganese Steel", ["hadfield", "manganese steel"]),
    ("Electrical Steel (Silicon Steel)", "Electrical Steel", ["electrical steel", "silicon steel", "ngo", "cgo"])
]
for n, sub, s in specials:
    alloys.append({"name": n, "cat": "Steel", "sub": sub, "search": s})

# Stainless Steels
austenitic = ["201", "202", "301", "302", "303", "304", "304L", "304H", "305", "309", "310", "310S", "316", "316L", "316Ti", "317L", "321", "347", "904L", "Nitronic 50"]
for grade in austenitic:
    alloys.append({"name": f"AISI {grade} Stainless Steel", "cat": "Stainless Steel", "sub": "Austenitic Stainless Steel", "search": [grade.lower()]})

ferritic = ["405", "409", "430", "434", "446"]
for grade in ferritic:
    alloys.append({"name": f"AISI {grade} Stainless Steel", "cat": "Stainless Steel", "sub": "Ferritic Stainless Steel", "search": [grade.lower()]})

martensitic = ["410", "416", "420", "431", "440A", "440B", "440C"]
for grade in martensitic:
    alloys.append({"name": f"AISI {grade} Stainless Steel", "cat": "Stainless Steel", "sub": "Martensitic Stainless Steel", "search": [grade.lower()]})

duplex = [("2101", "LDX 2101"), ("2205", "UNS S32205"), ("2304", "UNS S32304"), ("2507", "Super Duplex UNS S32750")]
for grade, alt in duplex:
    alloys.append({"name": f"{grade} Duplex Stainless Steel", "cat": "Stainless Steel", "sub": "Duplex Stainless Steel", "search": [grade, alt.lower().replace("uns ","")]})

ph = ["17-4", "15-5", "13-8", "17-7"]
for grade in ph:
    alloys.append({"name": f"{grade} PH Stainless Steel", "cat": "Stainless Steel", "sub": "Precipitation Hardening", "search": [grade, f"{grade}ph"]})

# Tool Steels
tool_steels = {
    "Water-Hardening Tool Steel": ["W1", "W2"],
    "Oil-Hardening Tool Steel": ["O1", "O2", "O6"],
    "Air-Hardening Tool Steel": ["A2", "A6", "A8"],
    "High Carbon-Chromium Tool Steel": ["D2", "D3", "D7"],
    "Shock-Resisting Tool Steel": ["S1", "S5", "S7"],
    "Hot-Work Tool Steel": ["H11", "H13", "H22"],
    "High-Speed Tool Steel": ["M2", "M4", "M42", "T1", "T15"]
}
for sub, grades in tool_steels.items():
    for grade in grades:
        alloys.append({"name": f"{grade} Tool Steel", "cat": "Tool Steel", "sub": sub, "search": [f"{grade.lower()} tool", f"aisi {grade.lower()}"]})

# Cast Irons
irons = [
    ("Gray Cast Iron (Class 20)", "Gray Iron", ["gray cast iron", "class 20"]),
    ("Gray Cast Iron (Class 30)", "Gray Iron", ["class 30"]),
    ("Gray Cast Iron (Class 40)", "Gray Iron", ["class 40"]),
    ("Gray Cast Iron (Class 50)", "Gray Iron", ["class 50"]),
    ("Gray Cast Iron (Class 60)", "Gray Iron", ["class 60"]),
    ("Ductile Iron (60-40-18)", "Ductile Iron", ["60-40-18"]),
    ("Ductile Iron (65-45-12)", "Ductile Iron", ["65-45-12"]),
    ("Ductile Iron (80-55-06)", "Ductile Iron", ["80-55-06"]),
    ("Ductile Iron (100-70-03)", "Ductile Iron", ["100-70-03"]),
    ("Ductile Iron (120-90-02)", "Ductile Iron", ["120-90-02"]),
    ("Austempered Ductile Iron (ADI)", "Austempered Ductile Iron", ["adi", "austempered"]),
    ("White Cast Iron", "White Iron", ["white cast iron"]),
    ("Malleable Iron", "Malleable Iron", ["malleable iron"]),
    ("Compacted Graphite Iron (CGI)", "CGI", ["compacted graphite"]),
    ("Ni-Hard Cast Iron", "White Iron", ["ni-hard"]),
    ("Ni-Resist Cast Iron", "Austenitic Cast Iron", ["ni-resist"])
]
for n, sub, s in irons:
    alloys.append({"name": n, "cat": "Cast Iron", "sub": sub, "search": s})

# 3. Deduplicate
print("Cross-referencing to find missing grades...")
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

print(f"Out of {len(alloys)} total standard industrial ferrous alloys checked, {len(missing_materials)} are currently missing from your database.")

# 4. Generate CSV
headers = ['category', 'subcategory', 'name', 'density', 'tensile_strength_min', 'yield_strength_min', 
           'elongation', 'hardness', 'elastic_modulus', 'thermal_conductivity', 'specific_heat', 
           'melting_point_min', 'composition', 'description']

output_file = 'Missing_Ferrous_Alloys_Template.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(missing_materials)

print(f"Template saved successfully to {output_file}!")
