"use client";
import Link from "next/link";
import { Database, Calculator, Workflow, Bot, BookOpen, ArrowRight } from "lucide-react";

export default function Home() {
  return (
    <main className="relative flex flex-col items-center justify-start min-h-screen pt-12 pb-24 px-6 lg:px-12 overflow-hidden">
      
      {/* Glassmorphism Background Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-600/10 blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-emerald-600/10 blur-[120px] pointer-events-none"></div>

      <div className="w-full max-w-5xl text-center space-y-10 relative z-10">
        
        <div className="space-y-6">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-blue-500/30 bg-blue-500/10 text-blue-400 text-sm font-bold uppercase tracking-wider backdrop-blur-md hover:bg-blue-500/20 transition-colors cursor-default">
            <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
            Welcome to the Next Generation
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-br from-white via-slate-200 to-slate-500 drop-shadow-sm">
            MatDataHub OS
          </h1>
          <p className="text-base md:text-xl text-slate-400 max-w-2xl mx-auto font-medium">
            Your centralized platform for engineering physics, materials data, and financial analytics.
          </p>
        </div>

        {/* Featured Engineering Blog Banner */}
        <div className="pt-6">
          <Link href="/resources" onClick={() => alert('Coming soon in the next release!')} className="group relative block overflow-hidden rounded-3xl border border-indigo-500/30 bg-indigo-950/20 text-left transition-all hover:bg-indigo-900/40 hover:border-indigo-500/60 hover:shadow-[0_0_40px_-10px_rgba(99,102,241,0.2)] backdrop-blur-sm">
            <div className="absolute top-0 left-0 w-1.5 h-full bg-gradient-to-b from-indigo-400 to-purple-500"></div>
            <div className="p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
              <div className="space-y-3 max-w-2xl">
                <div className="flex items-center gap-3">
                  <span className="px-2.5 py-1 text-[10px] font-black uppercase tracking-widest bg-indigo-500 text-white rounded-md shadow-lg">New Research</span>
                  <span className="text-xs font-bold text-slate-400">Sept 4, 2026 • 8 min read</span>
                </div>
                <h2 className="text-xl md:text-2xl font-bold text-white group-hover:text-indigo-300 transition-colors leading-tight">Modeling Thermal Expansion in Aerospace Alloys</h2>
                <p className="text-slate-400 text-sm md:text-base leading-relaxed">Deep dive into isotropic thermal expansion formulas and why Titanium out-performs Aluminum 7075.</p>
              </div>
              <div className="hidden md:flex flex-shrink-0 items-center justify-center p-4 bg-indigo-900/40 border border-indigo-500/20 rounded-2xl group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300 shadow-xl">
                <BookOpen className="w-8 h-8 text-indigo-400" />
              </div>
            </div>
          </Link>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 pt-8">
          
          <Link href="/materials" className="group p-8 rounded-3xl bg-slate-900/50 border border-slate-700/50 hover:border-emerald-500/50 hover:bg-slate-800/80 transition-all backdrop-blur-sm hover:shadow-[0_0_30px_-10px_rgba(16,185,129,0.15)] hover:-translate-y-1">
            <div className="w-14 h-14 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
              <Database className="w-7 h-7" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Browse Materials</h3>
            <p className="text-slate-400 text-sm leading-relaxed mb-6">Access 1000+ verified engineering materials and their physical properties.</p>
            <div className="text-xs font-bold text-emerald-400 flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              Explore Database <ArrowRight className="w-3 h-3" />
            </div>
          </Link>

          <Link href="/projects" className="group p-8 rounded-3xl bg-slate-900/50 border border-slate-700/50 hover:border-orange-500/50 hover:bg-slate-800/80 transition-all backdrop-blur-sm hover:shadow-[0_0_30px_-10px_rgba(249,115,22,0.15)] hover:-translate-y-1">
            <div className="w-14 h-14 rounded-2xl bg-orange-500/10 border border-orange-500/20 text-orange-400 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
              <Workflow className="w-7 h-7" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Project Workflows</h3>
            <p className="text-slate-400 text-sm leading-relaxed mb-6">Create, save, and manage complex material selection workflows.</p>
            <div className="text-xs font-bold text-orange-400 flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              View Workflows <ArrowRight className="w-3 h-3" />
            </div>
          </Link>

          <Link href="/ai" className="group p-8 rounded-3xl bg-slate-900/50 border border-slate-700/50 hover:border-blue-500/50 hover:bg-slate-800/80 transition-all backdrop-blur-sm hover:shadow-[0_0_30px_-10px_rgba(59,130,246,0.15)] hover:-translate-y-1">
            <div className="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
              <Bot className="w-7 h-7" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Ask AI Adviser</h3>
            <p className="text-slate-400 text-sm leading-relaxed mb-6">Describe constraints in plain English and let AI find the perfect material.</p>
            <div className="text-xs font-bold text-blue-400 flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              Ask Adviser <ArrowRight className="w-3 h-3" />
            </div>
          </Link>

        </div>

      </div>
    </main>
  );
}
