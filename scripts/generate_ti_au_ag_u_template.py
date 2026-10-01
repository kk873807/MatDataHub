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

print(f"Total existing materials: {len(existing_names)}")

alloys = []

# --- TITANIUM ALLOYS ---

# Commercially Pure (CP) Grades
ti_cp = [
    ("Grade 1", "Commercially Pure Titanium", ["grade 1", "cp1", "uns r50250"]),
    ("Grade 2", "Commercially Pure Titanium", ["grade 2", "cp2", "uns r50400"]),
    ("Grade 3", "Commercially Pure Titanium", ["grade 3", "cp3", "uns r50550"]),
    ("Grade 4", "Commercially Pure Titanium", ["grade 4", "cp4", "uns r50700"]),
    ("Grade 7", "Commercially Pure Titanium", ["grade 7", "ti-0.2pd", "uns r52400"]),
    ("Grade 12", "Near-Alpha Titanium", ["grade 12", "ti-0.3mo-0.8ni", "uns r53400"]),
]
for g, sub, s in ti_cp:
    alloys.append({"name": f"Titanium {g}", "cat": "Titanium", "sub": sub, "search": s})

# Alpha & Near-Alpha Alloys
ti_alpha = [
    ("Ti-5Al-2.5Sn (Grade 6)", "Alpha Titanium Alloy", ["ti-5al-2.5sn", "grade 6", "uns r54520"]),
    ("Ti-8Al-1Mo-1V", "Near-Alpha Titanium Alloy", ["ti-8al-1mo-1v", "ti-811"]),
    ("Ti-6Al-2Sn-4Zr-2Mo (Ti-6242)", "Near-Alpha Titanium Alloy", ["ti-6242", "ti-6al-2sn-4zr-2mo"]),
    ("IMI 834", "Near-Alpha Titanium Alloy", ["imi 834"]),
]
for n, sub, s in ti_alpha:
    alloys.append({"name": n, "cat": "Titanium", "sub": sub, "search": s})

# Alpha-Beta Alloys
ti_ab = [
    ("Ti-6Al-4V (Grade 5)", "Alpha-Beta Titanium Alloy", ["ti-6al-4v", "grade 5", "ti64", "uns r56400"]),
    ("Ti-6Al-4V ELI (Grade 23)", "Alpha-Beta Titanium Alloy", ["grade 23", "ti-6al-4v eli", "uns r56401"]),
    ("Ti-6Al-6V-2Sn", "Alpha-Beta Titanium Alloy", ["ti-6al-6v-2sn", "ti-662"]),
    ("Ti-6Al-2Sn-4Zr-6Mo (Ti-6246)", "Alpha-Beta Titanium Alloy", ["ti-6246", "ti-6al-2sn-4zr-6mo"]),
    ("Ti-3Al-2.5V (Grade 9)", "Alpha-Beta Titanium Alloy", ["grade 9", "ti-3al-2.5v", "uns r56320"]),
    ("Ti-6Al-7Nb", "Alpha-Beta Titanium Alloy", ["ti-6al-7nb"]),
]
for n, sub, s in ti_ab:
    alloys.append({"name": n, "cat": "Titanium", "sub": sub, "search": s})

# Beta Alloys
ti_beta = [
    ("Ti-10V-2Fe-3Al (Ti-10-2-3)", "Beta Titanium Alloy", ["ti-10v-2fe-3al", "ti-10-2-3"]),
    ("Ti-15V-3Cr-3Al-3Sn (Ti-15-3)", "Beta Titanium Alloy", ["ti-15-3", "ti-15v-3cr"]),
    ("Ti-3Al-8V-6Cr-4Mo-4Zr (Beta C)", "Beta Titanium Alloy", ["beta c", "ti-3al-8v-6cr"]),
    ("Ti-5Al-5V-5Mo-3Cr (Ti-5553)", "Beta Titanium Alloy", ["ti-5553", "ti-5al-5v-5mo-3cr"]),
]
for n, sub, s in ti_beta:
    alloys.append({"name": n, "cat": "Titanium", "sub": sub, "search": s})

# Titanium Aluminides
ti_aluminide = [
    ("Gamma TiAl (Ti-48Al-2Cr-2Nb)", "Titanium Aluminide", ["gamma tial", "ti-48al-2cr-2nb"]),
]
for n, sub, s in ti_aluminide:
    alloys.append({"name": n, "cat": "Titanium", "sub": sub, "search": s})

