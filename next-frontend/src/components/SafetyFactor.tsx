"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

export function SafetyFactor() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const [formData, setFormData] = useState({
    yield_strength: 250,
    load_n: 15000,
    area_cm2: 5,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) || 0 });
  };

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/calculators/safety_factor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (data.ok) setResult(data.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="p-6 rounded-2xl bg-neutral-900 border border-neutral-800 shadow-xl w-full h-full flex flex-col">
      <h2 className="text-xl font-bold mb-4 text-white">Safety Factor Analysis</h2>
      <div className="space-y-4 flex-grow">
        <div>
          <label className="block text-xs text-neutral-500 mb-1">Yield Strength (MPa)</label>
          <input type="number" name="yield_strength" value={formData.yield_strength} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:ring-2 focus:ring-emerald-500 outline-none" />
        </div>
        <div>
          <label className="block text-xs text-neutral-500 mb-1">Applied Load (N)</label>
          <input type="number" name="load_n" value={formData.load_n} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:ring-2 focus:ring-emerald-500 outline-none" />
        </div>
        <div>
          <label className="block text-xs text-neutral-500 mb-1">Cross-sectional Area (cm²)</label>
          <input type="number" name="area_cm2" value={formData.area_cm2} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:ring-2 focus:ring-emerald-500 outline-none" />
        </div>
      </div>
      <button onClick={handleCalculate} disabled={loading} className="mt-6 w-full py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-medium flex justify-center items-center">
        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Calculate"}
      </button>
      {result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 rounded-xl bg-emerald-900/20 border border-emerald-900/50">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs text-neutral-400">Stress</span>
            <span className="font-medium text-white">{result.stress_mpa.toFixed(2)} MPa</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-xs text-neutral-400">Safety Factor</span>
            <span className={`font-bold ${result.safety_factor >= 1.5 ? 'text-emerald-400' : 'text-red-400'}`}>{result.safety_factor.toFixed(2)}</span>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}
