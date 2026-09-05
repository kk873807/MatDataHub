"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, Layers, Loader2, Beaker } from "lucide-react";

export default function CompositeSynthesizer() {
  const [allMaterials, setAllMaterials] = useState<any[]>([]);
  const [matA, setMatA] = useState("");
  const [matB, setMatB] = useState("");
  const [volFractionA, setVolFractionA] = useState(50);
  
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/materials?per_page=100")
      .then(res => res.json())
      .then(data => setAllMaterials(data.materials || []));
  }, []);

  const handleSynthesize = () => {
    if (!matA || !matB) return;
    setLoading(true);
    
    // Simulate API call for Rule of Mixtures calculation
    setTimeout(() => {
      const objA = allMaterials.find(m => m.id.toString() === matA);
      const objB = allMaterials.find(m => m.id.toString() === matB);
      
      if (objA && objB) {
        const vA = volFractionA / 100;
        const vB = 1 - vA;
        
        // Rule of Mixtures (Upper Bound)
        const density = (objA.density * vA) + (objB.density * vB);
        const elastic_modulus = (objA.elastic_modulus * vA) + (objB.elastic_modulus * vB);
        const tensile = (objA.tensile_strength_min * vA) + (objB.tensile_strength_min * vB);
        const cost = (objA.cost_per_kg_min * vA) + (objB.cost_per_kg_min * vB);
        
        setResult({
          name: `Composite: ${vA*100}% ${objA.name} / ${vB*100}% ${objB.name}`,
          density: density.toFixed(2),
          elastic_modulus: elastic_modulus.toFixed(1),
          tensile: tensile.toFixed(0),
          cost: cost.toFixed(2)
        });
      }
      setLoading(false);
    }, 600);
  };

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto">
      <div className="w-full max-w-4xl mx-auto space-y-8">
        
        <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Analytics
        </Link>

        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <Layers className="w-8 h-8 text-cyan-400" />
            Composite Material Synthesizer
          </h1>
          <p className="text-slate-300 mt-2">Blend two materials using the Rule of Mixtures to predict hybrid mechanical properties.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Controls */}
          <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 space-y-6">
            <div>
              <label className="block text-sm font-semibold text-cyan-400 mb-2">Matrix Material (A)</label>
              <select value={matA} onChange={(e) => setMatA(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-white appearance-none outline-none focus:border-cyan-500">
                <option value="">Select Material...</option>
                {allMaterials.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-teal-400 mb-2">Reinforcement Material (B)</label>
              <select value={matB} onChange={(e) => setMatB(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-white appearance-none outline-none focus:border-teal-500">
                <option value="">Select Material...</option>
                {allMaterials.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
              </select>
            </div>

            <div>
              <div className="flex justify-between text-sm text-slate-300 mb-2">
                <span>Volume Fraction (Matrix A)</span>
                <span className="font-bold text-cyan-400">{volFractionA}%</span>
              </div>
              <input type="range" min="0" max="100" value={volFractionA} onChange={e => setVolFractionA(parseInt(e.target.value))} className="w-full accent-cyan-500" />
              <div className="flex justify-between text-xs text-slate-500 mt-1">
                <span>0% (All B)</span>
                <span>100% (All A)</span>
              </div>
            </div>

            <button 
              onClick={handleSynthesize}
              disabled={!matA || !matB || loading}
              className="w-full py-3 bg-cyan-600 hover:bg-cyan-700 disabled:opacity-50 text-white font-bold rounded-lg transition-colors flex items-center justify-center gap-2"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Beaker className="w-5 h-5" />}
              Synthesize Composite
            </button>
          </div>

          {/* Results */}
          <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 flex flex-col justify-center min-h-[300px]">
            {result ? (
              <div className="space-y-6">
                <div className="text-center">
                  <h3 className="text-sm text-slate-400 uppercase tracking-wider font-bold mb-1">Generated Hybrid</h3>
                  <p className="text-lg font-bold text-white leading-tight">{result.name}</p>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-center">
                    <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">Density</p>
                    <p className="text-2xl font-bold text-white">{result.density} <span className="text-sm font-normal text-slate-500">g/cm³</span></p>
                  </div>
                  <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-center">
                    <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">Est. Cost</p>
                    <p className="text-2xl font-bold text-emerald-400">₹{result.cost} <span className="text-sm font-normal text-emerald-600">/kg</span></p>
                  </div>
                  <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-center">
                    <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">Tensile Strength</p>
                    <p className="text-2xl font-bold text-white">{result.tensile} <span className="text-sm font-normal text-slate-500">MPa</span></p>
                  </div>
                  <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-center">
                    <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">Elastic Modulus</p>
                    <p className="text-2xl font-bold text-white">{result.elastic_modulus} <span className="text-sm font-normal text-slate-500">GPa</span></p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center text-slate-500">
                <Layers className="w-12 h-12 mx-auto mb-4 text-slate-700" />
                <p>Select two materials and adjust the volume fraction to calculate hybrid properties.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
