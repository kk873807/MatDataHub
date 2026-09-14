"use client";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search, Database, SlidersHorizontal, ExternalLink, Scale,
  Replace, Layers, FileDown, TrendingUp, ShieldCheck, ArrowRight,
  LayoutGrid, List, Info, Beaker, SearchCode
} from "lucide-react";
import { DemoEngine, type DemoStep, type DemoPhase } from "./DemoEngine";

/* ------------------------------------------------------------------ */
/*  Phases                                                             */
/* ------------------------------------------------------------------ */

const PHASES: DemoPhase[] = [
  { name: "Materials List", color: "blue" },
  { name: "Search", color: "violet" },
  { name: "Detail View", color: "emerald" },
];

/* ------------------------------------------------------------------ */
/*  Steps                                                              */
/* ------------------------------------------------------------------ */

const STEPS: DemoStep[] = [
  // === MATERIALS LIST VIEW === (phase 0)
  { label: "Materials page — browse 1000+ verified engineering materials", cursor: { x: 240, y: 60 }, duration: 4000, scroll: 0, phaseIndex: 0 },
  { label: "Material cards show name, category, key properties & est. cost", cursor: { x: 130, y: 150 }, duration: 4500, scroll: 0, phaseIndex: 0 },
  { label: "Each card shows Yield Strength, Density, and Est. Cost/kg", cursor: { x: 370, y: 150 }, duration: 5000, scroll: 0, phaseIndex: 0 },
  { label: "Use Category filter: Metals, Polymers, Ceramics, Composites", cursor: { x: 100, y: 95 }, duration: 4000, click: true, scroll: 0, phaseIndex: 0 },
  { label: "Sort results using the dropdown (e.g., Name, Cost, Tensile, Density)", cursor: { x: 350, y: 95 }, duration: 4000, click: true, scroll: 0, phaseIndex: 0 },

  // === SEARCH FLOW === (phase 1)
  { label: "Search by material name, grade, or standard...", cursor: { x: 200, y: 55 }, duration: 3000, click: true, scroll: 0, phaseIndex: 1 },
  { label: "Typing 'Gold'... autocomplete suggestions appear", cursor: { x: 200, y: 55 }, duration: 3000, scroll: 0, phaseIndex: 1 },
  { label: "Click a result to open its full detail view", cursor: { x: 200, y: 140 }, duration: 2500, click: true, scroll: 0, phaseIndex: 1 },

  // === DETAIL VIEW === (phase 2)
  { label: "Material header: category badge, name, description & applications", cursor: { x: 240, y: 80 }, duration: 5000, scroll: 0, phaseIndex: 2 },
  { label: "'Add to Compare' — send to radar chart analysis", cursor: { x: 80, y: 168 }, duration: 3500, click: true, scroll: 0, phaseIndex: 2 },
  { label: "'Find Substitution' — AI multi-objective alternative finder", cursor: { x: 190, y: 168 }, duration: 4000, click: true, scroll: 0, phaseIndex: 2 },
  { label: "'Use in Synthesizer' — blend as matrix or reinforcement", cursor: { x: 300, y: 168 }, duration: 4000, click: true, scroll: 0, phaseIndex: 2 },
  { label: "'Export PDF' — download full material datasheet", cursor: { x: 400, y: 168 }, duration: 3000, click: true, scroll: 0, phaseIndex: 2 },
  { label: "Market Price — estimated baseline cost with trend indicator", cursor: { x: 130, y: 225 }, duration: 4500, scroll: -80, phaseIndex: 2 },
  { label: "Standards & Identifiers — Standard, Grade, Equivalent, Data Source", cursor: { x: 370, y: 225 }, duration: 5500, scroll: -80, phaseIndex: 2 },
  { label: "Full properties: Yield, Tensile, Modulus, Density, Hardness, etc.", cursor: { x: 240, y: 305 }, duration: 5500, scroll: -160, phaseIndex: 2 },
  { label: "Historical Price Tracking (12M) — SVG area chart showing trends", cursor: { x: 240, y: 380 }, duration: 6000, scroll: -320, phaseIndex: 2 },
  { label: "Similar Materials — discover related alloys and alternatives", cursor: { x: 240, y: 445 }, duration: 4500, scroll: -450, phaseIndex: 2 },
  // Reset
  { label: "", cursor: { x: 460, y: 500 }, duration: 1000, scroll: 0, phaseIndex: 2 },
];

