"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, BookOpen, Database, Target, BrainCircuit, ShieldCheck, Cpu, TestTube2, CheckCircle2, MessageSquare, ThumbsUp } from "lucide-react";
import { API } from "@/lib/api";
import { InteractiveFeatures } from "@/components/InteractiveFeatures";
import { CbamLeadMagnet } from "@/components/CbamLeadMagnet";

export default function LandingPage() {
  const [currency, setCurrency] = useState<"INR" | "USD" | "EUR">("USD");
  const getPrice = (inr: number, usd: string, eur: string) => {
    if (currency === "USD") return `$${usd}`;
    if (currency === "EUR") return `€${eur}`;
    return `₹${inr}`;
  };
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [authChecked, setAuthChecked] = useState(false);
  
  useEffect(() => {
    // Capture Google OAuth token if present
    const urlParams = new URLSearchParams(window.location.search);
    const oauthToken = urlParams.get("t");
    if (oauthToken) {
      localStorage.setItem("token", oauthToken);
      localStorage.removeItem("tourCompleted"); localStorage.removeItem("ai_chat_history"); window.location.href = "/";
      return;
    }

    // Check auth — validate token before trusting it
    const token = localStorage.getItem("token");
    if (token) {
      fetch(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(r => {
          if (r.ok) {
            setIsLoggedIn(true);
          } else {
            // Token expired — clear stale session
            localStorage.removeItem("token");
            setIsLoggedIn(false);
          }
          setAuthChecked(true);
        })
        .catch(() => {
          localStorage.removeItem("token");
          setIsLoggedIn(false);
          setAuthChecked(true);
        });
    } else {
      setAuthChecked(true);
    }

    // Check query params for ?login=true
    if (window.location.search.includes('login=true')) {
      window.dispatchEvent(new Event("openLoginModal"));
    }
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-200 transition-colors duration-300 selection:bg-indigo-500/30 overflow-x-hidden font-sans">
      
      {/* Navbar */}
      

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 px-6">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-400/20 dark:bg-indigo-600/10 rounded-full blur-[120px] pointer-events-none"></div>
        <div className="max-w-5xl mx-auto text-center relative z-10">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-700 dark:text-indigo-300 text-xs font-semibold uppercase tracking-widest mb-6">
              <Database className="w-3.5 h-3.5" /> The Engineering Material Platform
            </div>
            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-slate-900 dark:text-white mb-6 font-heading leading-tight">
              Find the right material. <br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">Synthesize what&apos;s missing.</span>
            </h1>
            <p className="text-lg md:text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed font-light">
              Search 6,500+ engineering materials, let AI synthesize custom grades, estimate preliminary EU CBAM exposure, and integrate via API — pay once, use forever.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
              {authChecked && !isLoggedIn && (
                <>
                  <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="flex items-center gap-2 px-8 py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-all shadow-xl shadow-indigo-600/20 w-full sm:w-auto justify-center">
                    Access Platform <ArrowRight className="w-4 h-4" />
                  </button>
                  <Link href="/materials" className="flex items-center gap-2 px-7 py-3.5 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-800 rounded-xl font-bold transition-all w-full sm:w-auto justify-center">
                    Explore 6,500+ Materials
                  </Link>
                </>
              )}
              {authChecked && isLoggedIn && (
                <>
                  <Link href="/dashboard" className="flex items-center gap-2 px-8 py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-all shadow-xl shadow-indigo-600/20 w-full sm:w-auto justify-center">
                    Go to Dashboard <ArrowRight className="w-4 h-4" />
                  </Link>
                  <Link href="/materials" className="flex items-center gap-2 px-7 py-3.5 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-800 rounded-xl font-bold transition-all w-full sm:w-auto justify-center">
                    Browse 6,500+ Materials
                  </Link>
                </>
              )}
            </div>

            {/* Social Proof Stats */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 max-w-3xl mx-auto pt-4 border-t border-slate-200/70 dark:border-slate-800/70">
              {[
                { value: "6,500+", label: "Engineering Materials" },
                { value: "6", label: "Global Standards" },
                { value: "AI", label: "Material Synthesizer" },
                { value: "REST API", label: "Developer Access" },
              ].map((stat, i) => (
                <div key={i} className="text-center">
                  <div className="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white">{stat.value}</div>
                  <div className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mt-1">{stat.label}</div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Problem Section */}
      <section id="problem" className="py-24 bg-white dark:bg-slate-900/50 border-y border-slate-200 dark:border-slate-800/50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-6 font-heading">Material selection shouldn&apos;t require 12 browser tabs.</h2>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed mb-6">
                Engineers and material scientists waste hours cross-referencing scattered databases, supplier PDFs, and pricing spreadsheets just to make a single material decision.
              </p>
              <ul className="space-y-4">
                {["Supplier datasheets that contradict each other on the same alloy", "No way to quickly compare cost vs. strength vs. embodied carbon", "Hours spent on BOM and CBAM estimates that can be modeled in seconds"].map((item, i) => (
                  <li key={i} className="flex items-start gap-3 text-slate-600 dark:text-slate-300">
                    <Target className="w-5 h-5 text-rose-600 dark:text-rose-400 shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="bg-white dark:bg-slate-950 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 blur-[50px]"></div>
              
              <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4 mb-5 relative z-10">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center border border-indigo-500/20">
                    <Database className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  </div>
                  <div>
                    <div className="text-sm font-bold text-slate-900 dark:text-white">Unified Material Matrix</div>
                    <div className="text-xs text-slate-500 dark:text-slate-400">6,511 indexed grades • ASTM / ISO / DIN / EN / JIS</div>
                  </div>
                </div>
                <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
                  Live Index
                </span>
              </div>

              <div className="space-y-3 relative z-10">
                {[
                  { name: "AISI 4140 Alloy Steel", std: "ASTM A29 • Metal", yield: "415–655 MPa", density: "7.85 g/cm³", badge: "Cross-Validated" },
                  { name: "Titanium Grade 2 (CP)", std: "ASTM B265 • Titanium", yield: "275–345 MPa", density: "4.51 g/cm³", badge: "Aerospace / Marine" },
                  { name: "PTFE (Fluoropolymer)", std: "ASTM D4894 • Polymer", yield: "20–35 MPa", density: "2.15 g/cm³", badge: "327°C Melt" },
                ].map((mat, i) => (
                  <div key={i} className="p-3.5 bg-slate-50 dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 flex items-center justify-between gap-4">
                    <div>
                      <div className="text-sm font-bold text-slate-900 dark:text-white">{mat.name}</div>
                      <div className="text-xs text-slate-500 dark:text-slate-400">{mat.std}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-xs font-semibold text-indigo-600 dark:text-indigo-400">{mat.yield}</div>
                      <div className="text-[11px] text-slate-500 dark:text-slate-400">{mat.density} • {mat.badge}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* Solution Section */}
      <InteractiveFeatures />

      {/* Database Coverage & Global Standards */}
      <section id="coverage" className="py-24 bg-white dark:bg-slate-900/50 border-y border-slate-200 dark:border-slate-800/50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4 font-heading">
              6,500+ Engineering Grades. Cross-Referenced Globally.
            </h2>
            <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
              Every material profile unifies mechanical, thermal, electrical, and environmental properties alongside international standard equivalents.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-12">
            {[
              {
                icon: Cpu,
                title: "Metals, Steels & Superalloys",
                badge: "Ferrous & Non-Ferrous",
                desc: "Structural steels, stainless alloys, aluminum series, titanium grades, copper castings, and nickel superalloys with yield, tensile, hardness, and fatigue data.",
              },
              {
                icon: TestTube2,
                title: "Polymers, Ceramics & Composites",
                badge: "Advanced Materials",
                desc: "Engineering thermoplastics, fluoropolymers, elastomers, technical ceramics, and Rule-of-Mixtures hybrid composite synthesis for weight-critical assemblies.",
              },
              {
                icon: ShieldCheck,
                title: "BOM & CBAM Cost Estimator (Beta)",
                badge: "Preliminary Exposure",
                desc: "Upload multi-part Bills of Materials to roll up assembly weight, cost, and preliminary EU CBAM carbon-cost estimates by CN prefix and origin country.",
              },
            ].map((card, i) => (
              <div key={i} className="p-8 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-lg flex flex-col">
                <div className="flex items-center justify-between gap-3 mb-5">
                  <div className="w-11 h-11 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
                    <card.icon className="w-5 h-5" />
                  </div>
                  <span className="text-[11px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-slate-200/70 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                    {card.badge}
                  </span>
                </div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3 font-heading">{card.title}</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed flex-1">{card.desc}</p>
              </div>
            ))}
          </div>

          <div className="flex flex-col md:flex-row items-center justify-between gap-6 p-6 rounded-2xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mr-2">Indexed Standards:</span>
              {["ASTM / UNS", "ISO", "EN", "DIN", "JIS", "IS / GB"].map((std) => (
                <span key={std} className="px-3 py-1 text-xs font-bold rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300">
                  {std}
                </span>
              ))}
            </div>
            <Link href="/feedback" className="inline-flex items-center gap-2 px-5 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white rounded-xl font-semibold transition-colors text-xs border border-slate-300 dark:border-slate-700 shrink-0">
              <MessageSquare className="w-4 h-4" /> Request a Grade or Share Pilot Feedback
            </Link>
          </div>
        </div>
      </section>

      <CbamLeadMagnet />

      {/* Pricing */}
      <section id="pricing" className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4 font-heading">Pay Once. Use Forever. Lifetime Deals.</h2>
          <p className="text-slate-600 dark:text-slate-400">Skip the monthly subscriptions. Grab a lifetime deal before we switch to MRR monthly pricing on <strong>January 1st, 2027</strong>. No credit card required to start free.</p>
          
          <div className="flex justify-center items-center gap-2 mt-6">
             <button onClick={() => setCurrency("USD")} className={`px-4 py-1.5 rounded-full text-sm font-bold transition-all ${currency === "USD" ? "bg-emerald-500 text-white" : "bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-300 dark:hover:bg-slate-700"}`}>USD</button>
             <button onClick={() => setCurrency("EUR")} className={`px-4 py-1.5 rounded-full text-sm font-bold transition-all ${currency === "EUR" ? "bg-emerald-500 text-white" : "bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-300 dark:hover:bg-slate-700"}`}>EUR</button>
             <button onClick={() => setCurrency("INR")} className={`px-4 py-1.5 rounded-full text-sm font-bold transition-all ${currency === "INR" ? "bg-emerald-500 text-white" : "bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-300 dark:hover:bg-slate-700"}`}>INR</button>
          </div>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            
            {/* Free */}
            <div className="bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 flex flex-col">
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2 font-heading">Academic Free</h3>
              <p className="text-slate-600 dark:text-slate-400 text-sm mb-6 h-10">Perfect for students and open research.</p>
              <div className="text-4xl font-extrabold text-slate-900 dark:text-white mb-8">{getPrice(0, "0", "0")}<span className="text-sm font-medium text-slate-500 dark:text-slate-400">/lifetime</span></div>
              <ul className="space-y-3 mb-8 flex-1">
                {["Search 100+ basic materials", "View mechanical properties", "Basic AI Adviser", "Community Support"].map((f, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" /> {f}
                  </li>
                ))}
              </ul>
              {isLoggedIn ? <Link href="/dashboard" className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Go to Dashboard</Link> : <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Start Free</button>}
            </div>

            {/* Pro */}
            <div className="bg-slate-50 dark:bg-slate-900 border-2 border-indigo-500 rounded-2xl p-8 flex flex-col relative transform md:-translate-y-4 shadow-2xl shadow-indigo-900/20">
              <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-indigo-500 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Most Popular</div>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2 font-heading">Professional</h3>
              <p className="text-slate-600 dark:text-slate-400 text-sm mb-6 h-10">For independent engineers and small firms.</p>
              <div className="text-4xl font-extrabold text-slate-900 dark:text-white mb-8">{getPrice(499, "5.99", "5.49")}<span className="text-sm font-medium text-slate-500 dark:text-slate-400">/lifetime</span></div>
              <ul className="space-y-3 mb-8 flex-1">
                {["Full 6,500+ material database", "Export detailed PDFs", "Advanced AI Adviser", "Unlimited Workspaces"].map((f, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-indigo-600 dark:text-indigo-600 dark:text-indigo-400" /> {f}
                  </li>
                ))}
              </ul>
              {isLoggedIn ? <Link href="/account" className="block text-center w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition-colors">Upgrade in Account</Link> : <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition-colors">Upgrade to Pro</button>}
            </div>

            {/* Advanced */}
            <div className="bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 flex flex-col">
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2 font-heading">Advanced Enterprise</h3>
              <p className="text-slate-600 dark:text-slate-400 text-sm mb-6 h-10">Full financial & physics capabilities.</p>
              <div className="text-4xl font-extrabold text-slate-900 dark:text-white mb-8">Custom<span className="text-sm font-medium text-slate-500 dark:text-slate-400">/enterprise</span></div>
              <ul className="space-y-3 mb-8 flex-1">
                {["Priority email support", "Google sign-in (OAuth 2.0)", "Regulation data updates when the Commission republishes", "CBAM Cost Estimator (Beta) & Exports", "REST API access (10,000 requests/day)"].map((f, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-amber-500" /> {f}
                  </li>
                ))}
              </ul>
              {isLoggedIn ? <Link href="/account" className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Upgrade in Account</Link> : <button onClick={() => window.dispatchEvent(new Event("openLoginModal"))} className="block text-center w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-bold transition-colors">Get Advanced</button>}
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
          <p className="text-slate-500 dark:text-slate-400 text-sm">© 2026 MatDataHub. The smartest way to choose engineering materials.</p>
          <div className="flex gap-6">
            <Link href="/terms" className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-900 dark:text-white transition-colors">Terms & Conditions</Link>
            <Link href="/privacy" className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-900 dark:text-white transition-colors">Privacy Policy</Link>
            <Link href="/contact" className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-900 dark:text-white transition-colors">Contact</Link>
            <Link href="/admin" className="text-sm text-amber-600 dark:text-amber-500 hover:text-amber-700 dark:hover:text-amber-400 transition-colors font-bold">Admin Login</Link>
          </div>
        </div>
      </footer>
      
    </div>
  );
}
