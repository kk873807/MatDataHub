"use client";
import { GuidedDemo, DemoStep } from "./GuidedDemo";
import { LayoutDashboard, Search, Plus, Database, BarChart3, Workflow, Calculator } from "lucide-react";

const steps: DemoStep[] = [
  { caption: "Welcome to your Dashboard", detail: "This is your command center. It shows quick actions to jump to any tool, and lists your recent engineering workspaces.", cursor: { x: 240, y: 150 } },
  { caption: "Browse the Material Database", detail: "Click 'Browse Database' to instantly search across 1000+ verified engineering materials with mechanical, thermal, electrical, and economic properties.", cursor: { x: 100, y: 42 }, highlight: "browse", click: true },
  { caption: "Create a New Workspace", detail: "Click 'New Workspace' to start an engineering project. Each workspace has its own Bill of Materials (BOM), component list, weight/cost rollup, and built-in structural calculators.", cursor: { x: 310, y: 42 }, highlight: "new-workspace", click: true },
  { caption: "Quick Action — Material Search", detail: "Jump directly to the full database with advanced filters (category, tensile strength, cost, thermal conductivity) and sorting options.", cursor: { x: 80, y: 150 }, highlight: "qa-material", click: true },
  { caption: "Quick Action — CBAM Calculator", detail: "Calculate Carbon Border Adjustment Mechanism taxes for EU imports. Input production volume and emission factors to estimate your carbon levy per shipment.", cursor: { x: 230, y: 150 }, highlight: "qa-cbam", click: true },
  { caption: "Quick Action — Compare Materials", detail: "Select 2-3 materials and generate an interactive radar chart overlaying all their properties. The AI extracts key differences and recommends the best fit.", cursor: { x: 380, y: 150 }, highlight: "qa-compare", click: true },
  { caption: "Your Recent Workspaces", detail: "All your engineering projects appear here sorted by last modified date. Click any workspace to resume editing your BOM, run calculators, or export reports.", cursor: { x: 240, y: 260 }, highlight: "recent" },
];

export function SimulatedDashboardDemo() {
  return (
    <GuidedDemo steps={steps} height="min-h-[300px]">
      {(activeStep, highlight) => (
        <div className="w-full max-w-lg mx-auto bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
          {/* Top bar */}
          <div className="px-5 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center gap-2">
            <LayoutDashboard className="w-4 h-4 text-blue-500" />
            <span className="text-sm font-bold text-slate-900 dark:text-white">Dashboard</span>
          </div>
          <div className="p-4">
            {/* Action buttons */}
            <div className="flex gap-3 mb-4">
              <div className={`flex-1 flex items-center gap-2 px-3 py-2.5 rounded-xl border text-xs font-semibold transition-all ${highlight === "browse" ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-lg scale-[1.04] ring-2 ring-blue-300" : "border-slate-200 dark:border-slate-700"}`}>
                <Search className="w-3.5 h-3.5 text-blue-500" />
                <span className="text-slate-700 dark:text-slate-300">Browse Database</span>
              </div>
              <div className={`flex-1 flex items-center gap-2 px-3 py-2.5 rounded-xl text-xs font-semibold text-white transition-all ${highlight === "new-workspace" ? "bg-violet-600 shadow-lg scale-[1.04] ring-2 ring-violet-300" : "bg-gradient-to-r from-blue-600 to-violet-600"}`}>
                <Plus className="w-3.5 h-3.5" />
                <span>New Workspace</span>
              </div>
            </div>

            {/* Quick Actions */}
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Quick Actions</p>
            <div className="grid grid-cols-3 gap-2 mb-4">
              <div className={`p-3 rounded-xl border text-center transition-all ${highlight === "qa-material" ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-lg scale-[1.06] ring-2 ring-blue-300" : "border-slate-200 dark:border-slate-800"}`}>
                <Database className="w-4 h-4 text-blue-500 mx-auto mb-1" />
                <p className="text-[10px] font-bold text-slate-700 dark:text-slate-300">Material Search</p>
                <p className="text-[8px] text-slate-400">1000+ materials</p>
              </div>
              <div className={`p-3 rounded-xl border text-center transition-all ${highlight === "qa-cbam" ? "border-amber-400 bg-amber-50 dark:bg-amber-900/20 shadow-lg scale-[1.06] ring-2 ring-amber-300" : "border-slate-200 dark:border-slate-800"}`}>
                <Calculator className="w-4 h-4 text-amber-500 mx-auto mb-1" />
                <p className="text-[10px] font-bold text-slate-700 dark:text-slate-300">CBAM Calc</p>
                <p className="text-[8px] text-slate-400">Carbon tax</p>
              </div>
              <div className={`p-3 rounded-xl border text-center transition-all ${highlight === "qa-compare" ? "border-purple-400 bg-purple-50 dark:bg-purple-900/20 shadow-lg scale-[1.06] ring-2 ring-purple-300" : "border-slate-200 dark:border-slate-800"}`}>
                <BarChart3 className="w-4 h-4 text-purple-500 mx-auto mb-1" />
                <p className="text-[10px] font-bold text-slate-700 dark:text-slate-300">Compare</p>
                <p className="text-[8px] text-slate-400">Radar charts</p>
              </div>
            </div>

            {/* Recent */}
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Recent Workspaces</p>
            <div className={`p-4 rounded-xl border text-center transition-all ${highlight === "recent" ? "border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 shadow-lg ring-2 ring-slate-300" : "border-dashed border-slate-200 dark:border-slate-800"}`}>
              <Workflow className="w-5 h-5 text-slate-400 mx-auto mb-1" />
              <p className="text-[10px] text-slate-400">Your recent projects appear here</p>
            </div>
          </div>
        </div>
      )}
    </GuidedDemo>
  );
}
