"use client";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointer2, Workflow, Plus, Wrench, ShieldAlert, CheckCircle2 } from "lucide-react";

const STEPS = [
  { id: "idle",           duration: 800  },
  { id: "click-add",      duration: 800  },
  { id: "modal-open",     duration: 600  },
  { id: "type-name",      duration: 600  },
  { id: "type-material",  duration: 600  },
  { id: "click-save",     duration: 800  },
  { id: "bom-added",      duration: 1200 },
  { id: "click-calc",     duration: 800  },
  { id: "calc-open",      duration: 600  },
  { id: "fill-load",      duration: 600  },
  { id: "click-run",      duration: 800  },
  { id: "result",         duration: 3500 },
  { id: "reset",          duration: 600  },
];

const cursorPos: Record<string, { x: number; y: number }> = {
  idle:          { x: 420, y: 320 },
  "click-add":   { x: 400, y: 40  },
  "modal-open":  { x: 200, y: 120 },
  "type-name":   { x: 200, y: 120 },
  "type-material":{ x: 200, y: 170 },
  "click-save":  { x: 250, y: 230 },
  "bom-added":   { x: 250, y: 160 },
  "click-calc":  { x: 100, y: 300 },
  "calc-open":   { x: 200, y: 200 },
  "fill-load":   { x: 200, y: 200 },
  "click-run":   { x: 250, y: 270 },
  result:        { x: 300, y: 260 },
  reset:         { x: 420, y: 320 },
};

