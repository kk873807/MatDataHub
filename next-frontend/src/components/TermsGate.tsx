"use client";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { API } from "@/lib/api";
import { LEGAL_VERSION, LEGAL_LAST_UPDATED } from "@/lib/legal";

// Blocks a signed-in user until the server holds an acceptance of the current
// Terms/Privacy version. Covers Google sign-ups (which never see the register
// checkbox), accounts created before versioning, and anyone who accepted an
// older version. The acceptance time is set by the server, not by this page.
const SKIP_ROUTES = ["/terms", "/privacy"];

export function TermsGate() {
  const pathname = usePathname();
  const [needsAcceptance, setNeedsAcceptance] = useState(false);
  const [hadEarlierVersion, setHadEarlierVersion] = useState(false);
  const [checked, setChecked] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (SKIP_ROUTES.includes(pathname)) return;
    const urlToken = typeof window !== "undefined" ? new URLSearchParams(window.location.search).get("t") : null;
    const token = localStorage.getItem("token") || urlToken;
    if (!token) {
      setNeedsAcceptance(false);
      return;
    }
    fetch(`${API}/auth/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => (r.ok ? r.json() : null))
      .then(data => {
        if (!data) return;
        // Only gate when the backend reports the field and serves the same
        // version this frontend shows; otherwise a deploy is mid-flight and
        // an acceptance could not be recorded against the text on screen.
        if (data.terms_current === false && data.current_terms_version === LEGAL_VERSION) {
          setHadEarlierVersion(Boolean(data.terms_version));
          setNeedsAcceptance(true);
        } else {
          setNeedsAcceptance(false);
        }
      })
      .catch(() => {});
  }, [pathname]);

  if (!needsAcceptance || SKIP_ROUTES.includes(pathname)) return null;

  const accept = async () => {
    setError("");
    setSaving(true);
    try {
      const res = await fetch(`${API}/auth/accept-terms`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({ terms_version: LEGAL_VERSION }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.status === 409) {
        setError("Our Terms of Service were updated since you opened this tab. Please refresh the page to accept the latest version.");
        return;
      }
      if (!res.ok) throw new Error(data.detail || "Could not record your acceptance. Please refresh the page and try again.");
      setNeedsAcceptance(false);
    } catch (e: any) {
      setError(e?.message || "Could not record your acceptance. Please refresh the page and try again.");
    } finally {
      setSaving(false);
    }
  };

  const signOut = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 w-full max-w-md rounded-2xl shadow-2xl p-8">
        <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-2">
          {hadEarlierVersion ? "Our Terms have changed" : "Please accept our Terms"}
        </h2>
        <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
          {hadEarlierVersion
            ? `We updated the Terms of Service and Privacy Policy on ${LEGAL_LAST_UPDATED}. Please review and accept them to keep using MatDataHub.`
            : "Before you continue, please review and accept the Terms of Service and Privacy Policy."}
        </p>

        {error && (
          <div className="bg-red-500/10 border border-red-500/50 text-red-500 text-sm p-3 rounded-xl mb-4">
            <div>{error}</div>
            {error.toLowerCase().includes("refresh") && (
              <button
                type="button"
                onClick={() => window.location.reload()}
                className="mt-2 inline-block text-xs font-semibold underline hover:text-red-400"
              >
                Refresh page now
              </button>
            )}
          </div>
        )}

        <div className="flex items-start gap-2.5 mb-6 text-left">
          <input
            type="checkbox"
            id="gate-terms"
            checked={checked}
            onChange={e => setChecked(e.target.checked)}
            className="mt-1 h-4 w-4 rounded border-slate-300 dark:border-slate-700 text-blue-600 focus:ring-blue-500 cursor-pointer flex-shrink-0"
          />
          <label htmlFor="gate-terms" className="text-xs text-slate-600 dark:text-slate-400 leading-snug cursor-pointer select-none">
            I agree to the{" "}
            <a href="/terms" target="_blank" rel="noopener noreferrer" className="text-blue-600 dark:text-blue-400 underline font-medium">Terms of Service</a>{" "}
            and{" "}
            <a href="/privacy" target="_blank" rel="noopener noreferrer" className="text-blue-600 dark:text-blue-400 underline font-medium">Privacy Policy</a>
            {" "}(version {LEGAL_VERSION}). I understand that all CBAM calculations are preliminary estimates and not official compliance declarations.
          </label>
        </div>

        <button
          type="button"
          onClick={accept}
          disabled={!checked || saving}
          className="w-full bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 text-white font-bold py-3 rounded-xl transition-colors disabled:opacity-50"
        >
          {saving ? "Saving..." : "Accept and continue"}
        </button>
        <button
          type="button"
          onClick={signOut}
          className="w-full mt-3 text-sm text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
        >
          Sign out instead
        </button>
      </div>
    </div>
  );
}
