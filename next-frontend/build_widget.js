const fs = require('fs');

const widgetContent = "use client";
import { useState, useRef, useEffect } from "react";
import { usePathname } from "next/navigation";
import { Send, Loader2, Bot, X, Maximize2, Minimize2, Lock, ArrowUpRight, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Link from "next/link";
import { API } from "@/lib/api";

export function AiChatWidget() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  
  const [prompt, setPrompt] = useState("");
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Hidden on landing page
  if (pathname === "/") return null;

  useEffect(() => {
    if (isOpen && bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [history, loading, isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    const userMsg = { role: "user", content: prompt };
    setHistory(prev => [...prev, userMsg]);
    setPrompt("");
    setLoading(true);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch(\\/ai/chat\, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": token ? \Bearer \\ : ""
        },
        body: JSON.stringify({ prompt, history })
      });
      if (res.status === 403) {
        setHistory(prev => [...prev, { role: "assistant", content: "__UPGRADE__" }]);
        setLoading(false);
        return;
      }
      const data = await res.json();
      setHistory(prev => [...prev, {
        role: "assistant",
        content: data.response,
        materials: data.materials || []
      }]);
    } catch (error) {
      setHistory(prev => [...prev, { role: "assistant", content: "Sorry, there was an error processing your request." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating Button */}
      <motion.button
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: isOpen ? 0 : 1, opacity: isOpen ? 0 : 1 }}
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 left-6 z-50 p-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-full shadow-2xl shadow-emerald-600/30 transition-all hover:scale-110 flex items-center justify-center pointer-events-auto"
      >
        <Bot className="w-7 h-7" />
      </motion.button>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 50, scale: 0.9 }}
            transition={{ type: "spring", bounce: 0.3 }}
            className={\ixed bottom-6 left-6 z-50 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-[0_10px_40px_-10px_rgba(0,0,0,0.3)] dark:shadow-[0_10px_40px_-10px_rgba(0,0,0,0.8)] flex flex-col overflow-hidden pointer-events-auto transition-all duration-300 \\}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 bg-emerald-600 text-white border-b border-emerald-700/50">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                  <Bot className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold font-heading text-sm">AI Adviser</h3>
                  <p className="text-[10px] text-emerald-100 uppercase tracking-wider font-semibold">Engineering Assistant</p>
                </div>
              </div>
              <div className="flex items-center gap-1">
                <button onClick={() => setIsExpanded(!isExpanded)} className="p-2 hover:bg-white/20 rounded-lg transition-colors">
                  {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
                </button>
                <button onClick={() => setIsOpen(false)} className="p-2 hover:bg-white/20 rounded-lg transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Chat Body */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50 dark:bg-slate-950">
              {history.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-center space-y-4 opacity-50 px-6">
                  <div className="w-16 h-16 bg-emerald-200 dark:bg-emerald-900/30 rounded-full flex items-center justify-center">
                    <Bot className="w-8 h-8 text-emerald-600 dark:text-emerald-500" />
                  </div>
                  <h4 className="font-bold text-slate-900 dark:text-white">How can I help you?</h4>
                  <p className="text-xs text-slate-600 dark:text-slate-400">Ask about material substitutions, properties, or cost optimization.</p>
                </div>
              )}
              
              {history.map((msg, i) => (
                <div key={i} className={\lex gap-3 \\}>
                  <div className={\w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-1 \\}>
                    {msg.role === "user" ? <div className="w-3 h-3 bg-emerald-500 rounded-full" /> : <Bot className="w-4 h-4 text-white" />}
                  </div>
                  
                  {msg.content === "__UPGRADE__" ? (
                    <div className="bg-amber-100 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-700 p-4 rounded-2xl rounded-tl-none max-w-[85%] space-y-3 shadow-sm">
                      <div className="flex items-center gap-2 text-amber-700 dark:text-amber-400 font-bold text-sm"><Lock className="w-4 h-4" /> Pro Feature Required</div>
                      <p className="text-slate-700 dark:text-slate-300 text-xs leading-relaxed">The AI Adviser is available to <strong>Pro</strong> and <strong>Advanced</strong> members. Upgrade your account to unlock AI-powered recommendations.</p>
                      <Link href="/account" className="inline-flex items-center gap-1 px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded-xl transition-colors">
                        Upgrade Now <ArrowUpRight className="w-3 h-3" />
                      </Link>
                    </div>
                  ) : (
                    <div className={\p-4 rounded-2xl text-sm max-w-[85%] shadow-sm \\}>
                      <div className="prose prose-sm dark:prose-invert max-w-none text-xs sm:text-sm">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          components={{
                            p: ({children}) => <p className="leading-relaxed mb-2 last:mb-0">{children}</p>,
                            ul: ({children}) => <ul className="list-disc pl-4 space-y-1 mb-2 last:mb-0">{children}</ul>,
                            ol: ({children}) => <ol className="list-decimal pl-4 space-y-1 mb-2 last:mb-0">{children}</ol>,
                            code: ({className, children}) => {
                              const isBlock = className?.includes("language-");
                              return isBlock
                                ? <pre className="bg-slate-100 dark:bg-slate-950 p-2 rounded-lg overflow-x-auto my-2 text-xs border border-slate-200 dark:border-slate-800"><code className="text-emerald-600 dark:text-emerald-400">{children}</code></pre>
                                : <code className="bg-slate-100 dark:bg-slate-950 text-emerald-600 dark:text-emerald-400 px-1 py-0.5 rounded text-[10px]">{children}</code>;
                            },
                          }}
                        >
                          {msg.content}
                        </ReactMarkdown>
                      </div>
                      
                      {msg.materials && msg.materials.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-slate-200 dark:border-slate-800 space-y-2">
                          <h4 className="font-bold flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 text-xs"><Sparkles className="w-3.5 h-3.5" /> Database Matches</h4>
                          <div className="flex flex-col gap-2">
                            {msg.materials.map((m: any, j: number) => (
                              <div key={j} className="p-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl">
                                <p className="font-bold text-slate-900 dark:text-white text-xs">{m.name}</p>
                                <div className="flex justify-between items-center mt-1 text-[10px] text-slate-500 dark:text-slate-400">
                                  <span>{m.category}</span>
                                  <span className="font-bold text-emerald-600 dark:text-emerald-500">{m.cost}</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}

              {loading && (
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center shrink-0 mt-1 shadow-sm">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-2xl rounded-tl-none flex items-center gap-3 shadow-sm">
                    <Loader2 className="w-4 h-4 animate-spin text-emerald-600 dark:text-emerald-500" />
                    <span className="text-slate-500 dark:text-slate-400 text-xs font-medium tracking-wide">Analyzing...</span>
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>

            {/* Input Area */}
            <div className="p-3 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800">
              <form onSubmit={handleSubmit} className="relative flex items-center">
                <input
                  type="text"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Ask AI Adviser..."
                  disabled={loading}
                  className="w-full bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl pl-4 pr-12 py-3 text-sm text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                />
                <button type="submit" disabled={loading || !prompt.trim()} className="absolute right-1.5 p-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl transition-colors disabled:opacity-40">
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
;

fs.writeFileSync('src/components/AiChatWidget.tsx', widgetContent, 'utf-8');
console.log('Created AiChatWidget.tsx!');
