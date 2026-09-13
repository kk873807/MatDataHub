"use client";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointer2, Search, Database, ChevronRight, SlidersHorizontal, Info, ExternalLink } from "lucide-react";

interface Step {
  label: string;
  cursor: { x: number; y: number };
  duration: number;
  click?: boolean;
}

const STEPS: Step[] = [
  // Search flow
  { label: "Click the search bar to find materials", cursor: { x: 180, y: 48 }, duration: 1500 },
  { label: "Type a material name or standard grade...", cursor: { x: 180, y: 48 }, duration: 1200 },
  { label: "", cursor: { x: 180, y: 48 }, duration: 800 },
  { label: "", cursor: { x: 180, y: 48 }, duration: 800 },
  // Autocomplete
  { label: "Autocomplete suggestions appear instantly", cursor: { x: 180, y: 48 }, duration: 1800 },
  // Click result
  { label: "Click a result to view full details", cursor: { x: 200, y: 130 }, duration: 1200, click: true },
  // Detail view
  { label: "Full property card with all verified data", cursor: { x: 280, y: 170 }, duration: 2500 },
  // Filter flow
  { label: "Use category filters: Metal, Polymer, Ceramic, Composite", cursor: { x: 70, y: 305 }, duration: 2000, click: true },
  // Adv filters
  { label: "Set property thresholds: min tensile, max cost, thermal conductivity", cursor: { x: 200, y: 305 }, duration: 2200, click: true },
  // Sort
  { label: "Sort results by name, cost, tensile, or density", cursor: { x: 340, y: 305 }, duration: 1800, click: true },
  // Data source
  { label: "Every material's data source is verified (ASTM, ISO, DIN)", cursor: { x: 300, y: 350 }, duration: 2200 },
  // Export
  { label: "Export datasheets to CSV or share via link", cursor: { x: 430, y: 305 }, duration: 1800, click: true },
  // Reset
  { label: "", cursor: { x: 450, y: 380 }, duration: 600 },
];

