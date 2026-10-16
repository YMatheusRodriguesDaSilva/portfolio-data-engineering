"""Extract layer: read raw source files with basic validation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import RAW_GOOGLE, RAW_META

REQUIRED_COLUMNS = {
    "date",
    "channel",
    "campaign_name",
    "objective",
    "status",
    "spend",
    "impressions",
    "clicks",
    "conversions",
    "revenue",
}


def _read_source(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing raw file: {path}. Run generate_sample_data first.")
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"{path.name} missing columns: {sorted(missing)}")
    if df.empty:
        raise ValueError(f"{path.name} is empty")
    return df


def extract() -> pd.DataFrame:
    frames = [_read_source(RAW_GOOGLE), _read_source(RAW_META)]
    raw = pd.concat(frames, ignore_index=True)
    return raw
