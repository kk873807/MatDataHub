
import requests
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urls = [
    "https://www.makeitfrom.com/material-properties/Epoxy",
    "http://www.matweb.com/search/datasheettext.aspx?matguid=1c74545c91874b13a3e44f400cedfe39",
    "https://www.matweb.com/search/datasheettext.aspx?matguid=956da5edc80f4c62a72c15ca2b923494",
    "https://en.wikipedia.org/wiki/FR-4",
    "https://www.plasticsintl.com/products/laminate-g-10fr-4-glass-epoxy",
    "https://www.ulprospector.com/plastics/en/datasheet/112876/acculam-epoxyglas-g10-fr4",
    "https://www.makeitfrom.com/material-properties/NEMA-Industrial-Laminate",
    "https://www.matweb.com/search/DataSheet.aspx?MatGUID=035d2130b7f34d918e8d590659b85cb7",
    "http://www.performance-composites.com/carbonfibre/mechanicalproperties_2.asp",
    "https://acpcomposites.com/wp-content/uploads/2024/05/Mechanical-Properties-of-Carbon-Fiber-Composite-Materials.pdf",
    "https://assets.rs-online.com/v1699614257/Datasheets/94dbd134a6050eb5ac2e6e0ad5307516.pdf",
    "https://www.makeitfrom.com/material-properties/Rigid-Thermoset-Polyurethane-RPU",
    "https://sawbones.com/solid-rigid-polyurethane-foam-properties/",
    "https://dragonplate.com/Images/uploaded/PDFs/FR-3706-TDS%20LASTAFOAM%20technical%20data%20sheet.pdf",
    "https://cdn.shopify.com/s/files/1/0076/1856/0097/files/U150-ENG_1.pdf",
    "https://www.makeitfrom.com/material-properties/Polyurethane-Rubber-AU-EU",
    "https://www.makeitfrom.com/material-properties/Melamine-Formaldehyde-MF",
    "https://www.makeitfrom.com/material-properties/Melamine-Formaldehyde-Moulding-Compound",
    "https://www.britannica.com/technology/melamine-formaldehyde-resin",
    "https://www.makeitfrom.com/material-properties/Urea-Formaldehyde-UF",
    "https://www.bpf.co.uk/plastipedia/polymers/Default.aspx",
    "https://romar-voss.nl/downloads/tds/tds-derakane-signia-411-resin.pdf",
    "https://www.freemansupply.com/datasheets/derakane.pdf",
    "https://www.ulprospector.com/plastics/en/datasheet/7516/derakane-411-45",
    "https://www.makeitfrom.com/material-properties/Unsaturated-Polyester-UP",
    "https://omnexus.specialchem.com/product-categories/thermosets-upr-unsaturated-polyester-resin"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=10, verify=False)
        print(f"[{r.status_code}] {url}")
    except Exception as e:
        print(f"[ERROR] {url} - {str(e)}")
    time.sleep(0.3)

