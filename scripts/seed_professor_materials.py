import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models import Material

mats = [
    {
        "name": "Inconel 718",
        "category": "Metal",
        "subcategory": "Nickel Superalloy",
        "grade": "718",
        "standard": "UNS N07718",
        "density": 8.19,
        "tensile_strength_min": 1375,
        "tensile_strength_max": 1450,
        "yield_strength_min": 1100,
        "yield_strength_max": 1200,
        "elongation": 12,
        "elastic_modulus": 204.9,
        "thermal_conductivity": 11.4,
        "max_service_temp": 704,
        "cost_per_kg_min": 2500,
        "cost_per_kg_max": 3500,
        "applications": "Gas turbine engines, aerospace structures, nuclear reactors"
    },
    {
        "name": "Inconel 625",
        "category": "Metal",
        "subcategory": "Nickel Superalloy",
        "grade": "625",
        "standard": "UNS N06625",
        "density": 8.44,
        "tensile_strength_min": 827,
        "tensile_strength_max": 1034,
        "yield_strength_min": 414,
        "yield_strength_max": 650,
        "elongation": 30,
        "elastic_modulus": 207,
        "thermal_conductivity": 9.8,
        "max_service_temp": 982,
        "cost_per_kg_min": 2200,
        "cost_per_kg_max": 3000,
        "applications": "Marine applications, chemical processing equipment, aerospace exhaust systems"
    },
    {
        "name": "Aluminum 6061-T6",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "6061",
        "standard": "UNS A96061",
        "density": 2.70,
        "tensile_strength_min": 290,
        "tensile_strength_max": 310,
        "yield_strength_min": 240,
        "yield_strength_max": 275,
        "elongation": 10,
        "elastic_modulus": 68.9,
        "thermal_conductivity": 167,
        "max_service_temp": 150,
        "cost_per_kg_min": 250,
        "cost_per_kg_max": 400,
        "applications": "Bicycle frames, aircraft structures, automotive parts"
    },
    {
        "name": "Aluminum 7075-T6",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "7075",
        "standard": "UNS A97075",
        "density": 2.81,
        "tensile_strength_min": 572,
        "tensile_strength_max": 590,
        "yield_strength_min": 503,
        "yield_strength_max": 520,
        "elongation": 11,
        "elastic_modulus": 71.7,
        "thermal_conductivity": 130,
        "max_service_temp": 120,
        "cost_per_kg_min": 450,
        "cost_per_kg_max": 750,
        "applications": "Aerospace structural components, high-stress military applications"
    },
    {
        "name": "Aluminum 2024-T3",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "2024",
        "standard": "UNS A92024",
        "density": 2.78,
        "tensile_strength_min": 427,
        "tensile_strength_max": 483,
        "yield_strength_min": 290,
        "yield_strength_max": 345,
        "elongation": 15,
        "elastic_modulus": 73.1,
        "thermal_conductivity": 121,
        "max_service_temp": 150,
        "cost_per_kg_min": 350,
        "cost_per_kg_max": 600,
        "applications": "Aircraft fittings, gears and shafts, clock parts"
    },
    {
        "name": "Aluminum 5052-H32",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "5052",
        "standard": "UNS A95052",
        "density": 2.68,
        "tensile_strength_min": 228,
        "tensile_strength_max": 260,
        "yield_strength_min": 193,
        "yield_strength_max": 215,
        "elongation": 12,
        "elastic_modulus": 70.3,
        "thermal_conductivity": 138,
        "max_service_temp": 200,
        "cost_per_kg_min": 200,
        "cost_per_kg_max": 350,
        "applications": "Marine environments, electronic enclosures, fuel tanks"
    },
    {
        "name": "Aluminum 1100-H14",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1100",
        "standard": "UNS A91100",
        "density": 2.71,
        "tensile_strength_min": 110,
        "tensile_strength_max": 125,
        "yield_strength_min": 95,
        "yield_strength_max": 105,
        "elongation": 20,
        "elastic_modulus": 68.9,
        "thermal_conductivity": 220,
        "max_service_temp": 250,
        "cost_per_kg_min": 180,
        "cost_per_kg_max": 300,
        "applications": "Chemical equipment, food handling equipment, heat exchangers"
    }
]

def run_seed():
    db = SessionLocal()
    added = 0
    for data in mats:
        exists = db.query(Material).filter(Material.name == data["name"]).first()
        if not exists:
            mat = Material(**data, source_name="Industry Standard Seed", is_verified=True)
            db.add(mat)
            added += 1

    db.commit()
    db.close()
    return added

if __name__ == "__main__":
    added = run_seed()
    print(f"Seeded {added} high-grade materials (Inconel & Aluminum).")
