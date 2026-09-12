"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, BookOpen, Database, Target, BrainCircuit, ShieldCheck, Cpu, TestTube2, CheckCircle2, MessageSquare, ThumbsUp } from "lucide-react";
import { API } from "@/lib/api";

export default function LandingPage() {
  const [feedbacks, setFeedbacks] = useState<any[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [authChecked, setAuthChecked] = useState(false);
  
  useEffect(() => {
    // Capture Google OAuth token if present
    const urlParams = new URLSearchParams(window.location.search);
    const oauthToken = urlParams.get("t");
    if (oauthToken) {
      localStorage.setItem("token", oauthToken);
      window.history.replaceState({}, "", "/");
    }

    // Check auth
    const token = localStorage.getItem("token");
    if (token) setIsLoggedIn(true);
    setAuthChecked(true);

    // Check query params for ?login=true
    if (window.location.search.includes('login=true')) {
      window.dispatchEvent(new Event("openLoginModal"));
    }
  }, []);

  useEffect(() => {
    fetch(`${API}/feedback/public`)
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          // get top 3 most helpful feedbacks or just latest 3
          const sorted = data.filter(f => !f.parent_id).sort((a, b) => (b.helpful_votes || 0) - (a.helpful_votes || 0)).slice(0, 3);
          setFeedbacks(sorted);
        }
      })
      .catch(console.error);
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-white dark:bg-slate-950 text-white dark:text-slate-200 transition-colors duration-300 selection:bg-indigo-500/30 overflow-x-hidden font-sans">
      
      {/* Navbar */}
      

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 px-6">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-400/20 dark:bg-indigo-600/10 rounded-full blur-[120px] pointer-events-none"></div>
        <div className="max-w-5xl mx-auto text-center relative z-10">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-700 dark:text-indigo-300 text-xs font-semibold uppercase tracking-widest mb-6">
              <BookOpen className="w-3.5 h-3.5" /> Academic-Grade Materials Intelligence
            </div>
            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-slate-900 dark:text-white mb-6 font-heading leading-tight">
              Engineering decisions, <br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">backed by physics.</span>
            </h1>
            <p className="text-lg md:text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed font-light">
              A unified platform for mechanical properties, macroeconomic cost indices, and AI-driven substitution analysis. Designed for the rigor of modern R&D.
            </p>
                          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                {authChecked && !isLoggedIn && (
                  <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="flex items-center gap-2 px-8 py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-all shadow-xl shadow-indigo-600/20 w-full sm:w-auto justify-center">
                    Access Platform <ArrowRight className="w-4 h-4" />
                  </button>
                )}
              </div>
          </motion.div>
        </div>
      </section>

      {/* Problem Section */}
      <section id="problem" className="py-24 bg-white dark:bg-slate-50 dark:bg-slate-900/50 border-y border-slate-200 dark:border-slate-200 dark:border-slate-800/50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6 font-heading">The Data Fragmentation Problem</h2>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed mb-6">
                Engineers and material scientists spend countless hours cross-referencing isolated databases to find mechanical limits, pricing estimates, and ESG compliance factors (like CBAM).
              </p>
              <ul className="space-y-4">
                {["Inconsistent datasheets from different suppliers", "Lack of historical pricing trends for accurate BOM estimation", "Disconnect between mechanical viability and financial reality"].map((item, i) => (
                  <li key={i} className="flex items-start gap-3 text-slate-600 dark:text-slate-300">
                    <Target className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="bg-white dark:bg-slate-950 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 blur-[50px]"></div>
              
              <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4 mb-6 relative z-10">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-indigo-900/30 flex items-center justify-center border border-indigo-500/20">
                    <Database className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  </div>
                  <div>
                    <div className="h-2.5 w-24 bg-slate-700 rounded mb-1.5"></div>
                    <div className="h-2 w-16 bg-slate-100 dark:bg-slate-800 rounded"></div>
                  </div>
                </div>
                <div className="flex gap-1.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
                  <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
                  <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
                </div>
              </div>

              <div className="space-y-4 relative z-10 opacity-70 group-hover:opacity-100 transition-opacity">
                <div className="flex gap-4">
                  <div className="flex-1 h-24 bg-slate-50 dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-4">
                    <div className="h-2 w-1/3 bg-slate-700 rounded mb-4"></div>
                    <div className="h-8 w-2/3 bg-indigo-500/20 rounded"></div>
                  </div>
                  <div className="flex-1 h-24 bg-slate-50 dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-4">
                    <div className="h-2 w-1/3 bg-slate-700 rounded mb-4"></div>
                    <div className="h-8 w-2/3 bg-emerald-500/20 rounded"></div>
                  </div>
                </div>
                <div className="h-32 w-full bg-slate-50 dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-4 flex items-end gap-2">
                  {[40, 70, 45, 90, 65, 80, 50, 100, 75, 85].map((h, i) => (
                    <div key={i} className="flex-1 bg-indigo-500/40 rounded-t-sm" style={{ height: `${h}%` }}></div>
                  ))}
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section id="solution" className="py-24 px-6">
        <div className="max-w-7xl mx-auto text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4 font-heading">A Unified Academic & Industrial Solution</h2>
          <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">MatDataHub bridges the gap between theoretical material science and practical engineering economics.</p>
        </div>
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            { title: "Parametric Database", desc: "Search thousands of materials with verified mechanical, thermal, and electrical properties.", icon: Database, color: "text-blue-400" },
            { title: "Macroeconomic Pricing", desc: "Analyze supply chain risks and cost-per-kg trends mapped via trailing global indices.", icon: ShieldCheck, color: "text-emerald-600 dark:text-emerald-400" },
            { title: "AI Substitution", desc: "Use advanced algorithms to discover alternative materials based on multi-objective constraints.", icon: BrainCircuit, color: "text-purple-400" },
            { title: "CBAM Emissions", desc: "Calculate predictive Carbon Border Adjustment Mechanism taxes for EU procurement.", icon: Target, color: "text-amber-400" },
            { title: "Engineering Workspaces", desc: "Calculate beam deflection, thermal shock, and safety factors directly in your browser.", icon: Cpu, color: "text-rose-400" },
            { title: "Composite Synthesizer", desc: "Blend theoretical materials using Rule of Mixtures to predict hybrid properties.", icon: TestTube2, color: "text-cyan-400" },
          ].map((feat, i) => (
            <div key={i} className="bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl hover:bg-slate-100 dark:hover:bg-slate-100 dark:hover:bg-slate-800/40 transition-colors">
              <feat.icon className={`w-8 h-8 ${feat.color} mb-5`} />
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2 font-heading">{feat.title}</h3>
              <p className="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">{feat.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Featured Blog Banner */}
      <section id="blog" className="py-12 px-6">
        <div className="max-w-5xl mx-auto">
          <Link href="/resources"  className="group relative block overflow-hidden rounded-3xl border border-indigo-500/30 bg-white dark:bg-indigo-950/20 text-left transition-all hover:shadow-2xl shadow-lg border-slate-200 dark:border-indigo-500/30 hover:border-indigo-500/60 hover:shadow-[0_0_40px_-10px_rgba(99,102,241,0.2)] backdrop-blur-sm">
            <div className="absolute top-0 left-0 w-1.5 h-full bg-gradient-to-b from-indigo-400 to-purple-500"></div>
            <div className="p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
              <div className="space-y-3 max-w-2xl">
                <div className="flex items-center gap-3">
                  <span className="px-2.5 py-1 text-[10px] font-black uppercase tracking-widest bg-indigo-500 text-white rounded-md shadow-lg">New Research</span>
                  <span className="text-xs font-bold text-slate-600 dark:text-slate-400">Sept 4, 2026 • 8 min read</span>
                </div>
                <h2 className="text-xl md:text-2xl font-bold text-slate-900 dark:text-white group-hover:text-indigo-700 dark:hover:text-indigo-300 transition-colors leading-tight font-heading">Modeling Thermal Expansion in Aerospace Alloys</h2>
                <p className="text-slate-600 dark:text-slate-400 text-sm leading-relaxed max-w-xl">
                  A deep dive into how our new predictive modeling engine handles extreme temperature deltas in titanium composites compared to legacy FEM solvers.
                </p>
              </div>
              <div className="shrink-0 flex items-center justify-center w-12 h-12 rounded-full bg-indigo-500/20 text-indigo-600 dark:text-indigo-400 group-hover:bg-indigo-500 group-hover:text-white dark:hover:text-white transition-all">
                <ArrowRight className="w-5 h-5" />
              </div>
            </div>
          </Link>
        </div>
      </section>



      {/* Testimonials / Community Feedback */}
      <section className="py-24 bg-white dark:bg-slate-50 dark:bg-slate-900/50 border-y border-slate-200 dark:border-slate-200 dark:border-slate-800/50">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4 font-heading">Live Community Feedback</h2>
          <p className="text-slate-600 dark:text-slate-400 mb-12 max-w-2xl mx-auto">See what our community of engineers and scientists are saying directly from our platform.</p>
          
          <div className="grid md:grid-cols-3 gap-8 text-left">
            {feedbacks.length > 0 ? (
              feedbacks.map((fb, i) => (
                <div key={i} className="p-8 bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl flex flex-col relative overflow-hidden">
                  <div className="absolute top-0 left-0 w-1 h-full bg-indigo-500/50"></div>
                  <div className="flex items-center gap-2 mb-4">
                    <span className="text-xs font-semibold px-2 py-0.5 bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 rounded-full border border-indigo-700/50">{fb.category}</span>
                  </div>
                  <p className="text-slate-600 dark:text-slate-300 relative z-10 mb-6 text-sm leading-relaxed italic flex-1">"{fb.message}"</p>
                  <div className="flex justify-between items-end border-t border-slate-200 dark:border-slate-800 pt-4 mt-auto">
                    <div>
                      <p className="text-slate-900 dark:text-white font-bold text-sm">{fb.name || 'Anonymous Engineer'}</p>
                      <p className="text-slate-500 text-[10px]">{new Date(fb.created_at).toLocaleDateString()}</p>
                    </div>
                    <div className="flex items-center gap-1.5 text-xs text-slate-600 dark:text-slate-400">
                      <ThumbsUp className="w-3.5 h-3.5" /> {fb.helpful_votes || 0}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              // Fallback if no feedbacks loaded yet
              [
                { quote: "MatDataHub completely changed how we estimate aerospace BOM costs. The multi-objective substitution tool saved us months of R&D.", author: "Dr. Sarah Jenkins", role: "Lead Materials Scientist" },
                { quote: "Finally, a platform that understands both the physics and the economics of materials. The CBAM calculator is a lifesaver for EU imports.", author: "Marcus Thorne", role: "Supply Chain Director" },
                { quote: "The clean, academic interface makes it a joy to use. It feels like having an expert metallurgist sitting right next to you.", author: "Elena Rodriguez", role: "Mechanical Engineer" }
              ].map((test, i) => (
                <div key={i} className="p-8 bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl relative">
                  <div className="text-4xl text-indigo-500/20 absolute top-4 left-4 font-serif">"</div>
                  <p className="text-slate-600 dark:text-slate-300 relative z-10 mb-6 text-sm leading-relaxed italic flex-1">"{test.quote}"</p>
                  <div>
                    <p className="text-slate-900 dark:text-white font-bold text-sm">{test.author}</p>
                    <p className="text-slate-500 text-xs">{test.role}</p>
                  </div>
                </div>
              ))
            )}
          </div>
          
          <div className="mt-12">
             <Link href="/feedback" className="inline-flex items-center gap-2 px-6 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white rounded-xl font-medium transition-colors text-sm border border-slate-700">
               <MessageSquare className="w-4 h-4" /> View All Community Discussions
             </Link>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4 font-heading">Transparent Pricing Models</h2>
            <p className="text-slate-600 dark:text-slate-400">Select the tier that fits your research and engineering needs.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            
            {/* Free */}
            <div className="bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 flex flex-col">
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2 font-heading">Academic Free</h3>
              <p className="text-slate-600 dark:text-slate-400 text-sm mb-6 h-10">Perfect for students and open research.</p>
              <div className="text-4xl font-extrabold text-slate-900 dark:text-white mb-8">&#8377;0<span className="text-lg font-medium text-slate-500">/mo</span></div>
              <ul className="space-y-3 mb-8 flex-1">
                {["Search limited basic materials", "View mechanical properties", "Basic AI Adviser", "Community Support"].map((f, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" /> {f}
                  </li>
                ))}
              </ul>
              <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Start Free</button>
            </div>

            {/* Pro */}
            <div className="bg-slate-50 dark:bg-slate-900 border-2 border-indigo-500 rounded-2xl p-8 flex flex-col relative transform md:-translate-y-4 shadow-2xl shadow-indigo-900/20">
              <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-indigo-500 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Most Popular</div>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2 font-heading">Professional</h3>
              <p className="text-slate-600 dark:text-slate-400 text-sm mb-6 h-10">For independent engineers and small firms.</p>
              <div className="text-4xl font-extrabold text-slate-900 dark:text-white mb-8">&#8377;499<span className="text-lg font-medium text-slate-500">/mo</span></div>
              <ul className="space-y-3 mb-8 flex-1">
                {["Full 1000+ material database", "Export detailed PDFs", "Advanced AI Adviser", "Unlimited Workspaces"].map((f, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-indigo-600 dark:text-indigo-400" /> {f}
                  </li>
                ))}
              </ul>
              <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition-colors">Upgrade to Pro</button>
            </div>

            {/* Advanced */}
            <div className="bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 flex flex-col">
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2 font-heading">Advanced Enterprise</h3>
              <p className="text-slate-600 dark:text-slate-400 text-sm mb-6 h-10">Full financial & physics capabilities.</p>
              <div className="text-4xl font-extrabold text-slate-900 dark:text-white mb-8">&#8377;19,999<span className="text-lg font-medium text-slate-500">/mo</span></div>
              <ul className="space-y-3 mb-8 flex-1">
                {["Macroeconomic Proxy Pricing", "CBAM Emissions Calculator", "Engineering Physics Tools", "Composite Synthesizer", "Priority API Access"].map((f, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-amber-500" /> {f}
                  </li>
                ))}
              </ul>
              <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Get Advanced</button>
            </div>

          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800 py-12 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <Database className="w-5 h-5 text-indigo-500" />
            <span className="font-bold text-slate-900 dark:text-white">MatDataHub</span>
          </div>
          <p className="text-slate-500 text-sm">© 2026 MatDataHub. Empowering material intelligence.</p>
          <div className="flex gap-6">
            <Link href="/terms" className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-900 dark:text-white transition-colors">Terms & Conditions</Link>
            <Link href="/privacy" className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-900 dark:text-white transition-colors">Privacy Policy</Link>
            <Link href="/contact" className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-900 dark:text-white transition-colors">Contact</Link>
          </div>
        </div>
      </footer>
      
    </div>
  );
}
