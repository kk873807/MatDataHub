"use client";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bot, Send, Loader2, Sparkles, Lock, ArrowUpRight, ChevronRight } from "lucide-react";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { API } from "@/lib/api";

type Message = {
  role: "user" | "ai";
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

export default function AskAIPage() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);

  // Load chat history
  useEffect(() => {
    const saved = localStorage.getItem("ai_chat_history");
    if (saved) {
      try { setMessages(JSON.parse(saved)); } catch (e) {}
    }
  }, []);

  // Save chat history
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem("ai_chat_history", JSON.stringify(messages));
    }
  }, [messages]);
  const [tier, setTier] = useState<string | null>(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Daily message limit tracking
  const todayKey = `ai_msg_${new Date().toISOString().slice(0, 10)}`;
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

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSubmit = async (e: React.FormEvent | null, overridePrompt?: string) => {
    e?.preventDefault();
    const query = overridePrompt ?? prompt;
    if (!query.trim() || loading) return;

    // Check daily limit
    if (getDailyCount() >= getDailyLimit()) {
      const limitNum = getDailyLimit();
      setMessages(prev => [...prev,
        { role: "user", content: query },
        { role: "ai", content: `You've used all ${limitNum} of your daily AI queries. ${tier === "free" ? "Upgrade to Pro for 25 queries/day." : "Upgrade to Advanced for unlimited queries."}` }
      ]);
      setPrompt("");
      return;
    }

    setMessages(prev => [...prev, { role: "user", content: query }]);
    setPrompt("");
    setLoading(true);
    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${API}/ai/advise`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ prompt: query }),
      });
      const data = await res.json();
      if (res.status === 403) {
        setMessages(prev => [...prev, { role: "ai", content: "__UPGRADE__" }]);
      } else if (res.status === 401) {
        setMessages(prev => [...prev, { role: "ai", content: "Please sign in to use the AI Adviser." }]);
      } else {
        incrementDaily();
        setMessages(prev => [...prev, {
          role: "ai",
          content: data.response || data.detail || "Sorry, I could not process that.",
          materials: data.materials,
        }]);
      }
    } catch {
      setMessages(prev => [...prev, { role: "ai", content: "Network error. Please check the backend is running." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col h-[calc(100vh-2rem)] p-6 lg:p-10 w-full">
      <div className="w-full max-w-4xl mx-auto flex flex-col h-full bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl relative">

        <div className="p-6 border-b border-slate-800 bg-slate-950/50 flex items-center gap-4 flex-wrap">          <div className="w-full flex justify-end gap-2 mb-2 order-first md:order-last md:mb-0 md:w-auto md:ml-auto">            {messages.length > 0 && <button onClick={() => { setMessages([]); localStorage.removeItem("ai_chat_history"); }} className="px-3 py-1 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 text-xs font-bold rounded-full transition-colors">Clear Chat</button>}            {messages.length > 0 && <button onClick={() => { const text = messages.map(m => (m.role === "user" ? "USER: " : "AI: ") + m.content).join("\n\n"); const blob = new Blob([text], { type: "text/plain" }); const url = window.URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = "Chat_History.txt"; a.click(); }} className="px-3 py-1 bg-blue-900/30 hover:bg-blue-800/50 border border-blue-700/50 text-blue-400 text-xs font-bold rounded-full transition-colors">Export Chat</button>}          </div>
          <div className="w-12 h-12 rounded-xl bg-blue-600/20 flex items-center justify-center border border-blue-500/30">
            <Bot className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">AI Materials Adviser</h1>
            <p className="text-sm text-slate-400">Describe your requirements and I will recommend the best materials.</p>
          </div>
          {tier && tier !== "free" && (
            <span className="px-3 py-1 bg-emerald-900/30 border border-emerald-700/50 text-emerald-400 text-xs font-bold rounded-full uppercase tracking-wider">
              {tier} access
            </span>
          )}
          {tier && getDailyLimit() !== Infinity && (
            <span className={`${tier !== "free" ? "" : "ml-auto"} px-3 py-1 ${isLimitReached ? "bg-red-900/30 border-red-700/50 text-red-400" : "bg-slate-800 border-slate-700 text-slate-400"} border text-xs font-bold rounded-full`}>
              {getDailyCount()}/{getDailyLimit()} today
            </span>
          )}
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-900">
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center border border-blue-500/30 shrink-0 mt-1">
              <Bot className="w-4 h-4 text-blue-400" />
            </div>
            <div className="bg-slate-800 p-4 rounded-2xl rounded-tl-none text-slate-200 text-sm max-w-[85%] space-y-3">
              <p>Hello! I am your AI Materials Adviser. Describe your engineering constraints and I will recommend the best materials from our database.</p>
              {messages.length === 0 && (
                <div className="flex flex-wrap gap-2 pt-2">
                  {PROMPT_CHIPS.map((chip) => (
                    <button
                      key={chip}
                      onClick={() => handleSubmit(null, chip)}
                      className="flex items-center gap-1 px-3 py-1.5 bg-slate-700 hover:bg-blue-900/50 hover:border-blue-700 border border-slate-600 text-slate-300 text-xs rounded-full transition-all"
                    >
                      <ChevronRight className="w-3 h-3" />
                      {chip}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          <AnimatePresence>
            {messages.map((msg, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center border shrink-0 mt-1 ${msg.role === "user" ? "bg-emerald-600/20 border-emerald-500/30" : "bg-blue-600/20 border-blue-500/30"}`}>
                  {msg.role === "user" ? <div className="w-3 h-3 bg-emerald-400 rounded-full" /> : <Bot className="w-4 h-4 text-blue-400" />}
                </div>
                {msg.content === "__UPGRADE__" ? (
                  <div className="bg-amber-900/20 border border-amber-700/50 p-5 rounded-2xl rounded-tl-none max-w-[85%] space-y-3">
                    <div className="flex items-center gap-2 text-amber-400 font-bold"><Lock className="w-4 h-4" /> Pro Feature Required</div>
                    <p className="text-slate-300 text-sm">The AI Adviser is available to <strong>Pro</strong> and <strong>Advanced</strong> members. Upgrade your account to unlock AI-powered recommendations.</p>
                    <Link href="/account" className="inline-flex items-center gap-1 px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white text-sm font-bold rounded-lg transition-colors">
                      Upgrade Now <ArrowUpRight className="w-4 h-4" />
                    </Link>
                  </div>
                ) : (
                  <div className={`p-4 rounded-2xl text-sm max-w-[85%] space-y-4 ${msg.role === "user" ? "bg-emerald-900/40 border border-emerald-900 rounded-tr-none text-white" : "bg-slate-800 rounded-tl-none text-slate-200"}`}>
                    <div className="prose prose-invert prose-sm max-w-none [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          h1: ({children}) => <h3 className="text-lg font-bold text-white mt-4 mb-2">{children}</h3>,
                          h2: ({children}) => <h4 className="text-base font-bold text-white mt-3 mb-2">{children}</h4>,
                          h3: ({children}) => <h5 className="text-sm font-bold text-blue-300 mt-3 mb-1">{children}</h5>,
                          p: ({children}) => <p className="text-slate-200 leading-relaxed mb-2">{children}</p>,
                          strong: ({children}) => <strong className="text-white font-bold">{children}</strong>,
                          ul: ({children}) => <ul className="list-disc list-inside space-y-1 my-2 text-slate-200">{children}</ul>,
                          ol: ({children}) => <ol className="list-decimal list-inside space-y-1 my-2 text-slate-200">{children}</ol>,
                          li: ({children}) => <li className="text-slate-200 leading-relaxed">{children}</li>,
                          code: ({className, children}) => {
                            const isBlock = className?.includes("language-");
                            return isBlock
                              ? <pre className="bg-slate-900 border border-slate-700 rounded-lg p-3 overflow-x-auto my-2"><code className="text-emerald-400 text-xs">{children}</code></pre>
                              : <code className="bg-slate-900 text-emerald-400 px-1.5 py-0.5 rounded text-xs">{children}</code>;
                          },
                          table: ({children}) => <div className="overflow-x-auto my-3 rounded-lg border border-slate-700"><table className="w-full text-left text-xs">{children}</table></div>,
                          thead: ({children}) => <thead className="bg-slate-900 text-slate-400 uppercase text-xs">{children}</thead>,
                          tbody: ({children}) => <tbody className="divide-y divide-slate-700/50">{children}</tbody>,
                          tr: ({children}) => <tr className="hover:bg-slate-700/30 transition-colors">{children}</tr>,
                          th: ({children}) => <th className="px-3 py-2 font-semibold whitespace-nowrap">{children}</th>,
                          td: ({children}) => <td className="px-3 py-2 text-slate-300 whitespace-nowrap">{children}</td>,
                          blockquote: ({children}) => <blockquote className="border-l-2 border-blue-500 pl-3 my-2 text-slate-400 italic">{children}</blockquote>,
                          hr: () => <hr className="border-slate-700 my-3" />,
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                    {msg.materials && msg.materials.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-slate-700">
                        <h4 className="font-bold flex items-center gap-2 mb-3 text-blue-300"><Sparkles className="w-4 h-4" /> Top Database Matches</h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                          {msg.materials.map((m: any, j: number) => (
                            <div key={j} className="p-3 bg-slate-900 border border-slate-700 rounded-lg">
                              <p className="font-bold text-white text-sm">{m.name}</p>
                              <p className="text-xs text-slate-400 mt-1">{m.category} · {m.cost}</p>
                              <p className="text-xs text-slate-400">Tensile: {m.tensile_strength}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {loading && (
            <div className="flex gap-4">
              <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center border border-blue-500/30 shrink-0 mt-1">
                <Bot className="w-4 h-4 text-blue-400" />
              </div>
              <div className="bg-slate-800 p-4 rounded-2xl rounded-tl-none flex items-center gap-3">
                <Loader2 className="w-4 h-4 animate-spin text-blue-400" />
                <span className="text-slate-400 text-sm">Analyzing constraints and querying database...</span>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="p-4 border-t border-slate-800 bg-slate-950">
          <form onSubmit={handleSubmit} className="relative flex items-center">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe your material requirements..."
              disabled={loading}
              className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-4 pr-14 py-4 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            />
            <button type="submit" disabled={loading || !prompt.trim()} className="absolute right-2 p-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-40">
              <Send className="w-4 h-4" />
            </button>
          </form>
          <p className="text-xs text-slate-600 mt-2 text-center">AI Adviser available for Pro and Advanced users only.</p>
        </div>
      </div>
    </main>
  );
}
