"""
Comprehensive End-to-End Verification: Gap 3 (DB-Backed CBAM Defaults) & Gap 4 (Strict Compliance Mode)
==================================================================================================
Tests every pathway in the CBAM engine's emission factor resolution and strict mode quarantine logic.
"""

import pandas as pd
import sys
import os
import traceback

# Ensure the project root is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.workflows import BOMProcessor
from app.database import SessionLocal
from app.models import CBAMDefault

PASS = 0
FAIL = 0
ERRORS = []

def check(test_name, condition, detail=""):
    global PASS, FAIL, ERRORS
    if condition:
        PASS += 1
        print(f"  ✓ {test_name}")
    else:
        FAIL += 1
        ERRORS.append(f"{test_name}: {detail}")
        print(f"  ✗ {test_name} — {detail}")


def make_df(**overrides):
    """Build a single-row DataFrame with all required CBAM fields. Override any field."""
    base = {
        'material_id': 'TEST-001',
        'material_name': 'Hot-Rolled Steel Coil',
        'Weight_kg': 10000,
        'cbam_sector': 'Iron & Steel',
        'cn_code': '7208 51 00',
        'direct_emissions': '',          # leave blank to trigger fallback
        'indirect_emissions': '',
        'carbon_price_paid': 0,
        'supplier': 'TestCo',
        'country_of_origin': 'China',
        'destination': 'Germany',
        'shipment_date': '2026-06-15',
        'lead_time_days': 30,
        'single_source_flag': 'No',
        'geopolitical_risk': 'Low',
        'data_quality': 'Default Values',
        'supplier_risk_score': 25,
    }
    base.update(overrides)
    return pd.DataFrame([base])


print("=" * 80)
print("GAP 3: DATABASE-BACKED CBAM DEFAULT VALUES — END-TO-END VERIFICATION")
print("=" * 80)

db = SessionLocal()
processor = BOMProcessor(db)

# ─── Test 1: Verify the cbam_defaults table was seeded ───────────────────
print("\n── Test 1: Database Seeding Verification ──")
total_rows = db.query(CBAMDefault).count()
check("cbam_defaults table has rows", total_rows > 0, f"Found {total_rows} rows (expected 756)")
check("Exact 756 rows seeded (84 CN × 9 years)", total_rows == 756, f"Got {total_rows}")

# Spot-check specific values
steel_2026 = db.query(CBAMDefault).filter(
    CBAMDefault.cn_prefix == "7208",
    CBAMDefault.year == 2026
).first()
check("CN 7208 Steel 2026 exists in DB", steel_2026 is not None)
if steel_2026:
    check("Steel 2026 base_value = 2.01", abs(steel_2026.base_value - 2.01) < 0.001, f"Got {steel_2026.base_value}")
    check("Steel 2026 markup = 10%", abs(steel_2026.markup_pct - 0.10) < 0.001, f"Got {steel_2026.markup_pct}")
    check("Steel 2026 effective_value = 2.211", abs(steel_2026.effective_value - 2.211) < 0.001, f"Got {steel_2026.effective_value}")

hydrogen_2027 = db.query(CBAMDefault).filter(
    CBAMDefault.cn_prefix == "280410",
    CBAMDefault.year == 2027
).first()
check("CN 280410 Hydrogen 2027 exists", hydrogen_2027 is not None)
if hydrogen_2027:
    check("Hydrogen 2027 effective_value = 12.48", abs(hydrogen_2027.effective_value - 12.48) < 0.001, f"Got {hydrogen_2027.effective_value}")
    check("Hydrogen 2027 markup = 20%", abs(hydrogen_2027.markup_pct - 0.20) < 0.001, f"Got {hydrogen_2027.markup_pct}")

cement_2028 = db.query(CBAMDefault).filter(
    CBAMDefault.cn_prefix == "2523",
    CBAMDefault.year == 2028
).first()
check("CN 2523 Cement 2028 exists", cement_2028 is not None)
if cement_2028:
    check("Cement 2028 markup = 30%", abs(cement_2028.markup_pct - 0.30) < 0.001, f"Got {cement_2028.markup_pct}")
    expected = round(0.87 * 1.30, 3)
    check(f"Cement 2028 effective_value = {expected}", abs(cement_2028.effective_value - expected) < 0.01, f"Got {cement_2028.effective_value}")

