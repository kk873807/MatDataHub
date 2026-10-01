
import requests
import urllib3
urllib3.disable_warnings()

urls = [
    "https://cpstechnologysolutions.com/wp-content/uploads/2025/09/CPS-Alsic-2025-Final.pdf",
    "https://ceramics.ferrotec.com/materials/metal-matrix/al-sic/",
    "https://www-eng.lbl.gov/~shuman/NEXT/MATERIALS&COMPONENTS/MISC/AlSiC_Metal-Matrix-Composite-Datasheet.pdf",
    "https://www.specmaterials.com/silicon-carbide-fiber-1",
    "https://www.cambridge.org/core/product/F001DC9D9AA326DAA1F522F327C8788A",
    "https://ww2.nrc.gov/docs/ML1307/ML13079A685.pdf",
    "https://holtecinternational.com/products-and-services/innovative-technologies/neutronabsorbermaterial/"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

for u in urls:
    try:
        r = requests.get(u, headers=headers, timeout=10, verify=False, allow_redirects=True)
        print(f"[{r.status_code}] {u}")
    except Exception as e:
        print(f"[ERROR] {u}: {e}")

