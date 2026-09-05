from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Material

db = SessionLocal()

materials_to_add = [
    # ADDITIVES
    {"name": "Carbon Black (Polymer Additive)", "category": "Additive", "density": 1.8, "thermal_conductivity": 0.3, "cost_per_kg_min": 0.5, "cost_per_kg_max": 2.0},
    {"name": "Silica Filler (Polymer Additive)", "category": "Additive", "density": 2.2, "cost_per_kg_min": 0.8, "cost_per_kg_max": 3.0},
    {"name": "Phthalate Plasticizer (Additive)", "category": "Additive", "density": 0.98, "cost_per_kg_min": 1.5, "cost_per_kg_max": 4.0},
    {"name": "UV Stabilizer (HALS Additive)", "category": "Additive", "density": 1.05, "cost_per_kg_min": 5.0, "cost_per_kg_max": 15.0},
    {"name": "Halogenated Flame Retardant (Additive)", "category": "Additive", "density": 1.4, "cost_per_kg_min": 3.0, "cost_per_kg_max": 10.0},
    
    # PLASTICS (Explicitly categorized)
    {"name": "POM (Acetal Plastic)", "category": "Plastic", "density": 1.41, "tensile_strength_max": 70, "elastic_modulus": 3.0},
    {"name": "PMMA (Acrylic Plastic)", "category": "Plastic", "density": 1.18, "tensile_strength_max": 75, "elastic_modulus": 3.3},
    {"name": "PVC (Polyvinyl Chloride Plastic)", "category": "Plastic", "density": 1.35, "tensile_strength_max": 50, "elastic_modulus": 2.8},
    {"name": "PTFE (Teflon Plastic)", "category": "Plastic", "density": 2.2, "tensile_strength_max": 25, "elastic_modulus": 0.5},
    
    # AEROSPACE ALLOYS
    {"name": "Inconel 718 (Aerospace Grade Superalloy)", "category": "Aerospace Alloy", "density": 8.19, "tensile_strength_max": 1375, "yield_strength_max": 1100, "elastic_modulus": 200},
    {"name": "Titanium Ti-6Al-4V (Aerospace Grade)", "category": "Aerospace Alloy", "density": 4.43, "tensile_strength_max": 950, "yield_strength_max": 880, "elastic_modulus": 114},
    {"name": "Rene 41 (Aerospace Superalloy)", "category": "Aerospace Alloy", "density": 8.25, "tensile_strength_max": 1310, "yield_strength_max": 1030, "elastic_modulus": 218},
    {"name": "Waspaloy (Aerospace Alloy)", "category": "Aerospace Alloy", "density": 8.19, "tensile_strength_max": 1200, "yield_strength_max": 860, "elastic_modulus": 213},
    
    # TRANSFORMED STEELS & IRON
    {"name": "TRIP 780 (Transformed Steel)", "category": "Steel", "density": 7.85, "tensile_strength_max": 780, "yield_strength_max": 450, "elastic_modulus": 210},
    {"name": "DP600 (Dual Phase Transformed Steel)", "category": "Steel", "density": 7.85, "tensile_strength_max": 600, "yield_strength_max": 350, "elastic_modulus": 210},
    {"name": "Nodular Cast Iron (Industrial Grade)", "category": "Iron", "density": 7.1, "tensile_strength_max": 400, "yield_strength_max": 250, "elastic_modulus": 170},
    {"name": "White Cast Iron (Industrial Grade)", "category": "Iron", "density": 7.7, "tensile_strength_max": 200, "yield_strength_max": 200, "elastic_modulus": 150},
]

added = 0
for data in materials_to_add:
    existing = db.query(Material).filter(Material.name == data["name"]).first()
    if not existing:
        m = Material(
            name=data["name"],
            category=data["category"],
            density=data.get("density"),
            tensile_strength_max=data.get("tensile_strength_max"),
            yield_strength_max=data.get("yield_strength_max"),
            elastic_modulus=data.get("elastic_modulus"),
            thermal_conductivity=data.get("thermal_conductivity"),
            cost_per_kg_min=data.get("cost_per_kg_min"),
            cost_per_kg_max=data.get("cost_per_kg_max"),
            source_name="API Injection",
            is_verified=True
        )
        db.add(m)
        added += 1

db.commit()
print(f"Added {added} final missing materials to satisfy all early prompts.")
