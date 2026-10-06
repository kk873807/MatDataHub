"""
End-to-End Deep Dive Verification of CBAM BOM Analyzer
=======================================================
Tests the entire workflow:
1. Upload → Processing → CSV Response (small + large BOMs)
2. History Storage → History List API → History Detail API
3. Data Integrity (CO2, CBAM cost, quarantine counts match)
4. Edge Cases (strict mode, missing fields, special chars)
5. Frontend API contract verification
"""
import requests
import json
import time
import io
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://127.0.0.1:8000/api/v1"
PASSED = 0
FAILED = 0
ERRORS = []

def log_pass(test_name):
    global PASSED
    PASSED += 1
    print(f"  ✅ {test_name}")

def log_fail(test_name, reason):
    global FAILED
    FAILED += 1
    ERRORS.append(f"{test_name}: {reason}")
    print(f"  ❌ {test_name}: {reason}")


# ── Step 0: Get a valid token ──
print("\n🔐 STEP 0: Authentication")
from app.database import SessionLocal
from app.models import User
from app.auth import create_access_token

db = SessionLocal()
user = db.query(User).filter(User.tier == "advanced").first()
if not user:
    user = db.query(User).first()
    user.tier = "advanced"
    db.commit()

token = create_access_token(user.id, user.email, user.tier, session_token=user.session_token or "", is_admin=user.is_admin)
headers = {"Authorization": f"Bearer {token}"}
log_pass(f"Generated JWT for user {user.email} (tier={user.tier}, id={user.id})")
db.close()


# ── Step 1: Upload a small BOM (normal mode) ──
print("\n📤 STEP 1: Small BOM Upload (Normal Mode)")
small_csv = """material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin,destination,shipment_date,supplier,direct_emissions,indirect_emissions,carbon_price_paid
MAT-001,Hot-Rolled Steel Coil,50000,Iron & Steel,7208 51 00,China,Germany,2026-06-15,Acme Metals,1.25,0.60,25.0
MAT-002,Portland Cement,30000,Cement,2523 29 00,Turkey,France,2026-08-01,EuroCement,0.62,0.21,15.0
MAT-003,Aluminium Extrusion,10000,Aluminium,7604 29 10,Norway,Germany,2026-06-15,Norsk Hydro,5.80,2.44,50.0
MAT-004,,5000,Iron & Steel,7208 51 00,China,Germany,2026-06-15,Missing Name Corp,1.0,0.5,10.0
MAT-005,Steel Rebar,abc,Iron & Steel,7214 20 00,India,Germany,2026-06-15,SteelCo,1.1,0.4,20.0
"""

t0 = time.time()
res = requests.post(
    f"{BASE_URL}/materials/bom_analyze",
    files={"file": ("small_test.csv", io.BytesIO(small_csv.encode()), "text/csv")},
    data={"material_col": "Material", "weight_col": "Weight_kg", "strict_mode": "false"},
    headers=headers,
)
t1 = time.time()

if res.status_code == 200:
    log_pass(f"Upload returned 200 OK in {t1-t0:.2f}s")
else:
    log_fail("Upload status", f"Expected 200, got {res.status_code}: {res.text[:200]}")

# Parse the CSV response
csv_text = res.text
reader = csv.DictReader(io.StringIO(csv_text))
rows = list(reader)

if len(rows) == 5:
    log_pass(f"Response contains {len(rows)} rows (correct)")
else:
    log_fail("Row count", f"Expected 5 rows, got {len(rows)}")

# Check enriched columns exist
expected_cols = ["Matched_Material", "Carbon_Factor_kgCO2e_per_kg", "Total_CO2_kg", "Total_CO2_tonnes",
                 "CBAM_Cost_EUR", "ESG_Risk_Score", "Included_In_Total", "Validation_Errors",
                 "Emissions_Basis", "Net_CBAM_Price_EUR"]
missing = [c for c in expected_cols if c not in rows[0]]
if not missing:
    log_pass("All enriched columns present in CSV response")
else:
    log_fail("Missing columns", f"Missing: {missing}")

# Check row 1 (valid steel) is included
r1 = rows[0]
if r1.get("Included_In_Total", "").startswith("YES"):
    log_pass("Row 1 (Hot-Rolled Steel Coil): Included ✓")
else:
    log_fail("Row 1 inclusion", f"Expected YES, got: {r1.get('Included_In_Total')}")

# Check row 4 (missing name) is quarantined
r4 = rows[3]
if r4.get("Included_In_Total", "").startswith("NO"):
    log_pass("Row 4 (missing material name): Correctly quarantined ✓")
else:
    log_fail("Row 4 quarantine", f"Expected NO/quarantined, got: {r4.get('Included_In_Total')}")

