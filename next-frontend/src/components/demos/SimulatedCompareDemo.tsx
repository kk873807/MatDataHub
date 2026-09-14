"use client";
import { motion, AnimatePresence } from "framer-motion";
import {
  Scale, Replace, Factory, Layers, Search, BarChart3,
  Info, Download,
} from "lucide-react";
import { DemoEngine, type DemoStep, type DemoPhase } from "./DemoEngine";

/* ------------------------------------------------------------------ */
/*  Phases                                                             */
/* ------------------------------------------------------------------ */

const PHASES: DemoPhase[] = [
  { name: "Compare", color: "blue" },
  { name: "AI Substitution", color: "purple" },
  { name: "CBAM & ESG", color: "amber" },
  { name: "Synthesizer", color: "cyan" },
];

/* ------------------------------------------------------------------ */
/*  Steps                                                              */
/* ------------------------------------------------------------------ */

const STEPS: DemoStep[] = [
  // ===== COMPARE ===== (phase 0) — steps 0–7
  { label: "Analytics Hub — 4 enterprise tools: Compare, Substitution, CBAM, Synthesizer", cursor: { x: 240, y: 90 }, duration: 4500, phaseIndex: 0 },
  { label: "Open Side-by-Side Compare tool", cursor: { x: 120, y: 72 }, duration: 2500, click: true, phaseIndex: 0 },
  { label: "Search and add first material: Ti-6Al-4V Grade 5", cursor: { x: 180, y: 155 }, duration: 3500, click: true, phaseIndex: 0 },
  { label: "Search and add second material: Al 7075-T6", cursor: { x: 350, y: 155 }, duration: 3000, click: true, phaseIndex: 0 },
  { label: "Property Fingerprint — radar chart overlays all properties", cursor: { x: 120, y: 280 }, duration: 5000, scroll: -40, phaseIndex: 0 },
  { label: "Direct Comparison Matrix — property-by-property table with best values in green", cursor: { x: 360, y: 260 }, duration: 5500, scroll: -40, phaseIndex: 0 },
  { label: "AI Key Takeaways — automatically generated insights", cursor: { x: 240, y: 370 }, duration: 5500, scroll: -120, phaseIndex: 0 },
  { label: "Export comparison to CSV for offline analysis", cursor: { x: 400, y: 220 }, duration: 3000, click: true, scroll: -40, phaseIndex: 0 },

  // ===== SUBSTITUTION ===== (phase 1) — steps 8–12
  { label: "Open Smart AI Substitution tool", cursor: { x: 360, y: 72 }, duration: 3000, click: true, scroll: 0, phaseIndex: 1 },
  { label: "Select baseline material: ASTM A36 Steel", cursor: { x: 240, y: 160 }, duration: 3000, click: true, scroll: 0, phaseIndex: 1 },
  { label: "Set optimization weights: Cost 40%, Density 30%, Carbon 30%", cursor: { x: 240, y: 220 }, duration: 4500, scroll: 0, phaseIndex: 1 },
  { label: "Click 'Find Alternatives' — AI ranks all matches by fitness", cursor: { x: 240, y: 275 }, duration: 3000, click: true, scroll: 0, phaseIndex: 1 },
  { label: "Results: ranked alternatives with weighted fitness scores", cursor: { x: 280, y: 350 }, duration: 5000, scroll: -140, phaseIndex: 1 },

  // ===== CBAM ===== (phase 2) — steps 13–18
  { label: "Open Supply Chain Risk & CBAM tool", cursor: { x: 120, y: 120 }, duration: 3000, click: true, scroll: 0, phaseIndex: 2 },
  { label: "Choose input method: Upload CSV or Manual Entry", cursor: { x: 240, y: 160 }, duration: 3500, scroll: 0, phaseIndex: 2 },
  { label: "Enter: Steel 304L, 500 kg", cursor: { x: 240, y: 220 }, duration: 3500, scroll: 0, phaseIndex: 2 },
  { label: "Click 'Calculate CBAM & ESG'", cursor: { x: 240, y: 275 }, duration: 2500, click: true, scroll: 0, phaseIndex: 2 },
  { label: "Total Embodied Carbon: 925 kg CO2 — with per-material breakdown", cursor: { x: 240, y: 320 }, duration: 5500, scroll: -100, phaseIndex: 2 },
  { label: "Results Breakdown — emission factors, risk scores, obsolescence", cursor: { x: 240, y: 380 }, duration: 5000, scroll: -180, phaseIndex: 2 },

  // ===== SYNTHESIZER ===== (phase 3) — steps 19–25
  { label: "Open Composite Synthesizer tool", cursor: { x: 360, y: 120 }, duration: 3000, click: true, scroll: 0, phaseIndex: 3 },
  { label: "Select Matrix Material (A): Epoxy Resin", cursor: { x: 200, y: 165 }, duration: 3500, click: true, scroll: 0, phaseIndex: 3 },
  { label: "Select Reinforcement Material (B): Carbon Fiber T300", cursor: { x: 200, y: 210 }, duration: 3500, click: true, scroll: 0, phaseIndex: 3 },
  { label: "Adjust Volume Fraction slider — Matrix 40% / Reinforcement 60%", cursor: { x: 240, y: 260 }, duration: 4500, scroll: 0, phaseIndex: 3 },
  { label: "Click 'Synthesize Composite' — Rule of Mixtures calculates hybrid properties", cursor: { x: 240, y: 300 }, duration: 3000, click: true, scroll: 0, phaseIndex: 3 },
  { label: "Composite result: Density, Elastic Modulus, Tensile Strength, Thermal K", cursor: { x: 240, y: 365 }, duration: 5500, scroll: -140, phaseIndex: 3 },

  // Reset
  { label: "", cursor: { x: 460, y: 400 }, duration: 1000, scroll: 0, phaseIndex: 3 },
];

