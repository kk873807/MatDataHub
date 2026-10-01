import os

file_path = 'next-frontend/src/components/InteractiveFeatures.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Bot, GitCompare, Lock, Key', 'Bot, GitCompare, Lock, Key, Leaf')

new_feature = """  {
    id: "cbam",
    title: "CBAM Estimator",
    description: "Instantly estimate EU carbon tax liability for material exports before you ship.",
    icon: Leaf,
    color: "bg-emerald-500",
  },
"""
content = content.replace('const features = [', 'const features = [\n' + new_feature)

cbam_content = """          {activeTab === "cbam" && (
            <div className="space-y-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <div className="text-emerald-500 font-bold mb-1 uppercase text-xs tracking-wider">Lead Magnet Tool</div>
                  <h3 className="text-2xl font-black text-slate-900 dark:text-white font-heading">EU CBAM Carbon Tax Estimator</h3>
                </div>
                <div className="p-3 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 rounded-xl"><Leaf className="w-6 h-6" /></div>
              </div>
              
              <div className="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-5 mb-4 relative overflow-hidden">
                <div className="flex justify-between text-sm mb-4">
                  <span className="text-slate-500">Material Input:</span>
                  <span className="font-bold text-slate-800 dark:text-slate-200">1,000 kg (AISI 304 Steel)</span>
                </div>
                <div className="flex justify-between text-sm mb-4">
                  <span className="text-slate-500">Embodied Carbon Factor:</span>
                  <span className="font-bold text-slate-800 dark:text-slate-200">4.80 kg CO2 / kg</span>
                </div>
                <div className="w-full h-px bg-slate-200 dark:bg-slate-700 my-4"></div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-500 font-bold">Estimated EU Tax Liability:</span>
                  <span className="text-2xl font-black text-red-500">€312.00</span>
                </div>
              </div>
              
              <p className="text-slate-600 dark:text-slate-400 text-sm leading-relaxed mb-6">
                The EU Carbon Border Adjustment Mechanism (CBAM) requires strict emissions reporting for imports. Our full calculator lets you export compliance-ready reports for all your custom materials.
              </p>
              
              <div className="flex gap-4">
                <button className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-3 rounded-xl font-bold transition-all shadow-lg shadow-emerald-900/20 text-sm">
                  Run Full Audit
                </button>
              </div>
            </div>
          )}
"""
content = content.replace('{activeTab === "compare" && (', cbam_content + '\n          {activeTab === "compare" && (')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
