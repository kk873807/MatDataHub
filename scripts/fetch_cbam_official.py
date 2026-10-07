"""
Fetch the official text of Commission Implementing Regulation (EU) 2026/1740
(replacing Annexes I and IV of (EU) 2025/2621) and store it verbatim with provenance.

EUR-Lex answers direct requests with a bot challenge (HTTP 202, empty body), so the
page is retrieved through Firecrawl's scrape API. The raw HTML is saved unmodified
and its SHA-256 recorded, so the importer can prove which bytes it parsed.

Usage:
    python scripts/fetch_cbam_official.py            # uses FIRECRAWL_API_KEY from .env
    python scripts/fetch_cbam_official.py --file X   # register a manually downloaded copy
"""
import argparse
import datetime
import hashlib
import json
import os
import sys

import requests
from dotenv import load_dotenv

CELEX = "32026R1740"
SOURCE_URL = f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{CELEX}"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "cbam_official")
RAW_PATH = os.path.join(OUT_DIR, f"{CELEX}.html")
META_PATH = os.path.join(OUT_DIR, f"{CELEX}.provenance.json")


def write_provenance(raw: bytes, method: str):
    meta = {
        "celex": CELEX,
        "act": "Commission Implementing Regulation (EU) 2026/1740",
        "amends": "Implementing Regulation (EU) 2025/2621, Annexes I and IV replaced",
        "source_url": SOURCE_URL,
        "retrieved_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "retrieval_method": method,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(json.dumps(meta, indent=2))


def fetch_via_firecrawl() -> bytes:
    load_dotenv()
    key = os.getenv("FIRECRAWL_API_KEY")
    if not key:
        sys.exit("FIRECRAWL_API_KEY not set")
    resp = requests.post(
        "https://api.firecrawl.dev/v1/scrape",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"url": SOURCE_URL, "formats": ["rawHtml"], "proxy": "stealth",
              "timeout": 180000, "waitFor": 5000, "maxAge": 0},
        timeout=240,
    )
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        sys.exit(f"Firecrawl failed: {json.dumps(body)[:500]}")
    html = (body.get("data") or {}).get("rawHtml") or ""
    if len(html) < 10000:
        sys.exit(f"Suspiciously short response ({len(html)} chars) — likely a challenge page, not the act.")
    return html.encode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="Register a manually downloaded HTML copy instead of fetching")
    args = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)

    if args.file:
        with open(args.file, "rb") as f:
            raw = f.read()
        method = f"manual download ({os.path.basename(args.file)})"
    else:
        raw = fetch_via_firecrawl()
        method = "firecrawl /v1/scrape rawHtml (stealth proxy)"

    with open(RAW_PATH, "wb") as f:
        f.write(raw)
    write_provenance(raw, method)


if __name__ == "__main__":
    main()
