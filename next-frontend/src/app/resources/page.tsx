"use client";
import { useState } from "react";
import { BookOpen, HelpCircle, LifeBuoy, Send, Loader2, CheckCircle2, Search, ChevronDown, Clock, ArrowRight, Image as ImageIcon } from "lucide-react";

export default function ResourcesPage() {
  const [activeTab, setActiveTab] = useState<"faqs" | "blogs" | "support">("faqs");

  // Support State
  const [ticket, setTicket] = useState({ name: "", email: "", category: "Technical Support", message: "", image_data: null as string | null });
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  // FAQ State
  const [faqSearch, setFaqSearch] = useState("");
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const faqs = [
    { q: "How do I upgrade to the Enterprise EU-CBAM tier?", a: "Go to your Account settings and click 'Upgrade Plan'. Enterprise plans require contacting sales to provision dedicated ESG APIs." },
    { q: "What formula does the Composite Synthesizer use?", a: "The synthesizer uses the classical Rule of Mixtures (Voigt model) for upper bounds and the inverse Rule of Mixtures (Reuss model) for lower bounds, blending volumetric fractions of Matrix and Reinforcement materials." },
    { q: "Why am I getting a '429 Too Many Requests' error?", a: "To protect our verified dataset from automated scraping, free tiers are limited to 50 lookups per day. Next.js local development may hit this quickly. Upgrade to Pro for 1000/day." },
    { q: "How does the AI Material Substitution engine work?", a: "It converts physical properties into a normalized N-dimensional vector space and calculates the Euclidean Root Mean Square (RMS) distance, weighted by your custom sliders (Cost vs Density vs Strength)." },
    { q: "Can I export my Workflows Bill of Materials?", a: "Yes. Inside any active Project Workspace, click the 'Export CSV' button to instantly download your BOM with calculated mass and pricing." }
  ];

  const blogs = [
    { title: "Modeling Thermal Expansion in Aerospace Alloys", date: "Sept 4, 2026", author: "Dr. Alara Vance", readTime: "8 min", tag: "Physics", excerpt: "Deep dive into isotropic thermal expansion formulas and why Titanium out-performs Aluminum 7075 at Mach 2.5." },
    { title: "EU-CBAM Compliance: Navigating the 2026 Carbon Tax", date: "Aug 22, 2026", author: "ESG Policy Team", readTime: "5 min", tag: "Economics", excerpt: "How to automatically audit your supply chain BOM and forecast import tariffs before manufacturing." },
    { title: "Rule of Mixtures vs Halpin-Tsai for Composites", date: "Aug 15, 2026", author: "Prof. H. Chen", readTime: "12 min", tag: "Mathematics", excerpt: "Comparing mathematical models for predicting the transverse elastic modulus of continuous fiber composites." }
  ];

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setTicket({ ...ticket, image_data: reader.result as string });
      reader.readAsDataURL(file);
    }
  };

  const handleSupportSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = {
        name: ticket.name,
        email: ticket.email,
        category: ticket.category,
        message: ticket.message,
        image_data: ticket.image_data,
        page_context: "Support Ticket"
      };
      const res = await fetch("http://127.0.0.1:8000/api/v1/feedback/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        setSubmitted(true);
        setTicket({ name: "", email: "", category: "Technical Support", message: "", image_data: null });
      }
    } catch (err) {
      console.error("Failed to submit ticket:", err);
    } finally {
      setSubmitting(false);
    }
  };

  const filteredFaqs = faqs.filter(f => f.q.toLowerCase().includes(faqSearch.toLowerCase()) || f.a.toLowerCase().includes(faqSearch.toLowerCase()));

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto relative">
      <div className="w-full max-w-5xl mx-auto space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <BookOpen className="w-8 h-8 text-indigo-400" />
            Learning & Resources
          </h1>
          <p className="text-slate-300 mt-2">Get help, read documentation, and explore advanced engineering mathematics.</p>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800 gap-6">
          <button 
            onClick={() => setActiveTab("faqs")} 
            className={`pb-3 font-semibold text-sm transition-colors relative ${activeTab === 'faqs' ? 'text-indigo-400' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <span className="flex items-center gap-2"><HelpCircle className="w-4 h-4" /> FAQs</span>
            {activeTab === 'faqs' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500 rounded-t-full" />}
          </button>
          <button 
            onClick={() => setActiveTab("blogs")} 
            className={`pb-3 font-semibold text-sm transition-colors relative ${activeTab === 'blogs' ? 'text-indigo-400' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <span className="flex items-center gap-2"><BookOpen className="w-4 h-4" /> Engineering Blogs</span>
            {activeTab === 'blogs' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500 rounded-t-full" />}
          </button>
          <button 
            onClick={() => setActiveTab("support")} 
            className={`pb-3 font-semibold text-sm transition-colors relative ${activeTab === 'support' ? 'text-indigo-400' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <span className="flex items-center gap-2"><LifeBuoy className="w-4 h-4" /> Support Centre</span>
            {activeTab === 'support' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500 rounded-t-full" />}
          </button>
        </div>

        {/* FAQ Section */}
        {activeTab === "faqs" && (
          <div className="space-y-6">
            <div className="relative">
              <Search className="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
              <input 
                type="text" 
                placeholder="Search documentation and FAQs..." 
                value={faqSearch}
                onChange={e => setFaqSearch(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-12 pr-4 py-4 text-white outline-none focus:border-indigo-500 transition-colors"
              />
            </div>
            
            <div className="space-y-3">
              {filteredFaqs.map((faq, i) => (
                <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden transition-all">
                  <button 
                    onClick={() => setOpenFaq(openFaq === i ? null : i)}
                    className="w-full text-left p-4 flex justify-between items-center hover:bg-slate-800/50"
                  >
                    <span className="font-semibold text-slate-200">{faq.q}</span>
                    <ChevronDown className={`w-5 h-5 text-slate-500 transition-transform ${openFaq === i ? 'rotate-180' : ''}`} />
                  </button>
                  {openFaq === i && (
                    <div className="p-4 pt-0 text-slate-400 text-sm leading-relaxed border-t border-slate-800/50 mt-2 pt-4 bg-slate-950/30">
                      {faq.a}
                    </div>
                  )}
                </div>
              ))}
              {filteredFaqs.length === 0 && (
                <div className="text-center p-10 text-slate-500">No results found for "{faqSearch}". Please check the Support Centre.</div>
              )}
            </div>
          </div>
        )}

        {/* Blogs Section */}
        {activeTab === "blogs" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {blogs.map((blog, i) => (
              <div onClick={() => alert("Full blog post coming soon in the next release!")} key={i} className="bg-slate-900 border border-slate-800 p-6 rounded-2xl hover:border-indigo-500/50 transition-colors group cursor-pointer flex flex-col h-full">
                <div className="flex justify-between items-start mb-4">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 bg-indigo-900/30 px-2 py-1 rounded">{blog.tag}</span>
                  <div className="flex items-center gap-1 text-slate-500 text-xs font-medium">
                    <Clock className="w-3 h-3" /> {blog.readTime}
                  </div>
                </div>
                <h3 className="text-xl font-bold text-white mb-2 group-hover:text-indigo-300 transition-colors">{blog.title}</h3>
                <p className="text-sm text-slate-400 mb-6 flex-1">{blog.excerpt}</p>
                <div className="flex justify-between items-center border-t border-slate-800 pt-4 mt-auto">
                  <span className="text-xs text-slate-500 font-medium">By {blog.author}</span>
                  <span className="text-sm font-semibold text-indigo-400 flex items-center gap-1 group-hover:gap-2 transition-all">Read <ArrowRight className="w-4 h-4"/></span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Support Section */}
        {activeTab === "support" && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-10 max-w-2xl mx-auto">
            {submitted ? (
              <div className="text-center space-y-4 py-10">
                <CheckCircle2 className="w-16 h-16 text-emerald-500 mx-auto" />
                <h2 className="text-2xl font-bold text-white">Ticket Submitted</h2>
                <p className="text-slate-400">Our engineering team has received your request and will respond to {ticket.email || 'your account email'} within 24 hours.</p>
                <button onClick={() => setSubmitted(false)} className="mt-4 px-6 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-sm font-semibold transition-colors">
                  Submit Another Ticket
                </button>
              </div>
            ) : (
              <>
                <h2 className="text-xl font-bold text-white mb-2">Open a Support Ticket</h2>
                <p className="text-slate-400 text-sm mb-6">Need help with custom physics integration or experiencing a bug? Let us know.</p>
                <form onSubmit={handleSupportSubmit} className="space-y-5">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div>
                      <label className="block text-sm font-semibold text-slate-300 mb-1">Name</label>
                      <input 
                        type="text" required
                        value={ticket.name} onChange={e => setTicket({...ticket, name: e.target.value})}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-white outline-none focus:border-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-semibold text-slate-300 mb-1">Email Address</label>
                      <input 
                        type="email" required
                        value={ticket.email} onChange={e => setTicket({...ticket, email: e.target.value})}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-white outline-none focus:border-indigo-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-300 mb-1">Category</label>
                    <select 
                      value={ticket.category} onChange={e => setTicket({...ticket, category: e.target.value})}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-white outline-none focus:border-indigo-500"
                    >
                      <option>Technical Support</option>
                      <option>Billing & Enterprise Upgrades</option>
                      <option>Feature Request</option>
                      <option>Physics/Math Clarification</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-300 mb-1">Message</label>
                    <textarea 
                      required minLength={10}
                      value={ticket.message} onChange={e => setTicket({...ticket, message: e.target.value})}
                      placeholder="Describe your issue or question in detail..."
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-white outline-none focus:border-indigo-500 min-h-[120px]"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-300 mb-2">Screenshot Attachment (Optional)</label>
                    <div className="flex items-center gap-3">
                      <label className="flex items-center gap-2 px-4 py-2 bg-slate-900 hover:bg-slate-800 text-slate-200 text-sm font-medium rounded-lg cursor-pointer transition-colors border border-slate-800">
                        <ImageIcon className="w-4 h-4" /> Upload Image
                        <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" />
                      </label>
                      {ticket.image_data && <span className="text-sm text-emerald-400 flex items-center gap-1"><CheckCircle2 className="w-4 h-4"/> Attached</span>}
                    </div>
                  </div>
                  <button 
                    type="submit" disabled={submitting}
                    className="w-full flex items-center justify-center gap-2 py-3 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold rounded-lg transition-colors"
                  >
                    {submitting ? <Loader2 className="w-5 h-5 animate-spin" /> : <><Send className="w-4 h-4"/> Submit Ticket</>}
                  </button>
                </form>
              </>
            )}
          </div>
        )}

      </div>
    </main>
  );
}
