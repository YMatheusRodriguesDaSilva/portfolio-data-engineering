from __future__ import annotations

from src.extract import extract
from src.generate_sample_data import generate
from src.load import load
from src.metrics import compute_kpis
from src.pipeline import run
from src.quality import run_quality_checks
from src.transform import transform


def test_pipeline_end_to_end():
    generate(days=14)
    raw = extract()
    assert len(raw) > 0
    assert set(raw["channel"].unique()) == {"google_ads", "meta_ads"}

    tables = transform(raw)
    assert {"dim_date", "dim_channel", "dim_campaign", "fact_ads_performance"} <= set(tables)

    fact = tables["fact_ads_performance"]
    assert (fact["clicks"] <= fact["impressions"]).all()
    assert fact["campaign_id"].notna().all()

    results = run_quality_checks(tables)
    assert all(r.passed for r in results)

    db = load(tables)
    assert db.exists()


def test_kpis_and_cli_pipeline(tmp_path, monkeypatch):
    # Ensure pipeline run works with short window
    run(days=7, skip_generate=False)
    raw = extract()
    tables = transform(raw)
    kpis = compute_kpis(tables["fact_ads_performance"])
    assert kpis["spend"] > 0
    assert kpis["roas"] > 0
    assert 0 <= kpis["ctr"] <= 1


def test_transform_rejects_bad_dates():
    import pandas as pd
    import pytest

    bad = pd.DataFrame(
        {
            "date": ["not-a-date"],
            "channel": ["google_ads"],
            "campaign_name": ["X"],
            "objective": ["Conversions"],
            "status": ["ACTIVE"],
            "spend": [10],
            "impressions": [100],
            "clicks": [5],
            "conversions": [1],
            "revenue": [20],
        }
    )
    with pytest.raises(ValueError, match="Invalid dates"):
        transform(bad)
