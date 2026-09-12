"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { Database, Calculator, Workflow, Bot, BarChart3, Plus, ArrowRight, LayoutDashboard, Search } from "lucide-react";
import { API } from "@/lib/api";

export default function AppDashboard() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetch(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => res.json())
      .then(data => {
        if (!data.detail) setProfile(data);
      })
      .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500 dark:text-slate-400">Loading workspace...</div>;
  }

  return (
    <main className="p-6 lg:p-10 w-full max-w-7xl mx-auto space-y-10">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-3">
            <LayoutDashboard className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            Welcome{profile?.username ? `, ${profile.username}` : ''}
          </h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">Here is what's happening in your engineering workspace today.</p>
        </div>
        <div className="flex gap-3">
          <Link href="/materials" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 px-4 py-2 rounded-2xl text-sm font-semibold transition-colors flex items-center gap-2 text-slate-900 dark:text-white">
            <Search className="w-4 h-4" /> Browse Database
          </Link>
          <Link href="/projects" className="bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 px-4 py-2 rounded-2xl text-sm font-semibold transition-colors text-white flex items-center gap-2 shadow-lg shadow-indigo-600/20">
            <Plus className="w-4 h-4" /> New Workspace
          </Link>
        </div>
      </div>

      {/* Quick Actions Grid */}
      <div>
        <h2 className="text-lg font-bold text-slate-900 dark:text-white font-heading mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link href="/materials" className="bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl hover:bg-slate-100 dark:hover:bg-slate-800/50 hover:border-slate-200 dark:hover:border-slate-700 transition-all group">
            <Database className="w-6 h-6 text-blue-400 mb-3 group-hover:scale-110 transition-transform" />
            <h3 className="font-bold text-slate-900 dark:text-white font-heading text-sm mb-1">Material Search</h3>
            <p className="text-slate-500 dark:text-slate-400 text-xs">Access 1000+ verified materials.</p>
          </Link>
          <Link href="/analytics/cbam" className="bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl hover:bg-slate-100 dark:hover:bg-slate-800/50 hover:border-slate-200 dark:hover:border-slate-700 transition-all group">
            <Calculator className="w-6 h-6 text-amber-400 mb-3 group-hover:scale-110 transition-transform" />
            <h3 className="font-bold text-slate-900 dark:text-white font-heading text-sm mb-1">CBAM Calculator</h3>
            <p className="text-slate-500 dark:text-slate-400 text-xs">Estimate carbon tax emissions.</p>
          </Link>
          <Link href="/ai" className="bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl hover:bg-slate-100 dark:hover:bg-slate-800/50 hover:border-slate-200 dark:hover:border-slate-700 transition-all group">
            <Bot className="w-6 h-6 text-emerald-400 mb-3 group-hover:scale-110 transition-transform" />
            <h3 className="font-bold text-slate-900 dark:text-white font-heading text-sm mb-1">AI Adviser</h3>
            <p className="text-slate-500 dark:text-slate-400 text-xs">Chat with our engineering AI.</p>
          </Link>
          <Link href="/analytics/compare" className="bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl hover:bg-slate-100 dark:hover:bg-slate-800/50 hover:border-slate-200 dark:hover:border-slate-700 transition-all group">
            <BarChart3 className="w-6 h-6 text-purple-400 mb-3 group-hover:scale-110 transition-transform" />
            <h3 className="font-bold text-slate-900 dark:text-white font-heading text-sm mb-1">Compare Materials</h3>
            <p className="text-slate-500 dark:text-slate-400 text-xs">Side-by-side radar analysis.</p>
          </Link>
        </div>
      </div>

      {/* Recent Activity Mockup */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white font-heading">Recent Workspaces</h2>
          <Link href="/projects" className="text-xs font-semibold text-blue-600 dark:text-blue-400 hover:text-indigo-300 flex items-center gap-1">
            View All <ArrowRight className="w-3 h-3" />
          </Link>
        </div>
        <div className="bg-white dark:bg-slate-900/30 border border-slate-200 dark:border-slate-800 rounded-2xl p-6">
          <div className="text-center py-8">
            <Workflow className="w-10 h-10 text-slate-700 dark:text-slate-200 mx-auto mb-3" />
            <p className="text-slate-500 dark:text-slate-400 text-sm">You haven't created any engineering workspaces recently.</p>
            <Link href="/projects" className="inline-block mt-4 text-xs font-semibold bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-900 dark:text-white px-4 py-2 rounded-2xl transition-colors">
              Go to Workspaces
            </Link>
          </div>
        </div>
      </div>

    </main>
  );
}
