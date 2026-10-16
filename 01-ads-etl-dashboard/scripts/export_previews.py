"""Export static chart previews for the GitHub README."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.metrics import compute_kpis  # noqa: E402
from src.pipeline import run  # noqa: E402

DB = ROOT / "data" / "processed" / "warehouse.db"
ASSETS = ROOT / "assets"
CHANNEL_LABELS = {"google_ads": "Google Ads", "meta_ads": "Meta Ads"}


def load_df() -> pd.DataFrame:
    query = """
        SELECT
            d.full_date AS date,
            ch.channel_name AS channel,
            c.campaign_name AS campaign,
            f.spend, f.impressions, f.clicks, f.conversions, f.revenue
        FROM fact_ads_performance f
        JOIN dim_date d ON d.date_id = f.date_id
        JOIN dim_channel ch ON ch.channel_id = f.channel_id
        JOIN dim_campaign c ON c.campaign_id = f.campaign_id
    """
    with sqlite3.connect(DB) as conn:
        df = pd.read_sql_query(query, conn)
    df["date"] = pd.to_datetime(df["date"])
    df["channel_label"] = df["channel"].map(CHANNEL_LABELS).fillna(df["channel"])
    return df


def main() -> None:
    if not DB.exists():
        run(days=90)

    ASSETS.mkdir(parents=True, exist_ok=True)
    df = load_df()
    kpis = compute_kpis(df)

    daily = (
        df.groupby("date", as_index=False)[["spend", "revenue"]].sum().sort_values("date")
    )
    fig_trend = px.line(
        daily,
        x="date",
        y=["spend", "revenue"],
        title="Spend vs Revenue",
        template="plotly_white",
        labels={"value": "USD", "variable": "Metric", "date": "Date"},
    )
    fig_trend.update_layout(legend_title_text="", title_x=0.02)

    by_channel = df.groupby("channel_label", as_index=False)["spend"].sum()
    fig_pie = px.pie(
        by_channel,
        names="channel_label",
        values="spend",
        title="Spend share by channel",
        hole=0.45,
        template="plotly_white",
    )
    fig_pie.update_layout(title_x=0.02)

    by_campaign = (
        df.groupby("campaign", as_index=False)[["spend", "conversions", "revenue"]]
        .sum()
        .sort_values("spend", ascending=False)
    )
    fig_bar = px.bar(
        by_campaign,
        x="campaign",
        y="spend",
        color="conversions",
        title="Spend by campaign",
        template="plotly_white",
    )
    fig_bar.update_layout(title_x=0.02)

    outputs = {
        "preview_trend.png": fig_trend,
        "preview_channel.png": fig_pie,
        "preview_campaign.png": fig_bar,
    }

    for name, fig in outputs.items():
        path = ASSETS / name
        try:
            fig.write_image(path, width=1200, height=520, scale=2)
            print(f"Wrote {path}")
        except Exception as exc:  # kaleido may be missing
            html_path = path.with_suffix(".html")
            fig.write_html(html_path, include_plotlyjs="cdn")
            print(f"PNG failed ({exc}); wrote {html_path} instead")

    summary = ASSETS / "kpi_summary.md"
    summary.write_text(
        "\n".join(
            [
                "# KPI snapshot (synthetic data)",
                "",
                f"- Spend: `${kpis['spend']:,.0f}`",
                f"- Revenue: `${kpis['revenue']:,.0f}`",
                f"- ROAS: `{kpis['roas']:.2f}x`",
                f"- CTR: `{kpis['ctr'] * 100:.2f}%`",
                f"- CPC: `${kpis['cpc']:.2f}`",
                f"- CPA: `${kpis['cpa']:.2f}`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote {summary}")


if __name__ == "__main__":
    main()
