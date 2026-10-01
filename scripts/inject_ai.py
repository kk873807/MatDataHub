import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\MaterialManager.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I need to add Lucide icon Sparkles
if 'Sparkles' not in content:
    content = content.replace('import { Database, Upload, FileUp, Loader2, AlertCircle, CheckCircle2 } from "lucide-react";', 'import { Database, Upload, FileUp, Loader2, AlertCircle, CheckCircle2, Sparkles } from "lucide-react";')

# I need to add states for AI scraper
if 'const [aiQuery, setAiQuery] = useState("");' not in content:
    content = content.replace('const [error, setError] = useState("");', 'const [error, setError] = useState("");\n  const [aiQuery, setAiQuery] = useState("");\n  const [aiLoading, setAiLoading] = useState(false);')

# Inject the AI block
ai_block = '''
        <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl p-6 mt-6 border-l-4 border-l-purple-500">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white font-heading mb-4 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-500" /> AI Material Synthesizer
          </h3>
          <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">
            Type a material family (e.g., "Inconel alloys" or "High-density Polyethylene") and the AI will synthesize physical properties for 5-10 specific grades and auto-insert them into the database.
          </p>
          <form onSubmit={async (e) => {
            e.preventDefault();
            if (!aiQuery.trim()) return;
            setAiLoading(true); setMessage(""); setError("");
            try {
              const res = await fetch(`${API}/admin/scraper/ai`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  "Authorization": `Bearer ${localStorage.getItem("token")}`,
                },
                body: JSON.stringify({ query: aiQuery }),
              });
              const data = await res.json();
              if (!res.ok) throw new Error(data.detail || "AI synthesis failed");
              setMessage(data.message || "Successfully synthesized materials!");
              setAiQuery("");
            } catch (err: any) {
              setError(`AI Error: ${err.message}`);
            } finally {
              setAiLoading(false);
            }
          }}>
            <div className="flex gap-4">
              <input 
                type="text" 
                value={aiQuery} 
                onChange={(e) => setAiQuery(e.target.value)} 
                placeholder="E.g., Titanium alloys..." 
                className="flex-1 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white focus:outline-none focus:border-purple-500" 
              />
              <button disabled={aiLoading} type="submit" className="bg-purple-600 hover:bg-purple-500 text-white font-semibold py-2 px-6 rounded-xl transition-colors min-w-[140px] flex justify-center items-center">
                {aiLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Synthesize"}
              </button>
            </div>
          </form>
        </div>
        <div className="mt-6 text-center text-slate-500 dark:text-slate-400">
'''

bad = '''        <div className="mt-6 text-center text-slate-500 dark:text-slate-400">'''

if bad in content:
    content = content.replace(bad, ai_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added AI Synthesizer block")
else:
    print("Could not find block to insert AI Synthesizer")
