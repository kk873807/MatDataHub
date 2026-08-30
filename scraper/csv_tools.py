"""
Bulk CSV Import/Export tool for MatDataHub.

Usage:
    # Export current database to CSV
    python -m scraper.csv_tools export

    # Import materials from CSV
    python -m scraper.csv_tools import path/to/materials.csv

    # Import without clearing existing data
    python -m scraper.csv_tools import path/to/materials.csv --append
"""
import sys
import os
import csv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Material

# Fields that map directly from CSV columns to Material model
FIELDS = [
    "name", "category", "subcategory", "grade", "standard",
    "density", "tensile_strength_min", "tensile_strength_max",
    "yield_strength_min", "yield_strength_max", "elongation",
    "hardness", "elastic_modulus",
    "thermal_conductivity", "specific_heat",
    "melting_point_min", "melting_point_max", "max_service_temp",
    "cost_per_kg_min", "cost_per_kg_max", "cost_currency",
    "applications", "equivalent_grades", "composition", "description",
    "source_url", "source_name", "is_verified",
]

FLOAT_FIELDS = {
    "density", "tensile_strength_min", "tensile_strength_max",
    "yield_strength_min", "yield_strength_max", "elongation",
    "elastic_modulus", "thermal_conductivity", "specific_heat",
    "melting_point_min", "melting_point_max", "max_service_temp",
    "cost_per_kg_min", "cost_per_kg_max",
}

BOOL_FIELDS = {"is_verified"}


def parse_value(field, value):
    """Convert a CSV string value to the correct Python type."""
    if value is None or value.strip() == "":
        return None
    value = value.strip()
    if field in FLOAT_FIELDS:
        try:
            return float(value)
        except ValueError:
            return None
    if field in BOOL_FIELDS:
        return value.lower() in ("true", "1", "yes")
    return value


def import_csv(filepath, append=False):
    """Import materials from a CSV file into the database."""
    db = SessionLocal()

    try:
        if not append:
            count = db.query(Material).count()
            if count > 0:
                db.query(Material).delete()
                db.commit()
                print(f"  Cleared {count} existing materials.")

        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            inserted = 0
            skipped = 0
            for row in reader:
                # Skip rows without a name
                if not row.get("name", "").strip():
                    skipped += 1
                    continue

                # Build material data dict
                mat_data = {}
                for field in FIELDS:
                    if field in row:
                        mat_data[field] = parse_value(field, row[field])

                material = Material(**mat_data)
                db.add(material)
                inserted += 1

            db.commit()
            print(f"  Inserted {inserted} materials.")
            if skipped:
                print(f"  Skipped {skipped} rows (missing name).")

        # Summary
        total = db.query(Material).count()
        print(f"\n  TOTAL in database: {total} materials")
        for cat in ["Metal", "Polymer", "Ceramic", "Composite"]:
            n = db.query(Material).filter(Material.category == cat).count()
            if n > 0:
                print(f"    {cat:12s}  {n}")

    finally:
        db.close()


def export_csv(filepath="materials_export.csv"):
    """Export all materials from the database to a CSV file."""
    db = SessionLocal()

    try:
        materials = db.query(Material).order_by(Material.category, Material.name).all()

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()

            for m in materials:
                row = {}
                for field in FIELDS:
                    val = getattr(m, field, None)
                    row[field] = "" if val is None else str(val)
                writer.writerow(row)

        print(f"  Exported {len(materials)} materials to {filepath}")

    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python -m scraper.csv_tools export [output.csv]")
        print("  python -m scraper.csv_tools import input.csv [--append]")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "export":
        outfile = sys.argv[2] if len(sys.argv) > 2 else "materials_export.csv"
        print(f"\n=== Exporting materials to {outfile} ===\n")
        export_csv(outfile)

    elif action == "import":
        if len(sys.argv) < 3:
            print("Error: specify a CSV file to import")
            sys.exit(1)
        infile = sys.argv[2]
        append = "--append" in sys.argv
        mode = "APPEND" if append else "REPLACE"
        print(f"\n=== Importing materials from {infile} (mode: {mode}) ===\n")
        import_csv(infile, append=append)

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

    print("\n=== Done! ===\n")
