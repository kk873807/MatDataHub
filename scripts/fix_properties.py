
import sys
content = open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\materials\[id]\page.tsx', 'r', encoding='utf-8').read()

old_mech = '''              <div className=\"grid grid-cols-2 md:grid-cols-3 gap-4\">
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Yield Strength</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.yield_strength_min} -{\" \"}
                    {material.yield_strength_max}{\" \"}
                    <span className=\"text-xs text-slate-600 dark:text-slate-300\">MPa</span>
                  </p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Tensile Strength</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.tensile_strength_min} -{\" \"}
                    {material.tensile_strength_max}{\" \"}
                    <span className=\"text-xs text-slate-600 dark:text-slate-300\">MPa</span>
                  </p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Elastic Modulus</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.elastic_modulus}{\" \"}
                    <span className=\"text-xs text-slate-600 dark:text-slate-300\">GPa</span>
                  </p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Density</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.density}{\" \"}
                    <span className=\"text-xs text-slate-600 dark:text-slate-300\">g/cm³</span>
                  </p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Hardness</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.hardness_value || \"-\"}{\" \"}
                    <span className=\"text-xs text-slate-600 dark:text-slate-300\">
                      {material.hardness_scale}
                    </span>
                  </p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Max Temp</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.max_service_temp}{\" \"}
                    <span className=\"text-xs text-slate-600 dark:text-slate-300\">°C</span>
                  </p>
                </div>
              </div>'''.replace('\', '')

new_mech = '''              <div className=\"grid grid-cols-2 md:grid-cols-4 gap-4\">
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Yield Strength</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.yield_strength_min} - {material.yield_strength_max} <span className=\"text-xs text-slate-600 dark:text-slate-300\">MPa</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Tensile Strength</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.tensile_strength_min} - {material.tensile_strength_max} <span className=\"text-xs text-slate-600 dark:text-slate-300\">MPa</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Elastic Modulus</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.elastic_modulus || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">GPa</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Shear Modulus</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.shear_modulus || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">GPa</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Poisson's Ratio</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.poissons_ratio || \"-\"}</p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Density</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.density || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">g/cm³</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Compressive Strength</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.compressive_strength || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">MPa</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Fracture Toughness</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.fracture_toughness || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">MPa·m½</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Hardness</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.hardness_value || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">{material.hardness_scale}</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Crystal Structure</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white truncate\" title={material.crystal_structure || \"-\"}>{material.crystal_structure || \"-\"}</p>
                </div>
              </div>'''.replace('\', '')


old_therm = '''              <div className=\"grid grid-cols-2 md:grid-cols-3 gap-4\">
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Thermal Conductivity</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.thermal_conductivity || \"-\"}{\" \"}
                    <span className=\"text-xs text-slate-600 dark:text-slate-300\">W/mK</span>
                  </p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Specific Heat</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.specific_heat || \"-\"}{\" \"}
                    <span className=\"text-xs text-slate-600 dark:text-slate-300\">J/kgK</span>
                  </p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Melting Point</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.melting_point || \"-\"}{\" \"}
                    <span className=\"text-xs text-slate-600 dark:text-slate-300\">°C</span>
                  </p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Embodied Carbon</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.embodied_carbon || \"-\"}{\" \"}
                    <span className=\"text-xs text-slate-600 dark:text-slate-300\">kg CO2/kg</span>
                  </p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Water Usage</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.water_usage || \"-\"}{\" \"}
                    <span className=\"text-xs text-slate-600 dark:text-slate-300\">L/kg</span>
                  </p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Recyclability</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">
                    {material.recyclability_fraction
                      ? (material.recyclability_fraction * 100).toFixed(0) + \"%\"
                      : \"-\"}
                  </p>
                </div>
              </div>'''.replace('\', '')

new_therm = '''              <div className=\"grid grid-cols-2 md:grid-cols-4 gap-4\">
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Thermal Conductivity</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.thermal_conductivity || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">W/mK</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Specific Heat</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.specific_heat || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">J/kgK</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Thermal Exp. Coeff</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.thermal_expansion_coefficient || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">µm/m·K</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Melting Point</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.melting_point || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">°C</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Max Service Temp</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.max_service_temp || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">°C</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Electrical Resistivity</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.electrical_resistivity || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">µO·m</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Corrosion Resist.</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white capitalize truncate\" title={material.corrosion_resistance || \"-\"}>{material.corrosion_resistance || \"-\"}</p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Machinability</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white capitalize truncate\" title={material.machinability_rating || \"-\"}>{material.machinability_rating || \"-\"}</p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Embodied Carbon</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.embodied_carbon || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">kg CO2/kg</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Water Usage</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.water_usage || \"-\"} <span className=\"text-xs text-slate-600 dark:text-slate-300\">L/kg</span></p>
                </div>
                <div className=\"bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800\">
                  <p className=\"text-xs text-slate-600 dark:text-slate-300\">Recyclability</p>
                  <p className=\"text-lg font-semibold text-slate-900 dark:text-white\">{material.recyclability_fraction ? (material.recyclability_fraction * 100).toFixed(0) + \"%\" : \"-\"}</p>
                </div>
              </div>'''.replace('\', '')


content = content.replace(old_mech, new_mech)
content = content.replace(old_therm, new_therm)

open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\materials\[id]\page.tsx', 'w', encoding='utf-8').write(content)
print('Done!')

