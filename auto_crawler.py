import os
import json
import time
import requests
from firecrawl import FirecrawlApp
from groq import Groq  # <-- Replaces google.genai
from supabase import create_client, Client
from pydantic import BaseModel, Field
from typing import Optional, List
from dotenv import load_dotenv

# Initialize Clients
load_dotenv()
firecrawl_app = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"]) # <-- Groq Client

# 3. Exact Database Schema
class MaterialSchema(BaseModel):
    name: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    source_url: str = Field(description="The URL of the source")
    composition: Optional[str] = None
    crystal_structure: Optional[str] = None
    density: Optional[float] = Field(description="Density in g/cm3")
    yield_strength_min: Optional[float] = Field(description="Minimum Yield strength in MPa")
    yield_strength_max: Optional[float] = Field(description="Maximum Yield strength in MPa")
    tensile_strength_min: Optional[float] = Field(description="Minimum Tensile strength in MPa")
    tensile_strength_max: Optional[float] = Field(description="Maximum Tensile strength in MPa")
    elongation: Optional[float] = Field(description="Elongation at break in %")
    elastic_modulus: Optional[float] = Field(description="Elastic modulus in GPa")
    poissons_ratio: Optional[float] = Field(description="Poisson's ratio")
    fatigue_strength: Optional[float] = Field(description="Fatigue strength in MPa")
    shear_modulus: Optional[float] = Field(description="Shear modulus in GPa")
    compressive_strength: Optional[float] = Field(description="Compressive strength in MPa")
    fracture_toughness: Optional[float] = Field(description="Fracture toughness in MPa√m")
    impact_strength: Optional[float] = Field(description="Impact strength in J/m")
    weldability: Optional[str] = None
    hardness: Optional[str] = None
    max_service_temp: Optional[float] = Field(description="Max operating temperature in Celsius")
    thermal_conductivity: Optional[float] = None
    thermal_expansion_coefficient: Optional[float] = None
    specific_heat: Optional[float] = None
    creep_strength: Optional[float] = None
    corrosion_resistance: Optional[str] = None
    melting_point_min: Optional[float] = None
    melting_point_max: Optional[float] = None
    electrical_resistivity: Optional[float] = None
    electrical_conductivity: Optional[float] = None
    magnetic_permeability: Optional[float] = None
    embodied_carbon: Optional[float] = Field(description="Embodied carbon in kg CO2/kg")
    machinability_rating: Optional[float] = Field(description="Machinability rating (0-100)")
    recyclability_index: Optional[float] = Field(description="Recyclability index (0-1)")
    biocompatibility: Optional[str] = Field(description="Biocompatibility description")
    cost_per_kg_min: Optional[float] = Field(description="Minimum cost per kg in INR")
    cost_per_kg_max: Optional[float] = Field(description="Maximum cost per kg in INR")
    cost_currency: Optional[str] = Field(description="Currency of cost, e.g. INR")
    standard: Optional[str] = None
    grade: Optional[str] = None
    equivalent_grades: Optional[List[str]] = []
    uns_number: Optional[str] = None
    en_number: Optional[str] = None
    jis_number: Optional[str] = None
    din_number: Optional[str] = None
    is_number: Optional[str] = None
    gb_number: Optional[str] = None
    applications: Optional[List[str]] = []
    description: Optional[str] = None
    source_name: Optional[str] = None
    is_verified: Optional[bool] = None
    is_obsolete: Optional[bool] = None
    replacement_standard: Optional[str] = None
    data_type: Optional[str] = None
    verification_count: Optional[int] = None
    cross_validated: Optional[bool] = None
    data_quality_score: Optional[float] = None

def fallback_scraper(raw_markdown, page_url):
    """Zero-AI deterministic fallback for MakeItFrom markdown tables."""
    print("⚡ AI unavailable. Using deterministic zero-AI fallback parser...")
    
    raw_name = page_url.split('/')[-1]
    material_name = raw_name.replace('-', ' ')
    data = {"name": material_name, "source_url": page_url}
    
    # Upgraded number extractor to handle commas (e.g., "1,200" -> 1200.0)
    def extract_number(val_str):
        try:
            clean_str = val_str.replace(",", "")
            return float(clean_str.split()[0])
        except (ValueError, IndexError):
            return None

    for line in raw_markdown.split('\n'):
        if "|" not in line:
            continue
            
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 2:
            continue
            
        property_name = parts[0].lower()
        raw_value = parts[1]
        
        # Mechanical Properties
        if "density" in property_name:
            data["density"] = extract_number(raw_value)
        elif "tensile strength: ultimate" in property_name:
            data["tensile_strength_max"] = extract_number(raw_value)
        elif "tensile strength: yield" in property_name:
            data["yield_strength_min"] = extract_number(raw_value)
        elif "elastic modulus" in property_name or "young's modulus" in property_name:
            data["elastic_modulus"] = extract_number(raw_value)
        elif "elongation" in property_name:
            data["elongation"] = extract_number(raw_value)
        elif "poisson" in property_name:
            data["poissons_ratio"] = extract_number(raw_value)
            
        # Thermal Properties
        elif "melting" in property_name:
            data["melting_point_max"] = extract_number(raw_value)
        elif "thermal conductivity" in property_name:
            data["thermal_conductivity"] = extract_number(raw_value)
        elif "specific heat" in property_name:
            data["specific_heat"] = extract_number(raw_value)
        elif "maximum temperature" in property_name or "service temperature" in property_name:
            data["max_service_temp"] = extract_number(raw_value)
            
        # Pricing / Cost (MakeItFrom typically lists "Base Price" or "Cost")
        elif "price" in property_name or "cost" in property_name:
            data["cost_per_kg_min"] = extract_number(raw_value)
            data["cost_currency"] = "INR"
            
    return data

