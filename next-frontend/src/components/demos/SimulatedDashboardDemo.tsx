"use client";
import {
  LayoutDashboard, Search, Plus, Database, BarChart3, Workflow, Calculator,
} from "lucide-react";
import { DemoEngine, type DemoStep, type DemoPhase } from "./DemoEngine";

/* ------------------------------------------------------------------ */
/*  Phases                                                             */
/* ------------------------------------------------------------------ */

const PHASES: DemoPhase[] = [
  { name: "Quick Actions", color: "blue" },
  { name: "Workspaces", color: "violet" },
];

/* ------------------------------------------------------------------ */
/*  Steps                                                              */
/* ------------------------------------------------------------------ */

const STEPS: DemoStep[] = [
  { label: "Welcome to your Dashboard", detail: "This is your command center. It shows quick actions to jump to any tool, and lists your recent engineering workspaces.", cursor: { x: 240, y: 150 }, duration: 5000, phaseIndex: 0 },
  { label: "Browse the Material Database", detail: "Click 'Browse Database' to instantly search across 1000+ verified engineering materials with mechanical, thermal, electrical, and economic properties.", cursor: { x: 100, y: 42 }, duration: 5500, click: true, phaseIndex: 0 },
  { label: "Create a New Workspace", detail: "Click 'New Workspace' to start an engineering project. Each workspace has its own Bill of Materials (BOM), component list, weight/cost rollup, and built-in structural calculators.", cursor: { x: 310, y: 42 }, duration: 6000, click: true, phaseIndex: 0 },
  { label: "Quick Action — Material Search", detail: "Jump directly to the full database with advanced filters (category, tensile strength, cost, thermal conductivity) and sorting options.", cursor: { x: 80, y: 150 }, duration: 5000, click: true, phaseIndex: 0 },
  { label: "Quick Action — CBAM Calculator", detail: "Calculate Carbon Border Adjustment Mechanism taxes for EU imports. Input production volume and emission factors to estimate your carbon levy per shipment.", cursor: { x: 230, y: 150 }, duration: 5500, click: true, phaseIndex: 0 },
  { label: "Quick Action — Compare Materials", detail: "Select 2-3 materials and generate an interactive radar chart overlaying all their properties. The AI extracts key differences and recommends the best fit.", cursor: { x: 380, y: 150 }, duration: 5500, click: true, phaseIndex: 0 },
  { label: "Your Recent Workspaces", detail: "All your engineering projects appear here sorted by last modified date. Click any workspace to resume editing your BOM, run calculators, or export reports.", cursor: { x: 240, y: 260 }, duration: 5000, phaseIndex: 1 },
  // Reset
  { label: "", cursor: { x: 240, y: 300 }, duration: 1000, phaseIndex: 1 },
];

/* ------------------------------------------------------------------ */
/*  Highlight lookup                                                   */
/* ------------------------------------------------------------------ */

const HIGHLIGHT_MAP: Record<number, string> = {
  1: "browse",
  2: "new-workspace",
  3: "qa-material",
  4: "qa-cbam",
  5: "qa-compare",
  6: "recent",
};

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export function SimulatedDashboardDemo() {
  return (
    <DemoEngine
      steps={STEPS}
      phases={PHASES}
      windowHeight={360}
      header={
        <>
          <LayoutDashboard className="w-4 h-4 text-blue-500" />
          <span className="text-xs font-bold text-slate-700 dark:text-slate-200">
            Dashboard
          </span>
        </>
      }
    >
      {(step) => <DashboardContent step={step} highlight={HIGHLIGHT_MAP[step]} />}
    </DemoEngine>
  );
}

/* ------------------------------------------------------------------ */
/*  Inner content                                                      */
/* ------------------------------------------------------------------ */

function DashboardContent({ step, highlight }: { step: number; highlight?: string }) {
  return (
    <div className="p-4">
      {/* Action buttons */}
      <div className="flex gap-3 mb-4">
        <div className={`flex-1 flex items-center gap-2 px-3 py-2.5 rounded-xl border text-xs font-semibold transition-all duration-300 ${highlight === "browse" ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-[0_0_16px_rgba(59,130,246,0.10)] scale-[1.04] ring-2 ring-blue-300/60" : "border-slate-200 dark:border-slate-700"}`}>
          <Search className="w-3.5 h-3.5 text-blue-500" />
          <span className="text-slate-700 dark:text-slate-300">Browse Database</span>
        </div>
        <div className={`flex-1 flex items-center gap-2 px-3 py-2.5 rounded-xl text-xs font-semibold text-white transition-all duration-300 ${highlight === "new-workspace" ? "bg-violet-600 shadow-[0_0_16px_rgba(139,92,246,0.12)] scale-[1.04] ring-2 ring-violet-300/60" : "bg-gradient-to-r from-blue-600 to-violet-600"}`}>
          <Plus className="w-3.5 h-3.5" />
          <span>New Workspace</span>
        </div>
      </div>

      {/* Quick Actions */}
      <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Quick Actions</p>
      <div className="grid grid-cols-3 gap-2 mb-4">
        <div className={`p-3 rounded-xl border text-center transition-all duration-300 ${highlight === "qa-material" ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-[0_0_16px_rgba(59,130,246,0.10)] scale-[1.06] ring-2 ring-blue-300/60" : "border-slate-200 dark:border-slate-800"}`}>
          <Database className="w-4 h-4 text-blue-500 mx-auto mb-1" />
          <p className="text-[10px] font-bold text-slate-700 dark:text-slate-300">Material Search</p>
          <p className="text-[8px] text-slate-400">1000+ materials</p>
        </div>
        <div className={`p-3 rounded-xl border text-center transition-all duration-300 ${highlight === "qa-cbam" ? "border-amber-400 bg-amber-50 dark:bg-amber-900/20 shadow-[0_0_16px_rgba(245,158,11,0.10)] scale-[1.06] ring-2 ring-amber-300/60" : "border-slate-200 dark:border-slate-800"}`}>
          <Calculator className="w-4 h-4 text-amber-500 mx-auto mb-1" />
          <p className="text-[10px] font-bold text-slate-700 dark:text-slate-300">CBAM Calc</p>
          <p className="text-[8px] text-slate-400">Carbon tax</p>
        </div>
        <div className={`p-3 rounded-xl border text-center transition-all duration-300 ${highlight === "qa-compare" ? "border-purple-400 bg-purple-50 dark:bg-purple-900/20 shadow-[0_0_16px_rgba(168,85,247,0.10)] scale-[1.06] ring-2 ring-purple-300/60" : "border-slate-200 dark:border-slate-800"}`}>
          <BarChart3 className="w-4 h-4 text-purple-500 mx-auto mb-1" />
          <p className="text-[10px] font-bold text-slate-700 dark:text-slate-300">Compare</p>
          <p className="text-[8px] text-slate-400">Radar charts</p>
        </div>
      </div>

      {/* Recent */}
      <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Recent Workspaces</p>
      <div className={`p-4 rounded-xl border text-center transition-all duration-300 ${highlight === "recent" ? "border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 shadow-[0_0_16px_rgba(100,116,139,0.12)] ring-2 ring-slate-300/60" : "border-dashed border-slate-200 dark:border-slate-800"}`}>
        <Workflow className="w-5 h-5 text-slate-400 mx-auto mb-1" />
        <p className="text-[10px] text-slate-400">Your recent projects appear here</p>
      </div>
    </div>
  );
}
