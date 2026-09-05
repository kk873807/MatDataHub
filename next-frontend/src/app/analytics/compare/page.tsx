"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, Scale, Loader2, Info, Plus, X } from "lucide-react";

export default function CompareMaterials() {
  const [allMaterials, setAllMaterials] = useState<any[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [comparison, setComparison] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // Colors for up to 5 materials
  const colors = [
    { hex: "#3b82f6", bg: "rgba(59, 130, 246, 0.3)" }, // blue
    { hex: "#10b981", bg: "rgba(16, 185, 129, 0.3)" }, // emerald
    { hex: "#f59e0b", bg: "rgba(245, 158, 11, 0.3)" }, // amber
    { hex: "#8b5cf6", bg: "rgba(139, 92, 246, 0.3)" }, // purple
    { hex: "#ec4899", bg: "rgba(236, 72, 153, 0.3)" }  // pink
  ];

  // Fetch list of materials for dropdowns
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/materials?per_page=100")
      .then(res => res.json())
      .then(data => setAllMaterials(data.materials || []));
  }, []);

  // Fetch comparison
  useEffect(() => {
    if (selectedIds.length > 0) {
      setLoading(true);
      const queryParams = selectedIds.map(id => `ids=${id}`).join("&");
      fetch(`http://127.0.0.1:8000/api/v1/materials/compare?${queryParams}`)
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
            // Sort to match selection order
            const sorted = selectedIds.map(id => data.find(m => m.id.toString() === id)).filter(Boolean);
            setComparison(sorted);
          }
        })
        .finally(() => setLoading(false));
    } else {
      setComparison([]);
    }
  }, [selectedIds]);

  const propsToCompare = [
    { key: "yield_strength_min", label: "Yield Strength (MPa)", max: 2000 },
    { key: "tensile_strength_min", label: "Tensile Strength (MPa)", max: 2500 },
    { key: "elastic_modulus", label: "Elastic Modulus (GPa)", max: 400 },
    { key: "hardness_value", label: "Hardness", max: 500 },
    { key: "density", label: "Density (g/cm³)", max: 20 },
    { key: "max_service_temp", label: "Max Temp (°C)", max: 2000 },
    { key: "thermal_conductivity", label: "Thermal Conductivity (W/mK)", max: 400 },
    { key: "specific_heat", label: "Specific Heat (J/kgK)", max: 2000 },
    { key: "melting_point", label: "Melting Point (°C)", max: 3500 },
    { key: "embodied_carbon", label: "Carbon (kg CO2)", max: 50 },
    { key: "water_usage", label: "Water (L/kg)", max: 500 },
    { key: "cost_per_kg_min", label: "Cost (₹/kg)", max: 100000 }
  ];

  const handleAddMaterial = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    if (val && !selectedIds.includes(val) && selectedIds.length < 5) {
      setSelectedIds([...selectedIds, val]);
    }
    e.target.value = "";
  };

  const handleRemove = (index: number) => {
    const newIds = [...selectedIds];
    newIds.splice(index, 1);
    setSelectedIds(newIds);
  };

  const generateTakeaways = () => {
    if (comparison.length < 2) return null;
    const takeaways = [];
    
    // Find strongest
    const strongest = [...comparison].sort((a, b) => (b.yield_strength_min || 0) - (a.yield_strength_min || 0))[0];
    if (strongest) takeaways.push(`${strongest.name} offers the highest structural integrity (Yield Stress).`);
    
    // Find cheapest
    const cheapest = [...comparison].sort((a, b) => (a.cost_per_kg_min || Infinity) - (b.cost_per_kg_min || Infinity))[0];
    if (cheapest) takeaways.push(`${cheapest.name} is the most cost-effective option.`);

    // Find lightest
    const lightest = [...comparison].sort((a, b) => (a.density || Infinity) - (b.density || Infinity))[0];
    if (lightest) takeaways.push(`${lightest.name} is the lightest material, ideal for weight-sensitive applications.`);

    // Find most eco-friendly
    const eco = [...comparison].sort((a, b) => (a.embodied_carbon || Infinity) - (b.embodied_carbon || Infinity))[0];
    if (eco && eco.embodied_carbon) takeaways.push(`${eco.name} has the lowest embodied carbon footprint.`);

    return (
      <ul className="list-disc pl-5 space-y-2 text-slate-300 text-sm mt-4">
        {takeaways.map((t, i) => <li key={i}>{t}</li>)}
      </ul>
    );
  };

  // SVG Radar Chart Logic
  const renderRadar = () => {
    if (comparison.length === 0) return null;
    const center = 150;
    const radius = 100;
    const angleStep = (Math.PI * 2) / propsToCompare.length;
    
    const getCoordinates = (matIndex: number) => {
      const mat = comparison[matIndex];
      return propsToCompare.map((prop, i) => {
        const rawVal = mat[prop.key] || 0;
        let norm = rawVal / prop.max;
        if (norm > 1) norm = 1;
        
        const angle = i * angleStep - Math.PI / 2;
        const x = center + radius * norm * Math.cos(angle);
        const y = center + radius * norm * Math.sin(angle);
        return `${x},${y}`;
      }).join(" ");
    };

    return (
      <svg viewBox="0 0 300 300" className="w-full h-full max-w-sm mx-auto overflow-visible">
        {/* Background webs */}
        {[0.2, 0.4, 0.6, 0.8, 1].map(scale => (
          <polygon 
            key={scale}
            points={propsToCompare.map((_, i) => {
              const angle = i * angleStep - Math.PI / 2;
              return `${center + radius * scale * Math.cos(angle)},${center + radius * scale * Math.sin(angle)}`;
            }).join(" ")}
            fill="none" stroke="#334155" strokeWidth="1"
          />
        ))}
        {/* Axes */}
        {propsToCompare.map((prop, i) => {
          const angle = i * angleStep - Math.PI / 2;
          const x = center + radius * Math.cos(angle);
          const y = center + radius * Math.sin(angle);
          const textX = center + (radius + 25) * Math.cos(angle);
          const textY = center + (radius + 15) * Math.sin(angle);
          return (
            <g key={prop.key}>
              <line x1={center} y1={center} x2={x} y2={y} stroke="#334155" strokeWidth="1" strokeDasharray="4,4" />
              <text x={textX} y={textY} fill="#94a3b8" fontSize="8" textAnchor="middle" dominantBaseline="middle">
                {prop.label.split("(")[0].trim()}
              </text>
            </g>
          );
        })}
        {/* Polygons */}
        {comparison.map((_, idx) => (
          <polygon 
            key={idx}
            points={getCoordinates(idx)} 
            fill={colors[idx % colors.length].bg} 
            stroke={colors[idx % colors.length].hex} 
            strokeWidth="3" 
            style={{ mixBlendMode: 'screen' }}
          />
        ))}
      </svg>
    );
  };

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto">
      <div className="w-full max-w-6xl mx-auto space-y-8">
        
        <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Analytics
        </Link>

        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <Scale className="w-8 h-8 text-blue-400" />
            Multi-Material Compare
          </h1>
          <p className="text-slate-300 mt-2">Evaluate properties visually across multiple materials (Pro: up to 5, Advanced: unlimited APIs).</p>
        </div>

        {/* Dynamic Selectors */}
        <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex flex-wrap gap-3 mb-2">
            {selectedIds.map((id, idx) => {
              const mat = allMaterials.find(m => m.id.toString() === id);
              return (
                <div key={idx} className="flex items-center gap-2 bg-slate-950 border border-slate-700 rounded-full px-4 py-1.5 shadow-sm" style={{ borderLeft: `4px solid ${colors[idx % colors.length].hex}` }}>
                  <span className="text-sm font-bold text-white">{mat?.name || id}</span>
                  <button onClick={() => handleRemove(idx)} className="text-slate-500 hover:text-red-400"><X className="w-3 h-3" /></button>
                </div>
              );
            })}
          </div>

          <div className="flex items-center gap-4">
            <select
              onChange={handleAddMaterial}
              className="w-full max-w-sm bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-white appearance-none outline-none focus:border-blue-500"
              disabled={selectedIds.length >= 5}
            >
              <option className="bg-slate-900" value="">{selectedIds.length >= 5 ? "Maximum reached (Pro limit)" : "Add material to compare..."}</option>
              {allMaterials.filter(m => !selectedIds.includes(m.id.toString())).map(m => (
                <option className="bg-slate-900" key={m.id} value={m.id}>{m.name}</option>
              ))}
            </select>
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
          </div>
        ) : comparison.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Radar Fingerprint */}
            <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col">
              <h3 className="font-bold text-white mb-4 text-center">Property Fingerprint</h3>
              <div className="flex-1 flex items-center justify-center py-6">
                {renderRadar()}
              </div>
            </div>

            {/* Properties Table */}
            <div className="lg:col-span-2 space-y-6">
              <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl overflow-x-auto">
                <h3 className="font-bold text-white mb-4">Direct Comparison Matrix</h3>
                <table className="w-full text-left text-sm">
                  <thead>
                    <tr className="border-b border-slate-800">
                      <th className="pb-3 text-slate-400 font-medium whitespace-nowrap">Property</th>
                      {comparison.map((m, idx) => (
                        <th key={idx} className="pb-3 font-bold px-2 whitespace-nowrap" style={{ color: colors[idx % colors.length].hex }}>
                          {m.name}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800">
                    {propsToCompare.map(prop => (
                      <tr key={prop.key}>
                        <td className="py-3 text-slate-300 whitespace-nowrap">{prop.label}</td>
                        {comparison.map((m, idx) => (
                          <td key={idx} className="py-3 px-2 text-slate-200">
                            {m[prop.key] || '-'}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Key Takeaways */}
              {comparison.length >= 2 && (
                <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl">
                  <h3 className="font-bold text-white flex items-center gap-2">
                    <Info className="w-5 h-5 text-purple-400" />
                    Automated Insights & Key Takeaways
                  </h3>
                  {generateTakeaways()}
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="text-center py-20 text-slate-500 bg-slate-900/30 rounded-2xl border border-slate-800 border-dashed">
            Select materials above to generate the comparison matrix and radar fingerprint.
          </div>
        )}
      </div>
    </main>
  );
}
