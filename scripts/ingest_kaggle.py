#!/usr/bin/env python3
"""
ingest_kaggle.py – Download and import Kaggle material-science datasets.

Datasets:
    1. Steel properties and composition
    2. Iron alloys dataset
    3. Materials and mechanical properties (Autodesk)
    4. High entropy alloys

Requirements:
    pip install kaggle pandas
    Set up ~/.kaggle/kaggle.json  (or KAGGLE_USERNAME + KAGGLE_KEY env vars)

Usage:
    python scripts/ingest_kaggle.py                   # all datasets
    python scripts/ingest_kaggle.py --datasets steel_composition
"""

import os
import sys
import argparse
import logging
import glob
import zipfile
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Material, MaterialSource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("ingest_kaggle")

BATCH_SIZE = 500
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "kaggle")

# ---------------------------------------------------------------------------
# Dataset registry
# ---------------------------------------------------------------------------
DATASETS = {
    "steel_composition": {
        "slug": "virajparab/steel-industry-data",
        "desc": "Steel industry composition and properties",
        "category": "Metal",
        "subcategory": "Steel",
    },
    "iron_alloys": {
        "slug": "amanbarthwal/iron-alloys-dataset",
        "desc": "Iron alloys mechanical properties",
        "category": "Metal",
        "subcategory": "Iron Alloy",
    },
    "autodesk_materials": {
        "slug": "dhruvildave/autodesk-material-library",
        "desc": "Autodesk materials and mechanical properties",
        "category": "Metal",
        "subcategory": None,
    },
    "high_entropy_alloys": {
        "slug": "mohdwahaj/high-entropy-alloys",
        "desc": "High entropy alloys dataset",
        "category": "Metal",
        "subcategory": "High Entropy Alloy",
    },
}


def _safe_float(val):
    if val is None:
        return None
    try:
        f = float(val)
        return f if f == f else None
    except (TypeError, ValueError):
        return None


def _fuzzy_col(df, candidates):
    """Find the first column in df that fuzzy-matches one of the candidate names."""
    cols_lower = {c.lower().strip().replace(" ", "_").replace("-", "_"): c for c in df.columns}
    for cand in candidates:
        cand_norm = cand.lower().strip().replace(" ", "_").replace("-", "_")
        # Exact
        if cand_norm in cols_lower:
            return cols_lower[cand_norm]
        # Substring
        for k, v in cols_lower.items():
            if cand_norm in k or k in cand_norm:
                return v
    return None


def _download_dataset(slug: str, dest_dir: str):
    """Download a Kaggle dataset using kagglehub."""
    import kagglehub
    import shutil
    
    # Map KAGGLE_API_TOKEN from .env to KAGGLE_PAT
    token = os.getenv("KAGGLE_API_TOKEN", "")
    if token:
        os.environ["KAGGLE_PAT"] = token
        
    try:
        log.info("  Downloading '%s' via kagglehub...", slug)
        path = kagglehub.dataset_download(slug)
        log.info("  Downloaded to %s", path)
        
        # Copy CSVs from kagglehub cache to dest_dir
        os.makedirs(dest_dir, exist_ok=True)
        import glob
        for csv_file in glob.glob(os.path.join(path, "**", "*.csv"), recursive=True):
            shutil.copy2(csv_file, dest_dir)
            
        return True
    except Exception as exc:
        log.error("  Failed to download %s: %s", slug, exc)
        log.warning("  If you see 403 Forbidden, you must open the dataset URL in your browser and click 'Accept Terms'.")
        return False


def _find_csvs(directory: str):
    """Find all CSV files in directory (recursively)."""
    return glob.glob(os.path.join(directory, "**", "*.csv"), recursive=True)


