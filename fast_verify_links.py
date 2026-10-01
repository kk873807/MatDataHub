
import os
import csv
import time
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from supabase import create_client

urllib3.disable_warnings()

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def check_link(item):
    name, url = item
    status = "OK"
    error_details = ""
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, verify=False, allow_redirects=True)
        if r.status_code >= 400:
            status = "ERROR"
            error_details = f"HTTP {r.status_code}"
        elif "search" in r.url.lower() and "search" not in url.lower():
            status = "REDIRECT_TO_SEARCH"
            error_details = f"Redirected to: {r.url}"
    except requests.exceptions.Timeout:
        status = "ERROR"
        error_details = "Timeout after 10s"
    except requests.exceptions.TooManyRedirects:
        status = "ERROR"
        error_details = "Too many redirects"
    except requests.exceptions.RequestException as e:
        status = "ERROR"
        error_details = str(e).split(":")[-1].strip()
    
    if status != "OK":
        return {
            "Material Name": name,
            "Broken URL": url,
            "Issue Type": status,
            "Error Details": error_details
        }
    return None

def main():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # We must handle pagination since supabase select by default limits to 1000 rows
    all_materials = []
    limit = 1000
    offset = 0
    while True:
        response = supabase.table("materials").select("id, name, source_url").range(offset, offset + limit - 1).execute()
        if not response.data:
            break
        all_materials.extend(response.data)
        if len(response.data) < limit:
            break
        offset += limit
    
    tasks = []
    for mat in all_materials:
        name = mat.get("name", "Unknown")
        urls_str = mat.get("source_url", "")
        if not urls_str:
            continue
        urls = [u.strip() for u in urls_str.split(",") if u.strip()]
        for u in urls:
            tasks.append((name, u))
            
    broken_links = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_link, t): t for t in tasks}
        count = 0
        for future in as_completed(futures):
            count += 1
            if count % 500 == 0:
                print(f"Processed {count}/{len(tasks)} links...")
            res = future.result()
            if res:
                broken_links.append(res)
                
    with open("broken_links_report.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Material Name", "Broken URL", "Issue Type", "Error Details"])
        writer.writeheader()
        writer.writerows(broken_links)
        
    unique_mats = sorted(list(set(r["Material Name"] for r in broken_links)))
    
    with open("broken_materials_clean.txt", "w", encoding="utf-8") as f:
        for m in unique_mats:
            f.write(m + "\n")
            
    artifact_path = r"C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\broken_materials.md"
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.write("# Broken Materials List\n\n")
        f.write(f"Total broken links: {len(broken_links)}\n")
        f.write(f"Unique materials with broken links: {len(unique_mats)}\n\n")
        for m in unique_mats:
            f.write(f"- {m}\n")
    print(f"Done. Found {len(unique_mats)} unique materials with broken links.")

if __name__ == "__main__":
    main()

