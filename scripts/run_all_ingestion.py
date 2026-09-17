#!/usr/bin/env python3
"""
run_all_ingestion.py – Master orchestrator for all ingestion scripts.

Runs each ingestion script as a subprocess, captures output, and produces
a final summary. One failing script does NOT stop the others.

Usage:
    python scripts/run_all_ingestion.py                # run everything
    python scripts/run_all_ingestion.py --skip nist     # skip NIST
    python scripts/run_all_ingestion.py --only mp oqmd  # run only those two
"""

import os
import sys
import subprocess
import argparse
import logging
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("run_all")

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable

# ---------------------------------------------------------------------------
# Pipeline definition  (key, script_file, description, default_args)
# ---------------------------------------------------------------------------
PIPELINE = [
    {
        "key": "migrate",
        "script": "migrate_schema.py",
        "desc": "Schema migration (add columns / tables)",
        "args": [],
    },
    {
        "key": "mp",
        "script": "ingest_materials_project.py",
        "desc": "Materials Project (computational DFT)",
        "args": ["--limit", "1000"],
    },
    {
        "key": "matminer",
        "script": "ingest_matminer.py",
        "desc": "matminer built-in datasets",
        "args": [],
    },
    {
        "key": "aflow",
        "script": "ingest_aflow.py",
        "desc": "AFLOW database (computational alloys)",
        "args": ["--limit", "1000"],
    },
    {
        "key": "oqmd",
        "script": "ingest_oqmd.py",
        "desc": "OQMD (Open Quantum Materials Database)",
        "args": ["--limit", "1000"],
    },
    {
        "key": "kaggle",
        "script": "ingest_kaggle.py",
        "desc": "Kaggle material datasets",
        "args": [],
    },
    {
        "key": "nist",
        "script": "ingest_nist.py",
        "desc": "NIST Alloy Data (experimental)",
        "args": [],
    },
    {
        "key": "github",
        "script": "ingest_github_datasets.py",
        "desc": "GitHub open-source datasets",
        "args": [],
    },
    {
        "key": "validate",
        "script": "cross_validate.py",
        "desc": "Cross-validation across sources",
        "args": [],
    },
]


def _run_script(step: dict):
    """Run a single script and return (success: bool, duration_s: float, output: str)."""
    script_path = os.path.join(SCRIPTS_DIR, step["script"])
    if not os.path.isfile(script_path):
        return False, 0.0, f"Script not found: {script_path}"

    cmd = [PYTHON, script_path] + step.get("args", [])
    start = time.time()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,  # 1 hour max per script
            cwd=os.path.dirname(SCRIPTS_DIR),  # project root
        )
        duration = time.time() - start
        output = result.stdout + ("\n--- STDERR ---\n" + result.stderr if result.stderr else "")

        return result.returncode == 0, duration, output

    except subprocess.TimeoutExpired:
        return False, time.time() - start, "TIMEOUT: script exceeded 1 hour"
    except Exception as exc:
        return False, time.time() - start, f"Exception: {exc}"


def main():
    parser = argparse.ArgumentParser(description="Run all MatDataHub ingestion scripts")
    parser.add_argument("--skip", nargs="*", default=[],
                        help="Script keys to skip")
    parser.add_argument("--only", nargs="*", default=[],
                        help="Run ONLY these script keys")
    args = parser.parse_args()

    skip_set = set(args.skip)
    only_set = set(args.only) if args.only else None

    log.info("=" * 70)
    log.info("  MatDataHub – Full Ingestion Pipeline")
    log.info("  Started: %s", datetime.now().isoformat())
    log.info("=" * 70)

    results = []

    for step in PIPELINE:
        key = step["key"]

        if only_set and key not in only_set:
            continue
        if key in skip_set:
            log.info("⏭  Skipping [%s] %s", key, step["desc"])
            results.append({"key": key, "desc": step["desc"], "status": "SKIPPED", "duration": 0, "output": ""})
            continue

        log.info("")
        log.info(">> [%s] %s", key, step["desc"])
        log.info("-" * 50)

        success, duration, output = _run_script(step)

        status = "[OK]" if success else "[FAIL]"
        log.info("   %s  (%.1f s)", status, duration)

        # Print last 10 lines of output as a summary
        lines = output.strip().split("\n")
        for line in lines[-10:]:
            log.info("   │ %s", line)

        results.append({
            "key": key,
            "desc": step["desc"],
            "status": status,
            "duration": duration,
            "output": output,
        })

    # ---------------------------------------------------------------------------
    # Final Summary
    # ---------------------------------------------------------------------------
    log.info("")
    log.info("=" * 70)
    log.info("  FINAL SUMMARY")
    log.info("=" * 70)
    log.info("  %-12s  %-42s  %s  %s", "Key", "Description", "Status", "Time")
    log.info("  %s", "-" * 66)

    total_time = 0
    passed = 0
    failed = 0

    for r in results:
        log.info("  %-12s  %-42s  %-8s  %.1fs",
                 r["key"], r["desc"], r["status"], r["duration"])
        total_time += r["duration"]
        if "OK" in r["status"]:
            passed += 1
        elif "FAIL" in r["status"]:
            failed += 1

    log.info("")
    log.info("  Total time: %.1f s  |  Passed: %d  |  Failed: %d  |  Skipped: %d",
             total_time, passed, failed, len(results) - passed - failed)

    # Try to report current DB total
    try:
        from app.database import SessionLocal
        from app.models import Material, MaterialSource
        db = SessionLocal()
        mat_count = db.query(Material).count()
        src_count = db.query(MaterialSource).count()
        db.close()
        log.info("  Database totals: %d materials, %d source records", mat_count, src_count)
    except Exception:
        pass

    log.info("=" * 70)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
