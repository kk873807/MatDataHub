"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

export function Synthesizer() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const [formData, setFormData] = useState({
    mat1_density: 2.7,
    mat1_tensile: 310,
    mat1_cost_min: 2.5,
    mat1_vol_percent: 60,
    mat2_density: 7.8,
    mat2_tensile: 400,
    mat2_cost_min: 1.2,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) || 0 });
  };

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/calculators/synthesizer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (data.ok) {
        setResult(data.data);
      }
    } catch (error) {
      console.error("Error calculating:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 rounded-2xl bg-neutral-900 border border-neutral-800 shadow-xl max-w-2xl w-full mx-auto"
    >
      <h2 className="text-2xl font-bold mb-6 text-white flex items-center gap-2">
        Composite Synthesizer
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Material 1 */}
        <div className="space-y-4 p-4 rounded-xl bg-neutral-950/50 border border-neutral-800/50">
          <h3 className="text-lg font-medium text-neutral-300">Material 1</h3>
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Density (g/cm³)</label>
            <input type="number" name="mat1_density" value={formData.mat1_density} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Tensile Strength (MPa)</label>
            <input type="number" name="mat1_tensile" value={formData.mat1_tensile} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Cost ($/kg)</label>
            <input type="number" name="mat1_cost_min" value={formData.mat1_cost_min} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Volume %</label>
            <input type="number" name="mat1_vol_percent" value={formData.mat1_vol_percent} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
        </div>

        {/* Material 2 */}
        <div className="space-y-4 p-4 rounded-xl bg-neutral-950/50 border border-neutral-800/50">
          <h3 className="text-lg font-medium text-neutral-300">Material 2</h3>
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Density (g/cm³)</label>
            <input type="number" name="mat2_density" value={formData.mat2_density} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Tensile Strength (MPa)</label>
            <input type="number" name="mat2_tensile" value={formData.mat2_tensile} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Cost ($/kg)</label>
            <input type="number" name="mat2_cost_min" value={formData.mat2_cost_min} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Volume %</label>
            <div className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-neutral-500 cursor-not-allowed">
              {100 - formData.mat1_vol_percent}% (Auto)
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6">
        <button 
          onClick={handleCalculate}
          disabled={loading}
          className="w-full py-3 rounded-lg bg-blue-600 hover:bg-blue-700 transition-colors text-white font-medium flex items-center justify-center gap-2"
        >
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Calculate Blend Properties"}
        </button>
      </div>

      {result && (
        <motion.div 
          initial={{ opacity: 0, height: 0 }} 
          animate={{ opacity: 1, height: "auto" }}
          className="mt-6 p-4 rounded-xl bg-blue-900/20 border border-blue-900/50"
        >
          <h3 className="text-blue-400 font-medium mb-3">Estimated Composite Properties</h3>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <p className="text-xs text-neutral-400">Density</p>
              <p className="text-lg font-semibold text-white">{result.blend_density.toFixed(2)} <span className="text-sm font-normal text-neutral-500">g/cm³</span></p>
            </div>
            <div>
              <p className="text-xs text-neutral-400">Tensile Strength</p>
              <p className="text-lg font-semibold text-white">{result.blend_tensile.toFixed(0)} <span className="text-sm font-normal text-neutral-500">MPa</span></p>
            </div>
            <div>
              <p className="text-xs text-neutral-400">Cost</p>
              <p className="text-lg font-semibold text-white">${result.blend_cost.toFixed(2)} <span className="text-sm font-normal text-neutral-500">/kg</span></p>
            </div>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}