# --- GOLD ALLOYS ---
gold_grades = [
    ("Pure Gold (24K, 99.99%)", "Pure Gold", ["24k gold", "pure gold", "99.99% gold", "au 999"]),
    ("22K Gold Alloy (91.7% Au)", "Gold Alloy", ["22k gold", "22 karat"]),
    ("18K Yellow Gold Alloy (75% Au)", "Gold Alloy", ["18k yellow gold", "18 karat yellow"]),
    ("18K White Gold Alloy (75% Au)", "Gold Alloy", ["18k white gold", "18 karat white"]),
    ("18K Rose Gold Alloy (75% Au)", "Gold Alloy", ["18k rose gold", "18 karat rose"]),
    ("14K Yellow Gold Alloy (58.5% Au)", "Gold Alloy", ["14k yellow gold", "14 karat yellow"]),
    ("14K White Gold Alloy (58.5% Au)", "Gold Alloy", ["14k white gold", "14 karat white"]),
    ("10K Gold Alloy (41.7% Au)", "Gold Alloy", ["10k gold", "10 karat"]),
    ("Gold-Copper Alloy (Au-Cu)", "Gold-Copper Alloy", ["gold-copper", "au-cu alloy", "tumbaga"]),
    ("Dental Gold Alloy Type III", "Dental Gold", ["dental gold type iii", "dental gold type 3"]),
    ("Gold Bonding Wire (99.99% Au)", "Gold Wire", ["gold bonding wire", "au bonding wire"]),
]
for n, sub, s in gold_grades:
    alloys.append({"name": n, "cat": "Gold", "sub": sub, "search": s})

# --- SILVER ALLOYS ---
silver_grades = [
    ("Pure Silver (99.99% Ag, Fine Silver)", "Pure Silver", ["pure silver", "fine silver", "99.99% ag", "ag 999"]),
    ("Sterling Silver (92.5% Ag)", "Silver Alloy", ["sterling silver", "925 silver"]),
    ("Argentium Silver (93.5% Ag)", "Silver Alloy", ["argentium silver", "argentium 935"]),
    ("Coin Silver (90% Ag)", "Silver Alloy", ["coin silver", "90% silver"]),
    ("Silver-Copper Brazing Alloy (BAg-1, 45% Ag)", "Silver Brazing Alloy", ["bag-1", "45% silver braze", "silver brazing"]),
    ("Silver-Copper Brazing Alloy (BAg-7, 56% Ag)", "Silver Brazing Alloy", ["bag-7", "56% silver braze"]),
    ("Silver-Copper Eutectic (72Ag-28Cu)", "Silver-Copper Alloy", ["72ag-28cu", "silver-copper eutectic"]),
    ("Silver-Palladium Alloy (70Ag-30Pd)", "Silver-Palladium Alloy", ["silver-palladium", "ag-pd", "70ag-30pd"]),
    ("Silver Thick Film Paste (Conductor)", "Silver Paste", ["silver thick film", "silver paste conductor"]),
    ("Silver-Cadmium Oxide (AgCdO) Contact Material", "Electrical Contact", ["agcdo", "silver-cadmium oxide", "silver cadmium"]),
    ("Silver-Tungsten (AgW) Contact Material", "Electrical Contact", ["agw", "silver-tungsten", "silver tungsten"]),
]
for n, sub, s in silver_grades:
    alloys.append({"name": n, "cat": "Silver", "sub": sub, "search": s})

# --- URANIUM ALLOYS ---
uranium_grades = [
    ("Depleted Uranium (DU)", "Depleted Uranium", ["depleted uranium", "du metal"]),
    ("Natural Uranium Metal", "Natural Uranium", ["natural uranium", "unat"]),
    ("Enriched Uranium (LEU, 3-5% U-235)", "Enriched Uranium", ["enriched uranium", "leu"]),
    ("Uranium-0.75Ti (U-0.75Ti) Alloy", "Uranium-Titanium Alloy", ["u-0.75ti", "uranium-titanium", "staballoy"]),
    ("Uranium-6Nb (U-6Nb, Mulberry) Alloy", "Uranium-Niobium Alloy", ["u-6nb", "mulberry", "uranium-niobium"]),
    ("Uranium-2Mo (U-2Mo) Alloy", "Uranium-Molybdenum Alloy", ["u-2mo", "uranium-molybdenum"]),
    ("Uranium-10Mo (U-10Mo) Alloy", "Uranium-Molybdenum Alloy", ["u-10mo", "uranium 10 molybdenum"]),
    ("Uranium Dioxide (UO2) Nuclear Fuel", "Uranium Ceramic", ["uo2", "uranium dioxide", "uranium oxide fuel"]),
    ("Uranium-Zirconium (U-Zr) Alloy", "Uranium-Zirconium Alloy", ["u-zr", "uranium-zirconium"]),
    ("Uranium-Plutonium-Zirconium (U-Pu-Zr) Fuel", "Nuclear Fuel Alloy", ["u-pu-zr", "uranium-plutonium-zirconium"]),
]
for n, sub, s in uranium_grades:
    alloys.append({"name": n, "cat": "Uranium", "sub": sub, "search": s})

# 3. Deduplicate
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

# Count by category
from collections import Counter
cat_counts = Counter(m['category'] for m in missing_materials)
print(f"\nOut of {len(alloys)} total standard grades checked, {len(missing_materials)} are currently missing from your database:")
for cat, cnt in sorted(cat_counts.items()):
    print(f"  {cat}: {cnt} missing")

# 4. Generate CSV
headers = ['category', 'subcategory', 'name', 'density', 'tensile_strength_min', 'yield_strength_min', 
           'elongation', 'hardness', 'elastic_modulus', 'thermal_conductivity', 'specific_heat', 
           'melting_point_min', 'composition', 'description']

output_file = 'Missing_Ti_Au_Ag_U_Alloys_Template.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(missing_materials)

print(f"\nTemplate saved successfully to {output_file}!")
