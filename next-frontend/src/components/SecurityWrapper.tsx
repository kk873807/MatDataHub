"use client";

import { useEffect } from "react";

export function SecurityWrapper({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Prevent right-click context menu to deter casual scraping
    const handleContextMenu = (e: MouseEvent) => {
      e.preventDefault();
    };

    // Prevent text selection shortcuts (Ctrl+A)
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'a') {
        e.preventDefault();
      }
      // Deter basic DevTools shortcuts (F12, Ctrl+Shift+I)
      if (e.key === 'F12' || ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'i')) {
        e.preventDefault();
      }
    };

    document.addEventListener("contextmenu", handleContextMenu);
    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("contextmenu", handleContextMenu);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  return <div className="select-none">{children}</div>;
}
