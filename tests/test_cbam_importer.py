"""
Tests for scripts/import_cbam_defaults_2026_1740.py using a small synthetic page shaped like the EUR-Lex tables
(6 columns for Annex I per-country tables, 4 columns for the Annex IV 'highest default values' table).
No database, no network.   Run: pytest tests/test_cbam_importer.py -q   (or python tests/test_cbam_importer.py)
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("importer", os.path.join(os.path.dirname(HERE), "scripts", "import_cbam_defaults_2026_1740.py"))
imp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(imp)


def row6(*c):
    return "<tr>" + "".join(f"<td>{x}</td>" for x in c) + "</tr>"


def country_table(name, steel_total="1,500", fert_total="2,000", steel_cn="7208 51 00", fert_cn="3102 10 10", fert_header=True):
    head = f"<tr><td>{name}</td></tr>" + row6("Product CN Code", "Description", "Direct", "Indirect", "Total", "Route")
    steel = row6("Iron and steel", "", "", "", "", "") + row6(steel_cn, "Flat-rolled", "1,200", "0,300", steel_total, "route")
    fert = (row6("Fertilisers", "", "", "", "", "") if fert_header else "") + row6(fert_cn, "Urea", "1,000", "0,500", fert_total, "route")
    nodata = row6("7208 52 10", "Not published", "-", "-", "-", "-")
    return f"<table>{head}{steel}{nodata}{fert}</table>"


def page(countries=("Viet Nam", "Türkiye"), **kw):
    html = "".join(country_table(c, **kw) for c in countries)
    html += country_table("Other countries and territories", steel_total="2,000")
    html += ("<p>Annex IV: highest default values</p><table>"
             + "<tr><td>Product CN Code</td><td>Description</td><td>Total</td><td>Route</td></tr>"
             + "<tr><td>Cement</td><td></td><td></td><td></td></tr>"
             + "<tr><td>2523 10 00</td><td>Clinker</td><td>1,100</td><td>r</td></tr></table>")
    return f"<html><body>{html}</body></html>"


def test_parse_basic_shape_markups_and_countries():
    recs, stats = imp.parse_annexes(page())
    key = lambda cn, yr, ctry: [r for r in recs if r["cn_prefix"] == cn and r["year"] == yr and r["origin_country"] == ctry]
    steel = key("72085100", 2026, "Viet Nam")[0]
    assert steel["base_value"] == 1.5 and steel["sector"] == "Iron & Steel"
    assert abs(steel["effective_value"] - 1.65) < 1e-9 and steel["markup_pct"] == 0.10
    assert key("72085100", 2027, "Viet Nam")[0]["markup_pct"] == 0.20
    assert key("72085100", 2034, "Viet Nam")[0]["markup_pct"] == 0.30
    fert = key("31021010", 2026, "Türkiye")[0]
    assert fert["sector"] == "Fertilisers" and fert["markup_pct"] == 0.01 and fert["includes_indirect"] is True
    assert key("72085100", 2026, None)[0]["base_value"] == 2.0                # 'Other countries and territories' -> NULL
    clinker = key("25231000", 2026, "UNKNOWN_ORIGIN")[0]
    assert clinker["sector"] == "Cement" and clinker["source"].endswith("(Annex IV)") and clinker["includes_indirect"] is True
    assert not key("72085210", 2026, "Viet Nam")                               # '-' rows are skipped
    assert len(key("72085100", 2026, "Viet Nam") + key("72085100", 2027, "Viet Nam")) == 2
    assert stats["annex_i_tables"] == 3 and stats["annex_iv_tables"] == 1 and stats["rows_without_value"] == 3


def test_parse_direct_for_annex_ii_uses_direct_column():
    recs, _ = imp.parse_annexes(page(), direct_only_annex_ii=True)
    key = lambda cn, yr, ctry: [r for r in recs if r["cn_prefix"] == cn and r["year"] == yr and r["origin_country"] == ctry]
    steel = key("72085100", 2026, "Viet Nam")[0]
    # Direct emissions column is 1.200; total was 1.500
    assert steel["base_value"] == 1.2 and steel["sector"] == "Iron & Steel"
    assert steel["includes_indirect"] is False
    # Fertilisers still take total emissions (2.0)
    fert = key("31021010", 2026, "Türkiye")[0]
    assert fert["base_value"] == 2.0 and fert["sector"] == "Fertilisers"
    assert fert["includes_indirect"] is True


def test_validation_passes_on_clean_data():
    countries = tuple(f"Country{i}" for i in range(16))
    recs, _ = imp.parse_annexes(page(countries))
    errors, warnings = imp.validate(recs, min_rows=1)
    assert errors == [], errors


def test_validation_blocks_wrong_sector_which_would_apply_wrong_markup():
    # a fertiliser CN code that inherited the 'Iron & Steel' label (no header row in its table) must abort the import
    countries = tuple(f"Country{i}" for i in range(16))
    recs, _ = imp.parse_annexes(page(countries, fert_header=False))
    errors, _ = imp.validate(recs, min_rows=1)
    assert any("disagrees with the CN chapter" in e for e in errors), errors


def test_validation_blocks_duplicates_and_tiny_files():
    countries = tuple(f"Country{i}" for i in range(16))
    recs, _ = imp.parse_annexes(page(countries))
    errors, _ = imp.validate(recs + recs[:5], min_rows=1)
    assert any("duplicate" in e for e in errors)
    errors, _ = imp.validate(recs, min_rows=20000)
    assert any("only" in e and "rows parsed" in e for e in errors)
    assert imp.validate([], min_rows=1)[0] == ["no rows parsed"]


def test_parse_float_eu():
    assert imp.parse_float_eu("1,230") == 1.23 and imp.parse_float_eu("-") == 0.0 and imp.parse_float_eu("\xa02,5") == 2.5


def test_summary_reports_indirect_by_sector():
    recs, stats = imp.parse_annexes(page())
    s = imp.summarise(recs, stats)
    assert s["includes_indirect_true_by_sector_2026"]["Iron & Steel"] >= 1   # surfaces the direct-vs-total question
    assert s["global_rows_2026"] == 2 and s["named_countries"] == 2


if __name__ == "__main__":
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1; print("FAIL", name, "->", repr(e))
    print("ALL PASSED" if not failed else f"{failed} FAILED"); sys.exit(1 if failed else 0)
