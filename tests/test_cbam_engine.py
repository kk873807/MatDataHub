"""
Regression tests for the CBAM engine (app/workflows.py :: BOMProcessor).

Each test pins a bug that was reproduced on the production code before it was fixed.
No database is needed: BOMProcessor only calls db.query(...).all(), which FakeDB answers.

Run:  pytest tests/test_cbam_engine.py -q        (or: python tests/test_cbam_engine.py)
"""
import datetime
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import sqlalchemy  # noqa: F401  (real environment)
except ImportError:  # bare sandbox: stand-ins for the DB layer and fuzzy matcher only
    import _sandbox_stubs  # noqa: F401

import pandas as pd
from app.models import CBAMDefault
import app.workflows as w
from app.workflows import BOMProcessor, parse_weight_string, detect_weight_unit

os.environ["CBAM_DEFAULTS_TTL_SECONDS"] = "0"   # tests swap tables constantly: no process cache
NOW = datetime.datetime.now(datetime.timezone.utc)


def D(cn, country, base, year=2026, markup=0.10, source="Commission Implementing Regulation (EU) 2026/1740 (Annex I)"):
    return CBAMDefault(cn_prefix=cn, year=year, origin_country=country, base_value=base, markup_pct=markup,
                       effective_value=round(base * (1 + markup), 6), includes_indirect=False,
                       source=source, updated_at=NOW)


class _Q:
    def __init__(self, rows):
        self.rows = rows

    def all(self):
        return list(self.rows)


class FakeDB:
    def __init__(self, defaults=()):
        self.defaults = list(defaults)

    def query(self, *a):
        return _Q(self.defaults if (a and a[0] is CBAMDefault) else [])


DEFAULTS = [
    D("72085100", None, 2.0),
    D("72085100", "Viet Nam", 1.5),
    D("720851", "Viet Nam", 1.0),
    D("72085100", "Türkiye", 1.2),
    D("2523100090", "Turkmenistan", 1.54),
    D("25231000", None, 0.9),
]

BASE = dict(material_id="M1", name="HRC coil", weight_kg=1000, cn_code="72085100", country_of_origin="Viet Nam",
            destination="Germany", release_date="2026-03-10", supplier_name="S", importer="ACME")


def run(rows, defaults=None, weight_col="weight_kg", delimiter=",", dtype=None, **kw):
    recs = []
    for i, r in enumerate(rows):
        d = dict(BASE)
        d["material_id"] = f"M{i + 1}"
        d.update(r)
        recs.append(d)
    df = pd.DataFrame(recs)
    if dtype is not None:
        df = pd.read_csv(io.StringIO(df.to_csv(index=False)), dtype=dtype)
    p = BOMProcessor(FakeDB(DEFAULTS if defaults is None else defaults))
    return p.process_bom(df, "name", weight_col, delimiter=delimiter, **kw)


def one(rows, **kw):
    return run([rows] if isinstance(rows, dict) else rows, **kw).iloc[0]


# ───────────── sanity: the normal path still works ─────────────
def test_baseline_cost_unchanged():
    r = one({})  # 1000 kg x (1.5 base x 1.10) = 1.65 t ; x 75 EUR x 2.5 % phase-in
    assert r["Carbon_Factor_kgCO2e_per_kg"] == 1.65
    assert abs(r["Total_CO2_tonnes"] - 1.65) < 1e-6
    assert abs(r["CBAM_Cost_EUR"] - 1.65 * 75 * 0.025) < 0.01
    assert r["Included_In_Total"] == "YES"


# ───────────── weight parsing ─────────────
def test_dot_decimal_in_semicolon_file_is_not_x100():
    # was: '2500.75' -> 250075 kg because every dot was deleted
    assert one({"weight_kg": "2500.75"}, delimiter=";")["Parsed_Weight_kg"] == 2500.75


def test_decimal_comma_in_comma_file_is_not_x10():
    # was: '1,5' -> 15 kg and '12,5' -> 125 kg because every comma was deleted
    assert one({"weight_kg": "1,5"})["Parsed_Weight_kg"] == 1.5
    assert one({"weight_kg": "12,5"})["Parsed_Weight_kg"] == 12.5


def test_parse_weight_string_shapes():
    ok = {"2500.75": 2500.75, "1,5": 1.5, "0,500": 0.5, "0.5": 0.5, ".5": 0.5, "1.234,5": 1234.5,
          "1,234.5": 1234.5, "1.234.567": 1234567.0, "1,234,567": 1234567.0, "1 234,5": 1234.5,
          "1000": 1000.0, "1e3": 1000.0, "1234.5678": 1234.5678}
    for text, expected in ok.items():
        value, status = parse_weight_string(text)
        assert (value, status) == (expected, "ok"), (text, value, status)
    for text in ("1.234", "1,234", "12.345"):
        assert parse_weight_string(text)[1] == "ambiguous", text
    for text in ("12abc", "1.2.3", "1,2,3", "", "abc", "1.", ",", "12,34,567"):
        assert parse_weight_string(text)[1] == "invalid", text


