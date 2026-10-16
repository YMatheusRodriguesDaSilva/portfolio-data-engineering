# Ads ETL Pipeline + Analytics Dashboard

Portfolio project for **Data Engineer / Analytics Engineer**.

End-to-end flow:

1. Generate sample marketing ads extracts (Google Ads + Meta Ads style)
2. Run ETL into a **dimensional model** (SQLite)
3. Enforce **data quality gates**
4. Explore KPIs in a **Streamlit dashboard**

> Mirrors real work: paid-media extracts → pipelines → warehouse model → BI layer.

## Architecture

```text
raw CSV extracts
  → extract / validate
  → transform (clean + dimensional model)
  → quality gates
  → load (dim_date, dim_channel, dim_campaign, fact_ads_performance)
  → Streamlit dashboard (KPIs, trends, channel mix)
```

Details: [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md)

## Stack

- Python, pandas
- SQL / SQLite (PostgreSQL-friendly schema)
- Streamlit + Plotly
- pytest

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# full pipeline
python -m src.pipeline

# or with Make
make pipeline

# dashboard
streamlit run dashboard/app.py
# make dashboard

# tests
pytest -q
```

### Useful CLI flags

```bash
# custom sample window
python -m src.pipeline --days 30

# reuse existing files in data/raw
python -m src.pipeline --skip-generate
```

## KPIs

| KPI | Formula |
|-----|---------|
| CTR | clicks / impressions |
| CPC | spend / clicks |
| CPA | spend / conversions |
| ROAS | revenue / spend |

Also tracked: Spend, Impressions, Clicks, Conversions, Revenue.

## Project structure

```text
01-ads-etl-dashboard/
├── dashboard/app.py
├── docs/ARCHITECTURE.md
├── data/raw/
├── data/processed/
├── sql/schema.sql
├── src/
│   ├── config.py
│   ├── generate_sample_data.py
│   ├── extract.py
│   ├── transform.py
│   ├── quality.py
│   ├── metrics.py
│   ├── load.py
│   ├── logging_config.py
│   └── pipeline.py
├── tests/
├── Makefile
└── requirements.txt
```

## What this demonstrates

- ETL orchestration with clear layers
- Dimensional modeling (star schema)
- Data quality assertions before load
- Analytics / BI consumption layer
- Testable, reproducible portfolio code

## Author

Matheus Rodrigues da Silva — Data Engineer | Analytics Engineer
