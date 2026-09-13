"use client";
import { GuidedDemo, DemoStep } from "./GuidedDemo";
import { Workflow, Plus, FolderKanban, ShieldAlert, Thermometer, Activity, AlignEndVertical, IndianRupee, Flame, Wrench, Trash2 } from "lucide-react";

const steps: DemoStep[] = [
  { caption: "Engineering Workspaces Overview", detail: "A workspace is a self-contained engineering project. Each one has its own Bill of Materials (BOM), component list, total weight/cost rollup, and 6 built-in structural calculators. Pro and Advanced users can create unlimited workspaces.", cursor: { x: 240, y: 60 } },
  { caption: "Creating a New Workspace", detail: "Click the '+' button to create a workspace. Give it a name (e.g., 'Chassis Assembly') and an optional description. The workspace is instantly created and you can start adding components.", cursor: { x: 400, y: 38 }, highlight: "add-btn", click: true },
  { caption: "Adding Components to the BOM", detail: "Inside a workspace, click 'Add Component'. Enter the component name, select a material from the database, and specify the quantity and mass. The component is added to your Bill of Materials table.", cursor: { x: 200, y: 120 }, highlight: "bom", click: true },
  { caption: "BOM Auto-Rollup", detail: "As you add components, the system automatically calculates and displays the total assembly weight (kg), total cost (using real-time material pricing), and per-component cost breakdowns. Delete or edit components anytime.", cursor: { x: 350, y: 150 }, highlight: "rollup" },
  { caption: "Workspace Tools — 6 Built-in Calculators", detail: "Every workspace includes 6 structural engineering calculators. Select any component's material, then run calculations specific to that material's properties. Results are displayed inline.", cursor: { x: 200, y: 210 }, highlight: "tools" },
  { caption: "Calculator 1 — Safety Factor", detail: "Determines if a material will fail under applied stress. Input the applied load (N) and cross-sectional area (mm2). The calculator divides the material's Ultimate Tensile Strength by the applied stress to give you the Factor of Safety. FoS > 2.0 is generally acceptable.", cursor: { x: 100, y: 250 }, highlight: "calc-safety", click: true },
  { caption: "Calculator 2 — Thermal Expansion", detail: "Calculates how much a component will physically grow when heated. Input the original length (mm), initial temperature, and final temperature. Uses the material's Coefficient of Thermal Expansion to compute change in length (delta L) and induced thermal stress.", cursor: { x: 260, y: 250 }, highlight: "calc-thermal", click: true },
  { caption: "Calculator 3 — Fatigue Life", detail: "Predicts how many loading cycles a component can withstand before failure. Input the stress amplitude (MPa) and the material's fatigue coefficients. Uses S-N curve approximations to estimate the number of cycles to failure under repeated dynamic loading.", cursor: { x: 420, y: 250 }, highlight: "calc-fatigue", click: true },
  { caption: "Calculator 4 — Beam Deflection", detail: "Analyzes bending in structural beams. Input beam length (mm), load type (point or distributed), load magnitude (N), and the moment of inertia. Calculates maximum deflection (mm) and maximum bending stress using Euler-Bernoulli beam theory.", cursor: { x: 100, y: 310 }, highlight: "calc-beam", click: true },
  { caption: "Calculator 5 — Cost Optimizer", detail: "Compares your current BOM cost against alternative materials. The optimizer searches the database for materials with similar mechanical properties but lower cost-per-kg, showing potential savings per component and for the total assembly.", cursor: { x: 260, y: 310 }, highlight: "calc-cost", click: true },
  { caption: "Calculator 6 — Thermal Shock Resistance", detail: "Evaluates whether a material can survive rapid temperature changes without fracturing. Input the temperature differential and heat transfer coefficient. Uses the material's thermal conductivity, tensile strength, and elastic modulus to compute the Thermal Shock Resistance parameter (R).", cursor: { x: 420, y: 310 }, highlight: "calc-shock", click: true },
  { caption: "Export & Share Your Workspace", detail: "Once your BOM and calculations are complete, export the entire workspace as a report. Share the workspace link with colleagues for collaborative review. All data is saved and persists across sessions.", cursor: { x: 350, y: 38 }, highlight: "export" },
];

