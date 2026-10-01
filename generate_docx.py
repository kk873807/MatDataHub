from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import datetime

doc = Document()

# --- Page margins ---
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

# --- Styles ---
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
font.color.rgb = RGBColor(0x33, 0x33, 0x33)

for level in range(1, 4):
    h_style = doc.styles[f'Heading {level}']
    h_style.font.name = 'Calibri'
    h_style.font.color.rgb = RGBColor(0x1a, 0x1a, 0x2e)

def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shading = cell._element.get_or_add_tcPr()
        bg = shading.makeelement(qn('w:shd'), {
            qn('w:val'): 'clear',
            qn('w:color'): 'auto',
            qn('w:fill'): '1a1a2e'
        })
        shading.append(bg)
    # Data rows
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
        # Alternate row shading
        if r_idx % 2 == 0:
            for c_idx in range(len(headers)):
                shading = table.rows[r_idx + 1].cells[c_idx]._element.get_or_add_tcPr()
                bg = shading.makeelement(qn('w:shd'), {
                    qn('w:val'): 'clear',
                    qn('w:color'): 'auto',
                    qn('w:fill'): 'f0f4f8'
                })
                shading.append(bg)
    return table

def add_checkbox(doc, text, checked=False):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    symbol = "☐ " if not checked else "☑ "
    run = p.add_run(symbol + text)
    run.font.size = Pt(10)

def add_callout(doc, text, color_hex='FFF3CD', border_hex='F0AD4E'):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x85, 0x63, 0x04)
    run.bold = True
    # Background shading
    pPr = p._element.get_or_add_pPr()
    shd = pPr.makeelement(qn('w:shd'), {
        qn('w:val'): 'clear',
        qn('w:color'): 'auto',
        qn('w:fill'): color_hex
    })
    pPr.append(shd)

# ===== TITLE PAGE =====
for _ in range(6):
    doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run("CBAM Engine")
run.bold = True
run.font.size = Pt(36)
run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x2e)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run("Launch Readiness Assessment")
run.font.size = Pt(20)
run.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

doc.add_paragraph()

meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = meta.add_run(f"MatDataHub · {datetime.date.today().strftime('%B %d, %Y')}")
run.font.size = Pt(12)
run.font.color.rgb = RGBColor(0x94, 0xa3, 0xb8)

meta2 = doc.add_paragraph()
meta2.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = meta2.add_run("Based on adversarial QA testing across ~200 synthetic rows")
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x94, 0xa3, 0xb8)

meta3 = doc.add_paragraph()
meta3.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = meta3.add_run("CONFIDENTIAL — INTERNAL USE ONLY")
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0xDC, 0x26, 0x26)
run.bold = True

doc.add_page_break()

# ===== EXECUTIVE SUMMARY =====
doc.add_heading('Executive Summary', level=1)

p = doc.add_paragraph()
p.add_run("The CBAM calculation engine has been rigorously tested through multiple adversarial fix cycles against independent hand-built answer keys. ").font.size = Pt(11)
run = p.add_run("The engine logic is verified and trustworthy for scenario modeling, supplier risk assessment, and internal budgeting.")
run.bold = True
run.font.size = Pt(11)

p = doc.add_paragraph()
p.add_run("Four gaps remain between the current state and production readiness as a system of record for actual EU customs filings. This document details each gap, its risk level, and concrete remediation steps.").font.size = Pt(11)

doc.add_paragraph()

add_table(doc,
    ["Posture", "Prerequisites", "Use Case"],
    [
        ["Launch Now", "Add disclaimers", "Planning & estimation tool"],
        ["System of Record", "Gap 3 (defaults) + Gap 4 (sign-off)", "Actual CBAM tax filings"],
        ["Global Scale", "Gap 1 (performance) + Gap 2 (security)", "Multi-tenant production SaaS"],
    ]
)

doc.add_page_break()

