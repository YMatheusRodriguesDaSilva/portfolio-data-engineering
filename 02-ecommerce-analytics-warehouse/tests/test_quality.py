from __future__ import annotations

import sqlite3

from src.data_quality import run_checks
from src.run_warehouse import run


def test_warehouse_quality_gates():
    db = run(n_customers=40, n_orders=80)
    assert db.exists()
    with sqlite3.connect(db) as conn:
        results = run_checks(conn)
        tables = {
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
    assert {
        "dim_customer",
        "dim_product",
        "fact_order_items",
        "mart_daily_revenue",
        "mart_category_revenue",
        "mart_top_customers",
    } <= tables
    assert results
    assert all(r.passed for r in results)


def test_cancelled_orders_not_in_fact():
    db = run(n_customers=30, n_orders=60)
    with sqlite3.connect(db) as conn:
        bad = conn.execute(
            "SELECT COUNT(*) FROM fact_order_items WHERE status = 'cancelled'"
        ).fetchone()[0]
    assert bad == 0
