#!/usr/bin/env python3
"""
cross_validate.py – Cross-validate materials that appear in multiple sources.

Strategy:
    1. Group materials by normalised name/formula.
    2. For each group of ≥ 2, compare density, tensile_strength, yield_strength.
    3. Flag discrepancies > 5 % of the mean.
    4. Set cross_validated = True and compute data_quality_score.
    5. Update verification_count.

Usage:
    python scripts/cross_validate.py                     # run validation
    python scripts/cross_validate.py --threshold 10      # 10% tolerance
    python scripts/cross_validate.py --dry-run            # preview only
"""

import os
import sys
import re
import argparse
import logging
from datetime import datetime
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Material

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("cross_validate")


def _normalise(name: str) -> str:
    """Normalise a material name for grouping (lowercase, remove whitespace/punctuation)."""
    if not name:
        return ""
    s = name.lower().strip()
    # Remove common suffixes like "(Annealed)" etc.
    s = re.sub(r"\s*\(.*?\)\s*", " ", s)
    # Remove punctuation except hyphens
    s = re.sub(r"[^a-z0-9\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _pct_diff(values):
    """Return the max percentage deviation from the mean, or None if insufficient data."""
    vals = [v for v in values if v is not None and v > 0]
    if len(vals) < 2:
        return None
    mean = sum(vals) / len(vals)
    if mean == 0:
        return None
    max_dev = max(abs(v - mean) / mean * 100 for v in vals)
    return max_dev


def cross_validate(threshold: float = 5.0, dry_run: bool = False):
    log.info("=" * 60)
    log.info("Cross-Validation  (%s)", datetime.now().isoformat())
    log.info("Discrepancy threshold: %.1f%%", threshold)
    log.info("=" * 60)

    db = SessionLocal()

    try:
        materials = db.query(Material).all()
        log.info("Total materials in DB: %d", len(materials))

        # Group by normalised name
        groups = defaultdict(list)
        for mat in materials:
            key = _normalise(mat.name)
            if key:
                groups[key].append(mat)

        # Filter to groups with ≥ 2 entries
        multi = {k: v for k, v in groups.items() if len(v) >= 2}
        log.info("Materials with multiple entries (potential cross-validation): %d groups", len(multi))

        validated = 0
        flagged = 0

        for key, mats in multi.items():
            # Collect property values across entries
            densities = [m.density for m in mats]
            ts_vals = [m.tensile_strength_min for m in mats]
            ys_vals = [m.yield_strength_min for m in mats]

            density_dev = _pct_diff(densities)
            ts_dev = _pct_diff(ts_vals)
            ys_dev = _pct_diff(ys_vals)

            # Determine if any property has significant discrepancy
            discrepancies = []
            for prop_name, dev in [("density", density_dev), ("tensile_strength", ts_dev), ("yield_strength", ys_dev)]:
                if dev is not None and dev > threshold:
                    discrepancies.append(f"{prop_name}={dev:.1f}%")

            has_discrepancy = len(discrepancies) > 0
            n_sources = len(mats)
            n_with_data = sum(1 for m in mats if m.density or m.tensile_strength_min or m.yield_strength_min)

            # Compute quality score
            # Base: 0.5 + up to 0.3 for multiple sources + up to 0.2 for agreement
            base = 0.5
            source_bonus = min(0.3, n_sources * 0.1)
            agreement_bonus = 0.0 if has_discrepancy else 0.2
            quality_score = round(base + source_bonus + agreement_bonus, 2)

            if has_discrepancy:
                flagged += 1
                if flagged <= 20:
                    log.warning("  ⚠ '%s' (%d entries) – discrepancies: %s",
                                mats[0].name, n_sources, ", ".join(discrepancies))
            else:
                validated += 1

            if not dry_run:
                for mat in mats:
                    mat.verification_count = n_sources
                    mat.cross_validated = not has_discrepancy
                    mat.data_quality_score = quality_score

        if not dry_run:
            db.commit()
            log.info("Database updated.")
        else:
            log.info("[DRY-RUN] No changes written to database.")

        log.info("=" * 60)
        log.info("Cross-validation complete.")
        log.info("  Groups examined: %d", len(multi))
        log.info("  Validated (agreement ≤ %.1f%%): %d", threshold, validated)
        log.info("  Flagged (discrepancy > %.1f%%): %d", threshold, flagged)
        log.info("=" * 60)

    except Exception as exc:
        log.error("Error during cross-validation: %s", exc, exc_info=True)
        db.rollback()
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Cross-validate materials across sources")
    parser.add_argument("--threshold", type=float, default=5.0,
                        help="Max %% deviation before flagging (default: 5.0)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without updating the database")
    args = parser.parse_args()
    cross_validate(threshold=args.threshold, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
