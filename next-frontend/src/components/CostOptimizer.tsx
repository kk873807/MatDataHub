"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { IndianRupee, Loader2 } from "lucide-react";

export function CostOptimizer() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const [formData, setFormData] = useState({
    cost_per_kg: 5.5,
    volume_cm3: 100,
    density_gcm3: 2.7,
    batch_size: 1000
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) || 0 });
  };

  const handleCalculate = async () => {
    setLoading(true);
    // Simulate API call for complex cost optimization logic
    setTimeout(() => {
      const massKg = (formData.volume_cm3 * formData.density_gcm3) / 1000;
      const unitMaterialCost = massKg * formData.cost_per_kg;
      
      // Simple volume discount logic
      const discount = formData.batch_size > 5000 ? 0.15 : (formData.batch_size > 1000 ? 0.05 : 0);
      const optimizedUnitCost = unitMaterialCost * (1 - discount);
      
      setResult({
        unit_cost: unitMaterialCost,
        optimized_unit_cost: optimizedUnitCost,
        total_batch_cost: optimizedUnitCost * formData.batch_size,
        discount_applied: discount * 100
      });
      setLoading(false);
    }, 600);
  };

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="w-full">
      <div className="flex items-center gap-3 mb-4 border-b border-slate-700 pb-3">
        <div className="p-2 bg-emerald-900/30 rounded-lg text-emerald-400">
          <IndianRupee className="w-5 h-5" />
        </div>
        <div>
          <h3 className="font-bold text-white leading-tight">Cost Optimizer</h3>
          <p className="text-xs text-slate-400">Estimate volume discounting and batch costs</p>
        </div>
      </div>

      <div className="space-y-3">
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs text-slate-300 mb-1">Cost (₹/kg)</label>
            <input type="number" name="cost_per_kg" value={formData.cost_per_kg} onChange={handleChange} className="w-full bg-slate-800 rounded px-3 py-2 text-sm text-white outline-none focus:ring-1 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-xs text-slate-300 mb-1">Volume (cm³)</label>
            <input type="number" name="volume_cm3" value={formData.volume_cm3} onChange={handleChange} className="w-full bg-slate-800 rounded px-3 py-2 text-sm text-white outline-none focus:ring-1 focus:ring-emerald-500" />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs text-slate-300 mb-1">Density (g/cm³)</label>
            <input type="number" name="density_gcm3" value={formData.density_gcm3} onChange={handleChange} className="w-full bg-slate-800 rounded px-3 py-2 text-sm text-white outline-none focus:ring-1 focus:ring-emerald-500" />
          </div>
          <div>
            <label className="block text-xs text-slate-300 mb-1">Batch Size</label>
            <input type="number" name="batch_size" value={formData.batch_size} onChange={handleChange} className="w-full bg-slate-800 rounded px-3 py-2 text-sm text-white outline-none focus:ring-1 focus:ring-emerald-500" />
          </div>
        </div>
      </div>
      
      <button onClick={handleCalculate} disabled={loading} className="mt-5 w-full py-2 rounded bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold flex justify-center items-center transition-colors">
        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Optimize Cost"}
      </button>

      {result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 rounded-xl bg-emerald-900/20 border border-emerald-900/50 space-y-2">
          <div className="flex justify-between items-center border-b border-emerald-900/30 pb-2">
            <span className="text-xs text-slate-300">Base Unit Cost</span>
            <span className="font-medium text-slate-300">₹{result.unit_cost.toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-xs text-emerald-400 font-bold">Optimized Unit Cost</span>
            <span className="font-bold text-emerald-400">₹{result.optimized_unit_cost.toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center pt-1">
            <span className="text-xs text-slate-400">Total Batch Cost ({formData.batch_size} units)</span>
            <span className="font-bold text-white">₹{result.total_batch_cost.toFixed(2)}</span>
          </div>
          <p className="text-[10px] text-emerald-300 pt-2 border-t border-emerald-900/50">Volume discount of {result.discount_applied}% applied based on batch size economies of scale.</p>
        </motion.div>
      )}
    </motion.div>
  );
}
