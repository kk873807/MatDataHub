"use client";
import { useState } from "react";
import { ChevronDown, Search, HelpCircle, MessageSquare } from "lucide-react";
import Link from "next/link";

const FAQS = [
  {
    category: "General",
    questions: [
      { q: "What is MatDataHub?", a: "MatDataHub is an AI-powered materials database and analytics platform designed to help engineers and researchers discover, substitute, and analyze materials." },
      { q: "How accurate is the AI Adviser?", a: "Our AI Adviser is fine-tuned on peer-reviewed materials science literature and real-world supply chain data, achieving over 95% accuracy in property predictions." },
    ]
  },
  {
    category: "Pricing & Accounts",
    questions: [
      { q: "What is the difference between Pro and Advanced?", a: "Pro gives you 25 AI queries per day and access to all basic analytics. Advanced unlocks unlimited AI queries, the composite synthesizer, and API access." },
      { q: "Can I cancel my subscription anytime?", a: "Yes, you can cancel your subscription from your Account dashboard at any time. Your access will remain active until the end of your billing cycle." },
    ]
  },
  {
    category: "Technical",
    questions: [
      { q: "How do I export my workspaces?", a: "Inside any workspace, click the 'Export' button in the top right to download your data as a CSV or PDF report." },
      { q: "Where does the pricing data come from?", a: "We aggregate historical and real-time pricing data from global metal exchanges, supplier catalogs, and trade registries." },
    ]
  }
];

export default function FaqPage() {
  const [openQ, setOpenQ] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  const filteredFaqs = FAQS.map(cat => ({
    ...cat,
    questions: cat.questions.filter(q => q.q.toLowerCase().includes(search.toLowerCase()) || q.a.toLowerCase().includes(search.toLowerCase()))
  })).filter(cat => cat.questions.length > 0);

  return (
    <main className="min-h-screen bg-slate-50 dark:bg-slate-950 pt-10 pb-24">
      <div className="max-w-4xl mx-auto px-4 sm:px-6">
        
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white font-heading mb-6">How can we help?</h1>
          <div className="relative max-w-xl mx-auto">
            <Search className="w-5 h-5 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
            <input 
              type="text" 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search for answers..." 
              className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl pl-12 pr-4 py-4 text-slate-900 dark:text-white shadow-sm focus:border-blue-500 outline-none transition-colors text-lg"
            />
          </div>
        </div>

        <div className="space-y-12">
          {filteredFaqs.length === 0 ? (
            <div className="text-center py-12">
              <HelpCircle className="w-12 h-12 text-slate-300 dark:text-slate-700 mx-auto mb-4" />
              <p className="text-slate-500 dark:text-slate-400">No results found for "{search}"</p>
            </div>
          ) : (
            filteredFaqs.map((cat, i) => (
              <div key={i}>
                <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-6 flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-500"></span> {cat.category}
                </h2>
                <div className="space-y-3">
                  {cat.questions.map((q, j) => {
                    const id = `q-${i}-${j}`;
                    const isOpen = openQ === id;
                    return (
                      <div key={j} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden transition-all">
                        <button 
                          onClick={() => setOpenQ(isOpen ? null : id)}
                          className="w-full flex items-center justify-between p-5 text-left focus:outline-none"
                        >
                          <span className="font-semibold text-slate-900 dark:text-white">{q.q}</span>
                          <ChevronDown className={`w-5 h-5 text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
                        </button>
                        {isOpen && (
                          <div className="px-5 pb-5 pt-1 text-slate-600 dark:text-slate-400 leading-relaxed text-sm border-t border-slate-100 dark:border-slate-800/50 mt-2 pt-4">
                            {q.a}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            ))
          )}
        </div>

        <div className="mt-16 p-8 bg-gradient-to-r from-blue-600 to-violet-600 rounded-3xl text-center text-white">
          <MessageSquare className="w-10 h-10 mx-auto mb-4 opacity-80" />
          <h3 className="text-2xl font-bold font-heading mb-2">Still have questions?</h3>
          <p className="text-blue-100 mb-6 max-w-lg mx-auto">Our engineering support team is ready to help you with any technical or account-related inquiries.</p>
          <Link href="/contact" className="inline-block bg-white text-blue-600 hover:bg-slate-50 font-bold px-8 py-3 rounded-full transition-all hover:scale-105 shadow-lg">
            Contact Support
          </Link>
        </div>

      </div>
    </main>
  );
}
