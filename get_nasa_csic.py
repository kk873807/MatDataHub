
import requests
import fitz  # PyMuPDF
import io

url = "https://ntrs.nasa.gov/api/citations/20020072848/downloads/20020072848.pdf"
try:
    r = requests.get(url, verify=False, timeout=15)
    pdf = fitz.open(stream=r.content, filetype="pdf")
    for page in pdf:
        text = page.get_text()
        if "CVI" in text or "C/SiC" in text or "Tensile" in text:
            print(text)
except Exception as e:
    print(e)


