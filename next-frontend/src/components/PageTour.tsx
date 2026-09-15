"use client";
import { useState, useEffect, forwardRef, useImperativeHandle } from "react";
import dynamic from "next/dynamic";
import { Step } from "react-joyride";

const JoyrideComponent = dynamic(
  () => import("react-joyride").then((mod) => mod.Joyride),
  { ssr: false }
);

export interface PageTourRef {
  startTour: () => void;
}

interface PageTourProps {
  steps: Step[];
  storageKey: string;
}

export const PageTour = forwardRef<PageTourRef, PageTourProps>(({ steps, storageKey }, ref) => {
  const [run, setRun] = useState(false);
  const [mounted, setMounted] = useState(false);

  useImperativeHandle(ref, () => ({
    startTour: () => {
      setRun(true);
    }
  }));

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;
    const token = localStorage.getItem("token");
    if (!token) return;
    const hasCompleted = localStorage.getItem(storageKey);
    if (!hasCompleted) {
      const timer = setTimeout(() => setRun(true), 2000);
      return () => clearTimeout(timer);
    }
  }, [mounted, storageKey]);

  const handleJoyrideCallback = (data: any) => {
    const { status, action } = data;
    if (status === "finished" || status === "skipped" || action === "close") {
      setRun(false);
      localStorage.setItem(storageKey, "true");
    }
  };

  if (!mounted) return null;

  return (
    <JoyrideComponent
      steps={steps}
      run={run}
      continuous
      showSkipButton
      showProgress
      styles={{
        options: {
          primaryColor: "#059669",
          textColor: "#0f172a",
          backgroundColor: "#ffffff",
          overlayColor: "rgba(0, 0, 0, 0.6)",
          zIndex: 10000,
        }
      }}
      callback={handleJoyrideCallback}
    />
  );
});
PageTour.displayName = "PageTour";
