
import requests
r = requests.get("https://www.wood-database.com/east-indian-rosewood/", headers={"User-Agent": "Mozilla/5.0"}, verify=False)
print(f"Status: {r.status_code}")

