"use client";
import { motion } from "framer-motion";
import { MousePointer2 } from "lucide-react";

interface DemoCursorProps {
  x: number;
  y: number;
  click?: boolean;
  stepKey: number;
}

export function DemoCursor({ x, y, click, stepKey }: DemoCursorProps) {
  return (
    <motion.div
      className="absolute z-50 pointer-events-none"
      animate={{ x, y }}
      transition={{ type: "tween", ease: [0.22, 1, 0.36, 1], duration: 0.55 }}
    >
      {/* Subtle ambient glow */}
      <div className="absolute -top-2 -left-2 w-10 h-10 rounded-full bg-blue-500/10 dark:bg-blue-400/8 blur-md pointer-events-none" />

      {/* Main cursor */}
      <MousePointer2
        className="w-5 h-5 -rotate-12"
        style={{
          color: "#1e293b",
          fill: "white",
          filter: "drop-shadow(0 1px 3px rgba(0,0,0,0.2)) drop-shadow(0 4px 8px rgba(0,0,0,0.1))",
        }}
      />

      {/* Click effect — clean double-ring */}
      {click && (
        <>
          <motion.div
            key={`click-a-${stepKey}`}
            initial={{ scale: 0, opacity: 0.5 }}
            animate={{ scale: 3.5, opacity: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="absolute top-0 left-0 w-3 h-3 rounded-full border-2 border-blue-500/40"
          />
          <motion.div
            key={`click-b-${stepKey}`}
            initial={{ scale: 0, opacity: 0.3 }}
            animate={{ scale: 5, opacity: 0 }}
            transition={{ duration: 0.7, ease: "easeOut", delay: 0.06 }}
            className="absolute top-0 left-0 w-3 h-3 rounded-full border border-blue-400/25"
          />
        </>
      )}
    </motion.div>
  );
}
