import os
import re
import time
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

# Import the existing pipeline from auto_crawler
from auto_crawler import process_single_material

def scrape_aalco_category(category_url: str):
    print(f"🚀 Starting Aalco Scraper for category: {category_url}")
    
    # Initialize Firecrawl
    load_dotenv()
    app = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
    
    print("📥 Fetching category page to discover datasheets...")
    res = app.scrape_url(category_url)
    md = getattr(res, 'markdown', str(res))
    
    # Extract all .ashx links from the markdown
    # Format typically: [Link Text](https://www.aalco.co.uk/datasheets/Aluminium-Alloy-1050-0-Sheet_58.ashx "View")
    urls = re.findall(r'\]\((https://www\.aalco\.co\.uk/datasheets/[^\)]+\.ashx)', md)
    
    # Deduplicate while preserving order
    urls = list(dict.fromkeys(urls))
    
    print(f"✅ Found {len(urls)} unique datasheet links!")
    print("=" * 50)
    
    if len(urls) == 0:
        print("⚠️ No links found. Exiting.")
        return
        
    for i, url in enumerate(urls):
        # We split by ' ' in case the regex caught the title tag like .ashx "View" 
        clean_url = url.split('"')[0].strip()
        print(f"\n[{i+1}/{len(urls)}] Processing {clean_url}")
        process_single_material(clean_url)
        
    print("\n🏁 Aalco scraping completely finished!")

if __name__ == "__main__":
    target = "https://www.aalco.co.uk/datasheets/?gId=1"
    scrape_aalco_category(target)
