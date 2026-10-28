"""
Manual database backup script for MatDataHub (Supabase PostgreSQL -> local JSON dump).

Usage:
    .venv\\Scripts\\python.exe scripts/backup_supabase.py

Creates a timestamped backup under backups/ (which is gitignored) containing all
application tables (users, materials, custom_materials, bom_analyses, transactions,
upgrade_requests, feedback, projects, project_items, saved_materials, blogs) plus
the row count and latest timestamp of cbam_defaults.
"""
import datetime
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sqlalchemy import inspect, text
from app.database import engine


TABLES_TO_DUMP = [
    "users",
    "materials",
    "custom_materials",
    "bom_analyses",
    "transactions",
    "upgrade_requests",
    "feedback",
    "projects",
    "project_items",
    "saved_materials",
    "blogs",
]


def _default_serializer(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return str(obj)


def run_backup() -> str:
    backup_dir = os.path.join(ROOT, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    out_path = os.path.join(backup_dir, f"supabase_backup_{ts}.json")

    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    dump = {
        "created_at_utc": ts,
        "tables": {},
        "row_counts": {},
        "cbam_defaults_summary": {},
    }

    with engine.connect() as conn:
        for table in TABLES_TO_DUMP:
            if table not in existing_tables:
                continue
            rows = conn.execute(text(f'SELECT * FROM "{table}" ORDER BY id')).mappings().all()
            serialized = [dict(r) for r in rows]
            dump["tables"][table] = serialized
            dump["row_counts"][table] = len(serialized)

        if "cbam_defaults" in existing_tables:
            row = conn.execute(
                text("SELECT COUNT(*) AS cnt, MAX(updated_at) AS max_updated FROM cbam_defaults")
            ).mappings().first()
            dump["cbam_defaults_summary"] = {
                "count": row["cnt"] if row else 0,
                "max_updated_at": _default_serializer(row["max_updated"]) if row and row["max_updated"] else None,
            }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dump, f, indent=2, default=_default_serializer)

    return out_path, dump["row_counts"], dump["cbam_defaults_summary"]


if __name__ == "__main__":
    path, counts, cbam_info = run_backup()
    print(f"Backup written to: {path}")
    print(f"Row counts: {json.dumps(counts)}")
    print(f"cbam_defaults: {json.dumps(cbam_info)}")
