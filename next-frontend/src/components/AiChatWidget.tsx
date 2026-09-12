"use client";
import { useState, useRef, useEffect } from "react";
import { usePathname } from "next/navigation";
import { Send, Loader2, Bot, X, Maximize2, Minimize2, Lock, ArrowUpRight, Sparkles, Trash2, Download, ChevronRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Link from "next/link";
import { API } from "@/lib/api";

type Message = {
  role: "user" | "assistant" | "ai";
  content: string;
  materials?: any[];
};

const PROMPT_CHIPS = [
  "Best metal for 500°C operating temperature",
  "Cheapest corrosion-resistant polymer under Rs. 500/kg",
  "Lightweight material with tensile strength above 700 MPa",
  "Best ceramic for electrical insulation",
  "Steel alternative for marine environment",
];

export function AiChatWidget() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  
  const [prompt, setPrompt] = useState("");
  const [history, setHistory] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const [tier, setTier] = useState<string | null>(null);
  const [isAdmin, setIsAdmin] = useState(false);

  // Hidden on landing page
  if (pathname === "/") return null;

  // Daily message limit tracking
  const todayKey = typeof window !== "undefined" ? `ai_msg_${new Date().toISOString().slice(0, 10)}` : "ai_msg_default";
  const getDailyCount = () => {
    if (typeof window === "undefined") return 0;
    return parseInt(localStorage.getItem(todayKey) || "0", 10);
  };
  const incrementDaily = () => {
    if (typeof window === "undefined") return;
    localStorage.setItem(todayKey, String(getDailyCount() + 1));
  };
  const getDailyLimit = () => {
    if (isAdmin) return Infinity;
    if (tier === "advanced") return Infinity;
    if (tier === "pro") return 25;
    return 5;
  };
  const isLimitReached = getDailyCount() >= getDailyLimit();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) { setTier("free"); return; }
    fetch(`${API}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(r => r.ok ? r.json() : null)
      .then(d => { if (d) { setTier(d.tier || "free"); setIsAdmin(d.is_admin || false); } else { setTier("free"); } })
      .catch(() => setTier("free"));
  }, []);

  // Load chat history
  useEffect(() => {
    const saved = localStorage.getItem("ai_chat_history");
    if (saved) {
      try { setHistory(JSON.parse(saved)); } catch (e) {}
    }
  }, []);

  // Save chat history
  useEffect(() => {
    if (history.length > 0) {
      localStorage.setItem("ai_chat_history", JSON.stringify(history));
    }
  }, [history]);

  useEffect(() => {
    if (isOpen && bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [history, loading, isOpen]);

  const handleSubmit = async (e: React.FormEvent | null, overridePrompt?: string) => {
    e?.preventDefault();
    const query = overridePrompt ?? prompt;
    if (!query.trim() || loading) return;

    // Check daily limit
    if (getDailyCount() >= getDailyLimit()) {
      const limitNum = getDailyLimit();
      setHistory(prev => [...prev,
        { role: "user", content: query },
        { role: "assistant", content: `You've used all ${limitNum} of your daily AI queries. ${tier === "free" ? "Upgrade to Pro for 25 queries/day." : "Upgrade to Advanced for unlimited queries."}` }
      ]);
      setPrompt("");
      return;
    }

    const userMsg: Message = { role: "user", content: query };
    setHistory(prev => [...prev, userMsg]);
    setPrompt("");
    setLoading(true);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${API}/ai/advise`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: JSON.stringify({ prompt: query })
      });
      
      const data = await res.json();
      
      if (res.status === 403) {
        setHistory(prev => [...prev, { role: "assistant", content: "__UPGRADE__" }]);
      } else if (res.status === 401) {
        setHistory(prev => [...prev, { role: "assistant", content: "Please sign in to use the AI Adviser." }]);
      } else {
        incrementDaily();
        setHistory(prev => [...prev, {
          role: "assistant",
          content: data.response || data.detail || "Sorry, I could not process that.",
          materials: data.materials || []
        }]);
      }
    } catch (error) {
      setHistory(prev => [...prev, { role: "assistant", content: "Sorry, there was an error processing your request. Please check the backend is running." }]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setHistory([]);
    localStorage.removeItem("ai_chat_history");
  };

  const exportChat = () => {
    const text = history.map(m => (m.role === "user" ? "USER: " : "AI: ") + m.content).join("\n\n");
    const blob = new Blob([text], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Chat_History.txt";
    a.click();
  };

  return (
    <>
      {/* Floating Button */}
      <motion.button
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: isOpen ? 0 : 1, opacity: isOpen ? 0 : 1 }}
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 lg:left-6 lg:right-auto z-50 p-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-full shadow-2xl shadow-emerald-600/30 transition-all hover:scale-110 flex items-center justify-center pointer-events-auto"
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
            className={`fixed bottom-6 right-6 lg:left-6 lg:right-auto z-50 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-[0_10px_40px_-10px_rgba(0,0,0,0.3)] dark:shadow-[0_10px_40px_-10px_rgba(0,0,0,0.8)] flex flex-col overflow-hidden pointer-events-auto transition-all duration-300 origin-bottom-right lg:origin-bottom-left ${
              isExpanded ? "w-[90vw] md:w-[700px] h-[85vh] max-h-[900px]" : "w-[90vw] md:w-[450px] h-[70vh] max-h-[700px]"
            }`}
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
                {history.length > 0 && (
                  <>
                    <button onClick={exportChat} title="Export Chat" className="p-2 hover:bg-white/20 rounded-lg transition-colors">
                      <Download className="w-4 h-4" />
                    </button>
                    <button onClick={clearChat} title="Clear Chat" className="p-2 hover:bg-white/20 rounded-lg transition-colors">
                      <Trash2 className="w-4 h-4" />
                    </button>
                    <div className="w-[1px] h-4 bg-white/30 mx-1"></div>
                  </>
                )}
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
                <div className="flex flex-col h-full space-y-4 pt-6 px-2">
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center shadow-sm shrink-0">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-2xl rounded-tl-none text-slate-700 dark:text-slate-200 text-sm max-w-[95%] space-y-4 shadow-sm">
                      <p>Hello! I am your AI Materials Adviser. Describe your engineering constraints and I will recommend the best materials from our database.</p>
                      <div className="flex flex-wrap gap-2 pt-2">
                        {PROMPT_CHIPS.map((chip) => (
                          <button
                            key={chip}
                            onClick={() => handleSubmit(null, chip)}
                            className="flex items-center gap-1 px-3 py-1.5 bg-emerald-50 dark:bg-slate-800 hover:bg-emerald-100 dark:hover:bg-slate-700 border border-emerald-200 dark:border-slate-700 text-emerald-800 dark:text-emerald-300 text-xs rounded-full transition-all text-left leading-tight"
                          >
                            <ChevronRight className="w-3 h-3 shrink-0" />
                            {chip}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {history.map((msg, i) => (
                <div key={i} className={`flex gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-1 ${
                    msg.role === "user" ? "bg-emerald-200 dark:bg-emerald-900/40" : "bg-emerald-600 shadow-sm"
                  }`}>
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
                    <div className={`p-4 rounded-2xl text-sm max-w-[90%] shadow-sm overflow-hidden ${
                      msg.role === "user" 
                        ? "bg-emerald-100 dark:bg-emerald-900/30 border border-emerald-200 dark:border-emerald-800 rounded-tr-none text-slate-900 dark:text-white" 
                        : "bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-tl-none text-slate-700 dark:text-slate-200"
                    }`}>
                      <div className="prose prose-sm dark:prose-invert max-w-none text-xs sm:text-sm [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          components={{
                            h1: ({children}) => <h3 className="text-lg font-bold text-slate-900 dark:text-white font-heading mt-4 mb-2">{children}</h3>,
                            h2: ({children}) => <h4 className="text-base font-bold text-slate-900 dark:text-white font-heading mt-3 mb-2">{children}</h4>,
                            h3: ({children}) => <h5 className="text-sm font-bold text-emerald-600 dark:text-emerald-400 mt-3 mb-1">{children}</h5>,
                            p: ({children}) => <p className="leading-relaxed mb-2 last:mb-0">{children}</p>,
                            strong: ({children}) => <strong className="text-slate-900 dark:text-white font-bold">{children}</strong>,
                            ul: ({children}) => <ul className="list-disc pl-4 space-y-1 mb-2 last:mb-0">{children}</ul>,
                            ol: ({children}) => <ol className="list-decimal pl-4 space-y-1 mb-2 last:mb-0">{children}</ol>,
                            li: ({children}) => <li className="leading-relaxed">{children}</li>,
                            blockquote: ({children}) => <blockquote className="border-l-2 border-emerald-500 pl-3 my-2 text-slate-500 dark:text-slate-400 italic">{children}</blockquote>,
                            table: ({children}) => <div className="overflow-x-auto my-3 rounded-xl border border-slate-200 dark:border-slate-700"><table className="w-full text-left text-xs">{children}</table></div>,
                            thead: ({children}) => <thead className="bg-slate-50 dark:bg-slate-800 text-slate-500 dark:text-slate-400 uppercase text-xs">{children}</thead>,
                            tbody: ({children}) => <tbody className="divide-y divide-slate-200 dark:divide-slate-700">{children}</tbody>,
                            tr: ({children}) => <tr className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">{children}</tr>,
                            th: ({children}) => <th className="px-3 py-2 font-semibold whitespace-nowrap">{children}</th>,
                            td: ({children}) => <td className="px-3 py-2 text-slate-600 dark:text-slate-300 whitespace-nowrap">{children}</td>,
                            hr: () => <hr className="border-slate-200 dark:border-slate-700 my-3" />,
                            code: ({className, children}) => {
                              const isBlock = className?.includes("language-");
                              return isBlock
                                ? <pre className="bg-slate-100 dark:bg-slate-950 p-3 rounded-xl overflow-x-auto my-2 text-xs border border-slate-200 dark:border-slate-800"><code className="text-emerald-600 dark:text-emerald-400">{children}</code></pre>
                                : <code className="bg-slate-100 dark:bg-slate-950 text-emerald-600 dark:text-emerald-400 px-1 py-0.5 rounded text-[10px] break-words">{children}</code>;
                            },
                          }}
                        >
                          {msg.content}
                        </ReactMarkdown>
                      </div>
                      
                      {msg.materials && msg.materials.length > 0 && (
                        <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-800 space-y-3">
                          <h4 className="font-bold flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 text-xs"><Sparkles className="w-3.5 h-3.5" /> Database Matches</h4>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {msg.materials.map((m: any, j: number) => (
                              <div key={j} className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl">
                                <p className="font-bold text-slate-900 dark:text-white text-xs truncate">{m.name}</p>
                                <div className="flex justify-between items-center mt-1 text-[10px] text-slate-500 dark:text-slate-400">
                                  <span>{m.category}</span>
                                  <span className="font-bold text-emerald-600 dark:text-emerald-500">{m.cost}</span>
                                </div>
                                {m.tensile_strength && (
                                  <p className="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">Tensile: {m.tensile_strength}</p>
                                )}
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
            <div className="p-3 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex flex-col gap-2">
              <form onSubmit={handleSubmit} className="relative flex items-center">
                <input
                  type="text"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Describe your material requirements..."
                  disabled={loading}
                  className="w-full bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl pl-4 pr-12 py-3 text-sm text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                />
                <button type="submit" disabled={loading || !prompt.trim()} className="absolute right-1.5 p-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl transition-colors disabled:opacity-40">
                  <Send className="w-4 h-4" />
                </button>
              </form>
              
              <div className="flex justify-between items-center px-2 text-[10px] font-medium uppercase tracking-wider text-slate-400">
                {tier && tier !== "free" && <span>{tier} access</span>}
                {tier && getDailyLimit() !== Infinity && (
                  <span className={isLimitReached ? "text-red-500" : ""}>
                    {getDailyCount()}/{getDailyLimit()} today
                  </span>
                )}
                {!tier && <span className="ml-auto">AI Adviser available for Pro and Advanced users only</span>}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
