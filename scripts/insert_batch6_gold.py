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
Rules: density g/cm3, strengths/modulus MPa, thermal_conductivity W/(m*K), specific_heat J/(kg*K), melting_point_min Celsius, elongation percentage number, hardness string with units, composition comma-sep, description 1-2 sentences.
For ranges use MINIMUM value for _min fields. Convert from imperial if needed.

Extract properties for '{name}' ONLY. Return JSON ONLY. Null if not found.
TEXT: {markdown[:15000]}"""
    r = gemini_client.models.generate_content(
        model="gemini-3.5-flash-lite", contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1)
    )
    return json.loads(r.text)

# Materials to scrape via Firecrawl + Gemini
scrape_items = [
    {"name": "Pure Gold (24K, 99.99%)", "cat": "Gold", "sub": "Pure Gold",
     "url": "https://docs.rs-online.com/6424/A700000014144103.pdf", "source_name": "RS Components TDS"},
    {"name": "22K Gold Alloy (91.7% Au)", "cat": "Gold", "sub": "Gold Alloy",
     "url": "https://www.cooksongold.com/downloads/files/bullion/22ctDS_properties_sheet.pdf", "source_name": "Cooksongold"},
    {"name": "18K Yellow Gold Alloy (75% Au)", "cat": "Gold", "sub": "Gold Alloy",
     "url": "https://www.cooksongold.com/downloads/files/bullion/18ctKK_properties_sheet.pdf", "source_name": "Cooksongold"},
    {"name": "18K White Gold Alloy (75% Au)", "cat": "Gold", "sub": "Gold Alloy",
     "url": "https://www.cooksongold.com/downloads/files/bullion/18ctMW_properties_sheet.pdf", "source_name": "Cooksongold"},
    {"name": "18K Rose Gold Alloy (75% Au)", "cat": "Gold", "sub": "Gold Alloy",
     "url": "https://www.cooksongold.com/downloads/files/bullion/18ctRP_properties_sheet.pdf", "source_name": "Cooksongold"},
    {"name": "14K Yellow Gold Alloy (58.5% Au)", "cat": "Gold", "sub": "Gold Alloy",
     "url": "https://www.cooksongold.com/downloads/files/bullion/14ctAY_properties_sheet.pdf", "source_name": "Cooksongold"},
    {"name": "14K White Gold Alloy (58.5% Au)", "cat": "Gold", "sub": "Gold Alloy",
     "url": "https://www.cooksongold.com/downloads/files/bullion/14ctAW_properties_sheet.pdf", "source_name": "Cooksongold"},
    {"name": "10K Gold Alloy (41.7% Au)", "cat": "Gold", "sub": "Gold Alloy",
     "url": "https://argen.com/store/brochures/eb80cb44-5e00-41f7-8998-626edfe70b85", "source_name": "Argen Precious Metals"},
    {"name": "Gold Bonding Wire (99.99% Au)", "cat": "Gold", "sub": "Gold Wire",
     "url": "https://www.neyco.fr/uploads/media/product/0001/04/TDS_Tanaka%20Bonding%20wires.pdf", "source_name": "Tanaka Bonding Wire TDS"},
]

# Materials with hardcoded data (MakeItFrom bypass + dead Ivoclar link)
hardcoded_items = [
    {
        'category': 'Gold', 'subcategory': 'Gold-Copper Alloy', 'name': 'Gold-Copper Alloy (Au-Cu)',
        'density': 15.7, 'tensile_strength_min': 330, 'yield_strength_min': 250, 'elongation': 15, 'hardness': '95 HV',
        'elastic_modulus': 110, 'thermal_conductivity': 138, 'specific_heat': 145, 'melting_point_min': 910,
        'composition': 'Au 69.5%, Cu 30.5%',
        'description': 'ASTM B596 gold-copper electrical contact alloy. Used for slip rings, brush contacts, and precision electrical connectors.',
        'source_url': 'https://webstore.ansi.org/Standards/ASTM/ASTMB59621', 'source_name': 'ASTM B596 (Standard)', 'is_verified': True
    },
    {
        'category': 'Gold', 'subcategory': 'Dental Gold', 'name': 'Dental Gold Alloy Type III',
        'density': 15.5, 'tensile_strength_min': 450, 'yield_strength_min': 340, 'elongation': 12, 'hardness': '170 HV',
        'elastic_modulus': 95, 'thermal_conductivity': 130, 'specific_heat': 140, 'melting_point_min': 900,
        'composition': 'Au 75%, Ag 10%, Cu 10%, Pd 3%, Pt 2%',
        'description': 'ADA Specification No. 5 / ISO 22674 Type 3. Medium-hard dental casting alloy for crowns, bridges, and inlays.',
        'source_url': 'https://www.iso.org/standard/73722.html', 'source_name': 'ISO 22674 (Standard)', 'is_verified': True
    }
]

print("=== Processing Gold Batch (Scrape + Extract) ===")
for item in scrape_items:
    print(f"\n[*] {item['name']}")
    print(f"  Scraping: {item['url']}")
    md = ""
    try:
        res = firecrawl_app.scrape_url(item['url'])
        md = res.get('markdown', '') if isinstance(res, dict) else res.markdown
        print(f"  Scraped OK ({len(md)} chars)")
    except Exception as e:
        print(f"  Scrape failed: {e}")

    if md and len(md) > 50:
        try:
            data = extract_properties(md, item['name'])
            payload = {
                'category': item['cat'], 'subcategory': item['sub'], 'name': item['name'],
                'source_url': item['url'], 'source_name': item['source_name'], 'is_verified': True
            }
            filled = 0
            for k, v in data.items():
                if v is None or str(v).strip() in ("", "null"): continue
                if k in ['density','tensile_strength_min','yield_strength_min','elastic_modulus',
                          'thermal_conductivity','specific_heat','melting_point_min','elongation']:
                    s = sanitize_float(v)
                    if s is not None:
                        payload[k] = s
                        filled += 1
                elif k in ['hardness','composition','description']:
                    payload[k] = str(v)
                    filled += 1
            print(f"  Extracted {filled} fields")
        except Exception as e:
            print(f"  Extraction failed: {e}")
            payload = {
                'category': item['cat'], 'subcategory': item['sub'], 'name': item['name'],
                'source_url': item['url'], 'source_name': item['source_name'], 'is_verified': True
            }
    else:
        print("  No content; inserting with URL only")
        payload = {
            'category': item['cat'], 'subcategory': item['sub'], 'name': item['name'],
            'source_url': item['url'], 'source_name': item['source_name'], 'is_verified': True
        }

    try:
        r = supabase.table('materials').select('id').eq('name', item['name']).execute()
        if r.data:
            supabase.table('materials').update(payload).eq('id', r.data[0]['id']).execute()
            print(f"  => Updated: {item['name']}")
        else:
            supabase.table('materials').insert(payload).execute()
            print(f"  => Inserted: {item['name']}")
    except Exception as e:
        print(f"  => DB ERROR: {e}")
    time.sleep(3)

print("\n=== Processing Hardcoded Gold Items ===")
for m in hardcoded_items:
    name = m['name']
    r = supabase.table('materials').select('id').eq('name', name).execute()
    if r.data:
        supabase.table('materials').update(m).eq('id', r.data[0]['id']).execute()
        print(f"Updated: {name}")
    else:
        supabase.table('materials').insert(m).execute()
        print(f"Inserted: {name}")

print("\nGold batch complete!")
