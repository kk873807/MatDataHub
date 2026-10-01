import pdfplumber
pdf=pdfplumber.open('brochure.pdf')
print('Pages:', len(pdf.pages))
for i in range(min(15, len(pdf.pages))):
    t = pdf.pages[i].extract_tables()
    if t:
        print(f'Page {i} has {len(t)} tables')
        print(f'Sample table 1 on page {i}:', t[0][0])
