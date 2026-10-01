import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_ui = '''            {/* User Contributions */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl">'''

new_ui = '''            {/* Billing & Transactions */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl">
              <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50 dark:bg-slate-950/50">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-600 dark:text-emerald-400"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading">Financial Ledger</h2>
                    <p className="text-sm text-slate-500 dark:text-slate-400">All Razorpay transactions & upgrades</p>
                  </div>
                </div>
                <span className="bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 py-1 px-3 rounded-full text-sm font-bold">
                  {transactions.length} Records
                </span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 dark:bg-slate-950/80 text-slate-500 dark:text-slate-400 text-xs uppercase tracking-wider">
                    <tr>
                      <th className="px-6 py-4 font-semibold">Date</th>
                      <th className="px-6 py-4 font-semibold">User Email</th>
                      <th className="px-6 py-4 font-semibold">Tier</th>
                      <th className="px-6 py-4 font-semibold">Amount</th>
                      <th className="px-6 py-4 font-semibold">Razorpay ID</th>
                      <th className="px-6 py-4 font-semibold text-right">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {transactions.length === 0 ? (
                      <tr>
                        <td colSpan={6} className="px-6 py-8 text-center text-slate-500">No transactions recorded yet.</td>
                      </tr>
                    ) : (
                      transactions.map(txn => (
                        <tr key={txn.id} className="border-t border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900/50">
                          <td className="px-6 py-4 whitespace-nowrap">{new Date(txn.created_at).toLocaleString()}</td>
                          <td className="px-6 py-4 font-medium">{txn.user_email}</td>
                          <td className="px-6 py-4 capitalize">{txn.tier_purchased}</td>
                          <td className="px-6 py-4 font-bold text-slate-900 dark:text-white">&#8377;{txn.amount.toLocaleString()}</td>
                          <td className="px-6 py-4 text-xs font-mono text-slate-500">{txn.payment_id || "N/A"}</td>
                          <td className="px-6 py-4 text-right">
                            <span className={`text-xs font-bold uppercase px-2 py-1 rounded-full ${txn.status === 'completed' ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30' : 'bg-red-100 text-red-600 dark:bg-red-900/30'}`}>
                              {txn.status}
                            </span>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* User Contributions */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl">'''

if old_ui in content:
    content = content.replace(old_ui, new_ui)
    print("Injected Transactions UI block")
else:
    print("Failed to find old UI")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
