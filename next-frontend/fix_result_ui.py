import re

files = {
    'src/components/SafetyFactor.tsx': {
        'color': 'emerald',
        'regex': r'\{result && \([\s\S]*?<\/motion\.div>\s*\)\}',
        'replacement': '''{result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 rounded-xl bg-emerald-100 dark:bg-emerald-900/20 border border-emerald-900/50 space-y-2">
          <div className="flex justify-between items-center border-b border-emerald-900/30 pb-2">
            <span className="text-xs text-slate-600 dark:text-slate-300">Stress</span>
            <span className="font-medium text-slate-600 dark:text-slate-300">{result.stress_mpa.toFixed(2)} MPa</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-xs text-emerald-600 dark:text-emerald-400 font-bold">Safety Factor</span>
            <span className={ont-bold }>{result.safety_factor.toFixed(2)}</span>
          </div>
          <p className={	ext-[10px] pt-2 border-t border-emerald-900/50 }>
            {result.safety_factor >= 1.5 ? 'Design meets standard safety margins (>1.5).' : 'Warning: Design is below recommended safety margins.'}
          </p>
        </motion.div>
      )}'''
    },
    'src/components/ThermalExpansion.tsx': {
        'regex': r'\{result && \([\s\S]*?<\/motion\.div>\s*\)\}',
        'replacement': '''{result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 rounded-xl bg-orange-100 dark:bg-orange-900/20 border border-orange-900/50 space-y-2">
          <div className="flex justify-between items-center border-b border-orange-900/30 pb-2">
            <span className="text-xs text-slate-600 dark:text-slate-300">CTE (µm/m·°C)</span>
            <span className="font-medium text-slate-600 dark:text-slate-300">{result.cte.toFixed(1)}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-xs text-orange-600 dark:text-orange-400 font-bold">Expansion</span>
            <span className="font-bold text-orange-600 dark:text-orange-400">{result.expansion_mm.toFixed(3)} mm</span>
          </div>
          <p className="text-[10px] text-orange-600 dark:text-orange-300 pt-2 border-t border-orange-900/50">
            Total change in length due to thermal delta.
          </p>
        </motion.div>
      )}'''
    },
    'src/components/FatigueLife.tsx': {
        'regex': r'\{result && \([\s\S]*?<\/motion\.div>\s*\)\}',
        'replacement': '''{result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 rounded-xl bg-cyan-100 dark:bg-cyan-900/20 border border-cyan-900/50 space-y-2">
          <div className="flex justify-between items-center border-b border-cyan-900/30 pb-2">
            <span className="text-xs text-slate-600 dark:text-slate-300">Material Family</span>
            <span className="font-medium text-slate-600 dark:text-slate-300">{result.note.split(" ")[0]}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-xs text-cyan-600 dark:text-cyan-400 font-bold">Endurance Limit</span>
            <span className="font-bold text-cyan-600 dark:text-cyan-400">{result.endurance_limit.toFixed(1)} MPa</span>
          </div>
          <p className="text-[10px] text-cyan-600 dark:text-cyan-300 pt-2 border-t border-cyan-900/50">
            {result.note}
          </p>
        </motion.div>
      )}'''
    },
    'src/components/BeamDeflection.tsx': {
        'regex': r'\{result && \([\s\S]*?<\/motion\.div>\s*\)\}',
        'replacement': '''{result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 rounded-xl bg-purple-100 dark:bg-purple-900/20 border border-purple-900/50 space-y-2">
          <div className="flex justify-between items-center border-b border-purple-900/30 pb-2">
            <span className="text-xs text-slate-600 dark:text-slate-300">Modulus (E)</span>
            <span className="font-medium text-slate-600 dark:text-slate-300">{result.elastic_modulus_gpa} GPa</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-xs text-purple-600 dark:text-purple-400 font-bold">Max Deflection</span>
            <span className="font-bold text-purple-600 dark:text-purple-400">{result.deflection_mm.toFixed(3)} mm</span>
          </div>
          <p className="text-[10px] text-purple-600 dark:text-purple-300 pt-2 border-t border-purple-900/50">
            This represents the maximum physical displacement of the beam under the specified load and geometry.
          </p>
        </motion.div>
      )}'''
    },
    'src/components/ThermalShock.tsx': {
        'regex': r'\{result && \([\s\S]*?<\/motion\.div>\s*\)\}',
        'replacement': '''{result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 rounded-xl bg-orange-100 dark:bg-orange-900/20 border border-orange-900/50 space-y-2">
          <div className="flex justify-between items-center border-b border-orange-900/30 pb-2">
            <span className="text-xs text-slate-600 dark:text-slate-300">Induced Surface Stress</span>
            <span className="font-medium text-slate-600 dark:text-slate-300">{result.induced_stress.toFixed(1)} MPa</span>
          </div>
          <div className="flex justify-between items-center">
            <span className={	ext-xs font-bold }>Safety Margin</span>
            <span className={ont-bold }>{result.margin.toFixed(1)} MPa</span>
          </div>
          <p className={	ext-[10px] pt-2 border-t }>
            {result.survives ? '? Material Survives Thermal Shock.' : '? Fracture Imminent.'} Induced stress compares the sudden contraction forces against the material's yield limits.
          </p>
        </motion.div>
      )}'''
    }
}

for filepath, info in files.items():
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(info['regex'], info['replacement'], content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated all component results.")
