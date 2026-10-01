
import requests
import time

urls = [
    "https://ca.electro-wind.com/web-files/Sabic/ultem-datasheet.pdf",
    "https://protolabs.com/media/g3ehzag1/ryton-r-4-200na.pdf",
    "https://drakeplastics.com/wp-content/uploads/2016/01/Torlon-4203L.pdf",
    "https://www.synflex.com/tr/insulate/syntherm-isolierstoffe/ayrinti/datasheets/kaptonr-hn-polyimidfolie-46/",
    "https://docs.rs-online.com/f265/A700000014060820.pdf",
    "https://www.makeitfrom.com/material-properties/Liquid-Crystal-Polymer-LCP",
    "https://download.basf.com/p1/8a8081c57fd4b609017fd664c4583e10/de/ULTRASON%25C2%25AE_E2010_NATURAL",
    "https://protolabs.com/media/b2rj51rq/udel-p1700.pdf",
    "https://plasticker.de/docs/recybase/943_1756291360.pdf",
    "https://hpp.arkema.com/assets/arkema/TDS%20ARKEMA%20KEPSTAN%20serie%206000.pdf",
    "https://www.makeitfrom.com/material-properties/Polyphthalamide-PPA",
    "https://www.professionalplastics.com/professionalplastics/content/downloads/PTFE_FEP_PFA.pdf",
    "https://wkfluidhandling.com/wp-content/media/materials/pfa-perfluoroalkoxy.pdf",
    "https://www.makeitfrom.com/material-properties/Polyvinylidene-Fluoride-PVDF",
    "https://www.makeitfrom.com/compare/Ethylene-Tetrafluoroethylene-ETFE/Polyvinyl-Fluoride-PVF",
    "https://betaplastics.ulprospector.com/plastics/zh-cn/datasheet/436530/tefzel-etfe-ht-2162"
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

