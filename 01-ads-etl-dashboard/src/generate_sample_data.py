"""Generate realistic sample paid-media extracts (no API keys required)."""

from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from src.config import DATA_RAW, RAW_GOOGLE, RAW_META
from src.logging_config import get_logger

logger = get_logger("ads_etl.generate")


CAMPAIGNS = [
    ("Brand Awareness Q1", "Awareness"),
    ("Performance Prospecting", "Conversions"),
    ("Retargeting Cart", "Conversions"),
    ("App Install Push", "App Installs"),
]


def _build_frame(channel: str, start: datetime, days: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows: list[dict] = []
    for offset in range(days):
        day = start + timedelta(days=offset)
        for campaign_name, objective in CAMPAIGNS:
            impressions = int(rng.integers(8_000, 80_000))
            ctr = float(rng.uniform(0.008, 0.045))
            clicks = max(1, int(impressions * ctr))
            cpc = float(rng.uniform(0.35, 2.80))
            spend = round(clicks * cpc, 2)
            cvr = float(rng.uniform(0.01, 0.08))
            conversions = max(0, int(clicks * cvr))
            aov = float(rng.uniform(40, 180))
            revenue = round(conversions * aov, 2)
            rows.append(
                {
                    "date": day.strftime("%Y-%m-%d"),
                    "channel": channel,
                    "campaign_name": campaign_name,
                    "objective": objective,
                    "status": "ACTIVE",
                    "spend": spend,
                    "impressions": impressions,
                    "clicks": clicks,
                    "conversions": conversions,
                    "revenue": revenue,
                }
            )
    return pd.DataFrame(rows)


def generate(days: int = 90) -> tuple[pd.DataFrame, pd.DataFrame]:
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    start = datetime(2026, 7, 1)
    google = _build_frame("google_ads", start, days, seed=42)
    meta = _build_frame("meta_ads", start, days, seed=7)
    google.to_csv(RAW_GOOGLE, index=False)
    meta.to_csv(RAW_META, index=False)
    logger.info("Wrote %s (%s rows)", RAW_GOOGLE, len(google))
    logger.info("Wrote %s (%s rows)", RAW_META, len(meta))
    return google, meta


if __name__ == "__main__":
    generate()
