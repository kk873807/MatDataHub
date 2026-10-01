import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\account\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add transactions state and fetch
old_state = 'const [activeTab, setActiveTab] = useState("account");'
new_state = '''const [activeTab, setActiveTab] = useState("account");
  const [transactions, setTransactions] = useState<any[]>([]);

  useEffect(() => {
    if (activeTab === 'billing') {
      const token = localStorage.getItem("token");
      if (token) {
        fetch(`${API}/account/transactions`, {
          headers: { "Authorization": `Bearer ${token}` }
        })
          .then(res => res.ok ? res.json() : [])
          .then(data => setTransactions(data))
          .catch(() => setTransactions([]));
      }
    }
  }, [activeTab]);'''

if old_state in content and 'const [transactions, setTransactions]' not in content:
    content = content.replace(old_state, new_state)

# 2. Replace the hardcoded tbody in the account page billing tab
old_tbody = '''                  <tbody>
                    <tr>
                      <td colSpan={4} className="px-6 py-12 text-center text-slate-500 dark:text-slate-400">
                        <div className="flex flex-col items-center gap-3">
                          <div className="w-12 h-12 bg-slate-100 dark:bg-slate-800 rounded-full flex items-center justify-center">
                            <FileText className="w-6 h-6 text-slate-600 dark:text-slate-300" />
                          </div>
                          <p className="font-medium">No transactions yet</p>
                          <p className="text-sm text-slate-600 dark:text-slate-300 max-w-sm">Your payment history will appear here after your first purchase or subscription upgrade.</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>'''

new_tbody = '''                  <tbody>
                    {transactions.length === 0 && (
                      <tr>
                        <td colSpan={4} className="px-6 py-12 text-center text-slate-500 dark:text-slate-400">
                          <div className="flex flex-col items-center gap-3">
                            <div className="w-12 h-12 bg-slate-100 dark:bg-slate-800 rounded-full flex items-center justify-center">
                              <FileText className="w-6 h-6 text-slate-600 dark:text-slate-300" />
                            </div>
                            <p className="font-medium">No transactions yet</p>
                            <p className="text-sm text-slate-600 dark:text-slate-300 max-w-sm">Your payment history will appear here after your first purchase or subscription upgrade.</p>
                          </div>
                        </td>
                      </tr>
                    )}
                    {transactions.map((txn: any) => (
                      <tr key={txn.id} className="border-t border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900/50 transition-colors">
                        <td className="px-6 py-4 text-slate-700 dark:text-slate-300 whitespace-nowrap">{new Date(txn.created_at).toLocaleDateString()}</td>
                        <td className="px-6 py-4 text-slate-700 dark:text-slate-300 capitalize">Upgrade to {txn.tier_purchased}</td>
                        <td className="px-6 py-4 font-semibold text-slate-900 dark:text-white">&#8377;{txn.amount?.toLocaleString()}</td>
                        <td className="px-6 py-4 text-right">
                          <span className={`text-xs font-bold uppercase px-2 py-1 rounded-full ${txn.status === 'completed' ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400' : 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'}`}>{txn.status}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>'''

if old_tbody in content:
    content = content.replace(old_tbody, new_tbody)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated account page billing tab with live transactions")
