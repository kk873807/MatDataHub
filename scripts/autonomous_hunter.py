import os
import sys
import json
import time
import re
import csv
import warnings
warnings.filterwarnings('ignore')

from supabase import create_client
from dotenv import load_dotenv
import itertools
from firecrawl import FirecrawlApp

# AI Imports
from groq import Groq
from google import genai
from google.genai import types
from openai import OpenAI

from pydantic import BaseModel
from typing import Optional

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
firecrawl_app = FirecrawlApp(api_key=os.environ.get('FIRECRAWL_API_KEY'))

with open('.env', 'r', encoding='utf-8') as f:
    env_text = f.read()

# Load API Keys
groq_keys = re.findall(r'GROQ_API_KEY.*?=([^\s]+)', env_text)
gemini_keys = re.findall(r'GEMINI_API_KEY.*?=([^\s]+)', env_text)

groq_clients = [Groq(api_key=key) for key in groq_keys if key]
gemini_clients = [genai.Client(api_key=key) for key in gemini_keys if key]
gemini_cycle = itertools.cycle(gemini_clients) if gemini_clients else None

# Only create OpenAI client if a real key exists
openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
openai_client = OpenAI(api_key=openai_key) if openai_key and openai_key != "dummy_key" else None

CHECKPOINT_FILE = "hunter_checkpoint.json"
UNRESOLVED_FILE = "manual_hunt_required.csv"

# Two Gemini models with SEPARATE quota pools = 2x capacity
GEMINI_MODELS = ['gemini-3.6-flash', 'gemini-3.5-flash-lite']

# Only these columns exist in the Supabase 'materials' table
VALID_DB_COLUMNS = {
    'category', 'subcategory', 'grade', 'standard',
    'density', 'tensile_strength_min', 'tensile_strength_max',
    'yield_strength_min', 'yield_strength_max', 'elongation',
    'hardness', 'elastic_modulus',
    'thermal_conductivity', 'specific_heat',
    'melting_point_min', 'melting_point_max', 'max_service_temp',
    'cost_per_kg_min', 'cost_per_kg_max', 'cost_currency',
    'applications', 'equivalent_grades', 'composition', 'description',
    'source_url', 'source_name', 'extraction_method', 'is_verified',
}

# Float columns that must be pure numbers (no units like "7.6 g/cm³")
FLOAT_COLUMNS = {
    'density', 'tensile_strength_min', 'tensile_strength_max',
    'yield_strength_min', 'yield_strength_max', 'elongation',
    'elastic_modulus', 'thermal_conductivity', 'specific_heat',
    'melting_point_min', 'melting_point_max', 'max_service_temp',
    'cost_per_kg_min', 'cost_per_kg_max',
}

