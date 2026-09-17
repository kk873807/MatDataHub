#!/usr/bin/env python3
"""
ingest_matminer.py – Import materials from matminer built-in datasets.

Datasets loaded:
    • elastic_tensor_2015    – 1 181 materials with elastic properties
    • dielectric_constant    – 1 056 materials
    • expt_gap               – 6 354 materials with experimental band gaps
    • steel_strength          – steel compositions + strengths
    • castelli_perovskites   – 18 928 perovskites

Requirements:
    pip install matminer

Usage:
    python scripts/ingest_matminer.py                       # all datasets
    python scripts/ingest_matminer.py --datasets elastic_tensor_2015 expt_gap
"""

import os
import sys
import argparse
import logging
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Material, MaterialSource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("ingest_matminer")

BATCH_SIZE = 500

# Dataset → (data_type, description)
DATASET_META = {
    "elastic_tensor_2015": {
        "data_type": "computational",
        "desc": "DFT-computed elastic tensors (de Jong et al. 2015)",
        "doi": "10.1038/sdata.2015.9",
    },
    "dielectric_constant": {
        "data_type": "computational",
        "desc": "DFT-computed dielectric properties (Petousis et al. 2017)",
        "doi": "10.1038/sdata.2017.134",
    },
    "expt_gap": {
        "data_type": "experimental",
        "desc": "Experimentally measured band gaps (Zhuo et al. 2018)",
        "doi": "10.1021/acs.jpclett.8b00124",
    },
    "steel_strength": {
        "data_type": "experimental",
        "desc": "Experimental steel yield/tensile strengths from NIMS",
        "doi": None,
    },
    "castelli_perovskites": {
        "data_type": "computational",
        "desc": "DFT-computed perovskite properties (Castelli et al. 2012)",
        "doi": "10.1039/C2EE22341D",
    },
}

SOURCE_URL = "https://hackingmaterials.lbl.gov/matminer/dataset_summary.html"


def _safe_float(val):
    if val is None:
        return None
    try:
        f = float(val)
        return f if f == f else None
    except (TypeError, ValueError):
        return None


def _comp_str(row):
    """Try to get composition string from various column patterns."""
    for col in ("formula", "composition", "reduced_cell_formula", "pretty_formula"):
        if col in row.index and row[col] is not None:
            return str(row[col])
    return None


def _name(row):
    for col in ("formula", "pretty_formula", "composition", "reduced_cell_formula"):
        if col in row.index and row[col]:
            return str(row[col])
    return "Unknown"


def ingest_dataset(dataset_name: str, db):
    from matminer.datasets import load_dataset

    meta = DATASET_META.get(dataset_name)
    if not meta:
        log.warning("Unknown dataset '%s' – skipping", dataset_name)
        return 0

    log.info("Loading dataset '%s' …", dataset_name)
    try:
        df = load_dataset(dataset_name)
    except Exception as exc:
        log.error("Failed to load '%s': %s", dataset_name, exc)
        return 0

    log.info("  %d rows loaded", len(df))

    # Pre-load existing names for this source
    src_label = f"matminer ({dataset_name})"
    existing = set(
        db.query(Material.name, Material.grade)
        .filter(Material.source_name == src_label)
        .all()
    )

    added = 0
    errors = 0
    cols = set(df.columns)

    for idx, row in df.iterrows():
        try:
            name = _name(row)
            grade = f"matminer-{dataset_name}-{idx}"

            if (name, grade) in existing:
                continue

            # Extract fields based on dataset
            density = _safe_float(row.get("density")) if "density" in cols else None
            elastic_modulus = None
            shear_modulus = None
            poissons_ratio = None
            tensile_min = None
            tensile_max = None
            yield_min = None
            yield_max = None
            crystal_structure = None

            if dataset_name == "elastic_tensor_2015":
                elastic_modulus = _safe_float(row.get("K_VRH"))  # Bulk modulus
                shear_modulus = _safe_float(row.get("G_VRH"))
                poissons_ratio = _safe_float(row.get("poisson_ratio"))
                crystal_structure = str(row.get("structure", ""))[:50] if "structure" in cols else None
                # crystal_structure from structure object
                try:
                    crystal_structure = row["structure"].get_space_group_info()[0][:50]
                except Exception:
                    pass

            elif dataset_name == "steel_strength":
                tensile_min = _safe_float(row.get("tensile strength"))
                tensile_max = tensile_min
                yield_min = _safe_float(row.get("yield strength"))
                yield_max = yield_min

            comp = _comp_str(row)

            cat = "Metal" if dataset_name == "steel_strength" else "Computational Material"
            subcat = "Steel" if dataset_name == "steel_strength" else None
            if dataset_name == "castelli_perovskites":
                cat = "Ceramic"
                subcat = "Perovskite"

            mat = Material(
                name=name,
                grade=grade,
                category=cat,
                subcategory=subcat,
                data_type=meta["data_type"],
                density=density,
                elastic_modulus=elastic_modulus,
                shear_modulus=shear_modulus,
                poissons_ratio=poissons_ratio,
                tensile_strength_min=tensile_min,
                tensile_strength_max=tensile_max,
                yield_strength_min=yield_min,
                yield_strength_max=yield_max,
                crystal_structure=crystal_structure,
                composition=comp,
                source_name=src_label,
                source_url=SOURCE_URL,
                is_verified=True,
                verification_count=1,
                data_quality_score=0.75 if meta["data_type"] == "computational" else 0.85,
            )

            db.add(mat)
            db.flush()

            src = MaterialSource(
                material_id=mat.id,
                source_type="research_paper" if meta["doi"] else "database_api",
                source_name=src_label,
                source_url=SOURCE_URL,
                source_doi=meta.get("doi"),
                access_type="free",
                confidence_score=0.8,
                notes=meta["desc"],
            )
            db.add(src)

            existing.add((name, grade))
            added += 1

            if added % BATCH_SIZE == 0:
                db.commit()
                log.info("    … committed %d / %d rows", added, len(df))

        except Exception as exc:
            errors += 1
            if errors <= 5:
                log.warning("  Error on row %s: %s", idx, exc)
            db.rollback()

    db.commit()
    log.info("  [OK] '%s' done – added %d, errors %d", dataset_name, added, errors)
    return added


def main():
    parser = argparse.ArgumentParser(description="Ingest matminer datasets")
    parser.add_argument(
        "--datasets", nargs="*", default=list(DATASET_META.keys()),
        help="Datasets to load (default: all)")
    args = parser.parse_args()

    log.info("=" * 60)
    log.info("matminer Ingestion  (%s)", datetime.now().isoformat())
    log.info("Datasets: %s", ", ".join(args.datasets))
    log.info("=" * 60)

    db = SessionLocal()
    grand_total = 0

    try:
        for ds in args.datasets:
            count = ingest_dataset(ds, db)
            grand_total += count
    finally:
        db.close()

    log.info("=" * 60)
    log.info("matminer ingestion complete. Total added: %d", grand_total)
    log.info("=" * 60)


if __name__ == "__main__":
    main()