export function SimulatedWorkspaceDemo() {
  return (
    <GuidedDemo steps={steps} height="min-h-[360px]">
      {(activeStep, highlight) => (
        <div className="w-full max-w-lg mx-auto bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="px-5 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Workflow className="w-4 h-4 text-violet-500" />
              <span className="text-sm font-bold text-slate-900 dark:text-white">Chassis Assembly</span>
            </div>
            <div className="flex items-center gap-2">
              <div className={`transition-all ${highlight === "export" ? "ring-2 ring-blue-300 rounded-lg" : ""}`}>
                <span className="text-[10px] font-semibold text-blue-500 px-2 py-1 rounded-lg bg-blue-50 dark:bg-blue-900/20">Export</span>
              </div>
              <div className={`p-1.5 rounded-lg transition-all ${highlight === "add-btn" ? "bg-violet-100 dark:bg-violet-900/30 ring-2 ring-violet-400 shadow-lg scale-110" : "bg-slate-100 dark:bg-slate-800"}`}>
                <Plus className="w-3.5 h-3.5 text-violet-600" />
              </div>
            </div>
          </div>

          <div className="p-4">
            {/* BOM Table */}
            <div className={`mb-3 transition-all rounded-xl ${highlight === "bom" ? "ring-2 ring-violet-300 shadow-md" : ""}`}>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
                <FolderKanban className="w-3 h-3" /> Bill of Materials
              </p>
              <div className="space-y-1.5">
                <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span className="w-5 h-5 rounded bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-[10px] font-bold text-blue-600">1</span>
                    <span className="font-semibold text-slate-900 dark:text-white">Frame Rail</span>
                    <span className="text-slate-400">ASTM A36</span>
                  </div>
                  <span className="text-slate-500">12.5 kg &middot; $8.75</span>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span className="w-5 h-5 rounded bg-violet-100 dark:bg-violet-900/30 flex items-center justify-center text-[10px] font-bold text-violet-600">2</span>
                    <span className="font-semibold text-slate-900 dark:text-white">Cross Member</span>
                    <span className="text-slate-400">AISI 304</span>
                  </div>
                  <span className="text-slate-500">4.2 kg &middot; $11.76</span>
                </div>
              </div>
            </div>

            {/* Rollup */}
            <div className={`p-2.5 rounded-lg bg-gradient-to-r from-blue-50 to-violet-50 dark:from-blue-900/10 dark:to-violet-900/10 border border-blue-200 dark:border-blue-800 mb-3 flex justify-between text-xs transition-all ${highlight === "rollup" ? "ring-2 ring-blue-300 shadow-md scale-[1.02]" : ""}`}>
              <span className="font-bold text-blue-700 dark:text-blue-400">Total: 16.7 kg</span>
              <span className="font-bold text-violet-700 dark:text-violet-400">Cost: $20.51</span>
            </div>

            {/* Tools header */}
            <div className={`mb-2 transition-all ${highlight === "tools" ? "ring-2 ring-amber-300 rounded-lg p-1 shadow-md" : ""}`}>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                <Wrench className="w-3 h-3" /> Workspace Calculators
              </p>
            </div>

            {/* Calculator grid */}
            <div className="grid grid-cols-3 gap-1.5">
              {[
                { id: "calc-safety",  icon: ShieldAlert,      label: "Safety Factor",    color: "text-rose-500" },
                { id: "calc-thermal", icon: Thermometer,       label: "Thermal Exp.",     color: "text-orange-500" },
                { id: "calc-fatigue", icon: Activity,          label: "Fatigue Life",     color: "text-blue-500" },
                { id: "calc-beam",    icon: AlignEndVertical,  label: "Beam Deflection",  color: "text-indigo-500" },
                { id: "calc-cost",    icon: IndianRupee,       label: "Cost Optimizer",   color: "text-emerald-500" },
                { id: "calc-shock",   icon: Flame,             label: "Thermal Shock",    color: "text-red-500" },
              ].map((calc) => (
                <div
                  key={calc.id}
                  className={`p-2 rounded-lg border text-center transition-all ${highlight === calc.id ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-lg ring-2 ring-blue-300 scale-[1.08]" : "border-slate-200 dark:border-slate-800"}`}
                >
                  <calc.icon className={`w-4 h-4 ${calc.color} mx-auto mb-0.5`} />
                  <p className="text-[9px] font-bold text-slate-700 dark:text-slate-300 leading-tight">{calc.label}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </GuidedDemo>
  );
}
