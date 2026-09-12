import { Mail, MapPin, Phone, MessageSquare, ArrowRight } from "lucide-react";
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

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto mb-16">
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
