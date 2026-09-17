#!/usr/bin/env python3
"""
ingest_nist.py – Import materials from the NIST Alloy Data Web API.

Reference: https://trc.nist.gov/metals_data  (DOI: 10.18434/M32153)
GitHub:    ScottTownsendNIST/NIST-alloy-data-API

Focuses on: density, heat capacity, thermal conductivity for metal alloys.

Usage:
    python scripts/ingest_nist.py               # default 500 materials
    python scripts/ingest_nist.py --limit 0      # all available
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
log = logging.getLogger("ingest_nist")

BATCH_SIZE = 500

# NIST Alloy Data API endpoints
NIST_BASE = "https://trc.nist.gov/metals_data"
NIST_DOI = "10.18434/M32153"

# GitHub-hosted raw data as a fallback
GITHUB_RAW = "https://raw.githubusercontent.com/ScottTownsendNIST/NIST-alloy-data-API/main"

# Alloy systems to query
ALLOY_SYSTEMS = [
    "Fe", "Al", "Ti", "Cu", "Ni", "Cr", "Co",
    "Mn", "W", "Mo", "Zn", "Zr", "Nb",
    "Fe-Cr", "Fe-Ni", "Fe-Cr-Ni", "Al-Cu", "Al-Si",
    "Cu-Zn", "Cu-Sn", "Ti-Al", "Ni-Cr", "Co-Cr",
]


def _safe_float(val):
    if val is None:
        return None
    try:
        f = float(val)
        return f if f == f else None
    except (TypeError, ValueError):
        return None


def _fetch_nist_data(session, system: str):
    """Fetch data for a given alloy system from NIST API."""
    import requests

    urls_to_try = [
        f"{NIST_BASE}/api/alloys?system={system}",
        f"{NIST_BASE}/srd/alloys?system={system}",
        f"{GITHUB_RAW}/data/{system}.json",
    ]

    for url in urls_to_try:
        try:
            resp = session.get(url, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list) and len(data) > 0:
                    return data, url
                if isinstance(data, dict):
                    # Check for nested data arrays
                    for key in ("data", "results", "alloys", "entries"):
                        if key in data and isinstance(data[key], list):
                            return data[key], url
            time.sleep(0.3)
        except Exception:
            continue

    return [], None


def _extract_properties(entry: dict):
    """Extract material properties from a NIST entry dict."""
    props = {}

    # Try common key patterns
    for field, keys in {
        "density": ["density", "Density", "rho", "density_g_cm3"],
        "thermal_conductivity": ["thermal_conductivity", "thermalConductivity", "k", "conductivity_thermal"],
        "specific_heat": ["specific_heat", "heat_capacity", "specificHeat", "cp", "Cp"],
        "melting_point": ["melting_point", "meltingPoint", "Tm", "melting_temperature"],
        "elastic_modulus": ["elastic_modulus", "youngs_modulus", "E", "Young"],
        "poissons_ratio": ["poissons_ratio", "Poisson", "nu"],
        "thermal_expansion_coefficient": ["thermal_expansion", "CTE", "alpha"],
        "electrical_resistivity": ["electrical_resistivity", "resistivity"],
    }.items():
        for k in keys:
            if k in entry and entry[k] is not None:
                val = _safe_float(entry[k])
                if val is not None:
                    props[field] = val
                    break

    return props


def ingest(limit: int):
    import requests

    log.info("=" * 60)
    log.info("NIST Alloy Data Ingestion  (%s)", datetime.now().isoformat())
    log.info("Limit: %s", limit if limit else "ALL")
    log.info("=" * 60)

    db = SessionLocal()
    http = requests.Session()
    http.headers.update({"Accept": "application/json"})

    added = 0
    skipped = 0
    errors = 0

    existing = set(
        db.query(Material.name, Material.grade)
        .filter(Material.source_name == "NIST Alloy Database")
        .all()
    )

    try:
        for system in ALLOY_SYSTEMS:
            if limit and added >= limit:
                break

            log.info("  Querying system '%s' …", system)
            entries, api_url = _fetch_nist_data(http, system)

            if not entries:
                log.info("    No data for '%s'", system)
                continue

            log.info("    Got %d entries", len(entries))

            for entry in entries:
                if limit and added >= limit:
                    break

                try:
                    # Extract name/identifier
                    entry_id = entry.get("id") or entry.get("entry_id") or entry.get("alloy_id")
                    name = entry.get("name") or entry.get("alloy") or entry.get("composition") or f"{system} alloy"
                    name = str(name)[:200]
                    grade = f"nist-{system}-{entry_id}" if entry_id else f"nist-{system}-{added}"

                    if (name, grade) in existing:
                        skipped += 1
                        continue

                    props = _extract_properties(entry)
                    comp = entry.get("composition") or entry.get("chemical_composition") or system
                    source_url = f"{NIST_BASE}/entry/{entry_id}" if entry_id else f"{NIST_BASE}?system={system}"

                    mat = Material(
                        name=name,
                        grade=grade,
                        category="Metal",
                        subcategory=f"{system} Alloy",
                        data_type="experimental",
                        density=props.get("density"),
                        thermal_conductivity=props.get("thermal_conductivity"),
                        specific_heat=props.get("specific_heat"),
                        melting_point_min=props.get("melting_point"),
                        elastic_modulus=props.get("elastic_modulus"),
                        poissons_ratio=props.get("poissons_ratio"),
                        thermal_expansion_coefficient=props.get("thermal_expansion_coefficient"),
                        electrical_resistivity=props.get("electrical_resistivity"),
                        composition=str(comp)[:500],
                        source_name="NIST Alloy Database",
                        source_url=source_url,
                        is_verified=True,
                        verification_count=1,
                        data_quality_score=0.95,  # NIST = gold standard
                        description=f"NIST Standard Reference Data for {system} alloys (DOI: {NIST_DOI})",
                    )

                    db.add(mat)
                    db.flush()

                    src = MaterialSource(
                        material_id=mat.id,
                        source_type="government_db",
                        source_name="NIST Alloy Database",
                        source_url=source_url,
                        source_doi=NIST_DOI,
                        access_type="free",
                        confidence_score=0.95,
                        notes=f"NIST SRD alloy data, system={system}",
                    )
                    db.add(src)

                    existing.add((name, grade))
                    added += 1

                    if added % BATCH_SIZE == 0:
                        db.commit()
                        log.info("    … committed %d", added)

                except Exception as exc:
                    errors += 1
                    if errors <= 5:
                        log.warning("    Entry error: %s", exc)
                    db.rollback()

            time.sleep(0.5)

    except KeyboardInterrupt:
        log.info("Interrupted – committing …")
    finally:
        db.commit()
        db.close()
        http.close()

    log.info("=" * 60)
    log.info("NIST ingestion complete.")
    log.info("  Added:   %d", added)
    log.info("  Skipped: %d  (duplicates)", skipped)
    log.info("  Errors:  %d", errors)
    log.info("=" * 60)
    return added


def main():
    parser = argparse.ArgumentParser(description="Ingest NIST alloy data")
    parser.add_argument("--limit", type=int, default=500,
                        help="Max materials to fetch (0 = all). Default: 500")
    args = parser.parse_args()
    ingest(args.limit)


if __name__ == "__main__":
    main()
