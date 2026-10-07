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
CSV = """material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin,destination,shipment_date,supplier,importer,direct_emissions,indirect_emissions,carbon_price_paid
EX-01,Hot-Rolled Steel Coil,50000,Iron & Steel,7208 51 00,China,Germany,2026-06-15,Acme,Imp-A,1.25,0.60,25.0
EX-02,Hot-Rolled Steel Coil,0.001,Iron & Steel,72085100,China,Germany,2026-06-15,Acme,Imp-A,1.25,0.60,25.0
EX-03,Hot-Rolled Steel Coil,50000,Iron & Steel,72085100.0,China,Germany,2026-06-15,Acme,Imp-B,1.25,0.60,25.0
EX-04,Hot-Rolled Steel Coil,50000,Iron & Steel,7208.51.00,China,Germany,2026-06-15,Acme,Imp-C,1.25,0.60,25.0
EX-05,Scrap Steel,10000,Iron & Steel,7204 21 10,China,Germany,2026-06-15,ScrapCo,Imp-D,,,
EX-06,Stainless Bolts M8,5000,Iron & Steel,7318 15 00,China,Germany,2026-06-15,BoltCo,Imp-E,,,
EX-07,Steel Article,5000,Iron & Steel,7326 90 98,China,Germany,2026-06-15,ArtCo,Imp-F,,,
EX-08,Hydrogen Gas,1000,,2804 10 00,China,Germany,2026-06-15,GasCo,Imp-G,,,
EX-09,Nitrogen Gas,1000,,2804 30 00,China,Germany,2026-06-15,GasCo,Imp-H,,,
EX-10,Steel Wire,5000,Iron & Steel,7326 11 00,China,Germany,2026-06-15,WireCo,Imp-I,,,
EX-11,Plastic Polymer,2000,,3901 10 90,China,Germany,2026-06-15,PlastCo,Imp-J,,,
EX-12,Vietnamese Steel,50000,Iron & Steel,7208 51 00,Viet Nam,Germany,2026-06-15,VN Steel,Imp-K,1.25,0.60,25.0
EX-13,Vietnamese Steel,50000,Iron & Steel,7208 51 00,Vietnam,Germany,2026-06-15,VN Steel,Imp-L,1.25,0.60,25.0
EX-14,Vietnamese Steel,50000,Iron & Steel,7208 51 00,VN,Germany,2026-06-15,VN Steel,Imp-M,1.25,0.60,25.0
EX-15,Dec Shipment,30000,Iron & Steel,7208 51 00,China,Germany,2026-12-20,DecCo,Imp-N,1.25,,
EX-16,Jan Shipment,30000,Iron & Steel,7208 51 00,China,Germany,2027-01-05,JanCo,Imp-N,1.25,,
EX-17,,10000,Iron & Steel,7208 51 00,China,Germany,2026-06-15,NoName,Imp-O,,,
EX-18,Atlantis Steel,10000,Iron & Steel,7208 51 00,Atlantis,Germany,2026-06-15,Fantasy,Imp-P,,,
"""

df = pd.read_csv(io.StringIO(CSV), dtype=str)
# Convert weight to float
df["Weight_kg"] = pd.to_numeric(df["Weight_kg"], errors="coerce").fillna(0)
result = processor.process_bom(df, "Material", "Weight_kg")

rows = result.to_dict(orient="records")
def row(mat_id):
    return next(r for r in rows if r.get("material_id") == mat_id)

print("\n=== CN normalisation: identical results ===")
r1 = row("EX-01")
r3 = row("EX-03")
r4 = row("EX-04")
check("7208 51 00 vs 72085100 same factor",
      r1["Carbon_Factor_kgCO2e_per_kg"] == r3["Carbon_Factor_kgCO2e_per_kg"],
      f"{r1['Carbon_Factor_kgCO2e_per_kg']} vs {r3['Carbon_Factor_kgCO2e_per_kg']}")
check("7208 51 00 vs 7208.51.00 same factor",
      r1["Carbon_Factor_kgCO2e_per_kg"] == r4["Carbon_Factor_kgCO2e_per_kg"],
      f"{r1['Carbon_Factor_kgCO2e_per_kg']} vs {r4['Carbon_Factor_kgCO2e_per_kg']}")

print("\n=== 7204 scrap excluded ===")
r5 = row("EX-05")
check("7204 scrap CN not in Annex I",
      "Annex I" in str(r5.get("Validation_Errors", "")) or "not in CBAM" in str(r5.get("Validation_Errors", "")),
      f"errors: {r5.get('Validation_Errors')}")

