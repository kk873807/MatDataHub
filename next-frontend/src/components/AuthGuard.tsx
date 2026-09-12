"use client";
import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";

const PUBLIC_ROUTES = ["/", "/terms", "/privacy", "/contact", /* account is protected */];

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [isAuthorized, setIsAuthorized] = useState<boolean | null>(null);

  useEffect(() => {
    // If it's a public route, always allow
    if (PUBLIC_ROUTES.includes(pathname)) {
      setIsAuthorized(true);
      return;
    }

    // Check for token on protected routes
    const token = localStorage.getItem("token") || new URLSearchParams(window.location.search).get("t");
    if (!token) {
      router.replace("/?login=true");
    } else {
      setIsAuthorized(true);
    }
  }, [pathname, router]);

  if (isAuthorized === null && !PUBLIC_ROUTES.includes(pathname)) {
    return <div className="flex h-screen items-center justify-center bg-slate-50 dark:bg-slate-950 text-slate-500 dark:text-slate-400">Authenticating...</div>;
  }

  return <>{children}</>;
}
