"""Streamlit dashboard over e-commerce analytics marts."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "warehouse" / "ecommerce.db"


@st.cache_data(show_spinner=False)
def read_sql(query: str) -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)


def main() -> None:
    st.set_page_config(
        page_title="E-commerce Analytics Warehouse",
        page_icon="🛒",
        layout="wide",
    )
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.2rem; max-width: 1200px; }
        div[data-testid="stMetricValue"] { font-size: 1.35rem; }
        .footer-note {
            margin-top: 1.5rem;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            background: #f5f7f9;
            color: #4a5560;
            font-size: 0.88rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("E-commerce Analytics Warehouse")
    st.caption("SQL-first analytics · raw → staging → marts → quality gates → BI")
    st.caption("Dataset sintético para demo de portfolio — não são dados reais de cliente.")

    if not DB_PATH.exists():
        st.error("Warehouse não encontrado.")
        st.code("python -m src.run_warehouse", language="bash")
        st.stop()

    daily = read_sql("SELECT * FROM mart_daily_revenue ORDER BY date")
    by_cat = read_sql("SELECT * FROM mart_category_revenue ORDER BY revenue DESC")
    top_cust = read_sql("SELECT * FROM mart_top_customers ORDER BY revenue DESC LIMIT 15")
    fact_n = read_sql("SELECT COUNT(*) AS n, ROUND(SUM(item_revenue),2) AS revenue FROM fact_order_items")

    total_revenue = float(fact_n["revenue"].iloc[0] or 0)
    total_orders = int(daily["orders"].sum()) if len(daily) else 0
    avg_ticket = (total_revenue / total_orders) if total_orders else 0
    days = len(daily)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Revenue", f"${total_revenue:,.0f}")
    m2.metric("Orders", f"{total_orders:,}")
    m3.metric("Avg ticket", f"${avg_ticket:,.2f}")
    m4.metric("Days covered", f"{days}")

    with st.sidebar:
        st.header("Camadas")
        st.markdown("`raw_*` → `stg_*` → `dim_*` / `fact_*` / `mart_*`")
        st.divider()
        st.caption(f"DB: `{DB_PATH.name}`")

    daily["date"] = pd.to_datetime(daily["date"])
    fig_rev = px.line(
        daily,
        x="date",
        y="revenue",
        title="Receita diária (mart_daily_revenue)",
        template="plotly_white",
        labels={"date": "Data", "revenue": "Revenue (USD)"},
    )
    st.plotly_chart(fig_rev, use_container_width=True)

    left, right = st.columns(2)
    with left:
        fig_cat = px.bar(
            by_cat,
            x="category",
            y="revenue",
            title="Receita por categoria",
            template="plotly_white",
            text="revenue",
        )
        fig_cat.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        st.plotly_chart(fig_cat, use_container_width=True)
    with right:
        fig_orders = px.area(
            daily,
            x="date",
            y="orders",
            title="Pedidos por dia",
            template="plotly_white",
            labels={"orders": "Orders", "date": "Data"},
        )
        st.plotly_chart(fig_orders, use_container_width=True)

    st.subheader("Top clientes (mart_top_customers)")
    st.dataframe(
        top_cust,
        use_container_width=True,
        hide_index=True,
        column_config={
            "revenue": st.column_config.NumberColumn(format="$%.2f"),
            "orders": st.column_config.NumberColumn(format="%d"),
        },
    )

    if len(by_cat):
        top = by_cat.iloc[0]
        st.info(
            f"**Insight:** a categoria **{top['category']}** concentra "
            f"${top['revenue']:,.0f} de receita no recorte atual."
        )

    st.markdown(
        """
        <div class="footer-note">
          <strong>Como foi construído:</strong> extracts sintéticos → staging SQL →
          dimensões/fato/marts → data quality (FK, unicidade, reconciliação de receita) → BI.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
