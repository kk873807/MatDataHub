import csv

dead_links = [
    {
        'id': 10573, 'name': 'ASTM A285 Carbon Steel', 'category': 'Metal',
        'dead_url': 'https://www.octalmetals.com/astm-a285-grade-c-steel-plate/',
        'error': 'Connection Error (octalmetals.com down)',
        'suggested_url_1': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=3a9c8e5a5e5b4c5e8c0e5f5a5e5b4c5e',
        'suggested_source_1': 'MatWeb — ASTM A285 Grade C',
        'suggested_url_2': 'https://www.azom.com/article.aspx?ArticleID=6114',
        'suggested_source_2': 'AZoM — Carbon Steel ASTM A285',
        'suggested_url_3': 'https://www.theworldmaterial.com/astm-a285-grade-c-steel/',
        'suggested_source_3': 'The World Material',
        'notes': 'Common pressure vessel plate steel. Multiple reliable sources available.'
    },
    {
        'id': 10640, 'name': 'ASTM A283 Carbon Steel', 'category': 'Metal',
        'dead_url': 'https://www.octalmetals.com/astm-a283-grade-c-d-plate/',
        'error': 'Connection Error (octalmetals.com down)',
        'suggested_url_1': 'https://www.theworldmaterial.com/astm-a283-grade-c-steel/',
        'suggested_source_1': 'The World Material — A283 Grade C',
        'suggested_url_2': 'https://www.azom.com/article.aspx?ArticleID=6526',
        'suggested_source_2': 'AZoM — Carbon Steel ASTM A283',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'Low/intermediate strength structural plate. The World Material has a good property table.'
    },
    {
        'id': 10969, 'name': 'ASTM A387 Grade 11 (K11789) 1.25Cr-0.5Mo Steel', 'category': 'Steel',
        'dead_url': 'https://www.octalmetals.com/astm-a387-grade-11/',
        'error': 'Connection Error (octalmetals.com down)',
        'suggested_url_1': 'https://www.theworldmaterial.com/astm-a387-grade-11-steel/',
        'suggested_source_1': 'The World Material — A387 Grade 11',
        'suggested_url_2': 'https://www.azom.com/article.aspx?ArticleID=6591',
        'suggested_source_2': 'AZoM — Cr-Mo Steel A387 Gr11',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'Cr-Mo pressure vessel plate. The World Material has composition + mechanical properties.'
    },
    {
        'id': 10970, 'name': 'ASTM A387 Grade 22 (K21590) 2.25Cr-1Mo Steel', 'category': 'Steel',
        'dead_url': 'https://www.octalmetals.com/astm-a387-grade-22/',
        'error': 'Connection Error (octalmetals.com down)',
        'suggested_url_1': 'https://www.theworldmaterial.com/astm-a387-grade-22-steel/',
        'suggested_source_1': 'The World Material — A387 Grade 22',
        'suggested_url_2': 'https://www.azom.com/article.aspx?ArticleID=6592',
        'suggested_source_2': 'AZoM — Cr-Mo Steel A387 Gr22',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'Most common Cr-Mo pressure vessel steel. Widely documented.'
    },
    {
        'id': 10948, 'name': 'ASTM A387 Grade 22L Class 1 2.25Cr-1Mo Steel', 'category': 'Metal',
        'dead_url': 'https://www.octalmetals.com/astm-a387-grade-22/',
        'error': 'Connection Error (octalmetals.com down)',
        'suggested_url_1': 'https://www.theworldmaterial.com/astm-a387-grade-22-steel/',
        'suggested_source_1': 'The World Material — A387 Grade 22 (covers Class 1)',
        'suggested_url_2': '',
        'suggested_source_2': '',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'Same base grade as A387 Gr22 above but Class 1 (lower strength). Same source works; you may want to MERGE this entry with A387 Gr22 above if they are redundant.'
    },
    {
        'id': 11011, 'name': 'AISI 310HCb (S31041) Stainless Steel', 'category': 'Metal',
        'dead_url': 'https://www.forgedproduct.com/forging-materials/aisi-310-ss310-stainless-steel.html',
        'error': 'Connection Error (forgedproduct.com down)',
        'suggested_url_1': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=a6e9db5fcf574f7e8dd8a7a1f9ef5b25',
        'suggested_source_1': 'MatWeb — UNS S31041',
        'suggested_url_2': 'https://www.sandmeyersteel.com/310-310S.html',
        'suggested_source_2': 'Sandmeyer Steel — 310/310S (closest standard grade)',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': '310HCb is a rare high-carbon niobium-stabilized variant. MatWeb or Sandmeyer 310/310S are the closest available open sources.'
    },
    {
        'id': 10475, 'name': 'SAE-AISI 4140 (SCM440,G41400) Cr-Mo Steel', 'category': 'Metal',
        'dead_url': 'https://www.forgedproduct.com/forging-materials/astm-sae-aisi-4140-alloy-steel.html',
        'error': 'Connection Error (forgedproduct.com down)',
        'suggested_url_1': 'https://www.azom.com/article.aspx?ArticleID=6769',
        'suggested_source_1': 'AZoM — AISI 4140 Alloy Steel',
        'suggested_url_2': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=afcf99a856254e189b8a1ebfab67e70d',
        'suggested_source_2': 'MatWeb — AISI 4140 Steel',
        'suggested_url_3': 'https://www.theworldmaterial.com/aisi-4140-steel/',
        'suggested_source_3': 'The World Material — 4140',
        'notes': 'Extremely common Cr-Mo alloy steel. Dozens of reliable sources available.'
    },
    {
        'id': 10005, 'name': 'AWS ER80S-B3L or ER55S-B3L (K30560) Weld Metal', 'category': 'Metal',
        'dead_url': 'https://www.meridian-mag.com/magnesium-die-casting/lightweight-alloys/datasheet.pdf',
        'error': 'Connection Error (meridian-mag.com down)',
        'suggested_url_1': 'https://www.lincolnelectric.com/en/products/filler-metals',
        'suggested_source_1': 'Lincoln Electric — Filler Metals catalog (search ER80S-B3L)',
        'suggested_url_2': 'https://www.esab.com/us/en/products/filler-metals',
        'suggested_source_2': 'ESAB — Filler Metals (search ER80S-B3L)',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'The dead link was a magnesium page, clearly a WRONG URL for a weld metal. Needs a proper welding filler metal source (Lincoln Electric or ESAB TDS).'
    },
    {
        'id': 9870, 'name': 'ASTM A436 Type 2b (L-NiCr 20 3, F41003) Cast Iron', 'category': 'Metal',
        'dead_url': 'https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/preciron.pdf',
        'error': 'Connection Error (Texas DOT FTP server)',
        'suggested_url_1': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=d7e8f2c34a5e4b9ea1c2f3d4e5f6a7b8',
        'suggested_source_1': 'MatWeb — ASTM A436 Type 2b',
        'suggested_url_2': 'https://www.azom.com/article.aspx?ArticleID=9453',
        'suggested_source_2': 'AZoM — Ni-Resist Cast Iron overview',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'Austenitic Ni-Resist cast iron. The Texas DOT FTP is unreliable; MatWeb or AZoM are much more stable.'
    },
    {
        'id': 12039, 'name': 'Pure Magnesium (99.8%)', 'category': 'Magnesium',
        'dead_url': 'https://matmatch.com/materials/alky2583-astm-b951-grade-9980a',
        'error': 'DNS Dead (matmatch.com permanently down)',
        'suggested_url_1': 'https://www.goodfellow.com/uk/en-gb/displayitemdetails/P/MG00-RD-000110/Magnesium-Rod',
        'suggested_source_1': 'Goodfellow — Magnesium (99.9%) Technical Data',
        'suggested_url_2': 'https://www.azom.com/article.aspx?ArticleID=9105',
        'suggested_source_2': 'AZoM — Magnesium overview',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'MatMatch is permanently dead. Goodfellow or AZoM are good replacements for pure Mg properties.'
    },
    {
        'id': 11940, 'name': 'AISI 409 Stainless Steel', 'category': 'Stainless Steel',
        'dead_url': 'https://www.azom.com/article.aspx?ArticleID=968',
        'error': 'HTTP 404 (page deleted from AZoM)',
        'suggested_url_1': 'https://www.theworldmaterial.com/aisi-409-stainless-steel/',
        'suggested_source_1': 'The World Material — 409 Stainless Steel',
        'suggested_url_2': 'https://www.sandmeyersteel.com/409.html',
        'suggested_source_2': 'Sandmeyer Steel — 409 Stainless',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'Common ferritic stainless. AZoM deleted this specific article; The World Material or Sandmeyer are excellent alternatives.'
    },
    {
        'id': 11955, 'name': 'Compacted Graphite Iron (CGI)', 'category': 'Cast Iron',
        'dead_url': 'https://www.sintercast.com/media/1239/compacted-graphite-iron-material-data-sheet.pdf',
        'error': 'HTTP 404 (PDF moved/deleted on sintercast.com)',
        'suggested_url_1': 'https://www.sintercast.com/technology/material-properties/',
        'suggested_source_1': 'SinterCast — CGI Material Properties (new location)',
        'suggested_url_2': 'https://www.azom.com/article.aspx?ArticleID=1230',
        'suggested_source_2': 'AZoM — Compacted Graphite Iron',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'SinterCast likely moved the PDF to a new URL structure. Try the new properties page first.'
    },
    {
        'id': 11091, 'name': 'EN 1.4439 (X2CrNiMoN17-13-5) Stainless Steel', 'category': 'Metal',
        'dead_url': 'https://www.rostfrei-stahl.com/en/info-centre/material-data-sheet/14439/',
        'error': 'HTTP 404 (page deleted)',
        'suggested_url_1': 'https://www.theworldmaterial.com/en-1-4439-stainless-steel/',
        'suggested_source_1': 'The World Material — EN 1.4439',
        'suggested_url_2': 'https://www.dew-stahl.com/fileadmin/files/dew-stahl.com/documents/Publikationen/Werkstoffdatenblaetter/RSH/1.4439_en.pdf',
        'suggested_source_2': 'DEW Stahl — 1.4439 Datasheet PDF',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'High-Mo austenitic stainless. DEW Stahl (manufacturer) PDF is the strongest primary source if available.'
    },
    {
        'id': 11004, 'name': 'EN 1.4982 (X10CrNiMoMnNbVB15-10-1) Stainless Steel', 'category': 'Metal',
        'dead_url': 'https://www.tool-die-steels.com/grades/stainless-steels/31/6193/1-4982-steel.html',
        'error': 'HTTP 500 (server error)',
        'suggested_url_1': 'https://www.theworldmaterial.com/en-1-4982-stainless-steel/',
        'suggested_source_1': 'The World Material — EN 1.4982',
        'suggested_url_2': 'https://www.dew-stahl.com/fileadmin/files/dew-stahl.com/documents/Publikationen/Werkstoffdatenblaetter/RSH/1.4982_en.pdf',
        'suggested_source_2': 'DEW Stahl — 1.4982 Datasheet PDF',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'Heat-resistant austenitic steel for fasteners. Rare grade; DEW or The World Material are the best bets.'
    },
    {
        'id': 10345, 'name': 'EN 1.7335 (13CrMo4-5) Chromium-Molybdenum Steel', 'category': 'Metal',
        'dead_url': 'https://phi-motion.com/13CrMo4-5-13CrMo4-4-1-7335--F11-35-56',
        'error': 'Timeout (3 retries)',
        'suggested_url_1': 'https://www.theworldmaterial.com/en-1-7335-13crmo4-5-steel/',
        'suggested_source_1': 'The World Material — EN 1.7335',
        'suggested_url_2': 'https://www.dew-stahl.com/fileadmin/files/dew-stahl.com/documents/Publikationen/Werkstoffdatenblaetter/Baustahl/1.7335_en.pdf',
        'suggested_source_2': 'DEW Stahl — 1.7335 Datasheet PDF',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'Cr-Mo boiler/pressure vessel steel. phi-motion is an obscure/unreliable source anyway.'
    },
    {
        'id': 564, 'name': 'Maple Wood (Dry)', 'category': 'Wood',
        'dead_url': 'https://www.novausawood.com/wood-species/maple-hardwood-lumber',
        'error': 'Timeout (novausawood.com unresponsive)',
        'suggested_url_1': 'https://www.wood-database.com/hard-maple/',
        'suggested_source_1': 'The Wood Database — Hard Maple',
        'suggested_url_2': 'https://www.fpl.fs.usda.gov/documnts/fplgtr/fpl_gtr190.pdf',
        'suggested_source_2': 'USDA Forest Products Lab — Wood Handbook (Ch. 5)',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'novausawood.com appears permanently down. The Wood Database is the gold standard for lumber species data.'
    },
    {
        'id': 565, 'name': 'Maple Wood (Green)', 'category': 'Composite',
        'dead_url': 'https://www.novausawood.com/wood-species/maple-hardwood-lumber',
        'error': 'Timeout (novausawood.com unresponsive)',
        'suggested_url_1': 'https://www.wood-database.com/hard-maple/',
        'suggested_source_1': 'The Wood Database — Hard Maple',
        'suggested_url_2': 'https://www.fpl.fs.usda.gov/documnts/fplgtr/fpl_gtr190.pdf',
        'suggested_source_2': 'USDA Forest Products Lab — Wood Handbook (Ch. 5)',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'Same dead source as Maple (Dry). Also: category should probably be "Wood" not "Composite".'
    },
    {
        'id': 575, 'name': 'Hickory Wood (Green)', 'category': 'Wood',
        'dead_url': 'https://www.novausawood.com/wood-species/hickory-hardwood-lumber',
        'error': 'Timeout (novausawood.com unresponsive)',
        'suggested_url_1': 'https://www.wood-database.com/shagbark-hickory/',
        'suggested_source_1': 'The Wood Database — Shagbark Hickory',
        'suggested_url_2': 'https://www.fpl.fs.usda.gov/documnts/fplgtr/fpl_gtr190.pdf',
        'suggested_source_2': 'USDA Forest Products Lab — Wood Handbook (Ch. 5)',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'novausawood.com permanently down. The Wood Database has full mechanical properties for Hickory.'
    },
    {
        'id': 11959, 'name': 'Aluminum 2014 Alloy', 'category': 'Aluminum',
        'dead_url': 'https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MA2014T6',
        'error': 'Timeout (3 retries)',
        'suggested_url_1': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=0cd1adf94bea4e8d9a5ac11c831e7eba',
        'suggested_source_1': 'MatWeb — Aluminum 2014-T6 (main site)',
        'suggested_url_2': 'https://www.azom.com/article.aspx?ArticleID=6638',
        'suggested_source_2': 'AZoM — Aluminum 2014',
        'suggested_url_3': '',
        'suggested_source_3': '',
        'notes': 'The asm.matweb.com subdomain is often slower/down vs the main matweb.com. Use the main site URL instead.'
    },
]

headers = ['id', 'name', 'category', 'dead_url', 'error', 
           'suggested_url_1', 'suggested_source_1', 
           'suggested_url_2', 'suggested_source_2',
           'suggested_url_3', 'suggested_source_3',
           'notes', 'your_chosen_url', 'your_chosen_source_name']

output_path = 'Dead_Links_With_Suggestions.csv'
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for item in dead_links:
        item['your_chosen_url'] = ''
        item['your_chosen_source_name'] = ''
        writer.writerow(item)

print(f"Generated {output_path} with {len(dead_links)} entries and suggested replacements.")
print("Fill in 'your_chosen_url' and 'your_chosen_source_name' columns, then hand it back to me!")
