#!/usr/bin/env python3
"""
ingest_github_datasets.py – Download and import open-source material datasets
hosted on GitHub.

Repositories:
    • KittyCAD/material-properties          (JSON)
    • CitrineInformatics/MPEA_dataset       (CSV – Multi-Principal Element Alloys)
    • ElenaNKn/mechanical-properties        (CSV – low-alloy steels)
    • batiukmaks/Steel-Strength-Prediction  (CSV – steel strengths)

Requirements:
    pip install requests pandas

Usage:
    python scripts/ingest_github_datasets.py
    python scripts/ingest_github_datasets.py --repos kittycad citrine
"""

import os
import sys
import argparse
import logging
import json
from datetime import datetime
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Material, MaterialSource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("ingest_github")

BATCH_SIZE = 500
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "github")


def _safe_float(val):
    if val is None:
        return None
    try:
        f = float(val)
        return f if f == f else None
    except (TypeError, ValueError):
        return None


def _download(url: str, dest: str):
    """Download a file if it doesn't already exist."""
    import requests

    if os.path.exists(dest):
        return True
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            f.write(resp.content)
        log.info("    Downloaded → %s", dest)
        return True
    except Exception as exc:
        log.error("    Download failed (%s): %s", url, exc)
        return False


# ============================= KittyCAD ====================================
def ingest_kittycad(db):
    """KittyCAD/material-properties – JSON format."""
    repo_url = "https://github.com/KittyCAD/material-properties"
    raw_base = "https://raw.githubusercontent.com/KittyCAD/material-properties/main"

    # They store one JSON per material in data/ or materials/
    index_urls = [
        f"{raw_base}/data/materials.json",
        f"{raw_base}/materials.json",
        f"{raw_base}/index.json",
    ]

    import requests

    src_label = "GitHub: KittyCAD/material-properties"
    existing = set(
        db.query(Material.name, Material.grade)
        .filter(Material.source_name == src_label)
        .all()
    )

    added = 0
    errors = 0

    # Try to get the index or list of files
    data = None
    for url in index_urls:
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                break
        except Exception:
            continue

    if data is None:
        # Fallback: try the GitHub API to list repo contents
        try:
            api_url = "https://api.github.com/repos/KittyCAD/material-properties/contents/data"
            resp = requests.get(api_url, timeout=30)
            if resp.status_code == 200:
                files = resp.json()
                data = []
                for f in files:
                    if f.get("name", "").endswith(".json"):
                        try:
                            r = requests.get(f["download_url"], timeout=30)
                            if r.status_code == 200:
                                entry = r.json()
                                if isinstance(entry, dict):
                                    data.append(entry)
                                elif isinstance(entry, list):
                                    data.extend(entry)
                        except Exception:
                            continue
        except Exception as exc:
            log.warning("  KittyCAD GitHub API fallback failed: %s", exc)

    if not data:
        log.warning("  Could not fetch KittyCAD data – skipping")
        return 0

    materials_list = data if isinstance(data, list) else [data]

    for item in materials_list:
        try:
            name = item.get("name") or item.get("material") or "Unknown"
            name = str(name)[:200]
            grade = f"kittycad-{name}"

            if (name, grade) in existing:
                continue

            mat = Material(
                name=name,
                grade=grade,
                category=item.get("category", "Metal"),
                subcategory=item.get("subcategory"),
                data_type="experimental",
                density=_safe_float(item.get("density")),
                tensile_strength_min=_safe_float(item.get("tensile_strength") or item.get("ultimate_tensile_strength")),
                yield_strength_min=_safe_float(item.get("yield_strength")),
                elastic_modulus=_safe_float(item.get("elastic_modulus") or item.get("youngs_modulus")),
                poissons_ratio=_safe_float(item.get("poissons_ratio")),
                thermal_conductivity=_safe_float(item.get("thermal_conductivity")),
                specific_heat=_safe_float(item.get("specific_heat")),
                melting_point_min=_safe_float(item.get("melting_point")),
                composition=str(item.get("composition", ""))[:500] or None,
                source_name=src_label,
                source_url=repo_url,
                is_verified=True,
                verification_count=1,
                data_quality_score=0.7,
            )

            db.add(mat)
            db.flush()

            src = MaterialSource(
                material_id=mat.id,
                source_type="datasheet",
                source_name=src_label,
                source_url=repo_url,
                access_type="free",
                confidence_score=0.7,
                notes="Open-source material property database from KittyCAD",
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
                log.warning("  KittyCAD entry error: %s", exc)
            db.rollback()

    db.commit()
    log.info("  [OK] KittyCAD done – added %d, errors %d", added, errors)
    return added


# ============================ Citrine MPEA ==================================
def ingest_citrine(db):
    """CitrineInformatics/MPEA_dataset – Multi-Principal Element Alloys (CSV)."""
    import pandas as pd

    repo_url = "https://github.com/CitrineInformatics/MPEA_dataset"
    csv_url = "https://raw.githubusercontent.com/CitrineInformatics/MPEA_dataset/master/mpea_dataset.csv"
    local_path = os.path.join(DATA_DIR, "citrine_mpea.csv")

    if not _download(csv_url, local_path):
        # Try alternative paths
        alt_url = "https://raw.githubusercontent.com/CitrineInformatics/MPEA_dataset/main/mpea_dataset.csv"
        if not _download(alt_url, local_path):
            return 0

    src_label = "GitHub: CitrineInformatics/MPEA_dataset"
    existing = set(
        db.query(Material.name, Material.grade)
        .filter(Material.source_name == src_label)
        .all()
    )

    try:
        df = pd.read_csv(local_path, low_memory=False)
    except Exception as exc:
        log.error("  Failed to read Citrine CSV: %s", exc)
        return 0

    added = 0
    errors = 0

    for idx, row in df.iterrows():
        try:
            name = str(row.get("formula") or row.get("composition") or row.get("Alloy") or f"MPEA-{idx}")[:200]
            grade = f"citrine-mpea-{idx}"

            if (name, grade) in existing:
                continue

            mat = Material(
                name=name,
                grade=grade,
                category="Metal",
                subcategory="High Entropy Alloy",
                data_type="experimental",
                density=_safe_float(row.get("density")),
                tensile_strength_min=_safe_float(row.get("UTS") or row.get("tensile_strength")),
                yield_strength_min=_safe_float(row.get("YS") or row.get("yield_strength")),
                elongation=_safe_float(row.get("elongation") or row.get("Elongation")),
                hardness=str(row.get("hardness"))[:50] if "hardness" in row.index else None,
                elastic_modulus=_safe_float(row.get("E") or row.get("elastic_modulus")),
                composition=name,
                source_name=src_label,
                source_url=repo_url,
                is_verified=True,
                verification_count=1,
                data_quality_score=0.75,
            )

            db.add(mat)
            db.flush()

            src = MaterialSource(
                material_id=mat.id,
                source_type="research_paper",
                source_name=src_label,
                source_url=repo_url,
                access_type="free",
                confidence_score=0.75,
                notes="Citrine Informatics Multi-Principal Element Alloys dataset",
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
                log.warning("  Citrine row %d error: %s", idx, exc)
            db.rollback()

    db.commit()
    log.info("  [OK] Citrine MPEA done – added %d, errors %d", added, errors)
    return added


# =========================== ElenaNKn steels ================================
def ingest_elena(db):
    """ElenaNKn/mechanical-properties – low-alloy steels."""
    import pandas as pd

    repo_url = "https://github.com/ElenaNKn/mechanical-properties"
    csv_url = "https://raw.githubusercontent.com/ElenaNKn/mechanical-properties/master/data.csv"
    local_path = os.path.join(DATA_DIR, "elena_steels.csv")

    if not _download(csv_url, local_path):
        alt_url = "https://raw.githubusercontent.com/ElenaNKn/mechanical-properties/main/data.csv"
        if not _download(alt_url, local_path):
            return 0

    src_label = "GitHub: ElenaNKn/mechanical-properties"
    existing = set(
        db.query(Material.name, Material.grade)
        .filter(Material.source_name == src_label)
        .all()
    )

    try:
        df = pd.read_csv(local_path, low_memory=False)
    except Exception as exc:
        log.error("  Failed to read Elena CSV: %s", exc)
        return 0

    added = 0
    errors = 0

    for idx, row in df.iterrows():
        try:
            name = f"Low-Alloy Steel #{idx}"
            grade = f"elena-steel-{idx}"

            if (name, grade) in existing:
                continue

            # Build composition string from element columns
            el_cols = [c for c in df.columns if len(c) <= 3 and c[0].isupper()]
            comp_parts = []
            for c in el_cols:
                val = _safe_float(row.get(c))
                if val and val > 0:
                    comp_parts.append(f"{c}:{val}")
            comp = ", ".join(comp_parts) if comp_parts else None

            mat = Material(
                name=name,
                grade=grade,
                category="Metal",
                subcategory="Low-Alloy Steel",
                data_type="experimental",
                tensile_strength_min=_safe_float(row.get("Tensile strength") or row.get("UTS")),
                yield_strength_min=_safe_float(row.get("Yield strength") or row.get("YS")),
                elongation=_safe_float(row.get("Elongation")),
                hardness=str(row.get("Brinell hardness"))[:50] if "Brinell hardness" in row.index else None,
                impact_strength=_safe_float(row.get("Charpy impact energy")),
                composition=comp,
                source_name=src_label,
                source_url=repo_url,
                is_verified=True,
                verification_count=1,
                data_quality_score=0.7,
            )

            db.add(mat)
            db.flush()

            src = MaterialSource(
                material_id=mat.id,
                source_type="research_paper",
                source_name=src_label,
                source_url=repo_url,
                access_type="free",
                confidence_score=0.7,
                notes="Low-alloy steel mechanical properties from NIMS",
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
                log.warning("  Elena row %d error: %s", idx, exc)
            db.rollback()

    db.commit()
    log.info("  [OK] Elena steels done – added %d, errors %d", added, errors)
    return added


# ========================= batiukmaks steel =================================
def ingest_batiukmaks(db):
    """batiukmaks/Steel-Strength-Prediction – CSV."""
    import pandas as pd

    repo_url = "https://github.com/batiukmaks/Steel-Strength-Prediction"
    csv_url = "https://raw.githubusercontent.com/batiukmaks/Steel-Strength-Prediction/main/data/steel.csv"
    local_path = os.path.join(DATA_DIR, "batiukmaks_steel.csv")

    if not _download(csv_url, local_path):
        alt_url = "https://raw.githubusercontent.com/batiukmaks/Steel-Strength-Prediction/master/data/steel.csv"
        if not _download(alt_url, local_path):
            return 0

    src_label = "GitHub: batiukmaks/Steel-Strength-Prediction"
    existing = set(
        db.query(Material.name, Material.grade)
        .filter(Material.source_name == src_label)
        .all()
    )

    try:
        df = pd.read_csv(local_path, low_memory=False)
    except Exception as exc:
        log.error("  Failed to read batiukmaks CSV: %s", exc)
        return 0

    added = 0
    errors = 0

    for idx, row in df.iterrows():
        try:
            name = str(row.get("Steel") or row.get("Name") or f"Steel #{idx}")[:200]
            grade = f"batiukmaks-steel-{idx}"

            if (name, grade) in existing:
                continue

            mat = Material(
                name=name,
                grade=grade,
                category="Metal",
                subcategory="Steel",
                data_type="experimental",
                tensile_strength_min=_safe_float(row.get("Tensile Strength") or row.get("UTS")),
                yield_strength_min=_safe_float(row.get("Yield Strength") or row.get("YS")),
                elongation=_safe_float(row.get("Elongation")),
                hardness=str(row.get("Hardness"))[:50] if "Hardness" in row.index else None,
                composition=name,
                source_name=src_label,
                source_url=repo_url,
                is_verified=True,
                verification_count=1,
                data_quality_score=0.65,
            )

            db.add(mat)
            db.flush()

            src = MaterialSource(
                material_id=mat.id,
                source_type="datasheet",
                source_name=src_label,
                source_url=repo_url,
                access_type="free",
                confidence_score=0.65,
                notes="Steel strength prediction dataset",
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
                log.warning("  batiukmaks row %d error: %s", idx, exc)
            db.rollback()

    db.commit()
    log.info("  [OK] batiukmaks steel done – added %d, errors %d", added, errors)
    return added


# ===========================================================================
# Registry
# ===========================================================================
REPO_HANDLERS = {
    "kittycad": ("KittyCAD/material-properties", ingest_kittycad),
    "citrine": ("CitrineInformatics/MPEA_dataset", ingest_citrine),
    "elena": ("ElenaNKn/mechanical-properties", ingest_elena),
    "batiukmaks": ("batiukmaks/Steel-Strength-Prediction", ingest_batiukmaks),
}


def main():
    parser = argparse.ArgumentParser(description="Ingest GitHub material datasets")
    parser.add_argument("--repos", nargs="*", default=list(REPO_HANDLERS.keys()),
                        help="Repos to ingest (default: all)")
    args = parser.parse_args()

    log.info("=" * 60)
    log.info("GitHub Datasets Ingestion  (%s)", datetime.now().isoformat())
    log.info("Repos: %s", ", ".join(args.repos))
    log.info("=" * 60)

    os.makedirs(DATA_DIR, exist_ok=True)
    db = SessionLocal()
    grand_total = 0

    try:
        for key in args.repos:
            if key not in REPO_HANDLERS:
                log.warning("Unknown repo key '%s' – skipping", key)
                continue
            repo_name, handler = REPO_HANDLERS[key]
            log.info(">> Processing %s …", repo_name)
            count = handler(db)
            grand_total += count
    finally:
        db.close()

    log.info("=" * 60)
    log.info("GitHub ingestion complete. Total added: %d", grand_total)
    log.info("=" * 60)


if __name__ == "__main__":
    main()
