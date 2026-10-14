"""
Golden tests for the two demo BOMs on /analytics/cbam (the first numbers a prospect sees).

Every expected factor below was checked BY HAND against the text of Commission Implementing Regulation (EU) 2026/1740,
Annex I (which replaces Annex I to Implementing Regulation (EU) 2025/2621), using the EUR-Lex HTML stored in
data/cbam_official/32026R1740.html (sha256 d9b6c633...0f4501, retrieved 2026-10-07). Values are the 'total emissions'
column in tCO2e per tonne of good; the Regulation prints them with a decimal comma.

Rules used, from the introduction to that Annex I:
  * mark-up for cement, iron and steel, aluminium: 10 % in 2026
  * a listed country whose field shows '-' (or no value) takes the 'Other countries and territories' value
Cost = tonnes x total x 1.10 x EUR 75 (CBAM_REFERENCE_PRICE_EUR, an assumption) x 2.5 % (simplified 2026 phase-in).

The demo CSVs are read from the frontend source, so changing a demo row without updating this file fails here.
No database: a FakeDB serves exactly the Regulation rows listed in REG.

Run:  python tests/test_cbam_demo_golden.py     (or pytest)
"""
import datetime
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import sqlalchemy  # noqa: F401
except ImportError:
    import _sandbox_stubs  # noqa: F401

import pandas as pd
from app.models import CBAMDefault
import app.workflows as w
from app.workflows import BOMProcessor

os.environ["CBAM_DEFAULTS_TTL_SECONDS"] = "0"
NOW = datetime.datetime.now(datetime.timezone.utc)
SRC = "Commission Implementing Regulation (EU) 2026/1740 (Annex I)"
PAGE = os.path.join(ROOT, "next-frontend", "src", "app", "analytics", "cbam", "page.tsx")

# (cn_prefix as stored, country or None for 'Other countries and territories', total emissions as printed, indirect?)
REG = [
    ("7208",     "China",   3.187, False),   # China table: 7208 Flat-rolled ... hot-rolled                3,187
    ("7208",     None,      4.049, False),   # Other countries: 7208                                       4,049
    ("7208",     "Türkiye", 2.428, False),   # Türkiye table: 7208 (gives Türkiye a table in the index)    2,428
    ("76042910", "India",   3.413, False),   # India table: 7604 29 10 Bars and rods                       3,413
    ("76042910", None,      3.233, False),   # Other countries: 7604 29 10                                 3,233
    ("731815",   "Taiwan",  2.707, False),   # Taiwan table: 7318 15 Threaded screws and bolts             2,707
    ("731815",   "China",   6.375, False),   # China table: 7318 15                                        6,375
    ("731815",   None,      4.801, False),   # Other countries: 7318 15                                    4,801
    ("25232900", None,      1.440, True),    # Other countries: 2523 29 00 Grey Portland cement  1,360 + 0,080 = 1,440
    #                                          Türkiye table: 2523 29 00 shows '-' in all three columns -> no row
    ("72142000", "China",   3.169, False),   # China table: 7214 20 00 Bars and rods ... deformations       3,169
    ("76101000", "China",   4.896, False),   # China table: 7610 10 00 Doors, windows and their frames      4,896
]

# material_id -> (expected factor incl. 10 % mark-up, expected cost EUR, expected geography, Included_In_Total)
EXPECTED = {
    "MAT-A1": (3.506, 328.66, "COUNTRY", "YES"),      # 50 t, 7208 39 00 China -> 7208 China 3,187
    "MAT-A2": (3.754, 105.59, "COUNTRY", "YES"),      # 15 t, 7604 29 10 India 3,413
    "MAT-A3": (None, 0.0, None, "OUT OF SCOPE"),      # plastic, no CN code
    "MAT-A4": (2.978, 11.17, "COUNTRY", "YES"),       # 2 t, 7318 15 88 Taiwan -> 7318 15 Taiwan 2,707
    "MAT-C1": (1.584, 594.00, "GLOBAL", "YES"),       # 200 t, 2523 29 00 Turkey: Türkiye shows '-' -> Other 1,440
    "MAT-C2": (3.486, 653.61, "COUNTRY", "YES"),      # 100 t, 7214 20 00 China 3,169
    "MAT-C3": (5.386, 100.98, "COUNTRY", "YES"),      # 10 t, 7610 10 00 China 4,896
    "MAT-C4": (7.013, 65.74, "COUNTRY", "YES"),       # 5 t, 7318 15 20 China -> 7318 15 China 6,375 (2.35x Taiwan: real)
    "MAT-C5": (None, 0.0, None, "OUT OF SCOPE"),      # glass, no CN code
}


