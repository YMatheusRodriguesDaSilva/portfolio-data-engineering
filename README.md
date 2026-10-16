# Portfolio — Data Engineering & Analytics Engineering

Two end-to-end portfolio projects for LinkedIn / GitHub, focused on **Data Engineer** and **Analytics Engineer** skills.

| Project | What it shows |
|---------|----------------|
| [`01-ads-etl-dashboard`](./01-ads-etl-dashboard) | ETL/ELT pipeline + dimensional model + **Streamlit dashboard** |
| [`02-ecommerce-analytics-warehouse`](./02-ecommerce-analytics-warehouse) | Staging → marts SQL warehouse + data quality checks |

## Stack

- Python, SQL (SQLite for zero-setup local runs)
- ETL/ELT, dimensional modeling (fact/dimension)
- Streamlit (BI layer)
- pytest

## Quick start

```bash
# Project 1 — pipeline + dashboard
cd 01-ads-etl-dashboard
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline
streamlit run dashboard/app.py

# Project 2 — warehouse + quality
cd ../02-ecommerce-analytics-warehouse
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.run_warehouse
pytest -q
```

## Suggested GitHub layout

You can keep this monorepo **or** split into two public repos:

1. `ads-etl-dashboard`
2. `ecommerce-analytics-warehouse`

Add both links to LinkedIn **Featured**.

## Author

Matheus Rodrigues da Silva — Data Engineer | Analytics Engineer
