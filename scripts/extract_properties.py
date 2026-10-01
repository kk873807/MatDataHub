#!/usr/bin/env python3
import csv
import sys
import time
import argparse
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "mat-data-hub-property-extractor/1.0 (+https://mat-data-hub.vercel.app)"
}
DELAY = 1.0
TIMEOUT = 20

def load_targets(csv_path, limit=None):
    rows = [r for r in csv.DictReader(open(csv_path, encoding="utf-8"))
            if r.get("source_name") not in ("Materials Project",)
            and r.get("source_url") and "makeitfrom.com" in r.get("source_url")]
    return rows[:limit] if limit else rows

def parse_property_page(html, material_name, source_url):
    soup = BeautifulSoup(html, "html.parser")
    out = []
    
    # 1. Alloy Composition (tables)
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) >= 3:
            name_td = tds[0]
            # e.g. Iron (Fe) -> grab the first text element or just the text
            prop = name_td.get_text(separator=' ', strip=True)
            # MakeItFrom usually has "Iron (Fe) Fe", let's just grab the whole text and we can clean it later
            val = tds[-1].get_text(strip=True)
            if prop and val and any(char.isdigit() for char in val):
                out.append({
                    "material_name": material_name, "category": "Alloy Composition",
                    "property": prop, "value": val, "unit": "%",
                    "value_imperial": None, "unit_imperial": None, "source_url": source_url
                })

    # 2. Properties (divs with class mech, therm, elec, other, calc)
    for div in soup.find_all('div', class_=['mech', 'therm', 'elec', 'other', 'calc']):
        ps = div.find_all('p', recursive=False)
        if len(ps) >= 2:
            prop_name = ps[0].get_text(strip=True)
            val_p = ps[-1]
            
            imperial_span = val_p.find('span', class_='float-right')
            imp_val = None
            imp_unit = None
            if imperial_span:
                imp_i = imperial_span.find('i')
                imp_unit = imp_i.get_text(separator='', strip=True) if imp_i else None
                if imp_i: imp_i.extract()
                imp_val = imperial_span.get_text(strip=True)
                imperial_span.extract()
                
            met_i = val_p.find('i')
            met_unit = met_i.get_text(separator='', strip=True) if met_i else None
            if met_i: met_i.extract()
            met_val = val_p.get_text(strip=True)
            
            cat_classes = div.get('class', [])
            cat = "Otherwise Unclassified Properties"
            if 'mech' in cat_classes: cat = "Mechanical Properties"
            elif 'therm' in cat_classes: cat = "Thermal Properties"
            elif 'elec' in cat_classes: cat = "Electrical Properties"
            elif 'calc' in cat_classes: cat = "Common Calculations"
            
            out.append({
                "material_name": material_name, "category": cat,
                "property": prop_name, "value": met_val, "unit": met_unit,
                "value_imperial": imp_val, "unit_imperial": imp_unit, "source_url": source_url
            })
            
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    targets = load_targets(args.csv_path, args.limit)
    print(f"extracting properties for {len(targets)} materials...")

    all_rows, failed = [], []
    with requests.Session() as s:
        s.headers.update(HEADERS)
        for i, row in enumerate(targets, 1):
            name, url = row["material_name"], row["source_url"]
            try:
                r = s.get(url, timeout=TIMEOUT)
                if r.status_code != 200:
                    print(f"  ! {name}: HTTP {r.status_code}")
                    failed.append(name)
                    continue
                props = parse_property_page(r.text, name, url)
                if not props:
                    print(f"  ! {name}: 0 properties parsed - check page structure manually")
                    failed.append(name)
                else:
                    all_rows.extend(props)
            except Exception as e:
                print(f"  ! {name}: {e}")
                failed.append(name)
            if i % 20 == 0:
                print(f"  {i}/{len(targets)}")
            time.sleep(DELAY)

    if all_rows:
        with open("extracted_properties.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
            w.writeheader()
            w.writerows(all_rows)
        print(f"\nwrote extracted_properties.csv "
              f"({len(all_rows)} property rows across "
              f"{len(set(r['material_name'] for r in all_rows))} materials)")

if __name__ == "__main__":
    main()
