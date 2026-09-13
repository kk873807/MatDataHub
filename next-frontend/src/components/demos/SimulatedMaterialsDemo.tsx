"use client";
import { GuidedDemo, DemoStep } from "./GuidedDemo";
import { Database, Search, SlidersHorizontal, ChevronRight, ExternalLink, Info } from "lucide-react";

const steps: DemoStep[] = [
  { caption: "Material Database Overview", detail: "This page lets you search, filter, sort, and explore 1000+ verified engineering materials. Every material has verified mechanical, thermal, electrical, and economic properties sourced from ASTM, ISO, and DIN standards.", cursor: { x: 240, y: 40 } },
  { caption: "Search by Name or Grade", detail: "Type any material name (e.g., 'Steel', 'Titanium', 'Aluminium 7075') or standard grade (e.g., 'ASTM A36') into the search bar. Real-time autocomplete suggestions appear as you type.", cursor: { x: 150, y: 42 }, highlight: "search", click: true },
  { caption: "Filter by Category", detail: "Filter materials by category: Metal, Polymer, Ceramic, or Composite. This instantly narrows results to only that material family.", cursor: { x: 80, y: 105 }, highlight: "cat-filter", click: true },
  { caption: "Advanced Property Filters", detail: "Use numerical sliders to filter by exact thresholds — Minimum Tensile Strength (MPa), Maximum Cost per kg, and Minimum Thermal Conductivity (W/mK). Only materials matching ALL criteria are shown.", cursor: { x: 300, y: 105 }, highlight: "adv-filter" },
  { caption: "Sort Results", detail: "Sort results by Name (A-Z), Cost (low to high or high to low), Tensile Strength (highest first), or Density (lightest first) to find the best material for your use case.", cursor: { x: 420, y: 105 }, highlight: "sort" },
  { caption: "Material Card — Properties at a Glance", detail: "Each card shows the material name, category badge (color-coded), key properties (Density, Tensile Strength, Thermal Conductivity), and cost range. Hover to highlight it.", cursor: { x: 130, y: 200 }, highlight: "card-1" },
  { caption: "Click to Open Full Detail View", detail: "Clicking a material card opens its dedicated page with complete properties, standards & identifiers (ASTM/ISO/DIN designations), equivalent grades, pricing trends, similar materials, and the verified data source.", cursor: { x: 130, y: 200 }, highlight: "card-1", click: true },
  { caption: "Data Source Verification", detail: "Every material shows its data source. Hover over 'Verified Internal Database' to see that all properties are sourced from ASTM, ISO, DIN standards, reputable commodities indices, and validated scientific databases.", cursor: { x: 350, y: 280 }, highlight: "data-source" },
  { caption: "Export and Share", detail: "From any material's detail page, you can export the full datasheet to CSV for offline analysis, or copy a unique shareable link to send to your engineering team.", cursor: { x: 400, y: 40 }, highlight: "export" },
];

export function SimulatedMaterialsDemo() {
  return (
    <GuidedDemo steps={steps} height="min-h-[320px]">
      {(activeStep, highlight) => (
        <div className="w-full max-w-lg mx-auto bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
          <div className="p-4">
            {/* Search bar */}
            <div className={`border rounded-xl p-3 flex items-center gap-2 mb-3 transition-all ${highlight === "search" ? "border-blue-500 ring-2 ring-blue-300 shadow-lg" : "border-slate-200 dark:border-slate-700"}`}>
              <Search className="w-4 h-4 text-slate-400" />
              <span className="text-sm text-slate-400">Search 1000+ materials...</span>
            </div>

            {/* Filters row */}
            <div className="flex gap-2 mb-4">
              <div className={`px-3 py-1.5 rounded-lg border text-[10px] font-semibold flex items-center gap-1 transition-all ${highlight === "cat-filter" ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 ring-2 ring-blue-300 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                <Database className="w-3 h-3" /> Category
              </div>
              <div className={`px-3 py-1.5 rounded-lg border text-[10px] font-semibold flex items-center gap-1 transition-all ${highlight === "adv-filter" ? "border-emerald-400 bg-emerald-50 dark:bg-emerald-900/20 ring-2 ring-emerald-300 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                <SlidersHorizontal className="w-3 h-3" /> Filters
              </div>
              <div className={`px-3 py-1.5 rounded-lg border text-[10px] font-semibold flex items-center gap-1 ml-auto transition-all ${highlight === "sort" ? "border-violet-400 bg-violet-50 dark:bg-violet-900/20 ring-2 ring-violet-300 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                Sort by
              </div>
              <div className={`px-3 py-1.5 rounded-lg border text-[10px] font-semibold flex items-center gap-1 transition-all ${highlight === "export" ? "border-amber-400 bg-amber-50 dark:bg-amber-900/20 ring-2 ring-amber-300 shadow-md" : "border-slate-200 dark:border-slate-700"}`}>
                <ExternalLink className="w-3 h-3" /> Export
              </div>
            </div>

            {/* Results */}
            <div className="space-y-2">
              <div className={`p-3 rounded-xl border flex items-center justify-between transition-all ${highlight === "card-1" ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20 shadow-lg ring-2 ring-blue-300 scale-[1.02]" : "border-slate-200 dark:border-slate-800"}`}>
                <div>
                  <div className="flex items-center gap-2 mb-0.5">
                    <p className="text-sm font-bold text-slate-900 dark:text-white">AISI 304 Stainless Steel</p>
                    <span className="text-[8px] px-1.5 py-0.5 rounded bg-blue-100 dark:bg-blue-900/30 text-blue-600 font-bold">Metal</span>
                  </div>
                  <p className="text-[10px] text-slate-500">8.0 g/cm3 &middot; UTS 515 MPa &middot; 16.2 W/mK &middot; $2.80/kg</p>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-300" />
              </div>
              <div className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-0.5">
                    <p className="text-sm font-bold text-slate-900 dark:text-white">Aluminium 7075-T6</p>
                    <span className="text-[8px] px-1.5 py-0.5 rounded bg-blue-100 dark:bg-blue-900/30 text-blue-600 font-bold">Metal</span>
                  </div>
                  <p className="text-[10px] text-slate-500">2.81 g/cm3 &middot; UTS 572 MPa &middot; 130 W/mK &middot; $3.20/kg</p>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-300" />
              </div>
              <div className={`p-2 rounded-lg text-center transition-all ${highlight === "data-source" ? "bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-300 ring-2 ring-emerald-300 shadow-md" : ""}`}>
                <p className="text-[10px] text-emerald-600 font-semibold flex items-center justify-center gap-1">
                  <Info className="w-3 h-3" /> Data Source: Verified Internal Database (ASTM, ISO, DIN)
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </GuidedDemo>
  );
}
