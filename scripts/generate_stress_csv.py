"""
Generate a large CSV (50,000 rows) for stress-testing the CBAM BOM processor.
Usage: python scripts/generate_stress_csv.py
Output: scripts/stress_test_50k.csv
"""
import csv
import random
import os

ROWS = 50_000
OUTPUT = os.path.join(os.path.dirname(__file__), "stress_test_50k.csv")

SECTORS = ["Iron & Steel", "Cement", "Aluminium", "Fertilisers", "Hydrogen"]
CN_CODES = {
    "Iron & Steel": ["7208 51 00", "7207 11 14", "7209 15 00"],
    "Cement":       ["2523 29 00", "2523 21 00"],
    "Aluminium":    ["7601 10 00", "7604 29 10", "7606 11 10"],
    "Fertilisers":  ["3102 10 10", "3105 20 10"],
    "Hydrogen":     ["2804 10 00"],
}
COUNTRIES_NON_EU = ["China", "India", "Turkey", "Russia", "South Korea", "Brazil", "Japan", "USA", "Vietnam", "Indonesia"]
COUNTRIES_EU = ["Germany", "France", "Italy", "Spain", "Netherlands"]
SUPPLIERS = [
    "ArcelorMittal", "Tata Steel", "HeidelbergCement", "Norsk Hydro", "RUSAL",
    "Baowu Steel", "JSW Steel", "Vedanta", "Yara International", "Air Liquide",
    "ThyssenKrupp", "POSCO", "Nippon Steel", "CEMEX", "LafargeHolcim",
    "Hindalco", "Alcoa", "Rio Tinto", "BHP", "Vale"
]
MATERIALS = {
    "Iron & Steel": ["Hot-Rolled Steel Coil", "Cold-Rolled Steel Sheet", "Steel Rebar", "Steel Wire Rod", "Stainless Steel Plate"],
    "Cement":       ["Portland Cement", "Blended Cement", "White Cement", "Slag Cement"],
    "Aluminium":    ["Aluminium Ingot", "Aluminium Extrusion", "Aluminium Sheet", "Aluminium Wire"],
    "Fertilisers":  ["Urea Fertiliser", "Ammonium Nitrate", "NPK Blend"],
    "Hydrogen":     ["Grey Hydrogen", "Blue Hydrogen"],
}

def gen_row(i):
    sector = random.choice(SECTORS)
    cn_code = random.choice(CN_CODES[sector])
    material = random.choice(MATERIALS[sector])
    
    # 90% non-EU, 10% EU (which should be exempted)
    if random.random() < 0.10:
        origin = random.choice(COUNTRIES_EU)
    else:
        origin = random.choice(COUNTRIES_NON_EU)
    
    weight_kg = round(random.uniform(100, 500000), 2)
    direct_emissions = round(random.uniform(0.3, 3.0), 4)
    indirect_emissions = round(random.uniform(0.05, 1.5), 4)
    
    # 20% have paid some domestic carbon price
    carbon_price_paid = round(random.uniform(5, 60), 2) if random.random() < 0.20 else 0.0
    
    supplier = random.choice(SUPPLIERS)
    supplier_risk = random.randint(10, 95)
    single_source = random.choice(["Yes", "No"])
    geo_risk = random.choice(["Low", "Medium", "High"])
    
    # 5% have missing sector (edge case)
    if random.random() < 0.05:
        sector = ""
    
    # 3% have missing weight (edge case)
    if random.random() < 0.03:
        weight_kg = ""
    
    # Dates: 95% post-2026, 5% pre-2026
    if random.random() < 0.05:
        year = random.choice([2024, 2025])
    else:
        year = random.choice([2026, 2027, 2028, 2029, 2030])
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    shipment_date = f"{year}-{month:02d}-{day:02d}"
    
    return {
        "material_id": f"MAT-{i:06d}",
        "Material": material,
        "Weight_kg": weight_kg,
        "cbam_sector": sector,
        "cn_code": cn_code,
        "country_of_origin": origin,
        "destination": "Germany",
        "shipment_date": shipment_date,
        "supplier": supplier,
        "direct_emissions": direct_emissions,
        "indirect_emissions": indirect_emissions,
        "carbon_price_paid": carbon_price_paid,
        "supplier_risk_score": supplier_risk,
        "single_source_flag": single_source,
        "geopolitical_risk": geo_risk,
    }

def main():
    print(f"Generating {ROWS:,} rows...")
    fieldnames = [
        "material_id", "Material", "Weight_kg", "cbam_sector", "cn_code",
        "country_of_origin", "destination", "shipment_date", "supplier",
        "direct_emissions", "indirect_emissions", "carbon_price_paid",
        "supplier_risk_score", "single_source_flag", "geopolitical_risk"
    ]
    
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, ROWS + 1):
            writer.writerow(gen_row(i))
            if i % 10000 == 0:
                print(f"  ...{i:,} rows written")
    
    size_mb = os.path.getsize(OUTPUT) / (1024 * 1024)
    print(f"Done! {OUTPUT} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    main()
