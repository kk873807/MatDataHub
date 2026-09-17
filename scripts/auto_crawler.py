import os
import json
import time
from firecrawl import FirecrawlApp
from groq import Groq
from google import genai
from google.genai import types
from openai import OpenAI
from supabase import create_client, Client
from pydantic import BaseModel, Field
from typing import Optional, List
from dotenv import load_dotenv

# Initialize Clients
load_dotenv()
firecrawl_app = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"]) 
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Exact Database Schema
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
    equivalent_grades: Optional[List[str]] = Field(default_factory=list)
    uns_number: Optional[str] = None
    en_number: Optional[str] = None
    jis_number: Optional[str] = None
    din_number: Optional[str] = None
    is_number: Optional[str] = None
    gb_number: Optional[str] = None
    applications: Optional[List[str]] = Field(default_factory=list)
    description: Optional[str] = None
    source_name: Optional[str] = None
    is_verified: Optional[bool] = None
    is_obsolete: Optional[bool] = None
    replacement_standard: Optional[str] = None
    data_type: Optional[str] = None
    verification_count: Optional[int] = None
    cross_validated: Optional[bool] = None
    data_quality_score: Optional[float] = None
    extraction_method: Optional[str] = None  # FIX: Added missing field to track the AI used


def fallback_scraper(raw_markdown, page_url):
    """Zero-AI deterministic fallback for MakeItFrom markdown tables."""
    print("⚡ AI unavailable. Using deterministic zero-AI fallback parser...")
    
    raw_name = page_url.split('/')[-1].replace('.ashx', '')
    material_name = raw_name.replace('-', ' ')
    
    # Default categorizations based on source
    category = "Metal" if "aalco.co.uk" in page_url else None
    subcategory = "Aluminum Alloy" if "aalco.co.uk" in page_url and "Aluminium" in page_url else None
    
    data = {
        "name": material_name, 
        "source_url": page_url,
        "category": category,
        "subcategory": subcategory
    }
    
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
        
        if "density" in property_name:
            data["density"] = extract_number(raw_value)
        elif "tensile strength" in property_name and "ultimate" in property_name:
            data["tensile_strength_max"] = extract_number(raw_value)
        elif "tensile strength" in property_name: # Aalco
            data["tensile_strength_max"] = extract_number(raw_value)
        elif "tensile strength: yield" in property_name or "proof stress" in property_name:
            data["yield_strength_min"] = extract_number(raw_value)
        elif "elastic modulus" in property_name or "young's modulus" in property_name or "modulus of elasticity" in property_name:
            data["elastic_modulus"] = extract_number(raw_value)
        elif "elongation" in property_name:
            data["elongation"] = extract_number(raw_value)
        elif "poisson" in property_name:
            data["poissons_ratio"] = extract_number(raw_value)
        elif "melting" in property_name:
            data["melting_point_max"] = extract_number(raw_value)
        elif "thermal conductivity" in property_name:
            data["thermal_conductivity"] = extract_number(raw_value)
        elif "specific heat" in property_name:
            data["specific_heat"] = extract_number(raw_value)
        elif "maximum temperature" in property_name or "service temperature" in property_name:
            data["max_service_temp"] = extract_number(raw_value)
        elif "price" in property_name or "cost" in property_name:
            data["cost_per_kg_min"] = extract_number(raw_value)
            data["cost_currency"] = "INR"
        elif "hardness brinell" in property_name:
            data["hardness"] = f"{extract_number(raw_value)} HB"
            
    return data