# Check 2034 also has 30% markup
steel_2034 = db.query(CBAMDefault).filter(
    CBAMDefault.cn_prefix == "7208",
    CBAMDefault.year == 2034
).first()
check("Steel 2034 exists (future year coverage)", steel_2034 is not None)
if steel_2034:
    check("Steel 2034 markup = 30%", abs(steel_2034.markup_pct - 0.30) < 0.001, f"Got {steel_2034.markup_pct}")


# ─── Test 2: Three-Tier Fallback Chain ───────────────────────────────────
print("\n── Test 2: Three-Tier Emissions Fallback Chain ──")

# Tier 1: SUPPLIED (user provides direct_emissions)
df = make_df(direct_emissions=1.5)
res = processor.process_bom(df, 'material_name', 'Weight_kg')
check("Tier 1 SUPPLIED: basis = SUPPLIED", res['Emissions_Basis'].iloc[0] == "SUPPLIED", f"Got {res['Emissions_Basis'].iloc[0]}")
check("Tier 1 SUPPLIED: factor = 1.5", abs(res['Carbon_Factor_kgCO2e_per_kg'].iloc[0] - 1.5) < 0.01, f"Got {res['Carbon_Factor_kgCO2e_per_kg'].iloc[0]}")

# Tier 2: COMMISSION_DEFAULT (no user emissions, valid CN code)
df = make_df(direct_emissions='', cn_code='7208 51 00', shipment_date='2026-06-15')
res = processor.process_bom(df, 'material_name', 'Weight_kg')
check("Tier 2 COMMISSION_DEFAULT: basis", res['Emissions_Basis'].iloc[0] == "COMMISSION_DEFAULT", f"Got {res['Emissions_Basis'].iloc[0]}")
check("Tier 2 COMMISSION_DEFAULT: factor = 2.211 (steel 2026)", abs(res['Carbon_Factor_kgCO2e_per_kg'].iloc[0] - 2.211) < 0.01, f"Got {res['Carbon_Factor_kgCO2e_per_kg'].iloc[0]}")

# Tier 2 with different year: 2027 should give 2.412
df = make_df(direct_emissions='', cn_code='7208 51 00', shipment_date='2027-03-01')
res = processor.process_bom(df, 'material_name', 'Weight_kg')
check("Tier 2 year 2027: factor = 2.412", abs(res['Carbon_Factor_kgCO2e_per_kg'].iloc[0] - 2.412) < 0.01, f"Got {res['Carbon_Factor_kgCO2e_per_kg'].iloc[0]}")

# Tier 2 with 2028 should give 2.613
df = make_df(direct_emissions='', cn_code='7208 51 00', shipment_date='2028-01-15')
res = processor.process_bom(df, 'material_name', 'Weight_kg')
check("Tier 2 year 2028: factor = 2.613 (30% markup)", abs(res['Carbon_Factor_kgCO2e_per_kg'].iloc[0] - 2.613) < 0.01, f"Got {res['Carbon_Factor_kgCO2e_per_kg'].iloc[0]}")

# Tier 3: LEGACY_FALLBACK (no CN code, no user emissions, unrecognized material)
df = make_df(direct_emissions='', cn_code='', material_name='Widget XYZ Unknown')
res = processor.process_bom(df, 'material_name', 'Weight_kg')
basis = res['Emissions_Basis'].iloc[0]
check("Tier 3 LEGACY_FALLBACK: basis", basis in ("DEFAULT_FALLBACK", "LEGACY_FALLBACK"), f"Got {basis}")


# ─── Test 3: Progressive CN Prefix Matching ──────────────────────────────
print("\n── Test 3: Progressive CN Prefix Matching ──")

# Full 8-digit code should still match via prefix shortening
df = make_df(direct_emissions='', cn_code='72085100', shipment_date='2026-06-15')
res = processor.process_bom(df, 'material_name', 'Weight_kg')
check("Full CN 72085100 resolves via prefix 7208", res['Emissions_Basis'].iloc[0] == "COMMISSION_DEFAULT", f"Got {res['Emissions_Basis'].iloc[0]}")

