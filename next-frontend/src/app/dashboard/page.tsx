"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { Database, Calculator, Workflow, Bot, BarChart3, Plus, ArrowRight, LayoutDashboard, Search, Star, Zap, Clock, Box, Sparkles } from "lucide-react";
import { API } from "@/lib/api";

export default function AppDashboard() {
  const [profile, setProfile] = useState<any>(null);
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetch(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        if (!res.ok) {
          localStorage.removeItem("token");
          window.location.href = "/?login=true";
          return null;
        }
        return res.json();
      })
      .then(data => {
        if (data && !data.detail) {
          setProfile(data);
          if (data.tier === "pro" || data.tier === "advanced" || data.is_admin) {
            fetch(`${API}/projects/`, { headers: { Authorization: `Bearer ${token}` } })
            .then(r => r.ok ? r.json() : [])
            .then(projData => {
              if (Array.isArray(projData)) setProjects(projData.slice(0, 3));
            }).catch(console.error);
          }
        }
      })
      .catch(() => {
        localStorage.removeItem("token");
        window.location.href = "/?login=true";
      })
      .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  if (loading) {
    return <div className="flex h-[60vh] items-center justify-center">
      <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
    </div>;
  }

  const isProOrAbove = profile?.tier === "pro" || profile?.tier === "advanced" || profile?.is_admin;

  return (
    <main className="p-6 lg:p-10 w-full max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500">
      
      {/* Dynamic Header Banner */}
      <div className={`relative overflow-hidden rounded-3xl p-8 md:p-10 text-white ${
        profile?.tier === "advanced" || profile?.is_admin ? "bg-gradient-to-br from-violet-600 via-fuchsia-700 to-amber-600" :
        profile?.tier === "pro" ? "bg-gradient-to-br from-indigo-600 to-blue-700" :
        "bg-gradient-to-br from-slate-700 to-slate-900"
      }`}>
        <div className="absolute top-0 right-0 p-12 opacity-10 pointer-events-none">
          <Database className="w-64 h-64 -rotate-12 transform" />
        </div>
        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className="px-3 py-1 bg-white/20 backdrop-blur-md rounded-full text-xs font-bold uppercase tracking-wider">
                {profile?.tier || 'Free'} Tier
              </span>
              {profile?.is_admin && (
                <span className="px-3 py-1 bg-amber-500/90 backdrop-blur-md rounded-full text-xs font-bold uppercase tracking-wider text-slate-900">
                  Admin
                </span>
              )}
            </div>
            <h1 className="text-3xl md:text-4xl font-extrabold font-heading mb-2">
              Welcome back{profile?.username ? `, ${profile.username}` : ''}!
            </h1>
            <p className="text-white/80 max-w-lg">
              {isProOrAbove 
                ? "Your engineering workspaces and tools are ready. Pick up where you left off."
                : "You are currently on the Academic Free Tier. Upgrade to Pro to unlock Engineering Workspaces and PDF Exports."}
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto shrink-0">
            {!isProOrAbove && (
              <Link href="/account" className="bg-amber-500 hover:bg-amber-400 text-slate-900 px-6 py-3 rounded-2xl text-sm font-bold transition-colors text-center">
                Upgrade to Pro
              </Link>
            )}
            <Link href="/projects" className="bg-white/10 hover:bg-white/20 backdrop-blur-md border border-white/20 px-6 py-3 rounded-2xl text-sm font-bold transition-colors text-center flex items-center justify-center gap-2">
              <Plus className="w-4 h-4" /> New Workspace
            </Link>
          </div>
        </div>
      </div>

      {/* Stats/Quick Info */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center gap-4 shadow-sm">
          <div className="p-3 bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 rounded-xl"><Box className="w-6 h-6" /></div>
          <div>
            <p className="text-[10px] sm:text-xs font-bold text-slate-500 dark:text-slate-400 uppercase">Workspaces</p>
            <p className="text-xl sm:text-2xl font-black text-slate-900 dark:text-white font-heading">{projects.length}</p>
          </div>
        </div>
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center gap-4 shadow-sm">
          <div className="p-3 bg-emerald-100 dark:bg-emerald-900/40 text-emerald-600 dark:text-emerald-400 rounded-xl"><Sparkles className="w-6 h-6" /></div>
          <div>
            <p className="text-[10px] sm:text-xs font-bold text-slate-500 dark:text-slate-400 uppercase">AI Synthesizer Credits</p>
            <p className="text-xl sm:text-2xl font-black text-slate-900 dark:text-white font-heading">
              {profile?.tier === "advanced" || profile?.tier === "pro" || profile?.is_admin ? "Unlimited" : (profile?.ai_credits ?? 5)}
            </p>
          </div>
        </div>
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center gap-4 shadow-sm">
          <div className="p-3 bg-purple-100 dark:bg-purple-900/40 text-purple-600 dark:text-purple-400 rounded-xl"><Zap className="w-6 h-6" /></div>
          <div>
            <p className="text-[10px] sm:text-xs font-bold text-slate-500 dark:text-slate-400 uppercase">API Access</p>
            <p className="text-lg sm:text-xl font-black text-slate-900 dark:text-white font-heading">
              {profile?.api_key ? "Active" : profile?.tier === "advanced" || profile?.is_admin ? "Not Generated" : "Locked"}
            </p>
          </div>
        </div>
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center gap-4 shadow-sm">
          <div className="p-3 bg-amber-100 dark:bg-amber-900/40 text-amber-600 dark:text-amber-400 rounded-xl"><Star className="w-6 h-6" /></div>
          <div>
            <p className="text-[10px] sm:text-xs font-bold text-slate-500 dark:text-slate-400 uppercase">Saved Items</p>
            <p className="text-xl sm:text-2xl font-black text-slate-900 dark:text-white font-heading">{profile?.saved_count || 0}</p>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        
        {/* Main Content Area (Recent Workspaces) */}
        <div className="md:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-2">
              <Clock className="w-5 h-5 text-indigo-500" /> Recent Workspaces
            </h2>
            {isProOrAbove && projects.length > 0 && (
              <Link href="/projects" className="text-sm font-bold text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 transition-colors flex items-center gap-1">
                View All <ArrowRight className="w-4 h-4" />
              </Link>
            )}
          </div>

          {!isProOrAbove ? (
            <div className="bg-gradient-to-b from-white to-slate-50 dark:from-slate-900 dark:to-slate-950 border border-slate-200 dark:border-slate-800 rounded-3xl p-10 text-center relative overflow-hidden group">
              <div className="absolute inset-0 bg-[url('/noise.png')] opacity-[0.03] pointer-events-none"></div>
              <Workflow className="w-12 h-12 text-slate-300 dark:text-slate-700 mx-auto mb-4 group-hover:scale-110 transition-transform duration-500" />
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">Workspaces are locked</h3>
              <p className="text-slate-500 dark:text-slate-400 mb-6 max-w-sm mx-auto">You need a Professional or Advanced subscription to create Engineering Workspaces and Bill of Materials.</p>
              <Link href="/account" className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-xl font-bold transition-colors">
                <Zap className="w-4 h-4" /> Unlock Workspaces
              </Link>
            </div>
          ) : projects.length === 0 ? (
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 border-dashed rounded-3xl p-10 text-center">
              <Workflow className="w-12 h-12 text-slate-300 dark:text-slate-700 mx-auto mb-4" />
              <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">No workspaces yet</h3>
              <p className="text-slate-500 dark:text-slate-400 mb-6">Create your first engineering workspace to start building a BOM.</p>
              <Link href="/projects" className="inline-flex items-center gap-2 bg-slate-900 dark:bg-white text-white dark:text-slate-900 hover:bg-slate-800 dark:hover:bg-slate-100 px-6 py-2.5 rounded-xl font-bold transition-colors">
                <Plus className="w-4 h-4" /> Create Workspace
              </Link>
            </div>
          ) : (
            <div className="grid gap-4">
              {projects.map((proj) => (
                <Link key={proj.id} href={`/projects/${proj.id}`} className="block bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 hover:border-indigo-400 dark:hover:border-indigo-500 hover:shadow-lg hover:shadow-indigo-500/10 transition-all group">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div className="flex items-center gap-4">
                      <div className="shrink-0 w-12 h-12 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                        <Workflow className="w-6 h-6" />
                      </div>
                      <div>
                        <h3 className="font-bold text-lg text-slate-900 dark:text-white">{proj.name}</h3>
                        <p className="text-sm text-slate-500 dark:text-slate-400">{new Date(proj.created_at).toLocaleDateString()} • {proj.items?.length || 0} items</p>
                      </div>
                    </div>
                    <ArrowRight className="hidden sm:block w-5 h-5 text-slate-300 dark:text-slate-700 group-hover:text-indigo-500 group-hover:translate-x-1 transition-all" />
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>

        {/* Sidebar (Quick Actions) */}
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-500" /> Quick Tools
          </h2>
          <div className="grid gap-3">
            <Link href="/materials" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-2xl hover:border-blue-400 hover:shadow-md transition-all group flex items-center gap-4">
              <div className="shrink-0 w-10 h-10 bg-blue-50 dark:bg-blue-900/20 text-blue-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform"><Search className="w-5 h-5" /></div>
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white text-sm">Material Search</h3>
                <p className="text-slate-500 text-xs">Search 6500+ database</p>
              </div>
            </Link>
            <Link href="/analytics/compare" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-2xl hover:border-purple-400 hover:shadow-md transition-all group flex items-center gap-4">
              <div className="shrink-0 w-10 h-10 bg-purple-50 dark:bg-purple-900/20 text-purple-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform"><BarChart3 className="w-5 h-5" /></div>
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white text-sm">Compare Tool</h3>
                <p className="text-slate-500 text-xs">Radar charts & metrics</p>
              </div>
            </Link>
            <Link href="/analytics/cbam" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-2xl hover:border-amber-400 hover:shadow-md transition-all group flex items-center gap-4">
              <div className="shrink-0 w-10 h-10 bg-amber-50 dark:bg-amber-900/20 text-amber-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform"><Calculator className="w-5 h-5" /></div>
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white text-sm">CBAM Calculator</h3>
                <p className="text-slate-500 text-xs">Carbon tax estimates</p>
              </div>
            </Link>
            <Link href="/analytics/synthesizer" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-2xl hover:border-emerald-400 hover:shadow-md transition-all group flex items-center gap-4">
              <div className="shrink-0 w-10 h-10 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform"><Bot className="w-5 h-5" /></div>
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white text-sm">AI Synthesizer</h3>
                <p className="text-slate-500 text-xs">Generate custom grades</p>
              </div>
            </Link>
          </div>
        </div>

      </div>

    </main>
  );
}
