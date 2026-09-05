"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Loader2, AlertTriangle, ShieldCheck } from "lucide-react";

export function RiskAuditor() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [formData, setFormData] = useState({ material_name: "Titanium Alloy", embodied_carbon: 35.0, cost_per_kg_inr: 2500, volume_tons: 50, cbam_price_usd: 90 });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.type === "number" ? parseFloat(e.target.value) || 0 : e.target.value;
    setFormData({ ...formData, [e.target.name]: val });
  };

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/calculators/risk_auditor", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (data.ok) setResult(data.data);
    } catch (e) {} finally { setLoading(false); }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="p-6 rounded-2xl bg-neutral-900 border border-neutral-800 shadow-xl w-full col-span-1 md:col-span-2 lg:col-span-3">
      <h2 className="text-xl font-bold mb-6 text-white">Supply Chain & ESG Risk Auditor</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-4">
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Material Name (For Geopolitical AI Analysis)</label>
            <input type="text" name="material_name" value={formData.material_name} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white focus:ring-2 focus:ring-red-500 outline-none" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs text-neutral-500 mb-1">Embodied Carbon (kg CO2e/kg)</label>
              <input type="number" name="embodied_carbon" value={formData.embodied_carbon} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white outline-none" />
            </div>
            <div>
              <label className="block text-xs text-neutral-500 mb-1">Est. Volume (Tons)</label>
              <input type="number" name="volume_tons" value={formData.volume_tons} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white outline-none" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs text-neutral-500 mb-1">Cost (INR/kg)</label>
              <input type="number" name="cost_per_kg_inr" value={formData.cost_per_kg_inr} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white outline-none" />
            </div>
            <div>
              <label className="block text-xs text-neutral-500 mb-1">CBAM Carbon Price ($/Ton)</label>
              <input type="number" name="cbam_price_usd" value={formData.cbam_price_usd} onChange={handleChange} className="w-full bg-neutral-800 rounded px-3 py-2 text-sm text-white outline-none" />
            </div>
          </div>
          <button onClick={handleCalculate} disabled={loading} className="mt-4 w-full py-2.5 rounded-lg bg-red-600 hover:bg-red-700 text-white font-medium flex justify-center items-center">
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Audit Risk & CBAM Tax"}
          </button>
        </div>

        <div>
          {result ? (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-full flex flex-col justify-between">
              <div className="p-4 rounded-xl border" style={{ borderColor: result.geopolitics.risk_color, backgroundColor: `${result.geopolitics.risk_color}15` }}>
                <div className="flex items-center gap-2 mb-2">
                  {result.geopolitics.risk_level === "LOW" ? <ShieldCheck style={{ color: result.geopolitics.risk_color }} /> : <AlertTriangle style={{ color: result.geopolitics.risk_color }} />}
                  <h3 className="font-bold" style={{ color: result.geopolitics.risk_color }}>Geopolitical Risk: {result.geopolitics.risk_level}</h3>
                </div>
                <p className="text-sm text-neutral-300">{result.geopolitics.risk_text.replace(/\*\*/g, '')}</p>
              </div>

              <div className="mt-4 grid grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-neutral-950/50 border border-neutral-800">
                  <p className="text-xs text-neutral-500 mb-1">Total Carbon Footprint</p>
                  <p className="text-xl font-bold text-white">{result.total_carbon_tons.toLocaleString()} <span className="text-sm font-normal text-neutral-500">Tons CO2e</span></p>
                </div>
                <div className="p-4 rounded-xl bg-neutral-950/50 border border-neutral-800">
                  <p className="text-xs text-neutral-500 mb-1">Est. CBAM Carbon Tax</p>
                  <p className="text-xl font-bold text-red-400">${result.annual_cbam_tax_usd.toLocaleString(undefined, { maximumFractionDigits: 0 })} <span className="text-sm font-normal text-neutral-500">/ yr</span></p>
                </div>
              </div>
            </motion.div>
          ) : (
             <div className="h-full flex items-center justify-center border-2 border-dashed border-neutral-800 rounded-xl text-neutral-500 text-sm">
                Run an audit to see ESG & Geopolitical insights
             </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
