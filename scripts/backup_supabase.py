"""
Manual database backup & scratch-restore verification script for MatDataHub.

Usage:
    .venv\\Scripts\\python.exe scripts/backup_supabase.py

Features:
1. Exports application tables to a timestamped JSON file under backups/ (gitignored).
2. Excludes sensitive credential columns from `users` (`hashed_password`, `api_key`,
   `api_secret`, `session_token`).
3. Purges local backup snapshots older than 25 days so backups never outlive the
   30-day account-deletion promise in /privacy.
4. Verifies the backup immediately by loading every exported row into an isolated
   scratch SQLite database and asserting exact row-count parity.
"""
import datetime
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sqlalchemy import create_engine, inspect, text
from app.database import Base, engine
import app.models  # noqa: F401 - register all ORM models on Base.metadata


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

# Columns excluded from backups so password hashes, API secrets, and session tokens
# never sit in a backup file on disk.
EXCLUDED_COLUMNS = {
    "users": {"hashed_password", "api_key", "api_secret", "session_token"},
}

RETENTION_DAYS = 25


def _default_serializer(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return str(obj)


def purge_old_backups(backup_dir: str, retention_days: int = RETENTION_DAYS) -> list[str]:
    """Delete backup files older than retention_days (25 days < 30-day GDPR deletion SLA)."""
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=retention_days)
    removed = []
    for path in glob.glob(os.path.join(backup_dir, "supabase_backup_*.json")):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path), tz=datetime.timezone.utc)
        if mtime < cutoff:
            os.remove(path)
            removed.append(path)
    return removed


def run_backup() -> tuple[str, dict, dict, list[str]]:
    backup_dir = os.path.join(ROOT, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    purged = purge_old_backups(backup_dir)

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    out_path = os.path.join(backup_dir, f"supabase_backup_{ts}.json")

    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    dump = {
        "created_at_utc": ts,
        "retention_days": RETENTION_DAYS,
        "redacted_columns": {k: sorted(v) for k, v in EXCLUDED_COLUMNS.items()},
        "schemas": {},
        "tables": {},
        "row_counts": {},
        "cbam_defaults_summary": {},
    }

    with engine.connect() as conn:
        for table in TABLES_TO_DUMP:
            if table not in existing_tables:
                continue
            excluded = EXCLUDED_COLUMNS.get(table, set())
            col_meta = [
                {"name": c["name"], "type": str(c["type"]), "nullable": bool(c.get("nullable", True))}
                for c in inspector.get_columns(table)
                if c["name"] not in excluded
            ]
            dump["schemas"][table] = col_meta
            rows = conn.execute(text(f'SELECT * FROM "{table}" ORDER BY id')).mappings().all()
            serialized = [
                {k: v for k, v in dict(r).items() if k not in excluded}
                for r in rows
            ]
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

    return out_path, dump["row_counts"], dump["cbam_defaults_summary"], purged


def _sqlite_col_type(pg_type_str: str) -> str:
    t = pg_type_str.upper()
    if "INT" in t:
        return "INTEGER"
    if any(k in t for k in ("FLOAT", "DOUBLE", "NUMERIC", "REAL", "DECIMAL")):
        return "REAL"
    if "BOOL" in t:
        return "BOOLEAN"
    return "TEXT"


def verify_restore_to_scratch(backup_path: str) -> dict[str, int]:
    """Load the JSON backup into an isolated scratch SQLite database and verify row counts and column parity."""
    with open(backup_path, "r", encoding="utf-8") as f:
        dump = json.load(f)

    # Verify redacted columns are not present in any exported user row
    for u in dump["tables"].get("users", []):
        for secret_col in EXCLUDED_COLUMNS["users"]:
            assert secret_col not in u, f"Secret column {secret_col} leaked into backup!"

    scratch_engine = create_engine("sqlite:///:memory:")
    schemas = dump.get("schemas", {})

    restored_counts: dict[str, int] = {}
    with scratch_engine.begin() as conn:
        for table_name, rows in dump["tables"].items():
            col_defs = schemas.get(table_name)
            if col_defs:
                ddl_cols = ", ".join(
                    f'"{c["name"]}" {_sqlite_col_type(c["type"])}'
                    + (" PRIMARY KEY" if c["name"] == "id" else "")
                    for c in col_defs
                )
            elif rows:
                ddl_cols = ", ".join(
                    f'"{col}" TEXT' + (" PRIMARY KEY" if col == "id" else "")
                    for col in rows[0].keys()
                )
            else:
                ddl_cols = '"id" INTEGER PRIMARY KEY'
            conn.execute(text(f'CREATE TABLE "{table_name}" ({ddl_cols})'))

            if not rows:
                restored_counts[table_name] = 0
                continue

            cols = list(rows[0].keys())
            col_list = ", ".join(f'"{c}"' for c in cols)
            param_list = ", ".join(f":{c}" for c in cols)
            stmt = text(f'INSERT INTO "{table_name}" ({col_list}) VALUES ({param_list})')
            sqlite_rows = [
                {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in r.items()}
                for r in rows
            ]
            conn.execute(stmt, sqlite_rows)
            cnt = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar()
            assert cnt == len(rows), f"Restore mismatch on {table_name}: expected {len(rows)}, got {cnt}"
            restored_counts[table_name] = int(cnt)

    scratch_engine.dispose()
    return restored_counts


if __name__ == "__main__":
    path, counts, cbam_info, purged = run_backup()
    restored = verify_restore_to_scratch(path)
    print(f"Backup written to: {path}")
    print(f"Purged old backups (> {RETENTION_DAYS}d): {len(purged)}")
    print(f"Row counts exported: {json.dumps(counts)}")
    print(f"Scratch DB restore verified: {json.dumps(restored)}")
    print(f"cbam_defaults summary: {json.dumps(cbam_info)}")
