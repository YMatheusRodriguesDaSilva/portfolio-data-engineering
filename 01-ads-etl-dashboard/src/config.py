from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
SCHEMA_SQL = ROOT / "sql" / "schema.sql"
WAREHOUSE_DB = DATA_PROCESSED / "warehouse.db"

RAW_GOOGLE = DATA_RAW / "google_ads_daily.csv"
RAW_META = DATA_RAW / "meta_ads_daily.csv"

CHANNELS = {
    "google_ads": {"channel_id": 1, "channel_type": "Search/Performance"},
    "meta_ads": {"channel_id": 2, "channel_type": "Social"},
}
