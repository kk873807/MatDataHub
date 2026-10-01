import os
import csv
import time
import requests
import urllib3
from dotenv import load_dotenv
from supabase import create_client

urllib3.disable_warnings()

# Configuration
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
CSV_FILENAME = "broken_links_report.csv"

# Request Headers to bypass basic bot blocks
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def verify_links():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("Fetching all materials from the database...")
    # Handle pagination if you have more than 1000 rows
    response = supabase.table("materials").select("id, name, source_url").execute()
    materials = response.data
    print(f"Found {len(materials)} materials to process.")

    broken_links = []

    for idx, mat in enumerate(materials):
        name = mat.get("name", "Unknown")
        urls_str = mat.get("source_url", "")
        
        if not urls_str:
            continue
            
        # Split by comma in case of multiple links
        urls = [u.strip() for u in urls_str.split(",") if u.strip()]
        
        for url in urls:
            status = "OK"
            error_details = ""
            try:
                # Timeout set to 15 seconds so we don't hang forever
                r = requests.get(url, headers=HEADERS, timeout=15, verify=False, allow_redirects=True)
                
                # Check for bad status codes
                if r.status_code >= 400:
                    status = "ERROR"
                    error_details = f"HTTP {r.status_code}"
                
                # Check if we got redirected to a generic search page
                elif "search" in r.url.lower() and "search" not in url.lower():
                    status = "REDIRECT_TO_SEARCH"
                    error_details = f"Redirected to: {r.url}"
                    
            except requests.exceptions.Timeout:
                status = "ERROR"
                error_details = "Timeout after 15s"
            except requests.exceptions.TooManyRedirects:
                status = "ERROR"
                error_details = "Too many redirects"
            except requests.exceptions.RequestException as e:
                status = "ERROR"
                error_details = str(e).split(":")[-1].strip()

            if status != "OK":
                print(f"[{status}] {name} -> {url} ({error_details})")
                broken_links.append({
                    "Material Name": name,
                    "Broken URL": url,
                    "Issue Type": status,
                    "Error Details": error_details
                })
            
            # Sleep briefly to avoid hammering domains (like fpl.fs.usda.gov) and getting IP banned
            time.sleep(1)
            
        if (idx + 1) % 10 == 0:
            print(f"Processed {idx + 1}/{len(materials)} materials...")

    # Write results to CSV
    print(f"\nScan complete! Found {len(broken_links)} broken or suspicious links.")
    with open(CSV_FILENAME, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Material Name", "Broken URL", "Issue Type", "Error Details"])
        writer.writeheader()
        writer.writerows(broken_links)
    
    print(f"Report saved to {CSV_FILENAME}")

if __name__ == "__main__":
    verify_links()
