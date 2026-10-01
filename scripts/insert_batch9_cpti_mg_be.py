import os
import csv
import io
import re
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

csv_data = """category,subcategory,name,density,tensile_strength_min,yield_strength_min,elongation,hardness,elastic_modulus,thermal_conductivity,specific_heat,melting_point_min,composition,description,source_url,source_notes
Titanium,Commercially Pure Titanium,Titanium Grade 3,4.5,520,450,25,"266 HB (est. from Rockwell C 26)",104,16.4,0.523,1660,"Ti 99.1% (bal); C ≤0.10; Fe ≤0.30; H ≤0.015; N ≤0.05; O ≤0.35 (UNS R50550)","Unalloyed CP titanium, annealed 2 hr at 700°C, ASTM B265 Grade 3. High strength CP grade used in airframe skin, heat exchangers, cryogenic vessels.",https://www.aerospacemetals.com/wp-content/uploads/2023/07/Titanium-Grade-3-Annealed-Data-Sheet.pdf,"ASM Aerospace Specification Metals"
Titanium,Commercially Pure Titanium,Titanium Grade 4,4.51,550,480,15,,103,16.95,,1649,"Ti (bal); N ≤0.05; C ≤0.08; H ≤0.015; Fe ≤0.5; O ≤0.4 (UNS R50700, AMS 4901)","Highest-strength CP titanium grade (specified minima shown; typical UTS 655-690 MPa, YS 480-635 MPa, 20-25% elongation). Used in aerospace fasteners, jet engine components.",https://www.upmet.com/sites/default/files/products/datasheet/cp-grade-4-datasheet.pdf,"United Performance Metals / Arnold Magnetics"
Titanium,Commercially Pure Titanium,Titanium Grade 7 (Pd-enhanced),4.51,345,275,20,,112,21.79,,1660,"Ti (bal); Pd 0.12-0.25%; Fe ≤0.30; O ≤0.25; C ≤0.10; N ≤0.03; H ≤0.015 (UNS R52400)","CP titanium + Pd addition for enhanced crevice-corrosion resistance in reducing acids/chlorides; mechanically equivalent to Grade 2. Used in chemical processing (reactors, piping, heat exchangers).",https://aircraftmaterials.com/data/titanium/cpgr7.html,"Aircraft Materials UK / Elgiloy Specialty Metals"
Titanium,Commercially Pure Titanium,Titanium Grade 11 (Pd-enhanced),4.51,240,138,24,,112,21.79,,1660,"Ti (bal); Pd 0.12-0.25%; Fe ≤0.20; O ≤0.18; C ≤0.08; N ≤0.03; H ≤0.015 (UNS R52250)","Pd-enhanced CP titanium with properties similar to Grade 1; best ductility/formability of the Pd grades, high impact toughness. Used in chemical processing, desalination, marine.",https://www.atimaterials.com/Products/grade-11,"ATI / Elgiloy Specialty Metals"
Magnesium,Wrought Magnesium,AZ31B Magnesium Alloy,1.77,255,150,21,"56 HB",45,100,,605,"Al 2.5-3.5%; Zn 0.6-1.4%; Mn ≥0.2% min; Si ≤0.05; Cu ≤0.05; Ca ≤0.04; Mg (bal) (UNS M11311)","AZ31B-O (annealed) wrought magnesium sheet/plate; good room-temperature strength/ductility, corrosion resistance, weldability. Used in aircraft fuselage panels, electronics housings, tooling plate.",https://alloysintl.com/?p=7374,"Alloys International / Aircraft Materials"
Magnesium,Cast Magnesium,AZ91D Magnesium Alloy,1.81,230,150,3,"63 HB",44.8,72.7,1.047,470,"Al 8.30-9.70%; Zn 0.35-1.00%; Mn ≥0.130%; Cu ≤0.030; Fe ≤0.005; Ni ≤0.002; Si ≤0.100; Mg (bal) (UNS M11916)","Most common magnesium die-casting alloy; excellent corrosion resistance. Solidus 470°C / liquidus 595°C. Used for housings, covers, brackets, electronic enclosures.",https://www.tekogehause.de/uploads/manuali/materiali/AZ91D.pdf,"Tekogehäuse / Dead Sea Magnesium"
Magnesium,Cast Magnesium,AM60B Magnesium Alloy,1.80,270,130,16,"65 HB",45,61,1.02,434,"Al 5.6-6.4%; Mn 0.26-0.50%; Zn ≤0.2%; Si ≤0.05; Cu ≤0.008; Ni ≤0.001; Fe ≤0.004; Mg (bal)","High-ductility die-casting alloy for energy-absorbing, ductile-failure applications: seat frames, instrument panels, brackets. Non-equilibrium solidification range 434-615°C.",https://www.dsmag.co.il/product/am60b-12kg/,"Dead Sea Magnesium (DSM)"
Magnesium,Wrought Magnesium,ZK60A Magnesium Alloy,1.83,310,248,4,,46,120,960,550,"Zn 4.8-6.2%; Zr ≥0.45% min; other ≤0.30; Mg (bal) (UNS M16600)","Heat-treatable, high-strength wrought Mg alloy (T5 temper values shown) for extrusions/forgings needing shock and impact resistance; used in landing gear, brake housings, ribs/spars.",https://aircraftmaterials.com/data/magnesium/zk60a.html,"Aircraft Materials UK"
Magnesium,Wrought Magnesium,AZ80A Magnesium Alloy,1.80,310,205,2,"70-90 HB",45,76,1100,470,"Al 7.8-9.2%; Zn 0.20-0.8%; Mn 0.12-0.5%; Mg (bal) (UNS M11800)","High-strength wrought alloy for extrusions and forgings of simple design (T5 temper values shown); used in satellites, helicopter gearboxes/rotor hubs, landing gear struts.",https://www.luxfermeltechnologies.com/wp-content/uploads/2024/11/Elektron®-AZ80A-Datasheet.pdf,"Luxfer MEL Technologies"
Magnesium,Cast Magnesium,AS41B Magnesium Alloy,,225,140,6,"75 HB min",45,68,1000,570,"Al 3.5-5.0%; Mn 0.35-0.7%; Si 0.5-1.5%; Zn ≤0.12; Cu ≤0.020; Ni ≤0.002; Fe ≤0.0035; Mg (bal) (UNS M10412)","Creep-/heat-resistant die-casting alloy combining good ductility and strength; automotive powertrain and elevated-temperature die-cast components.",https://icastllp.com/material_db_pdf/ANSI%20AA%20AS41B.pdf,"ICAST Alloys / ANSI AA AS41B"
Magnesium,High-Temp Magnesium,WE43 Magnesium Alloy,1.84,220,172,2,"85-105 HV",45,51,966,540,"Y 3.7-4.3%; Rare earths 2.4-4.4%; Zr ≥0.4% min; Mg (bal) (UNS M18430)","High-strength, heat-treatable (T6) casting alloy retaining properties to 300°C without Ag or Th; excellent corrosion resistance. Used in aeroengine/helicopter transmission housings, motorsport.",https://www.luxfermeltechnologies.com/wp-content/uploads/2024/11/Elektron-WE43B-Datasheet.pdf,"Luxfer MEL Technologies"
Magnesium,High-Temp Magnesium,Elektron 21 Magnesium Alloy,1.82,248,145,2,"65-75 HB",44.8,116,1086,545,"Zn 0.2-0.5%; Nd 2.6-3.1%; Gd 1.0-1.7%; Zr saturated; Mg (bal) (UNS M12310)","Fully heat-treatable (T6) high-strength casting alloy for use to 200°C, excellent corrosion resistance and castability; developed for motorsport/aerospace (AMS 4429, ASTM B80).",https://www.luxfermeltechnologies.com/wp-content/uploads/2024/11/Luxfer-MEL-Technologies-Elektron-21.pdf,"Luxfer MEL Technologies"
Magnesium,Pure Magnesium,Pure Magnesium (99.8%),1.74,,,,,42.5,160,1030,650,"Mg ≥99.8%; Cu ≤0.02%; Pb ≤0.01%; Mn ≤0.1%; Ni ≤0.005%; Sn ≤0.01%; other ≤0.05% each (ASTM B951 Grade 9980A)","High-purity primary magnesium ingot/metal; base feedstock grade, not normally assigned structural tensile/yield/elongation specs.",https://matmatch.com/materials/alky2583-astm-b951-grade-9980a,"ASTM B951 (via Matmatch bypass) / Goodfellow"
Beryllium,Pure Beryllium,Pure Beryllium (S-65 Structural Grade),1.85,290,207,3,,290,216,1.95,1287,"Be ≥99.2%; BeO ≤0.90%; Al ≤0.05%; C ≤0.09%; Fe ≤0.08%; Mg ≤0.01%; Si ≤0.045%; other trace elements","Vacuum-hot-pressed high-purity beryllium; exceptional stiffness-to-weight ratio. Used in aerospace/satellite structures, optics, nuclear reflector components.",https://materion.com/products/beryllium-products/beryllium-metal,"Materion"
Beryllium,Pure Beryllium,Pure Beryllium (I-70 Instrument Grade),1.85,345,207,2,,290,216,1.95,1287,"Be ≥99.0%; BeO ≤0.70%; Al ≤0.07%; C ≤0.07%; Fe ≤0.10%; Mg ≤0.07%; Si ≤0.07%; other ≤0.04% each","Hot-isostatic-pressed (I-70-H) instrument/optical-grade beryllium; low oxide content gives good polishing characteristics and isotropy; stable -196°C to 226°C. Used in space/aerospace optics and instrumentation.",https://materion.com/products/beryllium-products/beryllium-metal,"Materion"
Beryllium,Beryllium-Aluminum Alloy,Beryllium-Aluminum Alloy (AlBeMet 162),2.071,262,193,2,,197,210,1465,,"Beryllium 60-64% (~62% typ.); balance aluminum (AlBeMet® AM162 / Al-62wt%Be)","HIP'd beryllium-aluminum metal-matrix composite; ~4x the specific stiffness of aluminum. Values shown are HIP'd-form minima; extruded bar reaches ~400 MPa UTS/276 MPa YS/7% elongation, rolled sheet ~379 MPa UTS/276 MPa YS/5% elongation. Used in avionics, satellite structures, precision instruments.",https://materion.com/products/metal-matrix-composites/albemet-albecast,"Materion"
"""

reader = csv.DictReader(io.StringIO(csv_data.strip()))

def sanitize_float(val):
    if not val: return None
    try: return float(val)
    except: return None

for row in reader:
    name = row['name']
    
    payload = {
        'category': row['category'],
        'subcategory': row['subcategory'],
        'name': name,
        'composition': row['composition'],
        'description': row['description'],
        'source_url': row['source_url'],
        'source_name': row['source_notes'],
        'is_verified': True
    }
    
    for k in ['density', 'tensile_strength_min', 'yield_strength_min', 'elongation', 
              'elastic_modulus', 'thermal_conductivity', 'specific_heat', 'melting_point_min']:
        s = sanitize_float(row[k])
        if s is not None:
            payload[k] = s
            
    if row['hardness']:
        payload['hardness'] = row['hardness']
        
    res = supabase.table('materials').select('id').eq('name', name).execute()
    if res.data:
        supabase.table('materials').update(payload).eq('id', res.data[0]['id']).execute()
        print(f"Updated: {name}")
    else:
        supabase.table('materials').insert(payload).execute()
        print(f"Inserted: {name}")

print("\nBatch 9 complete! Added 16 missing alloys.")
