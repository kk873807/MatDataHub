# End-to-End Guide: Manually Seeding Materials into MatDataHub

This guide is designed for absolute beginners. If you ever run out of credits here, you can use any free AI chat (like ChatGPT, Claude, or Gemini) to extract data from a website, and then manually run a script on your computer to put that data into your live website. 

Because your project uses a **Supabase Cloud Database**, any data you add from your local computer will *instantly* show up on your live Vercel frontend.

---

## Step 1: Extract Data using a Free AI Agent

Go to any free AI agent. Copy and paste the exact prompt below, replacing the `[INSERT URL]` with the material page you want to scrape.

**Prompt to copy-paste into the AI:**
```text
Please read the material properties from this URL: [INSERT URL]

Extract the data and format it EXACTLY as a Python dictionary matching this database schema. 
CRITICAL RULES:
1. Do not invent data. If a field is missing on the page, omit it or use None.
2. Density MUST be in g/cm³.
3. Temperatures MUST be in °C.
4. Strengths MUST be in MPa.
5. Provide ONLY the Python dictionary code block.

Format template:
{
    "name": "Material Name (Grade)",
    "category": "Metal", # or Polymer, Ceramic, etc.
    "subcategory": "Aluminum Alloy", # or Stainless Steel, etc.
    "grade": "Grade",
    "standard": "Standard info",
    "density": 0.0,
    "tensile_strength_min": 0.0,
    "tensile_strength_max": 0.0,
    "yield_strength_min": 0.0,
    "yield_strength_max": 0.0,
    "elastic_modulus": 0.0, # in GPa
    "hardness": "String value like 20-45 HB",
    "thermal_conductivity": 0.0,
    "specific_heat": 0.0,
    "melting_point_min": 0.0,
    "melting_point_max": 0.0,
    "max_service_temp": 0.0,
    "embodied_carbon": 0.0,
    "composition": "Chemical composition string",
    "equivalent_grades": "Equivalent grades string",
    "source_url": "[INSERT URL]",
    "source_name": "Website Name",
    "is_verified": True
}
```

---

## Step 2: Create a New Seed Script

Once the AI gives you the Python dictionaries, you need to create a script in your project to push them to the database.

1. Open your code editor (VS Code).
2. Go to the `scripts/` folder inside `MatDataHub`.
3. Create a new file, for example: `scripts/seed_new_materials.py`.
4. Copy and paste the foolproof template below into that file.

```python
import os
import sys

# Connect to your MatDataHub backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models import Material, MaterialSource

# ==========================================
# PASTE THE AI-GENERATED DICTIONARIES HERE:
# ==========================================
materials_data = [
    {
        # Example data (Replace this entire block with the AI output)
        "name": "Example Material",
        "category": "Metal",
        "subcategory": "Steel",
        "density": 7.85,
        "source_url": "https://example.com",
        "source_name": "Example Source",
        "is_verified": True
    }
]
# ==========================================

def run_seed():
    db = SessionLocal()
    added = 0
    skipped = 0

    for data in materials_data:
        # 1. Check if it already exists to prevent duplicates
        exists = db.query(Material).filter(Material.name == data["name"]).first()
        if exists:
            skipped += 1
            print(f"  [>>] Skipped (already exists): {data['name']}")
            continue

        # 2. Extract source info safely
        source_url = data.get("source_url")
        source_name_val = data.get("source_name", "Web Data")

        # 3. Add to Materials table
        mat = Material(**data)
        db.add(mat)
        db.flush() # Gets the new ID before fully saving

        # 4. Add to MaterialSources table (for UI/UX "Verified" links)
        if source_url:
            src = MaterialSource(
                material_id=mat.id,
                source_type="database",
                source_name=source_name_val,
                source_url=source_url,
                access_type="free",
                confidence_score=0.9,
                notes="Manually seeded material",
            )
            db.add(src)

        added += 1
        print(f"  [+] Added: {data['name']}")

    # 5. Save everything to Supabase
    db.commit()
    db.close()
    
    print(f"\n==================================================")
    print(f"  Total added:   {added}")
    print(f"  Total skipped: {skipped}")
    print(f"==================================================")
    return added

if __name__ == "__main__":
    print("[SEED] Starting manual material seed...")
    run_seed()
    print("[DONE] Script finished.")
```

> [!CAUTION]
> Make sure you are pasting the AI's dictionaries exactly inside the `materials_data = [ ... ]` brackets. Do not alter the indentation.

---

## Step 3: Run the Script Locally

You run this script on your computer, but because your `.env` file points to Supabase, it updates the live database.

1. Open a new Terminal in VS Code (`Ctrl` + `\`` or `Terminal > New Terminal`).
2. Ensure you are in the `MatDataHub` directory.
3. **Activate your virtual environment** (Crucial for Windows):
   ```powershell
   .venv\Scripts\activate
   ```
4. **Run the script**:
   ```powershell
   python scripts/seed_new_materials.py
   ```

You should see output saying `[+] Added: ...`. 
**Congratulations! The materials are now permanently in your live database.** Check your live Vercel website; they will already be on the materials tab.

---

## Step 4: Save your work to GitHub

Even though the database is already updated, you should save the script you just wrote to GitHub so your codebase is up to date.

In the VS Code terminal, run these commands one by one:

```powershell
git add .
git commit -m "feat: added manual seed script for new materials"
git push
```

---

## Step 5 (Optional): Expose an API Endpoint 

If you ever want to trigger this script remotely (e.g., via a URL rather than running a Python command), you can add an endpoint in `app/main.py`.

1. Open `app/main.py`.
2. Scroll to the bottom, right above `from app.routers import blogs`.
3. Add this code block:

```python
@app.get("/api/v1/admin/seed-new-materials")
def seed_new_materials_data():
    try:
        from scripts.seed_new_materials import run_seed
        added = run_seed()
        return {"ok": True, "message": f"Successfully seeded {added} materials!"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
```

Now, if you commit and push this, Vercel/Render will rebuild your backend. Once deployed, you could just visit `https://your-backend-url.onrender.com/api/v1/admin/seed-new-materials` in your browser to run the script remotely!

---

### Summary Checklist to Prevent Errors:
- [ ] Did you use the exact prompt schema to ask the AI?
- [ ] Is your virtual environment (`.venv\Scripts\activate`) active before running?
- [ ] Does your `.env` file contain the correct `DATABASE_URL=postgresql://...` Supabase link? (If yes, data syncs to Vercel instantly).
- [ ] Did you avoid using emojis in `print()` statements? (Windows CMD sometimes crashes with emojis).
