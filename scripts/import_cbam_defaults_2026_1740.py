"""
Parse the official EUR-Lex HTML of Commission Implementing Regulation (EU) 2026/1740 and load it into
the cbam_defaults table (Annex I: per-country defaults, Annex IV: highest defaults).

Changes from the first version:
  * Parse and validate EVERYTHING before touching the database. The old script deleted the table, committed,
    then started parsing, so any crash left production with an empty table.
  * Replace the table in ONE transaction (readers keep seeing the old data until the new data is complete).
  * Integrity checks that abort the import: duplicate keys, unknown sector, sector that disagrees with the CN
    chapter (mark-up depends on sector: 1 % fertilisers vs 10/20/30 % others), too few rows, SHA-256 of the HTML not
    matching the provenance file written by fetch_cbam_official.py.
  * --dry-run to parse and print statistics without a database.
  * Bulk insert (about 100k rows) instead of one ORM object per row.

Usage:
    python scripts/import_cbam_defaults_2026_1740.py --dry-run
    python scripts/import_cbam_defaults_2026_1740.py
"""
import argparse
import collections
import datetime
import hashlib
import json
import os
import re
import sys

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_HTML = os.path.join(ROOT, "data", "cbam_official", "32026R1740.html")

# Mark-ups as written in the Regulation text. VERIFY against the Official Journal before relying on them:
# the engine applies them once, here, through effective_value.
MARKUPS = {
    "Fertilisers": {y: 0.01 for y in range(2026, 2035)},
    "default": {2026: 0.10, 2027: 0.20, 2028: 0.30, 2029: 0.30, 2030: 0.30, 2031: 0.30, 2032: 0.30, 2033: 0.30, 2034: 0.30},
}
SECTOR_HEADERS = {"Cement": "Cement", "Iron and steel": "Iron & Steel", "Aluminium": "Aluminium",
                  "Fertilisers": "Fertilisers", "Hydrogen": "Hydrogen"}
SRC_ANNEX_I = "Commission Implementing Regulation (EU) 2026/1740 (Annex I)"
SRC_ANNEX_IV = "Commission Implementing Regulation (EU) 2026/1740 (Annex IV)"


def parse_float_eu(val: str) -> float:
    """Parse EU decimal comma (e.g. '1,230') to float."""
    v = val.strip().replace("\xa0", "")
    if v in ("-", "N/A", "", "see below"):
        return 0.0
    return float(v.replace(",", "."))


def expected_sector(code: str):
    """Sector implied by the CN chapter, used only to cross-check the sector read from the HTML."""
    if code.startswith("25"):
        return "Cement"
    if code.startswith(("72", "73", "26")):
        return "Iron & Steel"
    if code.startswith("76"):
        return "Aluminium"
    if code.startswith("2804"):
        return "Hydrogen"
    if code.startswith(("28", "31")):
        return "Fertilisers"
    return None


def _expand(code, desc, country, base, indirect_included, sector, source):
    schedule = MARKUPS["Fertilisers"] if sector == "Fertilisers" else MARKUPS["default"]
    for year, markup in schedule.items():
        yield {
            "cn_prefix": code, "sector": sector, "product_description": desc, "origin_country": country,
            "year": year, "base_value": base, "markup_pct": markup, "effective_value": base * (1.0 + markup),
            "includes_indirect": indirect_included, "source": source,
        }


