"use client";
import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Pause, Play } from "lucide-react";
import { DemoCursor } from "./DemoCursor";
import { DemoCaption } from "./DemoCaption";

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

export interface DemoStep {
  label: string;
  detail?: string;
  cursor: { x: number; y: number };
  duration: number;
  click?: boolean;
  scroll?: number;
  phaseIndex: number;
}

export interface DemoPhase {
  name: string;
  color: string;
}

interface DemoEngineProps {
  steps: DemoStep[];
  phases: DemoPhase[];
  /** Height of the inner simulated window (default 420px) */
  windowHeight?: number;
  /** Header rendered inside the window chrome (sticky top) */
  header?: React.ReactNode;
  /** The simulated UI content — receives current step index */
  children: (step: number) => React.ReactNode;
}

/* ------------------------------------------------------------------ */
/*  Phase Transition Card                                              */
/* ------------------------------------------------------------------ */

function PhaseTransition({ phase, index, total }: { phase: DemoPhase; index: number; total: number }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="absolute inset-0 z-30 flex items-center justify-center bg-white/95 dark:bg-slate-950/95 backdrop-blur-lg"
    >
      <div className="text-center px-8">
        {/* Phase counter dots */}
        <div className="flex items-center justify-center gap-2 mb-5">
          {Array.from({ length: total }).map((_, i) => (
            <div
              key={i}
              className={`rounded-full transition-all duration-500 ${
                i === index
                  ? "w-6 h-1.5 bg-blue-500"
                  : i < index
                  ? "w-1.5 h-1.5 bg-blue-300 dark:bg-blue-700"
                  : "w-1.5 h-1.5 bg-slate-200 dark:bg-slate-700"
              }`}
            />
          ))}
        </div>
        <p className="text-[10px] font-semibold uppercase tracking-[0.15em] text-slate-400 dark:text-slate-500 mb-2">
          Section {index + 1} of {total}
        </p>
        <motion.p
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15, duration: 0.3 }}
          className="text-base font-bold text-slate-800 dark:text-white tracking-tight"
        >
          {phase.name}
        </motion.p>
      </div>
    </motion.div>
  );
}

/* ------------------------------------------------------------------ */
/*  DemoEngine                                                         */
/* ------------------------------------------------------------------ */

