"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

export function FatigueLife() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [formData, setFormData] = useState({ material_name: "Alloy Steel", category: "Metal", tensile_strength: 850 });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.type === "number" ? parseFloat(e.target.value) || 0 : e.target.value;
    setFormData({ ...formData, [e.target.name]: val });
  };

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/calculators/fatigue_life", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (data.ok) setResult(data.data);
    } catch (e) {} finally { setLoading(false); }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl w-full h-full flex flex-col">
      <h2 className="text-xl font-bold mb-4 text-white">Fatigue Life Estimation</h2>
      <div className="space-y-4 flex-grow">
        <div>
          <label className="block text-xs text-slate-300 mb-1">Material Name</label>
          <input type="text" name="material_name" value={formData.material_name} onChange={handleChange} className="w-full bg-slate-800 rounded px-3 py-2 text-sm text-white focus:ring-2 focus:ring-cyan-500 outline-none" />
        </div>
        <div>
          <label className="block text-xs text-slate-300 mb-1">Category</label>
          <input type="text" name="category" value={formData.category} onChange={handleChange} className="w-full bg-slate-800 rounded px-3 py-2 text-sm text-white focus:ring-2 focus:ring-cyan-500 outline-none" />
        </div>
        <div>
          <label className="block text-xs text-slate-300 mb-1">Ultimate Tensile Strength (MPa)</label>
          <input type="number" name="tensile_strength" value={formData.tensile_strength} onChange={handleChange} className="w-full bg-slate-800 rounded px-3 py-2 text-sm text-white outline-none" />
        </div>
      </div>
      <button onClick={handleCalculate} disabled={loading} className="mt-6 w-full py-2.5 rounded-lg bg-cyan-600 hover:bg-cyan-700 text-white font-medium flex justify-center items-center">
        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Estimate Endurance"}
      </button>
      {result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 rounded-xl bg-cyan-900/20 border border-cyan-900/50">
          <p className="text-xs text-slate-200 mb-2">{result.note}</p>
          <div className="flex justify-between items-center">
            <span className="text-xs text-slate-200">Endurance Limit</span>
            <span className="font-bold text-cyan-400">{result.endurance_limit.toFixed(1)} MPa</span>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}
