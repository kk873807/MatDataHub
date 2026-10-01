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
- thermal_conductivity in W/(m*K) (convert from BTU: multiply by 1.731)
- specific_heat in J/(kg*K)
- melting_point_min in Celsius (convert from F: (F-32)*5/9)
- elongation as percentage number only
- hardness as string with units e.g. "36 HRC"
- composition as comma-separated string of elements with percentages
- description: 1-2 sentence summary of key applications

User Task: Extract numerical properties for '{name}'. Return JSON ONLY. Null if not found.
TEXT: {markdown[:15000]}"""
    
    r = gemini_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1)
    )
    return json.loads(r.text)

batch_5 = [
    {"name": "Ti-8Al-1Mo-1V", "cat": "Titanium", "sub": "Near-Alpha Titanium Alloy",
     "url": "https://www.timet.com/documents/datasheets/near-alpha-alloys/timetal-811.pdf",
     "source_name": "TIMET (Manufacturer)"},
    {"name": "Ti-6Al-2Sn-4Zr-2Mo (Ti-6242)", "cat": "Titanium", "sub": "Near-Alpha Titanium Alloy",
     "url": "https://www.timet.com/assets/local/documents/datasheets/alphaalloys/6242.pdf",
     "source_name": "TIMET (Manufacturer)"},
    {"name": "IMI 834", "cat": "Titanium", "sub": "Near-Alpha Titanium Alloy",
     "url": "https://www.timet.com/documents/datasheets/near-alpha-alloys/timetal-834.pdf",
     "source_name": "TIMET (Manufacturer)"},
    {"name": "Ti-6Al-6V-2Sn", "cat": "Titanium", "sub": "Alpha-Beta Titanium Alloy",
     "url": "https://carpentertechnology.com/alloy-finder/ti-6al-6v-2sn",
     "source_name": "Carpenter Technology (Manufacturer)"},
    {"name": "Ti-6Al-2Sn-4Zr-6Mo (Ti-6246)", "cat": "Titanium", "sub": "Alpha-Beta Titanium Alloy",
     "url": "https://www.timet.com/documents/datasheets/alpha-and-beta-alloys/timetal-6246.pdf",
     "source_name": "TIMET (Manufacturer)"},
    {"name": "Ti-6Al-7Nb", "cat": "Titanium", "sub": "Alpha-Beta Titanium Alloy",
     "url": "https://store.astm.org/f1295-24.html",
     "source_name": "ASTM F1295 (Standard)"},
    {"name": "Ti-10V-2Fe-3Al (Ti-10-2-3)", "cat": "Titanium", "sub": "Beta Titanium Alloy",
     "url": "https://www.timet.com/documents/datasheets/metastable-beta-alloys/timetal-10-2-3.pdf",
     "source_name": "TIMET (Manufacturer)"},
    {"name": "Ti-15V-3Cr-3Al-3Sn (Ti-15-3)", "cat": "Titanium", "sub": "Beta Titanium Alloy",
     "url": "https://www.timet.com/documents/datasheets/metastable-beta-alloys/timetal-15-3-3-3.pdf",
     "source_name": "TIMET (Manufacturer)"},
    {"name": "Ti-3Al-8V-6Cr-4Mo-4Zr (Beta C)", "cat": "Titanium", "sub": "Beta Titanium Alloy",
     "url": "https://www.carpentertechnology.com/alloy-finder/ti-3al-8v-6cr-4mo-4zr",
     "source_name": "Carpenter Technology (Manufacturer)"},
    {"name": "Ti-5Al-5V-5Mo-3Cr (Ti-5553)", "cat": "Titanium", "sub": "Beta Titanium Alloy",
     "url": "https://www.aubertduval.com/en/products/ti5553-titanium-alloys/",
     "source_name": "Aubert & Duval (Manufacturer)"},
    {"name": "Gamma TiAl (Ti-48Al-2Cr-2Nb)", "cat": "Titanium", "sub": "Titanium Aluminide",
     "url": "https://ntrs.nasa.gov/api/citations/20040028027/downloads/20040028027.pdf",
     "source_name": "NASA Technical Report"},
]

print("Processing Batch 5 (Titanium Alloys)...")
for item in batch_5:
    print(f"\n[*] {item['name']}")
    print(f"  Scraping: {item['url']}")
    
    md = ""
    try:
        res = firecrawl_app.scrape_url(item['url'])
        md = res.get('markdown', '') if isinstance(res, dict) else res.markdown
        print(f"  Scraped OK ({len(md)} chars)")
    except Exception as e:
        print(f"  Scrape failed: {e}")
    
    if not md or len(md) < 50:
        print("  => SKIPPED (no content). Will insert with URL only.")
        payload = {
            'category': item['cat'], 'subcategory': item['sub'], 'name': item['name'],
            'source_url': item['url'], 'source_name': item['source_name'], 'is_verified': True
        }
    else:
        print(f"  Extracting properties via Gemini...")
        try:
            data = extract_properties(md, item['name'])
            payload = {
                'category': item['cat'], 'subcategory': item['sub'], 'name': item['name'],
                'source_url': item['url'], 'source_name': item['source_name'], 'is_verified': True
            }
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
            print(f"  Extracted {filled} property fields")
        except Exception as e:
            print(f"  Extraction failed: {e}")
            payload = {
                'category': item['cat'], 'subcategory': item['sub'], 'name': item['name'],
                'source_url': item['url'], 'source_name': item['source_name'], 'is_verified': True
            }
    
    # Insert or update
    try:
        res = supabase.table('materials').select('id').eq('name', item['name']).execute()
        if res.data:
            supabase.table('materials').update(payload).eq('id', res.data[0]['id']).execute()
            print(f"  => Updated existing: {item['name']}")
        else:
            supabase.table('materials').insert(payload).execute()
            print(f"  => Inserted new: {item['name']}")
    except Exception as e:
        print(f"  => DB ERROR: {e}")
    
    time.sleep(3)

print("\nBatch 5 complete!")
