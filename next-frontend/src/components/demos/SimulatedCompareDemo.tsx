"use client";
import { GuidedDemo, DemoStep } from "./GuidedDemo";
import { Scale, Replace, Factory, Layers, BarChart3, Target } from "lucide-react";

const steps: DemoStep[] = [
  { caption: "Analytics Suite Overview", detail: "This page gives you access to 4 powerful analysis tools: Side-by-Side Compare, Smart AI Substitution, CBAM Emissions Calculator, and Composite Synthesizer. Each solves a different engineering problem.", cursor: { x: 240, y: 80 } },
  { caption: "Tool 1 — Side-by-Side Compare", detail: "Select 2-3 materials from the database. The system generates an interactive radar chart overlaying Density, Tensile Strength, Thermal Conductivity, Cost, and Carbon Footprint. An AI engine extracts the key takeaways (e.g., 'Material A is 42% more cost-effective').", cursor: { x: 100, y: 120 }, highlight: "compare", click: true },
  { caption: "How Compare Works", detail: "Step 1: Search and select a material in each dropdown. Step 2: Click 'Compare'. Step 3: View the radar fingerprint and a property-by-property table. Step 4: Read the AI-generated key takeaways summarizing which material wins on each axis.", cursor: { x: 100, y: 120 }, highlight: "compare" },
  { caption: "Tool 2 — Smart AI Substitution", detail: "Find alternative materials based on multi-objective optimization. Input a baseline material, then set importance weights for Cost, Density, and Carbon Footprint. The AI ranks all alternatives by a weighted fitness score.", cursor: { x: 260, y: 120 }, highlight: "substitution", click: true },
  { caption: "How Substitution Works", detail: "Step 1: Select your current material. Step 2: Drag sliders to set how much you care about Cost vs. Density vs. Carbon. Step 3: Click 'Find Alternatives'. Step 4: Review the ranked list — each alternative shows its fitness score and how it compares on every weighted parameter.", cursor: { x: 260, y: 120 }, highlight: "substitution" },
  { caption: "Tool 3 — CBAM Emissions Calculator", detail: "Calculate predictive Carbon Border Adjustment Mechanism taxes for EU procurement. Upload your Bill of Materials (BOM) to automatically compute ESG impact scores and estimate the carbon levy per shipment based on current EU pricing.", cursor: { x: 100, y: 230 }, highlight: "cbam", click: true },
  { caption: "How CBAM Works", detail: "Step 1: Select a material and enter production volume (tonnes). Step 2: Input the specific emission factor (tCO2/tonne) or use the database default. Step 3: Set the EU ETS carbon price. Step 4: The calculator outputs total embedded emissions and the estimated CBAM tax liability in EUR.", cursor: { x: 100, y: 230 }, highlight: "cbam" },
  { caption: "Tool 4 — Composite Synthesizer", detail: "Blend two materials using the Rule of Mixtures to predict theoretical hybrid properties. Select a matrix material and a fiber/reinforcement, set the fiber volume fraction, and generate a complete property profile for the composite.", cursor: { x: 260, y: 230 }, highlight: "synthesizer", click: true },
  { caption: "How Synthesizer Works", detail: "Step 1: Choose a matrix material (e.g., Epoxy Resin). Step 2: Choose a fiber (e.g., Carbon Fiber T300). Step 3: Set the fiber volume fraction (e.g., 60%). Step 4: View predicted Density, Elastic Modulus, Tensile Strength, and Thermal Conductivity using Voigt and Reuss bounds.", cursor: { x: 260, y: 230 }, highlight: "synthesizer" },
];

export function SimulatedCompareDemo() {
  return (
    <GuidedDemo steps={steps} height="min-h-[300px]">
      {(activeStep, highlight) => (
        <div className="w-full max-w-lg mx-auto bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
          <div className="px-5 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-blue-500" />
            <span className="text-sm font-bold text-slate-900 dark:text-white">Advanced Analytics</span>
          </div>
          <div className="p-4 grid grid-cols-2 gap-3">
            <div className={`p-4 rounded-xl border flex flex-col items-center text-center transition-all ${highlight === "compare" ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-lg ring-2 ring-blue-300 scale-[1.04]" : "border-slate-200 dark:border-slate-800"}`}>
              <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-2">
                <Scale className="w-5 h-5 text-blue-600" />
              </div>
              <p className="text-xs font-bold text-slate-900 dark:text-white mb-0.5">Side-by-Side Compare</p>
              <p className="text-[10px] text-slate-500">Radar charts & AI takeaways</p>
              <span className="text-[8px] mt-2 px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 font-bold">Free</span>
            </div>
            <div className={`p-4 rounded-xl border flex flex-col items-center text-center transition-all ${highlight === "substitution" ? "border-purple-400 bg-purple-50 dark:bg-purple-900/20 shadow-lg ring-2 ring-purple-300 scale-[1.04]" : "border-slate-200 dark:border-slate-800"}`}>
              <div className="w-10 h-10 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-2">
                <Replace className="w-5 h-5 text-purple-600" />
              </div>
              <p className="text-xs font-bold text-slate-900 dark:text-white mb-0.5">AI Substitution</p>
              <p className="text-[10px] text-slate-500">Multi-objective optimization</p>
              <span className="text-[8px] mt-2 px-2 py-0.5 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-600 font-bold">Pro</span>
            </div>
            <div className={`p-4 rounded-xl border flex flex-col items-center text-center transition-all ${highlight === "cbam" ? "border-amber-400 bg-amber-50 dark:bg-amber-900/20 shadow-lg ring-2 ring-amber-300 scale-[1.04]" : "border-slate-200 dark:border-slate-800"}`}>
              <div className="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center mb-2">
                <Factory className="w-5 h-5 text-amber-600" />
              </div>
              <p className="text-xs font-bold text-slate-900 dark:text-white mb-0.5">CBAM Emissions</p>
              <p className="text-[10px] text-slate-500">EU Carbon Tax calculator</p>
              <span className="text-[8px] mt-2 px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900/30 text-amber-600 font-bold">Enterprise</span>
            </div>
            <div className={`p-4 rounded-xl border flex flex-col items-center text-center transition-all ${highlight === "synthesizer" ? "border-cyan-400 bg-cyan-50 dark:bg-cyan-900/20 shadow-lg ring-2 ring-cyan-300 scale-[1.04]" : "border-slate-200 dark:border-slate-800"}`}>
              <div className="w-10 h-10 rounded-xl bg-cyan-100 dark:bg-cyan-900/30 flex items-center justify-center mb-2">
                <Layers className="w-5 h-5 text-cyan-600" />
              </div>
              <p className="text-xs font-bold text-slate-900 dark:text-white mb-0.5">Composite Synthesizer</p>
              <p className="text-[10px] text-slate-500">Rule of Mixtures blending</p>
              <span className="text-[8px] mt-2 px-2 py-0.5 rounded-full bg-cyan-100 dark:bg-cyan-900/30 text-cyan-600 font-bold">Pro</span>
            </div>
          </div>
        </div>
      )}
    </GuidedDemo>
  );
}
