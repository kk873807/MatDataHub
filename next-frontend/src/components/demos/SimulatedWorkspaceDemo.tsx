"use client";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointer2, Workflow, Plus, FolderKanban, ShieldAlert, Thermometer, Activity, AlignEndVertical, IndianRupee, Flame, Wrench, CheckCircle2, Component, Share2, FileText, Lock } from "lucide-react";

interface Step { label: string; cursor: { x: number; y: number }; duration: number; click?: boolean; }

const STEPS: Step[] = [
  // CREATE PROJECT (0-3)
  { label: "Click 'New Workspace' to start a project", cursor: { x: 380, y: 40 }, duration: 1500, click: true },
  { label: "Enter project name: 'Chassis Assembly'", cursor: { x: 250, y: 160 }, duration: 1200 },
  { label: "Enter description: 'Main structural frame'", cursor: { x: 250, y: 210 }, duration: 1200 },
  { label: "Click 'Create Workspace'", cursor: { x: 250, y: 270 }, duration: 1200, click: true },

  // WORKSPACE NAV & STATS (4-6)
  { label: "Builder Nav: Toggle between Standard BOM and Blueprints (JSON)", cursor: { x: 90, y: 140 }, duration: 3000 },
  { label: "Top Nav: Monitor Total Mass and Total Cost in real-time", cursor: { x: 290, y: 40 }, duration: 2500 },
  { label: "Top Nav: Generate a Professional PDF Engineering Report", cursor: { x: 420, y: 40 }, duration: 2500 },

  // ADD BOM COMPONENT (7-11)
  { label: "Click '+' to add a new component to your BOM", cursor: { x: 450, y: 100 }, duration: 1500, click: true },
  { label: "Enter component name: 'Cross Member'", cursor: { x: 290, y: 160 }, duration: 1200 },
  { label: "Assign material from database: AISI 304", cursor: { x: 290, y: 210 }, duration: 1200, click: true },
  { label: "Set quantity and mass: 2 pcs, 4.2 kg each", cursor: { x: 290, y: 260 }, duration: 1200 },
  { label: "Click 'Save' to add to Bill of Materials", cursor: { x: 290, y: 310 }, duration: 1200, click: true },

  // BOM VIEW (12-13)
  { label: "Component added! BOM auto-calculates weight & cost", cursor: { x: 320, y: 200 }, duration: 2200 },
  { label: "Total Mass and Cost update instantly: 20.9 kg, $20.51", cursor: { x: 290, y: 40 }, duration: 2500 },

  // CALCULATORS (14-27)
  { label: "Open Workspace Calculators for structural analysis", cursor: { x: 90, y: 240 }, duration: 2000 },
  // SAFETY FACTOR
  { label: "Calculator 1: Safety Factor — input load & area", cursor: { x: 60, y: 280 }, duration: 1800, click: true },
  { label: "Result: FoS = 2.42 — Component is safe!", cursor: { x: 320, y: 360 }, duration: 2000 },
  // THERMAL EXPANSION
  { label: "Calculator 2: Thermal Expansion — input temps & length", cursor: { x: 120, y: 280 }, duration: 1800, click: true },
  { label: "Result: deltaL = 2.38mm expansion", cursor: { x: 320, y: 360 }, duration: 2000 },
  // FATIGUE
  { label: "Calculator 3: Fatigue Life — stress amplitude input", cursor: { x: 60, y: 340 }, duration: 1800, click: true },
  { label: "Result: 1.2M cycles to failure (S-N curve)", cursor: { x: 320, y: 360 }, duration: 2000 },
  // BEAM DEFLECTION
  { label: "Calculator 4: Beam Deflection — length, load, moment", cursor: { x: 120, y: 340 }, duration: 1800, click: true },
  { label: "Result: max deflection = 0.97mm", cursor: { x: 320, y: 360 }, duration: 2000 },
  // COST OPTIMIZER
  { label: "Calculator 5: Cost Optimizer — finds cheaper alternatives", cursor: { x: 60, y: 400 }, duration: 1800, click: true },
  { label: "Potential savings: $4.20/assembly using AISI 1020", cursor: { x: 320, y: 360 }, duration: 2200 },
  // THERMAL SHOCK
  { label: "Calculator 6: Thermal Shock — survives rapid temp change?", cursor: { x: 120, y: 400 }, duration: 1800, click: true },
  { label: "Result: R = 12.4 — material can withstand thermal shock", cursor: { x: 320, y: 360 }, duration: 2200 },

  // RESET
  { label: "", cursor: { x: 450, y: 450 }, duration: 800 },
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
  
  // UI States
  const showProjectList = step <= 3;
  const showProjectModal = step >= 1 && step <= 3;
  const showWorkspace = step >= 4;
  const showComponentModal = step >= 8 && step <= 11;
  const showSecondRow = step >= 12;
  const activeCalc = step >= 15 && step <= 16 ? "safety" : step >= 17 && step <= 18 ? "thermal" : step >= 19 && step <= 20 ? "fatigue" : step >= 21 && step <= 22 ? "beam" : step >= 23 && step <= 24 ? "cost" : step >= 25 && step <= 26 ? "shock" : null;
  const showCalcResult = [16,18,20,22,24,26].includes(step);
  const calcResultText = step===16 ? "FoS = 2.42 — Safe" : step===18 ? "ΔL = 2.38mm" : step===20 ? "1.2M cycles" : step===22 ? "δ = 0.97mm" : step===24 ? "Save $4.20" : step===26 ? "R = 12.4 — OK" : "";

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 relative overflow-hidden min-h-[500px]">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

      <div className="relative z-10 w-full max-w-lg mx-auto">
        <div className="bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden h-[400px] flex flex-col">
          
          <AnimatePresence mode="wait">
            {showProjectList && (
              <motion.div key="list" exit={{ opacity: 0 }} className="flex-1 p-5 relative">
                <div className="flex justify-between items-center mb-6">
                  <h3 className="font-bold text-slate-900 dark:text-white flex items-center gap-2"><Workflow className="w-5 h-5 text-blue-500" /> Workspaces</h3>
                  <div className={`px-3 py-1.5 rounded-lg bg-blue-600 text-white text-xs font-bold transition-all ${step===0 ? "ring-4 ring-blue-300 scale-110 shadow-lg" : ""}`}>New Workspace</div>
                </div>
                <div className="space-y-3 opacity-50 pointer-events-none">
                  <div className="p-3 border border-slate-200 dark:border-slate-800 rounded-xl bg-slate-50 dark:bg-slate-900">
                    <p className="font-bold text-sm text-slate-800 dark:text-white">Suspension Arm</p>
                    <p className="text-xs text-slate-500 mt-1">2 components · 4.5 kg</p>
                  </div>
                  <div className="p-3 border border-slate-200 dark:border-slate-800 rounded-xl bg-slate-50 dark:bg-slate-900">
                    <p className="font-bold text-sm text-slate-800 dark:text-white">Engine Mount</p>
                    <p className="text-xs text-slate-500 mt-1">5 components · 12.1 kg</p>
                  </div>
                </div>

                {/* Create Project Modal */}
                <AnimatePresence>
                  {showProjectModal && (
                    <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9 }} className="absolute inset-0 bg-white/95 dark:bg-slate-950/95 backdrop-blur-sm p-6 z-20 flex flex-col justify-center">
                      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-5 shadow-xl">
                        <h4 className="font-bold text-slate-900 dark:text-white mb-4">Create New Workspace</h4>
                        <div className="space-y-3">
                          <div>
                            <label className="text-[10px] font-semibold text-slate-500 mb-1 block">Project Name</label>
                            <div className={`p-2 rounded-lg border text-xs ${step>=1?"border-blue-400 ring-1 ring-blue-200":"border-slate-200 dark:border-slate-700"}`}>{step>=1?<span className="text-slate-800 dark:text-white">Chassis Assembly<span className="animate-pulse text-blue-500">|</span></span>:<span className="text-slate-400">e.g. Engine Mount...</span>}</div>
                          </div>
                          <div>
                            <label className="text-[10px] font-semibold text-slate-500 mb-1 block">Description</label>
                            <div className={`p-2 rounded-lg border text-xs ${step>=2?"border-blue-400 ring-1 ring-blue-200":"border-slate-200 dark:border-slate-700"}`}>{step>=2?<span className="text-slate-800 dark:text-white">Main structural frame</span>:<span className="text-slate-400">Optional...</span>}</div>
                          </div>
                          <button className={`w-full py-2.5 rounded-lg text-xs font-bold text-white mt-2 transition-all ${step===3?"bg-blue-700 shadow-lg scale-[0.98]":"bg-blue-600"}`}>Create Workspace</button>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            )}

            {showWorkspace && (
              <motion.div key="workspace" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col h-full">
                {/* Workspace Top Nav */}
                <div className="px-4 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900/50">
                  <div className="flex items-center gap-2">
                    <Workflow className="w-4 h-4 text-blue-500" />
                    <span className="text-sm font-bold text-slate-900 dark:text-white">Chassis Assembly</span>
                  </div>
                  <div className="flex items-center gap-3 text-right">
                    <div className={`transition-all ${step===5||step===13?"ring-2 ring-emerald-300 rounded p-0.5 bg-emerald-50 dark:bg-emerald-900/20":""}`}>
                      <p className="text-[8px] uppercase tracking-wider text-slate-500 font-bold">Total Mass</p>
                      <p className={`text-[11px] font-bold ${step>=13?"text-slate-900 dark:text-white":"text-slate-600 dark:text-slate-400"}`}>{step>=13?"20.90":"12.50"} kg</p>
                    </div>
                    <div className={`transition-all ${step===5||step===13?"ring-2 ring-emerald-300 rounded p-0.5 bg-emerald-50 dark:bg-emerald-900/20":""}`}>
                      <p className="text-[8px] uppercase tracking-wider text-slate-500 font-bold">Total Cost</p>
                      <p className={`text-[11px] font-bold ${step>=13?"text-emerald-600":"text-emerald-500/70"}`}>&#8377;{step>=13?"20.51":"8.75"}</p>
                    </div>
                    <div className={`flex items-center gap-1 px-2 py-1.5 rounded-lg border text-[9px] font-bold transition-all ${step===6?"border-blue-400 bg-blue-50 dark:bg-blue-900/20 ring-2 ring-blue-300 shadow-md text-blue-700":"border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-800"}`}>
                      <FileText className="w-3 h-3" /> Report
                    </div>
                  </div>
                </div>

                <div className="flex flex-1 overflow-hidden">
                  {/* Sidebar Nav */}
                  <div className="w-1/3 border-r border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/30 p-3 overflow-y-auto">
                    <p className="text-[9px] uppercase tracking-wider text-slate-400 font-bold mb-2">Builder</p>
                    <div className="space-y-1 mb-4">
                      <div className={`flex items-center gap-1.5 p-2 rounded-lg text-[10px] font-medium transition-all ${step===4||activeCalc===null?"bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 border border-blue-200 dark:border-blue-800":"text-slate-500 border border-transparent"}`}>
                        <Component className="w-3.5 h-3.5" /> Standard BOM
                      </div>
                      <div className={`flex items-center gap-1.5 p-2 rounded-lg text-[10px] font-medium transition-all ${step===4?"ring-1 ring-violet-300 bg-violet-50 dark:bg-violet-900/20 text-violet-700 dark:text-violet-400":"text-slate-500 border border-transparent"}`}>
                        <Share2 className="w-3.5 h-3.5" /> Blueprints
                      </div>
                    </div>

                    <p className={`text-[9px] uppercase tracking-wider text-slate-400 font-bold mb-2 transition-all ${step===14?"text-blue-500":""}`}>Calculators</p>
                    <div className="grid grid-cols-2 gap-1.5">
                      {[
                        { id: "safety",  icon: ShieldAlert,     label: "Safety",   c: "rose" },
                        { id: "thermal", icon: Thermometer,      label: "Thermal",  c: "orange" },
                        { id: "fatigue", icon: Activity,         label: "Fatigue",  c: "blue" },
                        { id: "beam",    icon: AlignEndVertical, label: "Beam",     c: "indigo" },
                        { id: "cost",    icon: IndianRupee,      label: "Cost Opt", c: "emerald" },
                        { id: "shock",   icon: Flame,            label: "Th.Shock", c: "red" },
                      ].map(calc => (
                        <div key={calc.id} className={`p-2 rounded-lg border text-center transition-all ${activeCalc === calc.id ? `border-${calc.c}-400 bg-${calc.c}-50 dark:bg-${calc.c}-900/20 shadow-md ring-1 ring-${calc.c}-300 scale-[1.05]` : "border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950"}`}>
                          <calc.icon className={`w-3.5 h-3.5 mx-auto mb-0.5 ${activeCalc === calc.id ? `text-${calc.c}-600` : "text-slate-400"}`} />
                          <p className={`text-[8px] font-bold ${activeCalc === calc.id ? `text-${calc.c}-700 dark:text-${calc.c}-400` : "text-slate-500"}`}>{calc.label}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Main Content Area */}
                  <div className="w-2/3 p-4 relative bg-white dark:bg-slate-950">
                    
                    {/* BOM Table View */}
                    <AnimatePresence>
                      {activeCalc === null && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="h-full flex flex-col">
                          <div className="flex justify-between items-center mb-3">
                            <h4 className="font-bold text-slate-900 dark:text-white text-xs">Bill of Materials</h4>
                            <div className={`p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 transition-all ${step===7?"ring-2 ring-blue-400 bg-blue-100 dark:bg-blue-900/30 shadow-md scale-110":""}`}><Plus className="w-3 h-3 text-blue-600" /></div>
                          </div>
                          <div className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden text-[9px]">
                            <table className="w-full text-left">
                              <thead className="bg-slate-50 dark:bg-slate-900">
                                <tr><th className="p-2 text-slate-500">Component</th><th className="p-2 text-slate-500">Material</th><th className="p-2 text-slate-500">Mass</th></tr>
                              </thead>
                              <tbody>
                                <tr className="border-t border-slate-100 dark:border-slate-800">
                                  <td className="p-2 font-semibold text-slate-800 dark:text-slate-200">Frame Rail</td>
                                  <td className="p-2 text-slate-600 dark:text-slate-400">A36 Steel</td>
                                  <td className="p-2">12.5 kg</td>
                                </tr>
                                <AnimatePresence>
                                  {showSecondRow && (
                                    <motion.tr initial={{ opacity: 0, backgroundColor: "rgba(59,130,246,0.1)" }} animate={{ opacity: 1, backgroundColor: "transparent" }} className="border-t border-slate-100 dark:border-slate-800">
                                      <td className="p-2 font-semibold text-slate-800 dark:text-slate-200">Cross Member</td>
                                      <td className="p-2 text-slate-600 dark:text-slate-400">AISI 304</td>
                                      <td className="p-2">8.4 kg</td>
                                    </motion.tr>
                                  )}
                                </AnimatePresence>
                              </tbody>
                            </table>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>

                    {/* Calculator Detail View */}
                    <AnimatePresence>
                      {activeCalc !== null && (
                        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="h-full flex flex-col justify-center">
                          <div className="text-center mb-4">
                            <Wrench className="w-6 h-6 text-slate-400 mx-auto mb-2" />
                            <h4 className="font-bold text-slate-800 dark:text-white text-sm">Engineering Calculator</h4>
                            <p className="text-[10px] text-slate-500">Computing properties...</p>
                          </div>
                          
                          <AnimatePresence>
                            {showCalcResult && (
                              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="p-3 bg-emerald-50 dark:bg-emerald-900/20 rounded-xl border border-emerald-200 dark:border-emerald-800 text-center shadow-md">
                                <CheckCircle2 className="w-5 h-5 text-emerald-500 mx-auto mb-1" />
                                <p className="text-xs font-bold text-emerald-700 dark:text-emerald-400">{calcResultText}</p>
                              </motion.div>
                            )}
                          </AnimatePresence>
                        </motion.div>
                      )}
                    </AnimatePresence>

                    {/* Add Component Modal */}
                    <AnimatePresence>
                      {showComponentModal && (
                        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, scale: 0.95 }} className="absolute inset-0 bg-white/95 dark:bg-slate-950/95 backdrop-blur-sm p-4 z-20 flex flex-col justify-center">
                          <h4 className="font-bold text-slate-900 dark:text-white mb-3 text-xs">Add Component</h4>
                          <div className="space-y-2">
                            <div>
                              <label className="text-[9px] font-semibold text-slate-500 mb-0.5 block">Component Name</label>
                              <div className={`p-1.5 rounded-lg border text-[10px] ${step>=8?"border-blue-400 ring-1 ring-blue-200":"border-slate-200 dark:border-slate-700"}`}>{step>=8?<span className="text-slate-800 dark:text-white">Cross Member</span>:<span className="text-slate-400">Name...</span>}</div>
                            </div>
                            <div>
                              <label className="text-[9px] font-semibold text-slate-500 mb-0.5 block">Material</label>
                              <div className={`p-1.5 rounded-lg border text-[10px] ${step>=9?"border-blue-400 ring-1 ring-blue-200":"border-slate-200 dark:border-slate-700"}`}>{step>=9?<span className="text-slate-800 dark:text-white">AISI 304</span>:<span className="text-slate-400">Select...</span>}</div>
                            </div>
                            <div>
                              <label className="text-[9px] font-semibold text-slate-500 mb-0.5 block">Quantity & Mass</label>
                              <div className={`p-1.5 rounded-lg border text-[10px] ${step>=10?"border-blue-400 ring-1 ring-blue-200":"border-slate-200 dark:border-slate-700"}`}>{step>=10?<span className="text-slate-800 dark:text-white">2 pcs × 4.2 kg</span>:<span className="text-slate-400">Qty & kg...</span>}</div>
                            </div>
                            <button className={`w-full py-2 rounded-lg text-[10px] font-bold text-white mt-1 transition-all ${step===11?"bg-blue-700 shadow-md scale-[0.98]":"bg-blue-600"}`}>Save</button>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>

                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
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
