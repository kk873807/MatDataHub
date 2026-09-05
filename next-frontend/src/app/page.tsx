import Link from "next/link";
import { Database, Calculator, Workflow, Bot } from "lucide-react";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-[80vh] p-8 lg:p-12">
      <div className="w-full max-w-5xl text-center space-y-8">
        
        <div className="space-y-6">
          <div className="inline-block px-4 py-1.5 rounded-full border border-blue-900/50 bg-blue-900/20 text-blue-400 text-sm font-medium mb-4">
            Welcome to the Next Generation
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-br from-white via-neutral-200 to-neutral-500">
            MatDataHub OS
          </h1>
          <p className="text-lg md:text-2xl text-neutral-400 max-w-3xl mx-auto">
            Your centralized platform for engineering physics, materials data, and financial analytics.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 pt-12">
          
          <Link href="/materials" className="group p-8 rounded-2xl bg-neutral-900 border border-neutral-800 hover:border-neutral-700 hover:bg-neutral-800/50 transition-all">
            <div className="w-12 h-12 rounded-lg bg-emerald-900/30 text-emerald-400 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
              <Database className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Browse Materials</h3>
            <p className="text-neutral-400 text-sm">Access 1000+ verified engineering materials and their physical properties.</p>
          </Link>

          <Link href="/calculators" className="group p-8 rounded-2xl bg-neutral-900 border border-neutral-800 hover:border-neutral-700 hover:bg-neutral-800/50 transition-all">
            <div className="w-12 h-12 rounded-lg bg-purple-900/30 text-purple-400 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
              <Calculator className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Engineering Tools</h3>
            <p className="text-neutral-400 text-sm">Run physics, thermodynamics, and ESG financial calculations instantly.</p>
          </Link>

          <Link href="/projects" className="group p-8 rounded-2xl bg-neutral-900 border border-neutral-800 hover:border-neutral-700 hover:bg-neutral-800/50 transition-all">
            <div className="w-12 h-12 rounded-lg bg-orange-900/30 text-orange-400 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
              <Workflow className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Project Workflows</h3>
            <p className="text-neutral-400 text-sm">Create, save, and manage complex material selection workflows.</p>
          </Link>

          <Link href="/ai" className="group p-8 rounded-2xl bg-neutral-900 border border-neutral-800 hover:border-neutral-700 hover:bg-neutral-800/50 transition-all">
            <div className="w-12 h-12 rounded-lg bg-blue-900/30 text-blue-400 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
              <Bot className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Ask AI Adviser</h3>
            <p className="text-neutral-400 text-sm">Describe constraints in plain English and let AI find the perfect material.</p>
          </Link>

        </div>

      </div>
    </main>
  );
}
