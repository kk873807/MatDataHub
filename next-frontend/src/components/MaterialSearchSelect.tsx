"use client";
import { useState, useRef, useEffect } from "react";
import { Search, ChevronDown, Check } from "lucide-react";

export default function MaterialSearchSelect({ 
  materials, 
  onSelect, 
  placeholder = "Search and select a material...",
  disabled = false,
  excludeIds = []
}: { 
  materials: any[];
  onSelect: (id: string) => void;
  placeholder?: string;
  disabled?: boolean;
  excludeIds?: string[];
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState("");
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const filtered = materials.filter(m => 
    !excludeIds.includes(m.id.toString()) &&
    m.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="relative w-full max-w-sm" ref={ref}>
      <div 
        onClick={() => !disabled && setIsOpen(!isOpen)}
        className={`w-full bg-slate-50 dark:bg-slate-950 border ${disabled ? 'border-slate-200 dark:border-slate-800 opacity-50 cursor-not-allowed' : 'border-slate-200 dark:border-slate-800 hover:border-slate-600 cursor-pointer'} rounded-2xl px-4 py-3 flex items-center justify-between text-slate-600 dark:text-slate-300 transition-colors`}
      >
        <span className="truncate text-sm">{placeholder}</span>
        <ChevronDown className="w-4 h-4 text-slate-500" />
      </div>

      {isOpen && (
        <div className="absolute z-50 top-full left-0 mt-2 w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-[300px]">
          <div className="p-3 border-b border-slate-200 dark:border-slate-800 relative bg-slate-50 dark:bg-slate-950/50">
            <Search className="w-4 h-4 absolute left-6 top-1/2 -translate-y-1/2 text-slate-500" />
            <input 
              autoFocus
              type="text" 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by name..."
              className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl pl-10 pr-4 py-2 text-sm text-slate-900 dark:text-white outline-none focus:border-indigo-500"
            />
          </div>
          <div className="overflow-y-auto flex-1 p-2 space-y-1">
            {filtered.length === 0 ? (
              <div className="p-3 text-center text-sm text-slate-500">No materials found.</div>
            ) : (
              filtered.map(m => (
                <button
                  key={m.id}
                  onClick={() => {
                    onSelect(m.id.toString());
                    setIsOpen(false);
                    setSearch("");
                  }}
                  className="w-full text-left px-3 py-2 rounded-2xl hover:bg-slate-100 dark:hover:bg-slate-800 text-sm text-slate-600 dark:text-slate-300 transition-colors flex items-center justify-between group"
                >
                  <span className="truncate pr-4">{m.name}</span>
                  <span className="text-[10px] text-slate-500 uppercase font-bold px-2 py-0.5 bg-slate-50 dark:bg-slate-950 rounded hidden group-hover:block">{m.category}</span>
                </button>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
