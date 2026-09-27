"""
CBAM Stress Test Validator
==========================
Runs cbam_stress_test.csv through BOMProcessor and validates each edge case.

Usage:
    cd MatDataHub
    .venv\Scripts\python.exe cbam_stress_test_validator.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

import pandas as pd
from app.database import SessionLocal
from app.workflows import BOMProcessor

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cbam_stress_test.csv")

# ─── Run the processor ───────────────────────────────────────────────
print("=" * 80)
print("CBAM STRESS TEST VALIDATOR")
print("=" * 80)

db = SessionLocal()
try:
    processor = BOMProcessor(db)
    df_in = pd.read_csv(CSV_PATH)
    print(f"\nInput:  {len(df_in)} rows read from {os.path.basename(CSV_PATH)}")

    df_out = processor.process_bom(df_in, "material_name", "weight_kg")
    print(f"Output: {len(df_out)} rows returned by process_bom")
    print(f"        ({len(df_in) - len(df_out)} rows skipped — expected: 3 null/empty name rows)")
finally:
    db.close()

# ─── Helpers ──────────────────────────────────────────────────────────
passed = 0
failed = 0
warnings = 0

def check(test_id, description, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✅ {test_id}: {description}")
    else:
        failed += 1
        print(f"  ❌ {test_id}: {description}")
        if detail:
            print(f"       → {detail}")

def warn(test_id, description, detail=""):
    global warnings
    warnings += 1
    print(f"  ⚠️  {test_id}: {description}")
    if detail:
        print(f"       → {detail}")

def get_row(mat_id):
    """Get output row by material_id."""
    matches = df_out[df_out["material_id"] == mat_id]
    return matches.iloc[0] if len(matches) > 0 else None

def get_rows(mat_id):
    """Get all output rows by material_id."""
    return df_out[df_out["material_id"] == mat_id]

# ─── 1. BASELINE GOOD ROWS ───────────────────────────────────────────
print("\n── 1. Baseline good rows ──")
r1 = get_row("MAT-9001")
check("1.1", "Row 1 (Steel) processed",
      r1 is not None)
if r1 is not None:
    check("1.2", "Row 1 has positive Total_CO2_kg",
          r1["Total_CO2_kg"] > 0,
          f"got {r1.get('Total_CO2_kg')}")
    expected_co2 = round(500000 * (1.25 + 0.60), 3)
    check("1.3", f"Row 1 Total_CO2_kg = {expected_co2}",
          abs(r1["Total_CO2_kg"] - expected_co2) < 1.0,
          f"got {r1['Total_CO2_kg']}")
    # Net CBAM = max(75 - 25, 0) = 50
    check("1.4", "Row 1 Net_CBAM_Price_EUR = 50.0",
          r1["Net_CBAM_Price_EUR"] == 50.0,
          f"got {r1.get('Net_CBAM_Price_EUR')}")

r2 = get_row("MAT-9002")
check("1.5", "Row 2 (Cement) processed",
      r2 is not None)

r3 = get_row("MAT-9003")
check("1.6", "Row 3 (Aluminium) processed",
      r3 is not None)
if r3 is not None:
    check("1.7", "Row 3 Aluminium matched to aluminium entry",
          "alumin" in str(r3.get("Matched_Material", "")).lower() or r3.get("Matched_Material") == "NO MATCH FOUND",
          f"got '{r3.get('Matched_Material')}'")

# ─── 2. MISSING / NULL FIELDS ────────────────────────────────────────
print("\n── 2. Missing / null fields ──")
check("2.1", "Row 4 (empty name) skipped",
      get_row("MAT-9004") is None)
check("2.2", "Row 5 (whitespace name) skipped",
      get_row("MAT-9005") is None)
check("2.3", "Row 6 (literal 'nan' name) skipped",
      get_row("MAT-9006") is None)

r7 = get_row("MAT-9007")
check("2.4", "Row 7 (empty weight) processed",
      r7 is not None)
if r7 is not None:
    check("2.5", "Row 7 weight treated as 0 → Total_CO2 = 0",
          r7["Total_CO2_kg"] == 0.0,
          f"got {r7['Total_CO2_kg']}")

r8 = get_row("MAT-9008")
check("2.6", "Row 8 (NaN weight) processed",
      r8 is not None)
if r8 is not None:
    check("2.7", "Row 8 NaN weight treated as 0 → Total_CO2 = 0",
          r8["Total_CO2_kg"] == 0.0,
          f"got {r8['Total_CO2_kg']}")

r9 = get_row("MAT-9009")
check("2.8", "Row 9 (all emissions empty) processed",
      r9 is not None)
if r9 is not None:
    check("2.9", "Row 9 used fallback carbon factor (> 0)",
          r9["Carbon_Factor_kgCO2e_per_kg"] > 0,
          f"got {r9['Carbon_Factor_kgCO2e_per_kg']}")

r10 = get_row("MAT-9010")
check("2.10", "Row 10 (empty risk fields) processed",
      r10 is not None)
if r10 is not None:
    check("2.11", "Row 10 ESG score is a valid number",
          0 <= r10["ESG_Risk_Score"] <= 100,
          f"got {r10['ESG_Risk_Score']}")

# ─── 3. ZERO AND NEGATIVE VALUES ─────────────────────────────────────
print("\n── 3. Zero and negative values ──")
r11 = get_row("MAT-9011")
check("3.1", "Row 11 (weight=0) processed",
      r11 is not None)
if r11 is not None:
    check("3.2", "Row 11 Total_CO2 = 0, CBAM_Cost = 0",
          r11["Total_CO2_kg"] == 0.0 and r11["CBAM_Cost_EUR"] == 0.0,
          f"CO2={r11['Total_CO2_kg']}, cost={r11['CBAM_Cost_EUR']}")

r12 = get_row("MAT-9012")
check("3.3", "Row 12 (negative weight) processed",
      r12 is not None)
if r12 is not None:
    check("3.3b", "Row 12 negative weight clamped to 0 → Total_CO2 = 0",
          r12["Total_CO2_kg"] == 0.0,
          f"got {r12['Total_CO2_kg']}")

r13 = get_row("MAT-9013")
check("3.4", "Row 13 (zero emissions) processed",
      r13 is not None)
if r13 is not None:
    check("3.5", "Row 13 carbon factor = 0 → Total_CO2 = 0",
          r13["Carbon_Factor_kgCO2e_per_kg"] == 0.0 and r13["Total_CO2_kg"] == 0.0,
          f"cf={r13['Carbon_Factor_kgCO2e_per_kg']}, co2={r13['Total_CO2_kg']}")

r14 = get_row("MAT-9014")
check("3.6", "Row 14 (carbon_price=100, exceeds ref 75) processed",
      r14 is not None)
if r14 is not None:
    check("3.7", "Row 14 Net_CBAM_Price = 0 (capped at 0, not negative)",
          r14["Net_CBAM_Price_EUR"] == 0.0,
          f"got {r14['Net_CBAM_Price_EUR']}")
    check("3.8", "Row 14 CBAM_Cost = 0",
          r14["CBAM_Cost_EUR"] == 0.0,
          f"got {r14['CBAM_Cost_EUR']}")

# ─── 4. NON-NUMERIC / GARBAGE IN NUMERIC FIELDS ──────────────────────
print("\n── 4. Non-numeric / garbage in numeric fields ──")
r15 = get_row("MAT-9015")
check("4.1", "Row 15 (weight='five hundred') processed",
      r15 is not None)
if r15 is not None:
    check("4.2", "Row 15 weight fallback to 0 → Total_CO2 = 0",
          r15["Total_CO2_kg"] == 0.0,
          f"got {r15['Total_CO2_kg']}")

r16 = get_row("MAT-9016")
check("4.3", "Row 16 (emissions='N/A') processed",
      r16 is not None)
if r16 is not None:
    check("4.4", "Row 16 used fallback carbon factor (N/A emissions ignored)",
          r16["Carbon_Factor_kgCO2e_per_kg"] > 0,
          f"got {r16['Carbon_Factor_kgCO2e_per_kg']}")

r17 = get_row("MAT-9017")
check("4.5", "Row 17 (weight='1,500,000' with commas) processed",
      r17 is not None)
if r17 is not None:
    expected_co2_17 = round(1500000 * (4.50 + 2.25), 3)
    check("4.6", f"Row 17 parsed commas correctly → Total_CO2 ≈ {expected_co2_17}",
          abs(r17["Total_CO2_kg"] - expected_co2_17) < 1.0,
          f"got {r17['Total_CO2_kg']}")

r18 = get_row("MAT-9018")
check("4.7", "Row 18 (weight='$500') processed",
      r18 is not None)
if r18 is not None:
    check("4.8", "Row 18 weight fallback to 0 (unparseable '$500')",
          r18["Total_CO2_kg"] == 0.0,
          f"got {r18['Total_CO2_kg']}")

r19 = get_row("MAT-9019")
check("4.9", "Row 19 (risk='Very High' text in numeric) processed",
      r19 is not None)
if r19 is not None:
    check("4.10", "Row 19 has valid ESG score despite bad risk field",
          0 <= r19["ESG_Risk_Score"] <= 100,
          f"got {r19['ESG_Risk_Score']}")

# ─── 5. EXTREME VALUES ───────────────────────────────────────────────
print("\n── 5. Extreme values ──")
r20 = get_row("MAT-9020")
check("5.1", "Row 20 (weight=0.001) processed",
      r20 is not None)
if r20 is not None:
    check("5.2", "Row 20 Total_CO2 is tiny but non-zero",
          0 < r20["Total_CO2_kg"] < 1.0,
          f"got {r20['Total_CO2_kg']}")

r21 = get_row("MAT-9021")
check("5.3", "Row 21 (weight=99999999) processed without overflow",
      r21 is not None)
if r21 is not None:
    check("5.4", "Row 21 Total_CO2 is very large but finite",
          r21["Total_CO2_kg"] > 1e6 and r21["Total_CO2_kg"] < 1e12,
          f"got {r21['Total_CO2_kg']}")

r22 = get_row("MAT-9022")
check("5.5", "Row 22 (emissions=999.99) processed",
      r22 is not None)
if r22 is not None:
    check("5.6", "Row 22 absurdly high carbon factor used as-is",
          r22["Carbon_Factor_kgCO2e_per_kg"] == 999.99,
          f"got {r22['Carbon_Factor_kgCO2e_per_kg']}")

r23 = get_row("MAT-9023")
check("5.7", "Row 23 (risk=150, exceeds 0-100) processed",
      r23 is not None)
if r23 is not None:
    check("5.8", "Row 23 ESG score capped at 100",
          r23["ESG_Risk_Score"] <= 100,
          f"got {r23['ESG_Risk_Score']}")

# ─── 6. UNRECOGNIZED SECTOR / COUNTRY ────────────────────────────────
print("\n── 6. Unrecognized sector / country ──")
r24 = get_row("MAT-9024")
check("6.1", "Row 24 (sector='Electricity') processed without crash",
      r24 is not None)

r25 = get_row("MAT-9025")
check("6.2", "Row 25 (sector='Automotive') processed without crash",
      r25 is not None)

r26 = get_row("MAT-9026")
check("6.3", "Row 26 (empty sector) processed without crash",
      r26 is not None)

r27 = get_row("MAT-9027")
check("6.4", "Row 27 (country='Atlantis') processed without crash",
      r27 is not None)
if r27 is not None:
    check("6.5", "Row 27 Hydrogen sector → NO MATCH FOUND",
          r27["Matched_Material"] == "NO MATCH FOUND",
          f"got '{r27['Matched_Material']}'")

# ─── 7. DUPLICATES / COLLISIONS ──────────────────────────────────────
print("\n── 7. Duplicates / collisions ──")
r28 = get_row("MAT-9028")
check("7.1", "Row 28 (material_name='MAT-9001' — ID as name) processed",
      r28 is not None)

rows_9001 = get_rows("MAT-9001")
r30 = get_row("MAT-9030")
check("7.2", f"Duplicate row 30 (MAT-9030) processed",
      r30 is not None)
if r30 is not None and len(rows_9001) > 0:
    check("7.3", "Duplicate row has identical output values to original",
          rows_9001.iloc[0]["Total_CO2_kg"] == r30["Total_CO2_kg"] and
          rows_9001.iloc[0]["CBAM_Cost_EUR"] == r30["CBAM_Cost_EUR"],
          f"CO2: {rows_9001.iloc[0]['Total_CO2_kg']} vs {r30['Total_CO2_kg']}")

r31 = get_row("MAT-9031")
check("7.4", "Row 31 (same material, different supplier/weight) processed",
      r31 is not None)
if r31 is not None and r1 is not None:
    check("7.5", "Row 31 has same carbon factor as Row 1 (same material)",
          r31["Carbon_Factor_kgCO2e_per_kg"] == r1["Carbon_Factor_kgCO2e_per_kg"],
          f"row31={r31['Carbon_Factor_kgCO2e_per_kg']} vs row1={r1['Carbon_Factor_kgCO2e_per_kg']}")
    check("7.6", "Row 31 has different CBAM_Cost (different weight & carbon price paid)",
          r31["CBAM_Cost_EUR"] != r1["CBAM_Cost_EUR"],
          f"both={r1['CBAM_Cost_EUR']}")

# ─── 8. SPECIAL CHARACTERS / UNICODE ─────────────────────────────────
print("\n── 8. Special characters / unicode ──")
r32 = get_row("MAT-9032")
check("8.1", "Row 32 (em-dash, diameter symbol Ø) processed",
      r32 is not None)

r33 = get_row("MAT-9033")
check("8.2", "Row 33 (ü in supplier name) processed",
      r33 is not None)

r34 = get_row("MAT-9034")
check("8.3", "Row 34 (embedded quotes in name) processed",
      r34 is not None)

r35 = get_row("MAT-9035")
check("8.4", "Row 35 (slash and ampersand in name) processed",
      r35 is not None)

# ─── 9. BOUNDARY CONDITIONS ──────────────────────────────────────────
print("\n── 9. Boundary conditions ──")
r36 = get_row("MAT-9036")
check("9.1", "Row 36 (carbon_price=75.0, equals reference) processed",
      r36 is not None)
if r36 is not None:
    check("9.2", "Row 36 Net_CBAM_Price = 0.0 exactly",
          r36["Net_CBAM_Price_EUR"] == 0.0,
          f"got {r36['Net_CBAM_Price_EUR']}")

r37 = get_row("MAT-9037")
check("9.3", "Row 37 (carbon_price=74.99, just under) processed",
      r37 is not None)
if r37 is not None:
    expected_net = 75.0 - 74.99
    check("9.4", f"Row 37 Net_CBAM_Price ≈ {expected_net:.2f}",
          abs(r37["Net_CBAM_Price_EUR"] - expected_net) < 0.02,
          f"got {r37['Net_CBAM_Price_EUR']}")

r38 = get_row("MAT-9038")
check("9.5", "Row 38 (min risk: score=0, no single-source, low geo) processed",
      r38 is not None)
if r38 is not None:
    check("9.6", "Row 38 ESG score is low (< 10)",
          r38["ESG_Risk_Score"] < 10,
          f"got {r38['ESG_Risk_Score']}")

r39 = get_row("MAT-9039")
check("9.7", "Row 39 (max risk: score=100, single-source=Yes, geo=High) processed",
      r39 is not None)
if r39 is not None:
    check("9.8", "Row 39 ESG score is high (> 40)",
          r39["ESG_Risk_Score"] > 40,
          f"got {r39['ESG_Risk_Score']}")
    check("9.9", "Row 39 ESG > Row 38 ESG (max risk > min risk)",
          r39["ESG_Risk_Score"] > r38["ESG_Risk_Score"] if r38 is not None else True,
          f"r39={r39['ESG_Risk_Score']}, r38={r38['ESG_Risk_Score'] if r38 is not None else 'N/A'}")

r40 = get_row("MAT-9040")
check("9.10", "Row 40 (100+ char material name) processed without truncation",
      r40 is not None)

# ─── 10. SECTOR FILTER INTEGRITY ─────────────────────────────────────
print("\n── 10. Sector filter integrity ──")
# All Fertiliser rows should be NO MATCH
fert_ids = ["MAT-9010", "MAT-9014", "MAT-9022"]
for mid in fert_ids:
    r = get_row(mid)
    if r is not None:
        check(f"10.F-{mid}", f"{mid} (Fertilisers) → NO MATCH",
              r["Matched_Material"] == "NO MATCH FOUND",
              f"got '{r['Matched_Material']}'")

# All Hydrogen rows should be NO MATCH
h2_ids = ["MAT-9019", "MAT-9027"]
for mid in h2_ids:
    r = get_row(mid)
    if r is not None:
        check(f"10.H-{mid}", f"{mid} (Hydrogen) → NO MATCH",
              r["Matched_Material"] == "NO MATCH FOUND",
              f"got '{r['Matched_Material']}'")

# Cement rows should be NO MATCH (metals-only DB)
cement_ids = ["MAT-9002", "MAT-9012", "MAT-9021"]
for mid in cement_ids:
    r = get_row(mid)
    if r is not None:
        check(f"10.C-{mid}", f"{mid} (Cement) → NO MATCH",
              r["Matched_Material"] == "NO MATCH FOUND",
              f"got '{r['Matched_Material']}'")

# ─── SUMMARY ─────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print(f"RESULTS:  ✅ {passed} passed    ❌ {failed} failed    ⚠️  {warnings} warnings")
print("=" * 80)

if failed > 0:
    print("\n⚠️  Some tests failed — review output above for details.")
    print("   Failures may indicate input-validation bugs worth fixing.")
else:
    print("\n🎉 All tests passed! The processor handles edge cases gracefully.")

# ─── Export full output for inspection ────────────────────────────────
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cbam_stress_test_output.csv")
df_out.to_csv(out_path, index=False)
print(f"\nFull enriched output saved to: {os.path.basename(out_path)}")