# 6-digit code
df = make_df(direct_emissions='', cn_code='720851', shipment_date='2026-06-15')
res = processor.process_bom(df, 'material_name', 'Weight_kg')
check("6-digit CN 720851 resolves via prefix 7208", res['Emissions_Basis'].iloc[0] == "COMMISSION_DEFAULT", f"Got {res['Emissions_Basis'].iloc[0]}")

# Aluminium 7604 29 10
df = make_df(direct_emissions='', cn_code='7604 29 10', cbam_sector='Aluminium', material_name='Aluminium Extrusion')
res = processor.process_bom(df, 'material_name', 'Weight_kg')
check("Aluminium CN 76042910 resolves", res['Emissions_Basis'].iloc[0] == "COMMISSION_DEFAULT", f"Got {res['Emissions_Basis'].iloc[0]}")

# Hydrogen 280410
df = make_df(direct_emissions='', cn_code='2804 10', cbam_sector='Hydrogen', material_name='Hydrogen Gas', shipment_date='2026-06-15')
res = processor.process_bom(df, 'material_name', 'Weight_kg')
check("Hydrogen CN 280410 resolves", res['Emissions_Basis'].iloc[0] == "COMMISSION_DEFAULT", f"Got {res['Emissions_Basis'].iloc[0]}")
check("Hydrogen 2026 value = 11.44", abs(res['Carbon_Factor_kgCO2e_per_kg'].iloc[0] - 11.44) < 0.01, f"Got {res['Carbon_Factor_kgCO2e_per_kg'].iloc[0]}")


# ─── Test 4: SUPPLIED always takes priority over DB ──────────────────────
print("\n── Test 4: SUPPLIED Priority Over COMMISSION_DEFAULT ──")
df = make_df(direct_emissions=3.5, cn_code='72085100', shipment_date='2026-06-15')
res = processor.process_bom(df, 'material_name', 'Weight_kg')
check("User-supplied emissions override DB default", res['Emissions_Basis'].iloc[0] == "SUPPLIED", f"Got {res['Emissions_Basis'].iloc[0]}")
check("Factor = 3.5 (user value, not 2.211)", abs(res['Carbon_Factor_kgCO2e_per_kg'].iloc[0] - 3.5) < 0.01, f"Got {res['Carbon_Factor_kgCO2e_per_kg'].iloc[0]}")


# ─── Test 5: Financial Calculation Correctness ───────────────────────────
print("\n── Test 5: Financial Calculation Correctness ──")
# 100000 kg steel (100t, > 50t de minimis threshold), CN 7208, 2026, no user emissions, no carbon price paid, China→Germany
df = make_df(
    direct_emissions='', cn_code='7208 51 00', shipment_date='2026-06-15',
    carbon_price_paid=0, Weight_kg=100000,
    country_of_origin='China', destination='Germany'
)
res = processor.process_bom(df, 'material_name', 'Weight_kg')
factor = res['Carbon_Factor_kgCO2e_per_kg'].iloc[0]
total_co2_kg = res['Total_CO2_kg'].iloc[0]
total_co2_t = res['Total_CO2_tonnes'].iloc[0]
cbam_cost = res['CBAM_Cost_EUR'].iloc[0]

expected_co2_kg = 100000 * 2.211
expected_co2_t = expected_co2_kg / 1000.0
expected_cost = round(expected_co2_t * 75.0, 2)  # CBAM ref price = €75/t

check(f"Total CO2 = {expected_co2_kg} kg", abs(total_co2_kg - expected_co2_kg) < 1, f"Got {total_co2_kg}")
check(f"Total CO2 = {expected_co2_t} t", abs(total_co2_t - expected_co2_t) < 0.1, f"Got {total_co2_t}")
check(f"CBAM cost = €{expected_cost}", abs(cbam_cost - expected_cost) < 1, f"Got €{cbam_cost}")

# With carbon price paid = 25
df = make_df(
    direct_emissions='', cn_code='7208 51 00', shipment_date='2026-06-15',
    carbon_price_paid=25, Weight_kg=100000,
    country_of_origin='China', destination='Germany'
)
res = processor.process_bom(df, 'material_name', 'Weight_kg')
cbam_cost_net = res['CBAM_Cost_EUR'].iloc[0]
expected_net = round(expected_co2_t * (75.0 - 25.0), 2)
check(f"Net CBAM cost with €25 offset = €{expected_net}", abs(cbam_cost_net - expected_net) < 1, f"Got €{cbam_cost_net}")


