"use client";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointer2, Search, Database, ChevronRight, SlidersHorizontal, Info, ExternalLink, Scale, Replace, Layers, FileDown, TrendingUp, ShieldCheck, ArrowRight, LayoutGrid, List, Filter } from "lucide-react";

interface Step { label: string; cursor: { x: number; y: number }; duration: number; click?: boolean; }

const STEPS: Step[] = [
  // === MATERIALS LIST VIEW (steps 0-5) ===
  { label: "Materials page — browse 1000+ verified engineering materials", cursor: { x: 240, y: 60 }, duration: 2000 },
  { label: "Material cards show name, category, key properties & cost at a glance", cursor: { x: 130, y: 150 }, duration: 2200 },
  { label: "Each card shows Density, Tensile Strength, Thermal K & Cost/kg", cursor: { x: 370, y: 150 }, duration: 2200 },
  { label: "Toggle between Grid view and Table view", cursor: { x: 420, y: 60 }, duration: 1800, click: true },
  { label: "Use Category filter: Metal, Polymer, Ceramic, Composite", cursor: { x: 100, y: 95 }, duration: 2000, click: true },
  { label: "Sort by Name, Cost, Tensile Strength, or Density", cursor: { x: 350, y: 95 }, duration: 1800, click: true },

  // === SEARCH FLOW (steps 6-9) ===
  { label: "Search by material name, grade, or standard...", cursor: { x: 200, y: 55 }, duration: 1500, click: true },
  { label: "Typing 'Gold'... autocomplete suggestions appear", cursor: { x: 200, y: 55 }, duration: 1500 },
  { label: "Click a result to open its full detail view", cursor: { x: 200, y: 140 }, duration: 1200, click: true },

  // === DETAIL VIEW (steps 9-18) ===
  { label: "Material header: category badge, name, description & applications", cursor: { x: 240, y: 80 }, duration: 2500 },
  { label: "'Add to Compare' — send to radar chart analysis", cursor: { x: 80, y: 168 }, duration: 1800, click: true },
  { label: "'Find Substitution' — AI multi-objective alternative finder", cursor: { x: 190, y: 168 }, duration: 1800, click: true },
  { label: "'Use in Synthesizer' — blend as matrix or reinforcement", cursor: { x: 300, y: 168 }, duration: 1800, click: true },
  { label: "'Export PDF' — download full material datasheet", cursor: { x: 400, y: 168 }, duration: 1500, click: true },
  { label: "Market Price — real-time cost with trend indicator", cursor: { x: 130, y: 225 }, duration: 2200 },
  { label: "Standards & Identifiers — ASTM/ISO, Grade, Equivalents, Data Source", cursor: { x: 370, y: 225 }, duration: 2500 },
  { label: "Full properties: Density, Yield, UTS, Modulus, Thermal K, Hardness", cursor: { x: 240, y: 305 }, duration: 2500 },

  // === HISTORICAL PRICE CHART (step 17) ===
  { label: "Historical Price Tracking (12M) — SVG area chart showing cost trends over time", cursor: { x: 240, y: 380 }, duration: 3000 },

  // === SIMILAR MATERIALS (step 18) ===
  { label: "Similar Materials — discover related alloys and alternatives", cursor: { x: 240, y: 445 }, duration: 2200 },

  // === ADVANCED FILTERS (steps 19-21) ===
  { label: "Advanced Filters — set min tensile, max cost, min thermal conductivity", cursor: { x: 130, y: 480 }, duration: 2200, click: true },
  { label: "Export material datasheet to CSV or share via link", cursor: { x: 370, y: 480 }, duration: 1800, click: true },

  // Reset
  { label: "", cursor: { x: 460, y: 500 }, duration: 600 },
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
  const showList = step <= 5;
  const showSearch = step >= 6 && step <= 8;
  const showDetail = step >= 9 && step <= 20;

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 relative overflow-hidden min-h-[530px]">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

      <div className="relative z-10 w-full max-w-lg mx-auto">
        <div className="bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
          <div className="px-5 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center gap-2">
            <Database className="w-4 h-4 text-blue-500" />
            <span className="text-sm font-bold text-slate-900 dark:text-white">Material Database</span>
          </div>

          <div className="p-5">
            <AnimatePresence mode="wait">
              {/* === MATERIALS LIST VIEW === */}
              {showList && (
                <motion.div key="list" exit={{ opacity: 0, x: -30 }} className="space-y-3">
                  {/* Search + controls */}
                  <div className="flex gap-2 items-center">
                    <div className="flex-1 border rounded-xl p-2.5 flex items-center gap-2 border-slate-200 dark:border-slate-700">
                      <Search className="w-3.5 h-3.5 text-slate-400" />
                      <span className="text-[10px] text-slate-400">Search materials...</span>
                    </div>
                    <div className={`flex gap-1 transition-all ${step === 3 ? "ring-2 ring-blue-300 rounded-lg p-0.5" : ""}`}>
                      <div className="p-1.5 rounded bg-blue-100 dark:bg-blue-900/30"><LayoutGrid className="w-3 h-3 text-blue-600" /></div>
                      <div className="p-1.5 rounded bg-slate-100 dark:bg-slate-800"><List className="w-3 h-3 text-slate-400" /></div>
                    </div>
                  </div>

                  {/* Filters row */}
                  <div className="flex gap-2">
                    <div className={`flex gap-1.5 transition-all ${step === 4 ? "ring-2 ring-blue-300 rounded-lg p-0.5" : ""}`}>
                      {["All","Metal","Polymer","Ceramic"].map((c,i)=>(
                        <span key={c} className={`px-2 py-1 rounded-lg text-[9px] font-semibold border ${i===0?"bg-blue-500 text-white border-blue-500":"border-slate-200 dark:border-slate-700 text-slate-500"}`}>{c}</span>
                      ))}
                    </div>
                    <div className={`ml-auto px-2 py-1 rounded-lg border text-[9px] font-semibold flex items-center gap-1 transition-all ${step === 5 ? "ring-2 ring-violet-300 border-violet-400" : "border-slate-200 dark:border-slate-700 text-slate-500"}`}>
                      Sort ▾
                    </div>
                  </div>

                  {/* Material cards grid */}
                  <div className="grid grid-cols-2 gap-2">
                    {[
                      { n: "AISI 304 Stainless", cat: "Metal", d: "8.0", t: "515", k: "16.2", c: "$2.80" },
                      { n: "Al 7075-T6", cat: "Metal", d: "2.81", t: "572", k: "130", c: "$3.20" },
                      { n: "Ti-6Al-4V Grade 5", cat: "Metal", d: "4.43", t: "950", k: "6.7", c: "$25.0" },
                      { n: "PEEK", cat: "Polymer", d: "1.30", t: "100", k: "0.25", c: "$90.0" },
                    ].map((m, i) => (
                      <div key={i} className={`p-2.5 rounded-xl border transition-all ${(step === 1 && i === 0) || (step === 2 && i === 1) ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-md ring-1 ring-blue-300 scale-[1.03]" : "border-slate-200 dark:border-slate-800"}`}>
                        <div className="flex items-center gap-1.5 mb-1.5">
                          <p className="text-[10px] font-bold text-slate-900 dark:text-white leading-tight">{m.n}</p>
                          <span className={`text-[7px] px-1 py-0.5 rounded font-bold shrink-0 ${m.cat === "Metal" ? "bg-blue-100 text-blue-600" : "bg-green-100 text-green-600"}`}>{m.cat}</span>
                        </div>
                        <div className="grid grid-cols-2 gap-1">
                          <div><p className="text-[7px] text-slate-400">Density</p><p className="text-[9px] font-bold text-slate-700 dark:text-slate-300">{m.d}</p></div>
                          <div><p className="text-[7px] text-slate-400">UTS</p><p className="text-[9px] font-bold text-slate-700 dark:text-slate-300">{m.t} MPa</p></div>
                          <div><p className="text-[7px] text-slate-400">Thermal K</p><p className="text-[9px] font-bold text-slate-700 dark:text-slate-300">{m.k}</p></div>
                          <div><p className="text-[7px] text-slate-400">Cost</p><p className="text-[9px] font-bold text-emerald-600">{m.c}/kg</p></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </motion.div>
              )}

              {/* === SEARCH VIEW === */}
              {showSearch && (
                <motion.div key="search" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }}>
                  <div className={`border rounded-xl p-3 flex items-center gap-2 mb-3 border-blue-500 ring-2 ring-blue-200 dark:ring-blue-800`}>
                    <Search className="w-4 h-4 text-slate-400 shrink-0" />
                    <span className="text-sm text-slate-700 dark:text-slate-300 font-medium">{step >= 7 ? <>Gold<span className="animate-pulse text-blue-500">|</span></> : <span className="text-slate-400">Search...</span>}</span>
                  </div>
                  {step >= 7 && (
                    <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} className="mb-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl shadow-xl p-1.5 space-y-0.5">
                      <div className={`p-2 rounded-lg text-sm font-semibold ${step === 8 ? "bg-blue-50 dark:bg-blue-900/20 text-slate-800 dark:text-white" : "text-slate-600 dark:text-slate-400"}`}>18K Rose Gold</div>
                      <div className="p-2 rounded-lg text-sm text-slate-600 dark:text-slate-400">24K Pure Gold</div>
                      <div className="p-2 rounded-lg text-sm text-slate-600 dark:text-slate-400">Gold-Copper Alloy</div>
                    </motion.div>
                  )}
                </motion.div>
              )}

              {/* === DETAIL VIEW === */}
              {showDetail && (
                <motion.div key="detail" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} className="space-y-3">
                  {/* Header */}
                  <div className={`transition-all rounded-xl ${step === 9 ? "ring-2 ring-blue-200 shadow-md p-1 -m-1" : ""}`}>
                    <div className="flex items-center gap-1.5 mb-1">
                      <span className="text-[9px] px-1.5 py-0.5 rounded bg-blue-100 dark:bg-blue-900/30 text-blue-600 font-bold">Metal</span>
                      <span className="text-[9px] text-slate-400">•</span>
                      <span className="text-[9px] text-slate-500 font-semibold">Gold Alloy</span>
                    </div>
                    <h3 className="font-bold text-slate-900 dark:text-white text-base mb-1">18K Rose Gold</h3>
                    <p className="text-[10px] text-slate-500 leading-relaxed">75% Gold alloyed with Copper and Silver. Applications: Jewelry, electronics, dental, decorative coatings.</p>
                  </div>

                  {/* Action buttons */}
                  <div className="flex gap-1.5 flex-wrap">
                    {[
                      { label: "Add to Compare", icon: Scale, hl: step === 10 },
                      { label: "Find Substitution", icon: Replace, hl: step === 11 },
                      { label: "Use in Synthesizer", icon: Layers, hl: step === 12 },
                      { label: "Export PDF", icon: FileDown, hl: step === 13 },
                    ].map(btn => (
                      <div key={btn.label} className={`flex items-center gap-1 px-2 py-1.5 rounded-lg border text-[9px] font-semibold transition-all ${btn.hl ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 ring-2 ring-blue-300 shadow-md scale-[1.05] text-blue-700" : "border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400"}`}>
                        <btn.icon className="w-3 h-3" /> {btn.label}
                      </div>
                    ))}
                  </div>

                  {/* Market Price + Standards */}
                  <div className="grid grid-cols-2 gap-2">
                    <div className={`p-3 rounded-xl border transition-all ${step === 14 ? "border-emerald-400 ring-2 ring-emerald-200 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                      <p className="text-[9px] font-bold text-slate-400 uppercase mb-1">Market Price</p>
                      <p className="text-lg font-bold text-slate-900 dark:text-white">&#8377;50,000<span className="text-[10px] text-slate-400 font-normal">/kg</span></p>
                      <p className="text-[9px] text-slate-500">Estimated Baseline</p>
                      <div className="flex items-center gap-1 mt-1.5">
                        <TrendingUp className="w-3 h-3 text-emerald-500" />
                        <span className="text-[9px] font-semibold text-emerald-600">Market Trend</span>
                      </div>
                    </div>
                    <div className={`p-3 rounded-xl border transition-all ${step === 15 ? "border-violet-400 ring-2 ring-violet-200 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                      <p className="text-[9px] font-bold text-slate-400 uppercase mb-1.5">Standards & Identifiers</p>
                      {[{l:"Standard",v:"—"},{l:"Grade",v:"18K Rose"},{l:"Equivalent",v:"—"}].map(r=>(
                        <div key={r.l} className="flex justify-between mb-1"><span className="text-[9px] text-slate-500">{r.l}</span><span className="text-[9px] font-semibold text-slate-800 dark:text-white">{r.v}</span></div>
                      ))}
                      <div className="flex items-center gap-1 mt-1 pt-1 border-t border-slate-100 dark:border-slate-800">
                        <ShieldCheck className="w-3 h-3 text-emerald-500" />
                        <span className="text-[8px] font-semibold text-emerald-600">Verified Internal Database</span>
                      </div>
                    </div>
                  </div>

                  {/* Properties */}
                  <div className={`rounded-xl border p-3 transition-all ${step === 16 ? "border-blue-400 ring-2 ring-blue-200 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
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

                  {/* Historical Price Chart */}
                  <div className={`rounded-xl border p-3 transition-all ${step === 17 ? "border-emerald-400 ring-2 ring-emerald-200 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
                    <p className="text-[9px] font-bold text-slate-500 uppercase mb-1 flex items-center gap-1">
                      <TrendingUp className="w-3 h-3 text-emerald-500" /> Historical Price Tracking (12M)
                    </p>
                    <p className="text-[7px] text-slate-400 mb-2 flex items-start gap-1">
                      <Info className="w-2.5 h-2.5 mt-0.5 shrink-0" /> Macroeconomic proxy indexing for trend analysis. Consult supplier for exact pricing.
                    </p>
                    <div className="relative h-16">
                      <svg viewBox="0 0 200 50" className="w-full h-full" preserveAspectRatio="none">
                        <defs>
                          <linearGradient id="priceGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor="#10b981" stopOpacity="0.3"/>
                            <stop offset="100%" stopColor="#10b981" stopOpacity="0.02"/>
                          </linearGradient>
                        </defs>
                        {/* Area fill */}
                        <path d="M0,35 L20,32 L40,38 L60,30 L80,28 L100,25 L120,22 L140,20 L160,18 L180,15 L200,12 L200,50 L0,50 Z" fill="url(#priceGrad)" />
                        {/* Line */}
                        <path d="M0,35 L20,32 L40,38 L60,30 L80,28 L100,25 L120,22 L140,20 L160,18 L180,15 L200,12" fill="none" stroke="#10b981" strokeWidth="1.5" strokeLinecap="round"/>
                        {/* Data points */}
                        {[[0,35],[40,38],[80,28],[120,22],[160,18],[200,12]].map(([cx,cy],i) => (
                          <circle key={i} cx={cx} cy={cy} r="2" fill="#10b981" stroke="white" strokeWidth="1"/>
                        ))}
                      </svg>
                      {/* Y-axis labels */}
                      <span className="absolute top-0 left-0 text-[7px] text-slate-400">&#8377;52k</span>
                      <span className="absolute bottom-0 left-0 text-[7px] text-slate-400">&#8377;48k</span>
                      {/* X-axis */}
                      <div className="absolute bottom-[-12px] left-0 right-0 flex justify-between">
                        {["Jan","Mar","May","Jul","Sep","Nov"].map(m => (
                          <span key={m} className="text-[6px] text-slate-400">{m}</span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Similar Materials */}
                  <div className={`rounded-xl border p-3 transition-all ${step === 18 ? "border-amber-400 ring-2 ring-amber-200 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
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

                  {/* Advanced filters + Export */}
                  <div className="flex gap-2">
                    <div className={`flex-1 p-2.5 rounded-xl border text-center transition-all ${step === 19 ? "border-blue-400 ring-2 ring-blue-200 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                      <SlidersHorizontal className="w-3 h-3 mx-auto mb-0.5 text-blue-500" />
                      <p className="text-[9px] font-bold text-slate-700 dark:text-slate-300">Advanced Filters</p>
                      <p className="text-[7px] text-slate-400">Tensile, Cost, Thermal</p>
                    </div>
                    <div className={`flex-1 p-2.5 rounded-xl border text-center transition-all ${step === 20 ? "border-amber-400 ring-2 ring-amber-200 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                      <ExternalLink className="w-3 h-3 mx-auto mb-0.5 text-amber-500" />
                      <p className="text-[9px] font-bold text-slate-700 dark:text-slate-300">Export & Share</p>
                      <p className="text-[7px] text-slate-400">CSV, Share Link</p>
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
