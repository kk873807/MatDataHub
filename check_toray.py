
import requests
import urllib3
urllib3.disable_warnings()

variants = [
    "https://www.toraycma.com/wp-content/uploads/T300-Technical-Data-Sheet.pdf",
    "https://www.toraycma.com/wp-content/uploads/T300-Data-Sheet.pdf",
    "https://www.toraycma.com/file_viewer.php?id=3912"
]
for v in variants:
    r = requests.head(v, headers={"User-Agent":"Mozilla"}, verify=False)
    print(f"[{r.status_code}] {v}")

r = requests.head("https://wichita.edu/industry_and_defense/NIAR/Research/hexcel-8552/IM7-Unitape-2.pdf", headers={"User-Agent":"Mozilla"}, verify=False)
print(f"[{r.status_code}] IM7 Unitape (no www)")

