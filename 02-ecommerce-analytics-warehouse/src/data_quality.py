"""Data quality checks for marts."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from src.logging_config import get_logger

logger = get_logger("ecom_wh.quality")


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


def run_checks(conn: sqlite3.Connection) -> list[CheckResult]:
    results: list[CheckResult] = []

    def q(sql: str):
        return conn.execute(sql).fetchone()[0]

    null_emails = q("SELECT COUNT(*) FROM dim_customer WHERE email IS NULL OR email = ''")
    results.append(
        CheckResult("dim_customer_email_not_null", null_emails == 0, f"null/blank emails={null_emails}")
    )

    dup_customers = q(
        "SELECT COUNT(*) FROM (SELECT email, COUNT(*) c FROM dim_customer GROUP BY email HAVING c > 1)"
    )
    results.append(
        CheckResult("dim_customer_email_unique", dup_customers == 0, f"duplicate emails={dup_customers}")
    )

    orphan_products = q(
        """
        SELECT COUNT(*) FROM fact_order_items f
        LEFT JOIN dim_product p ON p.product_id = f.product_id
        WHERE p.product_id IS NULL
        """
    )
    results.append(
        CheckResult("fact_product_fk", orphan_products == 0, f"orphan product rows={orphan_products}")
    )

    orphan_customers = q(
        """
        SELECT COUNT(*) FROM fact_order_items f
        LEFT JOIN dim_customer c ON c.customer_id = f.customer_id
        WHERE c.customer_id IS NULL
        """
    )
    results.append(
        CheckResult("fact_customer_fk", orphan_customers == 0, f"orphan customer rows={orphan_customers}")
    )

    neg_revenue = q("SELECT COUNT(*) FROM fact_order_items WHERE item_revenue < 0")
    results.append(
        CheckResult("fact_revenue_non_negative", neg_revenue == 0, f"negative revenue rows={neg_revenue}")
    )

    cancelled_in_fact = q(
        "SELECT COUNT(*) FROM fact_order_items WHERE status NOT IN ('paid', 'shipped', 'delivered')"
    )
    results.append(
        CheckResult(
            "fact_excludes_cancelled",
            cancelled_in_fact == 0,
            f"invalid status rows={cancelled_in_fact}",
        )
    )

    mart_rows = q("SELECT COUNT(*) FROM mart_daily_revenue")
    results.append(CheckResult("mart_daily_revenue_not_empty", mart_rows > 0, f"rows={mart_rows}"))

    category_rows = q("SELECT COUNT(*) FROM mart_category_revenue")
    results.append(
        CheckResult("mart_category_revenue_not_empty", category_rows > 0, f"rows={category_rows}")
    )

    # revenue reconciliation: sum(fact) ~= sum(daily mart)
    fact_rev = q("SELECT ROUND(SUM(item_revenue), 2) FROM fact_order_items")
    mart_rev = q("SELECT ROUND(SUM(revenue), 2) FROM mart_daily_revenue")
    results.append(
        CheckResult(
            "revenue_reconciles_daily_mart",
            abs(float(fact_rev or 0) - float(mart_rev or 0)) < 0.01,
            f"fact={fact_rev} daily_mart={mart_rev}",
        )
    )

    return results


def assert_all_passed(conn: sqlite3.Connection) -> None:
    results = run_checks(conn)
    failed = [r for r in results if not r.passed]
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        logger.info("[%s] %s — %s", status, r.name, r.detail)
    if failed:
        raise AssertionError(f"{len(failed)} data quality checks failed")
