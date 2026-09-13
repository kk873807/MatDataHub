"use client";
import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MousePointer2, ChevronLeft, ChevronRight, Play, Pause } from "lucide-react";

export interface DemoStep {
  caption: string;
  detail: string;
  // cursor target position (relative to demo container)
  cursor: { x: number; y: number };
  // optional: which element to highlight (by index in the mockup)
  highlight?: string;
  // optional: click ripple effect
  click?: boolean;
}

interface GuidedDemoProps {
  steps: DemoStep[];
  children: (activeStep: number, highlightId: string | undefined) => React.ReactNode;
  height?: string;
}

function getDuration(step: DemoStep): number {
  const textLen = step.caption.length + step.detail.length;
  // Base 2.5s + 25ms per character, min 2.5s, max 7s
  return Math.min(7000, Math.max(2500, 2500 + textLen * 25));
}

export function GuidedDemo({ steps, children, height = "min-h-[340px]" }: GuidedDemoProps) {
  const [activeStep, setActiveStep] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [progress, setProgress] = useState(0);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const progressRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef(Date.now());

  const currentStep = steps[activeStep];
  const duration = getDuration(currentStep);

  const clearTimers = useCallback(() => {
    if (timerRef.current) clearTimeout(timerRef.current);
    if (progressRef.current) clearInterval(progressRef.current);
  }, []);

  const startStep = useCallback((stepIdx: number) => {
    clearTimers();
    setActiveStep(stepIdx);
    setProgress(0);
    startTimeRef.current = Date.now();
    const dur = getDuration(steps[stepIdx]);

    progressRef.current = setInterval(() => {
      const elapsed = Date.now() - startTimeRef.current;
      setProgress(Math.min(100, (elapsed / dur) * 100));
    }, 50);

    timerRef.current = setTimeout(() => {
      const next = (stepIdx + 1) % steps.length;
      startStep(next);
    }, dur);
  }, [steps, clearTimers]);

  useEffect(() => {
    if (playing) {
      startStep(activeStep);
    }
    return clearTimers;
  }, [playing]);

  const goTo = (idx: number) => {
    setPlaying(true);
    startStep(idx);
  };

  const prev = () => goTo((activeStep - 1 + steps.length) % steps.length);
  const next = () => goTo((activeStep + 1) % steps.length);

  const togglePlay = () => {
    if (playing) {
      clearTimers();
      setPlaying(false);
    } else {
      setPlaying(true);
    }
  };

  return (
    <div className="w-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl overflow-hidden">
      {/* Caption bar */}
      <div className="bg-white dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 px-6 py-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            {steps.map((_, i) => (
              <button
                key={i}
                onClick={() => goTo(i)}
                className={`w-2 h-2 rounded-full transition-all ${i === activeStep ? "bg-blue-500 w-6" : i < activeStep ? "bg-blue-300 dark:bg-blue-700" : "bg-slate-300 dark:bg-slate-700"}`}
              />
            ))}
          </div>
          <div className="flex items-center gap-1">
            <button onClick={prev} className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400 transition-colors">
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button onClick={togglePlay} className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400 transition-colors">
              {playing ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            </button>
            <button onClick={next} className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400 transition-colors">
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
        <AnimatePresence mode="wait">
          <motion.div key={activeStep} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.2 }}>
            <p className="text-sm font-bold text-slate-900 dark:text-white mb-1">
              <span className="text-blue-500 mr-1.5">Step {activeStep + 1}/{steps.length}</span>
              {currentStep.caption}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{currentStep.detail}</p>
          </motion.div>
        </AnimatePresence>
        {/* Progress bar */}
        <div className="mt-3 h-1 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
          <motion.div className="h-full bg-blue-500 rounded-full" style={{ width: `${progress}%` }} />
        </div>
      </div>

      {/* Mockup area */}
      <div className={`relative p-6 ${height}`}>
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808008_1px,transparent_1px),linear-gradient(to_bottom,#80808008_1px,transparent_1px)] bg-[size:24px_24px]"></div>
        <div className="relative z-10">
          {children(activeStep, currentStep.highlight)}
        </div>

        {/* Cursor */}
        <motion.div
          className="absolute z-50 pointer-events-none"
          animate={{ x: currentStep.cursor.x, y: currentStep.cursor.y }}
          transition={{ type: "tween", ease: "easeInOut", duration: 0.6 }}
        >
          <MousePointer2 className="w-6 h-6 text-black fill-white drop-shadow-lg -rotate-12" />
          {currentStep.click && (
            <motion.div
              key={activeStep}
              initial={{ scale: 0, opacity: 0.6 }}
              animate={{ scale: 2.5, opacity: 0 }}
              transition={{ duration: 0.5 }}
              className="absolute top-0 left-0 w-4 h-4 rounded-full bg-blue-500/50"
            />
          )}
        </motion.div>
      </div>
    </div>
  );
}
