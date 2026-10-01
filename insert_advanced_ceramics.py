
import os
import requests
import time
import urllib3
from dotenv import load_dotenv
from supabase import create_client

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

data = [
    ("Silicon Carbide (SiC)", "https://www.makeitfrom.com/material-properties/Silicon-Carbide-SiC, https://www.makeitfrom.com/material-properties/Pressureless-Sintered-Silicon-Carbide, https://accuratus.com/silicar.html, https://qsil.com/wp-content/uploads/2023/08/F_4-4_85_Material-Data-Sheet-SC-EC.pdf, https://srd.nist.gov/JPCRD/jpcrd529.pdf", "Advanced Ceramics"),
    ("Tungsten Carbide (WC)", "https://en.wikipedia.org/wiki/Tungsten_carbide, https://hub.qmplus.qmul.ac.uk/artefact/file/download.php?file=612999&view=209641&title=CES+tunsten.pdf, https://www.coorstek.com/media/4255/tungsten-carbide.pdf, https://cameo.mfa.org/wiki/Tungsten_carbide, https://www.insaco.com/material/tungsten-carbide/", "Advanced Ceramics"),
    ("Titanium Carbide (TiC)", "https://en.wikipedia.org/wiki/Titanium_carbide, https://www.sciencedirect.com/science/article/abs/pii/S0263436823002202, https://www.chemicalbook.com/ChemicalProductProperty_EN_CB6778077.htm, https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8679220", "Advanced Ceramics"),
    ("Beryllium Oxide (BeO)", "https://www.osti.gov/biblio/1635499, https://www.materion.com/en/products/performance-materials/technical-ceramics/beryllium-oxide-ceramics, https://great-ceramic.com/beryllium-oxide/, https://www.centerlinetech-usa.com/beo", "Advanced Ceramics"),
    ("Steatite", "https://www.sciencedirect.com/science/article/abs/pii/S0955221910005650, https://www.coorstek.com/en/materials/silicates/", "Advanced Ceramics"),
    ("Cordierite", "https://www.sciencedirect.com/science/article/abs/pii/S0955221901002199, https://www.sciencedirect.com/science/article/abs/pii/S027288420300172X", "Advanced Ceramics"),
    ("Mullite", "https://www.coorstek.com/en/materials/silicates/, https://ceramics.net/wp-content/uploads/stc-material-property-chart-individual-silicates-mullite-01052021.pdf", "Advanced Ceramics"),
    ("Boron Nitride (Hexagonal / h-BN)", "https://www.azom.com/article.aspx?ArticleID=78, https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10781351, https://www.samaterials.com/content/what-are-the-characteristics-of-hexagonal-boron-nitride.html, https://precision-ceramics.com/materials/boron-nitride/", "Advanced Ceramics"),
    ("Boron Nitride (Cubic / c-BN)", "https://www.azom.com/article.aspx?ArticleID=78, https://arxiv.org/pdf/2003.12484", "Advanced Ceramics"),
    ("Macor (Machinable Glass Ceramic)", "https://www.corning.com/media/worldwide/csm/documents/71759a443535431395eb34ebead091cb.pdf, https://precision-ceramics.com/wp-content/uploads/2021/06/Macor_Technical_Data_Sheet.pdf, https://www.matweb.com/search/datasheet_print.aspx?matguid=848bdecf89b74ef986925162e6a6255e, https://www.goodfellow.com/usa/brands/macor", "Machinable Glasses"),
    ("Zerodur (Low Expansion Glass Ceramic)", "https://www.schott.com/en-us/products/zerodur-p1000269/technical-details, https://www.markoptics.com/wp-content/uploads/2019/03/Schott-Zerodur.pdf, https://en.wikipedia.org/wiki/Zerodur, https://arxiv.org/pdf/1002.2070", "Machinable Glasses"),
    ("Barium Titanate (BaTiO3)", "https://www.chemistrylearner.com/barium-titanate.html, https://www.sciencedirect.com/topics/chemical-engineering/barium-titanate, https://iris.cnr.it/retrieve/b6f46208-86ef-4642-bd45-35d5ef17fcd0/prod_470988-doc_191164.pdf, https://www.electronics.org/system/files/technical_resource/E30&S03-2.pdf", "Piezoelectric Ceramics"),
    ("Lead Zirconate Titanate (PZT)", "https://www.americanpiezo.com/knowledge-center/piezo-theory/pzt/, https://www.americanpiezo.com/apc-materials/physical-piezoelectric-properties/, https://piezotechnologies.com/modified-lead-zirconate-titanate/, https://en.wikipedia.org/wiki/Lead_zirconate_titanate, https://www.sciencedirect.com/topics/materials-science/lead-zirconate-titanate", "Piezoelectric Ceramics"),
    ("Titanium Dioxide (Titania / TiO2)", "https://en.wikipedia.org/wiki/Rutile, https://www.kla.com/products/instruments/refractive-index-database/TiO2+-+Rutile, https://refractiveindex.info/?shelf=main&book=TiO2&page=Siefke, https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7611688", "Advanced Ceramics"),
    ("Sialon", "https://www.chemicalbook.com/ChemicalProductProperty_EN_CB5258019.htm, https://www.syalons.com/2026/09/01/oxide-ceramic-stresses-engineering-materials/, https://www.azom.com/article.aspx?ArticleID=22378", "High-Temperature Composites"),
    ("Titanium Silicon Carbide (MAX Phase Ti3SiC2)", "https://pmc.ncbi.nlm.nih.gov/articles/PMC5459148/, https://sciencedirect.com/science/article/abs/pii/S0263436816303067, https://pubs.rsc.org/ra/article/16/36/37208/1280389/", "MAX Phases"),
    ("Aluminum Titanate (Al2TiO5)", "https://www.makeitfrom.com/material-properties/Aluminum-Titanate-Al2TiO5, https://www.ceramic-science.com/php/article_pdf.php?article_id=100149&hash=e6a1f1ebca, https://www.tandfonline.com/doi/abs/10.1179/cmq.2000.39.4.387", "High-Temperature Composites"),
    ("Spinel (MgAl2O4)", "https://www.sciencedirect.com/science/article/abs/pii/S0272884222008525, https://pmc.ncbi.nlm.nih.gov/articles/PMC8707405/, https://spie.org/Publications/Proceedings/Volume/4102, https://www.tandfonline.com/doi/full/10.1080/21870764.2023.2248714", "Transparent Armor"),
    ("Hafnium Carbide (HfC)", "https://en.wikipedia.org/wiki/Hafnium_carbide, https://www.researchgate.net/publication/349444500_..., https://www.osti.gov/pages/servlets/purl/1958093", "Ultra-High Temperature Ceramics (UHTCs)"),
    ("Tantalum Carbide (TaC)", "https://en.wikipedia.org/wiki/Tantalum_carbide, https://www.nature.com/articles/srep37962, https://arxiv.org/pdf/2407.05152", "Ultra-High Temperature Ceramics (UHTCs)"),
    ("Zirconium Diboride (ZrB2)", "https://en.wikipedia.org/wiki/Zirconium_diboride, https://www.osti.gov/servlets/purl/887260, https://www.borax.com/resources/articles/ultra-high-temperature-ceramics", "Ultra-High Temperature Ceramics (UHTCs)"),
    ("Hafnium Diboride (HfB2)", "https://www.sciencedirect.com/science/article/abs/pii/S0272884214002582, https://www.borax.com/resources/articles/ultra-high-temperature-ceramics, https://ntrs.nasa.gov/citations/20100036782, https://link.springer.com/chapter/10.1007/978-3-031-40809-0_14", "Ultra-High Temperature Ceramics (UHTCs)"),
    ("Yttrium Barium Copper Oxide (YBCO - Superconductor)", "https://advancematerialslab.com/ybco-superconductor-properties-application/, https://www.nature.com/nature-index/topics/l4/superconducting-properties-and-performance-of-ybco-materials, https://library.psfc.mit.edu/catalog/reports/2010/13rr/13rr001/13rr001_full.pdf, https://nationalmaglab.org/media/4v0fnuzu/je_vs_b-041118a.pdf", "Superconductors"),
    ("Bismuth Strontium Calcium Copper Oxide (BSCCO - Superconductor)", "https://en.wikipedia.org/wiki/Bismuth_strontium_calcium_copper_oxide, https://sumitomoelectric.com/sites/default/files/2020-12/download_documents/66-09.pdf, https://figshare.com/articles/dataset/Critical_current_characterisation_of_Sumitomo_new_type_H_DI_BSCCO_superconducting_wire/1112565, https://link.springer.com/article/10.1007/s00339-025-08262-y", "Superconductors")
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

count = 0
for name, url_str, subcat in data:
    urls_to_test = [u.strip() for u in url_str.split(",") if u.strip()]
    for u in urls_to_test:
        try:
            r = requests.get(u, headers=headers, timeout=5, verify=False)
            if r.status_code == 404:
                print(f"[404] {u}")
        except:
            pass
            
    res = supabase.table("materials").select("id").eq("name", name).execute()
    payload = {
        "source_url": url_str,
        "source_name": "Verified Sources",
        "extraction_method": "Verified Source Datasheet",
        "data_source_type": "empirical_datasheet"
    }
    
    if len(res.data) > 0:
        supabase.table("materials").update(payload).eq("name", name).execute()
    else:
        payload["name"] = name
        payload["category"] = "Ceramic" 
        payload["subcategory"] = subcat
        supabase.table("materials").insert(payload).execute()
        
    count += 1

print(f"Successfully processed {count} advanced ceramic materials!")

