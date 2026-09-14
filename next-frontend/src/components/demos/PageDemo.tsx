"use client";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Play, X, RotateCcw } from "lucide-react";

interface PageDemoProps {
  pageKey: string;
  title: string;
  children: React.ReactNode;
}

export function PageDemo({ pageKey, title, children }: PageDemoProps) {
  const storageKey = `demo_dismissed_${pageKey}`;
  const [show, setShow] = useState(false);
  const [dismissed, setDismissed] = useState(true);

  useEffect(() => {
    const wasDismissed = localStorage.getItem(storageKey);
    if (!wasDismissed) {
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
      {/* Replay button */}
      {dismissed && !show && (
        <motion.button
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          onClick={handleReplay}
          className="group inline-flex items-center gap-2 px-4 py-2 mb-4 text-[13px] font-medium rounded-lg transition-all duration-200 border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 hover:border-blue-300 dark:hover:border-blue-700 hover:text-blue-600 dark:hover:text-blue-400 hover:shadow-sm"
        >
          <Play className="w-3.5 h-3.5" />
          {title}
        </motion.button>
      )}

      {/* Demo panel */}
      <AnimatePresence>
        {show && (
          <motion.div
            initial={{ opacity: 0, height: 0, marginBottom: 0 }}
            animate={{ opacity: 1, height: "auto", marginBottom: 24 }}
            exit={{ opacity: 0, height: 0, marginBottom: 0 }}
            transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
            className="overflow-hidden"
          >
            <div className="relative">
              {/* Header */}
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-2">
                  <Play className="w-3.5 h-3.5 text-blue-500" />
                  {title}
                </h3>
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => { setShow(false); setTimeout(() => setShow(true), 150); }}
                    className="p-1.5 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                    title="Replay"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                  </button>
                  <button
                    onClick={handleDismiss}
                    className="p-1.5 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                    title="Close"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>

              {/* Demo content */}
              {children}

              {/* Footer */}
              <div className="flex justify-end mt-3">
                <button
                  onClick={handleDismiss}
                  className="text-xs text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors px-2 py-1 rounded hover:bg-slate-50 dark:hover:bg-slate-800/50"
                >
                  Dismiss
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
