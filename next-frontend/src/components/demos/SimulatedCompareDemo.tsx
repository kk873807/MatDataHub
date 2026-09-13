"use client";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointer2, Scale, Replace, Factory, Layers, Search, BarChart3, Info, Upload, Download } from "lucide-react";

interface Step { label: string; cursor: { x: number; y: number }; duration: number; click?: boolean; }

const STEPS: Step[] = [
  // ===== COMPARE (steps 0-10) =====
  { label: "Open Side-by-Side Compare tool", cursor: { x: 120, y: 90 }, duration: 6000, click: true },
  { label: "Search for the first material...", cursor: { x: 120, y: 155 }, duration: 5000, click: true },
  { label: "Typing 'Titanium'...", cursor: { x: 120, y: 155 }, duration: 4000 },
  { label: "Select Ti-6Al-4V Grade 5", cursor: { x: 140, y: 195 }, duration: 5000, click: true },
  { label: "Search and select second material: Al 7075-T6", cursor: { x: 340, y: 155 }, duration: 6000, click: true },
  { label: "Click 'Run Comparison'", cursor: { x: 240, y: 230 }, duration: 5000, click: true },
  // Radar chart
  { label: "Property Fingerprint — radar chart overlays all properties", cursor: { x: 100, y: 310 }, duration: 5000 },
  // Comparison matrix
  { label: "Direct Comparison Matrix — property-by-property table with best values highlighted in green", cursor: { x: 280, y: 310 }, duration: 5500 },
  // Takeaways
  { label: "AI Key Takeaways — automatically generated insights", cursor: { x: 240, y: 390 }, duration: 5500 },
  // Export
  { label: "Export comparison to CSV for offline analysis", cursor: { x: 400, y: 280 }, duration: 6000, click: true },

  // ===== SUBSTITUTION (steps 10-15) =====
  { label: "Open Smart AI Substitution tool", cursor: { x: 360, y: 90 }, duration: 6000, click: true },
  { label: "Select baseline material: ASTM A36 Steel", cursor: { x: 240, y: 160 }, duration: 6000, click: true },
  { label: "Set optimization weights: Cost 40%, Density 30%, Carbon 30%", cursor: { x: 240, y: 210 }, duration: 4500 },
  { label: "Click 'Find Alternatives' — AI ranks all matches by fitness", cursor: { x: 240, y: 260 }, duration: 6000, click: true },
  { label: "Results: ranked alternatives with weighted fitness scores!", cursor: { x: 280, y: 340 }, duration: 5000 },

  // ===== CBAM (steps 15-23) =====
  { label: "Open Supply Chain Risk & CBAM tool", cursor: { x: 120, y: 420 }, duration: 6000, click: true },
  { label: "Choose input method: Upload CSV or Manual Entry", cursor: { x: 240, y: 160 }, duration: 3500 },
  { label: "Upload BOM — drag CSV file with Material & Weight columns", cursor: { x: 150, y: 200 }, duration: 4500, click: true },
  { label: "Or use Manual Entry — type material name and weight in kg", cursor: { x: 340, y: 200 }, duration: 4500, click: true },
  { label: "Enter: Steel 304L, 500 kg", cursor: { x: 240, y: 250 }, duration: 6000 },
  { label: "Click 'Calculate CBAM & ESG'", cursor: { x: 240, y: 290 }, duration: 5000, click: true },
  { label: "Total Embodied Carbon: 925 kg CO2 — with per-material breakdown", cursor: { x: 240, y: 340 }, duration: 5500 },
  { label: "Results Breakdown table — emission factors, risk scores, obsolescence", cursor: { x: 240, y: 390 }, duration: 5000 },

  // ===== SYNTHESIZER (steps 23-30) =====
  { label: "Open Composite Synthesizer tool", cursor: { x: 360, y: 420 }, duration: 6000, click: true },
  { label: "Select Matrix Material (A): Epoxy Resin", cursor: { x: 200, y: 170 }, duration: 3500, click: true },
  { label: "Select Reinforcement Material (B): Carbon Fiber T300", cursor: { x: 200, y: 210 }, duration: 3500, click: true },
  { label: "Adjust Volume Fraction slider — Matrix 40% / Reinforcement 60%", cursor: { x: 240, y: 250 }, duration: 4500 },
  { label: "Click 'Blend' — Rule of Mixtures calculates hybrid properties", cursor: { x: 240, y: 290 }, duration: 6000, click: true },
  { label: "Composite result: Density, Elastic Modulus, Tensile Strength, Thermal K", cursor: { x: 240, y: 360 }, duration: 5500 },

  // Reset
  { label: "", cursor: { x: 460, y: 460 }, duration: 600 },
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
  const phase = step <= 9 ? "compare" : step <= 14 ? "substitution" : step <= 22 ? "cbam" : step <= 28 ? "synthesizer" : "none";

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 relative min-h-[480px]">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] rounded-3xl overflow-hidden pointer-events-none"></div>

      <div className="relative z-10 w-full max-w-lg mx-auto">
        <div className="bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
          <div className="px-5 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-blue-500" />
            <span className="text-sm font-bold text-slate-900 dark:text-white">Advanced Analytics</span>
          </div>

          {/* Tool selector */}
          <div className="p-3 grid grid-cols-2 gap-2 border-b border-slate-100 dark:border-slate-800">
            {[
              { id: "compare", icon: Scale, label: "Compare", active: "border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-md ring-1 ring-blue-300" },
              { id: "substitution", icon: Replace, label: "AI Substitution", active: "border-purple-400 bg-purple-50 dark:bg-purple-900/20 shadow-md ring-1 ring-purple-300" },
              { id: "cbam", icon: Factory, label: "CBAM & ESG", active: "border-amber-400 bg-amber-50 dark:bg-amber-900/20 shadow-md ring-1 ring-amber-300" },
              { id: "synthesizer", icon: Layers, label: "Synthesizer", active: "border-cyan-400 bg-cyan-50 dark:bg-cyan-900/20 shadow-md ring-1 ring-cyan-300" },
            ].map(t => (
              <div key={t.id} className={`p-2 rounded-xl border text-center transition-all flex items-center gap-2 ${phase === t.id ? t.active : "border-slate-200 dark:border-slate-800"}`}>
                <t.icon className={`w-4 h-4 ${phase === t.id ? "text-slate-900 dark:text-white" : "text-slate-400"}`} />
                <span className={`text-[10px] font-bold ${phase === t.id ? "text-slate-900 dark:text-white" : "text-slate-500"}`}>{t.label}</span>
              </div>
            ))}
          </div>

          <div className="p-5 min-h-[280px]">
            <AnimatePresence mode="wait">
              {/* ===== COMPARE ===== */}
              {phase === "compare" && (
                <motion.div key="compare" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
                  {/* Material selectors */}
                  <div className="flex gap-3">
                    <div className={`flex-1 border rounded-xl p-2 flex items-center gap-1.5 transition-all ${step >= 1 && step <= 3 ? "border-blue-400 ring-1 ring-blue-200" : "border-slate-200 dark:border-slate-700"}`}>
                      <Search className="w-3 h-3 text-slate-400" />
                      <span className="text-[10px] font-medium text-slate-700 dark:text-slate-300">{step >= 3 ? "Ti-6Al-4V Grade 5" : step >= 2 ? <span>Titanium<span className="animate-pulse text-blue-500">|</span></span> : <span className="text-slate-400">Material 1...</span>}</span>
                    </div>
                    <div className={`flex-1 border rounded-xl p-2 flex items-center gap-1.5 transition-all ${step === 4 ? "border-blue-400 ring-1 ring-blue-200" : "border-slate-200 dark:border-slate-700"}`}>
                      <Search className="w-3 h-3 text-slate-400" />
                      <span className="text-[10px] font-medium text-slate-700 dark:text-slate-300">{step >= 4 ? "Aluminium 7075-T6" : <span className="text-slate-400">Material 2...</span>}</span>
                    </div>
                  </div>
                  <button className={`w-full py-2 rounded-xl text-xs font-bold text-white ${step >= 5 ? "bg-blue-600 shadow-lg" : "bg-slate-300 dark:bg-slate-700"}`}>{step >= 6 ? "Analysis Complete" : "Run Comparison"}</button>

                  {/* Results */}
                  {step >= 6 && (
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-3">
                      <div className="grid grid-cols-2 gap-3">
                        {/* Radar */}
                        <div className={`p-3 rounded-xl border transition-all ${step === 6 ? "border-blue-400 ring-2 ring-blue-200 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
                          <p className="text-[9px] font-bold text-slate-500 uppercase mb-2 text-center">Property Fingerprint</p>
                          <svg viewBox="0 0 120 120" className="w-full h-24 mx-auto">
                            {/* Grid circles */}
                            <circle cx="60" cy="60" r="45" fill="none" stroke="currentColor" className="text-slate-200 dark:text-slate-700" strokeWidth="0.5"/>
                            <circle cx="60" cy="60" r="30" fill="none" stroke="currentColor" className="text-slate-200 dark:text-slate-700" strokeWidth="0.5"/>
                            <circle cx="60" cy="60" r="15" fill="none" stroke="currentColor" className="text-slate-200 dark:text-slate-700" strokeWidth="0.5"/>
                            {/* Axes */}
                            {[0,60,120,180,240,300].map(a => { const r=45; const x=60+r*Math.cos((a-90)*Math.PI/180); const y=60+r*Math.sin((a-90)*Math.PI/180); return <line key={a} x1="60" y1="60" x2={x} y2={y} stroke="currentColor" className="text-slate-200 dark:text-slate-700" strokeWidth="0.5"/>; })}
                            {/* Labels */}
                            <text x="60" y="8" textAnchor="middle" className="fill-slate-500 text-[6px]">UTS</text>
                            <text x="105" y="35" textAnchor="start" className="fill-slate-500 text-[6px]">Yield</text>
                            <text x="105" y="90" textAnchor="start" className="fill-slate-500 text-[6px]">Cost</text>
                            <text x="60" y="115" textAnchor="middle" className="fill-slate-500 text-[6px]">Density</text>
                            <text x="10" y="90" textAnchor="end" className="fill-slate-500 text-[6px]">Carbon</text>
                            <text x="10" y="35" textAnchor="end" className="fill-slate-500 text-[6px]">Th.K</text>
                            {/* Ti polygon */}
                            <polygon points="60,18 95,40 90,85 60,95 25,80 30,38" fill="rgba(59,130,246,0.15)" stroke="#3b82f6" strokeWidth="1.5"/>
                            {/* Al polygon */}
                            <polygon points="60,25 85,35 98,75 60,100 20,85 22,42" fill="rgba(168,85,247,0.15)" stroke="#a855f7" strokeWidth="1.5"/>
                          </svg>
                          <div className="flex justify-center gap-3 mt-1">
                            <span className="text-[8px] flex items-center gap-1"><span className="w-2 h-2 rounded bg-blue-500"></span>Ti-6Al-4V</span>
                            <span className="text-[8px] flex items-center gap-1"><span className="w-2 h-2 rounded bg-purple-500"></span>Al 7075</span>
                          </div>
                        </div>

                        {/* Comparison matrix */}
                        <div className={`p-3 rounded-xl border transition-all ${step === 7 ? "border-blue-400 ring-2 ring-blue-200 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
                          <p className="text-[9px] font-bold text-slate-500 uppercase mb-2">Comparison Matrix</p>
                          <table className="w-full text-[9px]">
                            <thead><tr className="border-b border-slate-100 dark:border-slate-800">
                              <th className="pb-1 text-left text-slate-400">Property</th>
                              <th className="pb-1 text-blue-500">Ti</th>
                              <th className="pb-1 text-purple-500">Al</th>
                            </tr></thead>
                            <tbody>
                              {[{p:"Density",a:"4.43",b:"2.81",w:"b"},{p:"UTS",a:"950",b:"572",w:"a"},{p:"Yield",a:"880",b:"503",w:"a"},{p:"Cost/kg",a:"$25",b:"$3.2",w:"b"},{p:"Th.K",a:"6.7",b:"130",w:"b"}].map(r=>(
                                <tr key={r.p} className="border-b border-slate-50 dark:border-slate-900">
                                  <td className="py-1 text-slate-500">{r.p}</td>
                                  <td className={`py-1 text-center font-semibold ${r.w==="a"?"text-emerald-600":"text-slate-700 dark:text-slate-300"}`}>{r.a}</td>
                                  <td className={`py-1 text-center font-semibold ${r.w==="b"?"text-emerald-600":"text-slate-700 dark:text-slate-300"}`}>{r.b}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                          <div className={`mt-1.5 flex items-center gap-1 transition-all ${step === 9 ? "ring-1 ring-blue-300 rounded p-0.5" : ""}`}>
                            <Download className="w-3 h-3 text-slate-400" />
                            <span className="text-[8px] text-slate-400">Export CSV</span>
                          </div>
                        </div>
                      </div>

                      {/* Key Takeaways */}
                      <div className={`p-3 rounded-xl border transition-all ${step === 8 ? "border-purple-400 ring-2 ring-purple-200 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
                        <p className="text-[9px] font-bold text-slate-500 uppercase mb-2 flex items-center gap-1"><Info className="w-3 h-3 text-purple-500" /> Automated Insights & Key Takeaways</p>
                        <ul className="space-y-1 text-[10px] text-slate-600 dark:text-slate-400">
                          <li className="flex items-start gap-1.5"><span className="text-blue-500 mt-0.5">•</span> Ti-6Al-4V offers the highest structural integrity (Yield Stress: 880 MPa).</li>
                          <li className="flex items-start gap-1.5"><span className="text-purple-500 mt-0.5">•</span> Aluminium 7075-T6 is the most cost-effective option ($3.2/kg vs $25/kg).</li>
                          <li className="flex items-start gap-1.5"><span className="text-emerald-500 mt-0.5">•</span> Aluminium 7075-T6 is the lightest material (2.81 vs 4.43 g/cm3).</li>
                        </ul>
                      </div>
                    </motion.div>
                  )}
                </motion.div>
              )}

              {/* ===== SUBSTITUTION ===== */}
              {phase === "substitution" && (
                <motion.div key="sub" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
                  <div className={`border rounded-xl p-2 text-xs transition-all ${step===11?"border-purple-400 ring-1 ring-purple-200":"border-slate-200 dark:border-slate-700"}`}>
                    <span className="text-slate-500 text-[10px]">Baseline:</span> <span className="font-semibold text-slate-800 dark:text-white">{step>=11?"ASTM A36 Steel":"Select..."}</span>
                  </div>
                  <div className={`border rounded-xl p-3 transition-all ${step===12?"border-purple-400 ring-1 ring-purple-200":"border-slate-200 dark:border-slate-700"}`}>
                    <p className="text-[10px] font-bold text-slate-500 mb-2">Optimization Weights</p>
                    {[{l:"Cost",v:40,c:"bg-emerald-500"},{l:"Density",v:30,c:"bg-blue-500"},{l:"Carbon",v:30,c:"bg-amber-500"}].map(w=>(
                      <div key={w.l} className="flex items-center gap-2 mb-1">
                        <span className="text-[10px] text-slate-500 w-12">{w.l}</span>
                        <div className="flex-1 h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden"><div className={`h-full ${w.c} rounded-full transition-all`} style={{width:`${step>=12?w.v:0}%`}}></div></div>
                        <span className="text-[10px] font-bold text-slate-700 dark:text-slate-300 w-8">{step>=12?`${w.v}%`:""}</span>
                      </div>
                    ))}
                  </div>
                  <button className={`w-full py-2 rounded-xl text-xs font-bold text-white ${step>=13?"bg-purple-600 shadow-lg":"bg-slate-300 dark:bg-slate-700"}`}>{step>=14?"3 Alternatives Found":"Find Alternatives"}</button>
                  {step >= 14 && (
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-1.5">
                      {[{n:"AISI 1020 Steel",s:"92%"},{n:"S275JR Structural",s:"87%"},{n:"ASTM A572 Grade 50",s:"81%"}].map((r,i)=>(
                        <div key={i} className="flex items-center justify-between p-2 bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
                          <span className="text-[10px] font-bold text-slate-800 dark:text-white">{r.n}</span>
                          <span className="text-[10px] font-bold text-purple-600 bg-purple-100 dark:bg-purple-900/30 px-2 py-0.5 rounded">Fitness: {r.s}</span>
                        </div>
                      ))}
                    </motion.div>
                  )}
                </motion.div>
              )}

              {/* ===== CBAM ===== */}
              {phase === "cbam" && (
                <motion.div key="cbam" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
                  {/* Input method tabs */}
                  <div className={`flex gap-2 transition-all ${step===16?"ring-1 ring-amber-300 rounded-xl p-0.5":""}`}>
                    <div className={`flex-1 p-2 rounded-lg border text-center text-[10px] font-bold transition-all ${step===17?"border-amber-400 bg-amber-50 dark:bg-amber-900/20 ring-1 ring-amber-300 shadow-md":"border-slate-200 dark:border-slate-700 text-slate-500"}`}>
                      <Upload className="w-3 h-3 mx-auto mb-0.5" /> Upload CSV
                    </div>
                    <div className={`flex-1 p-2 rounded-lg border text-center text-[10px] font-bold transition-all ${step===18||step>=19?"border-amber-400 bg-amber-50 dark:bg-amber-900/20 ring-1 ring-amber-300 shadow-md":"border-slate-200 dark:border-slate-700 text-slate-500"}`}>
                      Manual Entry
                    </div>
                  </div>

                  {/* Upload area */}
                  {step === 17 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-4 border-2 border-dashed border-amber-300 rounded-xl text-center bg-amber-50/50 dark:bg-amber-900/10">
                      <Upload className="w-5 h-5 text-amber-500 mx-auto mb-1" />
                      <p className="text-[10px] font-bold text-slate-700 dark:text-slate-300">Drag BOM CSV here</p>
                      <p className="text-[8px] text-slate-400">Must have Material & Weight_kg columns</p>
                    </motion.div>
                  )}

                  {/* Manual entry */}
                  {step >= 18 && step <= 20 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-2">
                      <div className={`border rounded-xl p-2 transition-all ${step===19?"border-amber-400 ring-1 ring-amber-200":"border-slate-200 dark:border-slate-700"}`}>
                        <span className="text-[9px] text-slate-400">Material Name/Grade</span>
                        <p className="text-xs font-semibold text-slate-800 dark:text-white">{step>=19?"Steel 304L":"..."}</p>
                      </div>
                      <div className={`border rounded-xl p-2 transition-all ${step===19?"border-amber-400 ring-1 ring-amber-200":"border-slate-200 dark:border-slate-700"}`}>
                        <span className="text-[9px] text-slate-400">Weight (kg)</span>
                        <p className="text-xs font-semibold text-slate-800 dark:text-white">{step>=19?"500":"..."}</p>
                      </div>
                    </motion.div>
                  )}

                  {step >= 19 && <button className={`w-full py-2 rounded-xl text-xs font-bold text-white flex items-center justify-center gap-2 ${step>=20?"bg-amber-600 shadow-lg":"bg-slate-300 dark:bg-slate-700"}`}><Factory className="w-3 h-3" /> {step>=21?"Analysis Complete":"Calculate CBAM & ESG"}</button>}

                  {/* Results */}
                  {step >= 21 && (
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-2">
                      <div className={`p-3 rounded-xl border transition-all ${step===21?"border-amber-400 ring-2 ring-amber-200 shadow-lg":"border-slate-200 dark:border-slate-700"}`}>
                        <p className="text-[9px] text-slate-500 flex items-center gap-1"><Factory className="w-3 h-3 text-emerald-500" /> Total Embodied Carbon</p>
                        <p className="text-xl font-bold text-slate-900 dark:text-white">925 <span className="text-xs text-slate-400 font-normal">kg CO2</span></p>
                      </div>

                      <div className={`p-3 rounded-xl border transition-all ${step===22?"border-amber-400 ring-2 ring-amber-200 shadow-lg":"border-slate-200 dark:border-slate-700"}`}>
                        <p className="text-[9px] font-bold text-slate-500 uppercase mb-2">Results Breakdown</p>
                        <table className="w-full text-[9px]">
                          <thead><tr className="border-b border-slate-100 dark:border-slate-800">
                            <th className="pb-1 text-left text-slate-400">Material</th>
                            <th className="pb-1 text-slate-400">Weight</th>
                            <th className="pb-1 text-slate-400">Emission</th>
                            <th className="pb-1 text-slate-400">CO2</th>
                            <th className="pb-1 text-slate-400">Risk</th>
                          </tr></thead>
                          <tbody>
                            <tr><td className="py-1 font-semibold text-slate-800 dark:text-white">Steel 304L</td><td className="py-1 text-center">500 kg</td><td className="py-1 text-center">1.85</td><td className="py-1 text-center font-bold">925</td><td className="py-1 text-center"><span className="px-1 py-0.5 rounded bg-emerald-100 text-emerald-700 text-[8px] font-bold">Low</span></td></tr>
                          </tbody>
                        </table>
                        <div className="flex items-center gap-1 mt-2 pt-2 border-t border-slate-100 dark:border-slate-800">
                          <Download className="w-3 h-3 text-slate-400" />
                          <span className="text-[8px] text-slate-400">Export to CSV</span>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </motion.div>
              )}

              {/* ===== SYNTHESIZER ===== */}
              {phase === "synthesizer" && (
                <motion.div key="synth" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
                  <div className={`border rounded-xl p-2.5 transition-all ${step===24?"border-cyan-400 ring-1 ring-cyan-200":"border-slate-200 dark:border-slate-700"}`}>
                    <span className="text-[9px] font-semibold text-cyan-500">Matrix Material (A)</span>
                    <p className="text-xs font-semibold text-slate-800 dark:text-white">{step>=24?"Epoxy Resin":"Search matrix material..."}</p>
                  </div>
                  <div className={`border rounded-xl p-2.5 transition-all ${step===25?"border-teal-400 ring-1 ring-teal-200":"border-slate-200 dark:border-slate-700"}`}>
                    <span className="text-[9px] font-semibold text-teal-500">Reinforcement Material (B)</span>
                    <p className="text-xs font-semibold text-slate-800 dark:text-white">{step>=25?"Carbon Fiber T300":"Search reinforcement material..."}</p>
                  </div>
                  <div className={`border rounded-xl p-3 transition-all ${step===26?"border-cyan-400 ring-1 ring-cyan-200":"border-slate-200 dark:border-slate-700"}`}>
                    <div className="flex justify-between text-[10px] mb-1">
                      <span className="text-slate-500">Volume Fraction (Matrix A)</span>
                      <span className="font-bold text-cyan-500">{step>=26?"40%":"50%"}</span>
                    </div>
                    <div className="h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-cyan-500 to-teal-500 rounded-full transition-all" style={{width:step>=26?"40%":"50%"}}></div>
                    </div>
                    <div className="flex justify-between text-[8px] text-slate-400 mt-1">
                      <span>0% (All Reinforcement)</span>
                      <span>100% (All Matrix)</span>
                    </div>
                  </div>
                  <button className={`w-full py-2 rounded-xl text-xs font-bold text-white ${step>=27?"bg-cyan-600 shadow-lg":"bg-slate-300 dark:bg-slate-700"}`}>{step>=28?"Composite Generated":"Blend Materials"}</button>
                  {step >= 28 && (
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

      {/* Label - Sticky to viewport */}
      <div className="sticky bottom-6 z-40 flex justify-center pointer-events-none mt-4 h-0 overflow-visible">
        <AnimatePresence mode="wait">
          {s.label && (
            <motion.div key={step} initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: -40 }} exit={{ opacity: 0 }}
              className="bg-slate-900 dark:bg-slate-800 text-white text-xs sm:text-sm font-semibold px-5 py-3 rounded-xl shadow-2xl max-w-md text-center border border-slate-700"
            >{s.label}</motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Cursor */}
      <motion.div className="absolute z-50 pointer-events-none" animate={{ x: s.cursor.x, y: s.cursor.y }} transition={{ type: "tween", ease: "easeInOut", duration: 0.5 }}>
        <MousePointer2 className="w-7 h-7 text-black fill-white drop-shadow-xl -rotate-12" />
        {s.click && <motion.div key={step} initial={{ scale: 0, opacity: 0.6 }} animate={{ scale: 2.5, opacity: 0 }} transition={{ duration: 0.5 }} className="absolute top-0 left-0 w-4 h-4 rounded-full bg-blue-500/50" />}
      </motion.div>
    </div>
  );
}
