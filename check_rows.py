
import csv

try:
    with open("broken_links_report.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"Total rows in CSV (including duplicates): {len(rows)}")
        
        materials = set(row["Material Name"].strip() for row in rows if "Material Name" in row and row["Material Name"])
        print(f"Total unique materials: {len(materials)}")
except Exception as e:
    print("Error:", e)

