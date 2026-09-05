import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the Synthesizer Cost Rule of Mixtures
old_synth_math = """                                        ts1 = mat1.get("tensile_strength_max") or mat1.get("tensile_strength_min") or 0.0
                                        ts2 = mat2.get("tensile_strength_max") or mat2.get("tensile_strength_min") or 0.0
                                        blend_ts = (ts1 * (vol_m1/100.0)) + (ts2 * (vol_m2/100.0))
                                        
                                        c_min1 = mat1.get("cost_per_kg_min") or 0.0
                                        c_min2 = mat2.get("cost_per_kg_min") or 0.0
                                        blend_cost = (c_min1 * (vol_m1/100.0)) + (c_min2 * (vol_m2/100.0))"""

new_synth_math = """                                        ts1 = mat1.get("tensile_strength_max") or mat1.get("tensile_strength_min") or 0.0
                                        ts2 = mat2.get("tensile_strength_max") or mat2.get("tensile_strength_min") or 0.0
                                        blend_ts = (ts1 * (vol_m1/100.0)) + (ts2 * (vol_m2/100.0))
                                        
                                        c_min1 = mat1.get("cost_per_kg_min") or 0.0
                                        c_min2 = mat2.get("cost_per_kg_min") or 0.0
                                        
                                        # DEEP DIVE FIX: Cost is per kg (Mass), so it must be weighted by Mass Fraction, NOT Volume Fraction!
                                        mass_frac1 = (den1 * (vol_m1 / 100.0)) / blend_density if blend_density > 0 else 0
                                        mass_frac2 = (den2 * (vol_m2 / 100.0)) / blend_density if blend_density > 0 else 0
                                        blend_cost = (c_min1 * mass_frac1) + (c_min2 * mass_frac2)"""

if old_synth_math in content:
    content = content.replace(old_synth_math, new_synth_math)
    print("Synthesizer math fixed!")
else:
    print("WARNING: Could not find old synthesizer math block.")

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