def _defaults():
    return [CBAMDefault(cn_prefix=cn, year=2026, origin_country=c, base_value=v, markup_pct=0.10,
                        effective_value=round(v * 1.10, 6), includes_indirect=ind, source=SRC, updated_at=NOW)
            for cn, c, v, ind in REG]


class _Q:
    def __init__(self, rows):
        self.rows = rows

    def all(self):
        return list(self.rows)


class FakeDB:
    def query(self, *a):
        return _Q(_defaults() if (a and a[0] is CBAMDefault) else [])


def _demo_csvs():
    src = open(PAGE, encoding="utf-8").read()
    block = src[src.index("const DEMO_BOMS"):]
    return {k: v for k, v in re.findall(r"(\w+):\s*`([^`]*)`", block[:block.index("};") + 2])}


def _run(kind):
    df = pd.read_csv(io.StringIO(_demo_csvs()[kind]), dtype=str)       # same read as the upload route
    return BOMProcessor(FakeDB()).process_bom(df, "Material", "Weight_kg", strict_mode=True)


def _check(out):
    assert out["material_id"].is_unique, list(out["material_id"])
    for _, r in out.iterrows():
        mid = r["material_id"]
        factor, cost, geo, included = EXPECTED[mid]
        assert r["Included_In_Total"] == included, (mid, r["Included_In_Total"])
        assert "Duplicate material ID" not in str(r["Validation_Errors"]), mid
        assert abs(r["CBAM_Cost_EUR"] - cost) < 0.005, (mid, r["CBAM_Cost_EUR"], cost)
        if factor is not None:
            assert abs(r["Carbon_Factor_kgCO2e_per_kg"] - factor) < 0.0006, (mid, r["Carbon_Factor_kgCO2e_per_kg"], factor)
            assert r["Emissions_Basis"] == "COMMISSION_DEFAULT" and r["Default_Geography"] == geo, (mid, r["Default_Geography"])
    assert set(out["material_id"]) <= set(EXPECTED)


def test_demo_csvs_are_the_ones_this_file_was_checked_against():
    csvs = _demo_csvs()
    assert set(csvs) == {"automotive", "construction"}, set(csvs)
    ids = [line.split(",")[0] for k in csvs for line in csvs[k].strip().splitlines()[1:]]
    assert sorted(ids) == sorted(EXPECTED), ids


def test_automotive_demo_matches_the_regulation():
    _check(_run("automotive"))


def test_construction_demo_matches_the_regulation():
    out = _run("construction")
    _check(out)
    assert list(out["Included_In_Total"]).count("OUT OF SCOPE") == 1          # Glass Panes kept as the non-CBAM row


def test_turkiye_dash_falls_back_to_other_countries_and_says_why():
    r = _run("construction").set_index("material_id").loc["MAT-C1"]
    assert r["Default_Geography"] == "GLOBAL"
    assert "has no value for this CN code" in r["Notes"] and "Türkiye" in r["Notes"], r["Notes"]
    assert "check the spelling" not in r["Notes"], r["Notes"]                 # the spelling was fine


def test_country_without_any_table_still_gets_the_spelling_hint():
    df = pd.DataFrame([dict(material_id="X1", Material="coil", Weight_kg="1000", cn_code="7208 39 00",
                            country_of_origin="Brazil", destination="Germany", release_date="2026-06-15",
                            supplier="S", importer="DE1")])
    r = BOMProcessor(FakeDB()).process_bom(df, "Material", "Weight_kg").iloc[0]
    assert r["Default_Geography"] == "GLOBAL" and abs(r["Carbon_Factor_kgCO2e_per_kg"] - 4.454) < 0.0006
    assert "check the spelling" in r["Notes"] and "has no value for this CN code" not in r["Notes"]


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
