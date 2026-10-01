import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\routers\admin.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''    new_mat = Material(
        name=contrib.name,
        category=contrib.category,
        subcategory=contrib.subcategory,
        standard=contrib.grade,  # Mapping grade to standard for now, or keep grade? Public materials don't have grade, they have standard/origin
        source_name="User Contributed",
        description=contrib.description,
        source_url=contrib.source_url,
        elastic_modulus=contrib.elastic_modulus,
        density=contrib.density,
        yield_strength_min=contrib.yield_strength_min,
        tensile_strength_min=contrib.tensile_strength_min
    )'''

good = '''    hardness_str = None
    if contrib.hardness_min and contrib.hardness_scale:
        hardness_str = f"{contrib.hardness_min} {contrib.hardness_scale}"
    elif contrib.hardness_min:
        hardness_str = str(contrib.hardness_min)

    new_mat = Material(
        name=contrib.name,
        category=contrib.category,
        subcategory=contrib.subcategory,
        grade=contrib.grade,
        standard=contrib.grade,
        source_name="User Contributed",
        description=contrib.description,
        source_url=contrib.source_url,
        elastic_modulus=contrib.elastic_modulus,
        density=contrib.density,
        yield_strength_min=contrib.yield_strength_min,
        yield_strength_max=contrib.yield_strength_max,
        tensile_strength_min=contrib.tensile_strength_min,
        tensile_strength_max=contrib.tensile_strength_max,
        elongation=contrib.elongation_min,
        hardness=hardness_str,
        thermal_conductivity=contrib.thermal_conductivity,
        specific_heat=contrib.specific_heat,
        melting_point_min=contrib.melting_point,
        max_service_temp=contrib.max_service_temp
    )'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed complete mapping")
else:
    print("Block not found")
