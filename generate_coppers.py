import csv
import os

existing = [
    "C12200", "C14500", "C17200", "C28000", "C46400",
    "C63000", "C65500", "C70600", "C71500", "C75200"
]

missing_coppers = [
    # Pure & High Copper
    {"name": "Electrolytic Tough Pitch (ETP) Copper (UNS C11000)", "subcategory": "Pure Copper", "desc": "Most common copper for electrical applications.", "tensile": 220, "yield": 69, "density": 8.89, "thermal": 388, "cost": 9.50, "machinability": 20},
    {"name": "Oxygen-Free Electronic (OFE) Copper (UNS C10100)", "subcategory": "Pure Copper", "desc": "Highest purity copper, extremely high conductivity.", "tensile": 220, "yield": 69, "density": 8.94, "thermal": 391, "cost": 12.00, "machinability": 20},
    {"name": "Oxygen-Free (OFHC) Copper (UNS C10200)", "subcategory": "Pure Copper", "desc": "High conductivity, immune to hydrogen embrittlement.", "tensile": 220, "yield": 69, "density": 8.94, "thermal": 391, "cost": 11.50, "machinability": 20},
    {"name": "Chromium Copper (UNS C18200)", "subcategory": "High Copper Alloy", "desc": "High strength and conductivity, used for resistance welding electrodes.", "tensile": 345, "yield": 275, "density": 8.89, "thermal": 324, "cost": 15.00, "machinability": 20},
    {"name": "Zirconium Copper (UNS C15000)", "subcategory": "High Copper Alloy", "desc": "Retains strength at high temperatures.", "tensile": 300, "yield": 200, "density": 8.89, "thermal": 367, "cost": 18.00, "machinability": 20},
    
    # Brasses (Copper-Zinc)
    {"name": "Gilding Metal (95/5 Brass) (UNS C21000)", "subcategory": "Brass", "desc": "Used for coins, medals, and bullet jackets.", "tensile": 235, "yield": 83, "density": 8.86, "thermal": 232, "cost": 8.50, "machinability": 20},
    {"name": "Commercial Bronze (90/10 Brass) (UNS C22000)", "subcategory": "Brass", "desc": "Excellent cold workability, used for marine hardware.", "tensile": 255, "yield": 83, "density": 8.80, "thermal": 189, "cost": 8.30, "machinability": 20},
    {"name": "Red Brass (85/15 Brass) (UNS C23000)", "subcategory": "Brass", "desc": "Good corrosion resistance, used for plumbing pipes.", "tensile": 270, "yield": 83, "density": 8.75, "thermal": 159, "cost": 8.20, "machinability": 30},
    {"name": "Cartridge Brass (70/30) (UNS C26000)", "subcategory": "Brass", "desc": "Excellent ductility, standard for ammunition casings.", "tensile": 305, "yield": 105, "density": 8.53, "thermal": 121, "cost": 8.00, "machinability": 30},
    {"name": "Yellow Brass (65/35) (UNS C27000)", "subcategory": "Brass", "desc": "General purpose cold-working brass.", "tensile": 330, "yield": 110, "density": 8.47, "thermal": 116, "cost": 7.90, "machinability": 30},
    {"name": "Free-Cutting Brass (UNS C36000)", "subcategory": "Leaded Brass", "desc": "The standard for machinability (rating 100), contains lead.", "tensile": 338, "yield": 124, "density": 8.50, "thermal": 115, "cost": 8.10, "machinability": 100},
    {"name": "Forging Brass (UNS C37700)", "subcategory": "Leaded Brass", "desc": "Excellent hot forgeability.", "tensile": 350, "yield": 140, "density": 8.44, "thermal": 120, "cost": 8.10, "machinability": 80},
    {"name": "Architectural Bronze (UNS C38500)", "subcategory": "Leaded Brass", "desc": "Actually a leaded brass, used for extrusions.", "tensile": 415, "yield": 140, "density": 8.47, "thermal": 123, "cost": 8.20, "machinability": 90},
    {"name": "Admiralty Brass (UNS C44300)", "subcategory": "Tin Brass", "desc": "Inhibited with arsenic for corrosion resistance in heat exchangers.", "tensile": 330, "yield": 105, "density": 8.53, "thermal": 111, "cost": 8.50, "machinability": 30},

    # Phosphor Bronzes (Copper-Tin-Phosphorus)
    {"name": "Phosphor Bronze 5% (UNS C51000)", "subcategory": "Phosphor Bronze", "desc": "Used for electrical contacts, springs, and fasteners.", "tensile": 325, "yield": 130, "density": 8.86, "thermal": 71, "cost": 10.50, "machinability": 20},
    {"name": "Phosphor Bronze 8% (UNS C52100)", "subcategory": "Phosphor Bronze", "desc": "Higher strength and wear resistance.", "tensile": 380, "yield": 165, "density": 8.80, "thermal": 62, "cost": 11.00, "machinability": 20},

    # Aluminum Bronzes
    {"name": "Aluminum Bronze (UNS C61400)", "subcategory": "Aluminum Bronze", "desc": "High strength, excellent wear and corrosion resistance.", "tensile": 515, "yield": 240, "density": 7.89, "thermal": 57, "cost": 12.00, "machinability": 20},
    {"name": "Nickel Aluminum Bronze (UNS C63200)", "subcategory": "Aluminum Bronze", "desc": "Marine propellers and heavy-duty bearings.", "tensile": 655, "yield": 310, "density": 7.64, "thermal": 36, "cost": 14.00, "machinability": 20},

    # Silicon Bronzes
    {"name": "Low Silicon Bronze (UNS C65100)", "subcategory": "Silicon Bronze", "desc": "Excellent weldability, used for hardware.", "tensile": 275, "yield": 105, "density": 8.75, "thermal": 57, "cost": 11.50, "machinability": 30},

    # Cupronickels
    {"name": "Copper-Nickel 80/20 (UNS C71000)", "subcategory": "Cupronickel", "desc": "Excellent marine corrosion resistance.", "tensile": 340, "yield": 110, "density": 8.94, "thermal": 36, "cost": 13.50, "machinability": 20},
    
    # Nickel Silvers
    {"name": "Nickel Silver 18% (UNS C77000)", "subcategory": "Nickel Silver", "desc": "Silvery appearance, used for optical frames and springs.", "tensile": 415, "yield": 185, "density": 8.70, "thermal": 29, "cost": 12.50, "machinability": 30},
    
    # Cast Copper Alloys
    {"name": "Ounce Metal / Red Brass (UNS C83600)", "subcategory": "Cast Brass", "desc": "Standard 85-5-5-5 casting alloy.", "tensile": 255, "yield": 117, "density": 8.83, "thermal": 72, "cost": 9.00, "machinability": 84},
    {"name": "High-Leaded Tin Bronze (UNS C93200 / SAE 660)", "subcategory": "Cast Bronze", "desc": "The standard bearing bronze.", "tensile": 240, "yield": 125, "density": 8.93, "thermal": 59, "cost": 11.50, "machinability": 70},
    {"name": "Aluminum Bronze Casting (UNS C95400)", "subcategory": "Cast Aluminum Bronze", "desc": "High strength gear and bearing material.", "tensile": 586, "yield": 220, "density": 7.45, "thermal": 59, "cost": 12.50, "machinability": 60},
    {"name": "Manganese Bronze Casting (UNS C86300)", "subcategory": "Cast Manganese Bronze", "desc": "Very high strength, heavy load applications.", "tensile": 760, "yield": 415, "density": 7.73, "thermal": 35, "cost": 11.00, "machinability": 8}
]

