import os
import json
import time  # <-- Added so Python can pause
from firecrawl import FirecrawlApp
from google import genai
from google.genai import types
from supabase import create_client, Client
from pydantic import BaseModel, Field
from typing import Optional, List
from dotenv import load_dotenv

# 1. Load keys from the .env file automatically
load_dotenv()

# 2. Initialize API Clients
firecrawl_app = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 3. Define the exact structure Gemini must return
class MaterialSchema(BaseModel):
    name: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    source_url: str = Field(description="The URL of the source")
    composition: Optional[str] = None
    crystal_structure: Optional[str] = None
    
    # Core Mechanical Properties
    density: Optional[float] = Field(description="Density in g/cm3")
    yield_strength_min: Optional[float] = Field(description="Minimum Yield strength in MPa")
    yield_strength_max: Optional[float] = Field(description="Maximum Yield strength in MPa")
    tensile_strength_min: Optional[float] = Field(description="Minimum Tensile strength in MPa")
    tensile_strength_max: Optional[float] = Field(description="Maximum Tensile strength in MPa")
    elongation: Optional[float] = Field(description="Elongation at break in %")
    elastic_modulus: Optional[float] = Field(description="Elastic modulus in GPa")
    poissons_ratio: Optional[float] = Field(description="Poisson's ratio (dimensionless)")
    fatigue_strength: Optional[float] = Field(description="Fatigue strength in MPa")
    shear_modulus: Optional[float] = Field(description="Shear modulus in GPa")
    compressive_strength: Optional[float] = Field(description="Compressive strength in MPa")
    fracture_toughness: Optional[float] = Field(description="Fracture toughness in MPa√m")
    impact_strength: Optional[float] = Field(description="Impact strength in J/m")
    weldability: Optional[str] = Field(description="Weldability description")
    hardness: Optional[str] = None
    
    # Thermal & Environmental Properties
    max_service_temp: Optional[str] = Field(description="Max operating temperature in Celsius")
    thermal_conductivity: Optional[float] = Field(description="Thermal conductivity in W/mK")
    thermal_expansion_coefficient: Optional[float] = Field(description="Thermal expansion coefficient in 1/K")
    specific_heat: Optional[float] = Field(description="Specific heat in J/kgK")
    creep_strength: Optional[float] = Field(description="Creep strength in MPa")
    corrosion_resistance: Optional[str] = Field(description="Corrosion resistance description")
    melting_point_min: Optional[float] = Field(description="Minimum melting point in Celsius")
    melting_point_max: Optional[float] = Field(description="Maximum melting point in Celsius")
    
    # Electrical Properties and Magnetic Properties
    electrical_resistivity: Optional[float] = Field(description="Electrical resistivity in ohm·m")
    electrical_conductivity: Optional[float] = Field(description="Electrical conductivity in S/m")
    magnetic_permeability: Optional[float] = Field(description="Magnetic permeability in H/m")

    # Sustainability & Environmental Impact
    embodied_carbon: Optional[float] = Field(description="Embodied carbon in kg CO2/kg")
    machinability_rating: Optional[float] = Field(description="Machinability rating (0-100)")
    recyclability_index: Optional[float] = Field(description="Recyclability index (0-1)")
    biocompatibility: Optional[str] = Field(description="Biocompatibility description")
    
    # Pricing
    cost_per_kg_min: Optional[float] = Field(description="Minimum cost per kg in rupees")
    cost_per_kg_max: Optional[float] = Field(description="Maximum cost per kg in rupees")
    cost_currency: Optional[str] = Field(description="Currency of cost, e.g. INR, USD")

    # Standards & Identifiers
    standard: Optional[str] = Field(description="e.g. ISO 19062")
    grade: Optional[str] = Field(description="e.g. ABS")
    equivalent_grades: Optional[List[str]] = []
    uns_number: Optional[str] = Field(description="UNS number")
    en_number: Optional[str] = Field(description="EN number")
    jis_number: Optional[str] = Field(description="JIS number")
    din_number: Optional[str] = Field(description="DIN number")
    is_number: Optional[str] = Field(description="IS number")
    gb_number: Optional[str] = Field(description="GB number")

    # Applications
    applications: Optional[List[str]] = Field(description="List of common applications for this material")

    # Description & Meta
    description: Optional[str] = Field(description="A brief description of the material")
    source_name: Optional[str] = Field(description="The name of the source website, e.g. 'MakeItFrom'")
    is_verified: Optional[bool] = Field(description="Whether the source is a verified engineering source")
    is_obsolete: Optional[bool] = Field(description="Whether the material is considered obsolete or outdated")
    replacement_standard: Optional[str] = Field(description="If the material is obsolete, the standard that replaces it")
    data_type: Optional[str] = Field(description="The type of data, e.g. 'experimental', 'computational', 'manufacturer-provided'")
    verification_count: Optional[int] = Field(description="Number of independent verifications of this data")
    cross_validated: Optional[bool] = Field(description="Whether the data has been cross-validated with multiple sources")
    data_quality_score: Optional[float] = Field(description="A score (0-1) indicating the overall quality and reliability of the data")

