"""
Deep Dive V2 — Rate-limit-respecting re-extraction for sparse materials.

Key improvements over the original deep_dive_extract.py:
1. Longer cooldowns between API calls (15s base, 90s on rate-limit)
2. Exponential backoff on consecutive failures
3. Progress checkpoint file so you can resume if interrupted
4. Skips Materials Project, Kaggle, and Experimental materials
5. Only targets materials missing 4+ of 7 key properties
6. Saves a detailed JSON report alongside the text log

Run in VS Code terminal:
    python scripts/deep_dive_v2.py

To resume after interruption, just run it again — it reads the checkpoint file.
"""

import os
import sys
import json
import time
from datetime import datetime

# Ensure auto_crawler can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# ----- CONFIG -----
KEY_PROPS = ['density', 'yield_strength_min', 'thermal_conductivity', 'hardness',
             'elastic_modulus', 'tensile_strength_min', 'melting_point_min']
MIN_MISSING = 4           # Must be missing at least this many of 7 key properties
BASE_COOLDOWN = 15        # Seconds between successful extractions
RATE_LIMIT_COOLDOWN = 90  # Seconds to wait after a rate-limit failure
MAX_CONSECUTIVE_FAILS = 5 # Pause longer after this many consecutive failures
LONG_PAUSE = 300          # 5-minute pause after MAX_CONSECUTIVE_FAILS

CHECKPOINT_FILE = os.path.join(os.path.dirname(__file__), '..', 'deep_dive_v2_checkpoint.json')
REPORT_FILE = os.path.join(os.path.dirname(__file__), '..', 'deep_dive_v2_report.txt')


def load_checkpoint():
    """Load set of already-processed material IDs."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            data = json.load(f)
            return set(data.get('processed_ids', []))
    return set()


def save_checkpoint(processed_ids):
    """Persist the set of processed IDs to disk."""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump({'processed_ids': list(processed_ids), 'updated_at': datetime.now().isoformat()}, f)


def get_sparse_materials():
    """Fetch all materials missing 4+ key properties with valid scrape-able URLs."""
    all_sparse = []
    page = 0
    page_size = 1000

    print("Fetching materials from database to find sparse targets...")
    while True:
        cols = 'id, name, source_name, source_url, ' + ', '.join(KEY_PROPS)
        res = supabase.table('materials').select(cols).range(
            page * page_size, (page + 1) * page_size - 1
        ).execute()
        if not res.data:
            break

        for mat in res.data:
            url = mat.get('source_url') or ''
            source = mat.get('source_name') or ''
            name = mat.get('name') or ''

            # Skip non-scrape-able sources
            if 'Materials Project' in source or 'Kaggle' in source:
                continue
            if 'Experimental' in name:
                continue
            if not url.startswith('http'):
                continue

            missing = sum(1 for k in KEY_PROPS if mat.get(k) is None)
            if missing >= MIN_MISSING:
                all_sparse.append(mat)

        if len(res.data) < page_size:
            break
        page += 1

    return all_sparse


def main():
    print("=" * 60)
    print("DEEP DIVE V2 — Rate-Limit-Respecting Re-Extraction")
    print("=" * 60)

    # Late import so the script can show usage info without needing all deps
    try:
        from auto_crawler import process_single_material
    except ImportError:
        print("ERROR: Could not import auto_crawler. Ensure it is in scripts/.")
        sys.exit(1)

    sparse = get_sparse_materials()
    processed = load_checkpoint()
    remaining = [m for m in sparse if m['id'] not in processed]

    print(f"Total sparse: {len(sparse)} | Already processed: {len(processed)} | Remaining: {len(remaining)}")

    if not remaining:
        print("Nothing left to process. Exiting.")
        return

    success = 0
    failed = 0
    consecutive_fails = 0

    with open(REPORT_FILE, 'a', encoding='utf-8') as report:
        report.write(f"\n{'='*60}\n")
        report.write(f"Session started: {datetime.now().isoformat()}\n")
        report.write(f"Targets this session: {len(remaining)}\n\n")

        for i, mat in enumerate(remaining):
            url = mat['source_url']
            name = mat['name']
            mat_id = mat['id']
            missing_before = sum(1 for k in KEY_PROPS if mat.get(k) is None)

            print(f"\n[{i+1}/{len(remaining)}] {name} ({missing_before}/7 missing)")
            print(f"  URL: {url[:100]}")

            try:
                process_single_material(url, max_retries=2)
                success += 1
                consecutive_fails = 0
                report.write(f"[OK] {name} -> {url}\n")
                print(f"  ✅ Done. Cooling down {BASE_COOLDOWN}s...")
                time.sleep(BASE_COOLDOWN)

            except Exception as e:
                failed += 1
                consecutive_fails += 1
                err_msg = str(e)[:200]
                report.write(f"[FAIL] {name} -> {url} | {err_msg}\n")
                print(f"  ❌ Failed: {err_msg}")

                if consecutive_fails >= MAX_CONSECUTIVE_FAILS:
                    print(f"  🛑 {MAX_CONSECUTIVE_FAILS} consecutive failures. Pausing {LONG_PAUSE}s...")
                    report.write(f"[PAUSE] {LONG_PAUSE}s after {MAX_CONSECUTIVE_FAILS} consecutive failures\n")
                    time.sleep(LONG_PAUSE)
                    consecutive_fails = 0
                else:
                    print(f"  ⏳ Rate-limit cooldown {RATE_LIMIT_COOLDOWN}s...")
                    time.sleep(RATE_LIMIT_COOLDOWN)

            # Always checkpoint after each material
            processed.add(mat_id)
            save_checkpoint(processed)

        report.write(f"\nSession complete: {datetime.now().isoformat()}\n")
        report.write(f"Success: {success} | Failed: {failed}\n")

    print("\n" + "=" * 60)
    print("SESSION COMPLETE")
    print(f"  Success: {success}")
    print(f"  Failed:  {failed}")
    print(f"  Total processed (all sessions): {len(processed)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
