"""
Integration test: exercises the REAL BOMProcessor with all requested edge cases.
Run: $env:PYTHONPATH="."; python scripts/test_integration_edgecases.py
"""
import sys, os, io, re, csv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from app.database import SessionLocal
from app.workflows import BOMProcessor

PASSED = 0
FAILED = 0
ERRORS = []

def check(name, condition, detail=""):
    global PASSED, FAILED, ERRORS
    if condition:
        PASSED += 1
        print(f"  PASS  {name}")
    else:
        FAILED += 1
        ERRORS.append(f"{name}: {detail}")
        print(f"  FAIL  {name}: {detail}")


db = SessionLocal()
processor = BOMProcessor(db)

# Build the CSV with ALL requested edge cases
CSV = """material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin,destination,release_date,supplier,importer,other_cbam_imports_t,direct_emissions,indirect_emissions,carbon_price_paid
EX-50A,Test Mat,50000,Iron & Steel,7208 51 00,China,Germany,2026-06-15,Acme,Imp-Exactly-50,0,,,
EX-50B,Test Mat,50000.001,Iron & Steel,7208 51 00,China,Germany,2026-06-15,Acme,Imp-Over-50,0,,,
EX-Y1,Test Mat,30000,Iron & Steel,7208 51 00,China,Germany,2026-06-15,Acme,Imp-CrossYear,0,,,
EX-Y2,Test Mat,30000,Iron & Steel,7208 51 00,China,Germany,2027-01-15,Acme,Imp-CrossYear,0,,,
EX-Y3,Test Mat,30000,Iron & Steel,7208 51 00,China,Germany,2026-11-15,Acme,Imp-SameYear,0,,,
EX-Y4,Test Mat,30000,Iron & Steel,7208 51 00,China,Germany,2026-12-15,Acme,Imp-SameYear,0,,,
EX-I1,Test Mat,40000,Iron & Steel,7208 51 00,China,Germany,2026-06-15,Acme,Imp-A,0,,,
EX-I2,Test Mat,40000,Iron & Steel,7208 51 00,China,Germany,2026-06-15,Acme,Imp-B,0,,,
EX-O1,Test Mat,30000,Iron & Steel,7208 51 00,China,Germany,2026-06-15,Acme,Imp-Other,30.0,,,
EX-O2,Test Mat,20000,Iron & Steel,7208 51 00,China,Germany,2026-06-16,Acme,Imp-Other,30.0,,,
EX-CN,Test Mat,30000,Unrecognized,7208 51 00,China,Germany,2026-06-15,Acme,Imp-CN-Rescue,0,,,
EX-PLA,Plastic-Coated Pipe,30000,Iron & Steel,7306 11 00,China,Germany,2026-06-15,Acme,Imp-PlasticGuard,0,,,
EX-SHORT,Short CN,10000,Iron & Steel,7202,China,Germany,2026-06-15,Acme,Imp-Short,0,,,
"""

df = pd.read_csv(io.StringIO(CSV), dtype=str)
df["Weight_kg"] = pd.to_numeric(df["Weight_kg"], errors="coerce").fillna(0)
result = processor.process_bom(df, "Material", "Weight_kg")

rows = result.to_dict(orient="records")
def row(mat_id):
    return next(r for r in rows if r.get("material_id") == mat_id)

print("\n=== De Minimis EXACT 50t vs 50.001t ===")
r50a = row("EX-50A")
r50b = row("EX-50B")
check("Exactly 50t is exempt", "Possibly exempt" in str(r50a.get("DeMinimis_Status", "")), f"{r50a.get('DeMinimis_Status')}")
check("50.001t is NOT exempt", "Not exempt" in str(r50b.get("DeMinimis_Status", "")), f"{r50b.get('DeMinimis_Status')}")

print("\n=== De Minimis Cross-Year vs Same-Year ===")
ry1 = row("EX-Y1")
ry2 = row("EX-Y2")
ry3 = row("EX-Y3")
check("Cross-year separates totals", "Possibly exempt" in str(ry1.get("DeMinimis_Status", "")) and "Possibly exempt" in str(ry2.get("DeMinimis_Status", "")), f"Y1: {ry1.get('DeMinimis_Status')}, Y2: {ry2.get('DeMinimis_Status')}")
check("Same-year adds up", "Not exempt" in str(ry3.get("DeMinimis_Status", "")), f"{ry3.get('DeMinimis_Status')}")

print("\n=== De Minimis Multiple Importers ===")
ri1 = row("EX-I1")
ri2 = row("EX-I2")
check("Two importers at 40t each separate", "Possibly exempt" in str(ri1.get("DeMinimis_Status", "")) and "Possibly exempt" in str(ri2.get("DeMinimis_Status", "")), f"I1: {ri1.get('DeMinimis_Status')}")

print("\n=== De Minimis Other Imports Input ===")
ro1 = row("EX-O1")
ro2 = row("EX-O2")
check("Other imports correctly push over 50t limit", "Not exempt" in str(ro1.get("DeMinimis_Status", "")), f"{ro1.get('DeMinimis_Status')}")
check("Repeated other imports count only once per group", "50.0t in file, 30.0t other" in str(ro1.get("Notes", "")), f"{ro1.get('Notes')}")

print("\n=== CN-Rescued Row Counts Toward Threshold ===")
rcn = row("EX-CN")
check("CN-rescued row is in scope and counts to de minimis", "YES" in str(rcn.get("Included_In_Total", "")), f"{rcn.get('Included_In_Total')}")
check("CN-rescued row eligible mass", rcn.get("DeMinimis_Eligible_Mass_kg", 0) > 0, f"{rcn.get('DeMinimis_Eligible_Mass_kg')}")

print("\n=== Plastic-Coated Pipe Guard ===")
rpla = row("EX-PLA")
check("7306 pipe stays in scope despite polymer match", "YES" in str(rpla.get("Included_In_Total", "")) or "QUARANTINE" in str(rpla.get("Included_In_Total", "")), f"{rpla.get('Included_In_Total')}")
check("CN evidence wins over fuzzy polymer", "OUT OF SCOPE" not in str(rpla.get("Included_In_Total", "")), f"{rpla.get('Included_In_Total')}")

print("\n=== Short CN Code ===")
rsh = row("EX-SHORT")
check("Short CN is quarantined as incomplete", "Incomplete" in str(rsh.get("Validation_Errors", "")), f"{rsh.get('Validation_Errors')}")

print("\n=== Regulatory Diagnostics Output ===")
check("Outputs Annex I Reg Version", "Regulation (EU) 2023/956 Annex I" in str(r50a.get("CBAM_Defaults_Info", "")), f"{r50a.get('CBAM_Defaults_Info')}")

print(f"\n{'='*60}")
print(f"  INTEGRATION TEST COMPLETE")
print(f"  PASS: {PASSED}")
print(f"  FAIL: {FAILED}")
if ERRORS:
    print(f"\n  Failures:")
    for e in ERRORS:
        print(f"    * {e}")
print(f"{'='*60}")

db.close()
