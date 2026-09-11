import os
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 15)
        self.cell(0, 10, 'MatDataHub Admin Guide: Adding Materials', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font("Arial", 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font("Arial", '', 11)
        self.multi_cell(0, 6, body)
        self.ln(4)

def generate_guide():
    pdf = PDF()
    pdf.add_page()
    
    pdf.chapter_title('1. Introduction')
    pdf.chapter_body('This guide explains how to add new materials to the MatDataHub database. '
                     'As an administrator, you can add materials individually using the form, or in bulk '
                     'by uploading a CSV or Excel (.xlsx) file.')

    pdf.chapter_title('2. Single Material Add')
    pdf.chapter_body('Navigate to the "Manage Materials" tab in the Admin Dashboard. '
                     'Fill in the necessary fields such as Name, Category, Description, and any relevant '
                     'mechanical or thermal properties. Blank fields will be ignored and stored as empty '
                     'in the database, allowing for incomplete data entry. Click "Create Material" when done.')

    pdf.chapter_title('3. Bulk Uploading (CSV / Excel)')
    pdf.chapter_body('To upload multiple materials at once, prepare a spreadsheet (.csv or .xlsx). '
                     'The column headers in the first row MUST match the internal database property names exactly.')
    
    pdf.chapter_title('4. Accepted Column Headers')
    headers = (
        'Required/Common fields:\n'
        ' - name (e.g., "Inconel 718")\n'
        ' - category (e.g., "Metals", "Polymers")\n'
        ' - subcategory (e.g., "Superalloys", "Thermoplastics")\n'
        ' - description\n'
        ' - standard\n'
        ' - grade\n\n'
        'Properties (Numeric values only. Leave blank if unknown):\n'
        ' - yield_strength_min, yield_strength_max\n'
        ' - tensile_strength_min, tensile_strength_max\n'
        ' - elastic_modulus\n'
        ' - hardness_value\n'
        ' - density\n'
        ' - max_service_temp\n'
        ' - thermal_conductivity\n'
        ' - specific_heat\n'
        ' - melting_point\n'
        ' - embodied_carbon\n'
        ' - water_usage\n'
        ' - cost_per_kg_min\n\n'
        'Note: If a property is not mentioned or left blank in the spreadsheet, it will remain blank in the database.'
    )
    pdf.chapter_body(headers)
    
    pdf.chapter_title('5. Automating Material Prices')
    pdf.chapter_body('To keep prices updated and build user trust, material prices can be automated via scheduled '
                     'scraping or API integration (e.g., LME or COMEX). This automation periodically fetches '
                     'latest prices and inserts them into the PriceHistory table, ensuring historic traceability '
                     'and updating the visible cost_per_kg_min field. This provides transparency to the users '
                     'that the prices are up to date.')

    pdf.output("Admin_Material_Upload_Guide.pdf")

if __name__ == "__main__":
    generate_guide()
    print("Guide generated successfully!")