/* ------------------------------------------------------------------ */
/*  Highlight helper                                                   */
/* ------------------------------------------------------------------ */

const hl = (active: boolean, color = "blue") => {
  const c: Record<string, string> = {
    blue: "ring-2 ring-blue-400/60 shadow-[0_0_16px_rgba(59,130,246,0.12)] border-blue-400",
    purple: "ring-2 ring-purple-400/60 shadow-[0_0_16px_rgba(168,85,247,0.12)] border-purple-400",
    amber: "ring-2 ring-amber-400/60 shadow-[0_0_16px_rgba(245,158,11,0.12)] border-amber-400",
    cyan: "ring-2 ring-cyan-400/60 shadow-[0_0_16px_rgba(6,182,212,0.12)] border-cyan-400",
  };
  return active ? c[color] || c.blue : "";
};

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export function SimulatedCompareDemo() {
  return (
    <DemoEngine
      steps={STEPS}
      phases={PHASES}
      header={
        <>
          <BarChart3 className="w-4 h-4 text-blue-500" />
          <span className="text-xs font-bold text-slate-700 dark:text-slate-200">
            Advanced Analytics
          </span>
        </>
      }
    >
      {(step) => <CompareContent step={step} />}
    </DemoEngine>
  );
}

/* ------------------------------------------------------------------ */
/*  Inner content                                                      */
/* ------------------------------------------------------------------ */

