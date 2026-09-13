"use client";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointer2, Scale, Replace, Factory, Layers, Search, BarChart3 } from "lucide-react";

interface Step { label: string; cursor: { x: number; y: number }; duration: number; click?: boolean; }

const STEPS: Step[] = [
  // COMPARE FLOW
  { label: "Open Side-by-Side Compare tool", cursor: { x: 120, y: 90 }, duration: 1500, click: true },
  { label: "Search for the first material...", cursor: { x: 120, y: 155 }, duration: 1200, click: true },
  { label: "Typing 'Titanium'...", cursor: { x: 120, y: 155 }, duration: 1000 },
  { label: "Select Ti-6Al-4V Grade 5", cursor: { x: 140, y: 195 }, duration: 1200, click: true },
  { label: "Now search the second material...", cursor: { x: 340, y: 155 }, duration: 1200, click: true },
  { label: "Select Aluminium 7075-T6", cursor: { x: 340, y: 195 }, duration: 1200, click: true },
  { label: "Click 'Run Comparison'", cursor: { x: 240, y: 235 }, duration: 1200, click: true },
  { label: "Radar chart + AI takeaways generated!", cursor: { x: 280, y: 310 }, duration: 3000 },
  // SUBSTITUTION FLOW
  { label: "Open AI Substitution tool", cursor: { x: 360, y: 90 }, duration: 1500, click: true },
  { label: "Select baseline material: ASTM A36 Steel", cursor: { x: 240, y: 160 }, duration: 1500, click: true },
  { label: "Set weight: Cost 40%, Density 30%, Carbon 30%", cursor: { x: 240, y: 210 }, duration: 2000 },
  { label: "Click 'Find Alternatives' — AI ranks all matches", cursor: { x: 240, y: 250 }, duration: 1500, click: true },
  { label: "Results: ranked by weighted fitness score!", cursor: { x: 280, y: 310 }, duration: 2500 },
  // CBAM FLOW
  { label: "Open CBAM Emissions Calculator", cursor: { x: 120, y: 380 }, duration: 1500, click: true },
  { label: "Enter material, volume (tonnes), emission factor", cursor: { x: 240, y: 175 }, duration: 2000 },
  { label: "Set EU ETS carbon price (EUR/tonne)", cursor: { x: 240, y: 215 }, duration: 1500 },
  { label: "Calculate — total emissions & CBAM tax in EUR", cursor: { x: 240, y: 255 }, duration: 1500, click: true },
  { label: "CBAM tax liability calculated for EU compliance!", cursor: { x: 280, y: 310 }, duration: 2500 },
  // SYNTHESIZER FLOW
  { label: "Open Composite Synthesizer", cursor: { x: 360, y: 380 }, duration: 1500, click: true },
  { label: "Select matrix (e.g., Epoxy) and fiber (e.g., Carbon T300)", cursor: { x: 240, y: 175 }, duration: 2000 },
  { label: "Set fiber volume fraction: 60%", cursor: { x: 240, y: 215 }, duration: 1500 },
  { label: "Blend — Rule of Mixtures predicts hybrid properties!", cursor: { x: 240, y: 260 }, duration: 1500, click: true },
  { label: "Composite properties: Density, Modulus, Strength, Thermal K", cursor: { x: 280, y: 310 }, duration: 2500 },
  // Reset
  { label: "", cursor: { x: 450, y: 400 }, duration: 600 },
];

