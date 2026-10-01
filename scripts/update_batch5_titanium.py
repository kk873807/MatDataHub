import os
import json
import re
import time
from dotenv import load_dotenv
from supabase import create_client
from firecrawl import FirecrawlApp
from google import genai
from google.genai import types

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
firecrawl_app = FirecrawlApp(api_key=os.environ.get('FIRECRAWL_API_KEY'))

with open('.env', 'r', encoding='utf-8') as f:
    env_text = f.read()
gemini_keys = [k for k in re.findall(r'GEMINI_API_KEY.*?=([^\s]+)', env_text) if k]
gemini_client = genai.Client(api_key=gemini_keys[0]) if gemini_keys else None

def sanitize_float(value):
    if value is None: return None
    if isinstance(value, (int, float)): return float(value)
    if isinstance(value, str):
        m = re.search(r'-?\d+\.?\d*', value)
        if m: return float(m.group())
    return None

def extract_properties(markdown, name):
    schema = '{"density":null,"tensile_strength_min":null,"yield_strength_min":null,"elongation":null,"hardness":null,"elastic_modulus":null,"thermal_conductivity":null,"specific_heat":null,"melting_point_min":null,"composition":"","description":""}'
    prompt = f"""System Instruction: Output JSON matching exactly: {schema}
Rules:
- density in g/cm3
- tensile_strength_min, yield_strength_min, elastic_modulus in MPa (convert from ksi: multiply by 6.895)
- thermal_conductivity in W/(m*K) (convert from BTU/ft-hr-F: multiply by 1.731)
- specific_heat in J/(kg*K)
- melting_point_min in Celsius (convert from F: (F-32)*5/9)
- elongation as percentage number only
- hardness as string with units e.g. "36 HRC"
- composition as comma-separated string of elements with percentages
- description: 1-2 sentence summary of key applications
- For ranges, use the MINIMUM value for _min fields

User Task: Extract numerical properties for '{name}' ONLY. Ignore data for other alloys in the document. Return JSON ONLY. Null if not found.
TEXT: {markdown[:20000]}"""
    
    r = gemini_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1)
    )
    return json.loads(r.text)

# Step 1: Scrape the RTI/RMI guide once (used for items 4, 6, 9)
print("Step 1: Scraping RTI/RMI Titanium Alloy Guide PDF...")
rti_md = ""
rti_url = "https://www-eng.lbl.gov/~shuman/NEXT/MATERIALS&COMPONENTS/Pressure_vessels/tiguideWeb.pdf"
try:
    res = firecrawl_app.scrape_url(rti_url)
    rti_md = res.get('markdown', '') if isinstance(res, dict) else res.markdown
    print(f"  RTI Guide scraped: {len(rti_md)} chars")
except Exception as e:
    print(f"  RTI Guide scrape failed: {e}")

time.sleep(3)

# Step 2: Scrape the Aubert & Duval direct PDF (item 10)
print("\nStep 2: Scraping Aubert & Duval Ti5553 direct PDF...")
ad_md = ""
ad_url = "https://www.aubertduval.com/wp-content/uploads/2024/12/Ti5553_GB.pdf"
try:
    res = firecrawl_app.scrape_url(ad_url)
    ad_md = res.get('markdown', '') if isinstance(res, dict) else res.markdown
    print(f"  A&D Ti5553 scraped: {len(ad_md)} chars")
except Exception as e:
    print(f"  A&D Ti5553 scrape failed: {e}")

time.sleep(3)

# Step 3: Scrape the US Patent PDF (item 11)
print("\nStep 3: Scraping US Patent 8,876,992 PDF...")
patent_md = ""
patent_url = "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8876992"
try:
    res = firecrawl_app.scrape_url(patent_url)
    patent_md = res.get('markdown', '') if isinstance(res, dict) else res.markdown
    print(f"  Patent scraped: {len(patent_md)} chars")
except Exception as e:
    print(f"  Patent scrape failed: {e}")

# Now process the 5 sparse materials
updates = [
    {"name": "Ti-6Al-6V-2Sn", "md": rti_md, "url": rti_url, "source_name": "RTI/RMI Titanium Alloy Guide"},
    {"name": "Ti-6Al-7Nb", "md": rti_md, "url": rti_url, "source_name": "RTI/RMI Titanium Alloy Guide"},
    {"name": "Ti-3Al-8V-6Cr-4Mo-4Zr (Beta C)", "md": rti_md, "url": rti_url, "source_name": "RTI/RMI Titanium Alloy Guide"},
    {"name": "Ti-5Al-5V-5Mo-3Cr (Ti-5553)", "md": ad_md, "url": ad_url, "source_name": "Aubert & Duval (Manufacturer)"},
    {"name": "Gamma TiAl (Ti-48Al-2Cr-2Nb)", "md": patent_md, "url": patent_url, "source_name": "US Patent 8,876,992 (GE Aviation)"},
]

print("\n\nStep 4: Extracting properties and updating database...")
for item in updates:
    print(f"\n[*] {item['name']}")
    
    if not item['md'] or len(item['md']) < 50:
        print("  => SKIPPED (no content scraped)")
        continue
    
    try:
        data = extract_properties(item['md'], item['name'])
        payload = {'source_url': item['url'], 'source_name': item['source_name']}
        filled = 0
        for k, v in data.items():
            if v is None or str(v).strip() in ("", "null"): continue
            if k in ['density', 'tensile_strength_min', 'yield_strength_min', 'elastic_modulus',
                      'thermal_conductivity', 'specific_heat', 'melting_point_min', 'elongation']:
                s = sanitize_float(v)
                if s is not None:
                    payload[k] = s
                    filled += 1
            elif k in ['hardness', 'composition', 'description']:
                payload[k] = str(v)
                filled += 1
        
        print(f"  Extracted {filled} fields")
        
        # Update existing record
        res = supabase.table('materials').select('id').eq('name', item['name']).execute()
        if res.data:
            supabase.table('materials').update(payload).eq('id', res.data[0]['id']).execute()
            print(f"  => Updated: {item['name']}")
        else:
            print(f"  => NOT FOUND in DB (skipping)")
        
    except Exception as e:
        print(f"  => FAILED: {e}")
    
    time.sleep(3)

print("\nBatch 5 update complete!")
