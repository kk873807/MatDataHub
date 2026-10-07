import re

with open('next-frontend/src/app/analytics/cbam/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add states
if 'showConfirmModal' not in content:
    content = re.sub(r'(const \[error, setError\] = useState<string \| null>\(null\);)', r'\1\n  const [showConfirmModal, setShowConfirmModal] = useState(false);\n  const [confirmData, setConfirmData] = useState({ rows: 0, weight: 0 });', content)

# Find onSubmit
old_submit_start = """  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file && !pastedText) return;

    setLoading(true);
    setError(null);
    setResultsData([]);"""

new_submit_start = """  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file && !pastedText) return;

    let textToParse = pastedText;
    if (file) {
      textToParse = await file.text();
    }
    
    Papa.parse(textToParse, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        let totalWeight = 0;
        let weightCol = "";
        if (results.data.length > 0) {
          const keys = Object.keys(results.data[0] as any);
          weightCol = keys.find(k => k.toLowerCase().includes('weight') || k.toLowerCase().includes('qty') || k.toLowerCase().includes('quantity') || k.toLowerCase().includes('mass')) || "";
        }
        if (weightCol) {
          totalWeight = results.data.reduce((acc, row: any) => {
             const val = row[weightCol];
             if (!val) return acc;
             let cleanVal = String(val).replace(/ /g, '');
             if (cleanVal.match(/^\\d{1,3}(?:\\.\\d{3})*,\\d+$/)) {
                cleanVal = cleanVal.replace(/\\./g, '').replace(',', '.');
             } else if (cleanVal.match(/^\\d+,\\d+$/)) {
                cleanVal = cleanVal.replace(',', '.');
             } else if (cleanVal.match(/^\\d{1,3}(?:\\.\\d{3})+$/)) {
                cleanVal = cleanVal.replace(/\\./g, '');
             } else {
                cleanVal = cleanVal.replace(/,/g, '');
             }
             return acc + (parseFloat(cleanVal) || 0);
          }, 0);
        }
        setConfirmData({ rows: results.data.length, weight: totalWeight / 1000 });
        setShowConfirmModal(true);
      }
    });
  };

  const handleConfirmedSubmit = async () => {
    setShowConfirmModal(false);
    setLoading(true);
    setError(null);
    setResultsData([]);"""

content = content.replace(old_submit_start, new_submit_start)

# Add Modal JSX before the <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
modal_jsx = """      {showConfirmModal && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl max-w-sm w-full p-6 text-center">
            <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">Confirm Upload</h3>
            <p className="text-slate-600 dark:text-slate-400 mb-6">
              Parsed <strong className="text-slate-900 dark:text-white">{confirmData.rows} rows</strong>, <strong className="text-slate-900 dark:text-white">{confirmData.weight.toLocaleString(undefined, {maximumFractionDigits: 1})} t total</strong>. Please confirm to calculate.
            </p>
            <div className="flex gap-4">
              <button onClick={() => setShowConfirmModal(false)} className="flex-1 py-2 rounded-xl font-bold border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">Cancel</button>
              <button onClick={handleConfirmedSubmit} className="flex-1 py-2 rounded-xl font-bold bg-emerald-500 hover:bg-emerald-400 text-white transition-colors">Confirm & Calculate</button>
            </div>
          </div>
        </div>
      )}"""

# Insert modal
if modal_jsx not in content:
    content = content.replace('<div className="grid grid-cols-1 xl:grid-cols-3 gap-8">', modal_jsx + '\n\n        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">')

with open('next-frontend/src/app/analytics/cbam/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated UI")
