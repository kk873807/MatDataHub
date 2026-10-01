
import csv

materials = set()
try:
    with open("broken_links_report.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "Material Name" in row and row["Material Name"]:
                materials.add(row["Material Name"].strip())
except Exception as e:
    print("Error:", e)

with open("broken_materials_clean.txt", "w", encoding="utf-8") as f:
    for m in sorted(materials):
        f.write(m + "\n")
        print(m)

