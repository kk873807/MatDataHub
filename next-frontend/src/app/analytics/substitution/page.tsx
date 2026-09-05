"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, Replace, Loader2, Lock, ShieldAlert } from "lucide-react";

export default function SmartSubstitution() {
  const [allMaterials, setAllMaterials] = useState<any[]>([]);
  const [baseId, setBaseId] = useState("");
  const [weights, setWeights] = useState({
    cost: 50,
    density: 50,
    tensile: 50,
    carbon: 50
  });
  
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [isLocked, setIsLocked] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/materials?per_page=100")
      .then(res => res.json())
      .then(data => setAllMaterials(data.materials || []));
  }, []);

  const runSubstitution = async () => {
    if (!baseId) return;
    setLoading(true);
    setIsLocked(false);
    
    try {
      // Normalize weights 0-100 to 0.0-1.0
      const normalizedWeights = {
        cost: weights.cost / 100,
        density: weights.density / 100,
        tensile: weights.tensile / 100,
        carbon: weights.carbon / 100
      };

      const res = await fetch("http://127.0.0.1:8000/api/v1/materials/substitute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          base_material_id: parseInt(baseId),
          weights: normalizedWeights
        })
      });

      if (res.ok) {
        setResults(await res.json());
      } else if (res.status === 403) {
        setIsLocked(true);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto">
      <div className="w-full max-w-5xl mx-auto space-y-8">
        
        <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Analytics
        </Link>

        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <Replace className="w-8 h-8 text-purple-400" />
            Smart AI Substitution
          </h1>
          <p className="text-slate-300 mt-2">Discover optimal alternative materials based on weighted design priorities.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Controls Panel */}
          <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 space-y-6">
            <div>
              <label className="block text-sm font-semibold text-slate-200 mb-2">Base Material</label>
              <select
                value={baseId}
                onChange={(e) => setBaseId(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-white appearance-none outline-none focus:border-purple-500"
              >
                <option className="bg-slate-900" value="">Select target to replace...</option>
                {allMaterials.map(m => <option className="bg-slate-900" key={m.id} value={m.id}>{m.name}</option>)}
              </select>
            </div>

            <div className="space-y-4 pt-2 border-t border-slate-800">
              <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider">Optimization Weights</h3>
              
              <div>
                <div className="flex justify-between text-xs text-slate-300 mb-1">
                  <span>Reduce Cost</span>
                  <span>{weights.cost}%</span>
                </div>
                <input type="range" min="0" max="100" value={weights.cost} onChange={e => setWeights({...weights, cost: parseInt(e.target.value)})} className="w-full accent-purple-500" />
              </div>

              <div>
                <div className="flex justify-between text-xs text-slate-300 mb-1">
                  <span>Reduce Weight (Density)</span>
                  <span>{weights.density}%</span>
                </div>
                <input type="range" min="0" max="100" value={weights.density} onChange={e => setWeights({...weights, density: parseInt(e.target.value)})} className="w-full accent-purple-500" />
              </div>

              <div>
                <div className="flex justify-between text-xs text-slate-300 mb-1">
                  <span>Maximize Strength (Tensile)</span>
                  <span>{weights.tensile}%</span>
                </div>
                <input type="range" min="0" max="100" value={weights.tensile} onChange={e => setWeights({...weights, tensile: parseInt(e.target.value)})} className="w-full accent-purple-500" />
              </div>

              <div>
                <div className="flex justify-between text-xs text-slate-300 mb-1">
                  <span>Minimize Carbon (ESG)</span>
                  <span>{weights.carbon}%</span>
                </div>
                <input type="range" min="0" max="100" value={weights.carbon} onChange={e => setWeights({...weights, carbon: parseInt(e.target.value)})} className="w-full accent-purple-500" />
              </div>
            </div>

            <button 
              onClick={runSubstitution}
              disabled={!baseId || loading}
              className="w-full py-3 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg font-bold transition-colors"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : "Run AI Substitution"}
            </button>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2">
            {isLocked ? (
              <div className="p-8 h-full rounded-2xl bg-slate-900 border border-purple-500/30 text-center relative overflow-hidden flex flex-col items-center justify-center">
                <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 to-transparent"></div>
                <Lock className="w-12 h-12 text-purple-400 mx-auto mb-4 relative z-10" />
                <h2 className="text-2xl font-bold text-white mb-2 relative z-10">Pro Feature Locked</h2>
                <p className="text-slate-300 relative z-10 max-w-md mx-auto mb-6">
                  Smart AI Substitution is an advanced engine that analyzes hundreds of parametric variables to recommend material replacements. Upgrade to Pro to unlock this workflow.
                </p>
                <button className="relative z-10 px-8 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-bold transition-colors shadow-lg shadow-purple-900/50">
                  Upgrade to Pro
                </button>
              </div>
            ) : results.length > 0 ? (
              <div className="space-y-4">
                <h3 className="font-bold text-white">Top Alternative Recommendations</h3>
                {results.map((res, i) => (
                  <div key={res.id} className="bg-slate-900 p-5 rounded-xl border border-slate-800 relative overflow-hidden">
                    {i === 0 && <div className="absolute top-0 right-0 bg-purple-600 text-white text-[10px] font-bold px-3 py-1 rounded-bl-lg">BEST MATCH</div>}
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h4 className="text-lg font-bold text-white">{res.name}</h4>
                        <div className="text-sm text-purple-400 font-semibold">{Math.round(res.match_score * 100)}% Match Score</div>
                      </div>
                      <Link href={`/materials/${res.id}`} className="px-3 py-1 bg-slate-950 border border-slate-800 rounded text-xs text-slate-300 hover:text-white transition-colors">
                        View Details
                      </Link>
                    </div>
                    <div className="grid grid-cols-4 gap-4 pt-3 border-t border-slate-800">
                      <div>
                        <div className="text-[10px] text-slate-400 uppercase">Cost</div>
                        <div className="text-sm font-medium text-slate-200">₹{res.cost}/kg</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-400 uppercase">Density</div>
                        <div className="text-sm font-medium text-slate-200">{res.density} g/cm³</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-400 uppercase">Tensile</div>
                        <div className="text-sm font-medium text-slate-200">{res.tensile} MPa</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-400 uppercase">Carbon</div>
                        <div className="text-sm font-medium text-slate-200">{res.carbon} kgCO2</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-8 h-full rounded-2xl bg-slate-900 border border-slate-800 flex flex-col items-center justify-center text-center">
                <ShieldAlert className="w-10 h-10 text-slate-700 mb-4" />
                <h3 className="text-lg font-bold text-slate-400">Ready to Analyze</h3>
                <p className="text-sm text-slate-500 mt-2 max-w-sm">
                  Select a base material and configure your design priorities to discover optimal engineering alternatives.
                </p>
              </div>
            )}
          </div>

        </div>
      </div>
    </main>
  );
}
