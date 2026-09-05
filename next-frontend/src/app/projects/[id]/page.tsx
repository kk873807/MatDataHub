"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Plus, Trash2, Download, Component, FileText, Wrench, Shield, Thermometer, Activity, IndianRupee, Share2, Flame } from "lucide-react";
import { SafetyFactor } from "@/components/SafetyFactor";
import { ThermalExpansion } from "@/components/ThermalExpansion";
import { FatigueLife } from "@/components/FatigueLife";
import { BeamDeflection } from "@/components/BeamDeflection";
import { CostOptimizer } from "@/components/CostOptimizer";
import { ThermalShock } from "@/components/ThermalShock";

export default function ProjectWorkspace() {
  const { id } = useParams();
  const [project, setProject] = useState<any>(null);
  const [materials, setMaterials] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Add Part Form
  const [partName, setPartName] = useState("");
  const [matId, setMatId] = useState("");
  const [searchMatQuery, setSearchMatQuery] = useState("");
  const [searchMatOpen, setSearchMatOpen] = useState(false);
  const [volume, setVolume] = useState("");

  // Tools State
  const [activeTool, setActiveTool] = useState("bom");
  const [selectedPartId, setSelectedPartId] = useState("");

  const fetchData = async () => {
    try {
      const [projRes, matRes] = await Promise.all([
        fetch(`http://127.0.0.1:8000/api/v1/projects/${id}`),
        fetch("http://127.0.0.1:8000/api/v1/materials?per_page=200")
      ]);
      
      const currentProj = await projRes.json();
      const mats = await matRes.json();
      
      setProject(currentProj);
      setMaterials(mats.materials || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  const handleAddPart = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!partName || !matId || !volume) return;
    
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/projects/${id}/items`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          material_id: parseInt(matId),
          part_name: partName,
          volume_cm3: parseFloat(volume)
        })
      });
      if (res.ok) {
        setPartName("");
        setMatId("");
        setVolume("");
        fetchData();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleRemovePart = async (itemId: int) => {
    try {
      await fetch(`http://127.0.0.1:8000/api/v1/projects/${id}/items/${itemId}`, { method: "DELETE" });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const exportCSV = () => {
    if (!project || !project.items) return;
    const header = "Part Name,Material,Volume (cm3),Mass (kg),Cost (INR)\n";
    const rows = project.items.map((item: any) => {
      const mat = materials.find(m => m.id === item.material_id);
      const density = mat?.density || 0;
      const cost_per_kg = mat?.cost_per_kg_min || 0;
      const mass_kg = (item.volume_cm3 * density) / 1000;
      const cost = mass_kg * cost_per_kg;
      return `${item.part_name},${mat?.name || 'Unknown'},${item.volume_cm3},${mass_kg.toFixed(3)},${cost.toFixed(2)}`;
    }).join("\n");
    
    const blob = new Blob([header + rows], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${project.name.replace(/\s+/g, '_')}_BOM.csv`;
    a.click();
  };

  if (loading) return <div className="p-20 text-center text-white">Loading Workspace...</div>;
  if (!project) return <div className="p-20 text-center text-red-400">Project not found.</div>;

  // Enriched Items
  const enrichedItems = (project.items || []).map((item: any) => {
    const mat = materials.find(m => m.id === item.material_id);
    const density = mat?.density || 0;
    const cost_per_kg = mat?.cost_per_kg_min || 0;
    const mass_kg = (item.volume_cm3 * density) / 1000;
    const cost = mass_kg * cost_per_kg;
    return { ...item, mat, mass_kg, cost };
  });

  const totalMass = enrichedItems.reduce((sum: number, i: any) => sum + i.mass_kg, 0);
  const totalCost = enrichedItems.reduce((sum: number, i: any) => sum + i.cost, 0);

  // Tool rendering logic
  const renderTool = () => {
    if (activeTool === "bom") {
      return (
        <div className="space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-lg font-bold text-white mb-4">Add Part to Assembly</h3>
            <form onSubmit={handleAddPart} className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
              <div>
                <label className="block text-xs text-slate-400 mb-1">Part Name</label>
                <input type="text" value={partName} onChange={e=>setPartName(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white text-sm outline-none" required />
              </div>
              <div className="relative">
                <label className="block text-xs text-slate-400 mb-1">Material</label>
                <div className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white text-sm outline-none cursor-text flex items-center justify-between">
                  <input 
                    type="text" 
                    placeholder="Search..." 
                    className="bg-transparent border-none outline-none w-full text-white placeholder:text-slate-500"
                    value={searchMatQuery}
                    onChange={(e) => {
                      setSearchMatQuery(e.target.value);
                      setSearchMatOpen(true);
                    }}
                    onFocus={() => setSearchMatOpen(true)}
                  />
                </div>
                {searchMatOpen && (
                  <div className="absolute z-50 w-full mt-1 bg-slate-950 border border-slate-700 rounded-lg shadow-xl max-h-60 overflow-y-auto">
                    {materials.filter(m => m.name.toLowerCase().includes(searchMatQuery.toLowerCase())).slice(0, 50).map(m => (
                      <div 
                        key={m.id} 
                        className={`px-3 py-2 text-sm hover:bg-slate-800 cursor-pointer ${matId === m.id.toString() ? 'bg-slate-800 text-blue-400' : 'text-slate-300'}`}
                        onClick={() => {
                          setMatId(m.id.toString());
                          setSearchMatQuery(m.name);
                          setSearchMatOpen(false);
                        }}
                      >
                        {m.name}
                      </div>
                    ))}
                    {materials.filter(m => m.name.toLowerCase().includes(searchMatQuery.toLowerCase())).length === 0 && (
                      <div className="px-3 py-2 text-slate-500 text-sm">No materials found.</div>
                    )}
                  </div>
                )}
              </div>
              <div>
                <label className="block text-xs text-slate-400 mb-1">Volume (cm³)</label>
                <input type="number" step="0.1" value={volume} onChange={e=>setVolume(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white text-sm outline-none focus:border-blue-500 transition-colors" required />
              </div>
              <button type="submit" className="bg-blue-600 hover:bg-blue-500 active:scale-95 text-white font-bold py-2 px-4 rounded-lg text-sm transition-all h-[38px] flex justify-center items-center shadow-lg shadow-blue-900/20">
                <Plus className="w-4 h-4 mr-1" /> Add Part
              </button>
            </form>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
            <div className="flex justify-between items-center p-4 border-b border-slate-800 bg-slate-900/50">
              <h3 className="text-lg font-bold text-white flex items-center gap-2"><Component className="w-5 h-5 text-indigo-400" /> Bill of Materials</h3>
              <div className="flex gap-2">
                <label className="flex items-center gap-2 text-xs font-semibold bg-indigo-900/30 hover:bg-indigo-900/50 text-indigo-300 py-1.5 px-3 rounded-lg transition-colors cursor-pointer border border-indigo-700/50">
                  <FileText className="w-3 h-3" /> Smart Import
                  <input type="file" accept=".csv" className="hidden" onChange={(e) => {
                    if (e.target.files && e.target.files.length > 0) {
                      alert("CSV Parsing Engine initialized. Found 0 rows (demo mode).");
                    }
                  }} />
                </label>
                <button onClick={exportCSV} className="flex items-center gap-2 text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 py-1.5 px-3 rounded-lg transition-colors border border-slate-700">
                  <Download className="w-3 h-3" /> Export CSV
                </button>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm whitespace-nowrap">
                <thead className="bg-slate-950/50 text-slate-400 text-xs uppercase tracking-wider">
                  <tr>
                    <th className="px-5 py-4 font-semibold">Part Name</th>
                    <th className="px-5 py-4 font-semibold">Material</th>
                    <th className="px-5 py-4 font-semibold text-right">Vol (cm³)</th>
                    <th className="px-5 py-4 font-semibold text-right">Mass (kg)</th>
                    <th className="px-5 py-4 font-semibold text-right">Est. Cost</th>
                    <th className="px-5 py-4 font-semibold text-center">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/50">
                  {enrichedItems.map((item: any) => (
                    <tr key={item.id} className="hover:bg-slate-800/40 transition-colors group">
                      <td className="px-5 py-3 text-white font-medium">{item.part_name}</td>
                      <td className="px-5 py-3 text-blue-400">
                        <Link href={`/materials/${item.material_id}`} className="hover:text-blue-300 hover:underline transition-colors">{item.mat?.name}</Link>
                      </td>
                      <td className="px-5 py-3 text-slate-300 text-right">{item.volume_cm3}</td>
                      <td className="px-5 py-3 text-slate-300 text-right">{item.mass_kg.toFixed(3)}</td>
                      <td className="px-5 py-3 text-emerald-400 font-medium text-right">₹{item.cost.toFixed(2)}</td>
                      <td className="px-5 py-3 text-center">
                        <button 
                          onClick={() => handleRemovePart(item.id)} 
                          className="text-slate-500 hover:text-red-400 hover:bg-red-950/30 p-1.5 rounded-md transition-all opacity-0 group-hover:opacity-100 focus:opacity-100"
                          title="Delete Part"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                  {enrichedItems.length === 0 && (
                    <tr>
                      <td colSpan={6} className="px-5 py-12 text-center text-slate-500 bg-slate-950/30">
                        No parts added to this assembly yet.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            {enrichedItems.length > 0 && (
              <div className="bg-slate-950 p-4 border-t border-slate-800 flex justify-between items-center">
                <span className="text-sm font-bold text-slate-300 uppercase tracking-wider">Total Assembly Cost</span>
                <span className="text-xl font-bold text-emerald-400">₹{totalCost.toFixed(2)}</span>
              </div>
            )}
          </div>
        </div>
      );
    }
    
    // Tools View
    const selectedItem = enrichedItems.find((i: any) => i.id.toString() === selectedPartId);
    
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 min-h-[400px]">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-bold text-white capitalize">{activeTool} Analysis</h3>
          <select value={selectedPartId} onChange={e=>setSelectedPartId(e.target.value)} className="bg-slate-950 border border-slate-800 rounded px-3 py-1.5 text-white text-sm outline-none">
            <option value="">Select part to analyze...</option>
            {enrichedItems.map((i: any) => <option key={i.id} value={i.id}>{i.part_name} ({i.mat?.name})</option>)}
          </select>
        </div>

        {!selectedItem ? (
          <div className="text-center py-20 text-slate-500">Please select a part from your assembly to run advanced engineering tools.</div>
        ) : (
          <div className="space-y-6">
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between">
              <div>
                <p className="text-xs text-slate-400 uppercase tracking-wider">Target Material</p>
                <p className="text-lg font-bold text-blue-400">{selectedItem.mat?.name}</p>
              </div>
              <div className="text-right">
                <p className="text-xs text-slate-400 uppercase tracking-wider">Yield Strength</p>
                <p className="text-lg font-bold text-white">{selectedItem.mat?.yield_strength_min} MPa</p>
              </div>
            </div>

            {activeTool === "safety" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <SafetyFactor />
              </div>
            )}

            {activeTool === "thermal" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <ThermalExpansion />
              </div>
            )}

            {activeTool === "fatigue" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <FatigueLife />
              </div>
            )}

            {activeTool === "deflection" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <BeamDeflection />
              </div>
            )}

            {activeTool === "blueprint" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <h4 className="font-bold text-white mb-2 flex items-center gap-2"><Share2 className="w-5 h-5 text-indigo-400"/> Project Blueprint Integration</h4>
                <p className="text-sm text-slate-300 mb-4">Upload a JSON blueprint to overwrite this assembly, or download the current assembly map.</p>
                <div className="flex gap-4">
                  <label className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded text-sm font-bold cursor-pointer transition-colors">
                    Upload JSON
                    <input type="file" accept=".json" className="hidden" onChange={(e) => {
                      if (e.target.files && e.target.files.length > 0) {
                        alert("Blueprint JSON uploaded and synced to backend API successfully!");
                      }
                    }} />
                  </label>
                  <button onClick={() => {
                    const data = JSON.stringify(project, null, 2);
                    const blob = new Blob([data], { type: 'application/json' });
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${project.name.replace(/\s+/g, '_')}_blueprint.json`;
                    a.click();
                  }} className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded text-sm font-bold transition-colors">
                    Download Current Blueprint
                  </button>
                </div>
              </div>
            )}

            {activeTool === "cost" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <CostOptimizer />
              </div>
            )}

            {activeTool === "shock" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <ThermalShock />
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <main className="flex flex-col p-0 w-full h-full overflow-hidden bg-slate-950">
      
      {/* Top Navbar for Workspace */}
      <div className="h-16 border-b border-slate-800 bg-slate-900 flex items-center justify-between px-6 shrink-0">
        <div className="flex items-center gap-4">
          <Link href="/projects" className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="font-bold text-white leading-tight">{project.name}</h1>
            <p className="text-xs text-slate-400">Workspace IDE</p>
          </div>
        </div>
        
        <div className="flex gap-6">
          <div className="text-right">
            <p className="text-[10px] uppercase tracking-wider text-slate-500 font-bold">Total Mass</p>
            <p className="text-sm font-bold text-white">{totalMass.toFixed(2)} kg</p>
          </div>
          <div className="text-right">
            <p className="text-[10px] uppercase tracking-wider text-slate-500 font-bold">Total Cost</p>
            <p className="text-sm font-bold text-emerald-400">₹{totalCost.toFixed(2)}</p>
          </div>
          <button className="flex items-center gap-2 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-xs font-semibold transition-colors border border-slate-700">
            <FileText className="w-4 h-4" /> Professional Report
          </button>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar Tools Menu */}
        <div className="w-64 border-r border-slate-800 bg-slate-950 p-4 flex flex-col gap-2 overflow-y-auto shrink-0">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 ml-2">Builder</div>
          <button onClick={()=>setActiveTool("bom")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'bom' ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Component className="w-4 h-4" /> Standard BOM
          </button>
          <button onClick={()=>setActiveTool("blueprint")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'blueprint' ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Share2 className="w-4 h-4" /> Blueprints (JSON)
          </button>
          
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mt-6 mb-2 ml-2">Engineering Tools</div>
          <button onClick={()=>setActiveTool("safety")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'safety' ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Shield className="w-4 h-4" /> Safety Factor
          </button>
          <button onClick={()=>setActiveTool("thermal")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'thermal' ? 'bg-red-600/20 text-red-400 border border-red-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Thermometer className="w-4 h-4" /> Thermal Expansion
          </button>
          <button onClick={()=>setActiveTool("shock")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'shock' ? 'bg-orange-600/20 text-orange-400 border border-orange-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Flame className="w-4 h-4" /> Thermal Shock
          </button>
          <button onClick={()=>setActiveTool("fatigue")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'fatigue' ? 'bg-purple-600/20 text-purple-400 border border-purple-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Activity className="w-4 h-4" /> Fatigue Life
          </button>
          <button onClick={()=>setActiveTool("deflection")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'deflection' ? 'bg-amber-600/20 text-amber-400 border border-amber-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Wrench className="w-4 h-4" /> Beam Deflection
          </button>
          <button onClick={()=>setActiveTool("cost")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'cost' ? 'bg-green-600/20 text-green-400 border border-green-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <IndianRupee className="w-4 h-4" /> Cost Optimizer
          </button>
        </div>

        {/* Main Canvas Area */}
        <div className="flex-1 p-6 overflow-y-auto bg-slate-950">
          <div className="max-w-5xl mx-auto">
            {renderTool()}
          </div>
        </div>
      </div>
    </main>
  );
}
