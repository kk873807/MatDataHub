import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# We completely rewrite the file.
new_content = '''"use client";
import { useState, useEffect } from "react";
import { ShieldAlert, Check, X, Lock, Users, MessageSquare, FileText, Plus, Database, ShieldCheck } from "lucide-react";
import { API } from "@/lib/api";
import MaterialManager from "@/components/MaterialManager";
import BlogEditor from "@/components/BlogEditor";

export default function AdminDashboard() {
  const [authed, setAuthed] = useState(false);
  const [profile, setProfile] = useState<any>(null);
  const [secret, setSecret] = useState("");
  const [requests, setRequests] = useState<any[]>([]);
  const [feedback, setFeedback] = useState<any[]>([]);
  const [contributions, setContributions] = useState<any[]>([]);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedUsers, setExpandedUsers] = useState<Record<number, boolean>>({});
  const toggleExpand = (userId: number) => setExpandedUsers(prev => ({ ...prev, [userId]: !prev[userId] }));

  useEffect(() => {
    checkAdmin();
  }, []);

  const checkAdmin = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }
    
    try {
      const res = await fetch(`${API}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
        if (data.is_admin) {
          setAuthed(true);
          fetchAdminData(token);
        }
      }
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleClaimAdmin = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    try {
      const res = await fetch(`${API}/auth/make-me-admin`, {
        method: "POST",
        headers: { "X-Admin-Secret": secret, "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        window.location.reload();
      } else {
        setError("Invalid system secret.");
      }
    } catch (e) {
      setError("Network error");
    }
  };

  const fetchAdminData = async (token: string) => {
    try {
      const [reqRes, feedRes, contribRes, txnRes] = await Promise.all([
        fetch(`${API}/admin/upgrade-requests`, { headers: { "Authorization": `Bearer ${token}` } }),
        fetch(`${API}/feedback/`, { headers: { "Authorization": `Bearer ${token}` } }),
        fetch(`${API}/admin/user-contributions`, { headers: { "Authorization": `Bearer ${token}` } }),
        fetch(`${API}/admin/transactions`, { headers: { "Authorization": `Bearer ${token}` } })
      ]);

      if (reqRes.ok) setRequests(await reqRes.json());
      if (feedRes.ok) setFeedback(await feedRes.json());
      if (contribRes.ok) {
        const c = await contribRes.json();
        setContributions(c.users || []);
      }
      if (txnRes.ok) setTransactions(await txnRes.json());
    } catch (err) {
      console.error("Failed to fetch admin data", err);
    }
  };

  // ... (REST OF UI LOGIC)
'''

# Wait, I can't just replace the top half easily with regex because the bottom half is huge.
# I will use a python script to read, find the exact functions, and replace them.
