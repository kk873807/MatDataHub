"""
Seed the database with 25 real engineering materials.
Data sourced from public references (textbooks, manufacturer datasheets).

Usage:
    python -m scraper.seed_data

This clears existing data and inserts fresh materials.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import Material


MATERIALS = [
    # ═══════════════════════════════════════════
    #  CARBON & ALLOY STEELS
    # ═══════════════════════════════════════════
    {
        "name": "AISI 1018 Mild Steel",
        "category": "Metal", "subcategory": "Carbon Steel", "grade": "1018",
        "standard": "ASTM A108",
        "density": 7.87,
        "tensile_strength_min": 440, "tensile_strength_max": 490,
        "yield_strength_min": 370, "yield_strength_max": 390,
        "elongation": 15, "hardness": "126 HBW", "elastic_modulus": 205,
        "thermal_conductivity": 51.9, "specific_heat": 486,
        "melting_point_min": 1450, "melting_point_max": 1510,
        "cost_per_kg_min": 60, "cost_per_kg_max": 90, "cost_currency": "INR",
        "applications": "Shafts, pins, bolts, gears, machinery parts, general fabrication",
        "equivalent_grades": "C15 (EN), S15C (JIS), IS 1570 Grade 15C8",
        "composition": "Fe 98.8%, C 0.15-0.20%, Mn 0.60-0.90%",
        "source_name": "Textbook / ASM",
    },
    {
        "name": "AISI 1045 Medium Carbon Steel",
        "category": "Metal", "subcategory": "Carbon Steel", "grade": "1045",
        "standard": "ASTM A29",
        "density": 7.85,
        "tensile_strength_min": 565, "tensile_strength_max": 625,
        "yield_strength_min": 310, "yield_strength_max": 340,
        "elongation": 16, "hardness": "163 HBW", "elastic_modulus": 206,
        "thermal_conductivity": 49.8, "specific_heat": 486,
        "melting_point_min": 1410, "melting_point_max": 1460,
        "cost_per_kg_min": 65, "cost_per_kg_max": 100, "cost_currency": "INR",
        "applications": "Axles, crankshafts, connecting rods, hydraulic clamps",
        "equivalent_grades": "C45 (EN), S45C (JIS), IS 1570 Grade 45C8",
        "composition": "Fe 98.5%, C 0.43-0.50%, Mn 0.60-0.90%",
        "source_name": "Textbook / ASM",
    },
    {
        "name": "IS 2062 Grade E250A",
        "category": "Metal", "subcategory": "Structural Steel", "grade": "E250A",
        "standard": "IS 2062",
        "density": 7.85,
        "tensile_strength_min": 410, "tensile_strength_max": 410,
        "yield_strength_min": 250, "yield_strength_max": 250,
        "elongation": 23, "elastic_modulus": 200,
        "thermal_conductivity": 50, "specific_heat": 480,
        "melting_point_min": 1420, "melting_point_max": 1460,
        "cost_per_kg_min": 55, "cost_per_kg_max": 75, "cost_currency": "INR",
        "applications": "Bridges, buildings, general structural work (most common Indian structural steel)",
        "equivalent_grades": "ASTM A36, S275JR (EN), SS400 (JIS)",
        "composition": "Fe 98%, C 0.23% max, Mn 1.50% max, Si 0.40% max",
        "source_name": "BIS IS 2062",
    },

    # ═══════════════════════════════════════════
    #  STAINLESS STEELS
    # ═══════════════════════════════════════════
    {
        "name": "AISI 304 Stainless Steel",
        "category": "Metal", "subcategory": "Stainless Steel", "grade": "304",
        "standard": "ASTM A240",
        "density": 7.93,
        "tensile_strength_min": 515, "tensile_strength_max": 750,
        "yield_strength_min": 205, "yield_strength_max": 310,
        "elongation": 40, "hardness": "85 HRB", "elastic_modulus": 193,
        "thermal_conductivity": 16.2, "specific_heat": 500,
        "melting_point_min": 1400, "melting_point_max": 1455,
        "cost_per_kg_min": 250, "cost_per_kg_max": 400, "cost_currency": "INR",
        "applications": "Kitchen sinks, chemical tanks, food processing, medical instruments",
        "equivalent_grades": "SUS 304 (JIS), X5CrNi18-10 (EN), 08Cr18Ni10 (China)",
        "composition": "Fe 66-74%, Cr 18-20%, Ni 8-10.5%, Mn 2%",
        "source_name": "MatWeb",
    },
    {
        "name": "AISI 316 Stainless Steel",
        "category": "Metal", "subcategory": "Stainless Steel", "grade": "316",
        "standard": "ASTM A240",
        "density": 7.99,
        "tensile_strength_min": 515, "tensile_strength_max": 690,
        "yield_strength_min": 205, "yield_strength_max": 310,
        "elongation": 40, "hardness": "79 HRB", "elastic_modulus": 193,
        "thermal_conductivity": 16.3, "specific_heat": 500,
        "melting_point_min": 1375, "melting_point_max": 1400,
        "cost_per_kg_min": 320, "cost_per_kg_max": 550, "cost_currency": "INR",
        "applications": "Marine hardware, chemical processing, pharmaceutical equipment, surgical implants",
        "equivalent_grades": "SUS 316 (JIS), X5CrNiMo17-12-2 (EN)",
        "composition": "Fe 62-72%, Cr 16-18%, Ni 10-14%, Mo 2-3%",
        "source_name": "MatWeb",
    },
    {
        "name": "AISI 410 Stainless Steel",
        "category": "Metal", "subcategory": "Stainless Steel", "grade": "410",
        "standard": "ASTM A276",
        "density": 7.74,
        "tensile_strength_min": 450, "tensile_strength_max": 515,
        "yield_strength_min": 205, "yield_strength_max": 275,
        "elongation": 20, "hardness": "96 HRB", "elastic_modulus": 200,
        "thermal_conductivity": 24.9, "specific_heat": 460,
        "melting_point_min": 1480, "melting_point_max": 1530,
        "cost_per_kg_min": 200, "cost_per_kg_max": 350, "cost_currency": "INR",
        "applications": "Cutlery, steam turbine blades, valve trim, pump shafts",
        "equivalent_grades": "SUS 410 (JIS), X12Cr13 (EN)",
        "composition": "Fe 85%, Cr 11.5-13.5%, C 0.15% max",
        "source_name": "MatWeb",
    },

    # ═══════════════════════════════════════════
    #  ALUMINIUM ALLOYS
    # ═══════════════════════════════════════════
    {
        "name": "Aluminium 6061-T6",
        "category": "Metal", "subcategory": "Aluminium Alloy", "grade": "6061-T6",
        "standard": "ASTM B209",
        "density": 2.70,
        "tensile_strength_min": 290, "tensile_strength_max": 310,
        "yield_strength_min": 240, "yield_strength_max": 276,
        "elongation": 12, "hardness": "95 HBW", "elastic_modulus": 68.9,
        "thermal_conductivity": 167, "specific_heat": 896,
        "melting_point_min": 582, "melting_point_max": 652,
        "cost_per_kg_min": 220, "cost_per_kg_max": 350, "cost_currency": "INR",
        "applications": "Aerospace structures, bicycle frames, automotive parts, marine fittings",
        "equivalent_grades": "A96061 (UNS), AlMg1SiCu (EN), A6061 (JIS)",
        "composition": "Al 95.8-98.6%, Mg 0.8-1.2%, Si 0.4-0.8%, Cu 0.15-0.4%",
        "source_name": "MatWeb",
    },
    {
        "name": "Aluminium 2024-T3",
        "category": "Metal", "subcategory": "Aluminium Alloy", "grade": "2024-T3",
        "standard": "ASTM B209",
        "density": 2.78,
        "tensile_strength_min": 435, "tensile_strength_max": 485,
        "yield_strength_min": 290, "yield_strength_max": 345,
        "elongation": 18, "hardness": "120 HBW", "elastic_modulus": 73.1,
        "thermal_conductivity": 121, "specific_heat": 875,
        "melting_point_min": 502, "melting_point_max": 638,
        "cost_per_kg_min": 350, "cost_per_kg_max": 550, "cost_currency": "INR",
        "applications": "Aircraft fuselage, wing skins, rivets, truck wheels",
        "equivalent_grades": "A92024 (UNS), AlCu4Mg1 (EN), A2024 (JIS)",
        "composition": "Al 90.7-94.7%, Cu 3.8-4.9%, Mg 1.2-1.8%, Mn 0.3-0.9%",
        "source_name": "MatWeb",
    },
    {
        "name": "Aluminium 7075-T6",
        "category": "Metal", "subcategory": "Aluminium Alloy", "grade": "7075-T6",
        "standard": "ASTM B209",
        "density": 2.81,
        "tensile_strength_min": 510, "tensile_strength_max": 572,
        "yield_strength_min": 434, "yield_strength_max": 503,
        "elongation": 11, "hardness": "150 HBW", "elastic_modulus": 71.7,
        "thermal_conductivity": 130, "specific_heat": 960,
        "melting_point_min": 477, "melting_point_max": 635,
        "cost_per_kg_min": 500, "cost_per_kg_max": 800, "cost_currency": "INR",
        "applications": "Aerospace, military, rock climbing gear, high-stress structural parts",
        "equivalent_grades": "A97075 (UNS), AlZn5.5MgCu (EN), A7075 (JIS)",
        "composition": "Al 87.1-91.4%, Zn 5.1-6.1%, Mg 2.1-2.9%, Cu 1.2-2.0%",
        "source_name": "MatWeb",
    },

    # ═══════════════════════════════════════════
    #  COPPER ALLOYS
    # ═══════════════════════════════════════════
    {
        "name": "C11000 Electrolytic Tough Pitch Copper",
        "category": "Metal", "subcategory": "Copper", "grade": "C11000 (ETP)",
        "standard": "ASTM B152",
        "density": 8.94,
        "tensile_strength_min": 220, "tensile_strength_max": 250,
        "yield_strength_min": 69, "yield_strength_max": 76,
        "elongation": 45, "hardness": "40 HRF", "elastic_modulus": 117,
        "thermal_conductivity": 388, "specific_heat": 385,
        "melting_point_min": 1065, "melting_point_max": 1083,
        "cost_per_kg_min": 750, "cost_per_kg_max": 900, "cost_currency": "INR",
        "applications": "Electrical wire, bus bars, roofing, plumbing, heat exchangers",
        "equivalent_grades": "Cu-ETP (EN), C1100 (JIS)",
        "composition": "Cu 99.9% min",
        "source_name": "MatWeb",
    },
    {
        "name": "C36000 Free Cutting Brass",
        "category": "Metal", "subcategory": "Copper Alloy", "grade": "C36000",
        "standard": "ASTM B16",
        "density": 8.50,
        "tensile_strength_min": 340, "tensile_strength_max": 470,
        "yield_strength_min": 125, "yield_strength_max": 310,
        "elongation": 25, "hardness": "78 HRB", "elastic_modulus": 97,
        "thermal_conductivity": 115, "specific_heat": 380,
        "melting_point_min": 885, "melting_point_max": 900,
        "cost_per_kg_min": 600, "cost_per_kg_max": 800, "cost_currency": "INR",
        "applications": "Screw machine parts, fittings, valves, gears, lock components",
        "equivalent_grades": "CuZn36Pb3 (EN), C3604 (JIS)",
        "composition": "Cu 60-63%, Zn 35.5%, Pb 2.5-3.7%",
        "source_name": "MatWeb",
    },

    # ═══════════════════════════════════════════
    #  TOOL & SPECIALTY STEELS
    # ═══════════════════════════════════════════
    {
        "name": "AISI D2 Tool Steel",
        "category": "Metal", "subcategory": "Tool Steel", "grade": "D2",
        "standard": "ASTM A681",
        "density": 7.70,
        "tensile_strength_min": 550, "tensile_strength_max": 860,
        "yield_strength_min": 400, "yield_strength_max": 690,
        "elongation": 1, "hardness": "62 HRC", "elastic_modulus": 210,
        "thermal_conductivity": 20, "specific_heat": 460,
        "melting_point_min": 1395, "melting_point_max": 1420,
        "cost_per_kg_min": 300, "cost_per_kg_max": 500, "cost_currency": "INR",
        "applications": "Blanking dies, forming dies, knives, slitters, punches",
        "equivalent_grades": "X153CrMoV12 (EN), SKD11 (JIS)",
        "composition": "Fe 84%, Cr 11-13%, C 1.4-1.6%, Mo 0.7-1.2%, V 0.5-1.1%",
        "source_name": "Textbook / ASM",
    },
    {
        "name": "AISI 4140 Alloy Steel",
        "category": "Metal", "subcategory": "Alloy Steel", "grade": "4140",
        "standard": "ASTM A29",
        "density": 7.85,
        "tensile_strength_min": 655, "tensile_strength_max": 950,
        "yield_strength_min": 415, "yield_strength_max": 655,
        "elongation": 18, "hardness": "275 HBW", "elastic_modulus": 210,
        "thermal_conductivity": 42.6, "specific_heat": 473,
        "melting_point_min": 1416, "melting_point_max": 1450,
        "cost_per_kg_min": 80, "cost_per_kg_max": 130, "cost_currency": "INR",
        "applications": "Gears, shafts, spindles, fixtures, couplings, pump shafts",
        "equivalent_grades": "42CrMo4 (EN), SCM440 (JIS), IS 1570 Grade 40Cr4Mo3",
        "composition": "Fe 96.7%, Cr 0.80-1.10%, Mo 0.15-0.25%, C 0.38-0.43%",
        "source_name": "Textbook / ASM",
    },

    # ═══════════════════════════════════════════
    #  CAST IRON
    # ═══════════════════════════════════════════
    {
        "name": "Grey Cast Iron FG 200",
        "category": "Metal", "subcategory": "Cast Iron", "grade": "FG 200",
        "standard": "IS 210",
        "density": 7.15,
        "tensile_strength_min": 200, "tensile_strength_max": 200,
        "yield_strength_min": None, "yield_strength_max": None,
        "elongation": 0.5, "hardness": "180 HBW", "elastic_modulus": 110,
        "thermal_conductivity": 46, "specific_heat": 490,
        "melting_point_min": 1175, "melting_point_max": 1290,
        "cost_per_kg_min": 45, "cost_per_kg_max": 70, "cost_currency": "INR",
        "applications": "Engine blocks, machine tool beds, pipe fittings, manhole covers",
        "equivalent_grades": "ASTM A48 Class 30, GG-20 (DIN), FC200 (JIS)",
        "composition": "Fe 93%, C 3.0-3.5%, Si 1.8-2.4%",
        "source_name": "BIS IS 210",
    },

    # ═══════════════════════════════════════════
    #  POLYMERS
    # ═══════════════════════════════════════════
    {
        "name": "Nylon 6 (PA6)",
        "category": "Polymer", "subcategory": "Thermoplastic", "grade": "PA6",
        "standard": "ISO 1874",
        "density": 1.14,
        "tensile_strength_min": 70, "tensile_strength_max": 85,
        "yield_strength_min": 70, "yield_strength_max": 85,
        "elongation": 60, "elastic_modulus": 2.9,
        "thermal_conductivity": 0.25, "specific_heat": 1700,
        "melting_point_min": 220, "melting_point_max": 220,
        "max_service_temp": 120,
        "cost_per_kg_min": 180, "cost_per_kg_max": 280, "cost_currency": "INR",
        "applications": "Gears, bearings, automotive under-hood parts, cable ties, textiles",
        "composition": "Polycaprolactam",
        "source_name": "MakeItFrom",
    },
    {
        "name": "Nylon 66 (PA66)",
        "category": "Polymer", "subcategory": "Thermoplastic", "grade": "PA66",
        "standard": "ISO 1874",
        "density": 1.14,
        "tensile_strength_min": 75, "tensile_strength_max": 85,
        "yield_strength_min": 75, "yield_strength_max": 85,
        "elongation": 40, "elastic_modulus": 3.1,
        "thermal_conductivity": 0.26, "specific_heat": 1670,
        "melting_point_min": 255, "melting_point_max": 260,
        "max_service_temp": 130,
        "cost_per_kg_min": 200, "cost_per_kg_max": 320, "cost_currency": "INR",
        "applications": "Automotive radiator tanks, electrical connectors, zip ties, conveyor parts",
        "composition": "Polyhexamethylene adipamide",
        "source_name": "MakeItFrom",
    },
    {
        "name": "HDPE (High-Density Polyethylene)",
        "category": "Polymer", "subcategory": "Thermoplastic", "grade": "HDPE",
        "standard": "ASTM D4976",
        "density": 0.95,
        "tensile_strength_min": 25, "tensile_strength_max": 45,
        "yield_strength_min": 26, "yield_strength_max": 33,
        "elongation": 500, "elastic_modulus": 1.1,
        "thermal_conductivity": 0.49, "specific_heat": 1900,
        "melting_point_min": 130, "melting_point_max": 137,
        "max_service_temp": 80,
        "cost_per_kg_min": 100, "cost_per_kg_max": 150, "cost_currency": "INR",
        "applications": "Pipes, bottles, fuel tanks, playground equipment, cutting boards",
        "composition": "Polyethylene (high density, linear)",
        "source_name": "MakeItFrom",
    },
    {
        "name": "Polypropylene (PP Homopolymer)",
        "category": "Polymer", "subcategory": "Thermoplastic", "grade": "PP-H",
        "standard": "ISO 19069",
        "density": 0.91,
        "tensile_strength_min": 30, "tensile_strength_max": 40,
        "yield_strength_min": 35, "yield_strength_max": 40,
        "elongation": 150, "elastic_modulus": 1.5,
        "thermal_conductivity": 0.22, "specific_heat": 1920,
        "melting_point_min": 160, "melting_point_max": 170,
        "max_service_temp": 100,
        "cost_per_kg_min": 95, "cost_per_kg_max": 140, "cost_currency": "INR",
        "applications": "Packaging, automotive bumpers, battery cases, medical syringes, living hinges",
        "composition": "Isotactic polypropylene",
        "source_name": "MakeItFrom",
    },
    {
        "name": "ABS (Acrylonitrile Butadiene Styrene)",
        "category": "Polymer", "subcategory": "Thermoplastic", "grade": "ABS",
        "standard": "ISO 19062",
        "density": 1.05,
        "tensile_strength_min": 40, "tensile_strength_max": 50,
        "yield_strength_min": 42, "yield_strength_max": 52,
        "elongation": 20, "elastic_modulus": 2.3,
        "thermal_conductivity": 0.17, "specific_heat": 1400,
        "melting_point_min": 200, "melting_point_max": 260,
        "max_service_temp": 85,
        "cost_per_kg_min": 150, "cost_per_kg_max": 230, "cost_currency": "INR",
        "applications": "LEGO bricks, automotive dashboards, computer housings, 3D printing, helmets",
        "composition": "Acrylonitrile 20-25%, Butadiene 20-30%, Styrene 40-60%",
        "source_name": "MakeItFrom",
    },
    {
        "name": "PVC (Polyvinyl Chloride, Rigid)",
        "category": "Polymer", "subcategory": "Thermoplastic", "grade": "PVC-U",
        "standard": "ISO 1163",
        "density": 1.40,
        "tensile_strength_min": 40, "tensile_strength_max": 60,
        "yield_strength_min": 45, "yield_strength_max": 55,
        "elongation": 25, "elastic_modulus": 3.0,
        "thermal_conductivity": 0.16, "specific_heat": 1050,
        "melting_point_min": 160, "melting_point_max": 210,
        "max_service_temp": 65,
        "cost_per_kg_min": 80, "cost_per_kg_max": 130, "cost_currency": "INR",
        "applications": "Water pipes, window profiles, flooring, cable insulation, blood bags",
        "composition": "Polyvinyl chloride (unplasticized)",
        "source_name": "MakeItFrom",
    },
    {
        "name": "PTFE (Teflon)",
        "category": "Polymer", "subcategory": "Fluoropolymer", "grade": "PTFE",
        "standard": "ASTM D4894",
        "density": 2.15,
        "tensile_strength_min": 20, "tensile_strength_max": 35,
        "yield_strength_min": 10, "yield_strength_max": 15,
        "elongation": 300, "elastic_modulus": 0.5,
        "thermal_conductivity": 0.25, "specific_heat": 1000,
        "melting_point_min": 327, "melting_point_max": 327,
        "max_service_temp": 260,
        "cost_per_kg_min": 800, "cost_per_kg_max": 2000, "cost_currency": "INR",
        "applications": "Non-stick coatings, gaskets, seals, bearings, chemical-resistant linings",
        "composition": "Polytetrafluoroethylene",
        "source_name": "MakeItFrom",
    },

    # ═══════════════════════════════════════════
    #  CERAMICS
    # ═══════════════════════════════════════════
    {
        "name": "Alumina (Aluminium Oxide 99.5%)",
        "category": "Ceramic", "subcategory": "Oxide Ceramic", "grade": "Al2O3 99.5%",
        "standard": "ASTM C799",
        "density": 3.89,
        "tensile_strength_min": 260, "tensile_strength_max": 300,
        "yield_strength_min": None, "yield_strength_max": None,
        "elongation": 0, "hardness": "1500 HV", "elastic_modulus": 370,
        "thermal_conductivity": 35, "specific_heat": 880,
        "melting_point_min": 2072, "melting_point_max": 2072,
        "max_service_temp": 1750,
        "cost_per_kg_min": 400, "cost_per_kg_max": 1200, "cost_currency": "INR",
        "applications": "Cutting tools, spark plugs, electrical insulators, hip implants, kiln furniture",
        "composition": "Al2O3 99.5%",
        "source_name": "CeramTec / Textbook",
    },
    {
        "name": "Silicon Carbide (SiC)",
        "category": "Ceramic", "subcategory": "Non-Oxide Ceramic", "grade": "SiC",
        "standard": "ASTM C799",
        "density": 3.10,
        "tensile_strength_min": 250, "tensile_strength_max": 350,
        "yield_strength_min": None, "yield_strength_max": None,
        "elongation": 0, "hardness": "2500 HV", "elastic_modulus": 410,
        "thermal_conductivity": 120, "specific_heat": 750,
        "melting_point_min": 2730, "melting_point_max": 2730,
        "max_service_temp": 1600,
        "cost_per_kg_min": 800, "cost_per_kg_max": 3000, "cost_currency": "INR",
        "applications": "Grinding wheels, brake discs, armor plating, semiconductor wafers, kiln shelves",
        "composition": "SiC",
        "source_name": "CeramTec / Textbook",
    },

    # ═══════════════════════════════════════════
    #  COMPOSITES
    # ═══════════════════════════════════════════
    {
        "name": "E-Glass / Epoxy Composite",
        "category": "Composite", "subcategory": "Fiber Reinforced Polymer", "grade": "E-Glass/Epoxy",
        "density": 2.10,
        "tensile_strength_min": 800, "tensile_strength_max": 1200,
        "yield_strength_min": None, "yield_strength_max": None,
        "elongation": 2.5, "elastic_modulus": 45,
        "thermal_conductivity": 0.35, "specific_heat": 900,
        "max_service_temp": 150,
        "cost_per_kg_min": 300, "cost_per_kg_max": 700, "cost_currency": "INR",
        "applications": "Wind turbine blades, boat hulls, storage tanks, PCBs (FR-4), automotive body panels",
        "composition": "E-Glass fiber (60%) + Epoxy resin (40%)",
        "source_name": "Textbook / CompositesWorld",
    },
    {
        "name": "Carbon Fiber / Epoxy (CFRP)",
        "category": "Composite", "subcategory": "Fiber Reinforced Polymer", "grade": "T300/Epoxy",
        "density": 1.60,
        "tensile_strength_min": 1500, "tensile_strength_max": 2500,
        "yield_strength_min": None, "yield_strength_max": None,
        "elongation": 1.5, "elastic_modulus": 135,
        "thermal_conductivity": 5, "specific_heat": 800,
        "max_service_temp": 180,
        "cost_per_kg_min": 2000, "cost_per_kg_max": 5000, "cost_currency": "INR",
        "applications": "Aerospace structures, F1 cars, sports equipment (tennis rackets, bicycles), prosthetics",
        "composition": "T300 Carbon fiber (60%) + Epoxy resin (40%)",
        "source_name": "Textbook / CompositesWorld",
    },
]


def seed():
    """Clear all existing materials and insert the seed data."""
    db = SessionLocal()

    try:
        # Clear existing data
        count = db.query(Material).count()
        if count > 0:
            db.query(Material).delete()
            db.commit()
            print(f"  Cleared {count} existing materials.")

        # Insert all materials
        for mat_data in MATERIALS:
            material = Material(**mat_data)
            db.add(material)

        db.commit()
        print(f"  Inserted {len(MATERIALS)} materials.\n")

        # Summary by category
        print("  Summary:")
        for cat in ["Metal", "Polymer", "Ceramic", "Composite"]:
            n = db.query(Material).filter(Material.category == cat).count()
            print(f"    {cat:12s}  {n} materials")

        total = db.query(Material).count()
        print(f"\n  TOTAL: {total} materials in database")

    finally:
        db.close()


if __name__ == "__main__":
    print("\n=== MatDataHub: Seeding Database ===\n")
    seed()
    print("\n=== Done! ===\n")