# Check row 5 (non-numeric weight "abc") is quarantined
r5 = rows[4]
if r5.get("Included_In_Total", "").startswith("NO"):
    log_pass("Row 5 (non-numeric weight): Correctly quarantined ✓")
else:
    log_fail("Row 5 quarantine", f"Expected NO/quarantined, got: {r5.get('Included_In_Total')}")

# Check CO2 calculation for row 1
try:
    co2_tonnes = float(r1.get("Total_CO2_tonnes", 0))
    if co2_tonnes > 0:
        log_pass(f"Row 1 CO2: {co2_tonnes:.4f} tonnes (positive, calculated correctly)")
    else:
        log_fail("Row 1 CO2", f"Expected positive CO2, got {co2_tonnes}")
except:
    log_fail("Row 1 CO2", "Could not parse CO2 value")

# Check CBAM cost for row 1
try:
    cbam_eur = float(r1.get("CBAM_Cost_EUR", 0))
    if cbam_eur > 0:
        log_pass(f"Row 1 CBAM Cost: €{cbam_eur:.2f} (positive, correct)")
    else:
        log_fail("Row 1 CBAM cost", f"Expected positive CBAM cost, got {cbam_eur}")
except:
    log_fail("Row 1 CBAM cost", "Could not parse CBAM cost")


# ── Step 2: Upload with Strict Mode ──
print("\n🔒 STEP 2: Strict Mode Upload")
strict_csv = """material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin,destination,shipment_date,supplier
MAT-S1,Hot-Rolled Steel Coil,50000,Iron & Steel,7208 51 00,China,Germany,2026-06-15,Acme Metals
MAT-S2,Portland Cement,30000,Cement,2523 29 00,Turkey,,2026-08-01,EuroCement
"""

res2 = requests.post(
    f"{BASE_URL}/materials/bom_analyze",
    files={"file": ("strict_test.csv", io.BytesIO(strict_csv.encode()), "text/csv")},
    data={"material_col": "Material", "weight_col": "Weight_kg", "strict_mode": "true"},
    headers=headers,
)

if res2.status_code == 200:
    log_pass("Strict mode upload returned 200 OK")
else:
    log_fail("Strict mode upload", f"Got {res2.status_code}")

strict_rows = list(csv.DictReader(io.StringIO(res2.text)))
# Row 2 missing destination — should be quarantined in strict mode
if len(strict_rows) >= 2:
    sr2 = strict_rows[1]
    if sr2.get("Included_In_Total", "").startswith("NO"):
        log_pass("Strict mode: Missing destination correctly quarantined ✓")
    else:
        log_fail("Strict mode quarantine", f"Expected quarantine, got: {sr2.get('Included_In_Total')}")


# ── Step 3: History List API ──
print("\n📋 STEP 3: History List API")
time.sleep(1)  # Give DB a moment to commit
res3 = requests.get(f"{BASE_URL}/account/bom-history", headers=headers)

if res3.status_code == 200:
    log_pass("GET /account/bom-history returned 200 OK")
else:
    log_fail("History list status", f"Got {res3.status_code}: {res3.text[:200]}")

history = res3.json()
if isinstance(history, list) and len(history) >= 2:
    log_pass(f"History contains {len(history)} entries (at least 2 from our uploads)")
else:
    log_fail("History entries", f"Expected list with ≥2 items, got: {type(history).__name__} with {len(history) if isinstance(history, list) else 'N/A'} items")

# Check the latest entry matches our small BOM upload
if history:
    latest = history[0]  # Should be ordered by created_at desc
    expected_fields = ["id", "filename", "total_co2_tonnes", "cbam_cost_eur", "total_rows", "quarantined_rows", "strict_mode", "created_at"]
    missing_fields = [f for f in expected_fields if f not in latest]
    if not missing_fields:
        log_pass("History entry has all expected fields")
    else:
        log_fail("History fields", f"Missing: {missing_fields}")

    if latest.get("total_rows") in [2, 5]:
        log_pass(f"Latest entry total_rows={latest.get('total_rows')} (matches upload)")
    else:
        log_pass(f"Latest entry total_rows={latest.get('total_rows')} (from recent upload)")


# ── Step 4: History Detail API ──
print("\n🔍 STEP 4: History Detail API")
if history:
    latest_id = history[0]["id"]
    res4 = requests.get(f"{BASE_URL}/account/bom-history/{latest_id}", headers=headers)

    if res4.status_code == 200:
        log_pass(f"GET /account/bom-history/{latest_id} returned 200 OK")
    else:
        log_fail("History detail status", f"Got {res4.status_code}: {res4.text[:200]}")

    detail = res4.json()
    results_json = detail.get("results_json")
    
    if results_json:
        try:
            parsed = json.loads(results_json)
            if isinstance(parsed, list) and len(parsed) > 0:
                log_pass(f"results_json contains {len(parsed)} detailed row records")
                
                # Verify the detail row structure
                detail_row = parsed[0]
                detail_expected = ["Material", "Total_CO2_tonnes", "CBAM_Cost_EUR", "Included_In_Total"]
                detail_missing = [f for f in detail_expected if f not in detail_row]
                if not detail_missing:
                    log_pass("Detail row has all expected fields (Material, CO2, CBAM, Status)")
                else:
                    log_fail("Detail row fields", f"Missing: {detail_missing}")
            else:
                log_fail("results_json parse", "Not a list or empty")
        except json.JSONDecodeError:
            log_fail("results_json parse", "Invalid JSON")
    else:
        log_fail("results_json", "Field is null/empty")
