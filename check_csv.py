
import csv
with open("batch1_material_sources.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
    mp_count = sum(1 for r in rows if r.get("source_name") == "Materials Project")
    print(f"Total rows: {len(rows)}, MP rows: {mp_count}")

