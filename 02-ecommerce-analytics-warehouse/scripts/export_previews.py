"""Export chart previews for the GitHub README."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.run_warehouse import run  # noqa: E402

DB = ROOT / "data" / "warehouse" / "ecommerce.db"
ASSETS = ROOT / "assets"


def main() -> None:
    if not DB.exists():
        run()

    ASSETS.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB) as conn:
        daily = pd.read_sql_query("SELECT * FROM mart_daily_revenue ORDER BY date", conn)
        by_cat = pd.read_sql_query(
            "SELECT * FROM mart_category_revenue ORDER BY revenue DESC", conn
        )

    daily["date"] = pd.to_datetime(daily["date"])

    fig_daily = px.line(
        daily,
        x="date",
        y="revenue",
        title="Daily revenue",
        template="plotly_white",
    )
    fig_cat = px.bar(
        by_cat,
        x="category",
        y="revenue",
        title="Revenue by category",
        template="plotly_white",
    )
    fig_orders = px.area(
        daily,
        x="date",
        y="orders",
        title="Orders over time",
        template="plotly_white",
    )

    mapping = {
        "preview_daily_revenue.png": fig_daily,
        "preview_category.png": fig_cat,
        "preview_orders.png": fig_orders,
    }
    for name, fig in mapping.items():
        path = ASSETS / name
        try:
            fig.write_image(path, width=1200, height=520, scale=2)
            print(f"Wrote {path}")
        except Exception as exc:
            html = path.with_suffix(".html")
            fig.write_html(html, include_plotlyjs="cdn")
            print(f"PNG failed ({exc}); wrote {html}")


if __name__ == "__main__":
    main()