function CompareContent({ step }: { step: number }) {
  const phase = step <= 7 ? "compare" : step <= 12 ? "substitution" : step <= 18 ? "cbam" : step <= 25 ? "synthesizer" : "none";

  return (
    <div className="w-full min-h-full relative">
      {/* Tool selector */}
      <div className="p-3 grid grid-cols-2 gap-2 border-b border-slate-100 dark:border-slate-800">
        {[
          { id: "compare", icon: Scale, label: "Compare", badge: "Free", badgeColor: "bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700", active: "border-blue-400 bg-blue-50/50 dark:bg-blue-900/15 ring-1 ring-blue-300/50" },
          { id: "substitution", icon: Replace, label: "AI Substitution", badge: "Pro", badgeColor: "bg-purple-100 text-purple-600 border-purple-200 dark:bg-purple-900/30 dark:text-purple-400 dark:border-purple-700/50", active: "border-purple-400 bg-purple-50/50 dark:bg-purple-900/15 ring-1 ring-purple-300/50" },
          { id: "cbam", icon: Factory, label: "CBAM & ESG", badge: "Enterprise", badgeColor: "bg-amber-100 text-amber-600 border-amber-200 dark:bg-amber-900/30 dark:text-amber-400 dark:border-amber-700/50", active: "border-amber-400 bg-amber-50/50 dark:bg-amber-900/15 ring-1 ring-amber-300/50" },
          { id: "synthesizer", icon: Layers, label: "Synthesizer", badge: "Pro", badgeColor: "bg-cyan-100 text-cyan-600 border-cyan-200 dark:bg-cyan-900/30 dark:text-cyan-400 dark:border-cyan-700/50", active: "border-cyan-400 bg-cyan-50/50 dark:bg-cyan-900/15 ring-1 ring-cyan-300/50" },
        ].map(t => (
          <div key={t.id} className={`p-2 rounded-xl border text-center transition-all duration-300 ${phase === t.id ? t.active : "border-slate-200 dark:border-slate-800"}`}>
            <div className="flex items-center gap-2">
              <t.icon className={`w-3.5 h-3.5 ${phase === t.id ? "text-slate-900 dark:text-white" : "text-slate-400"}`} />
              <span className={`text-[9px] font-bold ${phase === t.id ? "text-slate-900 dark:text-white" : "text-slate-500"}`}>{t.label}</span>
            </div>
            <div className="mt-1">
              <span className={`text-[7px] font-bold uppercase px-1.5 py-0.5 rounded border ${t.badgeColor}`}>{t.badge}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="p-4">
        <AnimatePresence mode="wait">
          {/* ===== COMPARE ===== */}
          {phase === "compare" && (
            <motion.div key="compare" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
              {/* Material selectors */}
              <div className="flex gap-2">
                <div className={`flex-1 border rounded-xl p-2 flex items-center gap-1.5 transition-all duration-300 bg-white dark:bg-slate-900 ${step === 2 ? "border-blue-400 ring-1 ring-blue-200 shadow-[0_0_16px_rgba(59,130,246,0.1)]" : "border-slate-200 dark:border-slate-700"}`}>
                  <Search className="w-3 h-3 text-slate-400" />
                  <span className="text-[10px] font-medium text-slate-700 dark:text-slate-300">{step >= 2 ? "Ti-6Al-4V Grade 5" : <span className="text-slate-400">Material 1...</span>}</span>
                </div>
                <div className={`flex-1 border rounded-xl p-2 flex items-center gap-1.5 transition-all duration-300 bg-white dark:bg-slate-900 ${step === 3 ? "border-blue-400 ring-1 ring-blue-200 shadow-[0_0_16px_rgba(59,130,246,0.1)]" : "border-slate-200 dark:border-slate-700"}`}>
                  <Search className="w-3 h-3 text-slate-400" />
                  <span className="text-[10px] font-medium text-slate-700 dark:text-slate-300">{step >= 3 ? "Aluminium 7075-T6" : <span className="text-slate-400">Material 2...</span>}</span>
                </div>
              </div>

              {/* Results */}
              {step >= 4 && (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-3">
                  {/* Radar + Matrix side by side */}
                  <div className="grid grid-cols-2 gap-2">
                    {/* Radar Chart */}
                    <div className={`p-2.5 rounded-xl border transition-all duration-300 bg-white dark:bg-slate-900 ${step === 4 ? hl(true, "blue") : "border-slate-200 dark:border-slate-800"}`}>
                      <p className="text-[8px] font-bold text-slate-500 uppercase mb-1 text-center">Property Fingerprint</p>
                      <svg viewBox="0 0 120 120" className="w-full h-20 mx-auto">
                        <circle cx="60" cy="60" r="45" fill="none" stroke="currentColor" className="text-slate-200 dark:text-slate-700" strokeWidth="0.5"/>
                        <circle cx="60" cy="60" r="30" fill="none" stroke="currentColor" className="text-slate-200 dark:text-slate-700" strokeWidth="0.5"/>
                        <circle cx="60" cy="60" r="15" fill="none" stroke="currentColor" className="text-slate-200 dark:text-slate-700" strokeWidth="0.5"/>
                        {[0,60,120,180,240,300].map(a => { const r=45; const x=60+r*Math.cos((a-90)*Math.PI/180); const y=60+r*Math.sin((a-90)*Math.PI/180); return <line key={a} x1="60" y1="60" x2={x} y2={y} stroke="currentColor" className="text-slate-200 dark:text-slate-700" strokeWidth="0.5"/>; })}
                        <text x="60" y="8" textAnchor="middle" className="fill-slate-500 text-[6px]">UTS</text>
                        <text x="105" y="35" textAnchor="start" className="fill-slate-500 text-[6px]">Yield</text>
                        <text x="105" y="90" textAnchor="start" className="fill-slate-500 text-[6px]">Cost</text>
                        <text x="60" y="115" textAnchor="middle" className="fill-slate-500 text-[6px]">Density</text>
                        <text x="10" y="90" textAnchor="end" className="fill-slate-500 text-[6px]">Carbon</text>
                        <text x="10" y="35" textAnchor="end" className="fill-slate-500 text-[6px]">Th.K</text>
                        <polygon points="60,18 95,40 90,85 60,95 25,80 30,38" fill="rgba(59,130,246,0.15)" stroke="#3b82f6" strokeWidth="1.5"/>
                        <polygon points="60,25 85,35 98,75 60,100 20,85 22,42" fill="rgba(168,85,247,0.15)" stroke="#a855f7" strokeWidth="1.5"/>
                      </svg>
                      <div className="flex justify-center gap-3 mt-1">
                        <span className="text-[7px] flex items-center gap-1"><span className="w-1.5 h-1.5 rounded bg-blue-500"></span>Ti-6Al-4V</span>
                        <span className="text-[7px] flex items-center gap-1"><span className="w-1.5 h-1.5 rounded bg-purple-500"></span>Al 7075</span>
                      </div>
                    </div>

                    {/* Comparison Matrix */}
                    <div className={`p-2.5 rounded-xl border transition-all duration-300 bg-white dark:bg-slate-900 ${step === 5 ? hl(true, "blue") : "border-slate-200 dark:border-slate-800"}`}>
                      <div className="flex justify-between items-center mb-1.5">
                        <p className="text-[8px] font-bold text-slate-500 uppercase">Comparison Matrix</p>
                        <div className={`flex items-center gap-0.5 transition-all duration-300 ${step === 7 ? "ring-1 ring-blue-300 rounded p-0.5 bg-blue-50 dark:bg-blue-900/20" : ""}`}>
                          <Download className="w-2.5 h-2.5 text-slate-400" />
                          <span className="text-[7px] text-slate-400">CSV</span>
                        </div>
                      </div>
                      <table className="w-full text-[8px]">
                        <thead><tr className="border-b border-slate-100 dark:border-slate-800">
                          <th className="pb-0.5 text-left text-slate-400 font-medium">Property</th>
                          <th className="pb-0.5 text-blue-500 font-bold">Ti</th>
                          <th className="pb-0.5 text-purple-500 font-bold">Al</th>
                        </tr></thead>
                        <tbody>
                          {[{p:"Density",a:"4.43",b:"2.81",w:"b"},{p:"UTS",a:"950",b:"572",w:"a"},{p:"Yield",a:"880",b:"503",w:"a"},{p:"Cost/kg",a:"₹25",b:"₹3.2",w:"b"},{p:"Th.K",a:"6.7",b:"130",w:"b"},{p:"Carbon",a:"36",b:"8.2",w:"b"}].map(r => (
                            <tr key={r.p} className="border-b border-slate-50 dark:border-slate-900">
                              <td className="py-0.5 text-slate-500">{r.p}</td>
                              <td className={`py-0.5 text-center font-semibold ${r.w==="a"?"text-emerald-600":"text-slate-700 dark:text-slate-300"}`}>{r.a}{r.w==="a" && <span className="ml-0.5 text-[6px]">★</span>}</td>
                              <td className={`py-0.5 text-center font-semibold ${r.w==="b"?"text-emerald-600":"text-slate-700 dark:text-slate-300"}`}>{r.b}{r.w==="b" && <span className="ml-0.5 text-[6px]">★</span>}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* AI Insights */}
                  <div className={`p-3 rounded-xl border transition-all duration-300 bg-white dark:bg-slate-900 ${step === 6 ? hl(true, "purple") : "border-slate-200 dark:border-slate-800"}`}>
                    <p className="text-[9px] font-bold text-slate-500 uppercase mb-1.5 flex items-center gap-1"><Info className="w-3 h-3 text-purple-500" /> Automated Insights & Key Takeaways</p>
                    <ul className="space-y-1 text-[9px] text-slate-600 dark:text-slate-400">
                      <li className="flex items-start gap-1"><span className="text-blue-500 mt-0.5 shrink-0">•</span> Ti-6Al-4V offers the highest structural integrity (Yield: 880 MPa).</li>
                      <li className="flex items-start gap-1"><span className="text-purple-500 mt-0.5 shrink-0">•</span> Al 7075-T6 is the most cost-effective option (₹3.2/kg vs ₹25/kg).</li>
                      <li className="flex items-start gap-1"><span className="text-emerald-500 mt-0.5 shrink-0">•</span> Al 7075-T6 is the lightest material (2.81 vs 4.43 g/cm³).</li>
                      <li className="flex items-start gap-1"><span className="text-amber-500 mt-0.5 shrink-0">•</span> Al 7075-T6 has the lowest embodied carbon footprint.</li>
                    </ul>
                  </div>
                </motion.div>
              )}
            </motion.div>
          )}

          {/* ===== SUBSTITUTION ===== */}
          {phase === "substitution" && (
            <motion.div key="sub" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
              <div className={`border rounded-xl p-2 text-xs transition-all duration-300 bg-white dark:bg-slate-900 ${step===9?hl(true,"purple"):"border-slate-200 dark:border-slate-700"}`}>
                <span className="text-slate-500 text-[10px]">Baseline:</span> <span className="font-semibold text-slate-800 dark:text-white">{step>=9?"ASTM A36 Steel":"Select..."}</span>
              </div>
              <div className={`border rounded-xl p-3 transition-all duration-300 bg-white dark:bg-slate-900 ${step===10?hl(true,"purple"):"border-slate-200 dark:border-slate-700"}`}>
                <p className="text-[9px] font-bold text-slate-500 mb-2">Optimization Weights</p>
                {[{l:"Cost",v:40,c:"bg-emerald-500"},{l:"Density",v:30,c:"bg-blue-500"},{l:"Carbon",v:30,c:"bg-amber-500"}].map(w => (
                  <div key={w.l} className="flex items-center gap-2 mb-1">
                    <span className="text-[9px] text-slate-500 w-12">{w.l}</span>
                    <div className="flex-1 h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden"><div className={`h-full ${w.c} rounded-full transition-all`} style={{width:`${step>=10?w.v:0}%`}}></div></div>
                    <span className="text-[9px] font-bold text-slate-700 dark:text-slate-300 w-8">{step>=10?`${w.v}%`:""}</span>
                  </div>
                ))}
              </div>
              <button className={`w-full py-2 rounded-xl text-xs font-bold text-white transition-all ${step>=11?"bg-purple-600 shadow-lg":"bg-slate-300 dark:bg-slate-700"}`}>{step>=12?"3 Alternatives Found":"Find Alternatives"}</button>
              {step >= 12 && (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-1.5">
                  {[{n:"AISI 1020 Steel",s:"92%"},{n:"S275JR Structural",s:"87%"},{n:"ASTM A572 Grade 50",s:"81%"}].map((r,i) => (
                    <div key={i} className="flex items-center justify-between p-2 bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
                      <div>
                        <span className="text-[10px] font-bold text-slate-800 dark:text-white block">{r.n}</span>
                        <span className="text-[8px] text-slate-400">Metal • Structural Steel</span>
                      </div>
                      <span className="text-[9px] font-bold text-purple-600 bg-purple-100 dark:bg-purple-900/30 px-2 py-0.5 rounded-full border border-purple-200 dark:border-purple-800">Fitness: {r.s}</span>
                    </div>
                  ))}
                </motion.div>
              )}
            </motion.div>
          )}

          {/* ===== CBAM ===== */}
          {phase === "cbam" && (
            <motion.div key="cbam" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
              <div className="flex gap-2">
                <div className="flex-1 p-2 rounded-lg border text-center text-[10px] font-bold border-slate-200 dark:border-slate-700 text-slate-500">
                  Upload CSV
                </div>
                <div className={`flex-1 p-2 rounded-lg border text-center text-[10px] font-bold transition-all duration-300 ${step>=14?"border-amber-400 bg-amber-50 dark:bg-amber-900/20 ring-1 ring-amber-300":"border-slate-200 dark:border-slate-700 text-slate-500"}`}>
                  Manual Entry
                </div>
              </div>

              {step >= 15 && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-2">
                  <div className={`border rounded-xl p-2 transition-all duration-300 bg-white dark:bg-slate-900 ${step===15?hl(true,"amber"):"border-slate-200 dark:border-slate-700"}`}>
                    <span className="text-[9px] text-slate-400">Material Name/Grade</span>
                    <p className="text-xs font-semibold text-slate-800 dark:text-white">Steel 304L</p>
                  </div>
                  <div className="border rounded-xl p-2 bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-700">
                    <span className="text-[9px] text-slate-400">Weight (kg)</span>
                    <p className="text-xs font-semibold text-slate-800 dark:text-white">500</p>
                  </div>
                </motion.div>
              )}

              {step >= 16 && <button className={`w-full py-2 rounded-xl text-xs font-bold text-white flex items-center justify-center gap-2 transition-all ${step>=17?"bg-amber-600 shadow-lg":"bg-slate-300 dark:bg-slate-700"}`}><Factory className="w-3 h-3" /> {step>=17?"Analysis Complete":"Calculate CBAM & ESG"}</button>}

              {step >= 17 && (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-2">
                  <div className={`p-3 rounded-xl border transition-all duration-300 bg-white dark:bg-slate-900 ${step===17?hl(true,"amber"):"border-slate-200 dark:border-slate-800"}`}>
                    <p className="text-[9px] text-slate-500 flex items-center gap-1"><Factory className="w-3 h-3 text-emerald-500" /> Total Embodied Carbon</p>
                    <p className="text-xl font-bold text-slate-900 dark:text-white">925 <span className="text-xs text-slate-400 font-normal">kg CO2</span></p>
                  </div>

                  <div className={`p-3 rounded-xl border transition-all duration-300 bg-white dark:bg-slate-900 ${step===18?hl(true,"amber"):"border-slate-200 dark:border-slate-800"}`}>
                    <p className="text-[8px] font-bold text-slate-500 uppercase mb-1.5">Results Breakdown</p>
                    <table className="w-full text-[8px]">
                      <thead><tr className="border-b border-slate-100 dark:border-slate-800">
                        <th className="pb-0.5 text-left text-slate-400">Material</th>
                        <th className="pb-0.5 text-slate-400">Weight</th>
                        <th className="pb-0.5 text-slate-400">EF</th>
                        <th className="pb-0.5 text-slate-400">CO2</th>
                        <th className="pb-0.5 text-slate-400">Risk</th>
                      </tr></thead>
                      <tbody>
                        <tr><td className="py-1 font-semibold text-slate-800 dark:text-white">304L</td><td className="py-1 text-center">500kg</td><td className="py-1 text-center">1.85</td><td className="py-1 text-center font-bold">925</td><td className="py-1 text-center"><span className="px-1 py-0.5 rounded bg-emerald-100 text-emerald-700 text-[7px] font-bold dark:bg-emerald-900/30 dark:text-emerald-400">Low</span></td></tr>
                      </tbody>
                    </table>
                    <div className="flex items-center gap-1 mt-1.5 pt-1.5 border-t border-slate-100 dark:border-slate-800">
                      <Download className="w-2.5 h-2.5 text-slate-400" />
                      <span className="text-[7px] text-slate-400">Export to CSV</span>
                    </div>
                  </div>
                </motion.div>
              )}
            </motion.div>
          )}

          {/* ===== SYNTHESIZER ===== */}
          {phase === "synthesizer" && (
            <motion.div key="synth" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
              <div className={`border rounded-xl p-2.5 transition-all duration-300 bg-white dark:bg-slate-900 ${step===20?hl(true,"cyan"):"border-slate-200 dark:border-slate-700"}`}>
                <span className="text-[9px] font-semibold text-cyan-500">Matrix Material (A)</span>
                <p className="text-xs font-semibold text-slate-800 dark:text-white">{step>=20?"Epoxy Resin":"Search matrix material..."}</p>
              </div>
              <div className={`border rounded-xl p-2.5 transition-all duration-300 bg-white dark:bg-slate-900 ${step===21?hl(true,"cyan"):"border-slate-200 dark:border-slate-700"}`}>
                <span className="text-[9px] font-semibold text-teal-500">Reinforcement Material (B)</span>
                <p className="text-xs font-semibold text-slate-800 dark:text-white">{step>=21?"Carbon Fiber T300":"Search reinforcement material..."}</p>
              </div>
              <div className={`border rounded-xl p-3 transition-all duration-300 bg-white dark:bg-slate-900 ${step===22?hl(true,"cyan"):"border-slate-200 dark:border-slate-700"}`}>
                <div className="flex justify-between text-[9px] mb-1">
                  <span className="text-slate-500">Volume Fraction (Matrix A)</span>
                  <span className="font-bold text-cyan-500">{step>=22?"40%":"50%"}</span>
                </div>
                <div className="h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full transition-all" style={{width:step>=22?"40%":"50%"}}></div>
                </div>
                <div className="flex justify-between text-[7px] text-slate-400 mt-0.5">
                  <span>0% (All Reinforcement)</span>
                  <span>100% (All Matrix)</span>
                </div>
              </div>
              <button className={`w-full py-2 rounded-xl text-xs font-bold text-white transition-all ${step>=23?"bg-cyan-600 shadow-lg":"bg-slate-300 dark:bg-slate-700"}`}>{step>=24?"Composite Generated":"Synthesize Composite"}</button>
              {step >= 24 && (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-2 gap-2">
                  {[{l:"Density",v:"1.58 g/cm³"},{l:"Elastic Modulus",v:"142 GPa"},{l:"Tensile Strength",v:"1,240 MPa"},{l:"Thermal K",v:"7.2 W/mK"}].map(p => (
                    <div key={p.l} className="bg-cyan-50 dark:bg-cyan-900/20 p-2.5 rounded-xl border border-cyan-200 dark:border-cyan-800">
                      <p className="text-[7px] text-slate-500 uppercase font-bold">{p.l}</p>
                      <p className="text-sm font-bold text-slate-900 dark:text-white">{p.v}</p>
                    </div>
                  ))}
                </motion.div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