# ===== VERIFIED CAPABILITIES =====
doc.add_heading('Section 1: Verified Capabilities', level=1)
doc.add_paragraph("The following capabilities have been independently verified with per-row reconciliation against hand-built answer keys:")

add_table(doc,
    ["Capability", "Evidence", "Status"],
    [
        ["Carbon factor application (direct-only vs direct+indirect by sector)", "Steel/Al direct, Cement/Fert both", "✓ Verified"],
        ["CBAM cost netting against domestic carbon prices", "Carbon price floor, €75 reference, boundary cases", "✓ Verified"],
        ["EU/EEA origin exemptions (Iceland, Liechtenstein, Norway, Switzerland)", "XF-03/04/05/06, EX-03", "✓ Verified"],
        ["EU-27 destination scope (EFTA excluded from destination list)", "EX-03 Switzerland destination fix", "✓ Verified"],
        ["Transitional → Definitive phase boundary (pre-2026 = €0)", "DT-01 through DT-06", "✓ Verified"],
        ["50-tonne de minimis threshold (row-level, sector-aware)", "threshold_A and threshold_B CSVs", "✓ Verified"],
        ["Phase-in year toggle (2.5% / 5% / 100%)", "Dashboard reconciliation across all three views", "✓ Verified"],
        ["Plausibility bounds (50 t/t, sector-scoped)", "IN-06 steel indirect correctly ignored", "✓ Verified"],
        ["Input sanitisation (Inf, NaN, negatives, formula injection)", "Full edge-case suite", "✓ Verified"],
        ["Duplicate ID detection (case + whitespace insensitive)", "EDGE-DUP variants", "✓ Verified"],
        ["CN code validation (including 2507 cement scope)", "SC-05 calcined kaolinic clay", "✓ Verified"],
        ["ESG scoring (data quality, lead time, geopolitical, supplier risk)", "ES-00/11/12 spread (10/5/0 points)", "✓ Verified"],
        ["Missing-field flagging without blocking math", "Design-intentional flag-but-don't-exclude", "✓ Verified"],
        ["Dashboard ↔ CSV export reconciliation", "Both v2 and v3 datasets, to the kilogram", "✓ Verified"],
    ]
)

doc.add_page_break()

# ===== GAP 1: SCALE =====
doc.add_heading('Section 2: Gap Analysis', level=1)

doc.add_heading('Gap 1: Scale Testing', level=2)

p = doc.add_paragraph()
run = p.add_run("Risk Level: ")
run.bold = True
run = p.add_run("MEDIUM")
run.bold = True
run.font.color.rgb = RGBColor(0xF0, 0xAD, 0x4E)

doc.add_paragraph("All testing capped at approximately 120 rows. There is no signal on correctness or performance at real-world scale.")

doc.add_heading("What 'real-world' looks like:", level=3)
doc.add_paragraph("A mid-size EU importer: 2,000–10,000 BOM line items per year", style='List Bullet')
doc.add_paragraph("A large manufacturer: 50,000+ across multiple plants", style='List Bullet')
doc.add_paragraph("Concurrent API users uploading simultaneously", style='List Bullet')

doc.add_heading("Recommended Actions:", level=3)
add_checkbox(doc, "Generate a 10,000-row synthetic BOM with realistic distributions and verify totals reconcile")
add_checkbox(doc, "Profile process_bom() execution time and memory at 10K / 50K / 100K rows")
add_checkbox(doc, "Load-test the /api/v1/materials/bom-analyze endpoint with concurrent uploads")
add_checkbox(doc, "Add streaming/chunked processing if single-file memory exceeds acceptable limits")

doc.add_paragraph()

# ===== GAP 2: SECURITY =====
doc.add_heading('Gap 2: Security Beyond the Data Layer', level=2)

p = doc.add_paragraph()
run = p.add_run("Risk Level: ")
run.bold = True
run = p.add_run("MEDIUM")
run.bold = True
run.font.color.rgb = RGBColor(0xF0, 0xAD, 0x4E)

