import Link from "next/link";
import { Database, Calculator, Workflow, Bot, BookOpen } from "lucide-react";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-[80vh] p-8 lg:p-12">
      <div className="w-full max-w-5xl text-center space-y-8">
        
        <div className="space-y-6">
          <div className="inline-block px-4 py-1.5 rounded-full border border-blue-900/50 bg-blue-900/20 text-blue-400 text-sm font-medium mb-4">
            Welcome to the Next Generation
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-br from-white via-slate-200 to-slate-500">
            MatDataHub OS
          </h1>
          <p className="text-lg md:text-2xl text-slate-200 max-w-3xl mx-auto">
            Your centralized platform for engineering physics, materials data, and financial analytics.
          </p>
        </div>

        {/* Featured Engineering Blog Banner */}
        <div className="pt-10">
          <Link href="/resources" onClick={() => alert('Coming soon in the next release!')} className="group relative block overflow-hidden rounded-3xl border border-indigo-900/50 bg-indigo-950/20 text-left transition-all hover:bg-indigo-900/30 hover:border-indigo-500/50">
            <div className="absolute top-0 left-0 w-1.5 h-full bg-gradient-to-b from-indigo-400 to-purple-500"></div>
            <div className="p-8 md:p-10 flex flex-col md:flex-row items-center justify-between gap-8">
              <div className="space-y-4 max-w-2xl">
                <div className="flex items-center gap-3">
                  <span className="px-3 py-1 text-xs font-bold uppercase tracking-wider bg-indigo-600 text-white rounded-full">New Research</span>
                  <span className="text-sm font-medium text-slate-400">Sept 4, 2026 • 8 min read</span>
                </div>
                <h2 className="text-2xl md:text-3xl font-bold text-white group-hover:text-indigo-300 transition-colors">Modeling Thermal Expansion in Aerospace Alloys</h2>
                <p className="text-slate-300 text-lg">Deep dive into isotropic thermal expansion formulas and why Titanium out-performs Aluminum 7075 at Mach 2.5.</p>
              </div>
              <div className="flex-shrink-0 flex items-center justify-center p-4 bg-indigo-900/30 rounded-2xl group-hover:scale-110 transition-transform">
                <BookOpen className="w-12 h-12 text-indigo-400" />
              </div>
            </div>
          </Link>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 pt-12">
          
          <Link href="/materials" className="group p-8 rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 hover:bg-slate-800/50 transition-all">
            <div className="w-12 h-12 rounded-lg bg-emerald-900/30 text-emerald-400 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
              <Database className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Browse Materials</h3>
            <p className="text-slate-200 text-sm">Access 1000+ verified engineering materials and their physical properties.</p>
          </Link>

          <Link href="/projects" className="group p-8 rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 hover:bg-slate-800/50 transition-all">
            <div className="w-12 h-12 rounded-lg bg-orange-900/30 text-orange-400 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
              <Workflow className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Project Workflows</h3>
            <p className="text-slate-200 text-sm">Create, save, and manage complex material selection workflows.</p>
          </Link>

          <Link href="/ai" className="group p-8 rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 hover:bg-slate-800/50 transition-all">
            <div className="w-12 h-12 rounded-lg bg-blue-900/30 text-blue-400 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
              <Bot className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Ask AI Adviser</h3>
            <p className="text-slate-200 text-sm">Describe constraints in plain English and let AI find the perfect material.</p>
          </Link>

        </div>

      </div>
    </main>
  );
}