def parse_annexes(html: str, direct_only_annex_ii: bool = False):
    """Return (records, stats). Pure function: no database, no network."""
    soup = BeautifulSoup(html, "lxml")
    records = []
    stats = collections.Counter()
    current_sector = "Unknown"

    for t in soup.find_all("table"):
        rows = t.find_all("tr")
        ncols = max((len(r.find_all(["td", "th"])) for r in rows), default=0)

        if ncols == 6:  # Annex I: one table per country (or 'Other countries and territories')
            first = [c.get_text(" ", strip=True) for c in rows[0].find_all(["td", "th"])]
            country = first[0].strip() if len(first) == 1 else ""
            if "Product CN Code" in country or not country:
                continue
            if country.lower() == "other countries and territories":
                country = None  # global fallback
            stats["annex_i_tables"] += 1
            saw_header = False

            for r in rows[1:]:
                cells = [c.get_text(" ", strip=True) for c in r.find_all(["td", "th"])]
                if len(cells) != 6:
                    continue
                cn_raw, desc, direct_str, indirect_str, total_str = (cells[0].strip(), cells[1].strip(),
                                                                     cells[2], cells[3], cells[4])
                if "Product CN Code" in cn_raw:
                    continue
                if not desc and not direct_str and not total_str:
                    if cn_raw in SECTOR_HEADERS:                       # sector header row
                        current_sector = SECTOR_HEADERS[cn_raw]
                        saw_header = True
                    continue
                code = re.sub(r"\D", "", cn_raw)
                if not code:
                    continue
                total_val = parse_float_eu(total_str)
                direct_val = parse_float_eu(direct_str)
                indirect_val = parse_float_eu(indirect_str)

                # Annex II: Goods for which only direct emissions count (Iron & Steel, Aluminium, Hydrogen)
                if direct_only_annex_ii and current_sector in ("Iron & Steel", "Aluminium", "Hydrogen"):
                    val = direct_val if direct_val > 0.0 else total_val
                    has_indirect = False
                else:
                    val = total_val
                    has_indirect = indirect_val > 0

                if val == 0.0:          # '-' = no default value published
                    stats["rows_without_value"] += 1
                    continue
                if not saw_header:
                    stats["rows_with_inherited_sector"] += 1
                records.extend(_expand(code, desc, country, val, has_indirect,
                                       current_sector, SRC_ANNEX_I))

        elif ncols == 4:  # Annex IV: highest default values
            if not t.find_previous(string=re.compile(r"highest default values", re.I)):
                continue
            stats["annex_iv_tables"] += 1
            for r in rows:
                cells = [c.get_text(" ", strip=True) for c in r.find_all(["td", "th"])]
                if len(cells) != 4:
                    continue
                cn_raw, desc, total_str = cells[0].strip(), cells[1].strip(), cells[2]
                if "Product CN Code" in cn_raw:
                    continue
                if not desc and not total_str:
                    if cn_raw in SECTOR_HEADERS:
                        current_sector = SECTOR_HEADERS[cn_raw]
                    continue
                code = re.sub(r"\D", "", cn_raw)
                if not code:
                    continue
                total_val = parse_float_eu(total_str)
                if total_val == 0.0:
                    stats["rows_without_value"] += 1
                    continue
                records.extend(_expand(code, desc, "UNKNOWN_ORIGIN", total_val,
                                       current_sector in ("Cement", "Fertilisers"), current_sector, SRC_ANNEX_IV))
    return records, stats


def validate(records, min_rows=20000):
    """Return (errors, warnings). Any error aborts the import."""
    errors, warnings = [], []
    if not records:
        return ["no rows parsed"], warnings
    if len(records) < min_rows:
        errors.append(f"only {len(records)} rows parsed (< {min_rows}); the HTML is probably truncated or its layout changed "
                      f"(override with --min-rows if this is intentional)")

    keys = collections.Counter((r["cn_prefix"], r["year"], r["origin_country"]) for r in records)
    dups = [k for k, n in keys.items() if n > 1]
    if dups:
        errors.append(f"{len(dups)} duplicate (cn_prefix, year, country) keys, e.g. {dups[:3]}")

    bad_sector = sorted({r["sector"] for r in records} - set(SECTOR_HEADERS.values()))
    if bad_sector:
        errors.append(f"unrecognised sector value(s): {bad_sector}")

    mism = collections.Counter()
    examples = {}
    for r in records:
        if r["year"] != 2026:
            continue
        exp = expected_sector(r["cn_prefix"])
        if exp and exp != r["sector"]:
            k = (r["cn_prefix"][:4], r["sector"], exp)
            mism[k] += 1
            examples.setdefault(k, r["origin_country"])
    if mism:
        errors.append("sector read from the HTML disagrees with the CN chapter (this would apply the wrong mark-up): "
                      + "; ".join(f"{cn}* labelled '{got}' expected '{exp}' ({n} rows, e.g. {examples[(cn, got, exp)]})"
                                  for (cn, got, exp), n in list(mism.items())[:8]))

    countries = {r["origin_country"] for r in records if r["origin_country"] not in (None, "UNKNOWN_ORIGIN")}
    if len(countries) < 15:
        errors.append(f"only {len(countries)} named countries parsed")
    if not any(r["origin_country"] is None for r in records):
        errors.append("no 'Other countries and territories' (global) rows parsed")

    years = {r["year"] for r in records}
    if years != set(range(2026, 2035)):
        errors.append(f"years present: {sorted(years)}")
    odd = [r for r in records if r["year"] == 2026 and not (0 < r["base_value"] <= 60)]
    if odd:
        warnings.append(f"{len(odd)} rows with base_value outside (0, 60] t CO2/t, e.g. {odd[0]['cn_prefix']} {odd[0]['origin_country']} = {odd[0]['base_value']}")
    return errors, warnings


