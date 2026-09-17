#!/usr/bin/env python3
"""
ingest_materials_project.py – Import materials from the Materials Project API.

Requirements:
    pip install mp-api

Set the environment variable MP_API_KEY (get one free at materialsproject.org).

Usage:
    python scripts/ingest_materials_project.py                # default 1000 materials
    python scripts/ingest_materials_project.py --limit 5000   # fetch 5000
    python scripts/ingest_materials_project.py --limit 0      # fetch ALL
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
log = logging.getLogger("ingest_mp")

BATCH_SIZE = 500  # commit every N records


def _safe_float(val):
    """Return float or None for non-numeric values."""
    if val is None:
        return None
    try:
        f = float(val)
        return f if f == f else None  # filter NaN
    except (TypeError, ValueError):
        return None


def _composition_str(comp):
    """Convert a pymatgen Composition to a human-readable string like 'Fe:0.50, Cr:0.25, Ni:0.25'."""
    if comp is None:
        return None
    try:
        parts = []
        for el, frac in sorted(comp.fractional_composition.as_dict().items()):
            parts.append(f"{el}:{frac:.4f}")
        return ", ".join(parts)
    except Exception:
        return str(comp)


def _category_from_elements(comp):
    """Rough categorisation based on element types."""
    if comp is None:
        return "Computational Material", None
    try:
        elements = {str(e) for e in comp.elements}
    except Exception:
        return "Computational Material", None

    metals = {"Fe", "Al", "Ti", "Cu", "Ni", "Cr", "Co", "Mn", "W", "Mo",
              "Zn", "Zr", "Nb", "V", "Ta", "Hf", "Pt", "Au", "Ag", "Pd"}
    non_metals = {"C", "N", "O", "S", "F", "Cl", "Br", "I", "H", "P", "Se", "Te"}
    semiconductors = {"Si", "Ge", "Ga", "As", "In", "Sb", "Cd"}

    if elements <= metals:
        return "Metal", "Alloy (Computational)"
    if elements & semiconductors:
        return "Semiconductor", None
    if elements & metals and elements & non_metals:
        if "O" in elements:
            return "Ceramic", "Oxide"
        return "Metal", "Compound"
    return "Computational Material", None


def ingest(limit: int):
    try:
        from mp_api.client import MPRester
    except ImportError:
        log.error("mp-api is not installed. Run: pip install mp-api")
        sys.exit(1)

    api_key = os.getenv("MP_API_KEY", "")
    if not api_key:
        log.error("MP_API_KEY not set. Get one at https://materialsproject.org/api")
        sys.exit(1)

    db = SessionLocal()
    added = 0
    skipped = 0
    errors = 0

    log.info("=" * 60)
    log.info("Materials Project Ingestion  (%s)", datetime.now().isoformat())
    log.info("Limit: %s", limit if limit else "ALL")
    log.info("=" * 60)

    try:
        with MPRester(api_key) as mpr:
            # Fields to request
            fields = [
                "material_id", "formula_pretty", "density",
                "symmetry", "composition", "composition_reduced",
                "band_gap", "formation_energy_per_atom",
                "energy_above_hull", "is_stable",
            ]

            log.info("Querying Materials Project (this may take a while) …")

            # Fetch a summary of materials
            kwargs = {"fields": fields}
            if limit and limit > 0:
                kwargs["num_chunks"] = max(1, limit // 1000)
                kwargs["chunk_size"] = min(1000, limit)

            docs = mpr.materials.summary.search(**kwargs)

            if limit and limit > 0:
                docs = docs[:limit]

            total = len(docs)
            log.info("Received %d materials from MP", total)

            # Pre-load existing names for fast duplicate check
            existing = set(
                db.query(Material.name, Material.grade)
                .filter(Material.source_name == "Materials Project")
                .all()
            )

            for i, doc in enumerate(docs):
                try:
                    mp_id = str(doc.material_id)
                    name = doc.formula_pretty or mp_id
                    grade = mp_id  # unique identifier as grade

                    if (name, grade) in existing:
                        skipped += 1
                        continue

                    comp = getattr(doc, "composition", None)
                    cat, subcat = _category_from_elements(comp)
                    symmetry = getattr(doc, "symmetry", None)
                    crystal = symmetry.crystal_system.value if symmetry and hasattr(symmetry, "crystal_system") else None

                    mat = Material(
                        name=name,
                        grade=grade,
                        category=cat,
                        subcategory=subcat,
                        data_type="computational",
                        density=_safe_float(doc.density),
                        composition=_composition_str(comp),
                        crystal_structure=crystal,
                        elastic_modulus=None,  # set from elastic below if available
                        source_name="Materials Project",
                        source_url=f"https://materialsproject.org/materials/{mp_id}",
                        description=(
                            f"DFT-computed material from Materials Project. "
                            f"Band gap: {_safe_float(doc.band_gap)} eV, "
                            f"Formation energy: {_safe_float(doc.formation_energy_per_atom)} eV/atom"
                        ),
                        is_verified=True,
                        verification_count=1,
                        data_quality_score=0.7,
                    )

                    db.add(mat)
                    db.flush()  # get mat.id

                    # MaterialSource entry
                    src = MaterialSource(
                        material_id=mat.id,
                        source_type="database_api",
                        source_name="Materials Project",
                        source_url=f"https://materialsproject.org/materials/{mp_id}",
                        source_doi="10.17188/1313363",
                        access_type="free",
                        confidence_score=0.85,
                        notes=f"DFT GGA/GGA+U calculation, {crystal or 'unknown'} crystal system",
                    )
                    db.add(src)

                    existing.add((name, grade))
                    added += 1

                    # Batch commit
                    if added % BATCH_SIZE == 0:
                        db.commit()
                        log.info("  … committed %d / %d  (skipped %d)", added, total, skipped)

                except Exception as exc:
                    errors += 1
                    if errors <= 5:
                        log.warning("Error on doc %d: %s", i, exc)
                    db.rollback()

            # Final commit
            db.commit()

    except Exception as exc:
        log.error("Fatal error during MP ingestion: %s", exc, exc_info=True)
        db.rollback()
    finally:
        db.close()

    log.info("=" * 60)
    log.info("Materials Project ingestion complete.")
    log.info("  Added:   %d", added)
    log.info("  Skipped: %d  (duplicates)", skipped)
    log.info("  Errors:  %d", errors)
    log.info("=" * 60)
    return added


def main():
    parser = argparse.ArgumentParser(description="Ingest Materials Project data")
    parser.add_argument("--limit", type=int, default=1000,
                        help="Max materials to fetch (0 = all). Default: 1000")
    args = parser.parse_args()
    ingest(args.limit)


if __name__ == "__main__":
    main()
