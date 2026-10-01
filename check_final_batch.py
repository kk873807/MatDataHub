
import requests
import urllib3
urllib3.disable_warnings()

urls = [
    "https://ntrs.nasa.gov/api/citations/20080006463/downloads/20080006463.pdf",
    "https://ntrs.nasa.gov/api/citations/20000053472/downloads/20000053472.pdf",
    "https://ntrs.nasa.gov/api/citations/20020072848/downloads/20020072848.pdf",
    "https://matmatch.com/materials/sglx0013-sigrasic-carbon-fiber-reinforced-silicon-carbide-felt",
    "https://etheses.bham.ac.uk/id/eprint/5924/",
    "https://hexcel.com/wp-content/uploads/2026/01/HexWeb_HRH10_DataSheet_us.pdf",
    "https://hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf",
    "https://products.evonik.com/assets/35/22/ROHACELL_HERO_2022_April_EN_243522.pdf",
    "https://research.fs.usda.gov/treesearch/37421",
    "https://www.compositepanel.org/products/medium-density-fiberboard/",
    "https://apawood.org/osb",
    "https://awc.org/wp-content/uploads/2021/10/AWC_NDS2018-withCommentary_20200827_AWCWebsite_Chapter05.pdf",
    "https://www.fhwa.dot.gov/publications/research/infrastructure/structures/06103/06103.pdf",
    "https://doi.org/10.3390/aerospace6010007",
    "https://www2.mdpi.com/2073-4360/9/9/437",
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC7696086"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

for u in urls:
    try:
        r = requests.get(u, headers=headers, timeout=10, verify=False, allow_redirects=True)
        print(f"[{r.status_code}] {u}")
    except Exception as e:
        print(f"[ERROR] {u}: {e}")

