import { Calendar, ArrowRight, User } from "lucide-react";
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
