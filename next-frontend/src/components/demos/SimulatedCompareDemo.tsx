"use client";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Scale, MousePointer2 } from "lucide-react";

export function SimulatedCompareDemo() {
  const [step, setStep] = useState(0);

  useEffect(() => {
    // Sequence:
    // 0: Initial state, cursor at bottom right
    // 1: Cursor moves to search bar 1
    // 2: Typing "Titanium"
    // 3: Cursor clicks first result
    // 4: Cursor moves to search bar 2
    // 5: Typing "Aluminium"
    // 6: Cursor clicks first result
    // 7: Cursor moves to "Compare" button
    // 8: Clicks compare, shows radar chart
    // 9: Reset after a few seconds

    let sequence = [
      { step: 1, delay: 1000 },
      { step: 2, delay: 1000 },
      { step: 3, delay: 1000 },
      { step: 4, delay: 1000 },
      { step: 5, delay: 1000 },
      { step: 6, delay: 1000 },
      { step: 7, delay: 1000 },
      { step: 8, delay: 1000 },
      { step: 0, delay: 4000 }
    ];

    let currentTimeout: NodeJS.Timeout;
    
    const runSequence = (index: number) => {
      if (index >= sequence.length) return;
      currentTimeout = setTimeout(() => {
        setStep(sequence[index].step);
        runSequence(index + 1);
      }, sequence[index].delay);
    };

    runSequence(0);

    return () => clearTimeout(currentTimeout);
  }, [step === 0]); // restart when step resets to 0

  // Cursor positions based on step
  const cursorVariants = {
    0: { x: 400, y: 300, opacity: 0 },
    1: { x: 60, y: 50, opacity: 1 },
    2: { x: 60, y: 50, opacity: 1 },
    3: { x: 60, y: 120, opacity: 1 },
    4: { x: 260, y: 50, opacity: 1 },
    5: { x: 260, y: 50, opacity: 1 },
    6: { x: 260, y: 120, opacity: 1 },
    7: { x: 200, y: 160, opacity: 1, scale: 1 },
    8: { x: 200, y: 160, opacity: 1, scale: 0.9 }, // click effect
    9: { x: 400, y: 300, opacity: 0 }
  };

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 relative overflow-hidden flex flex-col items-center justify-center min-h-[400px]">
      
      {/* Background UI Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

      <div className="relative z-10 w-full max-w-lg bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl p-6">
        <h3 className="font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
          <Scale className="w-5 h-5 text-blue-500" /> Compare Materials
        </h3>

        <div className="flex gap-4 mb-6">
          {/* Material 1 Dropdown */}
          <div className="flex-1 relative">
            <div className={`border rounded-xl p-2 flex items-center gap-2 ${step >= 2 ? 'border-blue-500 ring-2 ring-blue-500/20' : 'border-slate-200 dark:border-slate-700'}`}>
              <Search className="w-4 h-4 text-slate-400" />
              <div className="text-sm font-medium text-slate-700 dark:text-slate-300">
                {step === 1 && <span className="animate-pulse">|</span>}
                {step >= 2 && step < 3 && <span>Titanium<span className="animate-pulse">|</span></span>}
                {step >= 3 && <span>Ti-6Al-4V Grade 5</span>}
                {step < 1 && <span className="text-slate-400">Select material...</span>}
              </div>
            </div>
            
            {/* Dropdown 1 */}
            <AnimatePresence>
              {step === 2 && (
                <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="absolute top-full left-0 w-full mt-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl shadow-xl p-2 z-20">
                   <div className="p-2 bg-slate-100 dark:bg-slate-700 rounded-lg text-sm font-medium hover:bg-blue-50 cursor-pointer">Ti-6Al-4V Grade 5</div>
                   <div className="p-2 text-sm text-slate-500">Titanium Grade 2</div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Material 2 Dropdown */}
          <div className="flex-1 relative">
            <div className={`border rounded-xl p-2 flex items-center gap-2 ${step >= 5 && step < 6 ? 'border-blue-500 ring-2 ring-blue-500/20' : 'border-slate-200 dark:border-slate-700'}`}>
              <Search className="w-4 h-4 text-slate-400" />
              <div className="text-sm font-medium text-slate-700 dark:text-slate-300">
                {step === 4 && <span className="animate-pulse">|</span>}
                {step === 5 && <span>Alumini<span className="animate-pulse">|</span></span>}
                {step >= 6 && <span>Aluminium 7075-T6</span>}
                {step < 4 && <span className="text-slate-400">Select material...</span>}
              </div>
            </div>

            {/* Dropdown 2 */}
            <AnimatePresence>
              {step === 5 && (
                <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="absolute top-full left-0 w-full mt-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl shadow-xl p-2 z-20">
                   <div className="p-2 bg-slate-100 dark:bg-slate-700 rounded-lg text-sm font-medium">Aluminium 7075-T6</div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        <button className={`w-full py-3 rounded-xl font-bold text-white transition-all ${step >= 8 ? 'bg-indigo-500' : 'bg-blue-600'}`}>
          {step >= 8 ? 'Generating Analysis...' : 'Run Comparison'}
        </button>

        {/* Results */}
        <AnimatePresence>
          {step >= 8 && (
            <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} className="mt-6 pt-6 border-t border-slate-100 dark:border-slate-800 overflow-hidden">
              <div className="flex items-center gap-4">
                 {/* Fake Radar Chart */}
                 <div className="relative w-32 h-32 rounded-full border border-slate-200 dark:border-slate-700 flex items-center justify-center">
                    <div className="absolute w-24 h-24 border border-slate-100 dark:border-slate-800 rounded-full"></div>
                    <div className="absolute w-full h-[1px] bg-slate-200 dark:bg-slate-700"></div>
                    <div className="absolute h-full w-[1px] bg-slate-200 dark:bg-slate-700"></div>
                    {/* Data Polygon 1 */}
                    <svg className="absolute inset-0 w-full h-full text-blue-500/30 fill-current"><polygon points="64,20 100,64 64,80 30,64" /></svg>
                    {/* Data Polygon 2 */}
                    <svg className="absolute inset-0 w-full h-full text-purple-500/30 fill-current"><polygon points="64,40 110,64 64,100 20,64" /></svg>
                 </div>
                 <div className="flex-1 space-y-3">
                   <div className="flex items-center gap-2"><div className="w-3 h-3 rounded bg-blue-500"></div><span className="text-xs font-semibold text-slate-700 dark:text-slate-300">Ti-6Al-4V wins on Ultimate Tensile</span></div>
                   <div className="flex items-center gap-2"><div className="w-3 h-3 rounded bg-purple-500"></div><span className="text-xs font-semibold text-slate-700 dark:text-slate-300">Al 7075 is 42% more cost-effective</span></div>
                   <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded overflow-hidden"><div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 w-3/4"></div></div>
                 </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* The Animated Mouse Pointer */}
      <motion.div
        className="absolute z-50 pointer-events-none"
        variants={cursorVariants}
        animate={String(step)}
        transition={{ type: "tween", ease: "easeInOut", duration: 0.6 }}
      >
        <MousePointer2 className="w-8 h-8 text-black fill-white drop-shadow-xl -rotate-12" />
      </motion.div>
    </div>
  );
}