def process_single_material(page_url, max_retries=3):
    """Core logic to scrape, extract, and save a single URL with automatic retries."""
    print(f"\nScraping {page_url}...")
    
    material_data = None
    
    # The Retry Loop: Attempts the whole process up to 'max_retries' times
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"🔄 Retrying {page_url} (Attempt {attempt + 1} of {max_retries})...")
                
            # 1. Scrape with Firecrawl
            scrape_result = firecrawl_app.scrape_url(page_url)
            raw_markdown = getattr(scrape_result, "markdown", getattr(scrape_result, "data", {}).get("markdown", ""))
            
            if not raw_markdown:
                print("❌ No markdown extracted.")
                if attempt < max_retries - 1:
                    time.sleep(10)
                    continue  # Skips to the next attempt
                return
                
            # 1.5 Extract metadata safely
            metadata = getattr(scrape_result, "metadata", getattr(scrape_result, "data", {}).get("metadata", {}))
            
            if hasattr(metadata, "title") and metadata.title:
                page_title = metadata.title
            elif isinstance(metadata, dict):
                page_title = metadata.get("title", "Unknown Webpage")
            else:
                page_title = "Unknown Webpage"
            
            prompt = f"""Extract all engineering material properties. Automatically convert units to match the requested schema perfectly.
            
            CRITICAL INSTRUCTION 1: The 'name' field is mandatory. The webpage title is "{page_title}". Use this title and the main document header to determine the exact material name. Never use 'Unknown Material'.
            CRITICAL INSTRUCTION 2: For all numerical fields, return ONLY the raw number. Do not include units. 
            CRITICAL INSTRUCTION 3: DATA DISAMBIGUATION. If the document lists multiple values... always extract the properties for the "Annealed", "Base", or most standard unmodified condition.
            
            Source URL: {page_url}
            
            Document:
            {raw_markdown}"""
            
            # --- THE AI WATERFALL ---
            try:
                print("🧠 Analyzing with Groq...")
                chat_completion = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"You are a data extractor. Output ONLY valid JSON matching this exact schema: {MaterialSchema.model_json_schema()}"},
                        {"role": "user", "content": prompt}
                    ],
                    model="openai/gpt-oss-20b",
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                material_data = json.loads(chat_completion.choices[0].message.content)
                material_data["extraction_method"] = "Groq"
                
            except Exception as e1:
                print(f"⚠️ Groq API failed (Limit Reached).")
                try:
                    print("🧠 Groq failed. Falling back to Gemini Backup AI...")
                    response = gemini_client.models.generate_content(
                        model='gemini-3.6-flash',  # FIX: Updated to active model
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=MaterialSchema,
                            temperature=0.1 
                        ),
                    )
                    material_data = json.loads(response.text)
                    material_data["extraction_method"] = "Gemini"
                    
                except Exception as e2:
                    print(f"⚠️ Gemini API failed (Limit Reached).")
                    try:
                        print("🧠 Gemini failed. Falling back to OpenAI (gpt-4o-mini)...")
                        response = openai_client.chat.completions.create(
                            model="gpt-4o-mini",
                            response_format={"type": "json_object"},
                            messages=[
                                {"role": "system", "content": f"You are a data extractor. Output ONLY valid JSON matching this exact schema: {MaterialSchema.model_json_schema()}"},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.1
                        )
                        material_data = json.loads(response.choices[0].message.content)
                        material_data["extraction_method"] = "OpenAI"

                    except Exception as e3:
                        print(f"⚠️ OpenAI API failed (Limit Reached).")
                        if "makeitfrom.com" in page_url or "aalco.co.uk" in page_url:
                            material_data = fallback_scraper(raw_markdown, page_url)
                            material_data["extraction_method"] = "Deterministic Parser"
                        else:
                            print("❌ All 3 AIs failed, and deterministic fallback cannot read random sources.")
            # --- END WATERFALL ---
            
            # If we successfully got data, BREAK out of the retry loop immediately!
            if material_data:
                break
                
        except Exception as e:
            print(f"❌ Error during attempt {attempt + 1}: {e}")
            
        # If we reach here, it means material_data is still None or an error occurred.
        if attempt < max_retries - 1:
            print("⏳ AI rate limit hit. Waiting 65 seconds for quotas to reset before retrying...")
            time.sleep(65)
            
    # 4. Save to Supabase (Only executes once the loop is finished)
    if material_data:
        if not material_data.get("source_url") or material_data.get("source_url") == "Unknown URL":
            material_data["source_url"] = page_url
            
        if not material_data.get("name") or material_data.get("name") == "Unknown Material":
            material_data["name"] = page_title.split(" - ")[0] 
            
        print(f"💾 Saving {material_data.get('name', 'Material')} to Supabase...")
        try:
            # Check if URL exists first since on_conflict requires a DB constraint
            existing = supabase.table('materials').select('id').eq('source_url', material_data['source_url']).execute()
            if existing.data:
                # Update existing
                supabase.table('materials').update(material_data).eq('id', existing.data[0]['id']).execute()
                print(f"✅ Success! (Updated existing data extracted via Groq/Gemini)")
            else:
                # Insert new
                supabase.table('materials').insert(material_data).execute()
                print(f"✅ Success! (Inserted new data extracted via Groq/Gemini)")
        except Exception as e:
            print(f"❌ Database error: {e}")
    else:
        print(f"⏭️ Skipping {page_url} after {max_retries} failed attempts.")
        
    print("⏳ Cooling down for 15 seconds before the next material...")
    time.sleep(15)


# ------------------------------------------------------------------
# Interactive Menu
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🚀 Mat Data Hub - Auto Crawler Menu")
    print("=" * 50)
    print("1. Map a website and extract a batch of materials")
    print("2. Extract specific material URLs manually")
    print("=" * 50)
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        target = input("\nEnter target website (e.g., https://www.makeitfrom.com): ").strip()
        batch_size = input("Enter batch size (how many to scrape? Press Enter to scrape ALL): ").strip()
        
        print(f"\n🗺️ Mapping out all URLs on {target}...")
        try:
            map_result = firecrawl_app.map_url(target)
            links = getattr(map_result, "links", [])
            if not links and isinstance(map_result, dict):
                links = map_result.get("links", [])
            print(f"✅ Found {len(links)} total links on the website!")
        except Exception as e:
            print(f"❌ Failed to map website: {e}")
            links = []

        material_urls = []
        for link in links:
            url_str = link.url if hasattr(link, "url") else link.get("url", str(link)) if isinstance(link, dict) else str(link)
            
            if "matweb.com" in target:
                if "DataSheet.aspx" in url_str and url_str not in material_urls:
                    material_urls.append(url_str)
                    
            elif "makeitfrom.com" in target:
                if "/material-properties/" in url_str and "/compare/" not in url_str:
                    if url_str not in material_urls and url_str != "https://www.makeitfrom.com/material-properties/":
                        material_urls.append(url_str)
                        
            else:
                if url_str not in material_urls:
                    material_urls.append(url_str)
                    
        print(f"🎯 Filtered down to {len(material_urls)} exact material pages.")
        
        if batch_size.isdigit() and int(batch_size) > 0:
            material_urls = material_urls[:int(batch_size)]
            print(f"⚠️ Limited batch size to {batch_size} materials.")
            
        print(f"🚀 Starting batch extraction for {len(material_urls)} materials...\n")
        
        for url in material_urls:
            process_single_material(url)
            
        print("\n🏁 Map & Scrape batch complete!")

    elif choice == "2":
        print("\nEnter material URLs one by one. Type 'done' when you are finished.")
        custom_urls = []
        while True:
            url = input("URL > ").strip()
            if url.lower() == 'done':
                break
            if url:
                custom_urls.append(url)
                
        if len(custom_urls) > 0:
            print(f"\n🚀 Starting custom extraction for {len(custom_urls)} materials...")
            for url in custom_urls:
                process_single_material(url)
            print("\n🏁 Custom extraction complete!")
        else:
            print("No URLs entered. Exiting.")
            
    else:
        print("❌ Invalid choice. Please run the script again and enter 1 or 2.")