def sanitize_float(value):
    """Extract a pure number from strings like '7.6 g/cm³' or '215 MPa'."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        # Extract the first number (including decimals and negatives)
        match = re.search(r'-?\d+\.?\d*', value)
        if match:
            return float(match.group())
    return None

def log_unresolved(mat_id, mat_name, reason):
    """Logs skipped materials to a CSV for manual hunting later."""
    file_exists = os.path.exists(UNRESOLVED_FILE)
    with open(UNRESOLVED_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["ID", "Material Name", "Reason"])
        writer.writerow([mat_id, mat_name, reason])

# ==========================================
# 2. SCHEMA DEFINITION
# ==========================================
class MaterialSchema(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    density: Optional[float] = None
    yield_strength_min: Optional[float] = None
    tensile_strength_min: Optional[float] = None
    elongation_min: Optional[float] = None
    elastic_modulus: Optional[float] = None
    hardness: Optional[float] = None
    melting_point_min: Optional[float] = None
    melting_point_max: Optional[float] = None
    thermal_conductivity: Optional[float] = None
    specific_heat: Optional[float] = None
    electrical_resistivity: Optional[float] = None
    magnetic_permeability: Optional[float] = None

# ==========================================
# 3. SEARCH ENGINE (FIRECRAWL SEARCH)
# ==========================================
def search_primary_source(material_name):
    """Searches the web for a primary datasheet using Firecrawl Search."""
    print(f"  🔍 Hunting web for: {material_name}...")
    
    query = f"{material_name} material properties datasheet -makeitfrom -wikipedia -researchgate"
    banned_domains = ['makeitfrom.com', 'wikipedia.org', 'researchgate.net', 'sciencedirect.com', 'kaggle.com']
    
    try:
        result = firecrawl_app.search(query)
        
        search_results = []
        if isinstance(result, list):
            search_results = result
        elif isinstance(result, dict) and 'data' in result:
            search_results = result['data']
        elif hasattr(result, 'web'):
            search_results = result.web
            
        for r in search_results:
            link = getattr(r, 'url', None)
            if not link and isinstance(r, dict):
                link = r.get('url')
            if not link: continue
            
            if any(b in link.lower() for b in banned_domains):
                continue
                
            publisher = "Primary Web Source"
            if "matweb.com" in link: publisher = "MatWeb"
            elif "azom.com" in link: publisher = "AZoM"
            elif ".pdf" in link.lower(): publisher = "Manufacturer Datasheet (PDF)"
            
            print(f"  🎯 Found Target: {link}")
            return link, publisher
            
    except Exception as e:
        print(f"  ⚠️ Search failed: {e}")
        
    return None, None

# ==========================================
# 4. AI EXTRACTION WATERFALL
# ==========================================
def extract_properties_from_markdown(markdown_text, material_name):
    """Groq -> Gemini (2 models x 7 keys = 14 attempts) -> OpenAI."""
    prompt = f"""
    Extract the material properties for '{material_name}' from the following text.
    Return a JSON object strictly matching the schema. 
    IMPORTANT: For numeric fields (density, strength, etc.), return ONLY the number, no units.
    Example: density should be 7.93 not "7.93 g/cm³"
    If a value is missing, return null.
    Convert all units to standard SI/metric (MPa for strength, g/cm³ for density, W/m·K for conductivity).

    TEXT:
    {markdown_text[:12000]}
    """
    
    # 1. Try Groq First
    try:
        if groq_clients:
            print("  🧠 Analyzing with Groq...")
            client = groq_clients[0]
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are a data extractor. Output ONLY valid JSON matching this schema: {MaterialSchema.model_json_schema()}"},
                    {"role": "user", "content": prompt}
                ],
                model="qwen/qwen3.8-27b",
                response_format={"type": "json_object"},
                temperature=0.1,
                timeout=30
            )
            material_data = json.loads(chat_completion.choices[0].message.content)
            material_data["extraction_method"] = "Groq Autonomous"
            print("  ✅ Groq succeeded!")
            return material_data
    except Exception as e:
        print(f"  ⚠️ Groq failed: {str(e)[:80]}")

    # 2. Try Gemini Rotation — 2 models x 7 keys = 14 total attempts
    print("  🧠 Falling back to Gemini Rotation...")
    if gemini_cycle and gemini_clients:
        for model_name in GEMINI_MODELS:
            for attempt in range(len(gemini_clients)):
                current_gemini = next(gemini_cycle)
                try:
                    label = f"{model_name} Key {attempt + 1}/{len(gemini_clients)}"
                    print(f"    🔄 Trying {label}...")
                    response = current_gemini.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.1,
                            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                        ),
                    )
                    material_data = json.loads(response.text)
                    material_data["extraction_method"] = "Gemini Autonomous"
                    print(f"    ✅ {label} succeeded!")
                    return material_data
                except Exception as e:
                    err_msg = str(e)[:100]
                    print(f"    ⚠️ {label} failed: {err_msg[:60]}")
                    if '404' in err_msg:
                        break  # Model not found, skip to next model
                    continue
                    
    print(f"  ⚠️ All Gemini models/keys exhausted.")

    # 3. Try OpenAI Fallback (only if real key exists)
    if openai_client:
        try:
            print("  🧠 Falling back to OpenAI (gpt-4o-mini)...")
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": f"Output ONLY valid JSON matching this schema: {MaterialSchema.model_json_schema()}"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                timeout=30
            )
            material_data = json.loads(response.choices[0].message.content)
            material_data["extraction_method"] = "OpenAI Autonomous"
            return material_data
        except Exception as e:
            print(f"  ❌ OpenAI failed: {str(e)[:80]}")
    
    raise Exception("All AIs exhausted their rate limits.")

# ==========================================
# 5. MAIN ORCHESTRATION
# ==========================================
def main():
    print("="*60)
    print("🤖 AUTONOMOUS SOURCE HUNTER & EXTRACTOR")
    print("="*60)
    
    state = {"processed_ids": []}
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except json.JSONDecodeError:
            state = {"processed_ids": []}

    print("Fetching targets from database...")
    materials = []
    page = 0
    page_size = 1000
    while True:
        res = supabase.table('materials').select('id, name, source_url').ilike('source_url', '%makeitfrom%').range(page * page_size, (page + 1) * page_size - 1).execute()
        if not res.data: break
        materials.extend(res.data)
        if len(res.data) < page_size: break
        page += 1
        
    targets = [m for m in materials if m['id'] not in state.get('processed_ids', [])]
    print(f"Total MakeItFrom Targets: {len(materials)} | Remaining to Process: {len(targets)}")
    print(f"AI Config: Groq({'✅' if groq_clients else '❌'}) | Gemini({len(gemini_clients)} keys x {len(GEMINI_MODELS)} models) | OpenAI({'✅' if openai_client else '❌ no key'})\n")

    success_count = 0
    fail_count = 0
    consecutive_ai_fails = 0

    for i, mat in enumerate(targets, 1):
        mat_id = mat['id']
        mat_name = mat['name']
        print(f"[{i}/{len(targets)}] {mat_name}")
        
        # 1. Search for new URL
        new_url, publisher = search_primary_source(mat_name)
        
        if not new_url:
            print("  ⏭️ Could not find a primary source. Skipping.")
            log_unresolved(mat_id, mat_name, "No primary source found on web")
            state['processed_ids'].append(mat_id)
            with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f: json.dump(state, f)
            fail_count += 1
            consecutive_ai_fails = 0
            time.sleep(6)  # Increased to respect 10 req/min Firecrawl limit
            continue
            
        # 2. Scrape with Firecrawl
        try:
            print(f"  🕷️ Scraping {new_url} via Firecrawl...")
            scrape_res = firecrawl_app.scrape_url(new_url)
            
            if hasattr(scrape_res, 'markdown') and scrape_res.markdown:
                markdown_content = scrape_res.markdown
            elif isinstance(scrape_res, dict):
                markdown_content = scrape_res.get('markdown', scrape_res.get('data', {}).get('markdown', ''))
            else:
                markdown_content = str(scrape_res)
                
            if not markdown_content or len(markdown_content) < 50:
                raise Exception("Empty or invalid scrape.")
        except Exception as e:
            print(f"  ⚠️ Scrape failed: {e}. Skipping.")
            log_unresolved(mat_id, mat_name, f"Scrape failed: {e}")
            state['processed_ids'].append(mat_id)
            with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f: json.dump(state, f)
            fail_count += 1
            consecutive_ai_fails = 0
            time.sleep(2)
            continue
            
        # 3. AI Extraction
        try:
            extracted_data = extract_properties_from_markdown(markdown_content, mat_name)
            
            # Only keep non-null values that match actual DB columns
            clean_data = {}
            for k, v in extracted_data.items():
                if v is None or k not in VALID_DB_COLUMNS:
                    continue
                # Sanitize float columns to strip units like "7.6 g/cm³"
                if k in FLOAT_COLUMNS:
                    sanitized = sanitize_float(v)
                    if sanitized is not None:
                        clean_data[k] = sanitized
                else:
                    clean_data[k] = v
            
            clean_data['source_url'] = new_url
            clean_data['source_name'] = f"{publisher} (AI Extracted)"
            
            print(f"  💾 Updating database ({len(clean_data)} fields)...")
            supabase.table('materials').update(clean_data).eq('id', mat_id).execute()
            print("  ✅ Success! Replaced MakeItFrom with Primary Source.")
            success_count += 1
            consecutive_ai_fails = 0
            
        except Exception as e:
            if "All AIs exhausted" in str(e):
                consecutive_ai_fails += 1
                wait_time = min(60 * consecutive_ai_fails, 300)  # Scale up: 60s, 120s, 180s... max 5min
                print(f"  ⏳ All AI quotas exhausted! Sleeping {wait_time}s (attempt {consecutive_ai_fails})...")
                time.sleep(wait_time)
                continue  # Retry this material
            else:
                print(f"  ⚠️ Extraction/Update failed: {e}")
                log_unresolved(mat_id, mat_name, f"Extraction failed: {e}")
                fail_count += 1
                consecutive_ai_fails = 0
                
        # Save Checkpoint & Cooldown
        state['processed_ids'].append(mat_id)
        with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f: json.dump(state, f)
        
        print(f"  ⏳ Cooldown 6s... [Session: ✅{success_count} ❌{fail_count}]\n")
        time.sleep(6)  # 6s guarantees max 10 iterations/min (20 requests/min max)

    print("\n" + "="*60)
    print(f"SESSION COMPLETE — ✅ Success: {success_count} | ❌ Failed: {fail_count}")
    print("="*60)

if __name__ == "__main__":
    main()
