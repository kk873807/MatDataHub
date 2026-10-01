
import re
from bs4 import BeautifulSoup

def extract_props(path, name):
    print(f"\n--- {name} ---")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "Modulus of Rupture" in line or "Elastic Modulus" in line or "Crushing Strength" in line or "Shrinkage" in line:
            print(line.strip())

extract_props(r"C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\.system_generated\steps\1801\content.md", "Teak")
extract_props(r"C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\.system_generated\steps\1803\content.md", "Walnut")

