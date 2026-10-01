
import requests
import urllib3
urllib3.disable_warnings()

urls = [
    "https://laminatedplastics.com/fr-4.pdf",
    "https://en.wikipedia.org/wiki/FR-4",
    "https://www.atlasfibre.com/material/fr-4/",
    "https://thegundcompany.com/wp-content/uploads/2024/03/NEMA-G-10-Glass-Epoxy-Laminate-by-The-Gund-Co.pdf",
    "https://www.boedeker.com/Product/Micaply-G-10-Glass-Epoxy-Laminate-Sheet",
    "https://www.makeitfrom.com/material-properties/NEMA-Grade-G-10-GEE-Glass-Epoxy-Laminate",
    "https://www.fibreglast.com/blogs/learning-center/physical-properties-of-laminates",
    "https://wichita.edu/industry_and_defense/NIAR/Research/tencate-bt250e-6/S2-Glass-Unitape.pdf",
    "https://www.agy.com/wp-content/uploads/2021/12/933_S-2_Roving-Aerospace.pdf",
    "https://acpcomposites.com/wp-content/uploads/2024/05/Mechanical-Properties-of-Carbon-Fiber-Composite-Materials.pdf"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

for u in urls:
    try:
        r = requests.get(u, headers=headers, timeout=10, verify=False)
        print(f"[{r.status_code}] {u}")
    except Exception as e:
        print(f"[ERROR] {u}: {e}")

