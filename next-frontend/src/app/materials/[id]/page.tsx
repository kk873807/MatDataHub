"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, TrendingUp, SearchCode, Beaker, ShieldAlert, Loader2, Lock } from "lucide-react";

export default function MaterialDetail() {
  const { id } = useParams();
  const [material, setMaterial] = useState<any>(null);
  const [priceHistory, setPriceHistory] = useState<any[]>([]);
  const [similar, setSimilar] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isSimilarLocked, setIsSimilarLocked] = useState(false);

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        // Fetch Details
        const res = await fetch(`http://127.0.0.1:8000/api/v1/materials/${id}`);
        if (res.ok) setMaterial(await res.json());

        // Fetch Price History
        const priceRes = await fetch(`http://127.0.0.1:8000/api/v1/materials/${id}/price-history`);
        if (priceRes.ok) setPriceHistory(await priceRes.json());

        // Fetch Similar
        const simRes = await fetch(`http://127.0.0.1:8000/api/v1/materials/${id}/similar?limit=3`);
        if (simRes.ok) {
          setSimilar(await simRes.json());
        } else if (simRes.status === 403) {
          setIsSimilarLocked(true);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    if (id) fetchAllData();
  }, [id]);

  if (loading) return <div className="flex justify-center items-center h-screen"><Loader2 className="w-8 h-8 animate-spin text-emerald-500" /></div>;
  if (!material) return <div className="p-10 text-center text-red-400">Material not found.</div>;

  const maxPrice = priceHistory.length > 0 ? Math.max(...priceHistory.map(p => p.cost_per_kg)) : 1;

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full">
      <div className="w-full max-w-7xl mx-auto space-y-6">
        
        <Link href="/materials" className="inline-flex items-center gap-2 text-slate-200 hover:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Database
        </Link>

        {/* Header */}
        <div className="p-8 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="flex flex-col md:flex-row justify-between items-start gap-4">
            <div>
              <div className="inline-block px-3 py-1 bg-emerald-900/30 text-emerald-400 text-xs font-bold rounded-full mb-3 uppercase tracking-wider">
                {material.category} • {material.subcategory}
              </div>
              <h1 className="text-4xl font-bold text-white mb-2">{material.name}</h1>
              <p className="text-slate-200 text-lg max-w-2xl">{material.description || "No description available."}</p>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-right min-w-[200px]">
              <p className="text-slate-300 text-sm mb-1">Current Market Price</p>
              <p className="text-3xl font-bold text-emerald-400">₹{material.cost_per_kg_min}<span className="text-lg text-slate-300">/kg</span></p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Properties Panel */}
          <div className="lg:col-span-2 space-y-6">
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2"><Beaker className="w-5 h-5 text-blue-400"/> Mechanical Properties</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <p className="text-xs text-slate-300">Yield Strength</p>
                  <p className="text-lg font-semibold text-white">{material.yield_strength_min} - {material.yield_strength_max} <span className="text-xs text-slate-300">MPa</span></p>
                </div>
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <p className="text-xs text-slate-300">Tensile Strength</p>
                  <p className="text-lg font-semibold text-white">{material.tensile_strength_min} - {material.tensile_strength_max} <span className="text-xs text-slate-300">MPa</span></p>
                </div>
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <p className="text-xs text-slate-300">Elastic Modulus</p>
                  <p className="text-lg font-semibold text-white">{material.elastic_modulus} <span className="text-xs text-slate-300">GPa</span></p>
                </div>
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <p className="text-xs text-slate-300">Density</p>
                  <p className="text-lg font-semibold text-white">{material.density} <span className="text-xs text-slate-300">g/cm³</span></p>
                </div>
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <p className="text-xs text-slate-300">Hardness</p>
                  <p className="text-lg font-semibold text-white">{material.hardness_value || "-"} <span className="text-xs text-slate-300">{material.hardness_scale}</span></p>
                </div>
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                  <p className="text-xs text-slate-300">Max Temp</p>
                  <p className="text-lg font-semibold text-white">{material.max_service_temp} <span className="text-xs text-slate-300">°C</span></p>
                </div>
              </div>
            </div>

            {/* Historical Price Tracking Graph */}
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
              <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2"><TrendingUp className="w-5 h-5 text-emerald-400"/> Historical Price Tracking (12M)</h3>
              {priceHistory.length > 0 ? (
                <div className="flex items-end gap-2 h-48 mt-4 pt-4 border-t border-slate-800">
                  {priceHistory.map((ph, idx) => {
                    const height = (ph.cost_per_kg / maxPrice) * 100;
                    return (
                      <div key={idx} className="flex-1 flex flex-col items-center gap-2 group relative">
                        <div 
                          className="w-full bg-emerald-500/20 hover:bg-emerald-500/50 border border-emerald-500/50 rounded-t-sm transition-all"
                          style={{ height: `${height}%` }}
                        ></div>
                        <span className="text-[10px] text-slate-300 whitespace-nowrap overflow-hidden text-ellipsis w-full text-center">
                          {new Date(ph.recorded_date).toLocaleString('default', { month: 'short' })}
                        </span>
                        {/* Tooltip */}
                        <div className="absolute -top-10 opacity-0 group-hover:opacity-100 bg-slate-800 text-white text-xs py-1 px-2 rounded pointer-events-none transition-opacity z-10 whitespace-nowrap">
                          ₹{ph.cost_per_kg.toFixed(2)}
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="h-48 mt-4 pt-4 border-t border-slate-800 flex flex-col items-center justify-center text-center">
                  <TrendingUp className="w-8 h-8 text-slate-700 mb-2" />
                  <p className="text-slate-400 text-sm">No historical pricing data available.</p>
                  <p className="text-slate-500 text-xs mt-1">This material lacks baseline cost data in our database.</p>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar Panel */}
          <div className="space-y-6">
            {/* Find Similar AI */}
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2"><SearchCode className="w-5 h-5 text-purple-400"/> Find Similar Materials</h3>
              {isSimilarLocked ? (
                <div className="p-5 rounded-xl bg-slate-950 border border-purple-500/30 text-center relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 to-transparent"></div>
                  <Lock className="w-8 h-8 text-purple-400 mx-auto mb-3 relative z-10" />
                  <h4 className="font-bold text-white text-sm mb-1 relative z-10">Pro Feature Locked</h4>
                  <p className="text-xs text-slate-400 relative z-10 mb-4">Upgrade to automatically discover physically similar materials.</p>
                  <button className="relative z-10 w-full py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-xs font-bold transition-colors">
                    Upgrade to Pro
                  </button>
                </div>
              ) : similar.length > 0 ? (
                <div className="space-y-3">
                  {similar.map(sim => (
                    <Link href={`/materials/${sim.id}`} key={sim.id} className="block p-3 rounded-lg bg-slate-950 border border-slate-800 hover:border-purple-500/50 transition-colors">
                      <p className="font-semibold text-white text-sm">{sim.name}</p>
                      <div className="flex justify-between text-xs text-slate-300 mt-1">
                        <span>{sim.category}</span>
                        <span className="text-purple-400">View →</span>
                      </div>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 text-sm text-slate-400 text-center">
                  <ShieldAlert className="w-6 h-6 text-slate-600 mx-auto mb-2" />
                  No similar materials found in database.
                </div>
              )}
            </div>
            
            {/* Metadata */}
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-sm">
              <h3 className="font-bold text-white mb-4 border-b border-slate-800 pb-2">Standards & Identifiers</h3>
              <div className="space-y-3">
                <div>
                  <span className="text-slate-300 block text-xs">Standard</span>
                  <span className="text-white">{material.standard || "-"}</span>
                </div>
                <div>
                  <span className="text-slate-300 block text-xs">Grade</span>
                  <span className="text-white">{material.grade || "-"}</span>
                </div>
                <div>
                  <span className="text-slate-300 block text-xs">Equivalent Grades</span>
                  <span className="text-white">{material.equivalent_grades || "-"}</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>
  );
}