headers = [
    "name", "category", "subcategory", "standards", "description", 
    "tensile_strength_mpa", "yield_strength_mpa", "elongation_percent", 
    "hardness_brinell", "density_g_cm3", "thermal_conductivity_w_mk", 
    "melting_point_c", "specific_heat_j_kgk", "cost_per_kg", 
    "carbon_footprint_kg_co2_kg", "applications", "machinability_rating"
]

csv_file = "C:/Users/KISHAN/.gemini/antigravity/brain/90857fe7-b886-4dbf-9d50-6634bcd34e13/.user_uploaded/missing_copper_grades.csv"

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for mat in missing_coppers:
        # Extract UNS for standards field
        uns = ""
        if "(UNS" in mat["name"]:
            uns = mat["name"].split("(UNS ")[1].split(")")[0]
        elif "(SAE" in mat["name"]:
             uns = mat["name"].split("(UNS ")[1].split(")")[0] # approximate handling

        writer.writerow({
            "name": mat["name"],
            "category": "Copper",
            "subcategory": mat["subcategory"],
            "standards": f"UNS {uns}" if uns else "",
            "description": mat["desc"],
            "tensile_strength_mpa": mat["tensile"],
            "yield_strength_mpa": mat["yield"],
            "elongation_percent": 15, # placeholder average
            "hardness_brinell": 80, # placeholder average
            "density_g_cm3": mat["density"],
            "thermal_conductivity_w_mk": mat["thermal"],
            "melting_point_c": 1000, # placeholder average
            "specific_heat_j_kgk": 385,
            "cost_per_kg": mat["cost"],
            "carbon_footprint_kg_co2_kg": 4.5,
            "applications": "Electrical, Marine, Architecture, Bearings",
            "machinability_rating": mat["machinability"]
        })
print("Done")