export function SimulatedWorkspaceDemo() {
  const [step, setStep] = useState("idle");
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    let idx = 0;
    const advance = () => {
      if (idx >= STEPS.length) { idx = 0; }
      setStep(STEPS[idx].id);
      timeoutRef.current = setTimeout(() => { idx++; advance(); }, STEPS[idx].duration);
    };
    advance();
    return () => { if (timeoutRef.current) clearTimeout(timeoutRef.current); };
  }, []);

  const stepIdx = STEPS.findIndex(s => s.id === step);
  const showModal   = stepIdx >= 2 && stepIdx <= 5;
  const showBOM     = stepIdx >= 6;
  const showCalcUI  = stepIdx >= 8 && stepIdx <= 11;
  const showResult  = stepIdx === 11;

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 relative overflow-hidden min-h-[400px]">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

      <div className="relative z-10 w-full max-w-lg mx-auto bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
        {/* Header bar */}
        <div className="px-6 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <h3 className="font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Workflow className="w-5 h-5 text-violet-500" /> Chassis Assembly
          </h3>
          <button className={`p-2 rounded-xl transition-all ${step === "click-add" ? "bg-violet-100 dark:bg-violet-900/30 ring-2 ring-violet-400 scale-110" : "bg-slate-100 dark:bg-slate-800"}`}>
            <Plus className="w-4 h-4 text-violet-600" />
          </button>
        </div>

        <div className="p-6 min-h-[280px] relative">
          {/* BOM table (always visible after step 6) */}
          {!showModal && (
            <div className="space-y-3">
              {/* Existing row */}
              <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-xs font-bold text-blue-600">1</div>
                  <div>
                    <p className="text-sm font-bold text-slate-900 dark:text-white">Frame Rail</p>
                    <p className="text-xs text-slate-500">ASTM A36 &middot; 12.5 kg</p>
                  </div>
                </div>
                <p className="text-xs font-semibold text-slate-600 dark:text-slate-400">$8.75</p>
              </div>

              {/* Newly added row (appears after bom-added) */}
              <AnimatePresence>
                {showBOM && (
                  <motion.div initial={{ opacity: 0, height: 0, y: -10 }} animate={{ opacity: 1, height: "auto", y: 0 }} className="p-3 rounded-xl bg-violet-50 dark:bg-violet-900/10 border-2 border-violet-300 dark:border-violet-700 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-violet-100 dark:bg-violet-900/30 flex items-center justify-center text-xs font-bold text-violet-600">2</div>
                      <div>
                        <p className="text-sm font-bold text-slate-900 dark:text-white">Cross Member</p>
                        <p className="text-xs text-slate-500">AISI 304 &middot; 4.2 kg</p>
                      </div>
                    </div>
                    <p className="text-xs font-semibold text-violet-600">$11.76</p>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Calculator section */}
              {showBOM && (
                <div className="pt-4 mt-4 border-t border-slate-100 dark:border-slate-800">
                  <div className={`flex items-center gap-2 p-3 rounded-xl transition-all cursor-pointer ${step === "click-calc" ? "bg-amber-50 dark:bg-amber-900/20 border-2 border-amber-400 shadow-md" : "bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800"}`}>
                    <Wrench className="w-4 h-4 text-amber-600" />
                    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">Workspace Tools</span>
                  </div>

                  {/* Calculator UI */}
                  <AnimatePresence>
                    {showCalcUI && (
                      <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} className="mt-3 p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">
                        <div className="flex items-center gap-2 mb-3">
                          <ShieldAlert className="w-4 h-4 text-rose-500" />
                          <span className="text-sm font-bold text-slate-900 dark:text-white">Safety Factor Calculator</span>
                        </div>
                        <div className="space-y-2 mb-3">
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-slate-500 w-20">Applied Load</span>
                            <div className={`flex-1 p-2 rounded-lg border text-xs font-mono ${stepIdx >= 9 ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20" : "border-slate-200 dark:border-slate-700"}`}>
                              {stepIdx >= 9 ? "85,000 N" : ""}
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-slate-500 w-20">Area (mm2)</span>
                            <div className={`flex-1 p-2 rounded-lg border text-xs font-mono ${stepIdx >= 9 ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20" : "border-slate-200 dark:border-slate-700"}`}>
                              {stepIdx >= 9 ? "450" : ""}
                            </div>
                          </div>
                        </div>
                        <button className={`w-full py-2 rounded-lg text-xs font-bold text-white ${stepIdx >= 10 ? "bg-rose-500 shadow-lg" : "bg-slate-400"}`}>
                          {stepIdx >= 10 ? "Calculating..." : "Run Calculation"}
                        </button>
                        
                        {/* Result */}
                        <AnimatePresence>
                          {showResult && (
                            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-3 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-700">
                              <div className="flex items-center gap-2">
                                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                                <span className="text-sm font-bold text-emerald-700 dark:text-emerald-400">Safety Factor: 2.42</span>
                              </div>
                              <p className="text-xs text-emerald-600 mt-1">Component is safe. FoS &gt; 2.0 meets aerospace standards.</p>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              )}
            </div>
          )}

          {/* Add Component Modal overlay */}
          <AnimatePresence>
            {showModal && (
              <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9 }} className="absolute inset-0 bg-white/95 dark:bg-slate-950/95 backdrop-blur-sm p-6 flex flex-col rounded-b-2xl z-20">
                <h4 className="font-bold text-slate-900 dark:text-white mb-4">Add Component</h4>
                <div className="space-y-3 flex-1">
                  <div>
                    <label className="text-xs font-semibold text-slate-500 mb-1 block">Component Name</label>
                    <div className={`p-2.5 rounded-lg border text-sm ${stepIdx >= 3 ? "border-violet-400 ring-1 ring-violet-300" : "border-slate-200 dark:border-slate-700"}`}>
                      {stepIdx >= 3 ? <span className="text-slate-800 dark:text-slate-200">Cross Member<span className="animate-pulse text-violet-500">|</span></span> : <span className="text-slate-400">Enter name...</span>}
                    </div>
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-slate-500 mb-1 block">Material</label>
                    <div className={`p-2.5 rounded-lg border text-sm ${stepIdx >= 4 ? "border-violet-400 ring-1 ring-violet-300" : "border-slate-200 dark:border-slate-700"}`}>
                      {stepIdx >= 4 ? <span className="text-slate-800 dark:text-slate-200">AISI 304 Stainless Steel</span> : <span className="text-slate-400">Select material...</span>}
                    </div>
                  </div>
                </div>
                <button className={`w-full py-3 rounded-xl font-bold text-white mt-4 transition-all ${step === "click-save" ? "bg-violet-600 shadow-lg scale-[0.97]" : "bg-violet-500"}`}>
                  Save Component
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Animated Cursor */}
      <motion.div
        className="absolute z-50 pointer-events-none"
        animate={cursorPos[step] || cursorPos.idle}
        transition={{ type: "tween", ease: "easeInOut", duration: 0.5 }}
      >
        <MousePointer2 className="w-7 h-7 text-black fill-white drop-shadow-xl -rotate-12" />
        {(step === "click-add" || step === "click-save" || step === "click-calc" || step === "click-run") && (
          <motion.div initial={{ scale: 0, opacity: 1 }} animate={{ scale: 2, opacity: 0 }} transition={{ duration: 0.4 }} className="absolute top-0 left-0 w-4 h-4 rounded-full bg-violet-500/40" />
        )}
      </motion.div>
    </div>
  );
}
