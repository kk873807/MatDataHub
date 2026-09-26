"use client";

import { Leaf, ArrowRight } from "lucide-react";
import Link from "next/link";

export function CbamLeadMagnet() {
  return (
    <section className="py-24 px-6 relative overflow-hidden bg-emerald-900">
      <div className="absolute inset-0 opacity-10 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-emerald-400 via-transparent to-transparent"></div>
      
      <div className="max-w-5xl mx-auto relative z-10 flex flex-col md:flex-row items-center gap-12">
        <div className="flex-1 text-left">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-800 text-emerald-300 text-xs font-bold rounded-full uppercase tracking-wider mb-6">
            <Leaf className="w-3 h-3" /> EU CBAM Compliance 2026
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6 font-heading">
            Don't get hit by unexpected EU Carbon Taxes.
          </h2>
          <p className="text-emerald-100/80 mb-8 leading-relaxed max-w-xl text-sm sm:text-base">
            The EU Carbon Border Adjustment Mechanism (CBAM) financial phase is active.
            Exporters are now liable for embodied emissions. Use our audit tool to calculate your exact financial liability per shipment.
          </p>
          <Link href="/analytics/cbam" className="inline-flex items-center gap-2 px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-white rounded-xl font-bold transition-all shadow-lg shadow-emerald-900/50">
            Run Free CBAM Audit <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="w-full md:w-[400px]">
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-3xl p-6 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/20 rounded-full blur-3xl"></div>
            
            <div className="flex justify-between text-sm mb-5">
              <span className="text-emerald-200">Material Exported:</span>
              <span className="font-bold text-white">1,000 kg (Steel)</span>
            </div>
            <div className="flex justify-between text-sm mb-5">
              <span className="text-emerald-200">Embodied Carbon Factor:</span>
              <span className="font-bold text-white">4.80 kg CO₂ / kg</span>
            </div>
            <div className="w-full h-px bg-white/10 my-5"></div>
            <div className="flex flex-col gap-1 mb-2">
              <span className="text-emerald-300/80 font-bold text-xs uppercase">Est. EU Tax Liability:</span>
              <div className="flex justify-between items-end">
                 <span className="text-4xl font-black text-white">€312.00</span>
                 <span className="text-xs text-emerald-200 mb-2">@ €65/tCO₂e</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
