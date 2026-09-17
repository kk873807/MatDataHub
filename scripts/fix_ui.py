
import sys
content = open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\materials\[id]\page.tsx', 'r', encoding='utf-8').read()

old_block = '''            {/* Metadata */}
            <div className=\"p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-sm\">
              <h3 className=\"font-bold text-slate-900 dark:text-white font-heading mb-4 border-b border-slate-200 dark:border-slate-800 pb-2\">
                Standards & Identifiers
              </h3>
              <div className=\"space-y-3\">
                <div>
                  <span className=\"text-slate-600 dark:text-slate-300 block text-xs\">Standard</span>
                  <span className=\"text-slate-900 dark:text-white\">{material.standard || \"-\"}</span>
                </div>
                <div>
                  <span className=\"text-slate-600 dark:text-slate-300 block text-xs\">Grade</span>
                  <span className=\"text-slate-900 dark:text-white\">{material.grade || \"-\"}</span>
                </div>
                <div>
                  <span className=\"text-slate-600 dark:text-slate-300 block text-xs\">
                    Equivalent Grades
                  </span>
                  <span className=\"text-slate-900 dark:text-white\">
                    {material.equivalent_grades || \"-\"}
                  </span>
                </div>
                <div className=\"pt-2 border-t border-slate-200 dark:border-slate-800 relative group cursor-pointer\">
                    <span className=\"text-slate-600 dark:text-slate-300 block text-xs flex items-center gap-1\">
                      Data Source <Info className=\"w-3 h-3 text-slate-400\" />
                    </span>
                    <span className=\"text-emerald-600 dark:text-emerald-400 font-medium border-b border-dashed border-emerald-400/50\">
                      {material.data_source || \"Verified Internal Database\"}
                    </span>
                    <div className=\"absolute bottom-full left-0 mb-2 w-72 bg-slate-900 dark:bg-slate-800 text-white text-xs rounded-xl p-3 shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50\">
                      All material properties, supply chain math, economics, and ESG/CBAM emission factors are rigorously sourced from verified industry standards (ASTM, ISO, DIN), reputable global commodities indices, and validated scientific databases (e.g., ICE DB University of Bath).
                      <div className=\"absolute top-full left-4 -mt-1 border-4 border-transparent border-t-slate-900 dark:border-t-slate-800\"></div>
                    </div>
                  </div>
              </div>
            </div>'''.replace('\', '')

new_block = '''            {/* Metadata */}
            <div className=\"p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-sm\">
              <h3 className=\"font-bold text-slate-900 dark:text-white font-heading mb-4 border-b border-slate-200 dark:border-slate-800 pb-2\">
                Standards & Identifiers
              </h3>
              <div className=\"grid grid-cols-2 gap-3 mb-6\">
                <div><span className=\"text-slate-600 dark:text-slate-300 block text-xs\">Standard</span><span className=\"text-slate-900 dark:text-white font-medium\">{material.standard || \"-\"}</span></div>
                <div><span className=\"text-slate-600 dark:text-slate-300 block text-xs\">Grade</span><span className=\"text-slate-900 dark:text-white font-medium\">{material.grade || \"-\"}</span></div>
                <div><span className=\"text-slate-600 dark:text-slate-300 block text-xs\">UNS Number</span><span className=\"text-slate-900 dark:text-white\">{material.uns_number || \"-\"}</span></div>
                <div><span className=\"text-slate-600 dark:text-slate-300 block text-xs\">EN / DIN</span><span className=\"text-slate-900 dark:text-white\">{material.en_number || material.din_number || \"-\"}</span></div>
                <div><span className=\"text-slate-600 dark:text-slate-300 block text-xs\">JIS (Japan)</span><span className=\"text-slate-900 dark:text-white\">{material.jis_number || \"-\"}</span></div>
                <div><span className=\"text-slate-600 dark:text-slate-300 block text-xs\">IS (India)</span><span className=\"text-slate-900 dark:text-white\">{material.is_number || \"-\"}</span></div>
              </div>

              <h3 className=\"font-bold text-slate-900 dark:text-white font-heading mb-4 border-b border-slate-200 dark:border-slate-800 pb-2 flex justify-between items-center\">
                Verified Sources
                {material.data_type === \"computational\" ? (
                  <span className=\"bg-indigo-100 text-indigo-700 text-[10px] px-2 py-0.5 rounded-full uppercase\">Computational</span>
                ) : (
                  <span className=\"bg-emerald-100 text-emerald-700 text-[10px] px-2 py-0.5 rounded-full uppercase\">Experimental</span>
                )}
              </h3>
              
              {material.sources && material.sources.length > 0 ? (
                <div className=\"space-y-3\">
                  {material.sources.map((src: any, idx: number) => (
                    <div key={idx} className=\"bg-slate-50 dark:bg-slate-950 p-3 rounded-lg border border-slate-200 dark:border-slate-800 text-xs shadow-sm\">
                      <div className=\"flex justify-between items-start mb-1\">
                        <span className=\"font-bold text-slate-900 dark:text-white\">{src.source_name}</span>
                        <span className=\"bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400 px-1.5 py-0.5 rounded text-[9px] uppercase font-bold\">
                          {src.access_type}
                        </span>
                      </div>
                      <p className=\"text-slate-500 mb-2 truncate\" title={src.notes}>{src.notes || src.source_type}</p>
                      {src.source_url ? (
                        <a href={src.source_url} target=\"_blank\" rel=\"noopener noreferrer\" className=\"text-blue-600 hover:underline flex items-center gap-1 font-medium\">
                          View Original Data <ChevronRight className=\"w-3 h-3\" />
                        </a>
                      ) : src.source_doi ? (
                        <a href={https://doi.org/} target=\"_blank\" rel=\"noopener noreferrer\" className=\"text-blue-600 hover:underline flex items-center gap-1 font-medium\">
                          DOI: {src.source_doi} <ChevronRight className=\"w-3 h-3\" />
                        </a>
                      ) : null}
                    </div>
                  ))}
                </div>
              ) : (
                <div className=\"p-3 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400 text-xs rounded-lg border border-amber-200 dark:border-amber-800/50\">
                  Manual verification pending. This material was added without an automated source link.
                </div>
              )}
            </div>'''.replace('\', '')

if old_block in content:
    content = content.replace(old_block, new_block)
    open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\materials\[id]\page.tsx', 'w', encoding='utf-8').write(content)
    print('SUCCESS')
else:
    print('FAILED TO FIND BLOCK')