export function SimulatedMaterialsDemo() {
  const [step, setStep] = useState(0);
  const ref = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    let i = 0;
    const go = () => {
      if (i >= STEPS.length) i = 0;
      setStep(i);
      ref.current = setTimeout(() => { i++; go(); }, STEPS[i].duration);
    };
    go();
    return () => { if (ref.current) clearTimeout(ref.current); };
  }, []);

  const s = STEPS[step];
  const typing = ["St", "Stee", "Steel", "Steel", "Steel"][Math.min(step, 4)] || "";
  const showSearch = step <= 5;
  const showAutocomplete = step === 4;
  const showDetail = step === 6;
  const showFilters = step >= 7 && step <= 11;

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 relative overflow-hidden min-h-[400px]">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

      <div className="relative z-10 w-full max-w-lg mx-auto">
        {/* Main Card */}
        <div className="bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
          <div className="px-5 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center gap-2">
            <Database className="w-4 h-4 text-blue-500" />
            <span className="text-sm font-bold text-slate-900 dark:text-white">Material Database</span>
          </div>

          <div className="p-5">
            <AnimatePresence mode="wait">
              {(showSearch || showAutocomplete) && !showDetail && (
                <motion.div key="search-view" exit={{ opacity: 0, x: -30 }}>
                  {/* Search bar */}
                  <div className={`border rounded-xl p-3 flex items-center gap-2 mb-3 transition-all ${step >= 1 && step <= 5 ? "border-blue-500 ring-2 ring-blue-200 dark:ring-blue-800" : "border-slate-200 dark:border-slate-700"}`}>
                    <Search className="w-4 h-4 text-slate-400 shrink-0" />
                    <span className="text-sm text-slate-700 dark:text-slate-300 font-medium">
                      {step >= 1 && step <= 5 ? (<>{typing}<span className="animate-pulse text-blue-500">|</span></>) : <span className="text-slate-400">Search 1000+ materials...</span>}
                    </span>
                  </div>

                  {/* Autocomplete dropdown */}
                  <AnimatePresence>
                    {showAutocomplete && (
                      <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="mb-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl shadow-xl p-1.5 space-y-0.5">
                        <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg text-sm font-semibold text-slate-800 dark:text-white">AISI 304 Stainless Steel</div>
                        <div className="p-2 rounded-lg text-sm text-slate-600 dark:text-slate-400">AISI 316L Stainless Steel</div>
                        <div className="p-2 rounded-lg text-sm text-slate-600 dark:text-slate-400">Structural Carbon Steel A36</div>
                      </motion.div>
                    )}
                  </AnimatePresence>

                  {/* Result cards */}
                  {step >= 5 && step <= 5 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-2">
                      <div className={`p-3 rounded-xl border flex items-center justify-between transition-all border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-md ring-1 ring-blue-300`}>
                        <div>
                          <div className="flex items-center gap-2 mb-0.5"><p className="text-sm font-bold text-slate-900 dark:text-white">AISI 304 Stainless Steel</p><span className="text-[8px] px-1.5 py-0.5 rounded bg-blue-100 text-blue-600 font-bold">Metal</span></div>
                          <p className="text-[10px] text-slate-500">8.0 g/cm3 · UTS 515 MPa · $2.80/kg</p>
                        </div>
                        <ChevronRight className="w-4 h-4 text-blue-500" />
                      </div>
                    </motion.div>
                  )}
                </motion.div>
              )}

              {showDetail && (
                <motion.div key="detail-view" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center"><Database className="w-5 h-5 text-blue-600" /></div>
                    <div>
                      <h3 className="font-bold text-slate-900 dark:text-white text-base">AISI 304 Stainless Steel</h3>
                      <p className="text-[10px] text-slate-500">Austenitic · ASTM A240 · DIN 1.4301</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-2 mb-3">
                    {[{l:"Density",v:"8.0 g/cm3"},{l:"Yield",v:"205 MPa"},{l:"UTS",v:"515 MPa"},{l:"Modulus",v:"193 GPa"},{l:"Thermal K",v:"16.2 W/mK"},{l:"Cost",v:"$2.80/kg"}].map(p=>(
                      <div key={p.l} className="bg-slate-50 dark:bg-slate-900 rounded-lg p-2">
                        <p className="text-[8px] text-slate-400 uppercase">{p.l}</p>
                        <p className="text-xs font-bold text-slate-900 dark:text-white">{p.v}</p>
                      </div>
                    ))}
                  </div>
                  <div className="p-2 bg-emerald-50 dark:bg-emerald-900/10 rounded-lg border border-emerald-200 dark:border-emerald-800">
                    <p className="text-[10px] text-emerald-600 font-semibold flex items-center gap-1"><Info className="w-3 h-3" /> Verified Internal Database (ASTM, ISO, DIN)</p>
                  </div>
                </motion.div>
              )}

              {showFilters && (
                <motion.div key="filter-view" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }}>
                  <div className="space-y-3">
                    {/* Category */}
                    <div className={`p-3 rounded-xl border transition-all ${step === 7 ? "border-blue-400 ring-2 ring-blue-200 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
                      <p className="text-[10px] font-bold text-slate-500 mb-2 uppercase">Category Filter</p>
                      <div className="flex gap-2">
                        {["Metal","Polymer","Ceramic","Composite"].map((c,i)=>(
                          <span key={c} className={`px-2 py-1 rounded-lg text-[10px] font-semibold border ${step===7 && i===0 ? "bg-blue-500 text-white border-blue-500" : "border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400"}`}>{c}</span>
                        ))}
                      </div>
                    </div>
                    {/* Adv filters */}
                    <div className={`p-3 rounded-xl border transition-all ${step === 8 ? "border-emerald-400 ring-2 ring-emerald-200 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
                      <p className="text-[10px] font-bold text-slate-500 mb-2 uppercase flex items-center gap-1"><SlidersHorizontal className="w-3 h-3" /> Advanced Filters</p>
                      <div className="space-y-2">
                        {[{l:"Min Tensile Strength",v:"400 MPa"},{l:"Max Cost/kg",v:"$5.00"},{l:"Min Thermal Conductivity",v:"10 W/mK"}].map(f=>(
                          <div key={f.l} className="flex items-center justify-between">
                            <span className="text-[10px] text-slate-500">{f.l}</span>
                            <span className="text-[10px] font-bold text-slate-800 dark:text-white bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded">{f.v}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    {/* Sort + Export */}
                    <div className="flex gap-3">
                      <div className={`flex-1 p-3 rounded-xl border text-center transition-all ${step === 9 ? "border-violet-400 ring-2 ring-violet-200 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
                        <p className="text-[10px] font-bold text-slate-500 mb-1">Sort By</p>
                        <p className="text-[10px] text-slate-700 dark:text-slate-300">Name · Cost · Tensile · Density</p>
                      </div>
                      <div className={`flex-1 p-3 rounded-xl border text-center transition-all ${step === 11 ? "border-amber-400 ring-2 ring-amber-200 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
                        <p className="text-[10px] font-bold text-slate-500 mb-1 flex items-center justify-center gap-1"><ExternalLink className="w-3 h-3" /> Export</p>
                        <p className="text-[10px] text-slate-700 dark:text-slate-300">CSV · Share Link</p>
                      </div>
                    </div>
                    {/* Data source */}
                    <div className={`p-2 rounded-lg text-center transition-all ${step === 10 ? "bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-300 ring-2 ring-emerald-200 shadow-lg" : ""}`}>
                      <p className="text-[10px] text-emerald-600 font-semibold flex items-center justify-center gap-1"><Info className="w-3 h-3" /> All data verified from ASTM, ISO, DIN, ICE DB</p>
                    </div>
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
