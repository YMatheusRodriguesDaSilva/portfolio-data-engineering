"""Build warehouse: load raw → staging SQL → marts SQL → quality checks."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

from src.data_quality import assert_all_passed
from src.generate_sample_data import generate
from src.logging_config import get_logger

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
WAREHOUSE = ROOT / "data" / "warehouse" / "ecommerce.db"
STAGING_SQL = ROOT / "sql" / "staging.sql"
MARTS_SQL = ROOT / "sql" / "marts.sql"

logger = get_logger("ecom_wh.pipeline")


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
        n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        logger.info("  %s: %s rows", table, n)


def run(
    n_customers: int = 120,
    n_orders: int = 400,
    skip_generate: bool = False,
) -> Path:
    if not skip_generate:
        logger.info("1/4 Generating synthetic e-commerce extracts...")
        generate(n_customers=n_customers, n_orders=n_orders)
    else:
        logger.info("1/4 Skipping generation (reusing data/raw)")

    WAREHOUSE.parent.mkdir(parents=True, exist_ok=True)
    if WAREHOUSE.exists():
        WAREHOUSE.unlink()

    with sqlite3.connect(WAREHOUSE) as conn:
        logger.info("2/4 Loading raw tables...")
        _load_raw(conn)

        logger.info("3/4 Applying staging + marts SQL models...")
        conn.executescript(STAGING_SQL.read_text(encoding="utf-8"))
        conn.executescript(MARTS_SQL.read_text(encoding="utf-8"))

        logger.info("4/4 Running data quality checks...")
        assert_all_passed(conn)
        conn.commit()

        summary = conn.execute(
            """
            SELECT
              (SELECT COUNT(*) FROM dim_customer),
              (SELECT COUNT(*) FROM dim_product),
              (SELECT COUNT(*) FROM fact_order_items),
              (SELECT ROUND(SUM(revenue), 2) FROM mart_daily_revenue)
            """
        ).fetchone()

    logger.info(
        "Warehouse ready → %s | customers=%s products=%s fact_rows=%s revenue=$%s",
        WAREHOUSE,
        summary[0],
        summary[1],
        summary[2],
        summary[3],
    )
    return WAREHOUSE


def main() -> None:
    parser = argparse.ArgumentParser(description="Build e-commerce analytics warehouse")
    parser.add_argument("--customers", type=int, default=120)
    parser.add_argument("--orders", type=int, default=400)
    parser.add_argument(
        "--skip-generate",
        action="store_true",
        help="Reuse existing CSV files in data/raw",
    )
    args = parser.parse_args()
    run(
        n_customers=args.customers,
        n_orders=args.orders,
        skip_generate=args.skip_generate,
    )


if __name__ == "__main__":
    main()