def send_webhook_alert(message):
    """Sends a message to Discord or Slack."""
    webhook_url = os.environ.get("WEBHOOK_URL")
    if not webhook_url:
        return
        
    # Slack looks for 'text', Discord looks for 'content' - passing both covers either platform!
    payload = {"text": message, "content": message} 
    
    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        print(f"⚠️ Could not send webhook alert: {e}")

def map_and_scrape(target_website: str):
    print(f"🗺️ Mapping out all URLs on {target_website}...")
    
    # Phase 1: Rapidly grab all URLs on the website (costs no Gemini tokens)
    try:
        # FIX: We removed the `search` parameter so Firecrawl just hands us everything it finds
        map_result = firecrawl_app.map_url(target_website)
        
        # Extract links safely for Firecrawl v2
        links = getattr(map_result, "links", [])
        if not links and isinstance(map_result, dict):
            links = map_result.get("links", [])
            
        print(f"✅ Found {len(links)} total links on the website!")
    except Exception as e:
        print(f"❌ Failed to map website: {e}")
        return

    # Phase 2: Filter out the junk pages
    material_urls = []
    for link in links:
        # Extract the raw URL string whether Firecrawl returns an object, dict, or string
        if hasattr(link, "url"):
            url_str = link.url
        elif isinstance(link, dict):
            url_str = link.get("url", "")
        else:
            url_str = str(link)

        # Match material property pages while ignoring comparison and category links
        if "/material-properties/" in url_str and "/compare/" not in url_str:
            # Exclude high-level category landing pages if needed
            if url_str not in material_urls and url_str != "https://www.makeitfrom.com/material-properties/":
                material_urls.append(url_str)
                
    print(f"🎯 Filtered down to {len(material_urls)} exact material pages.")
    
    if len(material_urls) == 0:
        print("\n⚠️ No exact material pages found! Check the URL format.")
        return
        
    # Now processing ALL discovered materials
    test_batch = material_urls
    print(f"🚀 Starting batch extraction for {len(test_batch)} materials...\n")
    
    # Phase 3: Scrape and extract with Gemini
    for page_url in test_batch:
        # Inside your Phase 3 loop for each page_url:
        print(f"\nScraping {page_url}...")
        
        try:
            scrape_result = firecrawl_app.scrape_url(page_url)
            raw_markdown = getattr(scrape_result, "markdown", getattr(scrape_result, "data", {}).get("markdown", ""))
            if not raw_markdown:
                continue
        except Exception as e:
            print(f"❌ Scraping failed: {e}")
            continue

        prompt = f"Extract all engineering material properties. Automatically convert units to match the requested schema perfectly. CRITICAL INSTRUCTION: For all numerical fields, return ONLY the raw number. Do not include units. Source URL: {page_url}\n\nDocument:\n{raw_markdown}"
        
        material_data = None
        
        try:
            print("🧠 Analyzing with Groq (openai/gpt-oss-20b)...")
            # Method 1: The AI Engine
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a data extractor. Output ONLY valid JSON matching this exact schema: {MaterialSchema.model_json_schema()}"
                    },
                    {"role": "user", "content": prompt}
                ],
                model="openai/gpt-oss-20b",
                response_format={"type": "json_object"},
                temperature=0.1
            )
            material_data = json.loads(chat_completion.choices[0].message.content)
            
        except Exception as e:
            print(f"⚠️ Groq API failed or rate limited: {e}")
            # Method 3: The Instant Fallback Engine
            material_data = fallback_scraper(raw_markdown, page_url)
            
        if material_data:
            # Failsafe URL injection
            if not material_data.get("source_url") or material_data.get("source_url") == "Unknown URL":
                material_data["source_url"] = page_url
                
            print(f"💾 Saving {material_data.get('name', 'Material')} to Supabase...")
            try:
                supabase.table('materials').insert(material_data).execute()
                print(f"✅ Success!")
            except Exception as e:
                print(f"❌ Database error: {e}")
                
        print("⏳ Cooling down for 5 seconds...\n")
        time.sleep(5)

    # (This goes at the very end of the map_and_scrape function)
    print("🏁 Map & Scrape batch complete!")
    
    # Trigger the alert to your phone/desktop
    send_webhook_alert(f"✅ Mat Data Hub Update: Successfully processed {len(test_batch)} materials!")

if __name__ == "__main__":
    target = "https://www.makeitfrom.com"
    map_and_scrape(target)