def process_material_page(target_url: str):
    print(f"Scraping {target_url}...")
    
    # 4. Firecrawl extracts the raw text
    scrape_result = firecrawl_app.scrape_url(target_url)
    raw_markdown = getattr(scrape_result, "markdown", "")
    if not raw_markdown and hasattr(scrape_result, "data"):
        raw_markdown = getattr(scrape_result.data, "markdown", "")

    print("Analyzing with Gemini...")
    
    # 5. Gemini forces output into your Pydantic schema
    prompt = f"""
    Extract all engineering material properties and automatically convert units to match the requested schema exactly. 
    For the 'category' field, infer the broad category (e.g., 'Metals', 'Polymers', 'Ceramics', or 'Composites').
    Source URL: {target_url}
    
    Document:
    {raw_markdown}
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = gemini_client.models.generate_content(
                model='gemini-3.6-flash', # <--- CRITICAL: Must be exactly this
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=MaterialSchema,
                    temperature=0.1 
                ),
            )
            break  # If successful, exit the retry loop!
        except Exception as e:
            error_msg = str(e)
            # Fail instantly if the model name is wrong so we don't wait 60 seconds for nothing
            if "404" in error_msg or "NOT_FOUND" in error_msg:
                raise Exception(f"❌ MODEL ERROR: Please ensure you are using 'gemini-3.6-flash'. Details: {error_msg}")
            
            if attempt < max_retries - 1:
                print(f"⚠️ Google API is busy (Attempt {attempt + 1}/{max_retries}). Waiting 60 seconds...")
                time.sleep(60)
            else:
                print("❌ Google API failed after 3 attempts.")
                raise e

    # Parse the JSON string returned by Gemini into a Python dictionary
    material_data = json.loads(response.text)
    
    # 6. Push directly to Supabase
    print(f"Saving {material_data.get('name', 'Material')} to Supabase...")
    
    # Change 'upsert' to 'insert' and remove the on_conflict line
    data, count = supabase.table('materials').insert(
        material_data
    ).execute()
    
    print(f"✅ Success! Data sent to Supabase.")

if __name__ == "__main__":
    # A list of verified engineering materials to scrape
    target_urls = [
        "https://www.makeitfrom.com/material/Extruded-Acrylonitrile-Butadiene-Styrene-ABS",
        "https://www.makeitfrom.com/material/6061-T6-Aluminum",
        "https://www.makeitfrom.com/material/304-Stainless-Steel",
        "https://www.makeitfrom.com/material/Polycarbonate-PC"
    ]
    
    print(f"🚀 Starting batch job for {len(target_urls)} materials...")
    
    successful = 0
    failed = 0
    
    for url in target_urls:
        try:
            process_material_page(url)
            successful += 1
        except Exception as e:
            print(f"❌ Failed to process {url}. Error: {str(e)}")
            failed += 1
            
        # UPDATED: Wait 60 seconds before scraping the next URL in the list
        print("⏳ Waiting 60 seconds to respect Google's free-tier rate limits...\n")
        time.sleep(60)
        
    print(f"🏁 Batch complete! Successfully added: {successful} | Failed: {failed}")