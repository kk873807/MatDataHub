"use client";
import { useState, useEffect } from "react";
import { Workflow, Lock, Plus, FolderKanban, Component, HardDrive, Share2, Play } from "lucide-react";

export default function WorkflowsPage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isLocked, setIsLocked] = useState(false);

  useEffect(() => {
    // In a real app with Auth context, we'd pass the Bearer token here.
    // For now, testing the endpoint directly to see if it returns 403.
    fetch("http://127.0.0.1:8000/api/v1/projects")
      .then(res => {
        if (res.status === 403 || res.status === 401) {
          setIsLocked(true);
          return null;
        }
        return res.json();
      })
      .then(data => {
        if (data) setProjects(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (isLocked) {
    return (
      <main className="flex flex-col p-6 lg:p-10 w-full h-full bg-slate-950 overflow-hidden relative">
        {/* Background Mockup */}
        <div className="absolute inset-0 opacity-20 pointer-events-none flex items-center justify-center">
          <div className="w-[800px] h-[600px] border border-slate-700 rounded-xl bg-slate-900 shadow-2xl relative">
            <div className="absolute top-4 left-4 flex gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <div className="absolute top-12 left-10 p-4 border border-blue-500/50 rounded bg-slate-800 text-xs text-blue-300 w-48">
              Engine Block Component
              <div className="mt-2 h-1 bg-slate-700 rounded w-full"><div className="h-full bg-blue-500 w-2/3"></div></div>
            </div>
            <div className="absolute top-40 left-64 p-4 border border-emerald-500/50 rounded bg-slate-800 text-xs text-emerald-300 w-48">
              Material: Aluminum 6061
              <div className="mt-2 text-white">Cost Rollup: ₹450/kg</div>
            </div>
            {/* SVG Connector Line */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none">
              <path d="M 230 70 C 280 70, 280 170, 330 170" fill="none" stroke="#475569" strokeWidth="2" strokeDasharray="4 4" />
            </svg>
          </div>
        </div>

        {/* Lock Overlay */}
        <div className="relative z-10 w-full h-full flex flex-col items-center justify-center">
          <div className="max-w-2xl text-center space-y-6 bg-slate-900/80 backdrop-blur-xl p-10 rounded-3xl border border-slate-800 shadow-2xl">
            <div className="w-20 h-20 mx-auto bg-blue-900/30 rounded-2xl flex items-center justify-center border border-blue-500/30">
              <Lock className="w-10 h-10 text-blue-400" />
            </div>
            
            <h1 className="text-4xl font-bold text-white">Engineering Workspaces</h1>
            <p className="text-slate-300 text-lg">
              Design multi-part assemblies, run dynamic cost rollups, and build visual engineering blueprints in an interactive drag-and-drop canvas.
            </p>

            <div className="grid grid-cols-2 gap-4 text-left mt-8">
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <Component className="w-6 h-6 text-indigo-400 mb-2" />
                <h3 className="font-bold text-white text-sm">Component Mapping</h3>
                <p className="text-xs text-slate-400 mt-1">Assign materials to individual parts and calculate total volume, weight, and assembly cost.</p>
              </div>
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <Share2 className="w-6 h-6 text-emerald-400 mb-2" />
                <h3 className="font-bold text-white text-sm">Visual Blueprints</h3>
                <p className="text-xs text-slate-400 mt-1">Connect nodes and dependencies in a live canvas environment.</p>
              </div>
            </div>

            <button className="mt-6 w-full py-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-blue-900/50">
              Upgrade to Pro to Unlock Workspaces
            </button>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto">
      <div className="w-full max-w-6xl mx-auto space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <Workflow className="w-8 h-8 text-blue-400" />
            Engineering Workspaces
          </h1>
          <p className="text-slate-300 mt-2">Manage your multi-part assemblies and interactive blueprints.</p>
        </div>

        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold text-white">My Projects</h2>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold transition-colors">
            <Plus className="w-4 h-4" /> New Workspace
          </button>
        </div>

        {projects.length === 0 ? (
          <div className="text-center py-20 text-slate-500 bg-slate-900/30 rounded-2xl border border-slate-800 border-dashed flex flex-col items-center">
            <FolderKanban className="w-12 h-12 mb-4 text-slate-600" />
            <p>No projects found. Create your first workspace to start mapping assemblies.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((proj: any) => (
              <div key={proj.id} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-blue-500/50 transition-colors group">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="font-bold text-white text-lg">{proj.name}</h3>
                  <HardDrive className="w-5 h-5 text-slate-600 group-hover:text-blue-400 transition-colors" />
                </div>
                <p className="text-sm text-slate-400 mb-6 line-clamp-2">{proj.description}</p>
                <div className="flex justify-between items-center text-xs text-slate-500">
                  <span>{proj.items?.length || 0} Components</span>
                  <button className="flex items-center gap-1 text-blue-400 hover:text-blue-300">
                    <Play className="w-3 h-3" /> Open Canvas
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
