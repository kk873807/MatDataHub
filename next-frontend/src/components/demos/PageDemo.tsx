"use client";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Play, X, RotateCcw } from "lucide-react";

interface PageDemoProps {
  pageKey: string;        // unique key for localStorage, e.g. "analytics", "materials"
  title: string;          // e.g. "See how Compare works"
  children: React.ReactNode; // the actual demo component
}

export function PageDemo({ pageKey, title, children }: PageDemoProps) {
  const storageKey = `demo_dismissed_${pageKey}`;
  const [show, setShow] = useState(false);
  const [dismissed, setDismissed] = useState(true); // start hidden until we check

  useEffect(() => {
    const wasDismissed = localStorage.getItem(storageKey);
    if (!wasDismissed) {
      // First visit — auto-show the demo
      setShow(true);
      setDismissed(false);
    } else {
      setDismissed(true);
      setShow(false);
    }
  }, [storageKey]);

  const handleDismiss = () => {
    setShow(false);
    setDismissed(true);
    localStorage.setItem(storageKey, "true");
  };

  const handleReplay = () => {
    setShow(true);
  };

  return (
    <>
      {/* Replay button — always visible when demo is dismissed */}
      {dismissed && !show && (
        <motion.button
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          onClick={handleReplay}
          className="flex items-center gap-2 px-4 py-2 mb-4 text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 hover:bg-blue-100 dark:hover:bg-blue-900/40 border border-blue-200 dark:border-blue-800 rounded-xl transition-all"
        >
          <Play className="w-4 h-4" /> {title}
        </motion.button>
      )}

      {/* Demo panel */}
      <AnimatePresence>
        {show && (
          <motion.div
            initial={{ opacity: 0, height: 0, marginBottom: 0 }}
            animate={{ opacity: 1, height: "auto", marginBottom: 24 }}
            exit={{ opacity: 0, height: 0, marginBottom: 0 }}
            transition={{ duration: 0.4, ease: "easeInOut" }}
            className="overflow-hidden"
          >
            <div className="relative">
              {/* Header */}
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300 flex items-center gap-2">
                  <Play className="w-4 h-4 text-blue-500" /> {title}
                </h3>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => { setShow(false); setTimeout(() => setShow(true), 100); }}
                    className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                    title="Replay"
                  >
                    <RotateCcw className="w-4 h-4" />
                  </button>
                  <button
                    onClick={handleDismiss}
                    className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                    title="Dismiss"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Demo content */}
              {children}

              {/* Footer */}
              <div className="flex justify-end mt-3">
                <button
                  onClick={handleDismiss}
                  className="text-xs font-semibold text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 transition-colors"
                >
                  Got it, don't show again
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
