"use client";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointer2, LayoutDashboard, Search, Plus, Database, BarChart3, Workflow } from "lucide-react";

const STEPS = [
  { id: "idle",           duration: 1000 },
  { id: "hover-search",   duration: 1200 },
  { id: "hover-workspace", duration: 1200 },
  { id: "hover-material", duration: 1200 },
  { id: "hover-cbam",     duration: 1200 },
  { id: "hover-compare",  duration: 1200 },
  { id: "hover-recent",   duration: 1500 },
  { id: "reset",          duration: 800  },
];

const cursorPos: Record<string, { x: number; y: number }> = {
  idle:              { x: 430, y: 300 },
  "hover-search":    { x: 100, y: 52  },
  "hover-workspace": { x: 260, y: 52  },
  "hover-material":  { x: 80,  y: 155 },
  "hover-cbam":      { x: 240, y: 155 },
  "hover-compare":   { x: 400, y: 155 },
  "hover-recent":    { x: 200, y: 260 },
  reset:             { x: 430, y: 300 },
};

const tooltips: Record<string, { text: string; pos: { x: number; y: number } }> = {
  "hover-search":    { text: "Search 1000+ verified materials instantly", pos: { x: 100, y: 80 } },
  "hover-workspace": { text: "Create engineering projects with BOM tracking", pos: { x: 220, y: 80 } },
  "hover-material":  { text: "Browse full database with advanced filters", pos: { x: 80, y: 185 } },
  "hover-cbam":      { text: "Calculate EU Carbon Border Adjustment taxes", pos: { x: 210, y: 185 } },
  "hover-compare":   { text: "Radar chart comparison of material properties", pos: { x: 350, y: 185 } },
  "hover-recent":    { text: "Your recent workspaces appear here", pos: { x: 200, y: 288 } },
};

export function SimulatedDashboardDemo() {
  const [step, setStep] = useState("idle");
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    let idx = 0;
    const advance = () => {
      if (idx >= STEPS.length) idx = 0;
      setStep(STEPS[idx].id);
      timeoutRef.current = setTimeout(() => { idx++; advance(); }, STEPS[idx].duration);
    };
    advance();
    return () => { if (timeoutRef.current) clearTimeout(timeoutRef.current); };
  }, []);

  const activeTooltip = tooltips[step];

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 relative overflow-hidden min-h-[340px]">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

      <div className="relative z-10 w-full max-w-lg mx-auto bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
        {/* Top bar */}
        <div className="px-5 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <LayoutDashboard className="w-4 h-4 text-blue-500" />
            <span className="text-sm font-bold text-slate-900 dark:text-white">Welcome, Engineer</span>
          </div>
          <span className="text-xs text-slate-400">Dashboard</span>
        </div>

        <div className="p-5">
          {/* Quick action buttons */}
          <div className="flex gap-3 mb-5">
            <div className={`flex-1 flex items-center gap-2 px-3 py-2.5 rounded-xl border text-xs font-semibold transition-all ${step === "hover-search" ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-md scale-[1.03]" : "border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900"}`}>
              <Search className="w-3.5 h-3.5 text-blue-500" />
              <span className="text-slate-700 dark:text-slate-300">Browse Database</span>
            </div>
            <div className={`flex-1 flex items-center gap-2 px-3 py-2.5 rounded-xl border text-xs font-semibold transition-all ${step === "hover-workspace" ? "border-violet-400 bg-violet-50 dark:bg-violet-900/20 shadow-md scale-[1.03]" : "border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900"}`}>
              <Plus className="w-3.5 h-3.5 text-violet-500" />
              <span className="text-slate-700 dark:text-slate-300">New Workspace</span>
            </div>
          </div>

          {/* Quick Actions grid */}
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Quick Actions</p>
          <div className="grid grid-cols-3 gap-2 mb-5">
            <div className={`p-3 rounded-xl border text-center transition-all ${step === "hover-material" ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-md scale-[1.05]" : "border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900"}`}>
              <Database className="w-4 h-4 text-blue-500 mx-auto mb-1" />
              <p className="text-[10px] font-bold text-slate-700 dark:text-slate-300">Materials</p>
            </div>
            <div className={`p-3 rounded-xl border text-center transition-all ${step === "hover-cbam" ? "border-amber-400 bg-amber-50 dark:bg-amber-900/20 shadow-md scale-[1.05]" : "border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900"}`}>
              <BarChart3 className="w-4 h-4 text-amber-500 mx-auto mb-1" />
              <p className="text-[10px] font-bold text-slate-700 dark:text-slate-300">CBAM</p>
            </div>
            <div className={`p-3 rounded-xl border text-center transition-all ${step === "hover-compare" ? "border-purple-400 bg-purple-50 dark:bg-purple-900/20 shadow-md scale-[1.05]" : "border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900"}`}>
              <Workflow className="w-4 h-4 text-purple-500 mx-auto mb-1" />
              <p className="text-[10px] font-bold text-slate-700 dark:text-slate-300">Compare</p>
            </div>
          </div>

          {/* Recent Workspaces */}
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Recent Workspaces</p>
          <div className={`p-4 rounded-xl border text-center transition-all ${step === "hover-recent" ? "border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 shadow-md" : "border-dashed border-slate-200 dark:border-slate-800"}`}>
            <p className="text-xs text-slate-400">Your recent projects appear here</p>
          </div>
        </div>
      </div>

      {/* Tooltip */}
      <AnimatePresence>
        {activeTooltip && (
          <motion.div
            key={step}
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            style={{ left: activeTooltip.pos.x, top: activeTooltip.pos.y }}
            className="absolute z-40 bg-slate-900 text-white text-xs font-semibold px-3 py-2 rounded-lg shadow-xl max-w-[220px] pointer-events-none"
          >
            {activeTooltip.text}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Animated Cursor */}
      <motion.div
        className="absolute z-50 pointer-events-none"
        animate={cursorPos[step] || cursorPos.idle}
        transition={{ type: "tween", ease: "easeInOut", duration: 0.5 }}
      >
        <MousePointer2 className="w-7 h-7 text-black fill-white drop-shadow-xl -rotate-12" />
      </motion.div>
    </div>
  );
}
