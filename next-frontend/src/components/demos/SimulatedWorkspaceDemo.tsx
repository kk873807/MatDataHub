"use client";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointer2, Workflow, Plus, FolderKanban, ShieldAlert, Thermometer, Activity, AlignEndVertical, IndianRupee, Flame, Wrench, CheckCircle2 } from "lucide-react";

interface Step { label: string; cursor: { x: number; y: number }; duration: number; click?: boolean; }

const STEPS: Step[] = [
  // CREATE PROJECT
  { label: "Click '+' to add a new component to your BOM", cursor: { x: 420, y: 40 }, duration: 1500, click: true },
  // MODAL
  { label: "Enter component name: 'Cross Member'", cursor: { x: 240, y: 120 }, duration: 1500 },
  { label: "Assign material from database: AISI 304", cursor: { x: 240, y: 170 }, duration: 1500, click: true },
  { label: "Set quantity and mass: 2 pcs, 4.2 kg each", cursor: { x: 240, y: 210 }, duration: 1500 },
  { label: "Click 'Save' to add to Bill of Materials", cursor: { x: 240, y: 260 }, duration: 1200, click: true },
  // BOM VIEW
  { label: "Component added! BOM auto-calculates weight & cost", cursor: { x: 300, y: 165 }, duration: 2200 },
  { label: "Total assembly: 16.7 kg, $20.51 — updates in real-time", cursor: { x: 300, y: 200 }, duration: 2200 },
  // CALCULATORS
  { label: "Open Workspace Calculators for structural analysis", cursor: { x: 200, y: 240 }, duration: 1500, click: true },
  // SAFETY FACTOR
  { label: "Calculator 1: Safety Factor — input load & area", cursor: { x: 85, y: 290 }, duration: 1800, click: true },
  { label: "Applied Load: 85,000 N | Area: 450 mm2", cursor: { x: 240, y: 310 }, duration: 1500 },
  { label: "Result: FoS = 2.42 — Component is safe!", cursor: { x: 240, y: 350 }, duration: 2000 },
  // THERMAL EXPANSION
  { label: "Calculator 2: Thermal Expansion — input temps & length", cursor: { x: 175, y: 290 }, duration: 1800, click: true },
  { label: "Length: 500mm, from 20C to 300C", cursor: { x: 240, y: 310 }, duration: 1500 },
  { label: "Result: deltaL = 2.38mm expansion", cursor: { x: 240, y: 350 }, duration: 2000 },
  // FATIGUE
  { label: "Calculator 3: Fatigue Life — stress amplitude input", cursor: { x: 265, y: 290 }, duration: 1800, click: true },
  { label: "Stress amplitude: 200 MPa cyclic loading", cursor: { x: 240, y: 310 }, duration: 1500 },
  { label: "Result: 1.2M cycles to failure (S-N curve)", cursor: { x: 240, y: 350 }, duration: 2000 },
  // BEAM DEFLECTION
  { label: "Calculator 4: Beam Deflection — length, load, moment", cursor: { x: 355, y: 290 }, duration: 1800, click: true },
  { label: "Beam: 1000mm, 5kN point load, I = 84.0 cm4", cursor: { x: 240, y: 310 }, duration: 1500 },
  { label: "Result: max deflection = 0.97mm", cursor: { x: 240, y: 350 }, duration: 2000 },
  // COST OPTIMIZER
  { label: "Calculator 5: Cost Optimizer — finds cheaper alternatives", cursor: { x: 85, y: 350 }, duration: 1800, click: true },
  { label: "Scanning database for materials with similar properties...", cursor: { x: 240, y: 370 }, duration: 1500 },
  { label: "Potential savings: $4.20/assembly using AISI 1020", cursor: { x: 240, y: 390 }, duration: 2200 },
  // THERMAL SHOCK
  { label: "Calculator 6: Thermal Shock — survives rapid temp change?", cursor: { x: 175, y: 350 }, duration: 1800, click: true },
  { label: "Temperature differential: 500C, heat transfer coeff: 200", cursor: { x: 240, y: 370 }, duration: 1500 },
  { label: "Result: R = 12.4 — material can withstand thermal shock", cursor: { x: 240, y: 390 }, duration: 2200 },
  // RESET
  { label: "", cursor: { x: 450, y: 400 }, duration: 800 },
];

