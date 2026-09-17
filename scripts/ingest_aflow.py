#!/usr/bin/env python3
"""
ingest_aflow.py – Import materials from the AFLOW database.

Queries binary and ternary alloys for common engineering elements
(Fe, Al, Ti, Cu, Ni, Cr, Co, Mn, W, Mo, Zn) via the aflow Python
package or REST API fallback.

Requirements:
    pip install aflow requests

Usage:
    python scripts/ingest_aflow.py                # default 1000
    python scripts/ingest_aflow.py --limit 5000
    python scripts/ingest_aflow.py --limit 0      # fetch all
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
log = logging.getLogger("ingest_aflow")

BATCH_SIZE = 500
REST_BASE = "http://aflowlib.duke.edu/API/aflux/?"

ELEMENTS = ["Fe", "Al", "Ti", "Cu", "Ni", "Cr", "Co", "Mn", "W", "Mo", "Zn"]


def _safe_float(val):
    if val is None:
        return None
    try:
        f = float(val)
        return f if f == f else None
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Strategy 1: aflow Python package
# ---------------------------------------------------------------------------
def _ingest_via_package(limit: int, db):
    import aflow
    from aflow import K  # keyword descriptors

    added = 0
    skipped = 0
    errors = 0

    existing = set(
        db.query(Material.name, Material.grade)
        .filter(Material.source_name == "AFLOW")
        .all()
    )

    # Build element pairs and triples for common engineering alloys
    element_combos = []
    for i, e1 in enumerate(ELEMENTS):
        for e2 in ELEMENTS[i + 1:]:
            element_combos.append(f"{e1}{e2}")
    # Limit combos for practicality
    element_combos = element_combos[:30]

    for combo in element_combos:
        try:
            log.info("  Querying AFLOW for species containing %s …", combo)
            results = (
                aflow.search(batch_size=100)
                .filter(K.species == combo)
                .select(
                    K.compound, K.auid, K.aurl,
                    K.density, K.enthalpy_formation_atom,
                    K.Bvoigt, K.Gvoigt, K.Pvoigt,
                    K.spacegroup_relax, K.nspecies,
                )
            )

            count = 0
            for entry in results:
                if limit and added >= limit:
                    break

                try:
                    auid = str(getattr(entry, "auid", ""))
                    aurl = str(getattr(entry, "aurl", ""))
                    compound = str(getattr(entry, "compound", "Unknown"))
                    grade = auid or aurl or f"aflow-{combo}-{count}"
                    name = compound

                    if (name, grade) in existing:
                        skipped += 1
                        count += 1
                        continue

                    # Build clickable URL
                    source_url = aurl if aurl.startswith("http") else f"http://aflowlib.duke.edu/search/entry/{auid}"

                    mat = Material(
                        name=name,
                        grade=grade,
                        category="Metal",
                        subcategory="Alloy (Computational)",
                        data_type="computational",
                        density=_safe_float(getattr(entry, "density", None)),
                        elastic_modulus=_safe_float(getattr(entry, "Bvoigt", None)),
                        shear_modulus=_safe_float(getattr(entry, "Gvoigt", None)),
                        poissons_ratio=_safe_float(getattr(entry, "Pvoigt", None)),
                        crystal_structure=str(getattr(entry, "spacegroup_relax", ""))[:50] or None,
                        composition=compound,
                        source_name="AFLOW",
                        source_url=source_url,
                        is_verified=True,
                        verification_count=1,
                        data_quality_score=0.7,
                        description=f"AFLOW computational entry. Enthalpy of formation: {_safe_float(getattr(entry, 'enthalpy_formation_atom', None))} eV/atom",
                    )

                    db.add(mat)
                    db.flush()

                    src = MaterialSource(
                        material_id=mat.id,
                        source_type="database_api",
                        source_name="AFLOW",
                        source_url=source_url,
                        access_type="free",
                        confidence_score=0.8,
                        notes=f"AFLOW REST API, AUID={auid}",
                    )
                    db.add(src)

                    existing.add((name, grade))
                    added += 1
                    count += 1

                    if added % BATCH_SIZE == 0:
                        db.commit()
                        log.info("  … committed %d (skipped %d)", added, skipped)

                except Exception as exc:
                    errors += 1
                    if errors <= 5:
                        log.warning("  Entry error: %s", exc)
                    db.rollback()

            if limit and added >= limit:
                break

        except Exception as exc:
            log.warning("  Query error for %s: %s", combo, exc)
            continue

    db.commit()
    return added, skipped, errors


# ---------------------------------------------------------------------------
# Strategy 2: REST API fallback
# ---------------------------------------------------------------------------
def _ingest_via_rest(limit: int, db):
    import requests

    added = 0
    skipped = 0
    errors = 0
    page_size = 100

    existing = set(
        db.query(Material.name, Material.grade)
        .filter(Material.source_name == "AFLOW")
        .all()
    )

    for el in ELEMENTS:
        if limit and added >= limit:
            break

        paging = 1
        while True:
            if limit and added >= limit:
                break

            url = (
                f"{REST_BASE}"
                f"species({el}*),nspecies(2,3),"
                f"paging({paging},{page_size}),"
                f"$compound,auid,aurl,density,enthalpy_formation_atom,"
                f"Bvoigt,Gvoigt,Pvoigt,spacegroup_relax"
            )

            try:
                resp = requests.get(url, timeout=60)
                resp.raise_for_status()
                data = resp.json()
            except Exception as exc:
                log.warning("  REST error for %s page %d: %s", el, paging, exc)
                break

            if not data:
                break

            for entry in data:
                if limit and added >= limit:
                    break

                try:
                    auid = entry.get("auid", "")
                    aurl = entry.get("aurl", "")
                    compound = entry.get("compound", "Unknown")
                    grade = auid or f"aflow-rest-{el}-{paging}-{added}"
                    name = compound

                    if (name, grade) in existing:
                        skipped += 1
                        continue

                    source_url = aurl if aurl and aurl.startswith("http") else f"http://aflowlib.duke.edu/search/entry/{auid}"

                    mat = Material(
                        name=name,
                        grade=grade,
                        category="Metal",
                        subcategory="Alloy (Computational)",
                        data_type="computational",
                        density=_safe_float(entry.get("density")),
                        elastic_modulus=_safe_float(entry.get("Bvoigt")),
                        shear_modulus=_safe_float(entry.get("Gvoigt")),
                        poissons_ratio=_safe_float(entry.get("Pvoigt")),
                        crystal_structure=str(entry.get("spacegroup_relax", ""))[:50] or None,
                        composition=compound,
                        source_name="AFLOW",
                        source_url=source_url,
                        is_verified=True,
                        verification_count=1,
                        data_quality_score=0.7,
                    )

                    db.add(mat)
                    db.flush()

                    src = MaterialSource(
                        material_id=mat.id,
                        source_type="database_api",
                        source_name="AFLOW",
                        source_url=source_url,
                        access_type="free",
                        confidence_score=0.8,
                        notes=f"AFLOW REST API, AUID={auid}",
                    )
                    db.add(src)

                    existing.add((name, grade))
                    added += 1

                    if added % BATCH_SIZE == 0:
                        db.commit()
                        log.info("  … committed %d", added)

                except Exception as exc:
                    errors += 1
                    if errors <= 5:
                        log.warning("  Entry error: %s", exc)
                    db.rollback()

            if len(data) < page_size:
                break
            paging += 1
            time.sleep(0.5)  # polite rate-limit

    db.commit()
    return added, skipped, errors


def ingest(limit: int):
    log.info("=" * 60)
    log.info("AFLOW Ingestion  (%s)", datetime.now().isoformat())
    log.info("Limit: %s", limit if limit else "ALL")
    log.info("=" * 60)

    db = SessionLocal()

    try:
        # Try the aflow package first
        try:
            import aflow  # noqa: F401
            log.info("Using aflow Python package …")
            added, skipped, errors = _ingest_via_package(limit, db)
        except ImportError:
            log.info("aflow package not found. Falling back to REST API …")
            added, skipped, errors = _ingest_via_rest(limit, db)
    finally:
        db.close()

    log.info("=" * 60)
    log.info("AFLOW ingestion complete.")
    log.info("  Added:   %d", added)
    log.info("  Skipped: %d", skipped)
    log.info("  Errors:  %d", errors)
    log.info("=" * 60)
    return added


def main():
    parser = argparse.ArgumentParser(description="Ingest AFLOW materials data")
    parser.add_argument("--limit", type=int, default=1000,
                        help="Max materials to fetch (0 = all). Default: 1000")
    args = parser.parse_args()
    ingest(args.limit)


if __name__ == "__main__":
    main()
