
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urls = [
    "https://www.toraycma.com/wp-content/uploads/T300-Technical-Data-Sheet-1.pdf",
    "https://hexcel.com/wp-content/uploads/2025/12/HexPly_8552_eu_DataSheet1.pdf",
    "https://hexcel.com/?p=711",
    "https://media.easycomposites.co.uk/datasheets/AS4_HexTow_DataSheet.pdf",
    "https://wichita.edu/industry_and_defense/NIAR/Research/hexcel-8552/AS4-Unitape-2.pdf",
    "https://eng.libretexts.org/Under_Construction/Aerospace_Structures_(Johnson)/08%3A_Laminated_bars_of_fiber-reinforced_polymer_composites/8.01%3A_Nomenclature_of_composite_materials",
    "https://www.toraycma.com/wp-content/uploads/M46J-Data-Sheet.pdf",
    "https://hexcel.com/wp-content/uploads/2025/12/IM7_HexTow_DataSheet.pdf",
    "https://www.aircraftspruce.com/catalog/pdf/01-01606tds.pdf",
    "https://www.wichita.edu/industry_and_defense/NIAR/Research/hexcel-8552/IM7-Unitape-2.pdf",
    "https://wichita.edu/industry_and_defense/NIAR/Documents/NCP-RP-2009-028-Rev-B-HEXCEL-8552-IM7-Uni-SAR-4-16-2019.pdf",
    "https://hexcel.com/wp-content/uploads/2026/01/HexTow_HM63_Flyer.pdf",
    "https://acpcomposites.com/shop/carbon-fiber/carbon-prepregs/5-8-oz-carbon-fiber-2x2-twill-weave-rts-prepreg",
    "https://acpcomposites.wpenginepowered.com/wp-content/uploads/2023/10/Carbon-Fiber-198-Prepreg-PDS.pdf",
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC9679481/",
    "https://data.mendeley.com/datasets/w32mrdmw7h/2",
    "https://www.wichita.edu/industry_and_defense/NIAR/Research/hexcel-8552/AS4-PW-2.pdf",
    "https://www.semcocarbon.com/file-downloads-folder/carbon-composite-spec-sheet-REV2.pdf",
    "https://www.ias.ac.in/article/fulltext/sadh/028/01-02/0349-0358",
    "https://doi.org/10.3389/fmats.2024.1374034"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

print("Checking CFRP Links...")
for u in urls:
    try:
        r = requests.get(u, headers=headers, timeout=10, verify=False, allow_redirects=True)
        print(f"[{r.status_code}] {u}")
    except Exception as e:
        print(f"[ERROR] {u}: {e}")

print("Done.")

