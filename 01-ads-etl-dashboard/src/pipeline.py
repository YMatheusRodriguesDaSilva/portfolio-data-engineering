"""Orchestrate generate → extract → transform → quality → load."""

from __future__ import annotations

import argparse

from src.extract import extract
from src.generate_sample_data import generate
from src.load import load
from src.logging_config import get_logger
from src.metrics import compute_kpis
from src.quality import assert_quality
from src.transform import transform

logger = get_logger("ads_etl.pipeline")


def run(days: int = 90, skip_generate: bool = False) -> None:
    if not skip_generate:
        logger.info("1/5 Generating sample raw extracts (%s days)...", days)
        generate(days=days)
    else:
        logger.info("1/5 Skipping sample generation (using existing raw files)")

    logger.info("2/5 Extracting...")
    raw = extract()
    logger.info("   raw rows: %s", len(raw))

    logger.info("3/5 Transforming to dimensional model...")
    tables = transform(raw)

    logger.info("4/5 Running data quality checks...")
    assert_quality(tables)

    logger.info("5/5 Loading warehouse...")
    load(tables)

    kpis = compute_kpis(tables["fact_ads_performance"])
    logger.info(
        "Pipeline OK | spend=$%.0f revenue=$%.0f ROAS=%.2fx CTR=%.2f%%",
        kpis["spend"],
        kpis["revenue"],
        kpis["roas"],
        kpis["ctr"] * 100,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ads ETL pipeline → dimensional SQLite warehouse"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Number of days of sample data to generate (default: 90)",
    )
    parser.add_argument(
        "--skip-generate",
        action="store_true",
        help="Reuse existing CSV files in data/raw",
    )
    args = parser.parse_args()
    run(days=args.days, skip_generate=args.skip_generate)


if __name__ == "__main__":
    main()
