"""Streamlit dashboard on top of the ads dimensional warehouse."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.metrics import compute_kpis  # noqa: E402

DB_PATH = ROOT / "data" / "processed" / "warehouse.db"

CHANNEL_LABELS = {
    "google_ads": "Google Ads",
    "meta_ads": "Meta Ads",
}


@st.cache_data(show_spinner=False)
def load_fact() -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()
    query = """
        SELECT
            d.full_date AS date,
            ch.channel_name AS channel,
            c.campaign_name AS campaign,
            c.objective,
            f.spend,
            f.impressions,
            f.clicks,
            f.conversions,
            f.revenue
        FROM fact_ads_performance f
        JOIN dim_date d ON d.date_id = f.date_id
        JOIN dim_channel ch ON ch.channel_id = f.channel_id
        JOIN dim_campaign c ON c.campaign_id = f.campaign_id
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)
    df["date"] = pd.to_datetime(df["date"])
    df["channel_label"] = df["channel"].map(CHANNEL_LABELS).fillna(df["channel"])
    return df


def apply_filters(
    df: pd.DataFrame,
    channels: list[str],
    campaigns: list[str],
    date_range,
) -> pd.DataFrame:
    filtered = df[df["channel"].isin(channels) & df["campaign"].isin(campaigns)].copy()
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]
    return filtered


def main() -> None:
    st.set_page_config(
        page_title="Ads Performance Dashboard",
        page_icon="📊",
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

    st.title("Ads Performance Dashboard")
    st.caption(
        "Camada analítica sobre o data warehouse dimensional · "
        "ETL (Python/SQL) → SQLite → Streamlit/Plotly"
    )
    st.caption("Dataset sintético para demo de portfolio — não são dados reais de cliente.")

    df = load_fact()
    if df.empty:
        st.error("Warehouse não encontrado.")
        st.code("python -m src.pipeline", language="bash")
        st.stop()

    channels = sorted(df["channel"].unique())
    campaigns = sorted(df["campaign"].unique())
    min_d, max_d = df["date"].min().date(), df["date"].max().date()

    with st.sidebar:
        st.header("Filtros")
        selected_channels = st.multiselect(
            "Canal",
            channels,
            default=channels,
            format_func=lambda c: CHANNEL_LABELS.get(c, c),
        )
        selected_campaigns = st.multiselect("Campanha", campaigns, default=campaigns)
        date_range = st.date_input(
            "Período",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
        )
        st.divider()
        st.markdown("**Modelo dimensional**")
        st.markdown(
            "`dim_date` · `dim_channel` · `dim_campaign` · `fact_ads_performance`"
        )

    if not selected_channels or not selected_campaigns:
        st.warning("Selecione ao menos um canal e uma campanha.")
        st.stop()

    filtered = apply_filters(df, selected_channels, selected_campaigns, date_range)
    if filtered.empty:
        st.warning("Nenhum dado para os filtros selecionados.")
        st.stop()

    metrics = compute_kpis(filtered)
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Spend", f"${metrics['spend']:,.0f}")
    m2.metric("Revenue", f"${metrics['revenue']:,.0f}")
    m3.metric("ROAS", f"{metrics['roas']:.2f}x")
    m4.metric("CTR", f"{metrics['ctr'] * 100:.2f}%")
    m5.metric("CPC", f"${metrics['cpc']:.2f}")
    m6.metric("CPA", f"${metrics['cpa']:.2f}")

    daily = (
        filtered.groupby("date", as_index=False)[["spend", "revenue", "clicks", "conversions"]]
        .sum()
        .sort_values("date")
    )
    fig_trend = px.line(
        daily,
        x="date",
        y=["spend", "revenue"],
        title="Spend vs Revenue ao longo do tempo",
        labels={"value": "USD", "variable": "Métrica", "date": "Data"},
        template="plotly_white",
    )
    fig_trend.update_layout(legend_title_text="")
    st.plotly_chart(fig_trend, use_container_width=True)

    left, right = st.columns(2)
    with left:
        by_channel = filtered.groupby("channel_label", as_index=False)["spend"].sum()
        fig_ch = px.pie(
            by_channel,
            names="channel_label",
            values="spend",
            title="Share de investimento por canal",
            hole=0.45,
            template="plotly_white",
        )
        st.plotly_chart(fig_ch, use_container_width=True)

    with right:
        by_campaign = (
            filtered.groupby("campaign", as_index=False)[["spend", "conversions", "revenue"]]
            .sum()
            .sort_values("spend", ascending=False)
        )
        fig_camp = px.bar(
            by_campaign,
            x="campaign",
            y="spend",
            color="conversions",
            title="Spend por campanha (cor = conversões)",
            template="plotly_white",
            labels={"spend": "Spend (USD)", "campaign": "Campanha", "conversions": "Conversões"},
        )
        st.plotly_chart(fig_camp, use_container_width=True)

    st.subheader("Performance por campanha")
    table = by_campaign.copy()
    table["ROAS"] = table.apply(
        lambda r: (r["revenue"] / r["spend"]) if r["spend"] else 0, axis=1
    )
    table["CPA"] = table.apply(
        lambda r: (r["spend"] / r["conversions"]) if r["conversions"] else 0, axis=1
    )
    st.dataframe(
        table.rename(
            columns={
                "campaign": "Campanha",
                "spend": "Spend",
                "conversions": "Conversões",
                "revenue": "Revenue",
            }
        ),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Spend": st.column_config.NumberColumn(format="$%.0f"),
            "Revenue": st.column_config.NumberColumn(format="$%.0f"),
            "ROAS": st.column_config.NumberColumn(format="%.2fx"),
            "CPA": st.column_config.NumberColumn(format="$%.2f"),
        },
    )

    best = table.sort_values("ROAS", ascending=False).iloc[0]
    st.info(
        f"**Insight:** a campanha **{best['campaign']}** lidera em ROAS "
        f"({best['ROAS']:.2f}x) no recorte atual."
    )

    st.markdown(
        """
        <div class="footer-note">
          <strong>Como foi construído:</strong> extract → transform → quality gates →
          load dimensional (dim_date, dim_channel, dim_campaign, fact_ads_performance) → BI.
          Dados gerados localmente para demonstração pública no GitHub.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
