"use client";
import { useState, useEffect } from "react";
import { Joyride, STATUS } from "react-joyride";
import { usePathname } from "next/navigation";

export function OnboardingTour() {
  const [run, setRun] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    // Only run the tour if the user is logged in (not on landing page)
    if (pathname === "/") return;
    
    // Check if the user has already completed the tour
    const hasCompleted = localStorage.getItem("tourCompleted");
    if (!hasCompleted) {
      // Small delay to ensure UI is rendered
      setTimeout(() => setRun(true), 1500);
    }
  }, [pathname]);

  const handleJoyrideCallback = (data: any) => {
    const { status } = data;
    const finishedStatuses: string[] = [STATUS.FINISHED, STATUS.SKIPPED];

    if (finishedStatuses.includes(status)) {
      setRun(false);
      localStorage.setItem("tourCompleted", "true");
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
      content: "This is your Dashboard. It gives you a quick overview of your recent activity and quick actions.",
      placement: "bottom" as const,
    },
    {
      target: ".tour-materials",
      content: "The Material Database is where you can search, compare, and filter through 1000+ verified engineering materials.",
      placement: "bottom" as const,
    },
    {
      target: ".tour-projects",
      content: "Workspaces! This is the most powerful feature. Here you can create projects, build multi-part Bill of Materials (BOM), and track total assembly weights, costs, and carbon footprints.",
      placement: "bottom" as const,
    },
    {
      target: ".tour-analytics",
      content: "Run advanced calculations like CBAM emissions modeling and deep multi-material radar comparisons.",
      placement: "bottom" as const,
    },
    {
      target: ".tour-ai-widget",
      content: "Stuck? Need a specific standard? Our specialized Engineering AI is always available right here to chat and help you find exact material properties.",
      placement: "left" as const,
    },
    {
      target: ".tour-account",
      content: "Manage your API keys, subscriptions, and custom enterprise materials in your Account settings. You're all set!",
      placement: "bottom-end" as const,
    }
  ];

  return (
    <Joyride
      steps={steps}
      run={run}
      continuous
      
      
      
      onEvent={handleJoyrideCallback}
      
    />
  );
}
