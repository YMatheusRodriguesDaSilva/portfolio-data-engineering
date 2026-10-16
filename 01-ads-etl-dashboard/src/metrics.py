"""Shared KPI calculations (pipeline reports + dashboard)."""

from __future__ import annotations

import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict[str, float]:
    spend = float(df["spend"].sum()) if len(df) else 0.0
    clicks = float(df["clicks"].sum()) if len(df) else 0.0
    impressions = float(df["impressions"].sum()) if len(df) else 0.0
    conversions = float(df["conversions"].sum()) if len(df) else 0.0
    revenue = float(df["revenue"].sum()) if len(df) else 0.0
    return {
        "spend": spend,
        "impressions": impressions,
        "clicks": clicks,
        "conversions": conversions,
        "revenue": revenue,
        "ctr": (clicks / impressions) if impressions else 0.0,
        "cpc": (spend / clicks) if clicks else 0.0,
        "cpa": (spend / conversions) if conversions else 0.0,
        "roas": (revenue / spend) if spend else 0.0,
    }
