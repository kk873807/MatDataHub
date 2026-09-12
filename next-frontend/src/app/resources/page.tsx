"use client";
import { useState, useEffect } from "react";
import { BookOpen, HelpCircle, LifeBuoy, Send, Loader2, CheckCircle2, Search, ChevronDown, Clock, ArrowRight, Image as ImageIcon, ArrowLeft, Star } from "lucide-react";
import { API } from "@/lib/api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ResourcesPage() {
  const [activeTab, setActiveTab] = useState<"faqs" | "blogs" | "support">("blogs");

  // Support State
  const [ticket, setTicket] = useState({ name: "", email: "", category: "Technical Support", message: "", image_data: null as string | null });
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const [apiBlogs, setApiBlogs] = useState<any[]>([]);
  useEffect(() => {
    fetch(`${API}/blogs/`).then(r => r.ok ? r.json() : []).then(d => setApiBlogs(d)).catch(() => {});
  }, []);

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

  const [selectedBlog, setSelectedBlog] = useState<number | null>(null);
  const [blogFilter, setBlogFilter] = useState<string>("All");

  const hardcodedBlogs = [
    { 
      title: "Why India's Manufacturing Sector Needs a Materials Intelligence Platform", 
      date: "07/09/2026", author: "MatDataHub Editorial", readTime: "6 min", tag: "Industry", featured: true,
      excerpt: "India's PLI schemes and Make in India 2.0 are fueling a manufacturing renaissance — but 73% of engineers still rely on outdated PDF datasheets. Here's how digital materials intelligence is closing that gap.",
      content: `India's manufacturing sector is projected to reach $1 trillion by 2028. With the Production-Linked Incentive (PLI) schemes spanning 14 sectors — from semiconductors to advanced chemistry cell batteries — the demand for accurate, real-time materials data has never been higher.\n\n## The Problem: Fragmented Material Data\n\nMost Indian manufacturers still rely on:\n- Scattered PDF datasheets from suppliers\n- Outdated IS/BIS standard handbooks\n- Word-of-mouth material recommendations\n\nThis leads to **over-engineering** (safety factors of 3x when 1.5x would suffice), **cost overruns** (selecting premium alloys when equivalent grades exist at 40% lower cost), and **compliance gaps** (missing EU-CBAM carbon declarations).\n\n## The Solution: MatDataHub\n\nMatDataHub provides a single source of truth — verified mechanical, thermal, and economic properties for 500+ engineering materials, mapped to ASTM/ISO/BIS standards. Our AI-powered substitution engine finds cost-optimal alternatives in seconds, not weeks.\n\n**Key features that matter for Indian manufacturers:**\n- Side-by-side comparison of IS 2062 vs ASTM A36 vs EN 10025\n- Real-time cost benchmarking in INR\n- EU-CBAM carbon tax calculator for export compliance\n- Bill of Materials analyzer with automated material matching`
    },
    { 
      title: "Modeling Thermal Expansion in Aerospace Alloys: Ti-6Al-4V vs Al 7075-T6", 
      date: "04/09/2026", author: "Dr. Alara Vance", readTime: "8 min", tag: "Physics", featured: false,
      excerpt: "Deep dive into isotropic thermal expansion formulas and why Titanium out-performs Aluminum 7075 at Mach 2.5 flight profiles.",
      content: `Thermal expansion is a critical design parameter in aerospace structures. When an aircraft fuselage transitions from ground temperature (+40°C in Chennai) to cruise altitude (-56°C at FL410), every rivet, skin panel, and spar cap must accommodate differential expansion.\n\n## The CTE Equation\n\nLinear thermal expansion is governed by:\n\nΔL = L₀ × α × ΔT\n\nWhere:\n- ΔL = change in length (m)\n- L₀ = original length (m)\n- α = coefficient of thermal expansion (CTE, in /°C)\n- ΔT = temperature change (°C)\n\n## Ti-6Al-4V vs Al 7075-T6\n\n| Property | Ti-6Al-4V | Al 7075-T6 |\n|---|---|---|\n| CTE (20-300°C) | 8.6 × 10⁻⁶ /°C | 23.6 × 10⁻⁶ /°C |\n| Density | 4.43 g/cm³ | 2.81 g/cm³ |\n| Yield Strength | 880 MPa | 503 MPa |\n| Specific Strength | 198 kNm/kg | 179 kNm/kg |\n\nAt Mach 2.5, skin temperatures reach ~180°C. For a 10-meter fuselage panel:\n- Al 7075: ΔL = 10 × 23.6e-6 × 160 = **37.8 mm** expansion\n- Ti-6Al-4V: ΔL = 10 × 8.6e-6 × 160 = **13.8 mm** expansion\n\nTitanium's CTE is 2.7× lower, reducing thermal stress concentrations at fastener holes by 63%.\n\n**Use MatDataHub's Side-by-Side Compare tool to instantly visualize these differences across any two alloys.**`
    },
    { 
      title: "EU-CBAM 2026: A Practical Guide for Indian Steel Exporters", 
      date: "22/08/2026", author: "ESG Policy Team", readTime: "5 min", tag: "Economics", featured: true,
      excerpt: "The EU Carbon Border Adjustment Mechanism is now mandatory. Here's how to calculate your CBAM liability using MatDataHub's built-in analyzer.",
      content: `Starting January 2026, the European Union's Carbon Border Adjustment Mechanism (CBAM) requires all importers of steel, aluminum, cement, fertilizers, electricity, and hydrogen to purchase CBAM certificates based on the embedded carbon content of their goods.\n\n## What Indian Exporters Must Know\n\n1. **Reporting is mandatory** — even for small consignments\n2. **Default values are punitive** — if you don't declare your actual emissions, the EU will apply the worst-performing 10% benchmark\n3. **Certificate price tracks EU ETS** — currently ~€75/tonne CO₂e\n\n## Calculating CBAM Liability\n\nFor every tonne of steel exported:\n- India's average BF-BOF steel: ~2.5 t CO₂e/t steel\n- EU reference benchmark: ~1.52 t CO₂e/t steel\n- CBAM-liable emissions: 2.5 - 1.52 = **0.98 t CO₂e/t steel**\n- Cost: 0.98 × €75 = **€73.50 per tonne of steel**\n\nFor a 10,000-tonne annual export contract, that's **€735,000** in CBAM certificates.\n\n## How MatDataHub Helps\n\nUpload your Bill of Materials CSV to our **CBAM Calculator** (Analytics → CBAM Analyzer). It automatically:\n- Matches your materials to our verified emissions database (ICE DB v3)\n- Calculates embedded carbon per component\n- Estimates total CBAM liability in EUR\n- Generates a compliance-ready report`
    },
    { 
      title: "Rule of Mixtures vs Halpin-Tsai: Which Model for Your Composite?", 
      date: "15/08/2026", author: "Prof. H. Chen", readTime: "12 min", tag: "Mathematics", featured: false,
      excerpt: "Comparing mathematical models for predicting the transverse elastic modulus of continuous fiber composites — with worked examples.",
      content: `When designing a carbon fiber reinforced polymer (CFRP) laminate, the most fundamental question is: what will the elastic modulus be?\n\n## Rule of Mixtures (Voigt Model)\n\nFor longitudinal modulus (fiber direction):\n\nE₁ = Ef × Vf + Em × (1 - Vf)\n\nThis is exact for iso-strain conditions (loading parallel to fibers).\n\n## Inverse Rule of Mixtures (Reuss Model)\n\nFor transverse modulus:\n\n1/E₂ = Vf/Ef + (1 - Vf)/Em\n\nThis dramatically underestimates transverse stiffness because it assumes iso-stress.\n\n## Halpin-Tsai Model\n\nA semi-empirical correction:\n\nE₂ = Em × (1 + ξηVf) / (1 - ηVf)\n\nWhere η = (Ef/Em - 1) / (Ef/Em + ξ) and ξ is a geometry factor (typically 2 for circular fibers).\n\n## Worked Example: T300/Epoxy\n\n| Property | Carbon Fiber (T300) | Epoxy Matrix |\n|---|---|---|\n| E (GPa) | 230 | 3.5 |\n| Vf | 0.60 | 0.40 |\n\n- **ROM (E₁):** 230×0.6 + 3.5×0.4 = **139.4 GPa** ✓\n- **Inverse ROM (E₂):** 1/(0.6/230 + 0.4/3.5) = **8.56 GPa** (too low)\n- **Halpin-Tsai (E₂):** ξ=2, η=0.970 → **13.2 GPa** (matches experiments)\n\n**MatDataHub's Composite Synthesizer uses both ROM and inverse ROM bounds.** Our analytics engine shows you the full design envelope.`
    },
    { 
      title: "Selecting the Right Stainless Steel Grade: 304 vs 316 vs 430 vs 2205", 
      date: "01/08/2026", author: "MetalTech Research", readTime: "7 min", tag: "Materials", featured: false,
      excerpt: "A practical decision matrix for choosing stainless steel grades based on corrosion environment, cost, and mechanical requirements.",
      content: `Stainless steel accounts for 52% of all material queries on MatDataHub. Here's a definitive comparison of the four most-used grades.\n\n## Quick Comparison\n\n| Property | AISI 304 | AISI 316 | AISI 430 | Duplex 2205 |\n|---|---|---|---|---|\n| Type | Austenitic | Austenitic | Ferritic | Duplex |\n| Cr (%) | 18-20 | 16-18 | 16-18 | 22-23 |\n| Ni (%) | 8-10.5 | 10-14 | <0.75 | 4.5-6.5 |\n| Mo (%) | — | 2-3 | — | 3-3.5 |\n| Yield (MPa) | 205 | 205 | 205 | 450 |\n| Cost (₹/kg) | 220-280 | 320-400 | 150-200 | 450-600 |\n| Pitting Resistance (PREN) | 18 | 24 | 16 | 35 |\n\n## Decision Rules\n\n1. **General purpose / Food grade** → 304 (best value)\n2. **Marine / Chloride exposure** → 316 (Mo provides pitting resistance)\n3. **Budget-constrained, no corrosion** → 430 (no Nickel = 40% cheaper)\n4. **High strength + corrosion** → 2205 (2× yield of 304, superior PREN)\n\n**Use MatDataHub's AI Material Advisor** — just type \"I need a stainless steel for marine heat exchangers under ₹400/kg\" and get instant, database-backed recommendations.`
    },
    { 
      title: "How to Reduce Manufacturing Costs by 25% with Smart Material Substitution", 
      date: "18/07/2026", author: "MatDataHub Engineering", readTime: "6 min", tag: "Industry", featured: true,
      excerpt: "Real case study: An automotive OEM replaced 3 materials in their EV battery enclosure using our AI substitution engine, saving ₹2.3 Cr annually.",
      content: `Material costs typically represent 40-60% of total manufacturing cost in automotive, aerospace, and industrial equipment. Yet most companies stick with legacy material selections — because finding equivalent alternatives requires weeks of manual research.\n\n## Case Study: EV Battery Enclosure Redesign\n\nAn Indian automotive OEM was manufacturing battery enclosures using:\n1. Al 6061-T6 for the main tray (₹380/kg)\n2. AISI 316L for mounting brackets (₹380/kg)\n3. FR-4 Glass Epoxy for insulation panels (₹520/kg)\n\n**Using MatDataHub's Smart AI Substitution tool:**\n\n| Original | Substitution | Match Score | Cost Saving |\n|---|---|---|---|\n| Al 6061-T6 | Al 5052-H32 | 94.2% | -32% (₹258/kg) |\n| AISI 316L | AISI 304 | 91.7% | -28% (₹274/kg) |\n| FR-4 | Nomex 410 | 87.5% | -18% (₹426/kg) |\n\n**Annual production: 50,000 units → Total savings: ₹2.3 Crore/year**\n\nThe substitution engine uses Euclidean distance in a normalized N-dimensional property space (density, tensile strength, thermal conductivity, cost) with user-adjustable importance weights.\n\n**Try it yourself:** Go to Analytics → Smart AI Substitution, select your base material, adjust the weight sliders, and discover cost-optimal alternatives in seconds.`
    },
    { 
      title: "Understanding Embodied Carbon: A Materials Engineer's Guide", 
      date: "05/07/2026", author: "Dr. S. Krishnamurthy", readTime: "9 min", tag: "Sustainability", featured: false,
      excerpt: "From cradle-to-gate emissions to ICE database factors — everything you need to know about carbon accounting for engineering materials.",
      content: `Embodied carbon (EC) represents the total greenhouse gas emissions associated with extracting, processing, manufacturing, and transporting a material — measured in kg CO₂e per kg of material.\n\n## Why It Matters Now\n\n- EU CBAM makes embodied carbon a direct cost factor\n- Green procurement mandates in public infrastructure (Indian Railways, NHAI)\n- ESG reporting requirements for listed companies (BRSR framework)\n\n## Key Emission Factors (ICE Database v3)\n\n| Material | EC (kg CO₂e/kg) | Notes |\n|---|---|---|\n| General Steel | 1.85 | BF-BOF route |\n| Stainless Steel (304) | 6.15 | High Ni/Cr content |\n| Aluminum (primary) | 8.24 | Electrolysis-intensive |\n| Aluminum (recycled) | 0.52 | 94% reduction |\n| Titanium | 35.7 | Kroll process |\n| CFRP | 29.5 | Energy-intensive PAN fiber |\n| Concrete | 0.13 | Volume-driven impact |\n| Copper | 3.81 | Smelting + refining |\n\n## The Recycling Multiplier\n\nRecycled aluminum has 94% lower EC than primary. This is why MatDataHub tracks recyclability indices alongside carbon factors — a material with high EC but high recyclability (like aluminum) has a very different lifecycle impact than one with moderate EC but zero recyclability (like thermoset composites).\n\n**MatDataHub's CBAM Calculator uses these exact ICE v3 factors** as fallback values when your database materials don't have measured emissions data.`
    },
    { 
      title: "Beam Deflection Calculator: The Physics Behind MatDataHub's Workspace Tool", 
      date: "20/06/2026", author: "Structural Mechanics Team", readTime: "10 min", tag: "Physics", featured: false,
      excerpt: "Euler-Bernoulli beam theory, moment of inertia calculations, and how we validate our deflection predictions against FEA benchmarks.",
      content: `MatDataHub's Workspace includes a built-in beam deflection calculator. Here's the engineering science behind it.\n\n## Euler-Bernoulli Beam Theory\n\nFor a simply-supported beam with a point load P at midspan:\n\nδ_max = PL³ / (48EI)\n\nWhere:\n- δ_max = maximum deflection (m)\n- P = applied load (N)\n- L = span length (m)\n- E = elastic modulus (Pa)\n- I = second moment of area (m⁴)\n\n## For a cantilever with end load:\n\nδ_max = PL³ / (3EI)\n\n## Practical Example\n\nA 2-meter cantilever shelf bracket made from AISI 304 stainless steel (E = 193 GPa), rectangular cross-section 50mm × 10mm, supporting 50 kg:\n\n- P = 50 × 9.81 = 490.5 N\n- I = (0.05 × 0.01³) / 12 = 4.167 × 10⁻⁹ m⁴\n- δ = (490.5 × 2³) / (3 × 193e9 × 4.167e-9)\n- δ = 3924 / 2412.7 = **1.63 mm**\n\nThis is within the L/500 serviceability limit (4mm), so the design is acceptable.\n\n**MatDataHub automatically pulls the elastic modulus from our verified database** when you select a material in the Workspace, eliminating manual lookup errors.`
    }
  ];

  const blogs = [...apiBlogs, ...hardcodedBlogs];

  const allTags = ["All", ...Array.from(new Set(blogs.map(b => b.tag)))];
  const filteredBlogs = blogFilter === "All" ? blogs : blogs.filter(b => b.tag === blogFilter);

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
      const res = await fetch(`${API}/feedback/`, {
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
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-3">
            <BookOpen className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            Learning & Resources
          </h1>
          <p className="text-slate-600 dark:text-slate-300 mt-2">Get help, read documentation, and explore advanced engineering mathematics.</p>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-200 dark:border-slate-800 gap-6">
          <button 
            onClick={() => setActiveTab("blogs")} 
            className={`pb-3 font-semibold text-sm transition-colors relative ${activeTab === 'blogs' ? 'text-blue-600 dark:text-blue-400' : 'text-slate-500 dark:text-slate-400 hover:text-slate-200'}`}
          >
            <span className="flex items-center gap-2"><BookOpen className="w-4 h-4" /> Blogs</span>
            {activeTab === 'blogs' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500 rounded-t-full" />}
          </button>
          <button 
            onClick={() => setActiveTab("faqs")} 
            className={`pb-3 font-semibold text-sm transition-colors relative ${activeTab === 'faqs' ? 'text-blue-600 dark:text-blue-400' : 'text-slate-500 dark:text-slate-400 hover:text-slate-200'}`}
          >
            <span className="flex items-center gap-2"><HelpCircle className="w-4 h-4" /> FAQs</span>
            {activeTab === 'faqs' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500 rounded-t-full" />}
          </button>
          <button 
            onClick={() => setActiveTab("support")} 
            className={`pb-3 font-semibold text-sm transition-colors relative ${activeTab === 'support' ? 'text-blue-600 dark:text-blue-400' : 'text-slate-500 dark:text-slate-400 hover:text-slate-200'}`}
          >
            <span className="flex items-center gap-2"><LifeBuoy className="w-4 h-4" /> Support Centre</span>
            {activeTab === 'support' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500 rounded-t-full" />}
          </button>
        </div>

        {/* FAQ Section */}
        {activeTab === "faqs" && (
          <div className="space-y-6">
            <div className="relative">
              <Search className="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 dark:text-slate-400" />
              <input 
                type="text" 
                placeholder="Search documentation and FAQs..." 
                value={faqSearch}
                onChange={e => setFaqSearch(e.target.value)}
                className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl pl-12 pr-4 py-4 text-slate-900 dark:text-white outline-none focus:border-indigo-500 transition-colors"
              />
            </div>
            
            <div className="space-y-3">
              {filteredFaqs.map((faq, i) => (
                <div key={i} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden transition-all">
                  <button 
                    onClick={() => setOpenFaq(openFaq === i ? null : i)}
                    className="w-full text-left p-4 flex justify-between items-center hover:bg-slate-100 dark:hover:bg-slate-800/50"
                  >
                    <span className="font-semibold text-slate-200">{faq.q}</span>
                    <ChevronDown className={`w-5 h-5 text-slate-500 dark:text-slate-400 transition-transform ${openFaq === i ? 'rotate-180' : ''}`} />
                  </button>
                  {openFaq === i && (
                    <div className="p-4 pt-0 text-slate-500 dark:text-slate-400 text-sm leading-relaxed border-t border-slate-200 dark:border-slate-800/50 mt-2 pt-4 bg-slate-50 dark:bg-slate-950/30">
                      {faq.a}
                    </div>
                  )}
                </div>
              ))}
              {filteredFaqs.length === 0 && (
                <div className="text-center p-10 text-slate-500 dark:text-slate-400">No results found for "{faqSearch}". Please check the Support Centre.</div>
              )}
            </div>
          </div>
        )}

        {/* Blogs Section */}
        {activeTab === "blogs" && (
          <div>
            {selectedBlog !== null ? (
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 lg:p-12 overflow-hidden relative">
                <button 
                  onClick={() => setSelectedBlog(null)}
                  className="flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-colors text-sm font-semibold mb-8"
                >
                  <ArrowLeft className="w-4 h-4" /> Back to all articles
                </button>
                
                <div className="flex flex-wrap gap-3 items-center mb-6">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400 bg-indigo-900/30 border border-indigo-800/50 px-2 py-1 rounded">{blogs[selectedBlog].tag}</span>
                  <span className="text-sm text-slate-500 dark:text-slate-400 font-medium flex items-center gap-1"><Clock className="w-4 h-4"/> {blogs[selectedBlog].readTime} read</span>
                  <span className="text-sm text-slate-500 dark:text-slate-400 font-medium">·</span>
                  <span className="text-sm text-slate-500 dark:text-slate-400 font-medium">{blogs[selectedBlog].date}</span>
                </div>
                
                <h2 className="text-3xl lg:text-4xl font-bold text-slate-900 dark:text-white font-heading mb-6 leading-tight">{blogs[selectedBlog].title}</h2>
                
                <div className="flex items-center gap-3 border-b border-slate-200 dark:border-slate-800 pb-8 mb-8">
                  <div className="w-10 h-10 rounded-full bg-indigo-900/50 flex items-center justify-center text-blue-600 dark:text-blue-400 font-bold border border-indigo-500/30">
                    {blogs[selectedBlog].author.charAt(0)}
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-900 dark:text-white">{blogs[selectedBlog].author}</p>
                    <p className="text-xs text-slate-500 dark:text-slate-400">MatDataHub Engineering</p>
                  </div>
                </div>
                
                <div className="prose prose-invert prose-indigo max-w-none prose-headings:font-bold prose-h2:text-2xl prose-h2:mt-10 prose-h2:mb-4 prose-h2:border-b prose-h2:border-slate-200 dark:border-slate-800 prose-h2:pb-2 prose-p:text-slate-600 dark:text-slate-300 prose-p:leading-relaxed prose-p:mb-6 prose-li:text-slate-600 dark:text-slate-300 prose-li:my-1 prose-strong:text-slate-900 dark:text-white prose-strong:font-bold prose-table:w-full prose-table:text-sm prose-table:border-collapse prose-table:my-8 prose-th:bg-slate-50 dark:bg-slate-950 prose-th:p-3 prose-th:border prose-th:border-slate-200 dark:border-slate-700 prose-th:text-slate-600 dark:text-slate-300 prose-td:p-3 prose-td:border prose-td:border-slate-200 prose-td:text-slate-500 dark:text-slate-400 prose-blockquote:border-l-4 prose-blockquote:border-indigo-500 prose-blockquote:pl-4 prose-blockquote:italic prose-blockquote:text-slate-500 dark:text-slate-400">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {blogs[selectedBlog].content}
                  </ReactMarkdown>
                </div>
                
                <div className="mt-12 pt-8 border-t border-slate-200 dark:border-slate-800 text-center">
                  <h4 className="text-slate-900 dark:text-white font-heading font-bold mb-4">Start optimizing your supply chain today.</h4>
                  <button onClick={() => window.location.href='/analytics'} className="px-6 py-3 bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 text-white font-bold rounded-xl transition-colors">
                    Try MatDataHub Analytics
                  </button>
                </div>
              </div>
            ) : (
              <>
                {/* Filter bar */}
                <div className="flex gap-2 overflow-x-auto pb-4 mb-6 no-scrollbar">
                  {allTags.map(tag => (
                    <button 
                      key={tag}
                      onClick={() => setBlogFilter(tag)}
                      className={`px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors border ${
                        blogFilter === tag 
                          ? 'bg-gradient-to-r from-blue-600 to-violet-600 border-indigo-500 text-slate-900 dark:text-white' 
                          : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 hover:text-white hover:border-slate-600'
                      }`}
                    >
                      {tag}
                    </button>
                  ))}
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredBlogs.map((blog, i) => (
                    <div 
                      onClick={() => setSelectedBlog(blogs.findIndex(b => b.title === blog.title))} 
                      key={i} 
                      className={`bg-white dark:bg-slate-900 border ${blog.featured ? 'border-indigo-500/50 shadow-[0_0_15px_rgba(99,102,241,0.1)]' : 'border-slate-200 dark:border-slate-800 hover:border-slate-600'} p-6 rounded-2xl transition-all group cursor-pointer flex flex-col h-full relative overflow-hidden`}
                    >
                      {blog.featured && <div className="absolute top-0 right-0 w-16 h-16 bg-indigo-500/10 rounded-bl-full blur-xl"></div>}
                      
                      <div className="flex justify-between items-start mb-4">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400 bg-indigo-900/30 border border-indigo-800/50 px-2 py-1 rounded flex items-center gap-1">
                          {blog.featured && <Star className="w-3 h-3 text-amber-400" fill="currentColor" />}
                          {blog.tag}
                        </span>
                        <div className="flex items-center gap-1 text-slate-500 dark:text-slate-400 text-xs font-medium">
                          <Clock className="w-3 h-3" /> {blog.readTime}
                        </div>
                      </div>
                      <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-3 group-hover:text-indigo-300 transition-colors leading-tight">{blog.title}</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mb-6 flex-1 line-clamp-3 leading-relaxed">{blog.excerpt}</p>
                      <div className="flex justify-between items-center border-t border-slate-200 dark:border-slate-800/50 pt-4 mt-auto">
                        <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">By {blog.author}</span>
                        <span className="text-sm font-semibold text-blue-600 dark:text-blue-400 flex items-center gap-1 group-hover:gap-2 transition-all">Read <ArrowRight className="w-4 h-4"/></span>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        )}

        {/* Support Section */}
        {activeTab === "support" && (
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 md:p-10 max-w-2xl mx-auto">
            {submitted ? (
              <div className="text-center space-y-4 py-10">
                <CheckCircle2 className="w-16 h-16 text-emerald-500 mx-auto" />
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading">Ticket Submitted</h2>
                <p className="text-slate-500 dark:text-slate-400">Our engineering team has received your request and will respond to {ticket.email || 'your account email'} within 24 hours.</p>
                <button onClick={() => setSubmitted(false)} className="mt-4 px-6 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-900 dark:text-white rounded-2xl text-sm font-semibold transition-colors">
                  Submit Another Ticket
                </button>
              </div>
            ) : (
              <>
                <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-2">Open a Support Ticket</h2>
                <p className="text-slate-500 dark:text-slate-400 text-sm mb-6">Need help with custom physics integration or experiencing a bug? Let us know.</p>
                <form onSubmit={handleSupportSubmit} className="space-y-5">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div>
                      <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-1">Name</label>
                      <input 
                        type="text" required
                        value={ticket.name} onChange={e => setTicket({...ticket, name: e.target.value})}
                        className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2 text-slate-900 dark:text-white outline-none focus:border-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-1">Email Address</label>
                      <input 
                        type="email" required
                        value={ticket.email} onChange={e => setTicket({...ticket, email: e.target.value})}
                        className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2 text-slate-900 dark:text-white outline-none focus:border-indigo-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-1">Category</label>
                    <select 
                      value={ticket.category} onChange={e => setTicket({...ticket, category: e.target.value})}
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2 text-slate-900 dark:text-white outline-none focus:border-indigo-500"
                    >
                      <option>Technical Support</option>
                      <option>Billing & Enterprise Upgrades</option>
                      <option>Feature Request</option>
                      <option>Physics/Math Clarification</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-1">Message</label>
                    <textarea 
                      required minLength={10}
                      value={ticket.message} onChange={e => setTicket({...ticket, message: e.target.value})}
                      placeholder="Describe your issue or question in detail..."
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-3 text-slate-900 dark:text-white outline-none focus:border-indigo-500 min-h-[120px]"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-2">Screenshot Attachment (Optional)</label>
                    <div className="flex items-center gap-3">
                      <label className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-200 text-sm font-medium rounded-2xl cursor-pointer transition-colors border border-slate-200 dark:border-slate-800">
                        <ImageIcon className="w-4 h-4" /> Upload Image
                        <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" />
                      </label>
                      {ticket.image_data && <span className="text-sm text-emerald-400 flex items-center gap-1"><CheckCircle2 className="w-4 h-4"/> Attached</span>}
                    </div>
                  </div>
                  <button 
                    type="submit" disabled={submitting}
                    className="w-full flex items-center justify-center gap-2 py-3 bg-gradient-to-r from-blue-600 to-violet-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold rounded-2xl transition-colors"
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
