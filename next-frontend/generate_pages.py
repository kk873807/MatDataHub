import os

blog_code = '''import { Calendar, ArrowRight, User } from "lucide-react";
import Link from "next/link";

const POSTS = [
  {
    title: "The Future of Sustainable Materials in Manufacturing",
    excerpt: "Discover how AI is accelerating the discovery of eco-friendly polymers and reducing industrial carbon footprints globally.",
    date: "Oct 15, 2026",
    author: "Dr. Sarah Chen",
    category: "Sustainability",
    image: "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&q=80&w=800",
  },
  {
    title: "Understanding High-Entropy Alloys",
    excerpt: "A deep dive into the properties, applications, and predictive modeling of next-generation metal structures.",
    date: "Oct 02, 2026",
    author: "James Wilson",
    category: "Materials Science",
    image: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=800",
  },
  {
    title: "MatDataHub 2.0: What's New",
    excerpt: "We're thrilled to announce our latest features, including the new AI Synthesizer and CBAM impact calculators.",
    date: "Sep 28, 2026",
    author: "Product Team",
    category: "Announcements",
    image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=800",
  }
];

export default function BlogPage() {
  return (
    <main className="min-h-screen bg-white dark:bg-slate-950 pt-10 pb-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white font-heading mb-6">Our Blog</h1>
          <p className="text-lg text-slate-600 dark:text-slate-400">
            Insights, updates, and deep dives into materials science, AI engineering, and the future of manufacturing.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {POSTS.map((post, i) => (
            <div key={i} className="group flex flex-col bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl overflow-hidden hover:shadow-xl hover:shadow-blue-900/5 transition-all">
              <div className="relative h-48 overflow-hidden">
                <img src={post.image} alt={post.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                <div className="absolute top-4 left-4">
                  <span className="px-3 py-1 bg-white/90 dark:bg-slate-900/90 backdrop-blur-sm text-blue-600 dark:text-blue-400 text-xs font-bold rounded-full">
                    {post.category}
                  </span>
                </div>
              </div>
              <div className="p-6 flex flex-col flex-1">
                <div className="flex items-center gap-4 text-xs text-slate-500 dark:text-slate-400 mb-4">
                  <span className="flex items-center gap-1.5"><Calendar className="w-4 h-4" /> {post.date}</span>
                  <span className="flex items-center gap-1.5"><User className="w-4 h-4" /> {post.author}</span>
                </div>
                <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-3 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  {post.title}
                </h2>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-6 flex-1 line-clamp-3">
                  {post.excerpt}
                </p>
                <Link href="#" className="inline-flex items-center gap-2 text-sm font-bold text-blue-600 dark:text-blue-400 group-hover:gap-3 transition-all">
                  Read Article <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
'''

faq_code = '''"use client";
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
                    const id = q--;
                    const isOpen = openQ === id;
                    return (
                      <div key={j} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden transition-all">
                        <button 
                          onClick={() => setOpenQ(isOpen ? null : id)}
                          className="w-full flex items-center justify-between p-5 text-left focus:outline-none"
                        >
                          <span className="font-semibold text-slate-900 dark:text-white">{q.q}</span>
                          <ChevronDown className={w-5 h-5 text-slate-400 transition-transform } />
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
'''

contact_code = '''import { Mail, MapPin, Phone, MessageSquare, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function ContactPage() {
  return (
    <main className="min-h-screen bg-slate-50 dark:bg-slate-950 pt-10 pb-24">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white font-heading mb-6">Get in touch</h1>
          <p className="text-lg text-slate-600 dark:text-slate-400">
            Whether you have a technical question, need custom enterprise integration, or just want to say hi, our team is here for you.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8 mb-16">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-3xl hover:shadow-xl hover:shadow-blue-900/5 transition-all text-center flex flex-col items-center">
            <div className="w-14 h-14 bg-blue-100 dark:bg-blue-900/30 rounded-2xl flex items-center justify-center mb-6">
              <Mail className="w-7 h-7 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-2">Email Support</h3>
            <p className="text-slate-500 dark:text-slate-400 text-sm mb-6 flex-1">Drop us an email and we'll get back to you within 24 hours.</p>
            <a href="mailto:support@matdatahub.com" className="font-bold text-blue-600 dark:text-blue-400 hover:underline">support@matdatahub.com</a>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-3xl hover:shadow-xl hover:shadow-blue-900/5 transition-all text-center flex flex-col items-center">
            <div className="w-14 h-14 bg-emerald-100 dark:bg-emerald-900/30 rounded-2xl flex items-center justify-center mb-6">
              <MessageSquare className="w-7 h-7 text-emerald-600 dark:text-emerald-400" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-2">Community Feedback</h3>
            <p className="text-slate-500 dark:text-slate-400 text-sm mb-6 flex-1">Have a feature request or found a bug? Post it on our feedback board.</p>
            <Link href="/feedback" className="font-bold text-emerald-600 dark:text-emerald-400 hover:underline inline-flex items-center gap-1">Go to Feedback <ArrowRight className="w-4 h-4"/></Link>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-3xl hover:shadow-xl hover:shadow-blue-900/5 transition-all text-center flex flex-col items-center">
            <div className="w-14 h-14 bg-violet-100 dark:bg-violet-900/30 rounded-2xl flex items-center justify-center mb-6">
              <MapPin className="w-7 h-7 text-violet-600 dark:text-violet-400" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-2">Office</h3>
            <p className="text-slate-500 dark:text-slate-400 text-sm mb-6 flex-1">MatDataHub HQ<br/>Innovation Park, Phase 1</p>
            <span className="font-bold text-violet-600 dark:text-violet-400">View on Map</span>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 md:p-12 max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-8">Send us a message</h2>
          <form className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">First Name</label>
                <input type="text" className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors" placeholder="Jane" />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Last Name</label>
                <input type="text" className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors" placeholder="Doe" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Email Address</label>
              <input type="email" className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors" placeholder="jane@example.com" />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Message</label>
              <textarea className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors min-h-[150px]" placeholder="How can we help you?"></textarea>
            </div>
            <button type="button" className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-xl transition-all hover:scale-105 shadow-lg shadow-blue-500/30">
              Send Message
            </button>
          </form>
        </div>

      </div>
    </main>
  );
}
'''

with open('src/app/blog/page.tsx', 'w', encoding='utf-8') as f:
    f.write(blog_code)

with open('src/app/faq/page.tsx', 'w', encoding='utf-8') as f:
    f.write(faq_code)

with open('src/app/contact/page.tsx', 'w', encoding='utf-8') as f:
    f.write(contact_code)

print("Created Blog, FAQ, and Contact pages")
