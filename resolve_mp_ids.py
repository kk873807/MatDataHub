#!/usr/bin/env python3
"""
resolve_mp_ids.py - turn the 568 chemical formulas into permanent Materials
Project mp-id URLs, and pull their properties at the same time.

Why this exists:
  A ?formula= deep link is a search route. What you actually want in your DB is
  the canonical, permanent per-material URL:
      https://next-gen.materialsproject.org/materials/mp-864911
  There is no way to derive that from the formula - it has to be looked up.
  The API does all 568 in a couple of minutes.

Setup:
    pip install mp-api
    # free API key: https://next-gen.materialsproject.org/api  (log in -> API key)
    export MP_API_KEY="your_key_here"

Usage:
    python resolve_mp_ids.py batch1_material_sources.csv

Output:
    batch2_materials_project.csv
        material_name, formula_pretty, mp_id, source_url,
        band_gap, formation_energy_per_atom, energy_above_hull,
        density, volume, symmetry, is_stable, theoretical

A formula can map to several polymorphs. This script keeps the most stable one
(lowest energy_above_hull) as the primary and records the rest in mp_id_alts,
which is usually what you want for a single canonical source link per material.
"""
import csv
import os
import sys
from mp_api.client import MPRester

API_KEY = os.environ.get("MP_API_KEY")
if not API_KEY:
    sys.exit("Set MP_API_KEY first. Get one free at "
             "https://next-gen.materialsproject.org/api")

BASE = "https://next-gen.materialsproject.org/materials/"

FIELDS = [
    "material_id", "formula_pretty", "band_gap",
    "formation_energy_per_atom", "energy_above_hull",
    "density", "volume", "symmetry", "is_stable", "theoretical",
]


def load_formulas(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [r["material_name"] for r in csv.DictReader(f)
                if r["source_name"] == "Materials Project"]


def main(path):
    formulas = load_formulas(path)
    print(f"resolving {len(formulas)} formulas...")

    rows, missing = [], []
    with MPRester(API_KEY) as mpr:
        for i, formula in enumerate(formulas, 1):
            try:
                docs = mpr.materials.summary.search(
                    formula=formula, fields=FIELDS)
            except Exception as e:
                print(f"  ! {formula}: {e}", file=sys.stderr)
                missing.append(formula)
                continue

            if not docs:
                missing.append(formula)
                continue

            docs.sort(key=lambda d: (d.energy_above_hull
                                     if d.energy_above_hull is not None
                                     else 9e9))
            best = docs[0]
            alts = [str(d.material_id) for d in docs[1:]]

            rows.append({
                "material_name": formula,
                "formula_pretty": best.formula_pretty,
                "mp_id": str(best.material_id),
                "source_url": BASE + str(best.material_id),
                "band_gap": best.band_gap,
                "formation_energy_per_atom": best.formation_energy_per_atom,
                "energy_above_hull": best.energy_above_hull,
                "density": best.density,
                "volume": best.volume,
                "crystal_system": (str(best.symmetry.crystal_system)
                                   if best.symmetry else None),
                "spacegroup": (best.symmetry.symbol
                               if best.symmetry else None),
                "is_stable": best.is_stable,
                "theoretical": best.theoretical,
                "mp_id_alts": ";".join(alts),
            })

            if i % 50 == 0:
                print(f"  {i}/{len(formulas)}")

    out = "batch2_materials_project.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"\nwrote {out}")
    print(f"resolved: {len(rows)}")
    print(f"missing:  {len(missing)}")
    if missing:
        with open("mp_unresolved.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(missing))
        print("  -> mp_unresolved.txt")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1
         else "batch1_material_sources.csv")
