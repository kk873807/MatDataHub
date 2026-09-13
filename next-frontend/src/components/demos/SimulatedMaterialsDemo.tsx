"use client";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Database, MousePointer2, ExternalLink, ChevronRight } from "lucide-react";

const STEPS = [
  { id: "idle",       duration: 800  },
  { id: "focus",      duration: 600  },
  { id: "type1",      duration: 400  },
  { id: "type2",      duration: 400  },
  { id: "type3",      duration: 400  },
  { id: "results",    duration: 1200 },
  { id: "hover-row",  duration: 800  },
  { id: "click-row",  duration: 600  },
  { id: "detail",     duration: 4000 },
  { id: "reset",      duration: 600  },
];

const cursorPos: Record<string, { x: number; y: number }> = {
  idle:       { x: 420, y: 320 },
  focus:      { x: 140, y: 38  },
  type1:      { x: 140, y: 38  },
  type2:      { x: 140, y: 38  },
  type3:      { x: 140, y: 38  },
  results:    { x: 140, y: 38  },
  "hover-row":{ x: 200, y: 120 },
  "click-row":{ x: 200, y: 120 },
  detail:     { x: 360, y: 260 },
  reset:      { x: 420, y: 320 },
};

const searchText: Record<string, string> = {
  idle: "",
  focus: "",
  type1: "St",
  type2: "Stee",
  type3: "Steel",
  results: "Steel",
  "hover-row": "Steel",
  "click-row": "Steel",
  detail: "Steel",
  reset: "",
};

export function SimulatedMaterialsDemo() {
  const [step, setStep] = useState("idle");
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    let idx = 0;
    const advance = () => {
      if (idx >= STEPS.length) { idx = 0; }
      setStep(STEPS[idx].id);
      timeoutRef.current = setTimeout(() => {
        idx++;
        advance();
      }, STEPS[idx].duration);
    };
    advance();
    return () => { if (timeoutRef.current) clearTimeout(timeoutRef.current); };
  }, []);

  const showResults = ["results", "hover-row", "click-row"].includes(step);
  const showDetail  = step === "detail";
  const hoverRow    = step === "hover-row" || step === "click-row";

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 relative overflow-hidden min-h-[400px]">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

      <div className="relative z-10 w-full max-w-lg mx-auto bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
        <AnimatePresence mode="wait">
          {!showDetail ? (
            <motion.div key="search" initial={{ opacity: 1 }} exit={{ opacity: 0, x: -40 }} className="p-6">
              <h3 className="font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2 text-lg">
                <Database className="w-5 h-5 text-blue-500" /> Material Search
              </h3>

              {/* Search bar */}
              <div className={`border rounded-xl p-3 flex items-center gap-2 mb-4 transition-all ${step !== "idle" && step !== "reset" ? "border-blue-500 ring-2 ring-blue-500/20" : "border-slate-200 dark:border-slate-700"}`}>
                <Search className="w-4 h-4 text-slate-400 shrink-0" />
                <span className="text-sm text-slate-700 dark:text-slate-300 font-medium">
                  {searchText[step] || ""}
                  {(step === "focus" || step.startsWith("type")) && <span className="animate-pulse text-blue-500">|</span>}
                  {!searchText[step] && step === "idle" && <span className="text-slate-400">Search 1000+ materials...</span>}
                </span>
              </div>

              {/* Results */}
              <AnimatePresence>
                {showResults && (
                  <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="space-y-2">
                    <div className={`p-3 rounded-xl border flex items-center justify-between transition-all cursor-pointer ${hoverRow ? "bg-blue-50 dark:bg-blue-900/20 border-blue-300 dark:border-blue-700 shadow-md" : "bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800"}`}>
                      <div>
                        <p className="text-sm font-bold text-slate-900 dark:text-white">AISI 304 Stainless Steel</p>
                        <p className="text-xs text-slate-500">Austenitic &middot; UTS 515 MPa &middot; $2.8/kg</p>
                      </div>
                      <ChevronRight className={`w-4 h-4 transition-colors ${hoverRow ? "text-blue-500" : "text-slate-300"}`} />
                    </div>
                    <div className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 flex items-center justify-between">
                      <div>
                        <p className="text-sm font-bold text-slate-900 dark:text-white">AISI 316L Stainless Steel</p>
                        <p className="text-xs text-slate-500">Marine Grade &middot; UTS 485 MPa &middot; $3.5/kg</p>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-300" />
                    </div>
                    <div className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 flex items-center justify-between">
                      <div>
                        <p className="text-sm font-bold text-slate-900 dark:text-white">Structural Carbon Steel A36</p>
                        <p className="text-xs text-slate-500">Mild &middot; UTS 400 MPa &middot; $0.7/kg</p>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-300" />
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ) : (
            <motion.div key="detail" initial={{ opacity: 0, x: 40 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0 }} className="p-6">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600">
                  <Database className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 dark:text-white text-lg">AISI 304 Stainless Steel</h3>
                  <p className="text-xs text-slate-500">Austenitic &middot; ASTM A240</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3 mb-4">
                {[
                  { label: "Density", value: "8.0 g/cm3" },
                  { label: "Yield Strength", value: "205 MPa" },
                  { label: "UTS", value: "515 MPa" },
                  { label: "Elastic Modulus", value: "193 GPa" },
                  { label: "Thermal Conductivity", value: "16.2 W/mK" },
                  { label: "Cost/kg", value: "$2.80" },
                ].map((p) => (
                  <div key={p.label} className="bg-slate-50 dark:bg-slate-900 rounded-lg p-2">
                    <p className="text-[10px] text-slate-500 uppercase tracking-wide">{p.label}</p>
                    <p className="text-sm font-bold text-slate-900 dark:text-white">{p.value}</p>
                  </div>
                ))}
              </div>

              <div className="pt-3 border-t border-slate-100 dark:border-slate-800">
                <p className="text-xs text-emerald-600 font-semibold flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span> Data Source: Verified Internal Database
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Animated Cursor */}
      <motion.div
        className="absolute z-50 pointer-events-none"
        animate={cursorPos[step] || cursorPos.idle}
        transition={{ type: "tween", ease: "easeInOut", duration: 0.5 }}
      >
        <MousePointer2 className="w-7 h-7 text-black fill-white drop-shadow-xl -rotate-12" />
        {step === "click-row" && (
          <motion.div initial={{ scale: 0, opacity: 1 }} animate={{ scale: 2, opacity: 0 }} transition={{ duration: 0.4 }} className="absolute top-0 left-0 w-4 h-4 rounded-full bg-blue-500/40" />
        )}
      </motion.div>
    </div>
  );
}
