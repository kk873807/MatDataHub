"use client";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointer2, Search, Database, ChevronRight, SlidersHorizontal, Info, ExternalLink, Scale, Replace, Layers, FileDown, TrendingUp, ShieldCheck, ArrowRight } from "lucide-react";

interface Step { label: string; cursor: { x: number; y: number }; duration: number; click?: boolean; }

const STEPS: Step[] = [
  // SEARCH FLOW
  { label: "Click the search bar to find materials", cursor: { x: 180, y: 48 }, duration: 1500 },
  { label: "Type a material name, grade, or standard...", cursor: { x: 180, y: 48 }, duration: 1000 },
  { label: "", cursor: { x: 180, y: 48 }, duration: 700 },
  { label: "", cursor: { x: 180, y: 48 }, duration: 700 },
  { label: "Autocomplete suggestions appear as you type", cursor: { x: 180, y: 48 }, duration: 1600 },
  { label: "Click a result to open its full detail view", cursor: { x: 200, y: 130 }, duration: 1200, click: true },
  // DETAIL VIEW - Header
  { label: "Material header: category, name, description & applications", cursor: { x: 240, y: 80 }, duration: 2500 },
  // Action buttons
  { label: "'Add to Compare' — sends this material to the radar chart tool", cursor: { x: 80, y: 165 }, duration: 2000, click: true },
  { label: "'Find Substitution' — finds alternatives via AI optimization", cursor: { x: 180, y: 165 }, duration: 2000, click: true },
  { label: "'Use in Synthesizer' — blend this as matrix or fiber", cursor: { x: 290, y: 165 }, duration: 2000, click: true },
  { label: "'Export PDF' — download the full datasheet", cursor: { x: 390, y: 165 }, duration: 1800, click: true },
  // Market price
  { label: "Market Price — real-time cost per kg with trend indicator", cursor: { x: 130, y: 220 }, duration: 2200 },
  // Standards
  { label: "Standards & Identifiers — ASTM/ISO standard, grade, equivalents", cursor: { x: 350, y: 220 }, duration: 2500 },
  // Data source
  { label: "Data Source — verified from ASTM, ISO, DIN, ICE databases", cursor: { x: 350, y: 285 }, duration: 2200 },
  // Properties
  { label: "Full property table: mechanical, thermal, electrical, economic", cursor: { x: 240, y: 330 }, duration: 2500 },
  // Similar materials
  { label: "Similar Materials — discover related alloys and alternatives", cursor: { x: 240, y: 395 }, duration: 2200 },
  // Historical price
  { label: "Historical Price Tracking — view cost trends over time", cursor: { x: 130, y: 260 }, duration: 2200 },
  // FILTER VIEW
  { label: "Back to search — use category filters: Metal, Polymer, Ceramic, Composite", cursor: { x: 80, y: 435 }, duration: 2000, click: true },
  { label: "Advanced filters: min tensile, max cost, thermal conductivity sliders", cursor: { x: 220, y: 435 }, duration: 2200, click: true },
  { label: "Sort results by name, cost, tensile strength, or density", cursor: { x: 360, y: 435 }, duration: 1800, click: true },
  // Reset
  { label: "", cursor: { x: 460, y: 460 }, duration: 600 },
];

