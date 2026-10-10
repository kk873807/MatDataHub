"""Tests for scripts/diagnose_cbam_defaults.py (pure analysis function; no database).  Run: python tests/test_cbam_diagnose.py"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(HERE), "scripts")
sys.path.insert(0, SCRIPTS)
spec = importlib.util.spec_from_file_location("diag", os.path.join(SCRIPTS, "diagnose_cbam_defaults.py"))
diag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diag)


def R(cn, country, base, year=2026, markup=0.10, sector="Iron & Steel", indirect=False):
    return dict(cn_prefix=cn, year=year, origin_country=country, sector=sector, base_value=base, markup_pct=markup,
                effective_value=base * (1 + markup), includes_indirect=indirect)


def test_clean_table_reports_no_integrity_problems():
    rows = [R("72085100", None, 2.0), R("72085100", "Viet Nam", 1.5), R("31021010", None, 2.0, markup=0.01, sector="Fertilisers")]
    rep = diag.analyse(rows)
    i = rep["integrity"]
    assert not i["sector_vs_cn_chapter_mismatches"] and not i["markup_vs_importer_schedule_mismatches"]
    assert i["effective_value_arithmetic_errors"] == 0 and i["duplicate_keys"] == 0


def test_detects_wrong_sector_markup_arithmetic_and_duplicates():
    rows = [R("31021010", None, 2.0, sector="Iron & Steel"),             # fertiliser labelled steel
            R("72085100", None, 2.0, markup=0.01),                         # steel with the fertiliser mark-up
            dict(R("72085100", "India", 2.0), effective_value=99.0),       # arithmetic broken
            R("72085200", None, 1.0), R("72085200", None, 1.0)]            # duplicate
    i = diag.analyse(rows)["integrity"]
    assert i["sector_vs_cn_chapter_mismatches"][0]["expected"] == "Fertilisers"
    assert i["markup_vs_importer_schedule_mismatches"] and i["effective_value_arithmetic_errors"] == 1 and i["duplicate_keys"] == 1


def test_lookup_order_conflict_is_found():
    rows = [R("72085100", None, 2.0), R("720851", "Viet Nam", 1.0), R("72085100", "India", 1.8)]
    lo = diag.analyse(rows)["lookup_order"]
    assert lo["of_which_values_differ"] == 1                                # Viet Nam only; India has its own 8-digit row
    ex = lo["examples"][0]
    assert ex["country"] == "Viet Nam" and ex["country_row_prefix"] == "720851" and ex["global_row_value"] == 2.2


def test_ten_digit_only_codes_and_indirect_are_listed():
    rows = [R("2523100090", "Turkmenistan", 1.5, sector="Cement", indirect=True), R("25231000", None, 0.9, sector="Cement"),
            R("72085100", "India", 1.5, indirect=True)]
    rep = diag.analyse(rows)
    assert rep["ten_digit"]["eight_digit_codes_with_only_ten_digit_rows_for_some_country"] == 1
    assert rep["indirect"]["rows_with_includes_indirect_true_2026"] == {"Cement": 1, "Iron & Steel": 1}
    assert rep["indirect"]["examples_iron_steel_aluminium"][0]["cn"] == "72085100"


def test_spot_check_is_reproducible_and_probe_uses_resolver():
    rows = [R(f"7208510{i}", None, 1.0 + i) for i in range(10)]
    a, b = diag.analyse(rows, sample_size=4)["spot_check"], diag.analyse(rows, sample_size=4)["spot_check"]
    assert a == b and len(a) == 4
    rep = diag.analyse(rows, resolver=lambda s: ("x", "Viet Nam") if s == "Vietnam" else (None, None))
    assert rep["countries"]["probe"]["Vietnam"] == "Viet Nam" and "no country-specific" in rep["countries"]["probe"]["Brazil"]


if __name__ == "__main__":
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1; print("FAIL", name, "->", repr(e))
    print("ALL PASSED" if not failed else f"{failed} FAILED"); sys.exit(1 if failed else 0)
