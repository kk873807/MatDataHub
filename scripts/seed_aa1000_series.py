"""
Seed script: AA 1000 Series (Commercially Pure Wrought Aluminum)
All 15 alloys scraped from MakeItFrom.com on 2026-09-16.
Data is inserted directly into the Supabase PostgreSQL database.

Usage:
    python scripts/seed_aa1000_series.py
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models import Material, MaterialSource

materials_data = [
    # ── 1. 1050 (A91050) Aluminum ──
    {
        "name": "1050 (A91050) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1050",
        "standard": "AA, EN, UNS",
        "density": 2.7,
        "tensile_strength_min": 76,
        "tensile_strength_max": 140,
        "yield_strength_min": 25,
        "yield_strength_max": 120,
        "elastic_modulus": 68,
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 640,
        "melting_point_max": 650,
        "max_service_temp": 170,
        "embodied_carbon": 8.3,
        "composition": "Al 99.5-100%, Fe 0-0.4%, Si 0-0.25%, Mn 0-0.050%, Cu 0-0.050%, Mg 0-0.050%, Ti 0-0.050%, Zn 0-0.050%",
        "equivalent_grades": "A91050, EN AW-1050, Al99,5",
        "uns_number": "A91050",
        "en_number": "EN AW-1050",
        "source_url": "https://www.makeitfrom.com/material-properties/1050-A91050-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 2. 1050A (Al99.5, 3.0255, 1B) Aluminum ──
    {
        "name": "1050A (Al99.5, 3.0255, 1B) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1050A",
        "standard": "ISO 6361-2, EN 573-3, EN 755-2, EN 485-2, EN 754-2, BS, AFNOR",
        "density": 2.7,
        "tensile_strength_min": 68,
        "tensile_strength_max": 170,
        "yield_strength_min": 22,
        "yield_strength_max": 150,
        "elastic_modulus": 68,
        "hardness": "20-45 HB",
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 650,
        "melting_point_max": 660,
        "max_service_temp": 170,
        "embodied_carbon": 8.2,
        "composition": "Al 99.5-100%, Fe 0-0.4%, Si 0-0.25%, Zn 0-0.070%, Mn 0-0.050%, Cu 0-0.050%, Ti 0-0.050%, Mg 0-0.050%",
        "equivalent_grades": "EN AW-1050A, Al99.5, 3.0255, 1B, A5",
        "en_number": "EN AW-1050A",
        "din_number": "3.0255",
        "source_url": "https://www.makeitfrom.com/material-properties/1050A-Al99.5-3.0255-1B-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 3. 1060 (Al99.6, A91060) Aluminum ──
    {
        "name": "1060 (Al99.6, A91060) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1060",
        "standard": "ASTM B209, ASTM B210, ASTM B211, ASTM B221, ASTM B483, EN, AA, UNS",
        "density": 2.7,
        "tensile_strength_min": 67,
        "tensile_strength_max": 130,
        "yield_strength_min": 17,
        "yield_strength_max": 110,
        "elastic_modulus": 68,
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 650,
        "melting_point_max": 660,
        "max_service_temp": 170,
        "embodied_carbon": 8.3,
        "composition": "Al 99.6-100%, Fe 0-0.35%, Si 0-0.25%, Cu 0-0.050%, V 0-0.050%, Zn 0-0.050%, Mn 0-0.030%, Ti 0-0.030%, Mg 0-0.030%",
        "equivalent_grades": "Al99.6, A91060, EN AW-1060, AA 1060",
        "uns_number": "A91060",
        "en_number": "EN AW-1060",
        "source_url": "https://www.makeitfrom.com/material-properties/1060-Al99.6-A91060-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 4. 1070 (Al99.7) Aluminum ──
    {
        "name": "1070 (Al99.7) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1070",
        "standard": "AA, EN, UNS",
        "density": 2.7,
        "tensile_strength_min": 73,
        "tensile_strength_max": 140,
        "yield_strength_min": 17,
        "yield_strength_max": 120,
        "elastic_modulus": 68,
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 640,
        "melting_point_max": 640,
        "max_service_temp": 170,
        "embodied_carbon": 8.3,
        "composition": "Al 99.7-100%, Fe 0-0.25%, Si 0-0.2%",
        "equivalent_grades": "EN AW-1070, Al99,7, UNS A91070",
        "uns_number": "A91070",
        "en_number": "EN AW-1070",
        "source_url": "https://www.makeitfrom.com/material-properties/1070-Al99.7-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 5. 1070A (Al99.7(A), 3.0275) Aluminum ──
    {
        "name": "1070A (Al99.7(A), 3.0275) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1070A",
        "standard": "AA, EN, AFNOR",
        "density": 2.7,
        "tensile_strength_min": 68,
        "tensile_strength_max": 140,
        "yield_strength_min": 17,
        "yield_strength_max": 120,
        "elastic_modulus": 68,
        "hardness": "18-40 HB",
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 640,
        "melting_point_max": 640,
        "max_service_temp": 170,
        "embodied_carbon": 8.2,
        "composition": "Al 99.7-100%, Fe 0-0.25%, Si 0-0.2%, Zn 0-0.070%, Cu 0-0.030%, Mg 0-0.030%, Mn 0-0.030%, Ti 0-0.030%",
        "equivalent_grades": "EN AW-1070A, Al99.7(A), AFNOR A7, 3.0275",
        "en_number": "EN AW-1070A",
        "din_number": "3.0275",
        "source_url": "https://www.makeitfrom.com/material-properties/1070A-Al99.7A-3.0275-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 6. 1080 (Al99.8) Aluminum ──
    {
        "name": "1080 (Al99.8) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1080",
        "standard": "EN, AA, UNS",
        "density": 2.7,
        "tensile_strength_min": 72,
        "tensile_strength_max": 130,
        "yield_strength_min": 17,
        "yield_strength_max": 120,
        "elastic_modulus": 68,
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 640,
        "melting_point_max": 640,
        "max_service_temp": 170,
        "embodied_carbon": 8.3,
        "composition": "Al 99.8-100%, Si 0-0.15%, Fe 0-0.15%, V 0-0.050%, Ga 0-0.030%, Ti 0-0.030%, Zn 0-0.030%, Cu 0-0.030%, Mg 0-0.020%, Mn 0-0.020%",
        "equivalent_grades": "EN AW-1080, Al99,8, AA 1080, UNS A91080",
        "uns_number": "A91080",
        "en_number": "EN AW-1080",
        "source_url": "https://www.makeitfrom.com/material-properties/1080-Al99.8-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 7. 1080A (Al99.8(A), 3.0285, 1A) Aluminum ──
    {
        "name": "1080A (Al99.8(A), 3.0285, 1A) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1080A",
        "standard": "EN 485-2, EN 573-3, ISO 6361-2, AA, BS, AFNOR",
        "density": 2.7,
        "tensile_strength_min": 74,
        "tensile_strength_max": 140,
        "yield_strength_min": 17,
        "yield_strength_max": 120,
        "elastic_modulus": 68,
        "hardness": "18-40 HB",
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 640,
        "melting_point_max": 640,
        "max_service_temp": 170,
        "embodied_carbon": 8.3,
        "composition": "Al 99.8-100%, Si 0-0.15%, Fe 0-0.15%, Zn 0-0.060%, Cu 0-0.030%, Ga 0-0.030%, Mn 0-0.020%, Ti 0-0.020%, Mg 0-0.020%",
        "equivalent_grades": "Al99.8(A), 3.0285, 1A, EN AW-1080A, AFNOR A8",
        "en_number": "EN AW-1080A",
        "din_number": "3.0285",
        "source_url": "https://www.makeitfrom.com/material-properties/1080A-Al99.8A-3.0285-1A-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 8. 1085 (Al99.85) Aluminum ──
    {
        "name": "1085 (Al99.85) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1085",
        "standard": "AA, EN (EN AW-1085, EN 573-3), ISO 6361-2, UNS",
        "density": 2.7,
        "tensile_strength_min": 73,
        "tensile_strength_max": 140,
        "yield_strength_min": 17,
        "yield_strength_max": 120,
        "elastic_modulus": 68,
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 640,
        "melting_point_max": 640,
        "max_service_temp": 170,
        "embodied_carbon": 8.3,
        "composition": "Al 99.85-100%, Fe 0-0.12%, Si 0-0.10%, V 0-0.050%, Cu 0-0.030%, Ga 0-0.030%, Zn 0-0.030%, Mg 0-0.020%, Mn 0-0.020%, Ti 0-0.020%",
        "equivalent_grades": "EN AW-1085, Al99.85, UNS A91085, AA 1085",
        "uns_number": "A91085",
        "en_number": "EN AW-1085",
        "source_url": "https://www.makeitfrom.com/material-properties/1085-Al99.85-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 9. 1100 (Al99.0Cu, A91100) Aluminum ──
    {
        "name": "1100 (Al99.0Cu, A91100) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1100",
        "standard": "AA, EN, ASTM",
        "density": 2.7,
        "tensile_strength_min": 86,
        "tensile_strength_max": 170,
        "yield_strength_min": 28,
        "yield_strength_max": 150,
        "elastic_modulus": 69,
        "thermal_conductivity": 220,
        "specific_heat": 900,
        "melting_point_min": 640,
        "melting_point_max": 660,
        "max_service_temp": 180,
        "embodied_carbon": 8.2,
        "composition": "Al 99.0-99.95%, Cu 0.050-0.20%, Fe 0-1.0%, Si 0-1.0%, Zn 0-0.10%, Mn 0-0.050%",
        "equivalent_grades": "UNS A91100, EN AW-1100, Al99.0Cu",
        "uns_number": "A91100",
        "en_number": "EN AW-1100",
        "source_url": "https://www.makeitfrom.com/material-properties/1100-Al99.0Cu-A91100-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 10. 1100A (Al99.0Cu(A)) Aluminum ──
    {
        "name": "1100A (Al99.0Cu(A)) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1100A",
        "standard": "AA, EN, AFNOR",
        "density": 2.7,
        "tensile_strength_min": 89,
        "tensile_strength_max": 170,
        "yield_strength_min": 29,
        "yield_strength_max": 150,
        "elastic_modulus": 69,
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 640,
        "melting_point_max": 640,
        "max_service_temp": 170,
        "embodied_carbon": 8.2,
        "composition": "Al 99.0-100%, Cu 0.050-0.20%, Fe 0-1.0%, Si 0-1.0%, Ti 0-0.10%, Zn 0-0.10%, Mg 0-0.10%, Mn 0-0.050%",
        "equivalent_grades": "EN AW-1100A, Al99.0Cu(A), AFNOR A45",
        "en_number": "EN AW-1100A",
        "source_url": "https://www.makeitfrom.com/material-properties/1100A-Al99.0CuA-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 11. 1200 (Al99.0, 3.0205, 1C, A91200) Aluminum ──
    {
        "name": "1200 (Al99.0, 3.0205, 1C, A91200) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1200",
        "standard": "AA, EN 485-2, EN 573-3, EN 754-2, EN 755-2, ASTM B491, ISO 6361-2, BS, AFNOR",
        "density": 2.7,
        "tensile_strength_min": 85,
        "tensile_strength_max": 180,
        "yield_strength_min": 28,
        "yield_strength_max": 160,
        "elastic_modulus": 69,
        "hardness": "23-48 HB",
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 650,
        "melting_point_max": 660,
        "max_service_temp": 170,
        "embodied_carbon": 8.2,
        "composition": "Al 99.0-100%, Fe 0-1.0%, Si 0-1.0%, Zn 0-0.10%, Cu 0-0.050%, Mn 0-0.050%, Ti 0-0.050%",
        "equivalent_grades": "Al99.0, 3.0205, EN AW-1200, A91200, BS 1C, AFNOR A-4",
        "uns_number": "A91200",
        "en_number": "EN AW-1200",
        "din_number": "3.0205",
        "source_url": "https://www.makeitfrom.com/material-properties/1200-Al99.0-3.0205-1C-A91200-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 12. 1230A Aluminum ──
    {
        "name": "1230A Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1230A",
        "standard": "AA, EN",
        "density": 2.7,
        "tensile_strength_min": 89,
        "tensile_strength_max": 170,
        "yield_strength_min": 29,
        "yield_strength_max": 150,
        "elastic_modulus": 69,
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 640,
        "melting_point_max": 640,
        "max_service_temp": 170,
        "embodied_carbon": 8.2,
        "composition": "Al 99.3-100%, Si 0-0.7%, Fe 0-0.7%, Cu 0-0.1%, Mn 0-0.050%, Mg 0-0.050%, Zn 0-0.050%",
        "equivalent_grades": "EN AW-1230A",
        "en_number": "EN AW-1230A",
        "source_url": "https://www.makeitfrom.com/material-properties/1230A-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 13. 1235 (Al99.35, A91235) Aluminum ──
    {
        "name": "1235 (Al99.35, A91235) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1235",
        "standard": "AA, EN, UNS",
        "density": 2.7,
        "tensile_strength_min": 80,
        "tensile_strength_max": 84,
        "yield_strength_min": 23,
        "yield_strength_max": 57,
        "elastic_modulus": 69,
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 640,
        "melting_point_max": 640,
        "max_service_temp": 170,
        "embodied_carbon": 8.3,
        "composition": "Al 99.35-100%, Si 0-0.65%, Fe 0-0.65%, Zn 0-0.1%, Ti 0-0.060%, Cu 0-0.050%, Mn 0-0.050%, Mg 0-0.050%",
        "equivalent_grades": "Al99.35, A91235, EN AW-1235",
        "uns_number": "A91235",
        "en_number": "EN AW-1235",
        "source_url": "https://www.makeitfrom.com/material-properties/1235-Al99.35-A91235-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 14. 1350 (E-Al99.5, EC, 3.0257, 1E, A91350) Aluminum ──
    {
        "name": "1350 (E-Al99.5, EC, 3.0257, 1E, A91350) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1350",
        "standard": "ASTM B230, ASTM B233, ASTM B236, ASTM B609, EN 485-2, EN 755-2",
        "density": 2.7,
        "tensile_strength_min": 68,
        "tensile_strength_max": 190,
        "yield_strength_min": 25,
        "yield_strength_max": 170,
        "elastic_modulus": 68,
        "hardness": "20-45 HB",
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 650,
        "melting_point_max": 660,
        "max_service_temp": 170,
        "embodied_carbon": 8.3,
        "composition": "Al 99.5-100%, Fe 0-0.4%, Si 0-0.1%, B 0-0.050%, Zn 0-0.050%, Cu 0-0.050%, Ga 0-0.030%, Ti 0-0.020%, V 0-0.020%, Mn 0-0.010%, Cr 0-0.010%",
        "equivalent_grades": "E-Al99.5, EC, 3.0257, 1E, UNS A91350, EN AW-1350",
        "uns_number": "A91350",
        "en_number": "EN AW-1350",
        "din_number": "3.0257",
        "source_url": "https://www.makeitfrom.com/material-properties/1350-E-Al99.5-EC-3.0257-1E-A91350-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
    # ── 15. 1435 (A91435) Aluminum ──
    {
        "name": "1435 (A91435) Aluminum",
        "category": "Metal",
        "subcategory": "Aluminum Alloy",
        "grade": "1435",
        "standard": "ASTM B483, AA, EN, UNS",
        "density": 2.7,
        "tensile_strength_min": 81,
        "tensile_strength_max": 150,
        "yield_strength_min": 23,
        "yield_strength_max": 130,
        "elastic_modulus": 69,
        "thermal_conductivity": 230,
        "specific_heat": 900,
        "melting_point_min": 640,
        "melting_point_max": 650,
        "max_service_temp": 170,
        "embodied_carbon": 8.2,
        "composition": "Al 99.35-99.7%, Fe 0.30-0.50%, Si 0-0.15%",
        "equivalent_grades": "AA 1435, UNS A91435, EN AW-1435",
        "uns_number": "A91435",
        "en_number": "EN AW-1435",
        "source_url": "https://www.makeitfrom.com/material-properties/1435-A91435-Aluminum",
        "source_name": "MakeItFrom.com",
        "is_verified": True,
    },
]


def run_seed():
    """Insert all AA 1000 series materials into the database, skipping duplicates."""
    db = SessionLocal()
    added = 0
    skipped = 0

    for data in materials_data:
        # Check for existing material by name to avoid duplicates
        exists = db.query(Material).filter(Material.name == data["name"]).first()
        if exists:
            skipped += 1
            print(f"  >> Skipped (already exists): {data['name']}")
            continue

        # Pop the source fields before creating the Material
        source_url = data.get("source_url")
        source_name_val = data.get("source_name")

        mat = Material(**data)
        db.add(mat)
        db.flush()  # Get the ID for the MaterialSource relation

        # Also add a proper MaterialSource entry for traceability
        if source_url:
            src = MaterialSource(
                material_id=mat.id,
                source_type="database",
                source_name=source_name_val or "MakeItFrom.com",
                source_url=source_url,
                access_type="free",
                confidence_score=0.9,
                notes="Scraped from MakeItFrom.com AA 1000 Series page (Sep 2026)",
            )
            db.add(src)

        added += 1
        print(f"  [+] Added: {data['name']}")

    db.commit()
    db.close()
    print(f"\n{'='*50}")
    print(f"  Total added:   {added}")
    print(f"  Total skipped: {skipped}")
    print(f"  Total in list: {len(materials_data)}")
    print(f"{'='*50}")
    return added


if __name__ == "__main__":
    print("[SEED] Seeding AA 1000 Series (Commercially Pure Wrought Aluminum)...")
    print(f"   Database: {os.getenv('DATABASE_URL', 'sqlite:///./matdatahub_dev.db')[:50]}...")
    print()
    added = run_seed()
    print(f"\n[DONE] Seeded {added} AA 1000 series materials.")
