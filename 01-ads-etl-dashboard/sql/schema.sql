-- Dimensional model for paid media performance

DROP TABLE IF EXISTS fact_ads_performance;
DROP TABLE IF EXISTS dim_campaign;
DROP TABLE IF EXISTS dim_channel;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date (
    date_id     INTEGER PRIMARY KEY, -- YYYYMMDD
    full_date   TEXT NOT NULL,
    year        INTEGER NOT NULL,
    month       INTEGER NOT NULL,
    day         INTEGER NOT NULL,
    week_of_year INTEGER NOT NULL,
    day_name    TEXT NOT NULL
);

CREATE TABLE dim_channel (
    channel_id   INTEGER PRIMARY KEY,
    channel_name TEXT NOT NULL UNIQUE,
    channel_type TEXT NOT NULL
);

CREATE TABLE dim_campaign (
    campaign_id   INTEGER PRIMARY KEY,
    campaign_name TEXT NOT NULL,
    objective     TEXT NOT NULL,
    status        TEXT NOT NULL
);

CREATE TABLE fact_ads_performance (
    fact_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id        INTEGER NOT NULL REFERENCES dim_date(date_id),
    channel_id     INTEGER NOT NULL REFERENCES dim_channel(channel_id),
    campaign_id    INTEGER NOT NULL REFERENCES dim_campaign(campaign_id),
    spend          REAL NOT NULL,
    impressions    INTEGER NOT NULL,
    clicks         INTEGER NOT NULL,
    conversions    INTEGER NOT NULL,
    revenue        REAL NOT NULL,
    loaded_at      TEXT NOT NULL
);

CREATE INDEX idx_fact_date ON fact_ads_performance(date_id);
CREATE INDEX idx_fact_channel ON fact_ads_performance(channel_id);
CREATE INDEX idx_fact_campaign ON fact_ads_performance(campaign_id);
