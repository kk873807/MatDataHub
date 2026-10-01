
import requests
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urls = [
    "https://www.makeitfrom.com/material-properties/Ethylene-Propylene-Diene-Rubber-EPDM-EPT",
    "https://o-ring.info/en/o-ring/technical%20handbook/06%20-%20eriks%20nv%20-%20o-ring%20technical%20handbook%20-%20basic%20elastomers.pdf",
    "https://allsealsinc.com/pdfs/dichtomatik_oring_handbook.pdf",
    "https://en.wikipedia.org/wiki/EPDM_rubber",
    "https://www.makeitfrom.com/material-properties/Acrylonitrile-Nitrile-Butadiene-Rubber-NBR-Buna-N",
    "https://en.wikipedia.org/wiki/Nitrile_rubber",
    "http://allsealsinc.com/03_Elastomers-Materials.pdf",
    "https://www.makeitfrom.com/material-properties/Hydrogenated-Acrylonitrile-Butadiene-Rubber-HNBR-HSN",
    "https://trp.co.uk/materials/datasheets/",
    "https://www.makeitfrom.com/material-properties/Styrene-Butadiene-Rubber-SBR-Buna-S",
    "https://www.makeitfrom.com/material-properties/Fluorocarbon-Rubber-FKM-FPM",
    "https://www.viton.com/en/-/media/files/viton/viton-selection-guide.pdf",
    "https://www.parker.com/us/en/divisions/o-ring-and-engineered-seals-division/resources/oring-ehandbook/oring-elastomers/material-selection-guide.html",
    "https://www.makeitfrom.com/material-properties/Perfluoroelastomer-FFKM",
    "https://www.dymseal.com/pdf/Kalrez%20Physical%20Properties%20&%20Compound%20Comparisons.pdf",
    "https://www.parrinst.com/wp-content/uploads/downloads/2011/07/Parr_DuPont-Kalrez-O-ring-Materials-Corrosion-Info.pdf",
    "https://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=93",
    "https://www.makeitfrom.com/material-properties/Chlorosulfonated-Polyethylene-Rubber-CSM",
    "https://www.makeitfrom.com/material-properties/Polyacrylate-Rubber-ACM",
    "https://download.basf.com/p1/8a8082587fd4b608017fd6411cdd6d63/en/Elastollan%3Csup%3E%C2%AE%3Csup%3E_%E2%80%93_Thermoplastic_Polyurethane_Elastomers_%28TPU%29_-_Product_Range_Range_Chart_English.pdf",
    "https://omnexus.specialchem.com/product-categories/tpes-tpvs-tpu-or-tpe-u-thermoplastic-polyurethane-tpu-ester-ether",
    "https://www.americanchemistry.com/content/download/4863/file/Thermoplastic-Polyurethanes-Bridge-The-Gap-Between-Rubber-and-Plastics.pdf",
    "https://www.hexpol.com/tpe/?p=3884",
    "https://business.specialchem.com/blog/top-25-most-popular-plastics-and-elastomers-on-specialchem",
    "https://upmold.com/wp-content/uploads/data-sheet/TPV-Santoprene_101-73.pdf",
    "https://www.phmolds.com/wp-content/uploads/2016/09/TPV-ExxonMobil-Santoprene-101-80-Black.pdf",
    "https://www.phmolds.com/wp-content/uploads/2016/09/TPV-ExxonMobil-Santoprene-101-64-Black.pdf",
    "https://en.wikipedia.org/wiki/Thermoplastic_vulcanizates"
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

