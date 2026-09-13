const fs = require('fs');

function fixDemo(path) {
  let file = fs.readFileSync(path, 'utf8');

  // Modify the wrapper layout
  // Replace the old grid div + main window
  file = file.replace(
    /<div className="w-full relative">\s*<div className="bg-slate-100.*?min-h-\[500px\]">/,
    `<div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-4 sm:p-6 relative">
      {/* Decorative Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] rounded-3xl pointer-events-none"></div>

      {/* FIXED HEIGHT WINDOW */}
      <div className="relative z-10 w-full max-w-lg mx-auto bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl h-[420px] overflow-hidden flex flex-col">
        <motion.div className="flex flex-col h-full w-full relative" animate={{ y: 0 }}>`
  );

  // Compare demo uses min-h-[480px]
  file = file.replace(
    /<div className="w-full bg-slate-100.*?min-h-\[480px\]">/,
    `<div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-4 sm:p-6 relative">
      {/* Decorative Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] rounded-3xl pointer-events-none"></div>

      {/* FIXED HEIGHT WINDOW */}
      <div className="relative z-10 w-full max-w-lg mx-auto bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl h-[420px] overflow-hidden flex flex-col">
        <motion.div className="flex flex-col h-full w-full relative" animate={{ y: s.scroll || 0 }}>`
  );

  // Remove the old grid layer
  file = file.replace(/<div className="absolute inset-0 bg-\[linear-gradient.*?pointer-events-none"><\/div>/, '');

  // Remove the old window container declarations since we wrapped them
  file = file.replace(/<div className="relative z-10 w-full max-w-lg mx-auto">\s*<div className="bg-white.*?flex flex-col">/, '');
  
  // Close the new motion.div inside the fixed window
  // Find the cursor and replace it to close the motion div
  file = file.replace(
    /\{\/\* Cursor \*\/\}\s*<motion\.div className="absolute z-50.*?<\/motion\.div>/,
    `{/* Cursor */}
        <motion.div className="absolute z-50 pointer-events-none" animate={{ x: s.cursor.x, y: s.cursor.y }} transition={{ type: "tween", ease: "easeInOut", duration: 0.5 }}>
          <MousePointer2 className="w-7 h-7 text-black fill-white drop-shadow-xl -rotate-12" />
          {s.click && <motion.div key={step} initial={{ scale: 0, opacity: 0.6 }} animate={{ scale: 2.5, opacity: 0 }} transition={{ duration: 0.5 }} className="absolute top-0 left-0 w-4 h-4 rounded-full bg-blue-500/50" />}
        </motion.div>
      </motion.div>
    </div>`
  );

  // Fix the label
  const oldLabel = /\{\/\* Label - Sticky to viewport \*\/\}[\s\S]*?<\/div>/;
  const newLabel = `{/* FIXED CAPTION LABEL */}
      <div className="mt-6 flex justify-center z-40 relative h-16">
        <AnimatePresence mode="wait">
          {s.label && (
            <motion.div key={step} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}
              className="bg-slate-900 dark:bg-slate-800 text-white text-sm sm:text-base font-semibold px-6 py-3 rounded-2xl shadow-xl max-w-md text-center border border-slate-800"
            >{s.label}</motion.div>
          )}
        </AnimatePresence>
      </div>`;
  file = file.replace(oldLabel, newLabel);
  
  // For the compare demo label format (it used absolute bottom-4 in an older state maybe, or sticky)
  file = file.replace(/\{\/\* Label \*\/\}\s*<AnimatePresence mode="wait">[\s\S]*?<\/AnimatePresence>/, newLabel);
  // Remove the wrapper div if it had one
  file = file.replace(/<div className="sticky bottom-6.*?overflow-visible">/, '');

  // Add a closing div for the outer container and handle any leftover tags
  // Actually, string replacement on JSX layout can be brittle. Let's just fix the files cleanly.
  fs.writeFileSync(path, file);
}

try { fixDemo('src/components/demos/SimulatedCompareDemo.tsx'); } catch(e){}
try { fixDemo('src/components/demos/SimulatedWorkspaceDemo.tsx'); } catch(e){}
console.log('Done');
