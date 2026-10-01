import csv
import math

accurate_coppers = [
    # Pure & High Copper
    {"name": "Electrolytic Tough Pitch (ETP) Copper (UNS C11000)", "subcategory": "Pure Copper", "desc": "Most common copper for electrical applications.", 
     "tensile": 220, "yield": 69, "elongation": 45, "hardness": 45, "density": 8.89, "thermal": 388, "melting": 1083, "specific": 385, "cost": 9.50, "carbon": 4.5, "machinability": 20},
    {"name": "Oxygen-Free Electronic (OFE) Copper (UNS C10100)", "subcategory": "Pure Copper", "desc": "Highest purity copper, extremely high conductivity.", 
     "tensile": 220, "yield": 69, "elongation": 50, "hardness": 45, "density": 8.94, "thermal": 391, "melting": 1083, "specific": 385, "cost": 12.00, "carbon": 4.6, "machinability": 20},
    {"name": "Oxygen-Free (OFHC) Copper (UNS C10200)", "subcategory": "Pure Copper", "desc": "High conductivity, immune to hydrogen embrittlement.", 
     "tensile": 220, "yield": 69, "elongation": 50, "hardness": 45, "density": 8.94, "thermal": 391, "melting": 1083, "specific": 385, "cost": 11.50, "carbon": 4.6, "machinability": 20},
    {"name": "Chromium Copper (UNS C18200)", "subcategory": "High Copper Alloy", "desc": "High strength and conductivity, used for resistance welding electrodes.", 
     "tensile": 345, "yield": 275, "elongation": 15, "hardness": 105, "density": 8.89, "thermal": 324, "melting": 1075, "specific": 380, "cost": 15.00, "carbon": 5.2, "machinability": 20},
    {"name": "Zirconium Copper (UNS C15000)", "subcategory": "High Copper Alloy", "desc": "Retains strength at high temperatures.", 
     "tensile": 300, "yield": 200, "elongation": 15, "hardness": 95, "density": 8.89, "thermal": 367, "melting": 1080, "specific": 385, "cost": 18.00, "carbon": 5.5, "machinability": 20},
    
    # Brasses (Copper-Zinc)
    {"name": "Gilding Metal (95/5 Brass) (UNS C21000)", "subcategory": "Brass", "desc": "Used for coins, medals, and bullet jackets.", 
     "tensile": 235, "yield": 83, "elongation": 45, "hardness": 50, "density": 8.86, "thermal": 232, "melting": 1050, "specific": 377, "cost": 8.50, "carbon": 4.2, "machinability": 20},
    {"name": "Commercial Bronze (90/10 Brass) (UNS C22000)", "subcategory": "Brass", "desc": "Excellent cold workability, used for marine hardware.", 
     "tensile": 255, "yield": 83, "elongation": 45, "hardness": 53, "density": 8.80, "thermal": 189, "melting": 1045, "specific": 377, "cost": 8.30, "carbon": 4.1, "machinability": 20},
    {"name": "Red Brass (85/15 Brass) (UNS C23000)", "subcategory": "Brass", "desc": "Good corrosion resistance, used for plumbing pipes.", 
     "tensile": 270, "yield": 83, "elongation": 48, "hardness": 58, "density": 8.75, "thermal": 159, "melting": 1025, "specific": 377, "cost": 8.20, "carbon": 4.0, "machinability": 30},
    {"name": "Cartridge Brass (70/30) (UNS C26000)", "subcategory": "Brass", "desc": "Excellent ductility, standard for ammunition casings.", 
     "tensile": 305, "yield": 105, "elongation": 53, "hardness": 65, "density": 8.53, "thermal": 121, "melting": 955, "specific": 377, "cost": 8.00, "carbon": 3.7, "machinability": 30},
    {"name": "Yellow Brass (65/35) (UNS C27000)", "subcategory": "Brass", "desc": "General purpose cold-working brass.", 
     "tensile": 330, "yield": 110, "elongation": 55, "hardness": 70, "density": 8.47, "thermal": 116, "melting": 930, "specific": 377, "cost": 7.90, "carbon": 3.6, "machinability": 30},
    {"name": "Free-Cutting Brass (UNS C36000)", "subcategory": "Leaded Brass", "desc": "The standard for machinability (rating 100), contains lead.", 
     "tensile": 338, "yield": 124, "elongation": 53, "hardness": 78, "density": 8.50, "thermal": 115, "melting": 900, "specific": 377, "cost": 8.10, "carbon": 3.9, "machinability": 100},
    {"name": "Forging Brass (UNS C37700)", "subcategory": "Leaded Brass", "desc": "Excellent hot forgeability.", 
     "tensile": 350, "yield": 140, "elongation": 45, "hardness": 78, "density": 8.44, "thermal": 120, "melting": 890, "specific": 377, "cost": 8.10, "carbon": 3.9, "machinability": 80},
    {"name": "Architectural Bronze (UNS C38500)", "subcategory": "Leaded Brass", "desc": "Actually a leaded brass, used for extrusions.", 
     "tensile": 415, "yield": 140, "elongation": 45, "hardness": 85, "density": 8.47, "thermal": 123, "melting": 885, "specific": 377, "cost": 8.20, "carbon": 3.9, "machinability": 90},
    {"name": "Admiralty Brass (UNS C44300)", "subcategory": "Tin Brass", "desc": "Inhibited with arsenic for corrosion resistance in heat exchangers.", 
     "tensile": 330, "yield": 105, "elongation": 50, "hardness": 65, "density": 8.53, "thermal": 111, "melting": 935, "specific": 377, "cost": 8.50, "carbon": 4.1, "machinability": 30},

    # Phosphor Bronzes (Copper-Tin-Phosphorus)
    {"name": "Phosphor Bronze 5% (UNS C51000)", "subcategory": "Phosphor Bronze", "desc": "Used for electrical contacts, springs, and fasteners.", 
     "tensile": 325, "yield": 130, "elongation": 48, "hardness": 77, "density": 8.86, "thermal": 71, "melting": 1050, "specific": 380, "cost": 10.50, "carbon": 5.1, "machinability": 20},
    {"name": "Phosphor Bronze 8% (UNS C52100)", "subcategory": "Phosphor Bronze", "desc": "Higher strength and wear resistance.", 
     "tensile": 380, "yield": 165, "elongation": 62, "hardness": 88, "density": 8.80, "thermal": 62, "melting": 1030, "specific": 380, "cost": 11.00, "carbon": 5.3, "machinability": 20},

    # Aluminum Bronzes
    {"name": "Aluminum Bronze (UNS C61400)", "subcategory": "Aluminum Bronze", "desc": "High strength, excellent wear and corrosion resistance.", 
     "tensile": 515, "yield": 240, "elongation": 40, "hardness": 140, "density": 7.89, "thermal": 57, "melting": 1040, "specific": 420, "cost": 12.00, "carbon": 6.0, "machinability": 20},
    {"name": "Nickel Aluminum Bronze (UNS C63200)", "subcategory": "Aluminum Bronze", "desc": "Marine propellers and heavy-duty bearings.", 
     "tensile": 655, "yield": 310, "elongation": 15, "hardness": 190, "density": 7.64, "thermal": 36, "melting": 1045, "specific": 420, "cost": 14.00, "carbon": 6.8, "machinability": 20},

    # Silicon Bronzes
    {"name": "Low Silicon Bronze (UNS C65100)", "subcategory": "Silicon Bronze", "desc": "Excellent weldability, used for hardware.", 
     "tensile": 275, "yield": 105, "elongation": 55, "hardness": 75, "density": 8.75, "thermal": 57, "melting": 1025, "specific": 380, "cost": 11.50, "carbon": 5.5, "machinability": 30},

    # Cupronickels
    {"name": "Copper-Nickel 80/20 (UNS C71000)", "subcategory": "Cupronickel", "desc": "Excellent marine corrosion resistance.", 
     "tensile": 340, "yield": 110, "elongation": 40, "hardness": 73, "density": 8.94, "thermal": 36, "melting": 1195, "specific": 380, "cost": 13.50, "carbon": 7.0, "machinability": 20},
    
    # Nickel Silvers
    {"name": "Nickel Silver 18% (UNS C77000)", "subcategory": "Nickel Silver", "desc": "Silvery appearance, used for optical frames and springs.", 
     "tensile": 415, "yield": 185, "elongation": 40, "hardness": 85, "density": 8.70, "thermal": 29, "melting": 1060, "specific": 380, "cost": 12.50, "carbon": 6.5, "machinability": 30},
    
    # Cast Copper Alloys
    {"name": "Ounce Metal / Red Brass (UNS C83600)", "subcategory": "Cast Brass", "desc": "Standard 85-5-5-5 casting alloy.", 
     "tensile": 255, "yield": 117, "elongation": 30, "hardness": 60, "density": 8.83, "thermal": 72, "melting": 995, "specific": 380, "cost": 9.00, "carbon": 4.2, "machinability": 84},
    {"name": "High-Leaded Tin Bronze (UNS C93200 / SAE 660)", "subcategory": "Cast Bronze", "desc": "The standard bearing bronze.", 
     "tensile": 240, "yield": 125, "elongation": 15, "hardness": 65, "density": 8.93, "thermal": 59, "melting": 970, "specific": 380, "cost": 11.50, "carbon": 4.8, "machinability": 70},
    {"name": "Aluminum Bronze Casting (UNS C95400)", "subcategory": "Cast Aluminum Bronze", "desc": "High strength gear and bearing material.", 
     "tensile": 586, "yield": 220, "elongation": 12, "hardness": 170, "density": 7.45, "thermal": 59, "melting": 1040, "specific": 420, "cost": 12.50, "carbon": 6.2, "machinability": 60},
    {"name": "Manganese Bronze Casting (UNS C86300)", "subcategory": "Cast Manganese Bronze", "desc": "Very high strength, heavy load applications.", 
     "tensile": 760, "yield": 415, "elongation": 18, "hardness": 225, "density": 7.73, "thermal": 35, "melting": 905, "specific": 380, "cost": 11.00, "carbon": 5.8, "machinability": 8}
]