def test_ambiguous_weight_is_quarantined_not_charged():
    r = one({"weight_kg": "1.234"}, delimiter=";")
    assert r["Included_In_Total"].startswith("QUARANTINED") and "Ambiguous weight" in r["Included_In_Total"]
    assert r["CBAM_Cost_EUR"] == 0.0


def test_garbage_weight_is_quarantined():
    r = one({"weight_kg": "12abc"})
    assert r["Included_In_Total"].startswith("QUARANTINED") and "Non-numeric" in r["Included_In_Total"]


def test_unit_detection_is_whole_word():
    assert detect_weight_unit("Piston_Weight_kg")[0] == 1.0      # was x1000 ('ton' inside 'Piston')
    assert detect_weight_unit("Carton_Weight")[0] == 1.0         # 'carton' contains 'ton'
    assert detect_weight_unit("Cotton_Weight")[0] == 1.0
    assert detect_weight_unit("Weight_Tonnes")[0] == 1000.0
    assert detect_weight_unit("Weight (t)")[0] == 1000.0
    assert detect_weight_unit("WeightTons")[0] == 1000.0
    assert detect_weight_unit("net_weight_mt")[0] == 1000.0
    assert detect_weight_unit("WeightKg")[0] == 1.0
    assert abs(detect_weight_unit("Net_Weight_lbs")[0] - 0.45359237) < 1e-9
    assert detect_weight_unit("Weight_g")[0] == 0.001
    mult, label = detect_weight_unit("weight")
    assert mult == 1.0 and "assumed" in label


def test_piston_column_end_to_end():
    r = one({"Piston_Weight_kg": 1000}, weight_col="Piston_Weight_kg")
    assert r["Parsed_Weight_kg"] == 1000.0 and "from column name" in r["Weight_Unit_Basis"]


def test_tonnes_column_end_to_end():
    r = one({"weight_tonnes": 2}, weight_col="weight_tonnes")
    assert r["Parsed_Weight_kg"] == 2000.0


# ───────────── dates ─────────────
def test_pre_2026_release_has_no_cost_and_does_not_count_toward_2026_de_minimis():
    # was: note said 'no financial liability' but the row was still charged
    rows = run([{"release_date": "2025-06-15", "weight_kg": 49000}, {"weight_kg": 2000}])
    old, new = rows.iloc[0], rows.iloc[1]
    assert old["CBAM_Cost_EUR"] == 0.0 and old["CBAM_Cost_After_DeMinimis_EUR"] == 0.0
    assert old["Total_CO2_tonnes"] > 0                      # still reported (reporting-only phase)
    assert old["DeMinimis_Eligible_Mass_kg"] == 0.0
    assert new["CBAM_Cost_EUR"] > 0
    assert new["DeMinimis_Status"].startswith("Possibly exempt")   # 49 t of 2025 goods must not push 2026 past 50 t


def test_eu_origin_and_non_eu_destination_are_still_exempt():
    assert one({"country_of_origin": "Germany"})["CBAM_Cost_EUR"] == 0.0
    assert one({"destination": "United States"})["CBAM_Cost_EUR"] == 0.0


# ───────────── default-value lookup ─────────────
def test_country_spelling_variants_hit_the_country_row():
    # table stores 'Viet Nam'; users type 'Vietnam'. was: silently fell back to the global value
    for spelling in ("Viet Nam", "Vietnam", "VIETNAM", "viet-nam"):
        r = one({"country_of_origin": spelling})
        assert r["Default_Geography"] == "COUNTRY" and r["Default_Country_Matched"] == "Viet Nam", spelling
        assert r["Carbon_Factor_kgCO2e_per_kg"] == 1.65, spelling


def test_accents_and_aliases():
    for spelling in ("Türkiye", "Turkiye", "Turkey"):
        r = one({"country_of_origin": spelling})
        assert r["Default_Country_Matched"] == "Türkiye", spelling
        assert r["Carbon_Factor_kgCO2e_per_kg"] == 1.32, spelling


def test_unlisted_country_uses_global_and_says_so():
    r = one({"country_of_origin": "Brazil"})
    assert r["Default_Geography"] == "GLOBAL" and r["Carbon_Factor_kgCO2e_per_kg"] == 2.2
    assert "No country-specific default found" in r["Notes"]


