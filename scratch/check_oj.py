from bs4 import BeautifulSoup
import re

html_path = "data/cbam_official/32026R1740.html"
with open(html_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")

targets = [
    "7226 99", # Vietnam
    "3105 51 00", # Ukraine
    "2804 10 00", # Brunei
    "7603", # Bolivia
    "7301", # Global
    "7306 21 00", # Taiwan
    "2523 29 00", # Tajikistan
    "7306 40 20", # Mexico
    "7209", # Uzbekistan
    "7306 11 00", # New Zealand
    "7304 49", # Indonesia
    "7220 11 00", # Ukraine
    "7214 91", # Ukraine
    "7304 24 00", # Uzbekistan
    "7318 23 00", # Australia
]

for table in soup.find_all("table"):
    for row in table.find_all("tr"):
        text = row.get_text(separator=" ", strip=True)
        for t in targets:
            if t in text:
                print(f"Match for {t}:")
                # print the columns
                cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
                if len(cols) > 2:
                    print(" | ".join(cols))
