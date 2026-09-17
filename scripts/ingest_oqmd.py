#!/usr/bin/env python3
"""
ingest_oqmd.py – Import materials from the Open Quantum Materials Database.

Uses the public REST API at http://oqmd.org/oqmdapi/ (no API key required).

Usage:
    python scripts/ingest_oqmd.py                 # default 1000
    python scripts/ingest_oqmd.py --limit 5000
    python scripts/ingest_oqmd.py --limit 0        # fetch all (100 000+)
"""

import os
import sys
import argparse
import logging
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Material, MaterialSource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("ingest_oqmd")

BATCH_SIZE = 500
API_BASE = "http://oqmd.org/oqmdapi/formationenergy"
PAGE_SIZE = 100  # OQMD caps at 100 per page


def _safe_float(val):
    if val is None:
        return None
    try:
        f = float(val)
        return f if f == f else None
    except (TypeError, ValueError):
        return None


def ingest(limit: int):
    import requests

    log.info("=" * 60)
    log.info("OQMD Ingestion  (%s)", datetime.now().isoformat())
    log.info("Limit: %s", limit if limit else "ALL")
    log.info("=" * 60)

    db = SessionLocal()
    added = 0
    skipped = 0
    errors = 0
    offset = 0

    # Pre-load existing entries
    existing = set(
        db.query(Material.name, Material.grade)
        .filter(Material.source_name == "OQMD")
        .all()
    )

    try:
        while True:
            if limit and added >= limit:
                break

            params = {
                "limit": PAGE_SIZE,
                "offset": offset,
                "fields": "name,entry_id,spacegroup,ntypes,band_gap,delta_e,volume_pa,composition_generic",
                "format": "json",
            }

            try:
                resp = requests.get(API_BASE, params=params, timeout=10)
                resp.raise_for_status()
                payload = resp.json()
            except Exception as exc:
                log.error("API error at offset %d: %s", offset, exc)
                errors += 1
                if errors >= 3:
                    log.error("Too many consecutive errors – OQMD might be down. Stopping.")
                    break
                time.sleep(2)
                continue

            data = payload.get("data", [])
            if not data:
                log.info("No more data at offset %d – done.", offset)
                break

            total_available = payload.get("meta", {}).get("total_count")
            if total_available and offset == 0:
                log.info("OQMD reports %s total entries", total_available)

            for entry in data:
                if limit and added >= limit:
                    break

                try:
                    entry_id = entry.get("entry_id")
                    name = entry.get("name") or entry.get("composition_generic") or f"oqmd-{entry_id}"
                    grade = f"oqmd-{entry_id}"

                    if (name, grade) in existing:
                        skipped += 1
                        continue

                    source_url = f"https://oqmd.org/materials/entry/{entry_id}"

                    # Determine category from composition
                    cat = "Computational Material"
                    subcat = None
                    ntypes = entry.get("ntypes")
                    if ntypes and int(ntypes) <= 2:
                        subcat = "Binary Compound"
                    elif ntypes and int(ntypes) == 3:
                        subcat = "Ternary Compound"

                    delta_e = _safe_float(entry.get("delta_e"))
                    band_gap = _safe_float(entry.get("band_gap"))
                    volume = _safe_float(entry.get("volume_pa"))

                    mat = Material(
                        name=name,
                        grade=grade,
                        category=cat,
                        subcategory=subcat,
                        data_type="computational",
                        crystal_structure=str(entry.get("spacegroup", ""))[:50] or None,
                        composition=name,
                        source_name="OQMD",
                        source_url=source_url,
                        is_verified=True,
                        verification_count=1,
                        data_quality_score=0.7,
                        description=(
                            f"OQMD DFT calculation. "
                            f"Formation energy: {delta_e} eV/atom, "
                            f"Band gap: {band_gap} eV, "
                            f"Volume/atom: {volume} Å³"
                        ),
                    )

                    db.add(mat)
                    db.flush()

                    src = MaterialSource(
                        material_id=mat.id,
                        source_type="database_api",
                        source_name="OQMD",
                        source_url=source_url,
                        source_doi="10.1007/s11837-013-0755-4",
                        access_type="free",
                        confidence_score=0.8,
                        notes=f"OQMD REST API, entry_id={entry_id}, spacegroup={entry.get('spacegroup')}",
                    )
                    db.add(src)

                    existing.add((name, grade))
                    added += 1

                    if added % BATCH_SIZE == 0:
                        db.commit()
                        log.info("  … committed %d (skipped %d, errors %d)", added, skipped, errors)

                except Exception as exc:
                    errors += 1
                    if errors <= 5:
                        log.warning("  Entry error (id=%s): %s", entry.get("entry_id"), exc)
                    db.rollback()

            offset += PAGE_SIZE
            time.sleep(1)  # polite rate-limit

    except KeyboardInterrupt:
        log.info("Interrupted – committing current batch …")
    finally:
        db.commit()
        db.close()

    log.info("=" * 60)
    log.info("OQMD ingestion complete.")
    log.info("  Added:   %d", added)
    log.info("  Skipped: %d  (duplicates)", skipped)
    log.info("  Errors:  %d", errors)
    log.info("=" * 60)
    return added


def main():
    parser = argparse.ArgumentParser(description="Ingest OQMD materials data")
    parser.add_argument("--limit", type=int, default=1000,
                        help="Max materials to fetch (0 = all). Default: 1000")
    args = parser.parse_args()
    ingest(args.limit)


if __name__ == "__main__":
    main()
