"use client";
import { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { ArrowLeft, Scale, Loader2, Info, Plus, X, Download, Lock } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { API } from "@/lib/api";
import MaterialSearchSelect from "@/components/MaterialSearchSelect";

function CompareMaterialsContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [allMaterials, setAllMaterials] = useState<any[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  useEffect(() => {
    const addId = searchParams.get("add");
    if (addId && !selectedIds.includes(addId)) setSelectedIds([addId, ...selectedIds]);
  }, [searchParams]);
  const [comparison, setComparison] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [userTier, setUserTier] = useState("free");
  const [isAdmin, setIsAdmin] = useState(false);

  // Colors for up to 5 materials
  const colors = [
    { hex: "#3b82f6", bg: "rgba(59, 130, 246, 0.3)" }, // blue
    { hex: "#10b981", bg: "rgba(16, 185, 129, 0.3)" }, // emerald
    { hex: "#f59e0b", bg: "rgba(245, 158, 11, 0.3)" }, // amber
    { hex: "#8b5cf6", bg: "rgba(139, 92, 246, 0.3)" }, // purple
    { hex: "#ec4899", bg: "rgba(236, 72, 153, 0.3)" }  // pink
  ];

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setIsAuthenticated(false);
      return;
    }
    fetch(`${API}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(async r => {
        if (r.ok) {
          const data = await r.json();
          setIsAuthenticated(true);
          setUserTier(data.tier || "free");
          setIsAdmin(data.is_admin || false);
        } else {
          setIsAuthenticated(false);
        }
      })
      .catch(() => setIsAuthenticated(false));
  }, []);

  // Fetch list of materials for dropdowns
  useEffect(() => {
    fetch(`${API}/materials?per_page=2000`)
      .then(res => res.json())
      .then(data => setAllMaterials(data.materials || []));
  }, []);

  // Fetch comparison
  useEffect(() => {
    if (selectedIds.length > 0) {
      setLoading(true);
      const token = localStorage.getItem("token");
      const headers: Record<string, string> = {};
      if (token) headers["Authorization"] = `Bearer ${token}`;
      const queryParams = selectedIds.map(id => `ids=${id}`).join("&");
      fetch(`${API}/materials/compare?${queryParams}`, { headers })
        .then(res => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.json();
        })
        .then(data => {
          if (Array.isArray(data)) {
            const sorted = selectedIds.map(id => data.find(m => m.id.toString() === id)).filter(Boolean);
            setComparison(sorted);
          }
        })
        .catch(err => console.error("Compare failed:", err))
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

  const maxCompare = isAdmin ? 99 : userTier === "advanced" ? 99 : userTier === "pro" ? 5 : 2;

  const handleAddMaterial = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    if (val && !selectedIds.includes(val) && selectedIds.length < maxCompare) {
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
      <ul className="list-disc pl-5 space-y-2 text-slate-600 dark:text-slate-300 text-sm mt-4">
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

  // CSV Export
  const exportCSV = () => {
    if (comparison.length === 0) return;
    const header = ["Property", ...comparison.map(m => m.name)].join(",");
    const rows = propsToCompare.map(prop => 
      [prop.label, ...comparison.map(m => m[prop.key] ?? "")].join(",")
    );
    const csv = [header, ...rows].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "material_comparison.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  // Winner detection (higher = better for most props, lower = better for cost/density/carbon/water)
  const lowerIsBetter = new Set(["density", "embodied_carbon", "water_usage", "cost_per_kg_min"]);
  const getBestIndex = (prop: { key: string }) => {
    if (comparison.length < 2) return -1;
    const vals = comparison.map(m => m[prop.key] ?? null);
    if (vals.every(v => v === null)) return -1;
    const isLower = lowerIsBetter.has(prop.key);
    let bestIdx = 0;
    for (let i = 1; i < vals.length; i++) {
      if (vals[i] === null) continue;
      if (vals[bestIdx] === null) { bestIdx = i; continue; }
      if (isLower ? vals[i] < vals[bestIdx] : vals[i] > vals[bestIdx]) bestIdx = i;
    }
    return vals[bestIdx] !== null ? bestIdx : -1;
  };

  if (isAuthenticated === null) {
    return <div className="flex items-center justify-center h-screen"><Loader2 className="w-8 h-8 animate-spin text-blue-500" /></div>;
  }

  if (isAuthenticated === false) {
    return (
      <main className="flex flex-col p-6 lg:p-10 w-full h-full">
        <div className="w-full max-w-5xl mx-auto space-y-6">
          <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to Analytics
          </Link>
          
          <div className="p-10 mt-10 rounded-3xl bg-white dark:bg-slate-900 border border-blue-500/30 text-center relative overflow-hidden flex flex-col items-center justify-center">
            <div className="w-20 h-20 bg-blue-950 rounded-full flex items-center justify-center mb-6 relative z-10 border border-blue-500/50">
              <Lock className="w-10 h-10 text-blue-500" />
            </div>
            
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white font-heading mb-4 relative z-10">Sign In Required</h2>
            <p className="text-slate-600 dark:text-slate-300 relative z-10 max-w-2xl mx-auto mb-8 text-lg">
              You must be signed in to use the Multi-Material Compare tool. 
            </p>
            
            <Link href="/account" className="relative z-10 px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold transition-all shadow-lg hover:scale-105">
              Sign In or Register
            </Link>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto">
      <div className="w-full max-w-6xl mx-auto space-y-8">
        
        <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Analytics
        </Link>

        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-3">
            <Scale className="w-8 h-8 text-blue-400" />
            Multi-Material Compare
          </h1>
          <p className="text-slate-600 dark:text-slate-300 mt-2">Evaluate properties visually across multiple materials (Pro: up to 5, Advanced: unlimited APIs).</p>
        </div>

        {/* Dynamic Selectors */}
        <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-4">
          <div className="flex flex-wrap gap-3 mb-2">
            {selectedIds.map((id, idx) => {
              const mat = allMaterials.find(m => m.id.toString() === id);
              return (
                <div key={idx} className="flex items-center gap-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-700 rounded-full px-4 py-1.5 shadow-sm" style={{ borderLeft: `4px solid ${colors[idx % colors.length].hex}` }}>
                  <span className="text-sm font-bold text-slate-900 dark:text-white">{mat?.name || id}</span>
                  <button onClick={() => handleRemove(idx)} className="text-slate-500 dark:text-slate-400 hover:text-red-400"><X className="w-3 h-3" /></button>
                </div>
              );
            })}
          </div>

          <div className="flex items-center gap-4">
            <MaterialSearchSelect
              materials={allMaterials}
              excludeIds={selectedIds}
              disabled={selectedIds.length >= maxCompare}
              placeholder={selectedIds.length >= maxCompare ? `Maximum reached (${userTier} tier limit: ${maxCompare})` : "Search and add material..."}
              onSelect={(id) => {
                if (!selectedIds.includes(id) && selectedIds.length < maxCompare) {
                  setSelectedIds([...selectedIds, id]);
                }
              }}
            />
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
          </div>
        ) : comparison.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Radar Fingerprint */}
            <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl flex flex-col">
              <h3 className="font-bold text-slate-900 dark:text-white font-heading mb-4 text-center">Property Fingerprint</h3>
              <div className="flex-1 flex items-center justify-center py-6">
                {renderRadar()}
              </div>
            </div>

            {/* Properties Table */}
            <div className="lg:col-span-2 space-y-6">
              <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-x-auto">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="font-bold text-slate-900 dark:text-white font-heading">Direct Comparison Matrix</h3>
                  <button onClick={exportCSV} className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs font-bold rounded-2xl transition-colors border border-slate-200 dark:border-slate-700">
                    <Download className="w-3 h-3" /> Export CSV
                  </button>
                </div>
                <table className="w-full text-left text-sm">
                  <thead>
                    <tr className="border-b border-slate-200 dark:border-slate-800">
                      <th className="pb-3 text-slate-500 dark:text-slate-400 font-medium whitespace-nowrap">Property</th>
                      {comparison.map((m, idx) => (
                        <th key={idx} className="pb-3 font-bold px-2 whitespace-nowrap" style={{ color: colors[idx % colors.length].hex }}>
                          {m.name}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800">
                    {propsToCompare.map(prop => {
                      const bestIdx = getBestIndex(prop);
                      return (
                        <tr key={prop.key}>
                          <td className="py-3 text-slate-600 dark:text-slate-300 whitespace-nowrap">{prop.label}</td>
                          {comparison.map((m, idx) => (
                            <td key={idx} className={`py-3 px-2 font-medium ${idx === bestIdx ? 'text-emerald-400 font-bold' : 'text-slate-200'}`}>
                              {m[prop.key] || '-'}
                              {idx === bestIdx && m[prop.key] && <span className="ml-1 text-[10px]">★</span>}
                            </td>
                          ))}
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {/* Key Takeaways */}
              {comparison.length >= 2 && (
                <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl">
                  <h3 className="font-bold text-slate-900 dark:text-white font-heading flex items-center gap-2">
                    <Info className="w-5 h-5 text-purple-400" />
                    Automated Insights & Key Takeaways
                  </h3>
                  {generateTakeaways()}
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="text-center py-20 text-slate-500 dark:text-slate-400 bg-white dark:bg-slate-900/30 rounded-2xl border border-slate-200 dark:border-slate-800 border-dashed">
            Select materials above to generate the comparison matrix and radar fingerprint.
          </div>
        )}
      </div>
    </main>
  );
}

export default function CompareMaterials() { return <Suspense fallback={<div className='p-12 text-center text-slate-500 dark:text-slate-400'>Loading...</div>}><CompareMaterialsContent /></Suspense>; }