# ─── Test 6: Pre-2026 Shipment → €0 ─────────────────────────────────────
print("\n── Test 6: Pre-2026 Exemption ──")
df = make_df(shipment_date='2025-12-31', direct_emissions=2.0)
res = processor.process_bom(df, 'material_name', 'Weight_kg')
check("Pre-2026 CBAM cost = €0", res['CBAM_Cost_EUR'].iloc[0] == 0.0, f"Got €{res['CBAM_Cost_EUR'].iloc[0]}")
notes = res['Notes'].iloc[0]
check("Pre-2026 note present", "Pre-2026" in str(notes), f"Notes: {notes}")


# ─── Test 7: EU/EEA Origin Exemption ────────────────────────────────────
print("\n── Test 7: EU/EEA Origin Exemption ──")
df = make_df(country_of_origin='Norway', direct_emissions=2.0)
res = processor.process_bom(df, 'material_name', 'Weight_kg')
check("Norway origin: CBAM cost = €0", res['CBAM_Cost_EUR'].iloc[0] == 0.0, f"Got €{res['CBAM_Cost_EUR'].iloc[0]}")
notes = res['Notes'].iloc[0]
check("Norway exempt note", "exempt" in str(notes).lower(), f"Notes: {notes}")


print("\n" + "=" * 80)
print("GAP 4: STRICT COMPLIANCE MODE — END-TO-END VERIFICATION")
print("=" * 80)

# ─── Test 8: Strict Mode Quarantines Missing Fields ─────────────────────
print("\n── Test 8: Strict Mode Hard Quarantine ──")

# A row with all fields filled → should pass in both modes
df_good = make_df(
    direct_emissions=2.0,
    cn_code='7208 51 00',
    country_of_origin='China',
    destination='Germany',
    shipment_date='2026-06-15',
    lead_time_days=30,
    single_source_flag='No',
    geopolitical_risk='Low',
    data_quality='Default Values',
    supplier_risk_score=25,
    supplier='TestCo',
)

res_normal = processor.process_bom(df_good, 'material_name', 'Weight_kg', strict_mode=False)
res_strict = processor.process_bom(df_good, 'material_name', 'Weight_kg', strict_mode=True)
check("Complete row: Normal mode → Included=YES", res_normal['Included_In_Total'].iloc[0].startswith("YES"), f"Got {res_normal['Included_In_Total'].iloc[0]}")
check("Complete row: Strict mode → Included=YES", res_strict['Included_In_Total'].iloc[0].startswith("YES"), f"Got {res_strict['Included_In_Total'].iloc[0]}")

# A row missing CN code → should pass normal, quarantine in strict
df_no_cn = make_df(direct_emissions=2.0, cn_code='', destination='Germany')
res_normal = processor.process_bom(df_no_cn, 'material_name', 'Weight_kg', strict_mode=False)
res_strict = processor.process_bom(df_no_cn, 'material_name', 'Weight_kg', strict_mode=True)
normal_included = res_normal['Included_In_Total'].iloc[0]
strict_included = res_strict['Included_In_Total'].iloc[0]
check("Missing CN: Normal mode → still included", normal_included.startswith("YES"), f"Got {normal_included}")
check("Missing CN: Strict mode → quarantined (NO)", strict_included.startswith("NO"), f"Got {strict_included}")
check("Strict mode reason mentions 'Strict Mode: Missing CN Code'", "Strict Mode: Missing CN Code" in strict_included, f"Got {strict_included}")

# A row missing geopolitical_risk → should pass normal, quarantine in strict
df_no_geo = make_df(direct_emissions=2.0, cn_code='72085100', geopolitical_risk='', destination='Germany')
res_normal = processor.process_bom(df_no_geo, 'material_name', 'Weight_kg', strict_mode=False)
res_strict = processor.process_bom(df_no_geo, 'material_name', 'Weight_kg', strict_mode=True)
check("Missing geo_risk: Normal → included", res_normal['Included_In_Total'].iloc[0].startswith("YES"), f"Got {res_normal['Included_In_Total'].iloc[0]}")
check("Missing geo_risk: Strict → quarantined", res_strict['Included_In_Total'].iloc[0].startswith("NO"), f"Got {res_strict['Included_In_Total'].iloc[0]}")

