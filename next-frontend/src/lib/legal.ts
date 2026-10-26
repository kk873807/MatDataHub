// Single source of truth for the Terms of Service / Privacy Policy version.
//
// Bump BOTH values on EVERY wording change to /terms or /privacy, in the same
// commit as the text change, together with CURRENT_TERMS_VERSION in app/legal.py.
// Then tag the commit `legal-<LEGAL_VERSION>` and push the tag.
//
// Do not render `new Date()` as the "last updated" date: pages are prerendered,
// so that shows the build date, not the date the wording changed.
export const LEGAL_VERSION = "2026-10-26";
export const LEGAL_LAST_UPDATED = "26 October 2026";
