"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Flame, Loader2 } from "lucide-react";

export function ThermalShock() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const [formData, setFormData] = useState({
    thermal_conductivity: 25,
    tensile_strength: 300,
    elastic_modulus: 70,
    thermal_expansion: 23,
    delta_t: 150
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) || 0 });
  };

  const handleCalculate = async () => {
    setLoading(true);
    // Simulate API calculation
    setTimeout(() => {
      // Thermal shock resistance parameter (R) approx formula:
      // R = (Tensile Strength * Thermal Conductivity) / (Elastic Modulus * Thermal Expansion)
      // Note: scaling factors applied for units matching
      const R_score = (formData.tensile_strength * formData.thermal_conductivity * 100) / 
                      (formData.elastic_modulus * 1e9 * formData.thermal_expansion * 1e-6);
      
      const induced_stress = formData.elastic_modulus * 1e3 * formData.thermal_expansion * 1e-6 * formData.delta_t; // MPa
      const survival_margin = formData.tensile_strength - induced_stress;

      setResult({
        r_score: R_score * 10,
        induced_stress: induced_stress,
        margin: survival_margin,
        survives: survival_margin > 0
      });
      setLoading(false);
    }, 600);
  };

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="w-full">
      <div className="flex items-center gap-3 mb-4 border-b border-slate-700 pb-3">
        <div className="p-2 bg-orange-900/30 rounded-lg text-orange-500">
          <Flame className="w-5 h-5" />
        </div>
        <div>
          <h3 className="font-bold text-white leading-tight">Thermal Shock Estimator</h3>
          <p className="text-xs text-slate-400">Assess fracture risk from rapid temp changes</p>
        </div>
      </div>

      <div className="space-y-3">
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-[10px] text-slate-300 mb-1 uppercase tracking-wider">Tensile (MPa)</label>
            <input type="number" name="tensile_strength" value={formData.tensile_strength} onChange={handleChange} className="w-full bg-slate-800 rounded px-2 py-1.5 text-sm text-white outline-none focus:ring-1 focus:ring-orange-500" />
          </div>
          <div>
            <label className="block text-[10px] text-slate-300 mb-1 uppercase tracking-wider">Modulus (GPa)</label>
            <input type="number" name="elastic_modulus" value={formData.elastic_modulus} onChange={handleChange} className="w-full bg-slate-800 rounded px-2 py-1.5 text-sm text-white outline-none focus:ring-1 focus:ring-orange-500" />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-[10px] text-slate-300 mb-1 uppercase tracking-wider">Conductivity (W/mK)</label>
            <input type="number" name="thermal_conductivity" value={formData.thermal_conductivity} onChange={handleChange} className="w-full bg-slate-800 rounded px-2 py-1.5 text-sm text-white outline-none focus:ring-1 focus:ring-orange-500" />
          </div>
          <div>
            <label className="block text-[10px] text-slate-300 mb-1 uppercase tracking-wider">Expansion (µm/mK)</label>
            <input type="number" name="thermal_expansion" value={formData.thermal_expansion} onChange={handleChange} className="w-full bg-slate-800 rounded px-2 py-1.5 text-sm text-white outline-none focus:ring-1 focus:ring-orange-500" />
          </div>
        </div>
        <div>
          <label className="block text-xs text-orange-300 mb-1 font-semibold mt-2">Expected Sudden Temp Drop (ΔT °C)</label>
          <input type="number" name="delta_t" value={formData.delta_t} onChange={handleChange} className="w-full bg-slate-900 border border-orange-900/50 rounded px-3 py-2 text-sm text-white outline-none focus:ring-1 focus:ring-orange-500" />
        </div>
      </div>
      
      <button onClick={handleCalculate} disabled={loading} className="mt-5 w-full py-2 rounded bg-orange-600 hover:bg-orange-700 text-white text-sm font-bold flex justify-center items-center transition-colors">
        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Run Simulation"}
      </button>

      {result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className={`mt-4 p-4 rounded-xl border ${result.survives ? 'bg-emerald-900/20 border-emerald-900/50' : 'bg-red-900/20 border-red-900/50'} space-y-2`}>
          <div className="flex justify-between items-center mb-1">
            <span className="text-xs text-slate-300">Induced Surface Stress</span>
            <span className="font-medium text-white">{result.induced_stress.toFixed(1)} MPa</span>
          </div>
          <div className="flex justify-between items-center mb-2 pb-2 border-b border-slate-700/50">
            <span className="text-xs text-slate-300">Safety Margin</span>
            <span className={`font-bold ${result.survives ? 'text-emerald-400' : 'text-red-400'}`}>{result.margin.toFixed(1)} MPa</span>
          </div>
          <p className={`text-xs font-bold text-center ${result.survives ? 'text-emerald-400' : 'text-red-400'}`}>
            {result.survives ? '✓ Material Survives Thermal Shock' : '⚠ Fracture Imminent'}
          </p>
          <p className="text-[10px] text-slate-400 text-center">Induced stress compares the sudden contraction forces against the material's yield limits.</p>
        </motion.div>
      )}
    </motion.div>
  );
}