# A row missing supplier → should warn in both, but only quarantine in strict
df_no_supplier = make_df(direct_emissions=2.0, cn_code='72085100', supplier='', destination='Germany')
res_normal = processor.process_bom(df_no_supplier, 'material_name', 'Weight_kg', strict_mode=False)
res_strict = processor.process_bom(df_no_supplier, 'material_name', 'Weight_kg', strict_mode=True)
check("Missing supplier: Normal → included", res_normal['Included_In_Total'].iloc[0].startswith("YES"), f"Got {res_normal['Included_In_Total'].iloc[0]}")
check("Missing supplier: Strict → quarantined", res_strict['Included_In_Total'].iloc[0].startswith("NO"), f"Got {res_strict['Included_In_Total'].iloc[0]}")


# ─── Test 9: Strict Mode De Minimis Exemption Disabled ───────────────────
print("\n── Test 9: Strict Mode De Minimis Exemption ──")

# Small BOM (1 tonne = 1000 kg), well under 50t threshold
df_small = make_df(
    direct_emissions=2.0,
    cn_code='7208 51 00',
    Weight_kg=1000,
    country_of_origin='China',
    destination='Germany',
    shipment_date='2026-06-15'
)

res_normal = processor.process_bom(df_small, 'material_name', 'Weight_kg', strict_mode=False)
res_strict = processor.process_bom(df_small, 'material_name', 'Weight_kg', strict_mode=True)

normal_cost = res_normal['CBAM_Cost_EUR'].iloc[0]
strict_cost = res_strict['CBAM_Cost_EUR'].iloc[0]
normal_notes = str(res_normal['Notes'].iloc[0])
strict_notes = str(res_strict['Notes'].iloc[0])

check("Normal mode: De minimis applied → CBAM cost = €0", normal_cost == 0.0, f"Got €{normal_cost}")
check("Normal mode: De minimis note present", "De minimis exemption applies" in normal_notes, f"Notes: {normal_notes}")
check("Strict mode: De minimis DISABLED → CBAM cost > €0", strict_cost > 0.0, f"Got €{strict_cost}")
check("Strict mode: Disabled note present", "De minimis exemption disabled" in strict_notes, f"Notes: {strict_notes}")

# Verify the strict mode cost is correct: 1 tonne × 2.0 kgCO2/kg = 2000 kg = 2.0 t → 2.0 × €75 = €150
expected_strict_cost = round(2.0 * 75.0, 2)
check(f"Strict mode cost = €{expected_strict_cost}", abs(strict_cost - expected_strict_cost) < 0.01, f"Got €{strict_cost}")


# ─── Test 10: Strict Mode + Complete Row (No Quarantine) ─────────────────
print("\n── Test 10: Strict Mode With Complete Data ──")

# A perfectly filled row above 50t → should have identical cost in both modes
df_big = make_df(
    direct_emissions=2.0,
    cn_code='7208 51 00',
    Weight_kg=100000,  # 100 tonnes — above de minimis
    country_of_origin='China',
    destination='Germany',
    shipment_date='2026-06-15'
)

res_normal = processor.process_bom(df_big, 'material_name', 'Weight_kg', strict_mode=False)
res_strict = processor.process_bom(df_big, 'material_name', 'Weight_kg', strict_mode=True)

check("Above 50t: Normal mode included", res_normal['Included_In_Total'].iloc[0].startswith("YES"), f"Got {res_normal['Included_In_Total'].iloc[0]}")
check("Above 50t: Strict mode included", res_strict['Included_In_Total'].iloc[0].startswith("YES"), f"Got {res_strict['Included_In_Total'].iloc[0]}")
check("Above 50t: Same cost both modes", abs(res_normal['CBAM_Cost_EUR'].iloc[0] - res_strict['CBAM_Cost_EUR'].iloc[0]) < 0.01, f"Normal={res_normal['CBAM_Cost_EUR'].iloc[0]}, Strict={res_strict['CBAM_Cost_EUR'].iloc[0]}")


# ─── Test 11: Sector-Specific Emission Factors ──────────────────────────
print("\n── Test 11: Sector-Specific Commission Defaults ──")

