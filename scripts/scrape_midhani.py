import os
import time
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
from dotenv import load_dotenv

# Initialize Environment
load_dotenv()
supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

HEADERS = {
    "User-Agent": "MatDataHub-WebCrawler/1.0 (contact: admin@matdatahub.com) - Strategic PSU data gathering",
}

URLS = {
    "Superalloys": "https://midhani-india.in/midhani_products/superalloy/",
    "Titanium Alloys": "https://midhani-india.in/midhani_products/titanium-titanium-alloys/",
    "Other Metals": "https://midhani-india.in/midhani_products/other-metals-and-alloys/"
}

def clean_text(text):
    if not text:
        return ""
    # Remove weird characters like \n, \t, etc.
    return " ".join(text.replace("\n", " ").strip().split())

def scrape_category(category_name, url):
    print(f"\n🚀 Scraping {category_name} from {url}")
    try:
        response = requests.get(url, headers=HEADERS, verify=False, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    
    if not tables:
        print("⚠️ No tables found on page.")
        return

    materials_scraped = 0
    for table_idx, table in enumerate(tables):
        rows = table.find_all("tr")
        if not rows or len(rows) < 2:
            continue
            
        # Parse headers
        headers = [clean_text(th.text) for th in rows[0].find_all(["th", "td"])]
        
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) != len(headers):
                continue
                
            row_data = {headers[i]: clean_text(cols[i].text) for i in range(len(headers))}
            
            # Find the primary name
            midhani_name = ""
            for key in row_data:
                if "MIDHANI" in key.upper() and "NAME" in key.upper():
                    midhani_name = row_data[key]
                    break
                    
            if not midhani_name:
                # Fallback to first column
                midhani_name = row_data[headers[0]]
                
            if not midhani_name or midhani_name.isspace():
                continue
                
            # Find equivalent grades and UNS
            equivalents = []
            uns_num = None
            
            for key, val in row_data.items():
                if not val or val == "-" or val.isspace():
                    continue
                if "UNS" in key.upper():
                    uns_num = val
                elif "MIDHANI" not in key.upper():
                    # It's some spec or trade name
                    # Split by common separators if needed, but keeping it as is might be better
                    equivalents.append(f"{key}: {val}")
                    
            material = {
                "name": midhani_name,
                "category": "Metal",
                "subcategory": category_name,
                "source_url": url,
                "equivalent_grades": equivalents,
                "extraction_method": "BeautifulSoup Scraper (Deterministic)",
                "source_name": "MIDHANI"
            }
            if uns_num:
                material["uns_number"] = uns_num
                
            save_to_supabase(material)
            materials_scraped += 1

    print(f"✅ Finished {category_name}. Scraped {materials_scraped} materials.")

def save_to_supabase(material):
    try:
        # Avoid duplicates based on name and source_url
        existing = supabase.table('materials').select('id').eq('name', material['name']).eq('source_url', material['source_url']).execute()
        if existing.data:
            supabase.table('materials').update(material).eq('id', existing.data[0]['id']).execute()
            print(f"  [UPDATED] {material['name']}")
        else:
            supabase.table('materials').insert(material).execute()
            print(f"  [INSERTED] {material['name']}")
    except Exception as e:
        print(f"  [ERROR] Database error for {material['name']}: {e}")

def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    for category, url in URLS.items():
        scrape_category(category, url)
        print("⏳ Respecting server resources. Waiting 2 seconds...")
        time.sleep(2)
        
    print("\n🏁 All MIDHANI data scraped successfully!")

if __name__ == "__main__":
    main()
