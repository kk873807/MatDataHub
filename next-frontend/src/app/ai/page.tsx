"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Bot, Send, Loader2, Sparkles } from "lucide-react";
import Link from "next/link";

export default function AskAIPage() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/ai/advise", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error(error);
      setResponse({ response: "Failed to reach the AI server. Please ensure the backend is running and you have Pro access." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col h-[calc(100vh-2rem)] p-6 lg:p-10 w-full">
      <div className="w-full max-w-4xl mx-auto flex flex-col h-full bg-neutral-900 border border-neutral-800 rounded-3xl overflow-hidden shadow-2xl relative">
        
        {/* Header */}
        <div className="p-6 border-b border-neutral-800 bg-neutral-950/50 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-600/20 flex items-center justify-center border border-blue-500/30">
            <Bot className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Ask AI Adviser</h1>
            <p className="text-sm text-neutral-400">Engineering constraint extractor & material recommender</p>
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-neutral-900">
          {/* Welcome Message */}
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center border border-blue-500/30 shrink-0 mt-1">
              <Bot className="w-4 h-4 text-blue-400" />
            </div>
            <div className="bg-neutral-800 p-4 rounded-2xl rounded-tl-none text-neutral-200 text-sm max-w-[85%]">
              Hello! I am your AI Materials Adviser. Describe your engineering constraints, and I will scan the database to recommend the perfect material.
              <br/><br/>
              <span className="text-neutral-400 italic">Example: "I need a metal under Rs. 1000/kg that can withstand 500 degrees Celsius and has a tensile strength of at least 800 MPa."</span>
            </div>
          </div>

          {/* Response */}
          {response && (
            <>
              <div className="flex gap-4 flex-row-reverse">
                <div className="w-8 h-8 rounded-full bg-emerald-600/20 flex items-center justify-center border border-emerald-500/30 shrink-0 mt-1">
                  <div className="w-4 h-4 bg-emerald-400 rounded-full" />
                </div>
                <div className="bg-emerald-900/40 border border-emerald-900 p-4 rounded-2xl rounded-tr-none text-white text-sm max-w-[85%]">
                  {prompt}
                </div>
              </div>
              
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="flex gap-4">
                <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center border border-blue-500/30 shrink-0 mt-1">
                  <Bot className="w-4 h-4 text-blue-400" />
                </div>
                <div className="bg-neutral-800 p-5 rounded-2xl rounded-tl-none text-neutral-200 text-sm max-w-[85%] space-y-4">
                  <div className="whitespace-pre-wrap">{response.response || response.detail}</div>
                  
                  {response.materials && response.materials.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-neutral-700">
                      <h4 className="font-bold flex items-center gap-2 mb-3 text-blue-300">
                        <Sparkles className="w-4 h-4" /> Top Database Matches
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {response.materials.map((m: any, i: number) => (
                          <div key={i} className="p-3 bg-neutral-900 border border-neutral-700 rounded-lg">
                            <p className="font-bold text-white text-sm">{m.name}</p>
                            <p className="text-xs text-neutral-400 mt-1">{m.category} • {m.cost}</p>
                            <p className="text-xs text-neutral-400">Strength: {m.tensile_strength}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </motion.div>
            </>
          )}
          
          {loading && (
             <div className="flex gap-4">
               <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center border border-blue-500/30 shrink-0 mt-1">
                 <Bot className="w-4 h-4 text-blue-400" />
               </div>
               <div className="bg-neutral-800 p-4 rounded-2xl rounded-tl-none flex items-center gap-3">
                 <Loader2 className="w-4 h-4 animate-spin text-blue-400" />
                 <span className="text-neutral-400 text-sm">Analyzing constraints & querying database...</span>
               </div>
             </div>
          )}
        </div>

        {/* Input Form */}
        <div className="p-4 border-t border-neutral-800 bg-neutral-950">
          <form onSubmit={handleSubmit} className="relative flex items-center">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe your material requirements..."
              disabled={loading}
              className="w-full bg-neutral-900 border border-neutral-800 rounded-xl pl-4 pr-12 py-4 text-white focus:ring-2 focus:ring-blue-500 outline-none"
            />
            <button
              type="submit"
              disabled={loading || !prompt.trim()}
              className="absolute right-2 p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
        </div>

      </div>
    </main>
  );
}
