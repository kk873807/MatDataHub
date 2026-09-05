"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

export function BeamDeflection() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [formData, setFormData] = useState({ material_name: "Steel", category: "Metal", force_n: 5000, length_mm: 2000, diameter_mm: 50 });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.type === "number" ? parseFloat(e.target.value) || 0 : e.target.value;
    setFormData({ ...formData, [e.target.name]: val });
  };

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/calculators/beam_deflection", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (data.ok) setResult(data.data);
    } catch (e) {} finally { setLoading(false); }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="p-6 rounded-2xl bg-neutral-900 border border-neutral-800 shadow-xl w-full h-full flex flex-col">
      <h2 className="text-xl font-bold mb-4 text-white">Beam Deflection</h2>
      <div className="space-y-4 flex-grow">
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Material Name</label>
            <input type="text" name="material_name" value={formData.material_name} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:ring-2 focus:ring-purple-500 outline-none" />
          </div>
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Category</label>
            <input type="text" name="category" value={formData.category} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:ring-2 focus:ring-purple-500 outline-none" />
          </div>
        </div>
        <div>
          <label className="block text-xs text-neutral-500 mb-1">Force applied (N)</label>
          <input type="number" name="force_n" value={formData.force_n} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white outline-none" />
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Length (mm)</label>
            <input type="number" name="length_mm" value={formData.length_mm} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white outline-none" />
          </div>
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Diameter (mm)</label>
            <input type="number" name="diameter_mm" value={formData.diameter_mm} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white outline-none" />
          </div>
        </div>
      </div>
      <button onClick={handleCalculate} disabled={loading} className="mt-6 w-full py-2.5 rounded-lg bg-purple-600 hover:bg-purple-700 text-white font-medium flex justify-center items-center">
        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Calculate"}
      </button>
      {result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 rounded-xl bg-purple-900/20 border border-purple-900/50">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs text-neutral-400">Modulus (E)</span>
            <span className="font-medium text-white">{result.elastic_modulus_gpa} GPa</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-xs text-neutral-400">Max Deflection</span>
            <span className="font-bold text-purple-400">{result.deflection_mm.toFixed(3)} mm</span>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}
