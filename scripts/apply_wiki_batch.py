import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

wiki_updates = [
    # 1199 Aluminium (fixing duplicates)
    ("1199 Aluminum", "https://www.goodfellow.com/eu/1199-aluminium-coil-group", "Goodfellow (Coil)"),
    ("1199 aluminium alloy", "DELETE", ""),
    
    # 5356 Aluminium
    ("5356 Aluminum", "https://prodcd.harrisproductsgroup.com/en/Products/53566033pop", "Harris Products (Weld Filler)"),
    
    # PVC (fixing duplicates)
    ("PVC (Polyvinyl Chloride Plastic)", "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-PVC.pdf", "Mitsubishi Chemical (Type I Rigid)"),
    ("Polyvinyl chloride", "DELETE", ""),
    
    # 8006 Aluminium
    ("8006 Aluminium Alloy", "https://matmatch.com/materials/alky2272-en-573-3-grade-aw-8006-o", "Matmatch (O-Temper)"),
    
    # POM
    ("POM (Acetal Plastic)", "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet_Acetron-POM-H.pdf", "Mitsubishi Acetron POM-H"),
    
    # Tungsten Carbide
    ("Tungsten Carbide (WC)", "https://en.wikipedia.org/wiki/Tungsten_carbide", "Wikipedia"),
    ("Tungsten carbide", "DELETE", ""),
    
    # Titanium Carbide
    ("Titanium Carbide (TiC)", "https://en.wikipedia.org/wiki/Titanium_carbide", "Wikipedia"),
    ("Titanium carbide", "DELETE", ""),
    
    # TiO2
    ("Titanium Dioxide (Titania / TiO2)", "https://crystran.com/media/wysiwyg/Materials/rutile-tio2-data-sheet.pdf", "Crystran Datasheet"),
    
    # Hafnium Carbide
    ("Hafnium Carbide (HfC)", "https://www.goodfellow.com/usa/resources/hafnium-carbide-hfc-material-information/", "Goodfellow"),
    
    # Tantalum Carbide
    ("Tantalum Carbide (TaC)", "https://www.goodfellow.com/usa/resources/tantalum-carbide-tac-material-information/", "Goodfellow"),
    
    # Zirconium Diboride
    ("Zirconium diboride", "https://research.birmingham.ac.uk/files/75972834/Sonber_CS_2016_0006.pdf", "Ceramics-Silikaty (2016 Paper)"),
    
    # BSCCO
    ("Bismuth Strontium Calcium Copper Oxide (BSCCO - Superconductor)", "https://en.wikipedia.org/wiki/Bismuth_strontium_calcium_copper_oxide", "Wikipedia"),
    
    # 304 Stainless
    ("304 Stainless Steel", "https://www.matweb.com/search/datasheet_print.aspx?matguid=abc4415b0f8b490387e3c922237098da", "MatWeb (Typical Annealed)"),
    
    # Borosilicate Tube
    ("Borosilicate Glass (Tube)", "https://media.schott.com/api/public/content/4b6b4e5d10744d29ac632bbd63dee5d8", "SCHOTT DURAN"),
    
    # Soda-Lime Glass (fixing duplicates)
    ("Soda-Lime Glass (Sheet)", "https://www.pilkington.com/-/media/pilkington/site-content/usa/window-manufacturers/technical-bulletins/ats-129---properties-of-soda-lime-silica-float-glass.pdf", "Pilkington ATS-129"),
    ("Soda-Lime Glass", "DELETE", ""),
    ("Soda-Lime Glass (Tube)", "https://media.schott.com/api/public/content/79a671737b4a4833aa91c99f68c4b5a3", "SCHOTT AR-GLAS"),
    
    # 5154 Aluminium
    ("5154 aluminium alloy", "https://www.makeitfrom.com/material-properties/5154-A95154-Aluminum", "MakeItFrom"),
    
    # 7039 Aluminium
    ("7039 aluminium alloy", "https://www.azom.com/article.aspx?ArticleID=8764", "AZoM"),
    
    # 7050 Aluminium
    ("7050 aluminium alloy", "https://metals.ulprospector.com/ja/datasheet/e272683/alcoa-7050-t7451", "Alcoa / UL Prospector (T7451)"),
    
    # PTFE
    ("PTFE (Teflon Plastic)", "https://www.materialdatacenter.com/ms/en/Teflon/The+Chemours+Company/Teflon%E2%84%A2+PTFE+7A+X/61699362/824", "Chemours (Resin Data)"),
]

print("Applying Wikipedia batch updates...")
for name, url, source_name in wiki_updates:
    if url == "DELETE":
        res = supabase.table('materials').delete().eq('name', name).execute()
        print(f"Deleted duplicate: {name} ({len(res.data)} rows)")
    else:
        res = supabase.table('materials').update({
            'source_url': url,
            'source_name': source_name
        }).eq('name', name).execute()
        print(f"Updated: {name} -> {url}")

print("\nDone with Wikipedia batch.")