doc.add_paragraph("CSV-injection and input sanitisation are verified. Authentication, authorization, data isolation, and API hardening are untested. For a tool handling confidential supplier and pricing data, this is not optional before a global launch.")

doc.add_heading("Recommended Actions:", level=3)
add_checkbox(doc, "Pen-test the API endpoints (auth bypass, IDOR, rate limiting under load)")
add_checkbox(doc, "Verify tenant data isolation — one customer's BOM must never leak to another")
add_checkbox(doc, "Audit token handling, session management, and credential storage")
add_checkbox(doc, "Review CORS, CSP headers, and HTTPS enforcement")
add_checkbox(doc, "Confirm GDPR compliance for storing supplier names, pricing, and country data")

doc.add_paragraph()

# ===== GAP 3: DEFAULT VALUES =====
doc.add_heading('Gap 3: Default Values Are Outdated', level=2)

p = doc.add_paragraph()
run = p.add_run("Risk Level: ")
run.bold = True
run = p.add_run("CRITICAL")
run.bold = True
run.font.color.rgb = RGBColor(0xDC, 0x26, 0x26)

add_callout(doc, "⚠  HIGHEST PRIORITY — The definitive CBAM period started 1 January 2026. The fallback factors in the engine (steel 2.01, hydrogen 10.4, etc.) are transitional-period values from 2023. The Commission has published new country- and product-specific defaults with mandatory markups: +10% in 2026, +20% in 2027, +30% in 2028. Any company relying on fallback values will systematically understate their CBAM liability.")

doc.add_heading("Impact:", level=3)
add_table(doc,
    ["Year", "Markup", "Example: Steel Default"],
    [
        ["2025 (transitional)", "0%", "2.01 t/t (current engine value)"],
        ["2026 (definitive)", "+10%", "~2.21 t/t"],
        ["2027", "+20%", "~2.41 t/t"],
        ["2028", "+30%", "~2.61 t/t"],
    ]
)

doc.add_paragraph()
doc.add_heading("Recommended Architecture:", level=3)

doc.add_paragraph("The hardcoded FALLBACK_CARBON_FACTORS dictionary should be replaced with a database-backed lookup pipeline:")

steps = [
    ("Data Source", "Commission-published Excel files containing country × CN code × year default values"),
    ("ETL Pipeline", "A script or admin endpoint that ingests these Excel files into a cbam_defaults database table"),
    ("Database Table", "Keyed on (cn_code_prefix, origin_country, year), with the year-specific markup already applied"),
    ("Runtime Lookup", "process_bom() queries this table first; falls back to the hardcoded dict only if the CN/country combo is missing"),
    ("Audit Column", "New Emissions_Source values: COMMISSION_DEFAULT vs SUPPLIED vs LEGACY_FALLBACK"),
    ("Staleness Check", "Warn if the defaults table hasn't been refreshed in >90 days"),
]
for title_text, desc in steps:
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(f"{title_text}: ")
    run.bold = True
    run.font.size = Pt(10)
    run = p.add_run(desc)
    run.font.size = Pt(10)

doc.add_heading("Action Items:", level=3)
add_checkbox(doc, "Download the Commission's current definitive-period default value Excel files")
add_checkbox(doc, "Build a cbam_defaults database table keyed on (cn_code_prefix, origin_country, year)")
add_checkbox(doc, "Apply the year-specific markup (+10%/+20%/+30%) automatically")
add_checkbox(doc, "Modify process_bom() to query this table first, falling back to the dict as last resort")
add_checkbox(doc, "Build an admin endpoint or script to re-import when the Commission publishes updates")
add_checkbox(doc, "Add a staleness check: warn if defaults haven't been refreshed in >90 days")

doc.add_paragraph()

# ===== GAP 4: REGULATORY SIGN-OFF =====
doc.add_heading('Gap 4: External Regulatory Sign-Off', level=2)