sectors = [
    ("Iron & Steel", "7208 51 00", "Hot-Rolled Steel Coil", 2.211),
    ("Aluminium", "7601 10 00", "Aluminium Ingot", None),  # check it resolves, value varies
    ("Cement", "2523 29 00", "Portland Cement", None),
    ("Hydrogen", "2804 10 00", "Hydrogen Gas", 11.44),
]

for sector, cn, mat_name, expected_val in sectors:
    df = make_df(
        direct_emissions='', cn_code=cn, cbam_sector=sector,
        material_name=mat_name, shipment_date='2026-06-15',
        country_of_origin='China', destination='Germany'
    )
    res = processor.process_bom(df, 'material_name', 'Weight_kg')
    basis = res['Emissions_Basis'].iloc[0]
    factor = res['Carbon_Factor_kgCO2e_per_kg'].iloc[0]
    check(f"{sector} ({cn[:4]}): resolves to COMMISSION_DEFAULT", basis == "COMMISSION_DEFAULT", f"Got {basis}, factor={factor}")
    if expected_val is not None:
        check(f"{sector} ({cn[:4]}): factor = {expected_val}", abs(factor - expected_val) < 0.01, f"Got {factor}")


# ─── Test 12: API Route strict_mode parameter ───────────────────────────
print("\n── Test 12: API Route Accepts strict_mode ──")
try:
    from app.routers.materials import analyze_bom
    import inspect
    sig = inspect.signature(analyze_bom)
    params = list(sig.parameters.keys())
    check("analyze_bom has 'strict_mode' parameter", 'strict_mode' in params, f"Params: {params}")
    
    # Check default value
    strict_param = sig.parameters.get('strict_mode')
    if strict_param:
        check("strict_mode default = False", "False" in str(strict_param.default), f"Default: {strict_param.default}")
except Exception as e:
    check("API route inspection", False, str(e))


# ─── Test 13: Staleness Warning ──────────────────────────────────────────
print("\n── Test 13: Staleness Detection ──")
check("Defaults not stale (recently seeded)", processor.cbam_defaults_stale == False, f"stale={processor.cbam_defaults_stale}")


# ─── Test 14: Multi-Row BOM with Mixed Tiers ────────────────────────────
print("\n── Test 14: Multi-Row BOM (Mixed Emission Sources) ──")
df_multi = pd.DataFrame([
    {
        'material_id': 'MIX-001', 'material_name': 'Hot-Rolled Steel Coil',
        'Weight_kg': 50000, 'cbam_sector': 'Iron & Steel',
        'cn_code': '7208 51 00', 'direct_emissions': 1.8,  # SUPPLIED
        'indirect_emissions': '', 'carbon_price_paid': 0,
        'supplier': 'A', 'country_of_origin': 'China', 'destination': 'Germany',
        'shipment_date': '2026-06-15', 'lead_time_days': 30,
        'single_source_flag': 'No', 'geopolitical_risk': 'Low',
        'data_quality': 'Verified', 'supplier_risk_score': 20, 'carbon_price_paid': 10
    },
    {
        'material_id': 'MIX-002', 'material_name': 'Steel Wire Rod',
        'Weight_kg': 30000, 'cbam_sector': 'Iron & Steel',
        'cn_code': '7213 91 10', 'direct_emissions': '',  # COMMISSION_DEFAULT
        'indirect_emissions': '', 'carbon_price_paid': 0,
        'supplier': 'B', 'country_of_origin': 'India', 'destination': 'France',
        'shipment_date': '2026-08-01', 'lead_time_days': 45,
        'single_source_flag': 'No', 'geopolitical_risk': 'Medium',
        'data_quality': 'Estimated', 'supplier_risk_score': 40
    },
    {
        'material_id': 'MIX-003', 'material_name': 'Widget Unknown',
        'Weight_kg': 5000, 'cbam_sector': '',
        'cn_code': '', 'direct_emissions': '',  # LEGACY_FALLBACK
        'indirect_emissions': '', 'carbon_price_paid': 0,
        'supplier': 'C', 'country_of_origin': 'USA', 'destination': 'Germany',
        'shipment_date': '2026-09-01', 'lead_time_days': 10,
        'single_source_flag': 'Yes', 'geopolitical_risk': 'Low',
        'data_quality': 'Default Values', 'supplier_risk_score': 15
    },
])

