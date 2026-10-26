"""
Single source of truth for the legal-document version the backend accepts.

Bump CURRENT_TERMS_VERSION on EVERY wording change to /terms or /privacy, in the
same commit as the text change, together with LEGAL_VERSION in
next-frontend/src/lib/legal.ts. Then tag that commit `legal-<version>` so the
exact wording behind each recorded acceptance can be shown later.

See docs/CBAM_Update_and_Maintenance_Guide.md, section "Legal document versioning".
"""

CURRENT_TERMS_VERSION = "2026-10-26"
