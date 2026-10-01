
import urllib.request
import io
import fitz # PyMuPDF
import sys

urls = {
    "HBS 600": "https://www.thyssenkrupp-steel.com/media/content_1/publikationen/precision_steel/produktinformationen_1/bainitischer_stahl/thyssenkrupp_precidur_hbs_600_pr_624_precision_steel_en.pdf",
    "HBS 800": "https://www.thyssenkrupp-steel.com/media/content_1/publikationen/precision_steel/produktinformationen_1/bainitischer_stahl/thyssenkrupp_hbs-800_product_information_precision_steel_en.pdf",
    "FB-W 300Y450T": "https://www.thyssenkrupp-steel.com/media/content_1/publikationen/produktinformationen/fb_w/thyssenkrupp_fb-w_product_information_steel_en_08-2016_01.pdf",
    "Bainidur 7980 CN": "https://www.dew-powder.com/fileadmin/files/metallpulver.de/documents/Publikationen/Deutsch/2020-05-07_Bainidur_7980_CN_DE.pdf",
    "T24": "https://www.czasopisma.pan.pl//Content/87592/PDF/10172%20Volume%2058%20Issue%203-6%20paper.pdf.pdf"
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        pdf_data = urllib.request.urlopen(req).read()
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        print(f"--- {name} ---")
        lines = text.split("\n")
        # Extract lines with numbers or keywords to keep output small
        for line in lines:
            line_lower = line.lower()
            if any(k in line_lower for k in ["yield", "tensile", "strength", "elongation", "mpa", "n/mm"]):
                print(line.strip())
    except Exception as e:
        print(f"Failed {name}: {e}")