def test_bare_korea_is_not_guessed():
    defaults = [D("72085100", None, 2.0), D("72085100", "Korea, Republic of", 1.0)]
    assert one({"country_of_origin": "Korea"}, defaults=defaults)["Default_Geography"] == "GLOBAL"
    assert one({"country_of_origin": "South Korea"}, defaults=defaults)["Default_Geography"] == "COUNTRY"


def test_lookup_order_is_explicit_and_switchable():
    defaults = [D("72085100", None, 2.0), D("720851", "Viet Nam", 1.0)]
    assert BOMProcessor.DEFAULT_LOOKUP_ORDER == "specificity_first"
    assert one({}, defaults=defaults)["Carbon_Factor_kgCO2e_per_kg"] == 2.2       # global 8-digit beats country 6-digit
    BOMProcessor.DEFAULT_LOOKUP_ORDER = "country_first"
    try:
        assert one({}, defaults=defaults)["Carbon_Factor_kgCO2e_per_kg"] == 1.1   # country-specific row wins
    finally:
        BOMProcessor.DEFAULT_LOOKUP_ORDER = "specificity_first"


def test_defaults_provenance_is_exposed():
    p = BOMProcessor(FakeDB(DEFAULTS))
    assert p.cbam_defaults_sources == ["Commission Implementing Regulation (EU) 2026/1740 (Annex I)"]
    assert "2023/956" in p.annex_version


# ───────────── column matching ─────────────
def test_indirect_column_is_never_read_as_direct():
    # was: 'direct_emissions' is a substring of 'indirect_emissions'
    r = one({"indirect_emissions_tco2e_per_t": 0.4})
    assert r["Emissions_Basis"] == "COMMISSION_DEFAULT"      # no direct figure supplied -> default, not 0.4


def test_direct_value_wins_regardless_of_column_order():
    df = pd.DataFrame([dict(BASE, indirect_emissions_tco2e_per_t=0.4, direct_emissions_tco2e_per_t=1.9)])
    out = BOMProcessor(FakeDB(DEFAULTS)).process_bom(df, "name", "weight_kg").iloc[0]
    assert out["Emissions_Basis"] == "SUPPLIED" and out["Carbon_Factor_kgCO2e_per_kg"] == 1.9


def test_spreadsheet_style_headers_match():
    df = pd.DataFrame([dict(BASE, **{"Direct Emissions (tCO2e/t)": 1.9, "Carbon Price Paid (EUR/tCO2e)": 10})])
    out = BOMProcessor(FakeDB(DEFAULTS)).process_bom(df, "name", "weight_kg").iloc[0]
    assert out["Carbon_Factor_kgCO2e_per_kg"] == 1.9 and out["Domestic_Carbon_Price_Paid_EUR"] == 10.0


def test_purchase_price_column_is_not_a_carbon_price():
    # was: 'price_paid' matched Unit_Price_Paid_EUR and zeroed the CBAM cost
    r = one({"Unit_Price_Paid_EUR": 500.0})
    assert r["Domestic_Carbon_Price_Paid_EUR"] == 0.0 and r["CBAM_Cost_EUR"] > 0


# ───────────── CN code handling ─────────────
def test_float_cn_artifact_is_repaired():
    # pandas turns an int column with one blank into floats: 72085100 -> '72085100.0'
    assert w._clean_cn("72085100.0") == "72085100"
    assert w._clean_cn("7208.51.00") == "72085100"
    assert w._clean_cn("7208 51 00") == "72085100"
    assert w._clean_cn("2523.0") == "2523"


def test_float_four_digit_cn_is_flagged_incomplete_not_silently_out_of_scope():
    # was: '2523.0' -> '25230' -> NOT_COVERED -> 'OUT OF SCOPE' (a cement row silently dropped)
    df = pd.read_csv(io.StringIO("material_id,name,weight_kg,cn_code,country_of_origin,destination,release_date,supplier_name\n"
                                 "M1,cement,1000,2523,Turkmenistan,Germany,2026-03-10,S\n"
                                 "M2,cement,1000,,Turkmenistan,Germany,2026-03-10,S\n"))
    out = BOMProcessor(FakeDB(DEFAULTS)).process_bom(df, "name", "weight_kg")
    assert "Incomplete CN code" in out.iloc[0]["Included_In_Total"]
    assert out.iloc[0]["Included_In_Total"] != "OUT OF SCOPE"


