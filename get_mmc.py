
import requests
import fitz  # PyMuPDF
import io

url = "https://cpstechnologysolutions.com/wp-content/uploads/2025/09/CPS-Alsic-2025-Final.pdf"
r = requests.get(url, verify=False)
pdf = fitz.open(stream=r.content, filetype="pdf")
for page in pdf:
    print(page.get_text())