res = processor.process_bom(df_multi, 'material_name', 'Weight_kg')
bases = res['Emissions_Basis'].tolist()
check("Multi-row: Row 1 = SUPPLIED", bases[0] == "SUPPLIED", f"Got {bases[0]}")
check("Multi-row: Row 2 = COMMISSION_DEFAULT", bases[1] == "COMMISSION_DEFAULT", f"Got {bases[1]}")
# Row 3 has no CN code and unknown material — should be LEGACY_FALLBACK or DEFAULT_FALLBACK
check("Multi-row: Row 3 = fallback tier", bases[2] in ("DEFAULT_FALLBACK", "LEGACY_FALLBACK"), f"Got {bases[2]}")

# Verify financial totals add up
included_costs = [r for i, r in res.iterrows() if str(r.get('Included_In_Total', '')).startswith('YES')]
total_cbam = sum(r['CBAM_Cost_EUR'] for _, r in res.iterrows())
check("Multi-row: Total CBAM cost > 0", total_cbam > 0, f"Got €{total_cbam}")


# ─── Test 15: Strict Mode on Multi-Row (partial quarantine) ──────────────
print("\n── Test 15: Strict Mode Multi-Row Partial Quarantine ──")
df_mixed_quality = pd.DataFrame([
    {   # Complete row — should pass strict mode
        'material_id': 'SM-001', 'material_name': 'Hot-Rolled Steel Coil',
        'Weight_kg': 100000, 'cbam_sector': 'Iron & Steel',
        'cn_code': '7208 51 00', 'direct_emissions': 2.0,
        'indirect_emissions': '', 'carbon_price_paid': 0,
        'supplier': 'GoodCo', 'country_of_origin': 'China', 'destination': 'Germany',
        'shipment_date': '2026-06-15', 'lead_time_days': 30,
        'single_source_flag': 'No', 'geopolitical_risk': 'Low',
        'data_quality': 'Verified', 'supplier_risk_score': 20
    },
    {   # Missing CN code — should quarantine in strict, pass in normal
        'material_id': 'SM-002', 'material_name': 'Steel Thing',
        'Weight_kg': 50000, 'cbam_sector': 'Iron & Steel',
        'cn_code': '', 'direct_emissions': 2.0,
        'indirect_emissions': '', 'carbon_price_paid': 0,
        'supplier': 'OkCo', 'country_of_origin': 'China', 'destination': 'Germany',
        'shipment_date': '2026-06-15', 'lead_time_days': 30,
        'single_source_flag': 'No', 'geopolitical_risk': 'Low',
        'data_quality': 'Default Values', 'supplier_risk_score': 20
    },
])

res_normal = processor.process_bom(df_mixed_quality, 'material_name', 'Weight_kg', strict_mode=False)
res_strict = processor.process_bom(df_mixed_quality, 'material_name', 'Weight_kg', strict_mode=True)

# Normal: both rows included
normal_included = [str(r) for r in res_normal['Included_In_Total'].tolist()]
check("Normal: Row 1 included", normal_included[0].startswith("YES"), f"Got {normal_included[0]}")
check("Normal: Row 2 included (missing CN is warning only)", normal_included[1].startswith("YES"), f"Got {normal_included[1]}")

# Strict: Row 1 included, Row 2 quarantined
strict_included = [str(r) for r in res_strict['Included_In_Total'].tolist()]
check("Strict: Row 1 still included", strict_included[0].startswith("YES"), f"Got {strict_included[0]}")
check("Strict: Row 2 quarantined", strict_included[1].startswith("NO"), f"Got {strict_included[1]}")

# Strict total should be lower (only 1 row contributes)
normal_total = res_normal['CBAM_Cost_EUR'].sum()
strict_total = res_strict['CBAM_Cost_EUR'].sum()
check("Strict total < Normal total (1 row quarantined)", strict_total < normal_total, f"Normal=€{normal_total}, Strict=€{strict_total}")


# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print(f"RESULTS: {PASS} passed, {FAIL} failed out of {PASS + FAIL} tests")
print("=" * 80)

if ERRORS:
    print("\nFAILED TESTS:")
    for e in ERRORS:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("\n🎉 ALL TESTS PASSED — Gap 3 and Gap 4 are verified end-to-end!")
    sys.exit(0)
