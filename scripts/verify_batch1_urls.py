import requests
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

urls = [
    (1, "AISI 1018 Steel", "https://www.makeitfrom.com/material-properties/SAE-AISI-1018-G10180-Carbon-Steel"),
    (3, "AISI 1018 Steel (Cold Drawn)", "https://www.makeitfrom.com/material-properties/Cold-Drawn-1018-Carbon-Steel"),
    (4, "AISI 1018 Steel (Hot Rolled)", "https://www.makeitfrom.com/material-properties/Hot-Rolled-1018-Carbon-Steel"),
    (6, "AISI 1045 Steel", "https://www.makeitfrom.com/material-properties/SAE-AISI-1045-S45C-G10450-Carbon-Steel"),
    (7, "AISI 1045 Steel (Annealed)", "https://www.makeitfrom.com/material-properties/Annealed-and-Cold-Drawn-1045-Carbon-Steel"),
    (8, "AISI 1045 Steel (Cold Drawn)", "https://www.makeitfrom.com/material-properties/Cold-Drawn-1045-Carbon-Steel"),
    (9, "AISI 1045 Steel (Hot Rolled)", "https://www.makeitfrom.com/material-properties/Hot-Rolled-1045-Carbon-Steel"),
    (10, "AISI 1045 Steel (Q&T)", "https://dl.asminternational.org/alloy-digest/article/20/10/CS-44/1863/AISI-1045Medium-Carbon-Steel"),
    # 4130 group
    (11, "AISI 4130 Steel", "https://www.makeitfrom.com/material-properties/SAE-AISI-4130-SCM430-G41300-Cr-Mo-Steel"),
    (12, "AISI 4130 Steel (Annealed)", "https://www.makeitfrom.com/material-properties/Annealed-SAE-AISI-4130-Cr-Mo-Steel"),
    (13, "AISI 4130 Steel (Cold Drawn)", "https://www.makeitfrom.com/material-properties/Cold-Finished-SAE-AISI-4130-Cr-Mo-Steel"),
    (14, "AISI 4130 Steel (Hot Rolled)", "https://www.makeitfrom.com/material-properties/Normalized-SAE-AISI-4130-Cr-Mo-Steel"),
    (15, "AISI 4130 Steel (Q&T)", "https://www.makeitfrom.com/material-properties/Quenched-and-Tempered-SAE-AISI-4130-Cr-Mo-Steel"),
    # 4140 group
    (16, "AISI 4140 Steel", "https://www.makeitfrom.com/material-properties/SAE-AISI-4140-SCM440-G41400-Cr-Mo-Steel"),
    (17, "AISI 4140 Steel (Annealed)", "https://www.makeitfrom.com/material-properties/Annealed-SAE-AISI-4140-Cr-Mo-Steel"),
    (18, "AISI 4140 Steel (Cold Drawn)", "https://www.makeitfrom.com/material-properties/Cold-Finished-SAE-AISI-4140-Cr-Mo-Steel"),
    (19, "AISI 4140 Steel (Hot Rolled)", "https://icme.hpc.msstate.edu/mediawiki/index.php/Mechanical_properties_of_4140_steel.html"),
    (20, "AISI 4140 Steel (Q&T)", "https://www.makeitfrom.com/material-properties/Quenched-and-Tempered-SAE-AISI-4140-Cr-Mo-Steel"),
    # 4340 group
    (21, "AISI 4340 Steel", "https://www.makeitfrom.com/material-properties/SAE-AISI-4340-SNCM439-G43400-Ni-Cr-Mo-Steel"),
    (22, "AISI 4340 Steel (Annealed)", "https://www.makeitfrom.com/material-properties/Annealed-SAE-AISI-4340-Ni-Cr-Mo-Steel"),
    (23, "AISI 4340 Steel (Cold Drawn)", "https://www.makeitfrom.com/material-properties/Cold-Finished-SAE-AISI-4340-Ni-Cr-Mo-Steel"),
    (24, "AISI 4340 Steel (Hot Rolled)", "https://www.makeitfrom.com/material-properties/Normalized-SAE-AISI-4340-Ni-Cr-Mo-Steel"),
    (25, "AISI 4340 Steel (Q&T)", "https://www.makeitfrom.com/material-properties/Quenched-and-Tempered-SAE-AISI-4340-Ni-Cr-Mo-Steel"),
]

print(f"Verifying {len(urls)} URLs...\n")

for num, name, url in urls:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        final_url = resp.url
        redirected = " -> REDIRECTED to " + final_url if final_url != url else ""
        
        # Check if the page title contains something relevant
        title = ""
        if resp.status_code == 200 and "makeitfrom.com" in url:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, "html.parser")
            t = soup.find("title")
            if t:
                title = t.text.strip()[:80]
        
        status = "OK" if resp.status_code == 200 else f"HTTP {resp.status_code}"
        title_str = f' | Title: "{title}"' if title else ""
        print(f"[{status}] #{num} {name}{redirected}{title_str}")
        
    except Exception as e:
        print(f"[ERROR] #{num} {name} -> {str(e)[:100]}")
    
    time.sleep(0.5)
