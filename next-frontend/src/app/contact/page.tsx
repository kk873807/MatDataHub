"use client";
import { Mail, MapPin, Phone, MessageSquare, ArrowRight, CheckCircle2, ImageIcon, Send, Loader2 } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

export default function ContactPage() {
  const [ticket, setTicket] = useState({ name: "", email: "", category: "Technical Support", message: "", image_data: "" });
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleImageUpload = (e: any) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setTicket({ ...ticket, image_data: reader.result as string });
      reader.readAsDataURL(file);
    }
  };

  const handleSupportSubmit = (e: any) => {
    e.preventDefault();
    setSubmitting(true);
    setTimeout(() => {
      setSubmitting(false);
      setSubmitted(true);
    }, 1500);
  };

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
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 md:p-12 max-w-4xl mx-auto">
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
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-8">Open a Support Ticket</h2>
              <form onSubmit={handleSupportSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Name</label>
                    <input 
                      type="text" required
                      value={ticket.name} onChange={e => setTicket({...ticket, name: e.target.value})}
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors text-slate-900 dark:text-white" placeholder="Jane Doe" 
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Email Address</label>
                    <input 
                      type="email" required
                      value={ticket.email} onChange={e => setTicket({...ticket, email: e.target.value})}
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors text-slate-900 dark:text-white" placeholder="jane@example.com" 
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Category</label>
                  <select 
                    value={ticket.category} onChange={e => setTicket({...ticket, category: e.target.value})}
                    className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors text-slate-900 dark:text-white"
                  >
                    <option>Technical Support</option>
                    <option>Billing & Enterprise Upgrades</option>
                    <option>Feature Request</option>
                    <option>Physics/Math Clarification</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Message</label>
                  <textarea 
                    required minLength={10}
                    value={ticket.message} onChange={e => setTicket({...ticket, message: e.target.value})}
                    className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors min-h-[150px] text-slate-900 dark:text-white" placeholder="Describe your issue or question in detail..."
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Screenshot Attachment (Optional)</label>
                  <div className="flex items-center gap-3">
                    <label className="flex items-center gap-2 px-4 py-3 bg-slate-100 dark:bg-slate-900 hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 text-sm font-medium rounded-xl cursor-pointer transition-colors border border-slate-200 dark:border-slate-800">
                      <ImageIcon className="w-5 h-5" /> Upload Image
                      <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" />
                    </label>
                    {ticket.image_data && <span className="text-sm text-emerald-600 dark:text-emerald-400 flex items-center gap-1"><CheckCircle2 className="w-4 h-4"/> Attached</span>}
                  </div>
                </div>
                <button 
                  type="submit" disabled={submitting}
                  className="w-full flex items-center justify-center gap-2 py-3 bg-gradient-to-r from-blue-600 to-violet-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold rounded-xl transition-all hover:scale-[1.02] shadow-lg shadow-blue-500/30"
                >
                  {submitting ? <Loader2 className="w-5 h-5 animate-spin" /> : <><Send className="w-4 h-4"/> Submit Ticket</>}
                </button>
              </form>
            </>
          )}
        </div>

      </div>
    </main>
  );
}
