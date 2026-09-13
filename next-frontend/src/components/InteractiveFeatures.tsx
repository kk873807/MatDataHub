"use client";
import { useState, useEffect } from "react";
import { Database, Workflow, Target, BrainCircuit, Bot, Search, LayoutDashboard, Send, ChevronRight, Zap } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const features = [
  {
    id: "database",
    title: "Parametric Database",
    desc: "Search thousands of materials with verified mechanical, thermal, and electrical properties mapped to global indices.",
    icon: Database,
    color: "bg-blue-500",
  },
  {
    id: "workspaces",
    title: "Engineering Workspaces",
    desc: "Manage multi-part assemblies, build interactive BOMs, and calculate total system weights and costs in real-time.",
    icon: Workflow,
    color: "bg-violet-500",
  },
  {
    id: "ai",
    title: "AI Materials Adviser",
    desc: "Chat with a specialized engineering AI to find exact alternatives based on multi-objective constraints and standards.",
    icon: Bot,
    color: "bg-emerald-500",
  },
  {
    id: "cbam",
    title: "CBAM & ESG Tracking",
    desc: "Calculate predictive Carbon Border Adjustment Mechanism taxes for your EU procurement workflows.",
    icon: Target,
    color: "bg-amber-500",
  },
];

export function InteractiveFeatures() {
  const [activeTab, setActiveTab] = useState(features[0].id);

  // Optional: Auto-rotate tabs
  useEffect(() => {
    const timer = setInterval(() => {
      setActiveTab((current) => {
        const currentIndex = features.findIndex((f) => f.id === current);
        return features[(currentIndex + 1) % features.length].id;
      });
    }, 6000);
    return () => clearInterval(timer);
  }, []);

  return (
    <section id="solution" className="py-24 px-6 bg-slate-50 dark:bg-slate-900/50 relative overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-500/5 dark:bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
      
      <div className="max-w-7xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-slate-900 dark:text-white mb-6 font-heading">
            Everything you need in <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-violet-600">one platform</span>
          </h2>
          <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto text-lg">
            MatDataHub replaces scattered spreadsheets and PDF datasheets with a unified, interactive workspace.
          </p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8 lg:gap-12 items-center">
          {/* Tabs Menu */}
          <div className="w-full lg:w-1/3 flex flex-col gap-3">
            {features.map((feat) => (
              <button
                key={feat.id}
                onClick={() => setActiveTab(feat.id)}
                className={`text-left p-6 rounded-2xl transition-all duration-300 border-2 ${
                  activeTab === feat.id
                    ? "bg-white dark:bg-slate-800 border-blue-500 shadow-xl scale-[1.02]"
                    : "bg-transparent border-transparent hover:bg-slate-100 dark:hover:bg-slate-800/50 hover:border-slate-200 dark:hover:border-slate-700"
                }`}
              >
                <div className="flex items-center gap-4 mb-3">
                  <div className={`p-2.5 rounded-xl text-white ${feat.color} ${activeTab === feat.id ? "shadow-lg" : ""}`}>
                    <feat.icon className="w-6 h-6" />
                  </div>
                  <h3 className={`text-xl font-bold font-heading ${activeTab === feat.id ? "text-slate-900 dark:text-white" : "text-slate-700 dark:text-slate-300"}`}>
                    {feat.title}
                  </h3>
                </div>
                <p className={`text-sm ${activeTab === feat.id ? "text-slate-600 dark:text-slate-300" : "text-slate-500"}`}>
                  {feat.desc}
                </p>
              </button>
            ))}
          </div>

          {/* Interactive Mockup Panel */}
          <div className="w-full lg:w-2/3">
            <div className="bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-2xl overflow-hidden aspect-video relative flex flex-col">
              {/* Browser Header */}
              <div className="bg-slate-100 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 p-4 flex items-center gap-2 shrink-0">
                <div className="w-3 h-3 rounded-full bg-red-400"></div>
                <div className="w-3 h-3 rounded-full bg-amber-400"></div>
                <div className="w-3 h-3 rounded-full bg-emerald-400"></div>
                <div className="ml-4 bg-white dark:bg-slate-800 text-slate-400 text-xs px-3 py-1.5 rounded-md flex-1 text-center font-mono max-w-sm mx-auto flex items-center justify-center gap-2">
                  <Zap className="w-3 h-3" /> app.matdatahub.com
                </div>
              </div>

              {/* Dynamic Content */}
              <div className="flex-1 relative bg-slate-50 dark:bg-slate-900/50 p-6 overflow-hidden">
                <AnimatePresence mode="wait">
                  {activeTab === "database" && (
                    <motion.div
                      key="database"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                      className="h-full flex flex-col gap-4"
                    >
                      <div className="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm flex items-center gap-3">
                        <Search className="text-slate-400 w-5 h-5" />
                        <div className="h-4 w-48 bg-slate-100 dark:bg-slate-700 rounded animate-pulse"></div>
                      </div>
                      <div className="grid grid-cols-2 gap-4 flex-1">
                        {[1, 2, 3, 4].map((i) => (
                          <div key={i} className="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col gap-3">
                            <div className="h-5 w-24 bg-blue-100 dark:bg-blue-900/30 rounded"></div>
                            <div className="h-3 w-full bg-slate-100 dark:bg-slate-700 rounded mt-2"></div>
                            <div className="h-3 w-2/3 bg-slate-100 dark:bg-slate-700 rounded"></div>
                            <div className="mt-auto pt-3 border-t border-slate-100 dark:border-slate-700 flex justify-between">
                               <div className="h-4 w-12 bg-emerald-100 dark:bg-emerald-900/30 rounded"></div>
                               <div className="h-4 w-16 bg-amber-100 dark:bg-amber-900/30 rounded"></div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </motion.div>
                  )}

                  {activeTab === "workspaces" && (
                    <motion.div
                      key="workspaces"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                      className="h-full flex gap-4"
                    >
                      <div className="w-1/3 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-4 flex flex-col gap-3">
                         <div className="h-4 w-24 bg-slate-200 dark:bg-slate-700 rounded mb-2"></div>
                         {[1, 2, 3].map(i => (
                           <div key={i} className="flex items-center gap-2 p-2 bg-slate-50 dark:bg-slate-900 rounded-lg">
                             <div className="w-6 h-6 rounded bg-violet-100 dark:bg-violet-900/30 shrink-0"></div>
                             <div className="h-3 w-full bg-slate-200 dark:bg-slate-700 rounded"></div>
                           </div>
                         ))}
                         <div className="mt-auto h-8 w-full border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-lg flex items-center justify-center">
                           <div className="h-3 w-16 bg-slate-200 dark:bg-slate-700 rounded"></div>
                         </div>
                      </div>
                      <div className="flex-1 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-4 flex flex-col gap-4">
                        <div className="flex justify-between items-center pb-4 border-b border-slate-100 dark:border-slate-700">
                          <div className="h-5 w-32 bg-slate-200 dark:bg-slate-700 rounded"></div>
                          <div className="h-6 w-20 bg-emerald-100 dark:bg-emerald-900/30 rounded-full"></div>
                        </div>
                        <div className="flex-1 flex items-center justify-center">
                          <div className="relative w-48 h-48 rounded-full border-[16px] border-slate-50 dark:border-slate-900 flex items-center justify-center">
                             <div className="absolute inset-[-16px] rounded-full border-[16px] border-violet-500 border-r-transparent border-b-transparent transform rotate-45"></div>
                             <div className="absolute inset-[-16px] rounded-full border-[16px] border-blue-500 border-l-transparent border-t-transparent transform -rotate-12"></div>
                             <div className="text-center">
                               <div className="h-4 w-16 bg-slate-200 dark:bg-slate-700 rounded mx-auto mb-2"></div>
                               <div className="h-6 w-24 bg-slate-800 dark:bg-slate-200 rounded mx-auto"></div>
                             </div>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {activeTab === "ai" && (
                    <motion.div
                      key="ai"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                      className="h-full flex flex-col max-w-lg mx-auto bg-white dark:bg-slate-800 rounded-2xl border border-emerald-200 dark:border-emerald-900/50 shadow-xl overflow-hidden"
                    >
                      <div className="bg-emerald-50 dark:bg-emerald-900/20 p-4 flex items-center gap-3 border-b border-emerald-100 dark:border-emerald-900/50">
                        <div className="w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center text-white shrink-0">
                          <Bot className="w-4 h-4" />
                        </div>
                        <div>
                          <div className="h-4 w-24 bg-emerald-200 dark:bg-emerald-700/50 rounded mb-1"></div>
                          <div className="h-2 w-16 bg-emerald-100 dark:bg-emerald-800/50 rounded"></div>
                        </div>
                      </div>
                      <div className="flex-1 p-4 flex flex-col gap-4">
                        <div className="self-end bg-blue-500 text-white p-3 rounded-2xl rounded-tr-sm max-w-[80%] text-sm">
                          Find me a high-strength steel alternative for a marine environment.
                        </div>
                        <div className="self-start bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 p-3 rounded-2xl rounded-tl-sm max-w-[90%] text-sm space-y-2">
                          <p>For marine environments, you need excellent corrosion resistance. I recommend looking at:</p>
                          <div className="bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center gap-2">
                            <div className="w-6 h-6 rounded bg-emerald-100 dark:bg-emerald-900/30"></div>
                            <div className="h-3 w-24 bg-slate-200 dark:bg-slate-700 rounded"></div>
                          </div>
                          <div className="bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center gap-2">
                            <div className="w-6 h-6 rounded bg-emerald-100 dark:bg-emerald-900/30"></div>
                            <div className="h-3 w-32 bg-slate-200 dark:bg-slate-700 rounded"></div>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {activeTab === "cbam" && (
                    <motion.div
                      key="cbam"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                      className="h-full bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-6 flex flex-col"
                    >
                      <div className="flex items-center gap-4 mb-8">
                        <div className="w-12 h-12 rounded-xl bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center text-amber-600">
                          <Target className="w-6 h-6" />
                        </div>
                        <div>
                          <div className="h-5 w-48 bg-slate-200 dark:bg-slate-700 rounded mb-2"></div>
                          <div className="h-3 w-32 bg-slate-100 dark:bg-slate-800 rounded"></div>
                        </div>
                      </div>
                      <div className="flex-1 flex gap-6">
                        <div className="w-1/2 space-y-4">
                          {[1, 2, 3].map(i => (
                            <div key={i}>
                              <div className="flex justify-between mb-1">
                                <div className="h-3 w-20 bg-slate-200 dark:bg-slate-700 rounded"></div>
                                <div className="h-3 w-12 bg-slate-200 dark:bg-slate-700 rounded"></div>
                              </div>
                              <div className="h-2 w-full bg-slate-100 dark:bg-slate-900 rounded-full overflow-hidden">
                                <div className={`h-full ${i === 1 ? 'bg-amber-500 w-3/4' : i === 2 ? 'bg-rose-500 w-1/2' : 'bg-emerald-500 w-1/4'}`}></div>
                              </div>
                            </div>
                          ))}
                        </div>
                        <div className="w-1/2 bg-slate-50 dark:bg-slate-900 rounded-xl p-4 flex flex-col justify-center items-center text-center border border-slate-100 dark:border-slate-800">
                           <div className="h-4 w-24 bg-slate-200 dark:bg-slate-700 rounded mb-4"></div>
                           <div className="h-10 w-32 bg-amber-500 dark:bg-amber-600 rounded-lg mb-2"></div>
                           <div className="h-3 w-40 bg-slate-200 dark:bg-slate-700 rounded"></div>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
