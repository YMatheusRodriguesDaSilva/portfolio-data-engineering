# Portfolio — Data Engineering & Analytics Engineering

[![CI](https://github.com/YMatheusRodriguesDaSilva/portfolio-data-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/YMatheusRodriguesDaSilva/portfolio-data-engineering/actions/workflows/ci.yml)

Dois projetos prontos para GitHub / LinkedIn Featured.

| Projeto | Foco | Destaque |
|---------|------|----------|
| [`01-ads-etl-dashboard`](./01-ads-etl-dashboard) | Data Engineering + BI | ETL de mídia paga → star schema → quality → Streamlit |
| [`02-ecommerce-analytics-warehouse`](./02-ecommerce-analytics-warehouse) | Analytics Engineering | SQL-first staging/marts → quality → Streamlit |

Ambos usam **dados sintéticos** (seguros para repo público).

## CI

A cada push na `main`, o GitHub Actions:
- gera dados / roda o pipeline
- executa `pytest` nos dois projetos

## Live dashboards (Streamlit Cloud)

Guia passo a passo: [`docs/STREAMLIT_CLOUD.md`](./docs/STREAMLIT_CLOUD.md)

## Quick start

```bash
# Projeto 1
cd 01-ads-etl-dashboard
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline
streamlit run dashboard/app.py

# Projeto 2
cd ../02-ecommerce-analytics-warehouse
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.run_warehouse
streamlit run dashboard/app.py
```

## Author

**Matheus Rodrigues da Silva** — Data Engineer | Analytics Engineer  
[LinkedIn](https://www.linkedin.com/in/mmatheusrodrigues/) · [GitHub](https://github.com/YMatheusRodriguesDaSilva)
