
import requests
import urllib3
urllib3.disable_warnings()

url = "https://www.agy.com/wp-content/uploads/2021/12/933_S-2_Glass_Roving.pdf"
try:
    r = requests.get(url, headers={"User-Agent": "Mozilla"}, verify=False)
    print(r.status_code)
except Exception as e:
    pass

