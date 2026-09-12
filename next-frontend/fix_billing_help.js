const fs = require('fs');

let content = fs.readFileSync('src/components/AccountModals.tsx', 'utf8');

// 1. Fix Billing Date and Manage Plan button
const oldBillingHeader = `<div className="flex items-center justify-between text-sm font-medium text-slate-300 border-t border-slate-700 pt-4">
                  <span>Next billing date: 15 Oct, 2026</span>
                  <button className="px-4 py-1.5 bg-white text-slate-900 rounded-lg hover:bg-slate-200 transition-colors font-bold">Manage Plan</button>
                </div>`;
const newBillingHeader = `<div className="flex items-center justify-between text-sm font-medium text-slate-300 border-t border-slate-700 pt-4">
                  <span>Next billing date: {profile.tier === 'free' ? 'N/A (Free Plan)' : (profile.next_billing_date ? new Date(profile.next_billing_date).toLocaleDateString() : 'Active Subscription')}</span>
                  {profile.tier !== 'free' && (
                    <button onClick={() => alert("Billing portal integration coming soon.")} className="px-4 py-1.5 bg-white text-slate-900 rounded-lg hover:bg-slate-200 transition-colors font-bold">Manage Plan</button>
                  )}
                  {profile.tier === 'free' && (
                    <button onClick={() => setActiveModal('account')} className="px-4 py-1.5 bg-white text-slate-900 rounded-lg hover:bg-slate-200 transition-colors font-bold">Upgrade Now</button>
                  )}
                </div>`;
content = content.replace(oldBillingHeader, newBillingHeader);

// 2. Fix Fake Transactions
const oldTransactions = `<h5 className="text-lg font-bold text-slate-900 dark:text-white mb-4">Recent Transactions</h5>
                <div className="space-y-3">
                  {[1, 2].map((i) => (
                    <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800">
                      <div className="flex items-center gap-4">
                        <div className="p-3 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 rounded-lg"><FileText className="w-5 h-5"/></div>
                        <div>
                          <p className="text-sm font-bold text-slate-900 dark:text-white">Invoice #MDH-{(1042-i)}</p>
                          <p className="text-xs text-slate-500">Sep {15-i}, 2026</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-6">
                        <span className="text-base font-bold text-slate-900 dark:text-white">$49.00</span>
                        <button className="text-slate-400 hover:text-blue-600 p-2"><Download className="w-4 h-4"/></button>
                      </div>
                    </div>
                  ))}
                </div>`;
const newTransactions = `<h5 className="text-lg font-bold text-slate-900 dark:text-white mb-4">Recent Transactions</h5>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead className="bg-slate-50 dark:bg-slate-950/80 text-slate-500 dark:text-slate-400 text-xs uppercase tracking-wider">
                      <tr>
                        <th className="px-6 py-4 font-semibold rounded-tl-xl">Date</th>
                        <th className="px-6 py-4 font-semibold">Description</th>
                        <th className="px-6 py-4 font-semibold">Amount</th>
                        <th className="px-6 py-4 font-semibold text-right rounded-tr-xl">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td colSpan={4} className="px-6 py-12 text-center text-slate-500 dark:text-slate-400 border-t border-slate-100 dark:border-slate-800">
                          <div className="flex flex-col items-center gap-3">
                            <div className="w-12 h-12 bg-slate-100 dark:bg-slate-800 rounded-full flex items-center justify-center">
                              <FileText className="w-6 h-6 text-slate-600 dark:text-slate-300" />
                            </div>
                            <p className="font-medium text-slate-900 dark:text-white">No transactions yet</p>
                            <p className="text-sm text-slate-500 max-w-sm mx-auto">Your payment history will appear here after your first purchase or subscription upgrade.</p>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>`;
content = content.replace(oldTransactions, newTransactions);

// 3. Fix Help Centre & Legal
const oldHelp = `<div className="p-8 rounded-2xl border border-amber-200 dark:border-amber-900/30 bg-amber-50 dark:bg-amber-900/10 text-center shadow-sm">
                <LifeBuoy className="w-12 h-12 text-amber-500 mx-auto mb-4"/>
                <h4 className="text-xl font-bold text-slate-900 dark:text-white mb-2">How can we help?</h4>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-6 max-w-sm mx-auto">Our engineering support team is available 24/7 to assist with your technical inquiries.</p>
                <button className="px-6 py-2.5 bg-amber-500 hover:bg-amber-600 text-white rounded-xl text-sm font-bold transition-colors shadow-lg shadow-amber-500/20">
                  Contact Support
                </button>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <a href="#" className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-center transition-colors shadow-sm">
                  <p className="text-base font-bold text-slate-900 dark:text-white mb-1">Documentation</p>
                  <p className="text-xs text-slate-500">API & Integration Guides</p>
                </a>
                <a href="#" className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-center transition-colors shadow-sm">
                  <p className="text-base font-bold text-slate-900 dark:text-white mb-1">Legal & Privacy</p>
                  <p className="text-xs text-slate-500">Terms of Service</p>
                </a>
              </div>`;

const newHelp = `<div className="p-8 rounded-2xl border border-amber-200 dark:border-amber-900/30 bg-amber-50 dark:bg-amber-900/10 text-center shadow-sm">
                <LifeBuoy className="w-12 h-12 text-amber-500 mx-auto mb-4"/>
                <h4 className="text-xl font-bold text-slate-900 dark:text-white mb-2">How can we help?</h4>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-6 max-w-sm mx-auto">Our engineering support team is available 24/7 to assist with your technical inquiries.</p>
                <a href="mailto:support@matdatahub.com" className="inline-block px-6 py-2.5 bg-amber-500 hover:bg-amber-600 text-white rounded-xl text-sm font-bold transition-colors shadow-lg shadow-amber-500/20">
                  Contact Support
                </a>
              </div>

              <div className="space-y-4">
                <details className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 cursor-pointer group shadow-sm">
                  <summary className="font-bold text-slate-900 dark:text-white group-hover:text-blue-600 dark:text-blue-400 transition-colors outline-none list-none flex justify-between items-center">
                    Privacy Policy
                    <span className="text-slate-400 group-hover:text-blue-500 text-sm opacity-50">+</span>
                  </summary>
                  <div className="mt-4 text-slate-500 dark:text-slate-400 text-sm space-y-2 pt-4 border-t border-slate-100 dark:border-slate-800">
                    <p>We respect your privacy and are committed to protecting your personal data.</p>
                    <p>Your passwords and secrets are encrypted. We do not sell your data to third parties.</p>
                  </div>
                </details>
                
                <details className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 cursor-pointer group shadow-sm">
                  <summary className="font-bold text-slate-900 dark:text-white group-hover:text-blue-600 dark:text-blue-400 transition-colors outline-none list-none flex justify-between items-center">
                    Terms of Service
                    <span className="text-slate-400 group-hover:text-blue-500 text-sm opacity-50">+</span>
                  </summary>
                  <div className="mt-4 text-slate-500 dark:text-slate-400 text-sm space-y-2 pt-4 border-t border-slate-100 dark:border-slate-800">
                    <p>By using MatDataHub, you agree to not abuse our APIs or scrape our database.</p>
                    <p>Be polite in community feedback. Violations will result in a permanent ban.</p>
                  </div>
                </details>
              </div>`;
content = content.replace(oldHelp, newHelp);

fs.writeFileSync('src/components/AccountModals.tsx', content);
console.log('Fixed billing and help sections');