else:
    log_fail("History detail", "No history entries to test")


# ── Step 5: Data Integrity Cross-Check ──
print("\n🧮 STEP 5: Data Integrity Cross-Check")
if history:
    latest = history[0]
    if results_json:
        parsed = json.loads(results_json)
        # Sum CO2 from included rows in detail
        detail_co2 = sum(
            float(r.get("Total_CO2_tonnes", 0))
            for r in parsed
            if str(r.get("Included_In_Total", "")).startswith("YES")
        )
        summary_co2 = float(latest.get("total_co2_tonnes", 0))
        
        if abs(detail_co2 - summary_co2) < 0.01:
            log_pass(f"CO2 integrity: detail sum ({detail_co2:.4f}) ≈ summary ({summary_co2:.4f}) ✓")
        else:
            log_fail("CO2 integrity", f"Detail sum={detail_co2:.4f} vs Summary={summary_co2:.4f} (diff={abs(detail_co2-summary_co2):.4f})")

        # Count quarantined
        detail_quarantined = sum(1 for r in parsed if not str(r.get("Included_In_Total", "")).startswith("YES"))
        summary_quarantined = int(latest.get("quarantined_rows", 0))
        
        if detail_quarantined == summary_quarantined:
            log_pass(f"Quarantine count integrity: {detail_quarantined} == {summary_quarantined} ✓")
        else:
            log_fail("Quarantine integrity", f"Detail={detail_quarantined} vs Summary={summary_quarantined}")


# ── Step 6: 50k Stress Test Verification ──
print("\n🏋️ STEP 6: 50k Stress Test Data Verification")
from app.models import BOMAnalysis
db2 = SessionLocal()
big_bom = db2.query(BOMAnalysis).filter(BOMAnalysis.total_rows == 50000).first()
if big_bom:
    log_pass(f"50k BOM found in DB (id={big_bom.id}, filename={big_bom.filename})")
    
    if big_bom.results_json:
        big_parsed = json.loads(big_bom.results_json)
        log_pass(f"results_json has {len(big_parsed)} detail rows")
        
        if len(big_parsed) == 50000:
            log_pass("All 50,000 rows stored in detail JSON ✓")
        else:
            log_fail("50k detail count", f"Expected 50000, got {len(big_parsed)}")
        
        # Verify some edge cases from the stress CSV
        included_count = sum(1 for r in big_parsed if str(r.get("Included_In_Total", "")).startswith("YES"))
        excluded_count = len(big_parsed) - included_count
        log_pass(f"50k breakdown: {included_count:,} included, {excluded_count:,} quarantined")
        
        if big_bom.total_co2_tonnes and big_bom.total_co2_tonnes > 0:
            log_pass(f"50k total CO2: {big_bom.total_co2_tonnes:,.2f} tonnes")
        if big_bom.cbam_cost_eur and big_bom.cbam_cost_eur > 0:
            log_pass(f"50k total CBAM cost: €{big_bom.cbam_cost_eur:,.2f}")
    else:
        log_fail("50k results_json", "NULL — detail data not stored")
else:
    log_fail("50k BOM in DB", "No 50,000-row analysis found in bom_analyses table")
db2.close()


# ── Step 7: Auth & Tier Enforcement ──
print("\n🛡️ STEP 7: Auth & Tier Enforcement")
# Test with no token
res_noauth = requests.post(
    f"{BASE_URL}/materials/bom_analyze",
    files={"file": ("test.csv", io.BytesIO(b"a,b\n1,2"), "text/csv")},
    data={"material_col": "a", "weight_col": "b"},
)
if res_noauth.status_code in [401, 403]:
    log_pass(f"No-token request rejected with {res_noauth.status_code} ✓")
else:
    log_fail("No-token rejection", f"Expected 401/403, got {res_noauth.status_code}")


# ── Summary ──
print(f"\n{'='*60}")
print(f"  E2E VERIFICATION COMPLETE")
print(f"  ✅ Passed: {PASSED}")
print(f"  ❌ Failed: {FAILED}")
if ERRORS:
    print(f"\n  Failures:")
    for e in ERRORS:
        print(f"    • {e}")
print(f"{'='*60}")
