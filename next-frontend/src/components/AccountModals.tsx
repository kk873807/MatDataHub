import React from 'react';
import { Settings, CreditCard, LifeBuoy, X, Download, Shield, Key, FileText, Zap } from 'lucide-react';

type AccountModalsProps = {
  activeModal: string | null;
  setActiveModal: (modal: string | null) => void;
  userInfo?: { name: string; tier: string; is_admin: boolean } | null;
};

export function AccountModals({ activeModal, setActiveModal, userInfo }: AccountModalsProps) {
  if (!activeModal) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm p-4" onClick={() => setActiveModal(null)}>
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl w-full max-w-lg p-0 overflow-hidden animate-in zoom-in-95" onClick={e => e.stopPropagation()}>
        
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50">
          <h3 className="font-bold text-slate-900 dark:text-white flex items-center gap-2">
            {activeModal === 'account' && <><Settings className="w-5 h-5 text-blue-600"/> Account Management</>}
            {activeModal === 'billing' && <><CreditCard className="w-5 h-5 text-emerald-600"/> Transactions & Billing</>}
            {activeModal === 'help' && <><LifeBuoy className="w-5 h-5 text-amber-600"/> Help Centre & Legal</>}
          </h3>
          <button onClick={() => setActiveModal(null)} className="p-1 text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-lg transition-colors">
            <X className="w-5 h-5"/>
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {activeModal === 'account' && (
            <div className="space-y-6">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center text-white font-bold text-2xl shadow-lg shadow-blue-500/30">
                  {userInfo?.name?.charAt(0).toUpperCase() || "U"}
                </div>
                <div>
                  <h4 className="text-xl font-bold text-slate-900 dark:text-white">{userInfo?.name || "User"}</h4>
                  <p className="text-sm text-slate-500 dark:text-slate-400 font-medium">Personal Account</p>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <button className="flex items-center gap-3 p-4 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 text-left transition-all group">
                  <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg group-hover:scale-110 transition-transform"><Key className="w-5 h-5 text-blue-600 dark:text-blue-400"/></div>
                  <div>
                    <p className="text-sm font-bold text-slate-900 dark:text-white">Security</p>
                    <p className="text-[10px] text-slate-500">Change password & 2FA</p>
                  </div>
                </button>
                <button className="flex items-center gap-3 p-4 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-violet-500 hover:bg-violet-50 dark:hover:bg-violet-900/20 text-left transition-all group">
                  <div className="p-2 bg-violet-100 dark:bg-violet-900/30 rounded-lg group-hover:scale-110 transition-transform"><Shield className="w-5 h-5 text-violet-600 dark:text-violet-400"/></div>
                  <div>
                    <p className="text-sm font-bold text-slate-900 dark:text-white">API Keys</p>
                    <p className="text-[10px] text-slate-500">Manage integrations</p>
                  </div>
                </button>
              </div>
            </div>
          )}

          {activeModal === 'billing' && (
            <div className="space-y-6">
              <div className="p-5 rounded-xl bg-gradient-to-br from-slate-900 to-slate-800 text-white shadow-xl relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-10"><Zap className="w-24 h-24"/></div>
                <p className="text-sm text-slate-300 font-medium uppercase tracking-wider mb-1">Current Plan</p>
                <div className="flex items-end gap-3 mb-4">
                  <h4 className="text-3xl font-black capitalize tracking-tight">{userInfo?.tier || "Free"}</h4>
                  <span className="text-sm text-emerald-400 font-bold mb-1 px-2 py-0.5 bg-emerald-400/10 rounded-full">Active</span>
                </div>
                <div className="flex items-center justify-between text-xs font-medium text-slate-300 border-t border-slate-700 pt-4">
                  <span>Next billing date: 15 Oct, 2026</span>
                  <button className="px-3 py-1 bg-white text-slate-900 rounded-lg hover:bg-slate-200 transition-colors">Manage Plan</button>
                </div>
              </div>

              <div>
                <h5 className="text-sm font-bold text-slate-900 dark:text-white mb-3">Recent Transactions</h5>
                <div className="space-y-2">
                  {[1, 2].map((i) => (
                    <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 rounded-md"><FileText className="w-4 h-4"/></div>
                        <div>
                          <p className="text-xs font-bold text-slate-900 dark:text-white">Invoice #MDH-{(1042-i)}</p>
                          <p className="text-[10px] text-slate-500">Sep {15-i}, 2026</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <span className="text-sm font-bold text-slate-900 dark:text-white">$49.00</span>
                        <button className="text-slate-400 hover:text-blue-600"><Download className="w-4 h-4"/></button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeModal === 'help' && (
            <div className="space-y-4">
              <div className="p-5 rounded-xl border border-amber-200 dark:border-amber-900/30 bg-amber-50 dark:bg-amber-900/10 text-center">
                <LifeBuoy className="w-10 h-10 text-amber-500 mx-auto mb-3"/>
                <h4 className="text-lg font-bold text-slate-900 dark:text-white mb-1">How can we help?</h4>
                <p className="text-xs text-slate-600 dark:text-slate-400 mb-4 max-w-xs mx-auto">Our engineering support team is available 24/7 to assist with your technical inquiries.</p>
                <button className="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-sm font-bold transition-colors shadow-lg shadow-amber-500/20">
                  Contact Support
                </button>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <a href="#" className="p-3 rounded-lg border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800 text-center transition-colors">
                  <p className="text-sm font-bold text-slate-900 dark:text-white">Documentation</p>
                  <p className="text-[10px] text-slate-500 mt-1">API & Integration Guides</p>
                </a>
                <a href="#" className="p-3 rounded-lg border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800 text-center transition-colors">
                  <p className="text-sm font-bold text-slate-900 dark:text-white">Legal & Privacy</p>
                  <p className="text-[10px] text-slate-500 mt-1">Terms of Service</p>
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
