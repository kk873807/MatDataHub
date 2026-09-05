"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { Search, Filter, Loader2, Database } from "lucide-react";
import { motion } from "framer-motion";

export default function MaterialsPage() {
  const [materials, setMaterials] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");

  useEffect(() => {
    const fetchMaterials = async () => {
      setLoading(true);
      try {
        let url = "http://127.0.0.1:8000/api/v1/materials?per_page=20";
        if (search) {
          url = `http://127.0.0.1:8000/api/v1/materials/search?q=${encodeURIComponent(search)}`;
        } else if (category) {
          url += `&category=${encodeURIComponent(category)}`;
        }

        const res = await fetch(url);
        const data = await res.json();
        setMaterials(data.materials || []);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    const debounce = setTimeout(fetchMaterials, 300);
    return () => clearTimeout(debounce);
  }, [search, category]);

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full">
      <div className="w-full max-w-7xl mx-auto flex flex-col gap-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="space-y-1">
            <h1 className="text-3xl font-bold text-white flex items-center gap-2">
              <Database className="w-8 h-8 text-emerald-500" /> Material Database
            </h1>
            <p className="text-slate-200">Search and filter verified engineering materials.</p>
          </div>
        </div>

        {/* Search & Filters */}
        <div className="flex flex-col md:flex-row gap-4 bg-slate-900 p-4 rounded-xl border border-slate-800">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-3 w-5 h-5 text-slate-300" />
            <input
              type="text"
              placeholder="Search by name, grade, standard, application..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-10 pr-4 py-2.5 text-white focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
            />
          </div>
          <div className="relative w-full md:w-64">
            <Filter className="absolute left-3 top-3 w-5 h-5 text-slate-300" />
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-10 pr-4 py-2.5 text-white appearance-none focus:ring-2 focus:ring-emerald-500 outline-none"
            >
              <option value="">All Categories</option>
              <option value="Metal">Metals</option>
              <option value="Polymer">Polymers</option>
              <option value="Ceramic">Ceramics</option>
              <option value="Composite">Composites</option>
            </select>
          </div>
        </div>

        {/* Results */}
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-emerald-500" />
          </div>
        ) : materials.length === 0 ? (
          <div className="text-center py-20 text-slate-300 bg-slate-900/50 rounded-xl border border-slate-800 border-dashed">
            No materials found matching your criteria.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {materials.map((mat, i) => (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                key={mat.id}
              >
                <Link href={`/materials/${mat.id}`} className="block h-full p-5 rounded-xl bg-slate-900 border border-slate-800 hover:border-emerald-500/50 hover:bg-slate-800/80 transition-all group">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold text-white text-lg group-hover:text-emerald-400 transition-colors line-clamp-1">{mat.name}</h3>
                  </div>
                  <div className="inline-block px-2 py-1 bg-slate-800 rounded text-xs text-slate-300 mb-4">
                    {mat.category} {mat.subcategory ? `• ${mat.subcategory}` : ''}
                  </div>
                  
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between border-b border-slate-800 pb-1">
                      <span className="text-slate-300">Yield Strength</span>
                      <span className="text-slate-300">{mat.yield_strength_min || '-'} MPa</span>
                    </div>
                    <div className="flex justify-between border-b border-slate-800 pb-1">
                      <span className="text-slate-300">Density</span>
                      <span className="text-slate-300">{mat.density || '-'} g/cm³</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Cost</span>
                      <span className="text-emerald-400 font-medium">₹{mat.cost_per_kg_min || '-'}/kg</span>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
