const fs = require('fs');
['src/components/demos/SimulatedMaterialsDemo.tsx', 'src/components/demos/SimulatedCompareDemo.tsx'].forEach(path => {
  let file = fs.readFileSync(path, 'utf8');
  
  // 1. Remove overflow-hidden from outer div
  file = file.replace(/overflow-hidden min-h-\[480px\]/g, 'min-h-[480px]');
  file = file.replace(/overflow-hidden min-h-\[530px\]/g, 'min-h-[530px]');
  
  // 2. Add pointer-events-none to absolute grid to allow clicks, and remove overflow-hidden from outer container
  file = file.replace(/<div className="absolute inset-0 bg-\[linear-gradient\(to_right,#80808012_1px,transparent_1px\),linear-gradient\(to_bottom,#80808012_1px,transparent_1px\)\] bg-\[size:24px_24px\]"><\/div>/g, 
  '<div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] rounded-3xl overflow-hidden pointer-events-none"></div>');
  
  // 3. Replace the entire label rendering block
  const oldLabelBlock = /\{\/\* Label \*\/\}\s*<AnimatePresence mode="wait">\s*\{s\.label && \(\s*<motion\.div key=\{step\} initial=\{\{ opacity: 0, y: 5 \}\} animate=\{\{ opacity: 1, y: 0 \}\} exit=\{\{ opacity: 0 \}\}\s*className="absolute bottom-4 left-1\/2 -translate-x-1\/2 z-40 bg-slate-900 text-white text-xs font-semibold px-4 py-2 rounded-xl shadow-xl max-w-sm text-center pointer-events-none"\s*>\s*\{s\.label\}\s*<\/motion\.div>\s*\)\}\s*<\/AnimatePresence>/g;
  
  const newLabelBlock = `{/* Label - Sticky to viewport */}
      <div className="sticky bottom-6 z-40 flex justify-center pointer-events-none mt-4 h-0 overflow-visible">
        <AnimatePresence mode="wait">
          {s.label && (
            <motion.div key={step} initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: -40 }} exit={{ opacity: 0 }}
              className="bg-slate-900 dark:bg-slate-800 text-white text-xs sm:text-sm font-semibold px-5 py-3 rounded-xl shadow-2xl max-w-md text-center border border-slate-700"
            >{s.label}</motion.div>
          )}
        </AnimatePresence>
      </div>`;
      
  file = file.replace(oldLabelBlock, newLabelBlock);

  // 4. Double the durations so they are readable
  file = file.replace(/duration: 1000/g, 'duration: 2000');
  file = file.replace(/duration: 1200/g, 'duration: 2500');
  file = file.replace(/duration: 1500/g, 'duration: 3000');
  file = file.replace(/duration: 1800/g, 'duration: 3500');
  file = file.replace(/duration: 2000/g, 'duration: 4000');
  file = file.replace(/duration: 2200/g, 'duration: 4500');
  file = file.replace(/duration: 2500/g, 'duration: 5000');
  file = file.replace(/duration: 2800/g, 'duration: 5500');
  file = file.replace(/duration: 3000/g, 'duration: 6000');

  fs.writeFileSync(path, file);
});
console.log('Fixed Materials and Compare demos');
