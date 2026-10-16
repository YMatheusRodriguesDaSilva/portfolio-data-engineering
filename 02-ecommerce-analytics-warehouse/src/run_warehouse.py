"""Build warehouse: load raw → staging SQL → marts SQL → quality checks."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.data_quality import assert_all_passed
from src.generate_sample_data import generate

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
WAREHOUSE = ROOT / "data" / "warehouse" / "ecommerce.db"
STAGING_SQL = ROOT / "sql" / "staging.sql"
MARTS_SQL = ROOT / "sql" / "marts.sql"


def _load_raw(conn: sqlite3.Connection) -> None:
    mapping = {
        "raw_customers": RAW / "customers.csv",
        "raw_products": RAW / "products.csv",
        "raw_orders": RAW / "orders.csv",
        "raw_order_items": RAW / "order_items.csv",
    }
    for table, path in mapping.items():
        if not path.exists():
            raise FileNotFoundError(path)
        pd.read_csv(path).to_sql(table, conn, if_exists="replace", index=False)


def run() -> Path:
    generate()
    WAREHOUSE.parent.mkdir(parents=True, exist_ok=True)
    if WAREHOUSE.exists():
        WAREHOUSE.unlink()

    with sqlite3.connect(WAREHOUSE) as conn:
        print("Loading raw tables...")
        _load_raw(conn)

        print("Applying staging models...")
        conn.executescript(STAGING_SQL.read_text(encoding="utf-8"))

        print("Building marts...")
        conn.executescript(MARTS_SQL.read_text(encoding="utf-8"))

        print("Running data quality checks...")
        assert_all_passed(conn)
        conn.commit()

    print(f"Warehouse ready → {WAREHOUSE}")
    return WAREHOUSE


if __name__ == "__main__":
    run()