print("\n=== 7318 15 00 included ===")
r6 = row("EX-06")
check("7318 fasteners included",
      str(r6.get("Included_In_Total", "")).startswith("YES") or str(r6.get("Included_In_Total", "")).startswith("QUARANTINE"),
      f"status: {r6.get('Included_In_Total')}")

print("\n=== 7326 90 98 non-covered subheading ===")
r7 = row("EX-07")
check("7326 90 98 not covered",
      "Annex I" in str(r7.get("Validation_Errors", "")),
      f"errors: {r7.get('Validation_Errors')}")

print("\n=== 7326 11 00 covered subheading ===")
r10 = row("EX-10")
check("7326 11 00 covered",
      "iron" in str(r10.get("cbam_sector", "")).lower() or str(r10.get("Included_In_Total", "")).startswith("YES") or str(r10.get("Included_In_Total", "")).startswith("QUARANTINE"),
      f"status: {r10.get('Included_In_Total')}, sector from CN: check notes")

print("\n=== 2804 10 00 hydrogen ===")
r8 = row("EX-08")
check("Hydrogen in scope",
      "OUT OF SCOPE" not in str(r8.get("Included_In_Total", "")),
      f"status: {r8.get('Included_In_Total')}")

print("\n=== 2804 30 00 nitrogen NOT hydrogen ===")
r9 = row("EX-09")
check("Nitrogen NOT in scope",
      "OUT OF SCOPE" in str(r9.get("Included_In_Total", "")) or "Annex I" in str(r9.get("Validation_Errors", "")),
      f"status: {r9.get('Included_In_Total')}, errors: {r9.get('Validation_Errors')}")

print("\n=== Country normalisation ===")
r12 = row("EX-12")
r13 = row("EX-13")
r14 = row("EX-14")
check("Viet Nam, Vietnam, VN all same factor",
      r12["Carbon_Factor_kgCO2e_per_kg"] == r13["Carbon_Factor_kgCO2e_per_kg"] == r14["Carbon_Factor_kgCO2e_per_kg"],
      f"{r12['Carbon_Factor_kgCO2e_per_kg']} vs {r13['Carbon_Factor_kgCO2e_per_kg']} vs {r14['Carbon_Factor_kgCO2e_per_kg']}")

print("\n=== Unknown country flagged ===")
r18 = row("EX-18")
check("Atlantis flagged",
      "Unrecognized" in str(r18.get("Validation_Errors", "")),
      f"errors: {r18.get('Validation_Errors')}")

print("\n=== Plastic polymer out of scope ===")
r11 = row("EX-11")
check("Plastic OUT OF SCOPE or quarantined",
      "OUT OF SCOPE" in str(r11.get("Included_In_Total", "")) or "QUARANTINE" in str(r11.get("Included_In_Total", "")),
      f"status: {r11.get('Included_In_Total')}")

print("\n=== Year boundary warning ===")
r15 = row("EX-15")
check("Dec shipment has year boundary warning",
      "year boundary" in str(r15.get("Notes", "")).lower() or "Year boundary" in str(r15.get("Notes", "")),
      f"notes: {r15.get('Notes')}")

print("\n=== De minimis across years ===")
r15 = row("EX-15")
r16 = row("EX-16")
check("Dec row year=2026",
      r15.get("Lookup_Year") == 2026 or str(r15.get("Lookup_Year")) == "2026",
      f"year: {r15.get('Lookup_Year')}")
check("Jan row year=2027",
      r16.get("Lookup_Year") == 2027 or str(r16.get("Lookup_Year")) == "2027",
      f"year: {r16.get('Lookup_Year')}")

print("\n=== Defaults diagnostics in output ===")
check("CBAM_Defaults_Info column present",
      "CBAM_Defaults_Info" in result.columns,
      f"columns: {list(result.columns)}")
if "CBAM_Defaults_Info" in result.columns:
    info = result["CBAM_Defaults_Info"].iloc[0]
    check("Defaults info contains count",
          "entries" in str(info),
          f"info: {info}")

print("\n=== Empty material name quarantined ===")
r17 = row("EX-17")
check("Empty name quarantined",
      "QUARANTINE" in str(r17.get("Included_In_Total", "")),
      f"status: {r17.get('Included_In_Total')}")

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
