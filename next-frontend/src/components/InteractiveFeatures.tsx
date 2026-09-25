"use client";
import { useState, useEffect } from "react";
import { 
  Database, Workflow, Target, Bot, 
  Search, SlidersHorizontal, Share2, 
  FolderKanban, ShieldAlert, Thermometer, Activity, AlignEndVertical, IndianRupee,
  Scale, Replace, Factory, Layers,
  MessageSquare, BookOpen, Lightbulb, ShieldCheck, Cpu
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const features = [
  {
    id: "database",
    title: "Parametric Database",
    desc: "Search, filter, and extract verified material properties from our global database.",
    icon: Database,
    color: "bg-blue-500",
    tools: [
      { name: "Global Search", desc: "Instantly lookup materials verified by ASTM, ISO, and DIN standards.", icon: Search, use: "Type a material name or grade to view its complete mechanical, thermal, and electrical properties." },
      { name: "Advanced Filtering", desc: "Filter materials by exact property thresholds.", icon: SlidersHorizontal, use: "Use sliders to restrict results (e.g., Density < 3.0 g/cm3, Yield Strength > 400 MPa)." },
      { name: "Export & Share", desc: "Download datasheets for offline analysis.", icon: Share2, use: "Export any material profile to CSV or share its unique secure link with your engineering team." }
    ]
  },
  {
    id: "workspaces",
    title: "Engineering Workspaces",
    desc: "Build assemblies and run structural calculations directly in your browser.",
    icon: Workflow,
    color: "bg-violet-500",
    tools: [
      { name: "Bill of Materials (BOM)", desc: "Manage multi-part assemblies.", icon: FolderKanban, use: "Add components and assign materials to automatically roll up total system weights and costs." },
      { name: "Safety Factor", desc: "Determine ultimate strength limits.", icon: ShieldAlert, use: "Input applied loads and cross-sectional areas to calculate if the material will fail under stress." },
      { name: "Thermal Expansion", desc: "Calculate linear growth.", icon: Thermometer, use: "Input temperature deltas to calculate physical expansion and induced thermal stresses." },
      { name: "Fatigue Life", desc: "Predict material failure cycles.", icon: Activity, use: "Analyze endurance limits under repeated dynamic loading using the S-N curve approximations." },
      { name: "Beam Deflection", desc: "Analyze bending forces.", icon: AlignEndVertical, use: "Input beam length and load types (point/distributed) to find maximum deflection in mm." },
      { name: "Cost Optimizer", desc: "Minimize assembly costs.", icon: IndianRupee, use: "Compare current BOM costs against alternative materials to find the most economical substitutions." }
    ]
  },
  {
    id: "analytics",
    title: "Analytics Suite",
    desc: "Deep-dive analysis tools for material substitution and ESG compliance.",
    icon: Target,
    color: "bg-amber-500",
    tools: [
      { name: "Side-by-Side Compare", desc: "Visual radar fingerprinting.", icon: Scale, use: "Select up to 3 materials to overlay their properties on a radar chart and extract AI-driven takeaways." },
      { name: "AI Substitution", desc: "Multi-objective optimization.", icon: Replace, use: "Input a baseline material and set weights for Cost, Density, and Carbon Footprint to find the optimal replacement." },
      { name: "CBAM Emissions", desc: "EU Carbon Tax prediction.", icon: Factory, use: "Calculate predictive Carbon Border Adjustment Mechanism taxes based on your procurement volume." },
      { name: "Composite Synthesizer", desc: "Predict hybrid properties.", icon: Layers, use: "Blend a matrix and fiber using the Rule of Mixtures to generate theoretical properties for a custom composite." }
    ]
  },
  {
    id: "ai",
    title: "AI Materials Adviser",
    desc: "Your dedicated engineering assistant for standards and alternatives.",
    icon: Bot,
    color: "bg-emerald-500",
    tools: [
      { name: "Context-Aware Chat", desc: "Engineering-focused conversational AI.", icon: MessageSquare, use: "Open the floating widget on any page to ask highly technical questions about materials and physics." },
      { name: "Standard Lookups", desc: "Cross-reference global indices.", icon: BookOpen, use: "Ask the AI to find exact equivalents (e.g., 'What is the DIN equivalent of ASTM A36?')." },
      { name: "Design Recommendations", desc: "Constraint-based material selection.", icon: Lightbulb, use: "Describe your environment (e.g., 'high-strength alloy for a corrosive marine environment') and receive tailored suggestions." }
    ]
  },
  {
    id: "admin",
    title: "Admin, API & Growth",
    desc: "Enterprise-grade access control, API provisioning, and automated DB expansion.",
    icon: ShieldCheck,
    color: "bg-purple-600",
    tools: [
      { name: "Role-Based Access (RBAC)", desc: "Secure multi-user permissions.", icon: ShieldCheck, use: "JWT-based true RBAC to safely manage admin capabilities, block users, and audit platform security." },
      { name: "AI Material Synthesizer", desc: "Automated DB expansion.", icon: Bot, use: "Admins can type a material family (e.g., 'Inconel') and the Groq LLM instantly synthesizes properties for multiple specific grades directly into the database." },
      { name: "Developer API Access", desc: "Programmatic platform integration.", icon: Cpu, use: "Advanced tier users can generate secure API keys (Client ID & Secret) to query the material database directly from their own Python or Node.js backends." }
    ]
  }
];

export function InteractiveFeatures() {
  const [activeTab, setActiveTab] = useState(features[0].id);

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveTab((current) => {
        const currentIndex = features.findIndex((f) => f.id === current);
        return features[(currentIndex + 1) % features.length].id;
      });
    }, 10000);
    return () => clearInterval(timer);
  }, []);

  const activeFeat = features.find(f => f.id === activeTab) || features[0];

  return (
    <section id="solution" className="py-24 px-6 bg-slate-50 dark:bg-slate-900/50 relative overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-500/5 dark:bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
      
      <div className="max-w-7xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-slate-900 dark:text-white mb-6 font-heading">
            One platform. <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-violet-600">Every material decision.</span>
          </h2>
          <p className="text-slate-600 dark:text-slate-400 max-w-3xl mx-auto text-lg">
            From searching a material database to building a Bill of Materials to predicting EU carbon taxes — MatDataHub replaces the spreadsheets, PDFs, and guesswork.
          </p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8 lg:gap-12 items-start">
          {/* Tabs Menu */}
          <div className="w-full lg:w-1/3 flex flex-col gap-3 lg:sticky lg:top-24">
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

          {/* Tools Panel */}
          <div className="w-full lg:w-2/3">
            <div className="bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-2xl overflow-hidden">
              {/* Header */}
              <div className="bg-slate-100 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 p-6">
                <AnimatePresence mode="wait">
                  <motion.div 
                    key={activeTab}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ duration: 0.2 }}
                    className="flex items-center gap-4"
                  >
                    <div className={`p-3 rounded-2xl text-white ${activeFeat.color}`}>
                      <activeFeat.icon className="w-8 h-8" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-slate-900 dark:text-white font-heading">{activeFeat.title}</h3>
                      <p className="text-slate-500 dark:text-slate-400 mt-1">{activeFeat.desc}</p>
                    </div>
                  </motion.div>
                </AnimatePresence>
              </div>

              {/* Tool Cards */}
              <div className="p-6">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={activeTab + "-tools"}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3 }}
                    className="grid grid-cols-1 md:grid-cols-2 gap-4"
                  >
                    {activeFeat.tools.map((tool, i) => (
                      <div key={i} className="bg-slate-50 dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 hover:shadow-md hover:border-slate-300 dark:hover:border-slate-700 transition-shadow group flex flex-col h-full">
                        <div className="flex items-center gap-3 mb-3">
                          <div className="p-2 rounded-lg bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 group-hover:bg-blue-100 dark:group-hover:bg-blue-900/40 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors shadow-sm">
                            <tool.icon className="w-5 h-5" />
                          </div>
                          <h4 className="font-bold text-slate-900 dark:text-white text-md font-heading">{tool.name}</h4>
                        </div>
                        <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">{tool.desc}</p>
                        <div className="mt-auto pt-3 border-t border-slate-200 dark:border-slate-700">
                          <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                            <span className="font-bold text-slate-700 dark:text-slate-400 block mb-1">How it works:</span>
                            {tool.use}
                          </p>
                        </div>
                      </div>
                    ))}
                  </motion.div>
                </AnimatePresence>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
