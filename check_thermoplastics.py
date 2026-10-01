
import requests
import urllib3
urllib3.disable_warnings()

urls = [
    "https://download.basf.com/p1/8a8082587fd4b608017fd6587a9757d9/en/ULTRAMID%3Csup%3E%C2%AE%3Csup%3E_A3EG6",
    "https://www.lookpolymers.com/polymer_Kingfa-PA66-G30-30-Glass-Fiber-Reinforced-PA66.php",
    "https://www.lookpolymers.com/polymer_Quadrant-EPP-Ertalon-66-GF30-PA-66-30-glass-filled-extruded-ISO-Data.php",
    "https://www.victrex.com/en/downloads/datasheets/victrex-peek-90ca30",
    "https://www.lookpolymers.com/polymer_Victrex-PEEK-450CA30-30-Carbon-Fiber-Reinforced.php",
    "https://ceadgroup.com/wp-content/uploads/2021/05/Materials-Victrex-PEEK-90CA30.pdf",
    "https://materialdatacenter.com/ms/zh/Makrolon/Covestro+Deutschland+AG/Makrolon%C2%AE+9125/640afdd0/410",
    "https://samtion.com/product/covestro-makrolon-9125/",
    "https://sukeplastics.com/products/covestro-makrolon-9125/",
    "https://www.lookpolymers.com/polymer_PolyOne-Edgetek-PC-20GF000-Polycarbonate-PC.php",
    "https://www.lookpolymers.com/polymer_Covestro-Makrolon-GF8001-Polycarbonate-20-Glass-Filled.php"
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

