import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

updates = {
    'AISI 4140': {'url': 'https://www.makeitfrom.com/material-properties/Normalized-4140-Cr-Mo-Steel', 'name': 'MakeItFrom (Normalized)'},
    'AISI 4340': {'url': 'https://www.makeitfrom.com/material-properties/SAE-AISI-4340-SNCM439-G43400-Ni-Cr-Mo-Steel', 'name': 'MakeItFrom'},
    'C26000 Cartridge Brass': {'url': 'https://www.makeitfrom.com/material-properties/UNS-C26000-CW505L-Cartridge-Brass', 'name': 'MakeItFrom'},
    'Monel 400': {'url': 'https://www.specialmetals.com/documents/technical-bulletins/monel-alloy-400.pdf', 'name': 'Verified Source (Special Metals SMC-053)'},
    'Phosphor Bronze (C51000)': {'url': 'https://www.makeitfrom.com/material-properties/UNS-C51000-CW451K-Phosphor-Bronze', 'name': 'MakeItFrom'},
    'Plywood (BWR Grade)': {'url': 'https://services.bis.gov.in/tmp/1733904079.pdf', 'name': 'Verified Source (IS 303:2024)'},
    'Titanium Grade 2': {'url': 'https://www.upmet.com:443/sites/default/files/datasheets/cp-grade-2.pdf', 'name': 'Verified Source (UPMET)'},
    'Titanium Grade 1': {'url': 'https://www.bibusmetals.cz/fileadmin/materials/PDF/BM_Datasheets/BM_datasheet_Ti_Grade_1.pdf', 'name': 'Verified Source (Bibus Metals)'},
    'Titanium Grade 23': {'url': 'https://www.bibusmetals.cz/fileadmin/materials/PDF/BM_Datasheets/BM_datasheet_Ti_Grade_23_Ti6-4ELI.pdf', 'name': 'Verified Source (Bibus Metals F136)'},
    'Titanium Grade 5': {'url': 'https://www.upmet.com/sites/default/files/datasheets/ti-6al-4v.pdf', 'name': 'Verified Source (UPMET)'},
    'Hastelloy C-276': {'url': 'https://haynesintl.com/en/datasheet/hastelloy-c-276-alloy/', 'name': 'Verified Source (Haynes Int)'},
    'Chalcogenide Glass (sheet)': {'url': 'https://media.schott.com/api/public/content/bef2171f769a4b6b93d6525e12a008d0', 'name': 'Verified Source (SCHOTT IRG 27)'},
    'Chalcogenide Glass (tube)': {'url': 'https://media.schott.com/api/public/content/bef2171f769a4b6b93d6525e12a008d0', 'name': 'Verified Source (SCHOTT IRG 27)'},
    'Chalcogenide Glass': {'url': 'https://media.schott.com/api/public/content/bef2171f769a4b6b93d6525e12a008d0', 'name': 'Verified Source (SCHOTT IRG 27)'},
    'Fluorozirconate (sheet)': {'url': 'https://leverrefluore.com/scientific-world/fluoride-glasses/', 'name': 'Verified Source (Le Verre Fluore)'},
    'Fluorozirconate (tube)': {'url': 'https://leverrefluore.com/scientific-world/fluoride-glasses/', 'name': 'Verified Source (Le Verre Fluore)'},
    'Lead Glass (sheet)': {'url': 'https://uqgoptics.com/wp-content/uploads/2019/06/Lead-Glass-Schott-RD50.pdf', 'name': 'Verified Source (SCHOTT RD 50)'},
    'Lead Glass (tube)': {'url': 'https://media.schott.com/api/public/content/28cc4b9b071c4ed3bc20b8590c86e801', 'name': 'Verified Source (SCHOTT 8532)'},
    'Austenitic Stainless (Food Grade)': {'url': 'https://otke-cdn.outokumpu.com/-/media/files/products/core/outokumpu-core-range-datasheet.pdf', 'name': 'Verified Source (Outokumpu Core 304/4301)'},
    'Austenitic Stainless (Marine Grade)': {'url': 'https://otke-cdn.outokumpu.com/-/media/files/products/supra/outokumpu-supra-range-datasheet.pdf', 'name': 'Verified Source (Outokumpu Supra 316/4404)'},
    'Rene 41': {'url': 'https://www.rolledalloys.ca/wp-content/uploads/RENE-41_Data-sheet-rolled-alloys.pdf', 'name': 'Verified Source (Rolled Alloys)'},
    'White Cast Iron': {'url': 'https://matmatch.com/materials/minfc39192-en-12513-grade-g-x-300-crmo-15-3-soft-annealed-a-', 'name': 'Verified Source (Substituted: EN 12513 G-X 300 CrMo 15 3)'},
    'Yb2AlGe3': {'url': 'https://www.osti.gov/dataexplorer/biblio/dataset/1310102', 'name': 'OSTI/Materials Project (DFT Computed Data)'},
    'YbMgCu4': {'url': 'https://www.osti.gov/dataexplorer/biblio/dataset/1355567', 'name': 'OSTI/Materials Project (DFT Computed Data)'},
    'YbMoClO4': {'url': 'https://www.osti.gov/dataexplorer/biblio/dataset/1311492', 'name': 'OSTI/Materials Project (DFT Computed Data)'},
    'YbSiPt2': {'url': 'https://www.osti.gov/dataexplorer/biblio/dataset/1310077', 'name': 'OSTI/Materials Project (DFT Computed Data, describes YbPt2Si)'},
    'Inconel 601': {'url': 'https://www.matweb.com/search/datasheettext.aspx?matguid=f3fb3ae6ebe54d98ad8fa01c74b6a3e8', 'name': 'Verified Source (MatWeb/Special Metals)'},
    'Inconel 617': {'url': 'https://www.matweb.com/search/datasheettext.aspx?matguid=adf2123d8e494e75aef7417989ffea92', 'name': 'Verified Source (MatWeb/Special Metals)'},
    'Ebony Wood': {'url': 'https://www.wood-database.com/gaboon-ebony/', 'name': 'Verified Source (Gaboon Ebony, 12% Moisture Content)'},
    'Balsa Wood': {'url': 'https://research.fs.usda.gov/treesearch/7149', 'name': 'Verified Source (USFS Wood Handbook)'},
    'Plywood (Birch)': {'url': 'https://gabarro.com/sites/default/files/2024-07/UPM%20Wisa%20Birch%20-%20Inf%20Tecn.pdf', 'name': 'Verified Source (UPM WISA-Birch)'}
}
updates['Phosphor Bronze'] = updates['Phosphor Bronze (C51000)']

# Since we don't have exact db names for all, we will fetch all materials missing a URL, and substring match.
res = supabase.table('materials').select('name, id').is_('source_url', 'null').execute()

updated_count = 0
for row in res.data:
    db_name = row['name']
    matched_key = None
    
    # Exact match first
    for k in updates.keys():
        if k.lower() == db_name.lower():
            matched_key = k
            break
            
    # Substring match if no exact match
    if not matched_key:
        for k in updates.keys():
            if k.lower() in db_name.lower():
                matched_key = k
                break

    if matched_key:
        info = updates[matched_key]
        print(f"Updating {db_name} -> {info['url']}")
        supabase.table('materials').update({'source_url': info['url'], 'source_name': info['name']}).eq('id', row['id']).execute()
        updated_count += 1
    else:
        print(f"UNMATCHED: {db_name}")

print(f'Final batch complete. Updated {updated_count} records.')