/* ------------------------------------------------------------------ */
/*  Highlight helper                                                   */
/* ------------------------------------------------------------------ */

const hl = (active: boolean) =>
  active
    ? "ring-2 ring-blue-400/50 shadow-[0_0_16px_rgba(59,130,246,0.12)] border-blue-400/60 bg-blue-50/60 dark:bg-blue-900/15 scale-[1.02]"
    : "";

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export function SimulatedMaterialsDemo() {
  return (
    <DemoEngine
      steps={STEPS}
      phases={PHASES}
      header={
        <>
          <Database className="w-4 h-4 text-blue-500" />
          <span className="text-xs font-bold text-slate-700 dark:text-slate-200">
            Material Database
          </span>
        </>
      }
    >
      {(step) => <MaterialsContent step={step} />}
    </DemoEngine>
  );
}

/* ------------------------------------------------------------------ */
/*  Inner content                                                      */
/* ------------------------------------------------------------------ */

function MaterialsContent({ step }: { step: number }) {
  const showList = step <= 4;
  const showSearch = step >= 5 && step <= 7;
  const showDetail = step >= 8;

  return (
    <div className="p-5 w-full min-h-full relative">
      <AnimatePresence mode="wait">
        {/* === MATERIALS LIST VIEW === */}
        {showList && (
          <motion.div key="list" exit={{ opacity: 0, x: -30 }} className="space-y-3">
            <div className="flex gap-2 items-center">
              <div className="flex-1 border rounded-xl p-2.5 flex items-center gap-2 border-slate-200 dark:border-slate-700">
                <Search className="w-3.5 h-3.5 text-slate-400" />
                <span className="text-[10px] text-slate-400">Search materials (e.g. Aluminum 6061)...</span>
              </div>
              <div className="flex gap-1 transition-all duration-300 rounded-lg p-0.5 border border-slate-200 dark:border-slate-700 text-[10px] px-2 text-slate-500">
                <SlidersHorizontal className="w-3 h-3" /> Filters
              </div>
            </div>

            <div className="flex gap-2 justify-between items-center">
              <div className={`flex gap-1.5 transition-all duration-300 rounded-lg p-0.5 ${step === 3 ? "ring-2 ring-blue-400/60 shadow-[0_0_20px_rgba(59,130,246,0.15)] bg-blue-50 dark:bg-blue-900/20" : ""}`}>
                <span className="px-2 py-1 rounded-lg text-[9px] font-semibold border border-slate-200 dark:border-slate-700 text-slate-500 bg-white dark:bg-slate-900">Category ▾</span>
              </div>
              <div className={`px-2 py-1 rounded-lg border text-[9px] font-semibold flex items-center gap-1 transition-all duration-300 ${step === 4 ? "ring-2 ring-violet-400/60 shadow-[0_0_20px_rgba(139,92,246,0.15)] border-violet-400 bg-violet-50 dark:bg-violet-900/20 text-violet-700" : "border-slate-200 dark:border-slate-700 text-slate-500 bg-white dark:bg-slate-900"}`}>
                Name (A-Z) ▾
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2">
              {[
                { n: "AISI 304 Stainless", cat: "Metal", d: "8.0", y: "215", c: "2.80" },
                { n: "Al 7075-T6", cat: "Metal", d: "2.81", y: "503", c: "3.20" },
                { n: "Ti-6Al-4V Grade 5", cat: "Metal", d: "4.43", y: "880", c: "25.0" },
                { n: "PEEK", cat: "Polymer", d: "1.30", y: "100", c: "90.0" },
              ].map((m, i) => (
                <div key={i} className={`p-2.5 rounded-xl border bg-white dark:bg-slate-900 transition-all duration-300 ${(step === 1 && i === 0) || (step === 2 && i === 1) ? hl(true) : "border-slate-200 dark:border-slate-800"}`}>
                  <div className="flex items-center gap-1.5 mb-2">
                    <p className="text-[10px] font-bold text-slate-900 dark:text-white leading-tight truncate">{m.n}</p>
                  </div>
                  <div className="mb-2">
                    <span className={`text-[7px] px-1.5 py-0.5 rounded-full font-bold shrink-0 border ${m.cat === "Metal" ? "bg-blue-100/50 text-blue-600 border-blue-200" : "bg-purple-100/50 text-purple-600 border-purple-200"}`}>{m.cat}</span>
                  </div>
                  <div className="space-y-1.5">
                    <div className="flex justify-between items-center bg-slate-50 dark:bg-slate-950 p-1 rounded">
                      <span className="text-[7px] text-slate-400 uppercase font-bold">Yield</span>
                      <span className="text-[8px] font-bold text-slate-700 dark:text-slate-300">{m.y} <span className="font-normal text-[7px] text-slate-400">MPa</span></span>
                    </div>
                    <div className="flex justify-between items-center bg-slate-50 dark:bg-slate-950 p-1 rounded">
                      <span className="text-[7px] text-slate-400 uppercase font-bold">Density</span>
                      <span className="text-[8px] font-bold text-slate-700 dark:text-slate-300">{m.d} <span className="font-normal text-[7px] text-slate-400">g/cm³</span></span>
                    </div>
                    <div className="flex justify-between items-center mt-2 pt-1 border-t border-slate-100 dark:border-slate-800">
                      <span className="text-[7px] text-slate-400 uppercase font-bold">Est. Cost</span>
                      <span className="text-[9px] font-bold text-emerald-600">₹{m.c}<span className="font-normal text-[7px]">/kg</span></span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {/* === SEARCH VIEW === */}
        {showSearch && (
          <motion.div key="search" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }}>
            <div className="border rounded-xl p-3 flex items-center gap-2 mb-3 border-emerald-500 ring-2 ring-emerald-200 dark:ring-emerald-900 bg-white dark:bg-slate-900">
              <Search className="w-4 h-4 text-slate-400 shrink-0" />
              <span className="text-sm text-slate-700 dark:text-slate-300 font-medium">{step >= 6 ? <>Gold<span className="animate-pulse text-emerald-500">|</span></> : <span className="text-slate-400">Search materials (e.g. Aluminum 6061)...</span>}</span>
            </div>
            {step >= 6 && (
              <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} className="mb-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-xl overflow-hidden">
                <div className={`px-4 py-3 text-sm flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 ${step === 7 ? "bg-slate-100 dark:bg-slate-800" : ""}`}>
                  <Search className="w-3.5 h-3.5 text-emerald-500" />
                  <div>
                    <p className="font-semibold text-slate-900 dark:text-white leading-tight">18K Rose Gold</p>
                    <p className="text-[10px] text-slate-500">Metal • 18K Rose</p>
                  </div>
                </div>
                <div className="px-4 py-3 text-sm flex items-center gap-3 border-b border-slate-100 dark:border-slate-800">
                  <Search className="w-3.5 h-3.5 text-emerald-500" />
                  <div>
                    <p className="font-semibold text-slate-900 dark:text-white leading-tight">24K Pure Gold</p>
                    <p className="text-[10px] text-slate-500">Metal</p>
                  </div>
                </div>
              </motion.div>
            )}
          </motion.div>
        )}

        {/* === DETAIL VIEW === */}
        {showDetail && (
          <motion.div key="detail" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} className="space-y-3 pb-8">
            {/* Header */}
            <div className={`bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-3 rounded-xl transition-all duration-300 ${step === 8 ? "ring-2 ring-blue-400/60 shadow-[0_0_24px_rgba(59,130,246,0.15)]" : ""}`}>
              <div className="inline-block px-1.5 py-0.5 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 text-[8px] font-bold rounded-full mb-1 border border-emerald-200 dark:border-emerald-800/50 uppercase">
                Metal • 18K Rose
              </div>
              <h3 className="font-bold text-slate-900 dark:text-white text-base mb-1">18K Rose Gold</h3>
              <p className="text-[10px] text-slate-500 leading-relaxed">75% Gold alloyed with Copper and Silver. Applications: Jewelry, electronics, dental, decorative coatings.</p>
              
              {/* Action buttons */}
              <div className="flex gap-1.5 flex-wrap mt-3">
                {[
                  { label: "Add to Compare", icon: Scale, hl: step === 9, bg: "bg-blue-600", text: "text-white" },
                  { label: "Find Substitution", icon: Replace, hl: step === 10, bg: "bg-purple-600", text: "text-white" },
                  { label: "Use in Synthesizer", icon: Layers, hl: step === 11, bg: "bg-cyan-600", text: "text-white" },
                  { label: "Export PDF", icon: FileDown, hl: step === 12, bg: "bg-slate-100 dark:bg-slate-800", text: "text-slate-900 dark:text-white" },
                ].map(btn => (
                  <div key={btn.label} className={`flex items-center gap-1 px-2 py-1.5 rounded-lg text-[9px] font-semibold transition-all duration-300 ${btn.bg} ${btn.text} ${btn.hl ? "ring-2 ring-offset-1 ring-blue-400 shadow-[0_0_16px_rgba(59,130,246,0.3)] scale-[1.05]" : ""}`}>
                    <btn.icon className="w-3 h-3" /> {btn.label}
                  </div>
                ))}
              </div>
            </div>

            {/* Market Price + Standards */}
            <div className="grid grid-cols-2 gap-2">
              <div className={`p-3 rounded-xl border transition-all duration-300 ${step === 13 ? "border-emerald-400 ring-2 ring-emerald-400/60 shadow-[0_0_16px_rgba(16,185,129,0.15)] bg-slate-50 dark:bg-slate-950" : "border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950"}`}>
                <p className="text-[9px] font-bold text-slate-500 uppercase mb-1">Market Price</p>
                <p className="text-lg font-bold text-emerald-600 dark:text-emerald-400">&#8377;50,000<span className="text-[10px] text-slate-500 font-normal">/kg</span></p>
                <p className="text-[8px] text-slate-500 uppercase font-bold mb-1">Estimated Baseline</p>
                <div className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-emerald-100 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-500">
                  <TrendingUp className="w-3 h-3" />
                  <span className="text-[8px] font-semibold">Market Trend</span>
                </div>
              </div>
              <div className={`p-3 rounded-xl border transition-all duration-300 ${step === 14 ? "border-violet-400 ring-2 ring-violet-400/60 shadow-[0_0_16px_rgba(139,92,246,0.15)] bg-white dark:bg-slate-900" : "border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900"}`}>
                <p className="text-[9px] font-bold text-slate-800 dark:text-white mb-2 pb-1 border-b border-slate-200 dark:border-slate-800">Standards & Identifiers</p>
                {[{l:"Standard",v:"—"},{l:"Grade",v:"18K Rose"},{l:"Equivalent",v:"—"}].map(r => (
                  <div key={r.l} className="flex justify-between mb-1"><span className="text-[9px] text-slate-500">{r.l}</span><span className="text-[9px] font-semibold text-slate-800 dark:text-white">{r.v}</span></div>
                ))}
                <div className="mt-1.5 pt-1.5 border-t border-slate-100 dark:border-slate-800">
                  <span className="text-[8px] text-slate-500 block">Data Source</span>
                  <span className="text-[9px] font-medium text-emerald-600 border-b border-dashed border-emerald-400/50 inline-block">Verified Internal Database</span>
                </div>
              </div>
            </div>

            {/* Properties */}
            <div className={`rounded-xl border p-3 transition-all duration-300 ${step === 15 ? "border-blue-400 ring-2 ring-blue-400/60 shadow-[0_0_16px_rgba(59,130,246,0.15)] bg-white dark:bg-slate-900" : "border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900"}`}>
              <p className="text-[10px] font-bold text-slate-800 dark:text-white mb-2 flex items-center gap-1.5"><Beaker className="w-3.5 h-3.5 text-blue-600" /> Mechanical Properties</p>
              <div className="grid grid-cols-3 gap-2">
                {[{l:"Yield Strength",v:"200", u:"MPa"},{l:"Tensile Strength",v:"350", u:"MPa"},{l:"Elastic Modulus",v:"80", u:"GPa"},{l:"Density",v:"15.5", u:"g/cm³"},{l:"Hardness",v:"150", u:"HV"},{l:"Max Temp",v:"900", u:"°C"}].map(p => (
                  <div key={p.l} className="bg-slate-50 dark:bg-slate-950 rounded-lg p-2 border border-slate-200 dark:border-slate-800">
                    <p className="text-[7px] text-slate-500">{p.l}</p>
                    <p className="text-[10px] font-bold text-slate-900 dark:text-white">{p.v} <span className="text-[7px] text-slate-500 font-normal">{p.u}</span></p>
                  </div>
                ))}
              </div>
            </div>

            {/* Historical Price Chart */}
            <div className={`rounded-xl border p-3 transition-all duration-300 ${step === 16 ? "border-emerald-400 ring-2 ring-emerald-400/60 shadow-[0_0_16px_rgba(16,185,129,0.15)] bg-white dark:bg-slate-900" : "border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900"}`}>
              <p className="text-[10px] font-bold text-slate-800 dark:text-white mb-1 flex items-center gap-1.5">
                <TrendingUp className="w-3.5 h-3.5 text-emerald-600" /> Historical Price Tracking (12M)
              </p>
              <p className="text-[7px] text-slate-500 mb-3 leading-relaxed flex gap-1">
                <Info className="w-2.5 h-2.5 shrink-0" /> Proxy indexing for trend analysis. Not a live spot-price.
              </p>
              <div className="relative h-20 border-t border-slate-200 dark:border-slate-800 pt-3">
                <svg viewBox="0 0 200 50" className="w-full h-full" preserveAspectRatio="none">
                  <defs>
                    <linearGradient id="priceGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#10b981" stopOpacity="0.4"/>
                      <stop offset="100%" stopColor="#10b981" stopOpacity="0.0"/>
                    </linearGradient>
                  </defs>
                  <path d="M0,35 L20,32 L40,38 L60,30 L80,28 L100,25 L120,22 L140,20 L160,18 L180,15 L200,12 L200,50 L0,50 Z" fill="url(#priceGrad)" />
                  <path d="M0,35 L20,32 L40,38 L60,30 L80,28 L100,25 L120,22 L140,20 L160,18 L180,15 L200,12" fill="none" stroke="#34d399" strokeWidth="2" strokeLinecap="round"/>
                </svg>
                <span className="absolute top-2 left-0 text-[7px] text-slate-400">&#8377;52k</span>
                <span className="absolute bottom-4 left-0 text-[7px] text-slate-400">&#8377;48k</span>
                <div className="absolute bottom-[-4px] left-4 right-4 flex justify-between">
                  {["Jan","Mar","May","Jul","Sep","Nov"].map(m => (
                    <span key={m} className="text-[6px] text-slate-400">{m}</span>
                  ))}
                </div>
              </div>
            </div>

            {/* Similar Materials */}
            <div className={`rounded-xl border p-3 transition-all duration-300 ${step === 17 ? "border-purple-400 ring-2 ring-purple-400/60 shadow-[0_0_16px_rgba(168,85,247,0.15)] bg-white dark:bg-slate-900" : "border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900"}`}>
              <p className="text-[10px] font-bold text-slate-800 dark:text-white mb-2 flex items-center gap-1.5"><SearchCode className="w-3.5 h-3.5 text-purple-600" /> Find Similar Materials</p>
              <div className="space-y-1.5">
                {["24K Pure Gold", "14K White Gold"].map(m => (
                  <div key={m} className="p-2 bg-slate-50 dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 flex justify-between items-center">
                    <p className="text-[9px] font-semibold text-slate-800 dark:text-white">{m}</p>
                    <span className="text-[8px] text-purple-600">View →</span>
                  </div>
                ))}
              </div>
            </div>

          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