export function DemoEngine({
  steps,
  phases,
  windowHeight = 420,
  header,
  children,
}: DemoEngineProps) {
  const [step, setStep] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [progress, setProgress] = useState(0);
  const [showPhaseCard, setShowPhaseCard] = useState(false);
  const [speed, setSpeed] = useState(1);

  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const progressRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const startTimeRef = useRef(Date.now());
  const prevPhaseRef = useRef(0);
  const containerRef = useRef<HTMLDivElement>(null);

  const s = steps[step];
  const currentPhaseIndex = s.phaseIndex;

  /* ---------- timer helpers ---------- */

  const clearTimers = useCallback(() => {
    if (timerRef.current) clearTimeout(timerRef.current);
    if (progressRef.current) clearInterval(progressRef.current);
  }, []);

  const startStep = useCallback(
    function startStep(idx: number) {
      clearTimers();
      const nextStep = steps[idx];
      if (!nextStep) return;

      // Phase transition check
      if (idx > 0 && nextStep.phaseIndex !== prevPhaseRef.current) {
        setShowPhaseCard(true);
        prevPhaseRef.current = nextStep.phaseIndex;
        timerRef.current = setTimeout(() => {
          setShowPhaseCard(false);
          setStep(idx);
          setProgress(0);
          startTimeRef.current = Date.now();
          const dur = nextStep.duration / speed;
          progressRef.current = setInterval(() => {
            const elapsed = Date.now() - startTimeRef.current;
            setProgress(Math.min(100, (elapsed / dur) * 100));
          }, 40);
          timerRef.current = setTimeout(() => {
            const next = (idx + 1) % steps.length;
            if (next === 0) prevPhaseRef.current = 0;
            startStep(next);
          }, dur);
        }, 1400 / speed);
      } else {
        setStep(idx);
        setProgress(0);
        startTimeRef.current = Date.now();
        const dur = nextStep.duration / speed;
        progressRef.current = setInterval(() => {
          const elapsed = Date.now() - startTimeRef.current;
          setProgress(Math.min(100, (elapsed / dur) * 100));
        }, 40);
        timerRef.current = setTimeout(() => {
          const next = (idx + 1) % steps.length;
          if (next === 0) prevPhaseRef.current = 0;
          startStep(next);
        }, dur);
      }
    },
    [steps, speed, clearTimers]
  );

  /* ---------- play/pause ---------- */

  useEffect(() => {
    if (playing) {
      startStep(step);
    } else {
      clearTimers();
    }
    return clearTimers;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playing, speed]);

  /* ---------- keyboard ---------- */

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > window.innerHeight) return;

      if (e.code === "Space") {
        e.preventDefault();
        setPlaying((p) => !p);
      } else if (e.code === "ArrowRight") {
        e.preventDefault();
        const next = (step + 1) % steps.length;
        setPlaying(true);
        prevPhaseRef.current = steps[next].phaseIndex;
        startStep(next);
      } else if (e.code === "ArrowLeft") {
        e.preventDefault();
        const prev = (step - 1 + steps.length) % steps.length;
        setPlaying(true);
        prevPhaseRef.current = steps[prev].phaseIndex;
        startStep(prev);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [step, steps, startStep]);

  /* ---------- speed cycle ---------- */

  const cycleSpeed = () => {
    setSpeed((s) => (s === 1 ? 1.5 : s === 1.5 ? 2 : 1));
  };

  /* ---------- render ---------- */

  return (
    <div
      ref={containerRef}
      className="w-full rounded-2xl sm:rounded-3xl p-3 sm:p-5 relative bg-gradient-to-b from-slate-50 to-slate-100/80 dark:from-slate-900 dark:to-slate-950 border border-slate-200/60 dark:border-slate-800/60"
    >
      {/* Subtle dot grid */}
      <div className="absolute inset-0 rounded-2xl sm:rounded-3xl pointer-events-none opacity-40 bg-[radial-gradient(#94a3b820_1px,transparent_1px)] bg-[size:16px_16px]" />

      {/* Top bar: INTERACTIVE DEMO badge + Speed + Play/Pause */}
      <div className="relative z-20 flex items-center justify-between mb-3 px-1">
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-blue-500/8 dark:bg-blue-400/10 border border-blue-500/15 dark:border-blue-400/15">
            <span className="relative flex h-1.5 w-1.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-500 opacity-60" />
              <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-blue-500" />
            </span>
            <span className="text-[10px] font-semibold tracking-wide text-blue-600 dark:text-blue-400 uppercase">
              Interactive Demo
            </span>
          </span>
        </div>

        <div className="flex items-center gap-1.5">
          {/* Speed toggle */}
          <button
            onClick={cycleSpeed}
            className="px-2 py-1 rounded-md text-[10px] font-mono font-bold text-slate-500 dark:text-slate-400 hover:bg-slate-200/60 dark:hover:bg-slate-800/60 transition-colors"
            title="Playback speed"
          >
            {speed}×
          </button>

          {/* Play/Pause */}
          <button
            onClick={() => setPlaying((p) => !p)}
            className="p-1.5 rounded-md text-slate-500 dark:text-slate-400 hover:bg-slate-200/60 dark:hover:bg-slate-800/60 transition-colors"
            title={playing ? "Pause demo" : "Resume demo"}
          >
            {playing ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* Main window chrome */}
      <div
        className="relative z-10 w-full max-w-lg mx-auto bg-white dark:bg-slate-950 border border-slate-200/80 dark:border-slate-700/40 rounded-xl sm:rounded-2xl overflow-hidden flex flex-col"
        style={{
          height: windowHeight,
          boxShadow:
            "0 1px 2px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.06), 0 16px 40px rgba(0,0,0,0.04)",
        }}
      >
        {/* Window title bar */}
        <div className="flex items-center gap-1.5 px-4 py-2 border-b border-slate-100 dark:border-slate-800/60 bg-slate-50/90 dark:bg-slate-900/90 shrink-0">
          <div className="w-2 h-2 rounded-full bg-rose-400/60" />
          <div className="w-2 h-2 rounded-full bg-amber-400/60" />
          <div className="w-2 h-2 rounded-full bg-emerald-400/60" />
          {header && (
            <div className="ml-2.5 flex items-center gap-1.5 border-l border-slate-200/60 dark:border-slate-700/40 pl-2.5">
              {header}
            </div>
          )}
        </div>

        {/* Viewport for scrolling */}
        <div className="flex-1 relative w-full overflow-hidden bg-white dark:bg-slate-950">
          {/* Phase transition overlay (fixed to viewport) */}
          <AnimatePresence>
            {showPhaseCard && phases[currentPhaseIndex] && (
              <PhaseTransition
                phase={phases[currentPhaseIndex]}
                index={currentPhaseIndex}
                total={phases.length}
              />
            )}
          </AnimatePresence>

          {/* Paused overlay (fixed to viewport) */}
          <AnimatePresence>
            {!playing && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="absolute inset-0 z-40 flex items-center justify-center bg-black/5 dark:bg-black/20 backdrop-blur-[1px] cursor-pointer"
                onClick={() => setPlaying(true)}
              >
                <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-white/90 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-700 shadow-lg">
                  <Play className="w-4 h-4 text-blue-500" />
                  <span className="text-xs font-semibold text-slate-600 dark:text-slate-300">Paused — click to resume</span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Scrolling content layer */}
          <motion.div
            className="w-full relative"
            animate={{ y: s.scroll || 0 }}
            transition={{ type: "spring", stiffness: 80, damping: 22 }}
          >
            {/* Demo content */}
            {children(step)}

            {/* Cursor (moves with content) */}
            {playing && (
              <DemoCursor
                x={s.cursor.x}
                y={s.cursor.y}
                click={s.click}
                stepKey={step}
              />
            )}
          </motion.div>
        </div>
      </div>

      {/* Caption panel */}
      <DemoCaption
        label={s.label}
        detail={s.detail}
        stepIndex={step}
        totalSteps={steps.length - 1}
        phases={phases}
        currentPhaseIndex={currentPhaseIndex}
        progress={progress}
        playing={playing}
      />
    </div>
  );
}
