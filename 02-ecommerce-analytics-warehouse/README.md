# E-commerce Analytics Warehouse

Analytics Engineering project: raw transactional extracts → **staging** → **marts** (dimensional / KPI tables) with **data quality checks**.

## Architecture

```
raw orders / items / customers (CSV)
   → staging views (typed, cleaned)
   → marts:
        dim_customer
        dim_product
        fact_order_items
        mart_daily_revenue
   → data quality assertions
```

## Stack

- Python + pandas (orchestration)
- SQL (SQLite, PostgreSQL-friendly syntax)
- pytest for quality gates

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m src.run_warehouse
pytest -q
```

## What recruiters should see

- Clear medallion-style layers (raw → staging → marts)
- SQL-first modeling
- Explicit data quality checks (nulls, duplicates, referential integrity, revenue sanity)

## Structure

```
02-ecommerce-analytics-warehouse/
├── sql/
│   ├── staging.sql
│   └── marts.sql
├── src/
│   ├── generate_sample_data.py
│   ├── run_warehouse.py
│   └── data_quality.py
├── data/raw/.gitkeep
├── data/warehouse/.gitkeep
└── tests/test_quality.py
```
