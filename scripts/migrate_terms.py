import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
db_url = os.getenv("DATABASE_URL", "").strip()

conn = psycopg2.connect(db_url, connect_timeout=10)
conn.autocommit = True
cur = conn.cursor()

print("Terminating stale idle-in-transaction backends...", flush=True)
cur.execute("""
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE state = 'idle in transaction' 
  AND pid != pg_backend_pid();
""")
terminated = cur.fetchall()
print(f"Terminated {len(terminated)} stale connection(s).", flush=True)

print("Running ALTER TABLE on public.users...", flush=True)
cur.execute("SET lock_timeout = '10s';")
cur.execute("ALTER TABLE public.users ADD COLUMN IF NOT EXISTS terms_accepted_at TIMESTAMPTZ;")
cur.execute("ALTER TABLE public.users ADD COLUMN IF NOT EXISTS terms_version VARCHAR(50);")
print("ALTER TABLE executed successfully!", flush=True)

cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='users';")
cols = [r[0] for r in cur.fetchall()]
print(f"Columns in public.users: {cols}", flush=True)

cur.close()
conn.close()
