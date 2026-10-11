"""
Read-only health check of the cbam_defaults table. It never writes.

    python scripts/diagnose_cbam_defaults.py                # prints a report
    python scripts/diagnose_cbam_defaults.py --json out.json

Sections
  1. Shape            rows per sector / geography / CN length
  2. Integrity        sector vs CN chapter, mark-up vs sector, effective_value arithmetic, duplicate keys
  3. Lookup order     where "longest CN prefix wins" and "country row wins" give DIFFERENT numbers
  4. Country names    every spelling in the table + whether common user spellings resolve to one
  5. Indirect         rows whose value includes indirect emissions, by sector
  6. Ten-digit codes  8-digit CN codes that only exist as 10-digit rows for some country
  7. Spot-check       a reproducible sample to compare by hand against the Official Journal

Sections 3, 5 and 6 are questions only the Regulation text can answer; this script finds the rows where the
answer matters so they can be checked, it does not decide them.
"""
import argparse
import collections
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PROBE_SPELLINGS = [
    "Vietnam", "Viet Nam", "Turkey", "Türkiye", "Russia", "Russian Federation", "South Korea", "Republic of Korea",
    "USA", "United States", "United States of America", "UK", "United Kingdom", "China", "People's Republic of China",
    "UAE", "United Arab Emirates", "India", "Egypt", "Ukraine", "Brazil", "South Africa", "Mexico", "Taiwan", "Japan",
    "Indonesia", "Malaysia", "Thailand", "Saudi Arabia", "Serbia", "Bosnia and Herzegovina", "North Macedonia",
    "Kazakhstan", "Laos", "Iran", "Moldova", "Congo", "Ivory Coast", "Eswatini", "Myanmar",
]


def _expected_sector(code):
    from import_cbam_defaults_2026_1740 import expected_sector
    return expected_sector(code)


def _markups():
    from import_cbam_defaults_2026_1740 import MARKUPS
    return MARKUPS


def analyse(rows, resolver=None, sample_size=25, seed=2026):
    """rows: list of dicts with cn_prefix, year, origin_country, sector, base_value, markup_pct, effective_value, includes_indirect."""
    out = {}
    r26 = [r for r in rows if r["year"] == 2026]

    # 1 shape
    out["shape"] = {
        "rows_total": len(rows), "rows_2026": len(r26),
        "by_sector": dict(collections.Counter(r["sector"] for r in r26)),
        "by_geography": {"global (NULL)": sum(1 for r in r26 if r["origin_country"] is None),
                         "UNKNOWN_ORIGIN (Annex IV)": sum(1 for r in r26 if r["origin_country"] == "UNKNOWN_ORIGIN"),
                         "named country": sum(1 for r in r26 if r["origin_country"] not in (None, "UNKNOWN_ORIGIN"))},
        "by_cn_length": dict(sorted(collections.Counter(len(r["cn_prefix"]) for r in r26).items())),
        "years": sorted({r["year"] for r in rows}),
    }

    # 2 integrity
    mk = _markups()
    sector_mismatch, markup_mismatch, arithmetic, dup = collections.Counter(), collections.Counter(), [], []
    seen = collections.Counter()
    for r in rows:
        seen[(r["cn_prefix"], r["year"], r["origin_country"])] += 1
        exp = _expected_sector(r["cn_prefix"])
        if exp and exp != r["sector"] and r["year"] == 2026:
            sector_mismatch[(r["cn_prefix"][:4], r["sector"], exp)] += 1
        sched = mk["Fertilisers"] if r["sector"] == "Fertilisers" else mk["default"]
        if r["year"] in sched and abs((r["markup_pct"] or 0) - sched[r["year"]]) > 1e-9:
            markup_mismatch[(r["sector"], r["year"], r["markup_pct"])] += 1
        if abs(r["effective_value"] - r["base_value"] * (1 + (r["markup_pct"] or 0))) > 1e-6:
            arithmetic.append((r["cn_prefix"], r["origin_country"], r["year"]))
    dup = [k for k, n in seen.items() if n > 1]
    out["integrity"] = {
        "sector_vs_cn_chapter_mismatches": [{"cn_prefix": k[0], "labelled": k[1], "expected": k[2], "rows": n}
                                            for k, n in sector_mismatch.most_common(20)],
        "markup_vs_importer_schedule_mismatches": [{"sector": k[0], "year": k[1], "markup_in_db": k[2], "rows": n}
                                                   for k, n in markup_mismatch.most_common(20)],
        "effective_value_arithmetic_errors": len(arithmetic), "arithmetic_examples": arithmetic[:5],
        "duplicate_keys": len(dup), "duplicate_examples": dup[:5],
    }

    # 3 lookup order
    by_country = collections.defaultdict(dict)       # country -> {cn_prefix: base_value}   (2026)
    glob = {}
    for r in r26:
        if r["origin_country"] is None:
            glob[r["cn_prefix"]] = r["effective_value"]
        elif r["origin_country"] != "UNKNOWN_ORIGIN":
            by_country[r["origin_country"]][r["cn_prefix"]] = r["effective_value"]
    pairs = []
    for g, gval in glob.items():
        if len(g) < 8:
            continue
        for country, table in by_country.items():
            if any(g[:n] in table for n in range(len(g), 7, -1)):   # country has its own row at 8+ digits -> no conflict
                continue
            for n in range(7, 1, -1):
                p = g[:n]
                if p in table:
                    pairs.append((g, country, p, gval, table[p]))
                    break
    differing = [p for p in pairs if abs(p[3] - p[4]) > 1e-9]
    out["lookup_order"] = {
        "pairs_where_a_shorter_country_row_exists_but_a_longer_global_row_exists": len(pairs),
        "of_which_values_differ": len(differing),
        "examples": [{"cn": p[0], "country": p[1], "country_row_prefix": p[2], "global_row_value": round(p[3], 4),
                      "country_row_value": round(p[4], 4)} for p in sorted(differing, key=lambda x: -abs(x[3] - x[4]))[:10]],
        "note": "Current engine (specificity_first) returns the global value; country_first returns the country value.",
    }

    # 4 country names
    names = sorted({r["origin_country"] for r in rows if r["origin_country"] not in (None, "UNKNOWN_ORIGIN")})
    probe = {}
    if resolver:
        for s in PROBE_SPELLINGS:
            key, stored = resolver(s)
            probe[s] = stored or "-- no country-specific table (global values would be used)"
    out["countries"] = {"count": len(names), "names": names, "probe": probe}

    # 5 indirect
    ind = collections.defaultdict(list)
    for r in r26:
        if r["includes_indirect"]:
            ind[r["sector"]].append(r)
    out["indirect"] = {
        "rows_with_includes_indirect_true_2026": {k: len(v) for k, v in ind.items()},
        "examples_iron_steel_aluminium": [
            {"cn": r["cn_prefix"], "country": r["origin_country"], "base_value_total": r["base_value"]}
            for s in ("Iron & Steel", "Aluminium") for r in ind.get(s, [])[:3]],
        "note": "base_value is the TOTAL (direct+indirect) column. If direct-only applies to a sector in the definitive "
                "period, those rows overstate the default; check the Regulation and tell me which sectors count indirect.",
    }

    # 6 ten-digit
    ten = collections.defaultdict(set)
    have8 = {(r["cn_prefix"], r["origin_country"]) for r in r26 if len(r["cn_prefix"]) == 8}
    for r in r26:
        if len(r["cn_prefix"]) == 10 and (r["cn_prefix"][:8], r["origin_country"]) not in have8:
            ten[r["cn_prefix"][:8]].add(r["origin_country"])
    out["ten_digit"] = {
        "eight_digit_codes_with_only_ten_digit_rows_for_some_country": len(ten),
        "examples": {k: sorted(map(str, v))[:5] for k, v in list(ten.items())[:8]},
        "note": "A user typing the 8-digit code gets the global value for these countries (the 10-digit rows are never reached).",
    }

    # 7 spot-check sample
    rng = random.Random(seed)
    sample = rng.sample(r26, min(sample_size, len(r26))) if r26 else []
    out["spot_check"] = [{"cn_prefix": r["cn_prefix"], "country": r["origin_country"] or "(other countries)", "sector": r["sector"],
                          "base_value_total": r["base_value"], "markup_2026": r["markup_pct"], "effective_2026": round(r["effective_value"], 4)}
                         for r in sample]
    return out


