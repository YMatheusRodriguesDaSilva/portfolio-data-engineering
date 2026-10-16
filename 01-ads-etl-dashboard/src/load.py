"""Load layer: create schema and load dimensional tables into SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.config import DATA_PROCESSED, SCHEMA_SQL, WAREHOUSE_DB
from src.logging_config import get_logger

logger = get_logger("ads_etl.load")


def _apply_schema(conn: sqlite3.Connection) -> None:
    schema = Path(SCHEMA_SQL).read_text(encoding="utf-8")
    conn.executescript(schema)


def load(tables: dict[str, pd.DataFrame]) -> Path:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    if WAREHOUSE_DB.exists():
        WAREHOUSE_DB.unlink()

    with sqlite3.connect(WAREHOUSE_DB) as conn:
        _apply_schema(conn)
        for name, frame in tables.items():
            frame.to_sql(name, conn, if_exists="append", index=False)
        conn.commit()

        counts = {
            table: conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in tables
        }

    logger.info("Loaded warehouse → %s", WAREHOUSE_DB)
    for table, n in counts.items():
        logger.info("  %s: %s rows", table, n)
    return WAREHOUSE_DB
