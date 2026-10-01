
import requests
import urllib3
urllib3.disable_warnings()

urls = [
    "https://www.dupont.com/content/dam/aramids/amer/us/en/safety/public/documents/en/Kevlar_Technical_Guide_0319.pdf",
    "https://norwegen-angelfreunde.de/attachment/26938-zugfestigkeit-pdf",
    "https://www.sciencedirect.com/science/article/abs/pii/S0142941819317568",
    "https://www.dsm.com/content/dam/dsm/dyneema/pt_BR/Downloads/LP%20Product%20Grades/DSM_Hard_Ballistic_solutions_BR.pdf",
    "https://www.toyobo-mc.jp/wordpress/wp-content/uploads/2023/09/hp_fiber_data_zylon_en.pdf",
    "https://www.lookpolymers.com/pdf/Toyobo-Zylon-HM-FiberEpoxy-Matrix-Unidirectional-Composite.pdf",
    "https://en.wikipedia.org/wiki/Zylon"
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

