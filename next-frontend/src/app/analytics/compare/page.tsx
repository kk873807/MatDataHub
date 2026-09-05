"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, Scale, Loader2, Info } from "lucide-react";

export default function CompareMaterials() {
  const [allMaterials, setAllMaterials] = useState<any[]>([]);
  const [matA, setMatA] = useState("");
  const [matB, setMatB] = useState("");
  
  const [comparison, setComparison] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // Fetch list of materials for dropdowns
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/materials?per_page=100")
      .then(res => res.json())
      .then(data => setAllMaterials(data.materials || []));
  }, []);

  // Fetch comparison when both selected
  useEffect(() => {
    if (matA && matB) {
      setLoading(true);
      fetch(`http://127.0.0.1:8000/api/v1/materials/compare?ids=${matA}&ids=${matB}`)
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
            // Sort to ensure A is first, B is second
            const sorted = [];
            const objA = data.find(m => m.id.toString() === matA);
            const objB = data.find(m => m.id.toString() === matB);
            if (objA) sorted.push(objA);
            if (objB) sorted.push(objB);
            setComparison(sorted);
          }
        })
        .finally(() => setLoading(false));
    } else {
      setComparison([]);
    }
  }, [matA, matB]);

  const propsToCompare = [
    { key: "yield_strength_min", label: "Yield Strength (MPa)", max: 2000 },
    { key: "tensile_strength_min", label: "Tensile Strength (MPa)", max: 2500 },
    { key: "elastic_modulus", label: "Elastic Modulus (GPa)", max: 400 },
    { key: "density", label: "Density (g/cm³)", max: 20 },
    { key: "thermal_conductivity", label: "Thermal Conductivity (W/mK)", max: 400 },
    { key: "cost_per_kg_min", label: "Cost (₹/kg)", max: 100000 }
  ];

  // SVG Radar Chart Logic
  const renderRadar = () => {
    if (comparison.length < 2) return null;
    const center = 150;
    const radius = 100;
    const angleStep = (Math.PI * 2) / propsToCompare.length;
    
    const getCoordinates = (matIndex: number) => {
      const mat = comparison[matIndex];
      return propsToCompare.map((prop, i) => {
        const rawVal = mat[prop.key] || 0;
        // Normalize 0 to 1
        let norm = rawVal / prop.max;
        if (norm > 1) norm = 1;
        
        const angle = i * angleStep - Math.PI / 2; // Start at top
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
              <line x1={center} y1={center} x2={x} y2={y} stroke="#334155" strokeWidth="1" />
              <text x={textX} y={textY} fill="#94a3b8" fontSize="8" textAnchor="middle" dominantBaseline="middle">
                {prop.label.split("(")[0].trim()}
              </text>
            </g>
          );
        })}
        {/* Polygons */}
        <polygon points={getCoordinates(0)} fill="rgba(59, 130, 246, 0.3)" stroke="#3b82f6" strokeWidth="2" />
        <polygon points={getCoordinates(1)} fill="rgba(16, 185, 129, 0.3)" stroke="#10b981" strokeWidth="2" />
      </svg>
    );
  };

  const generateTakeaways = () => {
    if (comparison.length < 2) return null;
    const [a, b] = comparison;
    const takeaways = [];
    
    if (a.yield_strength_min > b.yield_strength_min) takeaways.push(`${a.name} is stronger in yield stress.`);
    else if (b.yield_strength_min > a.yield_strength_min) takeaways.push(`${b.name} is stronger in yield stress.`);

    if (a.cost_per_kg_min < b.cost_per_kg_min) takeaways.push(`${a.name} is more cost-effective.`);
    else if (b.cost_per_kg_min < a.cost_per_kg_min) takeaways.push(`${b.name} is more cost-effective.`);

    if (a.density < b.density) takeaways.push(`${a.name} is lighter, better for aerospace/automotive.`);
    else if (b.density < a.density) takeaways.push(`${b.name} is lighter, better for aerospace/automotive.`);

    return (
      <ul className="list-disc pl-5 space-y-2 text-slate-300 text-sm">
        {takeaways.map((t, i) => <li key={i}>{t}</li>)}
      </ul>
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
            Side-by-Side Comparison
          </h1>
          <p className="text-slate-300 mt-2">Evaluate properties visually and extract key takeaways between materials.</p>
        </div>

        {/* Selectors */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-900 p-6 rounded-2xl border border-slate-800">
          <div>
            <label className="block text-sm font-semibold text-blue-400 mb-2">Material A</label>
            <select
              value={matA}
              onChange={(e) => setMatA(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-white appearance-none outline-none focus:border-blue-500"
            >
              <option className="bg-slate-900" value="">Select Material...</option>
              {allMaterials.map(m => <option className="bg-slate-900" key={m.id} value={m.id}>{m.name}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-semibold text-emerald-400 mb-2">Material B</label>
            <select
              value={matB}
              onChange={(e) => setMatB(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-white appearance-none outline-none focus:border-emerald-500"
            >
              <option className="bg-slate-900" value="">Select Material...</option>
              {allMaterials.map(m => <option className="bg-slate-900" key={m.id} value={m.id}>{m.name}</option>)}
            </select>
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
          </div>
        ) : comparison.length === 2 ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Radar Fingerprint */}
            <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col">
              <h3 className="font-bold text-white mb-4 text-center">Property Fingerprint</h3>
              <div className="flex-1 flex items-center justify-center py-6">
                {renderRadar()}
              </div>
              <div className="flex justify-center gap-6 mt-4">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-blue-500/50 border border-blue-500"></div>
                  <span className="text-xs text-slate-300">Material A</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-emerald-500/50 border border-emerald-500"></div>
                  <span className="text-xs text-slate-300">Material B</span>
                </div>
              </div>
            </div>

            {/* Properties Table */}
            <div className="lg:col-span-2 space-y-6">
              <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl overflow-x-auto">
                <h3 className="font-bold text-white mb-4">Direct Comparison</h3>
                <table className="w-full text-left text-sm">
                  <thead>
                    <tr className="border-b border-slate-800">
                      <th className="pb-3 text-slate-400 font-medium">Property</th>
                      <th className="pb-3 text-blue-400 font-bold">{comparison[0].name}</th>
                      <th className="pb-3 text-emerald-400 font-bold">{comparison[1].name}</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800">
                    {propsToCompare.map(prop => {
                      const valA = comparison[0][prop.key] || 0;
                      const valB = comparison[1][prop.key] || 0;
                      return (
                        <tr key={prop.key}>
                          <td className="py-3 text-slate-300">{prop.label}</td>
                          <td className={`py-3 ${valA > valB ? 'text-white font-semibold' : 'text-slate-400'}`}>
                            {valA || '-'}
                          </td>
                          <td className={`py-3 ${valB > valA ? 'text-white font-semibold' : 'text-slate-400'}`}>
                            {valB || '-'}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {/* Key Takeaways */}
              <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl">
                <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                  <Info className="w-4 h-4 text-purple-400" />
                  Key Takeaways
                </h3>
                {generateTakeaways()}
              </div>
            </div>
            
          </div>
        ) : (
          <div className="text-center py-20 text-slate-500 bg-slate-900/30 rounded-2xl border border-slate-800 border-dashed">
            Select two materials above to generate the comparison matrix and radar fingerprint.
          </div>
        )}
      </div>
    </main>
  );
}