export function SimulatedMaterialsDemo() {
  const [step, setStep] = useState(0);
  const ref = useRef<NodeJS.Timeout | null>(null);
  useEffect(() => {
    let i = 0;
    const go = () => { if (i >= STEPS.length) i = 0; setStep(i); ref.current = setTimeout(() => { i++; go(); }, STEPS[i].duration); };
    go();
    return () => { if (ref.current) clearTimeout(ref.current); };
  }, []);

  const s = STEPS[step];
  const typing = ["", "Go", "Gold", "Gold", "Gold"][Math.min(step, 4)] || "";
  const showSearch = step <= 5;
  const showDetail = step >= 6 && step <= 16;
  const showFilters = step >= 17 && step <= 19;

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 relative overflow-hidden min-h-[480px]">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

      <div className="relative z-10 w-full max-w-lg mx-auto">
        <div className="bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
          <div className="px-5 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center gap-2">
            <Database className="w-4 h-4 text-blue-500" />
            <span className="text-sm font-bold text-slate-900 dark:text-white">Material Database</span>
          </div>

          <div className="p-5">
            <AnimatePresence mode="wait">
              {/* === SEARCH VIEW === */}
              {showSearch && (
                <motion.div key="search" exit={{ opacity: 0, x: -30 }}>
                  <div className={`border rounded-xl p-3 flex items-center gap-2 mb-3 transition-all ${step >= 1 && step <= 5 ? "border-blue-500 ring-2 ring-blue-200 dark:ring-blue-800" : "border-slate-200 dark:border-slate-700"}`}>
                    <Search className="w-4 h-4 text-slate-400 shrink-0" />
                    <span className="text-sm text-slate-700 dark:text-slate-300 font-medium">
                      {step >= 1 && step <= 5 ? <>{typing}<span className="animate-pulse text-blue-500">|</span></> : <span className="text-slate-400">Search 1000+ materials...</span>}
                    </span>
                  </div>
                  <AnimatePresence>
                    {step === 4 && (
                      <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="mb-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl shadow-xl p-1.5 space-y-0.5">
                        <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg text-sm font-semibold text-slate-800 dark:text-white">18K Rose Gold</div>
                        <div className="p-2 rounded-lg text-sm text-slate-600 dark:text-slate-400">24K Pure Gold</div>
                        <div className="p-2 rounded-lg text-sm text-slate-600 dark:text-slate-400">Gold-Copper Alloy</div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                  {step === 5 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-3 rounded-xl border border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-md ring-1 ring-blue-300 flex items-center justify-between">
                      <div>
                        <div className="flex items-center gap-2 mb-0.5"><p className="text-sm font-bold text-slate-900 dark:text-white">18K Rose Gold</p><span className="text-[8px] px-1.5 py-0.5 rounded bg-blue-100 text-blue-600 font-bold">Metal</span></div>
                        <p className="text-[10px] text-slate-500">Gold Alloy · 75% Au + Cu + Ag</p>
                      </div>
                      <ChevronRight className="w-4 h-4 text-blue-500" />
                    </motion.div>
                  )}
                </motion.div>
              )}

              {/* === DETAIL VIEW === */}
              {showDetail && (
                <motion.div key="detail" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} className="space-y-3">
                  {/* Header */}
                  <div className={`transition-all rounded-xl ${step === 6 ? "ring-2 ring-blue-200 shadow-md p-1 -m-1" : ""}`}>
                    <div className="flex items-center gap-1.5 mb-1">
                      <span className="text-[9px] px-1.5 py-0.5 rounded bg-blue-100 dark:bg-blue-900/30 text-blue-600 font-bold">Metal</span>
                      <span className="text-[9px] text-slate-400">•</span>
                      <span className="text-[9px] text-slate-500 font-semibold">Gold Alloy</span>
                    </div>
                    <h3 className="font-bold text-slate-900 dark:text-white text-base mb-1">18K Rose Gold</h3>
                    <p className="text-[10px] text-slate-500 leading-relaxed">75% Gold alloyed with Copper and Silver to produce a red/pink tint and increase scratch resistance. Applications: Jewelry, electronics, dental.</p>
                  </div>

                  {/* Action buttons */}
                  <div className="flex gap-1.5 flex-wrap">
                    {[
                      { label: "Add to Compare", icon: Scale, hl: step === 7 },
                      { label: "Find Substitution", icon: Replace, hl: step === 8 },
                      { label: "Use in Synthesizer", icon: Layers, hl: step === 9 },
                      { label: "Export PDF", icon: FileDown, hl: step === 10 },
                    ].map(btn => (
                      <div key={btn.label} className={`flex items-center gap-1 px-2 py-1.5 rounded-lg border text-[9px] font-semibold transition-all ${btn.hl ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 ring-2 ring-blue-300 shadow-md scale-[1.05] text-blue-700" : "border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400"}`}>
                        <btn.icon className="w-3 h-3" /> {btn.label}
                      </div>
                    ))}
                  </div>

                  {/* Market Price + Standards side by side */}
                  <div className="grid grid-cols-2 gap-2">
                    {/* Market Price */}
                    <div className={`p-3 rounded-xl border transition-all ${step === 11 || step === 16 ? "border-emerald-400 ring-2 ring-emerald-200 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                      <p className="text-[9px] font-bold text-slate-400 uppercase mb-1">Market Price</p>
                      <p className="text-lg font-bold text-slate-900 dark:text-white">&#8377;50,000<span className="text-[10px] text-slate-400 font-normal">/kg</span></p>
                      <p className="text-[9px] text-slate-500">Estimated Baseline</p>
                      <div className={`flex items-center gap-1 mt-1.5 transition-all ${step === 16 ? "ring-1 ring-amber-300 rounded p-0.5" : ""}`}>
                        <TrendingUp className="w-3 h-3 text-emerald-500" />
                        <span className="text-[9px] font-semibold text-emerald-600">Market Trend: +2.3%</span>
                      </div>
                    </div>

                    {/* Standards & Identifiers */}
                    <div className={`p-3 rounded-xl border transition-all ${step === 12 ? "border-violet-400 ring-2 ring-violet-200 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                      <p className="text-[9px] font-bold text-slate-400 uppercase mb-1.5">Standards & Identifiers</p>
                      {[{l:"Standard",v:"—"},{l:"Grade",v:"18K Rose"},{l:"Equivalent",v:"—"}].map(r=>(
                        <div key={r.l} className="flex justify-between mb-1"><span className="text-[9px] text-slate-500">{r.l}</span><span className="text-[9px] font-semibold text-slate-800 dark:text-white">{r.v}</span></div>
                      ))}
                      <div className={`flex items-center gap-1 mt-1.5 pt-1.5 border-t border-slate-100 dark:border-slate-800 transition-all ${step === 13 ? "ring-1 ring-emerald-300 rounded p-0.5 bg-emerald-50 dark:bg-emerald-900/20" : ""}`}>
                        <ShieldCheck className="w-3 h-3 text-emerald-500" />
                        <span className="text-[9px] font-semibold text-emerald-600">Verified Internal Database</span>
                      </div>
                    </div>
                  </div>

                  {/* Properties table */}
                  <div className={`rounded-xl border p-3 transition-all ${step === 14 ? "border-blue-400 ring-2 ring-blue-200 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                    <p className="text-[9px] font-bold text-slate-400 uppercase mb-2">Properties</p>
                    <div className="grid grid-cols-3 gap-1.5">
                      {[{l:"Density",v:"15.5 g/cm3"},{l:"Yield",v:"200 MPa"},{l:"UTS",v:"350 MPa"},{l:"Modulus",v:"80 GPa"},{l:"Thermal K",v:"120 W/mK"},{l:"Hardness",v:"150 HV"}].map(p=>(
                        <div key={p.l} className="bg-slate-50 dark:bg-slate-900 rounded-lg p-1.5">
                          <p className="text-[7px] text-slate-400 uppercase">{p.l}</p>
                          <p className="text-[10px] font-bold text-slate-900 dark:text-white">{p.v}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Similar Materials */}
                  <div className={`rounded-xl border p-3 transition-all ${step === 15 ? "border-amber-400 ring-2 ring-amber-200 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                    <p className="text-[9px] font-bold text-slate-400 uppercase mb-2">Similar Materials</p>
                    <div className="flex gap-2">
                      {["24K Pure Gold", "14K White Gold", "Gold-Copper Alloy"].map(m => (
                        <div key={m} className="flex-1 p-2 bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 text-center">
                          <p className="text-[9px] font-bold text-slate-800 dark:text-white">{m}</p>
                          <ArrowRight className="w-3 h-3 text-slate-400 mx-auto mt-1" />
                        </div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}

              {/* === FILTER VIEW === */}
              {showFilters && (
                <motion.div key="filters" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} className="space-y-3">
                  <div className={`p-3 rounded-xl border transition-all ${step === 17 ? "border-blue-400 ring-2 ring-blue-200 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
                    <p className="text-[10px] font-bold text-slate-500 mb-2 uppercase">Category Filter</p>
                    <div className="flex gap-2">
                      {["Metal","Polymer","Ceramic","Composite"].map((c,i)=>(
                        <span key={c} className={`px-2 py-1 rounded-lg text-[10px] font-semibold border ${step===17 && i===0 ? "bg-blue-500 text-white border-blue-500" : "border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400"}`}>{c}</span>
                      ))}
                    </div>
                  </div>
                  <div className={`p-3 rounded-xl border transition-all ${step === 18 ? "border-emerald-400 ring-2 ring-emerald-200 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
                    <p className="text-[10px] font-bold text-slate-500 mb-2 uppercase flex items-center gap-1"><SlidersHorizontal className="w-3 h-3" /> Advanced Filters</p>
                    {[{l:"Min Tensile Strength",v:"400 MPa"},{l:"Max Cost/kg",v:"$5.00"},{l:"Min Thermal Conductivity",v:"10 W/mK"}].map(f=>(
                      <div key={f.l} className="flex items-center justify-between mb-1.5"><span className="text-[10px] text-slate-500">{f.l}</span><span className="text-[10px] font-bold text-slate-800 dark:text-white bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded">{f.v}</span></div>
                    ))}
                  </div>
                  <div className={`p-3 rounded-xl border text-center transition-all ${step === 19 ? "border-violet-400 ring-2 ring-violet-200 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
                    <p className="text-[10px] font-bold text-slate-500 mb-1">Sort By</p>
                    <p className="text-[10px] text-slate-700 dark:text-slate-300">Name (A-Z) · Cost (low-high) · Tensile (highest) · Density (lightest)</p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>

      {/* Label */}
      <AnimatePresence mode="wait">
        {s.label && (
          <motion.div key={step} initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
            className="absolute bottom-4 left-1/2 -translate-x-1/2 z-40 bg-slate-900 text-white text-xs font-semibold px-4 py-2 rounded-xl shadow-xl max-w-sm text-center pointer-events-none"
          >{s.label}</motion.div>
        )}
      </AnimatePresence>

      {/* Cursor */}
      <motion.div className="absolute z-50 pointer-events-none" animate={{ x: s.cursor.x, y: s.cursor.y }} transition={{ type: "tween", ease: "easeInOut", duration: 0.5 }}>
        <MousePointer2 className="w-7 h-7 text-black fill-white drop-shadow-xl -rotate-12" />
        {s.click && <motion.div key={step} initial={{ scale: 0, opacity: 0.6 }} animate={{ scale: 2.5, opacity: 0 }} transition={{ duration: 0.5 }} className="absolute top-0 left-0 w-4 h-4 rounded-full bg-blue-500/50" />}
      </motion.div>
    </div>
  );
}
