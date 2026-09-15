"use client";
import { useState, useEffect } from "react";
import dynamic from "next/dynamic";

// Dynamically import Joyride to avoid SSR issues (it uses document/window)
const JoyrideComponent = dynamic(
  () => import("react-joyride").then((mod) => mod.Joyride),
  { ssr: false }
);

export function OnboardingTour() {
  const [run, setRun] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;

    // Only run the tour if the user is logged in
    const token = localStorage.getItem("token");
    if (!token) return;

    // Check if the user has already completed the tour
    const hasCompleted = localStorage.getItem("tourCompleted");
    if (!hasCompleted) {
      // Delay to ensure DOM elements with tour classes are rendered
      const timer = setTimeout(() => setRun(true), 2500);
      return () => clearTimeout(timer);
    }
  }, [mounted]);

  const handleJoyrideCallback = (data: any) => {
    const { status, action, type } = data;
    if (status === "finished" || status === "skipped" || action === "close" || type === "error") {
      setRun(false);
      if (type !== "error") {
        localStorage.setItem("tourCompleted", "true");
      }
    }
  };

  const steps = [
    {
      target: "body",
      content: "Welcome to MatDataHub! Let's take a quick 1-minute tour of your new AI-powered engineering platform.",
      placement: "center" as const,
      disableBeacon: true,
    },
    {
      target: ".tour-dashboard",
      content: "This is your Dashboard — a quick overview of your recent activity, quick actions, and workspace shortcuts.",
      placement: "bottom" as const,
    },
    {
      target: ".tour-materials",
      content: "The Material Database — search, filter, and explore 1000+ verified engineering materials with detailed property datasheets.",
      placement: "bottom" as const,
    },
    {
      target: ".tour-projects",
      content: "Engineering Workspaces — create projects, build multi-part Bill of Materials (BOM), and track total assembly weight, cost, and carbon footprint.",
      placement: "bottom" as const,
    },
    {
      target: ".tour-analytics",
      content: "Advanced Analytics — run side-by-side material comparisons, AI-powered substitutions, CBAM emissions modeling, and composite material synthesis.",
      placement: "bottom" as const,
    },
    {
      target: ".tour-ai-widget",
      content: "Your AI Engineering Assistant — click this button anytime to ask questions about material properties, standards, or get recommendations.",
      placement: "top" as const,
    },
    {
      target: ".tour-account",
      content: "Account & Settings — manage your profile, API keys, subscriptions, and custom enterprise materials. You're all set!",
      placement: "bottom-end" as const,
    },
  ];

  if (!mounted) return null;

  return (
    <JoyrideComponent
      steps={steps}
      run={run}
      continuous={true}
      options={{
        primaryColor: "#059669",
        textColor: "#0f172a",
        backgroundColor: "#ffffff",
        overlayColor: "rgba(0, 0, 0, 0.5)",
        zIndex: 10000,
        skipBeacon: true,
        buttons: ["back", "close", "primary", "skip"]
      }}
      onEvent={handleJoyrideCallback}
    />
  );
}
