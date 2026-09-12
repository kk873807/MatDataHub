"use client";
import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { Search, Filter, Loader2, Database, SlidersHorizontal, X, ArrowDownAZ, TrendingUp, Scale, Zap, Beaker, FileBox, Lock, Shield } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { API } from "@/lib/api";

const FREE_BROWSE_LIMIT = 40;

export default function MaterialsPage() {
  const [materials, setMaterials] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  
  // Autocomplete
  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);
  
  // Filters
  const [category, setCategory] = useState("");
  const [minTensile, setMinTensile] = useState<number | "">("");
  const [maxCost, setMaxCost] = useState<number | "">("");
  const [minThermal, setMinThermal] = useState<number | "">("");
  const [perPage, setPerPage] = useState(50);
  
  // Sorting
  const [sortBy, setSortBy] = useState("name_asc");
  const [showFilters, setShowFilters] = useState(false);

  // Tier gating
  const [userTier, setUserTier] = useState<string | null>(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const isFree = !isAdmin && (!userTier || userTier === "free");

  // Fetch user tier
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) { setUserTier("free"); return; }
    fetch(`${API}/auth/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.ok ? r.json() : null)
      .then(d => { if (d) { setUserTier(d.tier || "free"); setIsAdmin(d.is_admin || false); } else { setUserTier("free"); } })
      .catch(() => setUserTier("free"));
  }, []);

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(e.target as Node)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Fetch autocomplete suggestions
  useEffect(() => {
    if (search.length < 2) { setSuggestions([]); return; }
    const timer = setTimeout(async () => {
      try {
        const res = await fetch(`${API}/materials/autocomplete?q=${encodeURIComponent(search)}`);
        if (res.ok) {
          const data = await res.json();
          setSuggestions(data);
          setShowSuggestions(data.length > 0);
        }
      } catch { /* ignore */ }
    }, 200);
    return () => clearTimeout(timer);
  }, [search]);

  useEffect(() => {
    const fetchMaterials = async () => {
      setLoading(true);
      try {
        let url = `${API}/materials/?per_page=${perPage}`;
        
        if (search) {
          url = `${API}/materials/search?q=${encodeURIComponent(search)}&per_page=${perPage}`;
        } else {
          if (category) url += `&category=${encodeURIComponent(category)}`;
          if (minTensile !== "") url += `&min_tensile=${minTensile}`;
          if (maxCost !== "") url += `&max_cost=${maxCost}`;
          if (minThermal !== "") url += `&min_thermal_conductivity=${minThermal}`;
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
  }, [search, category, minTensile, maxCost, minThermal, perPage]);

  // Client-side sorting
  const sortedAll = [...materials].sort((a, b) => {
    if (sortBy === "name_asc") return a.name.localeCompare(b.name);
    if (sortBy === "cost_asc") return (a.cost_per_kg_min || 999999) - (b.cost_per_kg_min || 999999);
    if (sortBy === "cost_desc") return (b.cost_per_kg_min || 0) - (a.cost_per_kg_min || 0);
    if (sortBy === "tensile_desc") return (b.tensile_strength_min || 0) - (a.tensile_strength_min || 0);
    if (sortBy === "density_asc") return (a.density || 999999) - (b.density || 999999);
    return 0;
  });

  // Cap for free users
  const isFreeCapped = isFree && sortedAll.length > FREE_BROWSE_LIMIT;
  const sortedMaterials = isFree ? sortedAll.slice(0, FREE_BROWSE_LIMIT) : sortedAll;

  const activeFiltersCount = (category ? 1 : 0) + (minTensile !== "" ? 1 : 0) + (maxCost !== "" ? 1 : 0) + (minThermal !== "" ? 1 : 0);

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full overflow-y-auto">
      <div className="w-full max-w-7xl mx-auto flex flex-col gap-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="space-y-1">
            <h1 className="text-3xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-3">
              <Database className="w-8 h-8 text-emerald-500" /> Material Database
            </h1>
            <p className="text-slate-600 dark:text-slate-300">Search and filter verified engineering materials.</p>
          </div>
        </div>

        {/* Search & Top Filters */}
        <div className="flex flex-col bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 gap-5 shadow-lg">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="relative flex-1" ref={searchRef}>
              <Search className="absolute left-4 top-3.5 w-5 h-5 text-slate-500 dark:text-slate-400" />
              <input
                type="text"
                placeholder="Search materials (e.g. Aluminum 6061)..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                onFocus={() => setShowSuggestions(suggestions.length > 0)}
                className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl pl-12 pr-4 py-3 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 outline-none transition-all placeholder:text-slate-500"
              />
              <AnimatePresence>
                {showSuggestions && suggestions.length > 0 && (
                  <motion.div 
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute z-20 w-full mt-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-2xl max-h-60 overflow-y-auto overflow-x-hidden"
                  >
                    {suggestions.map((s) => (
                      <button
                        key={s.id}
                        onClick={() => {
                          setSearch(s.name);
                          setShowSuggestions(false);
                        }}
                        className="w-full text-left px-5 py-3 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors flex items-center gap-4 border-b border-slate-200 dark:border-slate-800/50 last:border-0"
                      >
                        <Search className="w-4 h-4 text-emerald-500 shrink-0" />
                        <div className="flex-1 min-w-0">
                          <p className="text-slate-900 dark:text-white text-sm font-semibold truncate">{s.name}</p>
                          <p className="text-slate-500 dark:text-slate-400 text-xs mt-0.5">{s.category}{s.grade ? ` • ${s.grade}` : ""}</p>
                        </div>
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
            
            <div className="flex gap-3">
              <div className="relative">
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="h-full appearance-none bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl pl-4 pr-10 py-3 text-slate-600 dark:text-slate-300 font-medium hover:border-slate-200 dark:hover:border-slate-700 focus:border-emerald-500 outline-none transition-colors"
                >
                  <option value="name_asc">Name (A-Z)</option>
                  <option value="cost_asc">Cost (Low-High)</option>
                  <option value="cost_desc">Cost (High-Low)</option>
                  <option value="tensile_desc">Tensile (High-Low)</option>
                  <option value="density_asc">Density (Low-High)</option>
                </select>
                <ArrowDownAZ className="w-4 h-4 text-slate-500 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>

              <button 
                onClick={() => setShowFilters(!showFilters)}
                className={`flex items-center gap-2 px-5 py-3 rounded-xl border transition-all font-semibold ${showFilters ? 'bg-emerald-900/40 border-emerald-500 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.15)]' : 'bg-slate-50 dark:bg-slate-950 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'}`}
              >
                <SlidersHorizontal className="w-5 h-5" />
                Filters {activeFiltersCount > 0 && <span className="flex items-center justify-center w-5 h-5 bg-emerald-500 text-slate-950 rounded-full text-xs ml-1">{activeFiltersCount}</span>}
              </button>
            </div>
          </div>

          {/* Advanced Filters Panel */}
          <AnimatePresence>
            {showFilters && (
              <motion.div 
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="overflow-hidden border-t border-slate-200 dark:border-slate-800/60 pt-5 mt-1"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-5">
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 dark:text-slate-400 mb-1.5 uppercase tracking-wider">Material Category</label>
                    <select
                      value={category}
                      onChange={(e) => setCategory(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-sm text-slate-900 dark:text-white appearance-none outline-none focus:border-emerald-500 transition-colors"
                    >
                      <option className="bg-white dark:bg-slate-900" value="">All Categories</option>
                      <option className="bg-white dark:bg-slate-900" value="Metal">Metals</option>
                      <option className="bg-white dark:bg-slate-900" value="Polymer">Polymers</option>
                      <option className="bg-white dark:bg-slate-900" value="Ceramic">Ceramics</option>
                      <option className="bg-white dark:bg-slate-900" value="Composite">Composites</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 dark:text-slate-400 mb-1.5 uppercase tracking-wider">Min Tensile (MPa)</label>
                    <input
                      type="number"
                      placeholder="e.g. 300"
                      value={minTensile}
                      onChange={(e) => setMinTensile(e.target.value ? Number(e.target.value) : "")}
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-sm text-slate-900 dark:text-white outline-none focus:border-emerald-500 transition-colors"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 dark:text-slate-400 mb-1.5 uppercase tracking-wider">Max Cost (₹/kg)</label>
                    <input
                      type="number"
                      placeholder="e.g. 500"
                      value={maxCost}
                      onChange={(e) => setMaxCost(e.target.value ? Number(e.target.value) : "")}
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-sm text-slate-900 dark:text-white outline-none focus:border-emerald-500 transition-colors"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 dark:text-slate-400 mb-1.5 uppercase tracking-wider">Min Thermal (W/m·K)</label>
                    <input
                      type="number"
                      placeholder="e.g. 15"
                      step="0.1"
                      value={minThermal}
                      onChange={(e) => setMinThermal(e.target.value ? Number(e.target.value) : "")}
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-sm text-slate-900 dark:text-white outline-none focus:border-emerald-500 transition-colors"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 dark:text-slate-400 mb-1.5 uppercase tracking-wider">Results Limit</label>
                    <select
                      value={perPage}
                      onChange={(e) => setPerPage(Number(e.target.value))}
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-sm text-slate-900 dark:text-white appearance-none outline-none focus:border-emerald-500 transition-colors"
                    >
                      <option className="bg-white dark:bg-slate-900" value={20}>20 materials</option>
                      <option className="bg-white dark:bg-slate-900" value={50}>50 materials</option>
                      <option className="bg-white dark:bg-slate-900" value={100}>100 materials</option>
                    </select>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          
          {/* Active Filter Tags */}
          {activeFiltersCount > 0 && (
            <div className="flex flex-wrap gap-2 pt-3 border-t border-slate-200 dark:border-slate-800/50 mt-1">
              <span className="text-xs font-semibold text-slate-500 flex items-center mr-2">Active:</span>
              {category && (
                <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-900/30 text-emerald-400 border border-emerald-800/50 rounded-full text-xs font-medium">
                  {category}
                  <button onClick={() => setCategory("")} className="hover:text-emerald-200"><X className="w-3 h-3" /></button>
                </span>
              )}
              {minTensile !== "" && (
                <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-blue-900/30 text-blue-400 border border-blue-800/50 rounded-full text-xs font-medium">
                  Tensile &gt; {minTensile} MPa
                  <button onClick={() => setMinTensile("")} className="hover:text-blue-200"><X className="w-3 h-3" /></button>
                </span>
              )}
              {maxCost !== "" && (
                <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-900/30 text-amber-400 border border-amber-800/50 rounded-full text-xs font-medium">
                  Cost &lt; ₹{maxCost}/kg
                  <button onClick={() => setMaxCost("")} className="hover:text-amber-200"><X className="w-3 h-3" /></button>
                </span>
              )}
              {minThermal !== "" && (
                <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-orange-900/30 text-orange-400 border border-orange-800/50 rounded-full text-xs font-medium">
                  Thermal &gt; {minThermal}
                  <button onClick={() => setMinThermal("")} className="hover:text-orange-200"><X className="w-3 h-3" /></button>
                </span>
              )}
              <button onClick={() => { setCategory(""); setMinTensile(""); setMaxCost(""); setMinThermal(""); }} className="text-xs text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white ml-2 underline underline-offset-2">
                Clear all
              </button>
            </div>
          )}
        </div>

        <div className="flex justify-between items-center text-sm">
          <span className="text-slate-500 dark:text-slate-400 font-medium">
            {!loading && (
              <>Showing <span className="text-slate-900 dark:text-white font-bold">{sortedMaterials.length}</span> {sortedMaterials.length === 1 ? 'material' : 'materials'}</>
            )}
          </span>
        </div>

        {/* Results */}
        {loading ? (
          <div className="flex flex-col justify-center items-center py-32 space-y-4">
            <Loader2 className="w-10 h-10 animate-spin text-emerald-500" />
            <p className="text-slate-500 dark:text-slate-400 font-medium animate-pulse">Searching material database...</p>
          </div>
        ) : sortedMaterials.length === 0 ? (
          <div className="text-center py-24 bg-white dark:bg-slate-900/40 rounded-2xl border border-slate-200 dark:border-slate-800/60 border-dashed flex flex-col items-center justify-center">
            <div className="w-20 h-20 bg-slate-100 dark:bg-slate-800/50 rounded-full flex items-center justify-center mb-6">
              <FileBox className="w-10 h-10 text-slate-500" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-2">No materials found</h3>
            <p className="text-slate-500 dark:text-slate-400 max-w-md mx-auto mb-6">We couldn't find any materials matching your specific filters and search criteria.</p>
            <button 
              onClick={() => { setSearch(""); setCategory(""); setMinTensile(""); setMaxCost(""); setMinThermal(""); }}
              className="px-6 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-900 dark:text-white rounded-2xl font-semibold transition-colors"
            >
              Clear all filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            {sortedMaterials.map((mat, i) => {
              // Determine category color
              let catColor = "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700";
              if (mat.category === "Metal") catColor = "bg-blue-900/30 text-blue-400 border-blue-800/50";
              if (mat.category === "Polymer") catColor = "bg-purple-900/30 text-purple-400 border-purple-800/50";
              if (mat.category === "Ceramic") catColor = "bg-orange-900/30 text-orange-400 border-orange-800/50";
              if (mat.category === "Composite") catColor = "bg-emerald-900/30 text-emerald-400 border-emerald-800/50";

              return (
                <motion.div
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: Math.min(i * 0.05, 0.5) }}
                  key={mat.id}
                >
                  <Link href={`/materials/${mat.id}`} className="block h-full flex flex-col p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-emerald-500/50 hover:bg-white dark:hover:bg-slate-900/80 hover:shadow-xl hover:shadow-emerald-900/10 transition-all group relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-slate-800 to-transparent opacity-20 group-hover:from-emerald-800 transition-colors pointer-events-none rounded-tr-2xl"></div>
                    
                    <div className="flex justify-between items-start mb-3 relative z-10">
                      <h3 className="font-bold text-slate-900 dark:text-white font-heading text-lg group-hover:text-emerald-400 transition-colors line-clamp-1 pr-2" title={mat.name}>{mat.name}</h3>
                    </div>
                    
                    <div className="mb-5 relative z-10">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${catColor}`}>
                        {mat.category} {mat.subcategory ? `• ${mat.subcategory}` : ''}
                      </span>
                    </div>
                    
                    <div className="space-y-2.5 text-sm mt-auto relative z-10">
                      <div className="flex justify-between items-center border-b border-slate-200 dark:border-slate-800/60 pb-1.5">
                        <span className="text-slate-500 dark:text-slate-400 flex items-center gap-1.5"><TrendingUp className="w-3.5 h-3.5" /> Yield</span>
                        <span className="text-slate-200 font-medium">{mat.yield_strength_min || '-'} MPa</span>
                      </div>
                      <div className="flex justify-between items-center border-b border-slate-200 dark:border-slate-800/60 pb-1.5">
                        <span className="text-slate-500 dark:text-slate-400 flex items-center gap-1.5"><Scale className="w-3.5 h-3.5" /> Density</span>
                        <span className="text-slate-200 font-medium">{mat.density || '-'} g/cm³</span>
                      </div>
                      <div className="flex justify-between items-center pt-0.5">
                        <span className="text-slate-500 dark:text-slate-400 flex items-center gap-1.5"><Zap className="w-3.5 h-3.5" /> Est. Cost</span>
                        <span className="text-emerald-400 font-bold">₹{mat.cost_per_kg_min || '-'}/kg</span>
                      </div>
                    </div>
                  </Link>
                </motion.div>
              );
            })}
          </div>
        )}

        {/* Free tier upgrade banner */}
        {isFreeCapped && (
          <div className="mt-6 p-6 rounded-2xl bg-gradient-to-r from-emerald-950/60 to-slate-900 border border-emerald-800/40 text-center">
            <div className="flex items-center justify-center gap-3 mb-3">
              <Lock className="w-5 h-5 text-emerald-400" />
              <h3 className="text-lg font-bold text-slate-900 dark:text-white font-heading">Showing first {FREE_BROWSE_LIMIT} of {sortedAll.length}+ materials</h3>
            </div>
            <p className="text-slate-600 dark:text-slate-300 text-sm mb-4">Upgrade to Pro to browse the full materials database with unlimited search and advanced filters.</p>
            <Link href="/account" className="inline-block px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold transition-all hover:scale-105">
              Upgrade to Pro
            </Link>
          </div>
        )}

        {/* Enterprise Data Trust Disclaimer */}
        <div className="mt-10 p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/50 flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
          <div className="w-12 h-12 bg-emerald-900/30 rounded-full flex items-center justify-center shrink-0 border border-emerald-800/50">
            <Shield className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <h4 className="text-slate-900 dark:text-white font-heading font-bold text-sm mb-1">Enterprise-Grade Data Reliability</h4>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-4xl">
              All material properties, supply chain math, economics, and ESG/CBAM emission factors are rigorously sourced from verified industry standards (ASTM, ISO, DIN), reputable global commodities indices, and validated scientific databases (e.g., ICE DB University of Bath). MatDataHub prioritizes absolute mathematical accuracy for engineering and compliance workflows.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
