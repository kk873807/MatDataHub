#!/usr/bin/env python3
"""
validate_links.py - HTTP-check every source_url in batch1_material_sources.csv
and write back a verified file with real status codes.

Usage:
    pip install httpx
    python validate_links.py batch1_material_sources.csv

Output:
    batch1_material_sources.VERIFIED.csv   (adds http_status + final_url)
    broken_links.csv                       (only the failures, for re-work)

Notes:
  - MakeItFrom rows are the ones worth checking: a 200 proves the slug is correct.
  - Materials Project rows are a JS app; a 200 only proves the route loads,
    not that the formula exists. Use resolve_mp_ids.py for those instead.
"""
import csv
import sys
import asyncio
import httpx

CONCURRENCY = 8          # be polite; MakeItFrom is a small site
TIMEOUT = 20.0
DELAY = 0.15             # seconds between requests per worker

HEADERS = {
    "User-Agent": "mat-data-hub-linkcheck/1.0 (+https://mat-data-hub.vercel.app)"
}


async def check(client, sem, row):
    url = row.get("source_url", "").strip()
    if not url:
        row["http_status"] = "NO_URL"
        row["final_url"] = ""
        return row
    async with sem:
        try:
            r = await client.get(url, follow_redirects=True)
            row["http_status"] = str(r.status_code)
            row["final_url"] = str(r.url)
        except Exception as e:
            row["http_status"] = f"ERR:{type(e).__name__}"
            row["final_url"] = ""
        await asyncio.sleep(DELAY)
    return row


async def main(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    sem = asyncio.Semaphore(CONCURRENCY)
    async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS) as client:
        tasks = [check(client, sem, r) for r in rows]
        done = []
        for i, coro in enumerate(asyncio.as_completed(tasks), 1):
            done.append(await coro)
            if i % 25 == 0:
                print(f"  checked {i}/{len(tasks)}", file=sys.stderr)

    # preserve original order
    order = {r["material_name"]: i for i, r in enumerate(rows)}
    done.sort(key=lambda r: order.get(r["material_name"], 0))

    fields = list(done[0].keys())
    out = path.replace(".csv", ".VERIFIED.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(done)

    bad = [r for r in done if r["http_status"] != "200"]
    with open("broken_links.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(bad)

    print(f"\nwrote {out}")
    print(f"ok:     {len(done) - len(bad)}")
    print(f"broken: {len(bad)}  -> broken_links.csv")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1
                     else "batch1_material_sources.csv"))
