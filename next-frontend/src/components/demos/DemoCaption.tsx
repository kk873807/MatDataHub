"use client";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronRight } from "lucide-react";

interface Phase {
  name: string;
  color: string;
}

interface DemoCaptionProps {
  label: string;
  detail?: string;
  stepIndex: number;
  totalSteps: number;
  phases: Phase[];
  currentPhaseIndex: number;
  progress: number;
  playing?: boolean;
}

export function DemoCaption({
  label,
  detail,
  stepIndex,
  totalSteps,
  phases,
  currentPhaseIndex,
  progress,
  playing = true,
}: DemoCaptionProps) {
  if (!label) return <div className="min-h-[88px]" />;

  return (
    <div className="mt-4 relative z-40 px-1">
      <div className="relative max-w-lg mx-auto overflow-hidden rounded-xl border border-slate-200/70 dark:border-slate-700/40 bg-white/85 dark:bg-slate-900/85 backdrop-blur-2xl shadow-[0_4px_24px_rgba(0,0,0,0.06)] dark:shadow-[0_4px_24px_rgba(0,0,0,0.3)]">
        
        {/* Progress bar */}
        <div className="h-[3px] bg-slate-100 dark:bg-slate-800 overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-blue-500 via-blue-400 to-blue-500"
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.15, ease: "linear" }}
          />
        </div>

        <div className="px-4 sm:px-5 py-3.5">
          {/* Top row: phase breadcrumbs + step counter */}
          <div className="flex items-center justify-between mb-2">
            {/* Phase breadcrumbs */}
            <nav className="flex items-center gap-0.5 min-w-0 overflow-hidden">
              {phases.map((phase, i) => (
                <div
                  key={i}
                  className={`flex items-center gap-0.5 shrink-0 transition-all duration-300 ${
                    i === currentPhaseIndex
                      ? "opacity-100"
                      : i < currentPhaseIndex
                      ? "opacity-50"
                      : "opacity-30"
                  }`}
                >
                  {i > 0 && (
                    <ChevronRight className="w-2.5 h-2.5 text-slate-300 dark:text-slate-600 mx-0.5 shrink-0" />
                  )}
                  <span
                    className={`text-[9px] font-semibold tracking-wide whitespace-nowrap transition-colors duration-300 ${
                      i === currentPhaseIndex
                        ? "text-blue-600 dark:text-blue-400"
                        : "text-slate-400 dark:text-slate-500"
                    }`}
                  >
                    {phase.name}
                  </span>
                </div>
              ))}
            </nav>

            {/* Step counter */}
            <div className="flex items-center gap-1.5 shrink-0 ml-3">
              {!playing && (
                <span className="text-[8px] font-semibold text-amber-500 uppercase tracking-wider">
                  Paused
                </span>
              )}
              <span className="text-[10px] font-mono text-slate-400 dark:text-slate-500 tabular-nums">
                <span className="font-bold text-slate-500 dark:text-slate-400">{stepIndex + 1}</span>
                <span className="text-slate-300 dark:text-slate-600 mx-0.5">/</span>
                {totalSteps}
              </span>
            </div>
          </div>

          {/* Label text */}
          <AnimatePresence mode="wait">
            <motion.div
              key={stepIndex}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -4 }}
              transition={{ duration: 0.2 }}
            >
              <p className="text-[13px] sm:text-sm font-medium text-slate-800 dark:text-slate-100 leading-relaxed">
                {label}
              </p>
              {detail && (
                <p className="text-[11px] sm:text-xs text-slate-500 dark:text-slate-400 mt-1.5 leading-relaxed">
                  {detail}
                </p>
              )}
            </motion.div>
          </AnimatePresence>

          {/* Keyboard hints — minimal, professional */}
          <div className="flex items-center gap-2.5 mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-800/50">
            <span className="text-[9px] text-slate-400 dark:text-slate-500 flex items-center gap-1">
              <kbd className="inline-flex items-center justify-center min-w-[1.25rem] h-4 px-1 rounded bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-[8px] font-mono text-slate-500 dark:text-slate-400">
                ␣
              </kbd>
              <span className="hidden sm:inline">pause</span>
            </span>
            <span className="text-[9px] text-slate-400 dark:text-slate-500 flex items-center gap-1">
              <kbd className="inline-flex items-center justify-center min-w-[1.25rem] h-4 px-1 rounded bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-[8px] font-mono text-slate-500 dark:text-slate-400">
                ←
              </kbd>
              <kbd className="inline-flex items-center justify-center min-w-[1.25rem] h-4 px-1 rounded bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-[8px] font-mono text-slate-500 dark:text-slate-400">
                →
              </kbd>
              <span className="hidden sm:inline">navigate</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