def summarise(records, stats):
    r26 = [r for r in records if r["year"] == 2026]
    by_len = collections.Counter(len(r["cn_prefix"]) for r in r26)
    by_sector = collections.Counter(r["sector"] for r in r26)
    countries = {r["origin_country"] for r in r26 if r["origin_country"] not in (None, "UNKNOWN_ORIGIN")}
    return {
        "rows_total": len(records), "rows_2026": len(r26), "named_countries": len(countries),
        "global_rows_2026": sum(1 for r in r26 if r["origin_country"] is None),
        "unknown_origin_rows_2026": sum(1 for r in r26 if r["origin_country"] == "UNKNOWN_ORIGIN"),
        "by_cn_length_2026": dict(sorted(by_len.items())), "by_sector_2026": dict(by_sector),
        "includes_indirect_true_by_sector_2026": dict(collections.Counter(r["sector"] for r in r26 if r["includes_indirect"])),
        **dict(stats),
    }


def replace_table(records):
    """Delete + bulk insert in a single transaction."""
    sys.path.insert(0, ROOT)
    from app.database import engine, SessionLocal, Base
    from app.models import CBAMDefault
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        before = db.query(CBAMDefault).count()
        db.query(CBAMDefault).delete()
        for i in range(0, len(records), 5000):
            db.bulk_insert_mappings(CBAMDefault, records[i:i + 5000])
        db.commit()
        return before
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default=DEFAULT_HTML)
    ap.add_argument("--dry-run", action="store_true", help="parse + validate, do not touch the database")
    ap.add_argument("--min-rows", type=int, default=20000)
    ap.add_argument("--direct-for-annex-ii", action="store_true", help="use direct emissions column for Annex II sectors (Iron & Steel, Aluminium, Hydrogen)")
    args = ap.parse_args()

    if not os.path.exists(args.html):
        sys.exit(f"File not found: {args.html}. Run fetch_cbam_official.py first.")
    raw = open(args.html, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    prov_path = args.html.replace(".html", ".provenance.json")
    if os.path.exists(prov_path):
        expected = json.load(open(prov_path, encoding="utf-8")).get("sha256")
        if expected and expected != sha:
            sys.exit(f"ABORT: {args.html} (sha256 {sha[:12]}…) is not the file recorded in {os.path.basename(prov_path)} ({expected[:12]}…).")
    else:
        print(f"WARNING: no provenance file next to the HTML; cannot prove which bytes are being imported (sha256 {sha}).")

    print("Parsing HTML…")
    records, stats = parse_annexes(raw.decode("utf-8", errors="replace"), direct_only_annex_ii=args.direct_for_annex_ii)
    summary = summarise(records, stats)
    print(json.dumps(summary, indent=2))
    errors, warnings = validate(records, args.min_rows)
    for w in warnings:
        print("WARNING:", w)
    if errors:
        for e in errors:
            print("ERROR:", e)
        sys.exit("ABORT: validation failed; the database was not modified.")
    if args.dry_run:
        print("Dry run OK; database not modified.")
        return

    before = replace_table(records)
    manifest = {"imported_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "html_sha256": sha,
                "rows_replaced": before, "rows_inserted": len(records), "summary": summary}
    out = args.html.replace(".html", ".import.json")
    json.dump(manifest, open(out, "w", encoding="utf-8"), indent=2)
    print(f"✓ Replaced {before} rows with {len(records)} rows. Manifest: {out}")


if __name__ == "__main__":
    main()