# ───────────── de minimis ─────────────
def test_de_minimis_cost_column_zeroes_exempt_importers_only():
    small = run([{"weight_kg": 3000}, {"weight_kg": 3000}, {"weight_kg": 4000}])
    assert all(small["DeMinimis_Status"].str.startswith("Possibly exempt"))
    assert (small["CBAM_Cost_EUR"] > 0).all()                      # headline = cost if NOT exempt
    assert (small["CBAM_Cost_After_DeMinimis_EUR"] == 0).all()
    big = run([{"weight_kg": 30000}, {"weight_kg": 30000}])        # 60 t
    assert all(big["DeMinimis_Status"].str.startswith("Not exempt"))
    assert (big["CBAM_Cost_After_DeMinimis_EUR"] == big["CBAM_Cost_EUR"]).all()


def test_de_minimis_is_per_importer():
    rows = run([{"weight_kg": 30000, "importer": "A"}, {"weight_kg": 30000, "importer": "B"}])
    assert all(rows["DeMinimis_Status"].str.startswith("Possibly exempt"))


def test_disable_de_minimis_charges_everyone():
    rows = run([{"weight_kg": 3000}], disable_deminimis=True)
    assert rows.iloc[0]["DeMinimis_Status"] == "Disabled by user"
    assert rows.iloc[0]["CBAM_Cost_After_DeMinimis_EUR"] == rows.iloc[0]["CBAM_Cost_EUR"] > 0


# ───────────── the upload route's CSV read (dtype=str) end to end ─────────────
def test_route_style_read_keeps_cn_codes_and_weights_intact():
    csv_text = (
        "material_id;name;weight_kg;cn_code;country_of_origin;destination;release_date;supplier_name\n"
        "M1;coil;2500.75;72085100;Vietnam;Germany;2026-03-10;S\n"
        "M2;coil;1,5;72085100;Vietnam;Germany;2026-03-10;S\n"
        "M3;coil;1.234,5;;Vietnam;Germany;2026-03-10;S\n"          # blank CN must not turn row 1 into floats
    )
    df = pd.read_csv(io.StringIO(csv_text), sep=";", dtype=str)       # exactly what analyze_bom now does
    out = BOMProcessor(FakeDB(DEFAULTS)).process_bom(df, "name", "weight_kg", delimiter=";")
    assert list(out["Parsed_Weight_kg"]) == [2500.75, 1.5, 1234.5]
    assert out.iloc[0]["Default_Match_Digits"] == 8 and out.iloc[0]["Default_Country_Matched"] == "Viet Nam"
    assert out.iloc[2]["Included_In_Total"].startswith("QUARANTINED")  # missing CN code is still flagged


# ───────────── defaults cache ─────────────
def test_defaults_are_cached_between_requests_and_cache_can_be_invalidated():
    class CountingDB(FakeDB):
        loads = 0

        def query(self, *a):
            if a and a[0] is CBAMDefault:
                CountingDB.loads += 1
            return super().query(*a)

    os.environ["CBAM_DEFAULTS_TTL_SECONDS"] = "600"
    w.invalidate_cbam_defaults_cache()
    try:
        BOMProcessor(CountingDB(DEFAULTS))
        BOMProcessor(CountingDB(DEFAULTS))
        assert CountingDB.loads == 1                    # second request reused the process cache
        w.invalidate_cbam_defaults_cache()
        BOMProcessor(CountingDB(DEFAULTS))
        assert CountingDB.loads == 2
        w.invalidate_cbam_defaults_cache()
        BOMProcessor(CountingDB([]))                    # an empty table is never cached
        BOMProcessor(CountingDB([]))
        assert CountingDB.loads == 4
    finally:
        os.environ["CBAM_DEFAULTS_TTL_SECONDS"] = "0"
        w.invalidate_cbam_defaults_cache()


def test_missing_updated_at_does_not_wipe_the_defaults():
    # was: max() of an empty sequence raised, the except-branch cleared the whole cache and every row fell back to estimates
    rows = [D("72085100", None, 2.0)]
    rows[0].updated_at = None
    r = one({}, defaults=rows)
    assert r["Emissions_Basis"] == "COMMISSION_DEFAULT"


# ───────────── taxable CO2 column (drives the UI's what-if years) ─────────────
def test_taxable_co2_follows_the_cost_rules():
    rows = run([{}, {"country_of_origin": "Germany"}, {"release_date": "2025-06-15"}, {"weight_kg": "12abc"}])
    taxable = list(rows["CBAM_Taxable_CO2_tonnes"])
    assert taxable[0] == rows.iloc[0]["Total_CO2_tonnes"] > 0
    assert taxable[1:] == [0.0, 0.0, 0.0]     # EU origin, pre-2026 release, quarantined


if __name__ == "__main__":
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, "->", repr(e))
    print(f"\n{'ALL PASSED' if not failed else str(failed) + ' FAILED'}")
    sys.exit(1 if failed else 0)