headers = [
    "name", "category", "subcategory", "standards", "description", 
    "tensile_strength_mpa", "yield_strength_mpa", "elongation_percent", 
    "hardness_brinell", "density_g_cm3", "thermal_conductivity_w_mk", 
    "melting_point_c", "specific_heat_j_kgk", "cost_per_kg", 
    "carbon_footprint_kg_co2_kg", "applications", "machinability_rating"
]

csv_file = "C:/Users/KISHAN/.gemini/antigravity/brain/90857fe7-b886-4dbf-9d50-6634bcd34e13/.user_uploaded/accurate_copper_grades.csv"

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for mat in accurate_coppers:
        uns = ""
        if "(UNS" in mat["name"]:
            uns = mat["name"].split("(UNS ")[1].split(")")[0]
        elif "(SAE" in mat["name"]:
             uns = mat["name"].split("(UNS ")[1].split(")")[0]

        writer.writerow({
            "name": mat["name"],
            "category": "Copper",
            "subcategory": mat["subcategory"],
            "standards": f"UNS {uns}" if uns else "",
            "description": mat["desc"],
            "tensile_strength_mpa": mat["tensile"],
            "yield_strength_mpa": mat["yield"],
            "elongation_percent": mat["elongation"],
            "hardness_brinell": mat["hardness"],
            "density_g_cm3": mat["density"],
            "thermal_conductivity_w_mk": mat["thermal"],
            "melting_point_c": mat["melting"],
            "specific_heat_j_kgk": mat["specific"],
            "cost_per_kg": mat["cost"],
            "carbon_footprint_kg_co2_kg": mat["carbon"],
            "applications": "Electrical, Marine, Architecture, Bearings",
            "machinability_rating": mat["machinability"]
        })
print("Done")
