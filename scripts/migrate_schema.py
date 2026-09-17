#!/usr/bin/env python3
"""
migrate_schema.py – Safely add new columns / tables for MatDataHub v2.

Adds:
  • New columns on the 'materials' table (data_type, poissons_ratio, etc.)
  • The 'material_sources' table
  • The 'material_price_links' table

Safe to run multiple times – every statement uses IF NOT EXISTS / exception guards.

Usage:
    python scripts/migrate_schema.py            # apply migrations
    python scripts/migrate_schema.py --dry-run  # show SQL without executing
"""

import os
import sys
import argparse
import logging
from datetime import datetime

# ---------------------------------------------------------------------------
# Path fix so `from app…` works when called from project root
# ---------------------------------------------------------------------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("migrate_schema")

# ---------------------------------------------------------------------------
# Column definitions to add to `materials`
# (column_name, column_type_sql)
# ---------------------------------------------------------------------------
NEW_MATERIAL_COLUMNS = [
    # Data quality
    ("data_type",                    "VARCHAR(20) DEFAULT 'experimental'"),
    ("verification_count",           "INTEGER DEFAULT 0"),
    ("cross_validated",              "BOOLEAN DEFAULT FALSE"),
    ("data_quality_score",           "FLOAT DEFAULT 0.0"),

    # Additional mechanical
    ("poissons_ratio",               "FLOAT"),
    ("fatigue_strength",             "FLOAT"),
    ("shear_modulus",                "FLOAT"),
    ("compressive_strength",         "FLOAT"),
    ("impact_strength",              "FLOAT"),
    ("creep_strength",               "FLOAT"),
    ("fracture_toughness",           "FLOAT"),

    # Thermal
    ("thermal_expansion_coefficient","FLOAT"),

    # Electrical / magnetic
    ("electrical_resistivity",       "FLOAT"),
    ("electrical_conductivity",      "FLOAT"),
    ("magnetic_permeability",        "FLOAT"),

    # Material characteristics
    ("corrosion_resistance",         "VARCHAR(200)"),
    ("machinability_rating",         "FLOAT"),
    ("weldability",                  "VARCHAR(100)"),
    ("biocompatibility",             "VARCHAR(200)"),
    ("crystal_structure",            "VARCHAR(50)"),

    # International standards
    ("uns_number",                   "VARCHAR(20)"),
    ("en_number",                    "VARCHAR(50)"),
    ("jis_number",                   "VARCHAR(50)"),
    ("din_number",                   "VARCHAR(50)"),
    ("is_number",                    "VARCHAR(50)"),
    ("gb_number",                    "VARCHAR(50)"),

    # ESG
    ("embodied_carbon",              "FLOAT"),
    ("recyclability_index",          "FLOAT"),
    ("is_obsolete",                  "BOOLEAN DEFAULT FALSE"),
    ("replacement_standard",         "VARCHAR(200)"),
]

# ---------------------------------------------------------------------------
# Table creation statements
# ---------------------------------------------------------------------------
CREATE_MATERIAL_SOURCES = """
CREATE TABLE IF NOT EXISTS material_sources (
    id              SERIAL PRIMARY KEY,
    material_id     INTEGER NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    source_type     VARCHAR(50)  NOT NULL,
    source_name     VARCHAR(200) NOT NULL,
    source_url      VARCHAR(1000),
    source_doi      VARCHAR(200),
    source_isbn     VARCHAR(50),
    access_type     VARCHAR(20) DEFAULT 'free',
    confidence_score FLOAT DEFAULT 1.0,
    notes           TEXT,
    date_accessed   TIMESTAMPTZ DEFAULT NOW()
);
"""

CREATE_MATERIAL_SOURCES_INDEXES = [
    "CREATE INDEX IF NOT EXISTS ix_material_sources_material_id ON material_sources(material_id);",
    "CREATE INDEX IF NOT EXISTS ix_material_sources_material_id_type ON material_sources(material_id, source_type);",
]

CREATE_MATERIAL_PRICE_LINKS = """
CREATE TABLE IF NOT EXISTS material_price_links (
    id                SERIAL PRIMARY KEY,
    material_id       INTEGER NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    price_source_name VARCHAR(200) NOT NULL,
    price_source_url  VARCHAR(1000),
    price_type        VARCHAR(50)  DEFAULT 'market',
    price_per_kg      FLOAT,
    price_currency    VARCHAR(3)   DEFAULT 'INR',
    price_date        TIMESTAMPTZ,
    access_type       VARCHAR(20)  DEFAULT 'free',
    notes             TEXT,
    created_at        TIMESTAMPTZ  DEFAULT NOW()
);
"""

CREATE_MATERIAL_PRICE_LINKS_INDEXES = [
    "CREATE INDEX IF NOT EXISTS ix_material_price_links_material_id ON material_price_links(material_id);",
]


def _add_column_safe(conn, table: str, col_name: str, col_type: str, dry_run: bool):
    """Add a column only if it does not exist (PostgreSQL-specific)."""
    sql = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_name = '{table}' AND column_name = '{col_name}'
        ) THEN
            ALTER TABLE {table} ADD COLUMN {col_name} {col_type};
        END IF;
    END $$;
    """
    if dry_run:
        log.info("[DRY-RUN] Would add column %s.%s  (%s)", table, col_name, col_type)
    else:
        conn.execute(text(sql))
        log.info("  [OK] column %s.%s ensured", table, col_name)


def run_migration(dry_run: bool = False):
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    if not DATABASE_URL:
        log.error("DATABASE_URL is not set in .env – aborting.")
        sys.exit(1)

    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    log.info("=" * 60)
    log.info("MatDataHub Schema Migration  (%s)", datetime.now().isoformat())
    log.info("=" * 60)

    with engine.begin() as conn:
        # --- 1. New columns on materials ---------------------------------
        log.info(">> Step 1/3 - Adding new columns to 'materials' table ...")
        for col_name, col_type in NEW_MATERIAL_COLUMNS:
            _add_column_safe(conn, "materials", col_name, col_type, dry_run)

        # Add index on data_type if missing
        if not dry_run:
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS ix_materials_data_type ON materials(data_type);"
            ))
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS ix_materials_uns_number ON materials(uns_number);"
            ))
        log.info("  [OK] materials columns done")

        # --- 2. material_sources table -----------------------------------
        log.info(">> Step 2/3 - Creating 'material_sources' table ...")
        if dry_run:
            log.info("[DRY-RUN] Would create material_sources table")
        else:
            conn.execute(text(CREATE_MATERIAL_SOURCES))
            for idx_sql in CREATE_MATERIAL_SOURCES_INDEXES:
                conn.execute(text(idx_sql))
        log.info("  [OK] material_sources done")

        # --- 3. material_price_links table -------------------------------
        log.info(">> Step 3/3 - Creating 'material_price_links' table ...")
        if dry_run:
            log.info("[DRY-RUN] Would create material_price_links table")
        else:
            conn.execute(text(CREATE_MATERIAL_PRICE_LINKS))
            for idx_sql in CREATE_MATERIAL_PRICE_LINKS_INDEXES:
                conn.execute(text(idx_sql))
        log.info("  [OK] material_price_links done")

    log.info("=" * 60)
    log.info("Migration complete. All changes applied successfully.")
    log.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="MatDataHub schema migration")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print SQL operations without executing")
    args = parser.parse_args()
    run_migration(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
