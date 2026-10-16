"""Transform layer: clean, type, and prepare dimensional payloads."""

from __future__ import annotations

import pandas as pd


def transform(raw: pd.DataFrame) -> dict[str, pd.DataFrame]:
    df = raw.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if df["date"].isna().any():
        raise ValueError("Invalid dates found in raw extract")

    numeric_cols = ["spend", "impressions", "clicks", "conversions", "revenue"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Business rules / data quality
    df = df[df["impressions"] >= 0]
    df = df[df["clicks"] <= df["impressions"]]
    df["channel"] = df["channel"].str.strip().str.lower()
    df["campaign_name"] = df["campaign_name"].str.strip()
    df["objective"] = df["objective"].str.strip()
    df["status"] = df["status"].str.upper().str.strip()

    dim_date = (
        df[["date"]]
        .drop_duplicates()
        .assign(
            date_id=lambda x: x["date"].dt.strftime("%Y%m%d").astype(int),
            full_date=lambda x: x["date"].dt.strftime("%Y-%m-%d"),
            year=lambda x: x["date"].dt.year,
            month=lambda x: x["date"].dt.month,
            day=lambda x: x["date"].dt.day,
            week_of_year=lambda x: x["date"].dt.isocalendar().week.astype(int),
            day_name=lambda x: x["date"].dt.day_name(),
        )
        .drop(columns=["date"])
        .sort_values("date_id")
        .reset_index(drop=True)
    )

    channel_map = {
        "google_ads": (1, "Search/Performance"),
        "meta_ads": (2, "Social"),
    }
    dim_channel = pd.DataFrame(
        [
            {
                "channel_id": channel_map[ch][0],
                "channel_name": ch,
                "channel_type": channel_map[ch][1],
            }
            for ch in sorted(df["channel"].unique())
            if ch in channel_map
        ]
    )

    dim_campaign = (
        df[["campaign_name", "objective", "status"]]
        .drop_duplicates()
        .sort_values("campaign_name")
        .reset_index(drop=True)
        .assign(campaign_id=lambda x: x.index + 1)
    )

    fact = df.merge(
        dim_campaign,
        on=["campaign_name", "objective", "status"],
        how="left",
    )
    fact["date_id"] = fact["date"].dt.strftime("%Y%m%d").astype(int)
    fact["channel_id"] = fact["channel"].map(lambda c: channel_map[c][0])
    fact = fact[
        [
            "date_id",
            "channel_id",
            "campaign_id",
            "spend",
            "impressions",
            "clicks",
            "conversions",
            "revenue",
        ]
    ].copy()
    fact["loaded_at"] = pd.Timestamp.utcnow().isoformat()

    return {
        "dim_date": dim_date,
        "dim_channel": dim_channel,
        "dim_campaign": dim_campaign[["campaign_id", "campaign_name", "objective", "status"]],
        "fact_ads_performance": fact,
    }
