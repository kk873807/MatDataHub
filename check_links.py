
import requests
import time

urls = [
    "https://xometry.asia/wp-content/uploads/2021/03/1770691110-Nylon-6.pdf",
    "https://www.goodfellow.com/usa/rilsan-bmntld-nylon-11-rod-group",
    "https://hpp.arkema.com/assets/arkema/TDS_RILSAN%C2%AE%20PA11%20T%20GREY%207310%20AC_ko_WW.pdf",
    "https://www.bopla.de/fileadmin/product_data/00_Materialdatenblaetter/PA_12_LR7MHI_Vestamid/PA_DB_12_LR7MHI_Vestamid.pdf",
    "https://hpp.arkema.com/assets/arkema/TDS_RILSAMID%C2%AE%20AESNO%20MED_en_WW.pdf",
    "https://plasticsfinder.envalior.com/api/document/tech/Stanyl%C2%AE%20HGR3-W/O4uVuqP5d/en",
    "https://plasticker.de/docs/recybase/4089_1768399051.pdf",
    "https://plasticker.de/docs/recybase/31599_1724311132.pdf",
    "https://www.protolabs.com/media/ipwe0ehh/2026-026-cnc-material-data-sheet_ppe-ps-noryl-265.pdf",
    "https://www.protolabs.com/media/zlknjwmd/2026-026-cnc-material-data-sheet_pom-h.pdf",
    "https://www.curbellplastics.com/wp-content/uploads/2022/11/Acetal-Data-Sheet.pdf",
    "https://www.scribd.com/document/437515969/Polyacetal",
    "https://www.kkpc.com/download/?seq=7273",
    "https://www.makeitfrom.com/material-properties/Acrylonitrile-Styrene-Acrylate-ASA",
    "https://www.uniboxinfo.com/datasheets/terlux.pdf"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"[{r.status_code}] {url}")
    except Exception as e:
        print(f"[ERROR] {url} - {str(e)}")
    time.sleep(0.5)

