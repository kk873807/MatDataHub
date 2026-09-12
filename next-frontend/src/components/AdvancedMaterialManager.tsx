"use client";
import { useState, useRef } from "react";
import Papa from "papaparse";
import * as XLSX from "xlsx";
import { Database, Upload, FileUp, Loader2, AlertCircle, CheckCircle2 } from "lucide-react";
import { API } from "@/lib/api";

export default function AdvancedMaterialManager() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setMessage("");
    setError("");

    try {
      if (file.name.endsWith(".csv")) {
        Papa.parse(file, {
          header: true,
          dynamicTyping: true,
          skipEmptyLines: true,
          complete: (results) => {
            uploadData(results.data);
          },
          error: (err: any) => {
            setError(`CSV Parsing Error: ${err.message}`);
            setLoading(false);
          }
        });
      } else if (file.name.endsWith(".xlsx") || file.name.endsWith(".xls")) {
        const reader = new FileReader();
        reader.onload = (evt) => {
          try {
            const bstr = evt.target?.result;
            const wb = XLSX.read(bstr, { type: "binary" });
            const wsname = wb.SheetNames[0];
            const ws = wb.Sheets[wsname];
            const data = XLSX.utils.sheet_to_json(ws);
            uploadData(data);
          } catch (err: any) {
            setError(`Excel Parsing Error: ${err.message}`);
            setLoading(false);
          }
        };
        reader.readAsBinaryString(file);
      } else {
        setError("Unsupported file format. Please upload .csv or .xlsx");
        setLoading(false);
      }
    } catch (err: any) {
      setError(`Unexpected error: ${err.message}`);
      setLoading(false);
    }
  };

  const uploadData = async (data: any[]) => {
    try {
      // Clean up data: Remove empty values and ensure numbers are properly typed
      const cleanedData = data.map((row) => {
        const cleanedRow: any = {};
        for (const key in row) {
          if (row[key] !== null && row[key] !== undefined && row[key] !== "") {
            cleanedRow[key] = row[key];
          }
        }
        return cleanedRow;
      });

      const res = await fetch(`${API}/materials/custom/bulk`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(cleanedData),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Failed to upload materials");
      }

      const result = await res.json();
      setMessage(`Successfully processed. Inserted: ${result.inserted}, Skipped (already exists): ${result.skipped}`);
    } catch (err: any) {
      setError(`Upload Error: ${err.message}`);
    } finally {
      setLoading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl mt-8">
      <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50 dark:bg-slate-950/50">
        <div className="flex items-center gap-3">
          <Database className="w-5 h-5 text-cyan-400" />
          <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading">Database Management (Materials)</h2>
        </div>
      </div>
      <div className="p-6">
        <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white font-heading mb-2 flex items-center gap-2">
            <Upload className="w-5 h-5 text-slate-500 dark:text-slate-400" /> Bulk Upload Materials
          </h3>
          <p className="text-sm text-slate-500 dark:text-slate-400 mb-6">
            Upload a .csv or .xlsx file containing material properties. The column headers must exactly match the database property names (e.g., name, category, yield_strength_min). Blank cells will be ignored.
          </p>

          <div className="flex items-center gap-4">
            <input
              type="file"
              accept=".csv, .xlsx, .xls"
              onChange={handleFileUpload}
              ref={fileInputRef}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="cursor-pointer bg-cyan-600 hover:bg-cyan-500 text-slate-900 dark:text-white font-semibold py-2 px-6 rounded-2xl transition-colors flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileUp className="w-4 h-4" />}
              {loading ? "Processing..." : "Select File"}
            </label>
            <span className="text-sm text-slate-500 dark:text-slate-400">Supported: .csv, .xlsx</span>
          </div>

          {error && (
            <div className="mt-4 p-3 bg-red-900/20 border border-red-500/50 rounded-2xl flex items-start gap-2 text-red-400 text-sm">
              <AlertCircle className="w-5 h-5 shrink-0" />
              <p>{error}</p>
            </div>
          )}

          {message && (
            <div className="mt-4 p-3 bg-emerald-900/20 border border-emerald-500/50 rounded-2xl flex items-start gap-2 text-emerald-400 text-sm">
              <CheckCircle2 className="w-5 h-5 shrink-0" />
              <p>{message}</p>
            </div>
          )}
        </div>

        <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl p-6 mt-6">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white font-heading mb-4 flex items-center gap-2">
            <Database className="w-5 h-5 text-slate-500 dark:text-slate-400" /> Add Single Material
          </h3>
          <form onSubmit={async (e) => {
            e.preventDefault();
            setLoading(true); setMessage(""); setError("");
            const formData = new FormData(e.currentTarget);
            const mat: any = {};
            formData.forEach((value, key) => {
              if (value) mat[key] = isNaN(Number(value)) || key === "name" || key === "category" || key === "subcategory" || key === "description" || key === "standard" || key === "grade" ? value : Number(value);
            });
            try {
              const res = await fetch(`${API}/materials/custom`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  "Authorization": `Bearer ${localStorage.getItem("token")}`,
                },
                body: JSON.stringify(mat),
              });
              if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Failed to upload material");
              }
              setMessage(`Successfully added ${mat.name}`);
              (e.target as HTMLFormElement).reset();
            } catch (err: any) {
              setError(`Upload Error: ${err.message}`);
            } finally {
              setLoading(false);
            }
          }}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <input type="text" name="name" placeholder="Name (Required)" required className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="text" name="category" placeholder="Category (Required)" required className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="text" name="subcategory" placeholder="Subcategory" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="text" name="grade" placeholder="Grade" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="number" step="any" name="yield_strength_min" placeholder="Yield Strength (Min)" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="number" step="any" name="tensile_strength_min" placeholder="Tensile Strength (Min)" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="number" step="any" name="elastic_modulus" placeholder="Elastic Modulus" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="number" step="any" name="density" placeholder="Density" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="number" step="any" name="cost_per_kg_min" placeholder="Cost / kg (Min)" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
            </div>
            <textarea name="description" placeholder="Description" className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white mb-4"></textarea>
            <button disabled={loading} type="submit" className="bg-cyan-600 hover:bg-cyan-500 text-slate-900 dark:text-white font-semibold py-2 px-6 rounded-2xl transition-colors">
              {loading ? "Adding..." : "Add Material"}
            </button>
          </form>
        </div>
        <div className="mt-6 text-center text-slate-500 dark:text-slate-400">
           <a href="/Admin_Material_Upload_Guide.pdf" target="_blank" className="text-cyan-400 hover:underline text-sm flex items-center justify-center gap-1">
             View Admin Upload Guide (PDF)
           </a>
        </div>
      </div>
    </div>
  );
}
