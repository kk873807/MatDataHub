"use client";

import { useEffect } from "react";

export function SecurityWrapper({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Prevent right-click context menu to deter casual scraping, but allow on inputs
    const handleContextMenu = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (target.tagName !== 'INPUT' && target.tagName !== 'TEXTAREA') {
        e.preventDefault();
      }
    };

    // Prevent text selection shortcuts (Ctrl+A), but allow inside inputs
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      const isInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable;
      
      if (!isInput && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'a') {
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

  // Removed global 'select-none' which breaks input highlighting
  return <div>{children}</div>;
}
