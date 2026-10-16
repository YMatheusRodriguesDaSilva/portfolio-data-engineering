"""Data quality checks on transformed tables before load."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.logging_config import get_logger

logger = get_logger("ads_etl.quality")


@dataclass
class QualityResult:
    name: str
    passed: bool
    detail: str


def run_quality_checks(tables: dict[str, pd.DataFrame]) -> list[QualityResult]:
    fact = tables["fact_ads_performance"]
    dim_campaign = tables["dim_campaign"]
    dim_channel = tables["dim_channel"]
    dim_date = tables["dim_date"]
    results: list[QualityResult] = []

    results.append(
        QualityResult(
            "fact_not_empty",
            len(fact) > 0,
            f"rows={len(fact)}",
        )
    )
    results.append(
        QualityResult(
            "clicks_lte_impressions",
            bool((fact["clicks"] <= fact["impressions"]).all()),
            "all fact rows must satisfy clicks <= impressions",
        )
    )
    results.append(
        QualityResult(
            "non_negative_metrics",
            bool(
                (fact[["spend", "impressions", "clicks", "conversions", "revenue"]] >= 0)
                .all()
                .all()
            ),
            "spend/impressions/clicks/conversions/revenue >= 0",
        )
    )
    orphan_campaigns = ~fact["campaign_id"].isin(dim_campaign["campaign_id"])
    results.append(
        QualityResult(
            "campaign_fk",
            not orphan_campaigns.any(),
            f"orphan campaign rows={int(orphan_campaigns.sum())}",
        )
    )
    orphan_channels = ~fact["channel_id"].isin(dim_channel["channel_id"])
    results.append(
        QualityResult(
            "channel_fk",
            not orphan_channels.any(),
            f"orphan channel rows={int(orphan_channels.sum())}",
        )
    )
    orphan_dates = ~fact["date_id"].isin(dim_date["date_id"])
    results.append(
        QualityResult(
            "date_fk",
            not orphan_dates.any(),
            f"orphan date rows={int(orphan_dates.sum())}",
        )
    )
    dup_keys = fact.duplicated(
        subset=["date_id", "channel_id", "campaign_id"], keep=False
    )
    results.append(
        QualityResult(
            "grain_unique",
            not dup_keys.any(),
            f"duplicate grain rows={int(dup_keys.sum())}",
        )
    )
    return results


def assert_quality(tables: dict[str, pd.DataFrame]) -> None:
    results = run_quality_checks(tables)
    failed = [r for r in results if not r.passed]
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        logger.info("[%s] %s — %s", status, r.name, r.detail)
    if failed:
        names = ", ".join(r.name for r in failed)
        raise AssertionError(f"Data quality failed: {names}")