export function SimulatedCompareDemo() {
  const [step, setStep] = useState(0);
  const ref = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    let i = 0;
    const go = () => { if (i >= STEPS.length) i = 0; setStep(i); ref.current = setTimeout(() => { i++; go(); }, STEPS[i].duration); };
    go();
    return () => { if (ref.current) clearTimeout(ref.current); };
  }, []);

  const s = STEPS[step];
  // Determine which tool panel to show
  const phase = step <= 7 ? "compare" : step <= 12 ? "substitution" : step <= 17 ? "cbam" : step <= 22 ? "synthesizer" : "none";

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 relative overflow-hidden min-h-[440px]">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

      <div className="relative z-10 w-full max-w-lg mx-auto">
        <div className="bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
          <div className="px-5 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-blue-500" />
            <span className="text-sm font-bold text-slate-900 dark:text-white">Advanced Analytics</span>
          </div>

          {/* Tool selector grid */}
          <div className="p-3 grid grid-cols-2 gap-2 border-b border-slate-100 dark:border-slate-800">
            {[
              { id: "compare", icon: Scale, label: "Compare", c: "blue" },
              { id: "substitution", icon: Replace, label: "AI Substitution", c: "purple" },
              { id: "cbam", icon: Factory, label: "CBAM Emissions", c: "amber" },
              { id: "synthesizer", icon: Layers, label: "Synthesizer", c: "cyan" },
            ].map(t => (
              <div key={t.id} className={`p-2 rounded-xl border text-center transition-all flex items-center gap-2 ${phase === t.id ? `border-${t.c}-400 bg-${t.c}-50 dark:bg-${t.c}-900/20 shadow-md ring-1 ring-${t.c}-300` : "border-slate-200 dark:border-slate-800"}`}>
                <t.icon className={`w-4 h-4 ${phase === t.id ? `text-${t.c}-600` : "text-slate-400"}`} />
                <span className={`text-[10px] font-bold ${phase === t.id ? "text-slate-900 dark:text-white" : "text-slate-500"}`}>{t.label}</span>
              </div>
            ))}
          </div>

          {/* Tool content */}
          <div className="p-5 min-h-[220px]">
            <AnimatePresence mode="wait">
              {/* COMPARE */}
              {phase === "compare" && (
                <motion.div key="compare" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                  <div className="flex gap-3 mb-4">
                    <div className={`flex-1 border rounded-xl p-2 flex items-center gap-1.5 transition-all ${step >= 1 && step <= 3 ? "border-blue-400 ring-1 ring-blue-200" : "border-slate-200 dark:border-slate-700"}`}>
                      <Search className="w-3 h-3 text-slate-400" />
                      <span className="text-[10px] font-medium text-slate-700 dark:text-slate-300">{step >= 3 ? "Ti-6Al-4V Grade 5" : step >= 2 ? <span>Titanium<span className="animate-pulse text-blue-500">|</span></span> : <span className="text-slate-400">Material 1...</span>}</span>
                    </div>
                    <div className={`flex-1 border rounded-xl p-2 flex items-center gap-1.5 transition-all ${step >= 4 && step <= 5 ? "border-blue-400 ring-1 ring-blue-200" : "border-slate-200 dark:border-slate-700"}`}>
                      <Search className="w-3 h-3 text-slate-400" />
                      <span className="text-[10px] font-medium text-slate-700 dark:text-slate-300">{step >= 5 ? "Aluminium 7075-T6" : <span className="text-slate-400">Material 2...</span>}</span>
                    </div>
                  </div>
                  <button className={`w-full py-2 rounded-xl text-xs font-bold text-white mb-4 ${step >= 6 ? "bg-blue-600 shadow-lg" : "bg-slate-300 dark:bg-slate-700"}`}>{step >= 7 ? "Analysis Complete" : "Run Comparison"}</button>
                  {step >= 7 && (
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="flex gap-3">
                      <div className="w-24 h-24 rounded-full border-2 border-slate-200 dark:border-slate-700 relative flex items-center justify-center shrink-0">
                        <svg className="absolute inset-0 w-full h-full"><polygon points="48,8 80,48 48,72 16,48" className="fill-blue-500/20 stroke-blue-500" strokeWidth="1.5"/></svg>
                        <svg className="absolute inset-0 w-full h-full"><polygon points="48,20 88,48 48,88 10,48" className="fill-purple-500/20 stroke-purple-500" strokeWidth="1.5"/></svg>
                      </div>
                      <div className="space-y-1.5 flex-1">
                        <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded bg-blue-500"></div><span className="text-[10px] font-semibold text-slate-700 dark:text-slate-300">Ti-6Al-4V wins on tensile strength</span></div>
                        <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded bg-purple-500"></div><span className="text-[10px] font-semibold text-slate-700 dark:text-slate-300">Al 7075 is 42% more cost-effective</span></div>
                        <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded bg-emerald-500"></div><span className="text-[10px] font-semibold text-slate-700 dark:text-slate-300">Al 7075 is 63% lighter (density)</span></div>
                      </div>
                    </motion.div>
                  )}
                </motion.div>
              )}
              {/* SUBSTITUTION */}
              {phase === "substitution" && (
                <motion.div key="sub" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
                  <div className={`border rounded-xl p-2 text-xs transition-all ${step === 9 ? "border-purple-400 ring-1 ring-purple-200" : "border-slate-200 dark:border-slate-700"}`}>
                    <span className="text-slate-500 text-[10px]">Baseline:</span> <span className="font-semibold text-slate-800 dark:text-white">{step >= 9 ? "ASTM A36 Steel" : "Select..."}</span>
                  </div>
                  <div className={`border rounded-xl p-3 transition-all ${step === 10 ? "border-purple-400 ring-1 ring-purple-200" : "border-slate-200 dark:border-slate-700"}`}>
                    <p className="text-[10px] font-bold text-slate-500 mb-2">Optimization Weights</p>
                    {[{l:"Cost",v:40,c:"bg-emerald-500"},{l:"Density",v:30,c:"bg-blue-500"},{l:"Carbon",v:30,c:"bg-amber-500"}].map(w=>(
                      <div key={w.l} className="flex items-center gap-2 mb-1">
                        <span className="text-[10px] text-slate-500 w-12">{w.l}</span>
                        <div className="flex-1 h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden"><div className={`h-full ${w.c} rounded-full`} style={{width:`${step>=10?w.v:0}%`}}></div></div>
                        <span className="text-[10px] font-bold text-slate-700 dark:text-slate-300 w-8">{step>=10?`${w.v}%`:""}</span>
                      </div>
                    ))}
                  </div>
                  <button className={`w-full py-2 rounded-xl text-xs font-bold text-white ${step>=11?"bg-purple-600 shadow-lg":"bg-slate-300 dark:bg-slate-700"}`}>{step>=12?"3 Alternatives Found":"Find Alternatives"}</button>
                  {step >= 12 && (
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-1.5">
                      {[{n:"AISI 1020 Steel",s:"92%"},{n:"S275JR",s:"87%"},{n:"ASTM A572",s:"81%"}].map((r,i)=>(
                        <div key={i} className="flex items-center justify-between p-2 bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
                          <span className="text-[10px] font-bold text-slate-800 dark:text-white">{r.n}</span>
                          <span className="text-[10px] font-bold text-purple-600 bg-purple-100 dark:bg-purple-900/30 px-2 py-0.5 rounded">Fitness: {r.s}</span>
                        </div>
                      ))}
                    </motion.div>
                  )}
                </motion.div>
              )}
              {/* CBAM */}
              {phase === "cbam" && (
                <motion.div key="cbam" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
                  <div className={`border rounded-xl p-3 space-y-2 transition-all ${step===14?"border-amber-400 ring-1 ring-amber-200":"border-slate-200 dark:border-slate-700"}`}>
                    {[{l:"Material",v:"Structural Steel A36"},{l:"Volume",v:"500 tonnes"},{l:"Emission Factor",v:"1.85 tCO2/t"}].map(f=>(
                      <div key={f.l} className="flex justify-between text-xs"><span className="text-slate-500">{f.l}</span><span className="font-semibold text-slate-800 dark:text-white">{step>=14?f.v:"—"}</span></div>
                    ))}
                  </div>
                  <div className={`border rounded-xl p-2 text-xs transition-all ${step===15?"border-amber-400 ring-1 ring-amber-200":"border-slate-200 dark:border-slate-700"}`}>
                    <span className="text-slate-500">EU ETS Price:</span> <span className="font-semibold text-slate-800 dark:text-white">{step>=15?"€95/tonne":"—"}</span>
                  </div>
                  <button className={`w-full py-2 rounded-xl text-xs font-bold text-white ${step>=16?"bg-amber-600 shadow-lg":"bg-slate-300 dark:bg-slate-700"}`}>{step>=17?"Calculation Complete":"Calculate CBAM Tax"}</button>
                  {step >= 17 && (
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="p-3 bg-amber-50 dark:bg-amber-900/20 rounded-xl border border-amber-200 dark:border-amber-800 space-y-1">
                      <div className="flex justify-between text-xs"><span className="text-slate-600">Total Emissions</span><span className="font-bold text-slate-900 dark:text-white">925 tCO2</span></div>
                      <div className="flex justify-between text-xs"><span className="text-slate-600">CBAM Tax Liability</span><span className="font-bold text-amber-700 text-base">€87,875</span></div>
                    </motion.div>
                  )}
                </motion.div>
              )}
              {/* SYNTHESIZER */}
              {phase === "synthesizer" && (
                <motion.div key="synth" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
                  <div className={`border rounded-xl p-3 space-y-2 transition-all ${step===19?"border-cyan-400 ring-1 ring-cyan-200":"border-slate-200 dark:border-slate-700"}`}>
                    <div className="flex justify-between text-xs"><span className="text-slate-500">Matrix</span><span className="font-semibold text-slate-800 dark:text-white">{step>=19?"Epoxy Resin":"Select..."}</span></div>
                    <div className="flex justify-between text-xs"><span className="text-slate-500">Fiber</span><span className="font-semibold text-slate-800 dark:text-white">{step>=19?"Carbon Fiber T300":"Select..."}</span></div>
                  </div>
                  <div className={`border rounded-xl p-2 transition-all ${step===20?"border-cyan-400 ring-1 ring-cyan-200":"border-slate-200 dark:border-slate-700"}`}>
                    <div className="flex items-center gap-2 text-xs"><span className="text-slate-500">Fiber Volume:</span><div className="flex-1 h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden"><div className="h-full bg-cyan-500 rounded-full" style={{width:step>=20?"60%":"0%"}}></div></div><span className="font-bold text-slate-800 dark:text-white">{step>=20?"60%":"—"}</span></div>
                  </div>
                  <button className={`w-full py-2 rounded-xl text-xs font-bold text-white ${step>=21?"bg-cyan-600 shadow-lg":"bg-slate-300 dark:bg-slate-700"}`}>{step>=22?"Composite Generated":"Blend Materials"}</button>
                  {step >= 22 && (
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-2 gap-2">
                      {[{l:"Density",v:"1.58 g/cm3"},{l:"Elastic Modulus",v:"142 GPa"},{l:"Tensile Strength",v:"1,240 MPa"},{l:"Thermal K",v:"7.2 W/mK"}].map(p=>(
                        <div key={p.l} className="bg-cyan-50 dark:bg-cyan-900/20 p-2 rounded-lg border border-cyan-200 dark:border-cyan-800">
                          <p className="text-[8px] text-slate-500 uppercase">{p.l}</p>
                          <p className="text-xs font-bold text-slate-900 dark:text-white">{p.v}</p>
                        </div>
                      ))}
                    </motion.div>
                  )}
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