def ingest_dataset(ds_key: str, ds_info: dict, db):
    """Download + ingest one Kaggle dataset."""
    import pandas as pd

    slug = ds_info["slug"]
    dest = os.path.join(DATA_DIR, ds_key)
    os.makedirs(dest, exist_ok=True)

    # Download if no CSV files exist locally
    csvs = _find_csvs(dest)
    if not csvs:
        ok = _download_dataset(slug, dest)
        if not ok:
            return 0
        csvs = _find_csvs(dest)

    if not csvs:
        log.warning("  No CSV files found for '%s' – skipping", ds_key)
        return 0

    src_label = f"Kaggle: {ds_info['desc']}"
    source_url = f"https://www.kaggle.com/datasets/{slug}"

    existing = set(
        db.query(Material.name, Material.grade)
        .filter(Material.source_name == src_label)
        .all()
    )

    added = 0
    errors = 0

    for csv_path in csvs:
        log.info("  Processing %s …", os.path.basename(csv_path))
        try:
            df = pd.read_csv(csv_path, low_memory=False)
        except Exception as exc:
            log.warning("    Failed to read %s: %s", csv_path, exc)
            continue

        # Auto-detect columns
        name_col = _fuzzy_col(df, ["name", "material", "alloy", "formula", "composition", "steel_type", "grade"])
        density_col = _fuzzy_col(df, ["density", "rho"])
        ts_col = _fuzzy_col(df, ["tensile_strength", "uts", "ultimate_tensile_strength", "tensile"])
        ys_col = _fuzzy_col(df, ["yield_strength", "yield", "0.2%_proof_stress", "proof_stress"])
        elong_col = _fuzzy_col(df, ["elongation", "elongation_%", "elong"])
        hardness_col = _fuzzy_col(df, ["hardness", "hrc", "hrb", "hv", "brinell"])
        elastic_col = _fuzzy_col(df, ["elastic_modulus", "youngs_modulus", "modulus", "e_gpa"])
        comp_col = _fuzzy_col(df, ["composition", "alloy_composition", "chemical_composition"])

        for idx, row in df.iterrows():
            try:
                # Build name
                if name_col and pd.notna(row.get(name_col)):
                    name = str(row[name_col]).strip()[:200]
                else:
                    name = f"{ds_info.get('subcategory', 'Material')} #{idx}"

                grade = f"kaggle-{ds_key}-{idx}"
                if (name, grade) in existing:
                    continue

                mat = Material(
                    name=name,
                    grade=grade,
                    category=ds_info["category"],
                    subcategory=ds_info.get("subcategory"),
                    data_type="experimental",
                    density=_safe_float(row.get(density_col)) if density_col else None,
                    tensile_strength_min=_safe_float(row.get(ts_col)) if ts_col else None,
                    tensile_strength_max=_safe_float(row.get(ts_col)) if ts_col else None,
                    yield_strength_min=_safe_float(row.get(ys_col)) if ys_col else None,
                    yield_strength_max=_safe_float(row.get(ys_col)) if ys_col else None,
                    elongation=_safe_float(row.get(elong_col)) if elong_col else None,
                    hardness=str(row.get(hardness_col))[:50] if hardness_col and pd.notna(row.get(hardness_col)) else None,
                    elastic_modulus=_safe_float(row.get(elastic_col)) if elastic_col else None,
                    composition=str(row.get(comp_col))[:500] if comp_col and pd.notna(row.get(comp_col)) else None,
                    source_name=src_label,
                    source_url=source_url,
                    is_verified=True,
                    verification_count=1,
                    data_quality_score=0.6,
                )

                db.add(mat)
                db.flush()

                src = MaterialSource(
                    material_id=mat.id,
                    source_type="datasheet",
                    source_name=src_label,
                    source_url=source_url,
                    access_type="free",
                    confidence_score=0.65,
                    notes=f"Kaggle dataset: {slug}, file: {os.path.basename(csv_path)}, row {idx}",
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
                    log.warning("    Row %d error: %s", idx, exc)
                db.rollback()

    db.commit()
    log.info("  ✓ '%s' done – added %d, errors %d", ds_key, added, errors)
    return added


def main():
    parser = argparse.ArgumentParser(description="Ingest Kaggle materials datasets")
    parser.add_argument("--datasets", nargs="*", default=list(DATASETS.keys()),
                        help="Dataset keys to load (default: all)")
    args = parser.parse_args()

    log.info("=" * 60)
    log.info("Kaggle Ingestion  (%s)", datetime.now().isoformat())
    log.info("Datasets: %s", ", ".join(args.datasets))
    log.info("=" * 60)

    os.makedirs(DATA_DIR, exist_ok=True)
    db = SessionLocal()
    grand_total = 0

    try:
        for ds_key in args.datasets:
            if ds_key not in DATASETS:
                log.warning("Unknown dataset key '%s' – skipping", ds_key)
                continue
            count = ingest_dataset(ds_key, DATASETS[ds_key], db)
            grand_total += count
    finally:
        db.close()

    log.info("=" * 60)
    log.info("Kaggle ingestion complete. Total added: %d", grand_total)
    log.info("=" * 60)


if __name__ == "__main__":
    main()
