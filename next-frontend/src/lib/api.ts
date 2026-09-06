// Centralized API configuration
// In production, set NEXT_PUBLIC_API_URL to your backend URL (e.g., https://matdatahub-api.onrender.com)
// In development, it falls back to localhost
export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
export const API = `${API_BASE}/api/v1`;
