
import requests
url = "https://archive.org/wayback/available?url=https://www-eng.lbl.gov/~shuman/NEXT/MATERIALS%26COMPONENTS/MISC/AlSiC_Metal-Matrix-Composite-Datasheet.pdf"
r = requests.get(url, verify=False)
print(r.json())