def render(rep):
    def h(t):
        print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)
    h("1. SHAPE"); print(json.dumps(rep["shape"], indent=1, ensure_ascii=False))
    h("2. INTEGRITY (all of these should be empty / 0)"); print(json.dumps(rep["integrity"], indent=1, ensure_ascii=False))
    h("3. LOOKUP ORDER (rows where the choice changes the number)"); print(json.dumps(rep["lookup_order"], indent=1, ensure_ascii=False))
    h("4. COUNTRY NAMES"); c = rep["countries"]
    print(f"{c['count']} named countries in the table:\n  " + "; ".join(c["names"]))
    if c["probe"]:
        print("\nHow common user spellings resolve:")
        for k, v in c["probe"].items():
            print(f"  {k:32s} -> {v}")
    h("5. INDIRECT EMISSIONS IN base_value"); print(json.dumps(rep["indirect"], indent=1, ensure_ascii=False))
    h("6. TEN-DIGIT CODES"); print(json.dumps(rep["ten_digit"], indent=1, ensure_ascii=False))
    h("7. SPOT-CHECK SAMPLE (compare each line with the Official Journal table for that country)")
    for s in rep["spot_check"]:
        print(f"  {s['cn_prefix']:>10}  {s['country']:<28} {s['sector']:<13} total={s['base_value_total']:<8} markup={s['markup_2026']}  effective={s['effective_2026']}")


def load_rows_from_db():
    from app.database import SessionLocal
    from app.models import CBAMDefault
    db = SessionLocal()
    try:
        return [{"cn_prefix": d.cn_prefix, "year": d.year, "origin_country": d.origin_country, "sector": d.sector,
                 "base_value": d.base_value, "markup_pct": d.markup_pct, "effective_value": d.effective_value,
                 "includes_indirect": bool(d.includes_indirect)} for d in db.query(CBAMDefault).all()]
    finally:
        db.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="also write the full report to this file")
    args = ap.parse_args()
    rows = load_rows_from_db()
    resolver = None
    try:
        from app.workflows import BOMProcessor, _norm_country, _COUNTRY_GROUP
        countries = {}
        for r in rows:
            if r["origin_country"] and r["origin_country"] != "UNKNOWN_ORIGIN":
                countries.setdefault(_norm_country(r["origin_country"]), r["origin_country"])

        def resolver(name):
            n = _norm_country(name)
            for cand in [n] + sorted(_COUNTRY_GROUP.get(n, frozenset()) - {n}):
                if cand in countries:
                    return cand, countries[cand]
            return None, None
    except Exception as e:  # noqa: BLE001
        print("(country probe skipped:", e, ")")
    rep = analyse(rows, resolver)
    render(rep)
    if args.json:
        json.dump(rep, open(args.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("\nFull report written to", args.json)


if __name__ == "__main__":
    main()