export function SimulatedWorkspaceDemo() {
  const [step, setStep] = useState(0);
  const ref = useRef<NodeJS.Timeout | null>(null);
  useEffect(() => {
    let i = 0;
    const go = () => { if (i >= STEPS.length) i = 0; setStep(i); ref.current = setTimeout(() => { i++; go(); }, STEPS[i].duration); };
    go();
    return () => { if (ref.current) clearTimeout(ref.current); };
  }, []);

  const s = STEPS[step];
  const showModal = step >= 1 && step <= 4;
  const showBOM = step >= 5;
  const showCalcs = step >= 7;
  const activeCalc = step >= 8 && step <= 10 ? "safety" : step >= 11 && step <= 13 ? "thermal" : step >= 14 && step <= 16 ? "fatigue" : step >= 17 && step <= 19 ? "beam" : step >= 20 && step <= 22 ? "cost" : step >= 23 && step <= 25 ? "shock" : null;
  const showResult = [10,13,16,19,22,25].includes(step);
  const resultText = step===10 ? "FoS = 2.42 — Safe" : step===13 ? "ΔL = 2.38mm" : step===16 ? "1.2M cycles" : step===19 ? "δ = 0.97mm" : step===22 ? "Save $4.20" : step===25 ? "R = 12.4 — OK" : "";

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 relative overflow-hidden min-h-[440px]">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

      <div className="relative z-10 w-full max-w-lg mx-auto">
        <div className="bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="px-5 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-2"><Workflow className="w-4 h-4 text-violet-500" /><span className="text-sm font-bold text-slate-900 dark:text-white">Chassis Assembly</span></div>
            <div className={`p-1.5 rounded-lg transition-all ${step===0?"bg-violet-100 dark:bg-violet-900/30 ring-2 ring-violet-400 shadow-lg scale-110":"bg-slate-100 dark:bg-slate-800"}`}><Plus className="w-3.5 h-3.5 text-violet-600" /></div>
          </div>

          <div className="p-4 min-h-[340px] relative">
            {/* Modal overlay */}
            <AnimatePresence>
              {showModal && (
                <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9 }} className="absolute inset-0 bg-white/95 dark:bg-slate-950/95 backdrop-blur-sm p-5 z-20 rounded-b-2xl flex flex-col">
                  <h4 className="font-bold text-slate-900 dark:text-white mb-4 text-sm">Add Component</h4>
                  <div className="space-y-3 flex-1">
                    <div>
                      <label className="text-[10px] font-semibold text-slate-500 mb-1 block">Component Name</label>
                      <div className={`p-2 rounded-lg border text-xs ${step>=1?"border-violet-400 ring-1 ring-violet-200":"border-slate-200 dark:border-slate-700"}`}>{step>=1?<span className="text-slate-800 dark:text-white">Cross Member<span className="animate-pulse text-violet-500">|</span></span>:<span className="text-slate-400">Enter name...</span>}</div>
                    </div>
                    <div>
                      <label className="text-[10px] font-semibold text-slate-500 mb-1 block">Material</label>
                      <div className={`p-2 rounded-lg border text-xs ${step>=2?"border-violet-400 ring-1 ring-violet-200":"border-slate-200 dark:border-slate-700"}`}>{step>=2?<span className="text-slate-800 dark:text-white">AISI 304 Stainless Steel</span>:<span className="text-slate-400">Select material...</span>}</div>
                    </div>
                    <div>
                      <label className="text-[10px] font-semibold text-slate-500 mb-1 block">Quantity & Mass</label>
                      <div className={`p-2 rounded-lg border text-xs ${step>=3?"border-violet-400 ring-1 ring-violet-200":"border-slate-200 dark:border-slate-700"}`}>{step>=3?<span className="text-slate-800 dark:text-white">2 pcs × 4.2 kg</span>:<span className="text-slate-400">Qty & kg...</span>}</div>
                    </div>
                  </div>
                  <button className={`w-full py-2.5 rounded-xl text-xs font-bold text-white mt-3 transition-all ${step===4?"bg-violet-600 shadow-lg scale-[0.97]":"bg-violet-500"}`}>Save Component</button>
                </motion.div>
              )}
            </AnimatePresence>

            {/* BOM content */}
            {!showModal && (
              <>
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1"><FolderKanban className="w-3 h-3" /> Bill of Materials</p>
                <div className="space-y-1.5 mb-3">
                  <div className="p-2 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2"><span className="w-5 h-5 rounded bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-[10px] font-bold text-blue-600">1</span><span className="font-semibold text-slate-900 dark:text-white">Frame Rail</span><span className="text-slate-400">A36</span></div>
                    <span className="text-slate-500">12.5 kg · $8.75</span>
                  </div>
                  <AnimatePresence>
                    {showBOM && (
                      <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="p-2 rounded-lg bg-violet-50 dark:bg-violet-900/10 border-2 border-violet-300 dark:border-violet-700 flex items-center justify-between text-xs">
                        <div className="flex items-center gap-2"><span className="w-5 h-5 rounded bg-violet-100 dark:bg-violet-900/30 flex items-center justify-center text-[10px] font-bold text-violet-600">2</span><span className="font-semibold text-slate-900 dark:text-white">Cross Member</span><span className="text-slate-400">304</span></div>
                        <span className="text-violet-600 font-semibold">8.4 kg · $11.76</span>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>

                {/* Rollup */}
                {showBOM && (
                  <div className="p-2 rounded-lg bg-gradient-to-r from-blue-50 to-violet-50 dark:from-blue-900/10 dark:to-violet-900/10 border border-blue-200 dark:border-blue-800 mb-3 flex justify-between text-xs">
                    <span className="font-bold text-blue-700 dark:text-blue-400">Total: 20.9 kg</span>
                    <span className="font-bold text-violet-700 dark:text-violet-400">Cost: $20.51</span>
                  </div>
                )}

                {/* Calculator section */}
                {showCalcs && (
                  <>
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1"><Wrench className="w-3 h-3" /> Calculators</p>
                    <div className="grid grid-cols-3 gap-1.5 mb-3">
                      {[
                        { id: "safety",  icon: ShieldAlert,     label: "Safety",   c: "rose" },
                        { id: "thermal", icon: Thermometer,      label: "Thermal",  c: "orange" },
                        { id: "fatigue", icon: Activity,         label: "Fatigue",  c: "blue" },
                        { id: "beam",    icon: AlignEndVertical, label: "Beam",     c: "indigo" },
                        { id: "cost",    icon: IndianRupee,      label: "Cost Opt", c: "emerald" },
                        { id: "shock",   icon: Flame,            label: "Th.Shock", c: "red" },
                      ].map(calc => (
                        <div key={calc.id} className={`p-2 rounded-lg border text-center transition-all ${activeCalc === calc.id ? `border-${calc.c}-400 bg-${calc.c}-50 dark:bg-${calc.c}-900/20 shadow-md ring-1 ring-${calc.c}-300 scale-[1.06]` : "border-slate-200 dark:border-slate-800"}`}>
                          <calc.icon className={`w-3.5 h-3.5 mx-auto mb-0.5 ${activeCalc === calc.id ? `text-${calc.c}-600` : "text-slate-400"}`} />
                          <p className="text-[9px] font-bold text-slate-700 dark:text-slate-300">{calc.label}</p>
                        </div>
                      ))}
                    </div>
                    {/* Result */}
                    <AnimatePresence>
                      {showResult && (
                        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="p-2.5 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg border border-emerald-200 dark:border-emerald-700 flex items-center gap-2">
                          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                          <span className="text-xs font-bold text-emerald-700 dark:text-emerald-400">{resultText}</span>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </>
                )}
              </>
            )}
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
        {s.click && <motion.div key={step} initial={{ scale: 0, opacity: 0.6 }} animate={{ scale: 2.5, opacity: 0 }} transition={{ duration: 0.5 }} className="absolute top-0 left-0 w-4 h-4 rounded-full bg-violet-500/50" />}
      </motion.div>
    </div>
  );
}
