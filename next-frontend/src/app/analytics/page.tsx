"use client";
import Link from "next/link";
import { BarChart3, Scale, Replace, Factory, Layers } from "lucide-react";
import { motion } from "framer-motion";

export default function AnalyticsDashboard() {
  const tools = [
    {
      title: "Side-by-Side Compare",
      description: "Compare properties, view radar fingerprints, and extract key takeaways between multiple materials.",
      icon: Scale,
      color: "text-blue-400",
      bg: "bg-blue-900/20",
      border: "hover:border-blue-500/50",
      href: "/analytics/compare",
      badge: "Free"
    },
    {
      title: "Smart AI Substitution",
      description: "Find alternative materials based on weighted parameters like cost, density, and carbon footprint.",
      icon: Replace,
      color: "text-purple-400",
      bg: "bg-purple-900/20",
      border: "hover:border-purple-500/50",
      href: "/analytics/substitution",
      badge: "Pro"
    },
    {
      title: "Supply Chain Risk & CBAM",
      description: "Upload your Bill of Materials (BOM) to automatically calculate ESG impact and obsolescence risk.",
      icon: Factory,
      color: "text-amber-400",
      bg: "bg-amber-900/20",
      border: "hover:border-amber-500/50",
      href: "/analytics/cbam",
      badge: "Enterprise"
    },
    {
      title: "Composite Synthesizer",
      description: "Blend two materials using the Rule of Mixtures to predict hybrid mechanical properties.",
      icon: Layers,
      color: "text-cyan-400",
      bg: "bg-cyan-900/20",
      border: "hover:border-cyan-500/50",
      href: "/analytics/synthesizer",
      badge: "Pro"
    }
  ];

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto">
      <div className="w-full max-w-5xl mx-auto space-y-8">
        <div>
          <h1 className="text-4xl font-bold text-white flex items-center gap-3">
            <BarChart3 className="w-10 h-10 text-indigo-400" />
            Advanced Analytics
          </h1>
          <p className="text-slate-300 mt-2 text-lg max-w-3xl">
            Leverage enterprise-grade tools to benchmark materials, run AI substitutions, and calculate supply chain emissions.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
          {tools.map((tool, i) => (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              key={tool.title}
            >
              <Link href={tool.href} className={`block h-full p-6 rounded-2xl bg-slate-900 border border-slate-800 ${tool.border} transition-all group relative overflow-hidden`}>
                <div className={`w-12 h-12 rounded-xl ${tool.bg} flex items-center justify-center mb-4`}>
                  <tool.icon className={`w-6 h-6 ${tool.color}`} />
                </div>
                
                <h3 className="text-xl font-bold text-white mb-2 group-hover:text-indigo-300 transition-colors">{tool.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed mb-6">{tool.description}</p>
                
                <div className="absolute top-4 right-4">
                  <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded border ${
                    tool.badge === 'Free' ? 'bg-slate-800 border-slate-700 text-slate-300' :
                    tool.badge === 'Pro' ? 'bg-purple-900/30 border-purple-700/50 text-purple-400' :
                    'bg-amber-900/30 border-amber-700/50 text-amber-400'
                  }`}>
                    {tool.badge}
                  </span>
                </div>
                
                <div className="mt-auto flex items-center text-sm font-semibold text-indigo-400 group-hover:text-indigo-300">
                  Launch Tool →
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>
    </main>
  );
}