p = doc.add_paragraph()
run = p.add_run("Risk Level: ")
run.bold = True
run = p.add_run("HIGH")
run.bold = True
run.font.color.rgb = RGBColor(0xDC, 0x26, 0x26)

doc.add_paragraph("All testing was adversarial QA using invented data and general knowledge — not a customs lawyer's or CBAM verifier's review. The definitive period now requires mandatory third-party verification by an accredited CBAM verifier for the data a company actually files.")

doc.add_heading("Specific Uncertainties Flagged During Testing:", level=3)
doc.add_paragraph("Whether iron ore and calcined kaolinic clay definitively fall under Annex I scope (best-guess inclusion)", style='List Bullet')
doc.add_paragraph("The exact boundary between 'reporting-only' and 'financially liable' for edge-case dates", style='List Bullet')
doc.add_paragraph("Whether the 50t de minimis threshold applies per-importer or per-declarant", style='List Bullet')

doc.add_heading("Action Items:", level=3)
add_checkbox(doc, "Engage a qualified CBAM advisor or trade-compliance firm to review the rule implementation")
add_checkbox(doc, "Cross-reference all CN code scope decisions against the official Annex I list")
add_checkbox(doc, "Add prominent disclaimers: 'For planning purposes only — not a substitute for professional CBAM advice'")
add_checkbox(doc, "Consider a 'compliance mode' toggle that adds conservative assumptions and flags all uncertainties")

doc.add_page_break()

# ===== SCOPE: MULTI-JURISDICTION =====
doc.add_heading('Section 3: Scope Decision — EU-Only vs Multi-Jurisdiction', level=1)

doc.add_paragraph("The current engine covers EU CBAM only, which already applies to any exporter worldwide shipping into the EU-27. 'Global' customer reach is inherent to the current feature.")

add_table(doc,
    ["Jurisdiction", "Status", "Timeline"],
    [
        ["EU CBAM", "Definitive period live", "January 2026 →"],
        ["UK CBAM", "Announced", "January 2027 →"],
        ["Australia CBAM", "Under consideration", "TBD"],
        ["Canada CBAM", "Under study", "TBD"],
    ]
)

doc.add_paragraph()
add_callout(doc, "ℹ  Adding UK CBAM support is new functionality requiring separate carbon pricing references, different CN/HS code mappings, and UK-specific exemption rules. It should not block EU launch but should be planned as a distinct feature track sharing the same database-backed architecture.", 'DBEAFE', '3B82F6')

doc.add_page_break()

# ===== RECOMMENDED LAUNCH POSTURE =====
doc.add_heading('Section 4: Recommended Launch Posture', level=1)

add_table(doc,
    ["Phase", "Prerequisites", "Use Case", "Timeline"],
    [
        ["Launch Now", "Add disclaimers to the UI", "Planning & estimation tool, supplier risk assessment, internal budgeting", "Immediate"],
        ["System of Record", "Gap 3 (current defaults) + Gap 4 (regulatory sign-off)", "Actual CBAM tax filings submitted to EU customs", "4–8 weeks"],
        ["Global Scale", "Gap 1 (performance) + Gap 2 (security hardening)", "Multi-tenant production SaaS with concurrent users", "8–12 weeks"],
    ]
)

doc.add_paragraph()

p = doc.add_paragraph()
run = p.add_run("Bottom Line: ")
run.bold = True
run.font.size = Pt(12)
run = p.add_run("The engine is trustworthy for what was tested. It should not calculate numbers a real company submits to EU customs until the default-value source is current and someone with real CBAM authority has signed off on it.")
run.font.size = Pt(11)

# ===== FOOTER =====
doc.add_paragraph()
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("— End of Document —")
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x94, 0xa3, 0xb8)
run.italic = True

# Save
output_path = r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\CBAM_Launch_Readiness.docx"
doc.save(output_path)
print(f"Document saved to: {output_path}")
