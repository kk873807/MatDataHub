import csv
from app.database import SessionLocal
from app.models import Material

csv_file = "C:/Users/KISHAN/.gemini/antigravity/brain/90857fe7-b886-4dbf-9d50-6634bcd34e13/.user_uploaded/accurate_copper_grades.csv"

db = SessionLocal()

try:
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            mat = Material(
                name=row["name"],
                category=row["category"],
                subcategory=row["subcategory"],
                standard=row["standards"],
                description=row["description"],
                tensile_strength_min=float(row["tensile_strength_mpa"]) if row["tensile_strength_mpa"] else None,
                yield_strength_min=float(row["yield_strength_mpa"]) if row["yield_strength_mpa"] else None,
                elongation=float(row["elongation_percent"]) if row["elongation_percent"] else None,
                hardness=row["hardness_brinell"] + " HB" if row["hardness_brinell"] else None,
                density=float(row["density_g_cm3"]) if row["density_g_cm3"] else None,
                thermal_conductivity=float(row["thermal_conductivity_w_mk"]) if row["thermal_conductivity_w_mk"] else None,
                melting_point_min=float(row["melting_point_c"]) if row["melting_point_c"] else None,
                specific_heat=float(row["specific_heat_j_kgk"]) if row["specific_heat_j_kgk"] else None,
                cost_per_kg_min=float(row["cost_per_kg"]) if row["cost_per_kg"] else None,
                embodied_carbon=float(row["carbon_footprint_kg_co2_kg"]) if row["carbon_footprint_kg_co2_kg"] else None,
                applications=row["applications"],
                temper_condition="Annealed" if "Cast" not in row["subcategory"] else "As-Cast",
                source_name="CDA / LME / ICA Projections",
                source_url="https://alloys.copper.org/"
            )
            db.add(mat)
            count += 1
    db.commit()
    print(f"Successfully inserted {count} copper grades into the database.")
except Exception as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()
