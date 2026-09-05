"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { Workflow, Plus, FolderKanban, HardDrive, Play, Loader2, X, Trash2 } from "lucide-react";

export default function WorkflowsPage() {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newProjectName, setNewProjectName] = useState("");
  const [newProjectDesc, setNewProjectDesc] = useState("");
  const [creating, setCreating] = useState(false);

  const fetchProjects = () => {
    setLoading(true);
    fetch("http://127.0.0.1:8000/api/v1/projects")
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) setProjects(data);
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProjectName) return;
    setCreating(true);
    
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/projects", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newProjectName, description: newProjectDesc })
      });
      if (res.ok) {
        setIsModalOpen(false);
        setNewProjectName("");
        setNewProjectDesc("");
        fetchProjects();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (e: React.MouseEvent, projectId: number) => {
    e.preventDefault(); // Prevent navigating to the project link
    if (!confirm("Are you sure you want to delete this workspace?")) return;
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/projects/${projectId}`, {
        method: "DELETE"
      });
      if (res.ok) {
        fetchProjects();
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto relative">
      <div className="w-full max-w-6xl mx-auto space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <Workflow className="w-8 h-8 text-blue-400" />
            Engineering Workspaces
          </h1>
          <p className="text-slate-300 mt-2">Manage your multi-part assemblies and interactive blueprints.</p>
        </div>

        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold text-white">Your Projects</h2>
          <button 
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold transition-colors shadow-lg shadow-blue-900/50"
          >
            <Plus className="w-4 h-4" /> Create Project
          </button>
        </div>

        {loading ? (
          <div className="flex justify-center py-20"><Loader2 className="w-8 h-8 animate-spin text-blue-500" /></div>
        ) : projects.length === 0 ? (
          <div className="text-center py-20 text-slate-500 bg-slate-900/30 rounded-2xl border border-slate-800 border-dashed flex flex-col items-center">
            <FolderKanban className="w-12 h-12 mb-4 text-slate-600" />
            <p className="font-semibold text-slate-400">No projects found.</p>
            <p className="text-sm">Create your first workspace to start mapping assemblies.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((proj: any) => (
              <Link key={proj.id} href={`/projects/${proj.id}`} className="block">
                <div className="p-6 h-full rounded-2xl bg-slate-900 border border-slate-800 hover:border-blue-500/50 transition-colors group flex flex-col cursor-pointer relative">
                  
                  {/* Delete Button */}
                  <button 
                    onClick={(e) => handleDelete(e, proj.id)}
                    className="absolute top-4 right-4 p-2 text-slate-600 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity bg-slate-950 rounded-lg border border-slate-800"
                    title="Delete Project"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>

                  <div className="flex justify-between items-start mb-4 pr-10">
                    <h3 className="font-bold text-white text-lg group-hover:text-blue-400 transition-colors">{proj.name}</h3>
                  </div>
                  <p className="text-sm text-slate-400 mb-6 flex-1 line-clamp-2">{proj.description}</p>
                  <div className="flex justify-between items-center text-xs text-slate-500 mt-auto pt-4 border-t border-slate-800">
                    <span>{proj.items?.length || 0} Components</span>
                    <span className="flex items-center gap-1 text-blue-400 font-semibold group-hover:text-blue-300">
                      <Play className="w-3 h-3" /> Open Canvas
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Create Project Modal */}
      {isModalOpen && (
        <div className="absolute inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 w-full max-w-md shadow-2xl relative">
            <button onClick={() => setIsModalOpen(false)} className="absolute top-4 right-4 text-slate-400 hover:text-white">
              <X className="w-5 h-5" />
            </button>
            <h2 className="text-xl font-bold text-white mb-6">Create New Workspace</h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-slate-300 mb-1">Project Name</label>
                <input 
                  type="text" 
                  value={newProjectName}
                  onChange={e => setNewProjectName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-white outline-none focus:border-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-300 mb-1">Description (Optional)</label>
                <textarea 
                  value={newProjectDesc}
                  onChange={e => setNewProjectDesc(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-white outline-none focus:border-blue-500 min-h-[100px]"
                />
              </div>
              <button 
                type="submit" 
                disabled={!newProjectName || creating}
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-bold rounded-lg transition-colors mt-2"
              >
                {creating ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : "Create Project"}
              </button>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}
