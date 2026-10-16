# Portfolio — Data Engineering & Analytics Engineering

[![CI](https://github.com/YMatheusRodriguesDaSilva/portfolio-data-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/YMatheusRodriguesDaSilva/portfolio-data-engineering/actions/workflows/ci.yml)

Dois projetos prontos para GitHub / LinkedIn Featured.

| Projeto | Foco | Live demo |
|---------|------|-----------|
| [`01-ads-etl-dashboard`](./01-ads-etl-dashboard) | Data Engineering + BI | [Streamlit](https://portfolio-data-engineering-dktms26fxjcscyufkdrkwq.streamlit.app/) |
| [`02-ecommerce-analytics-warehouse`](./02-ecommerce-analytics-warehouse) | Analytics Engineering | [Streamlit](https://portfolio-data-engineering-as4n734uekubaxk4fknmqz.streamlit.app/) |

Ambos usam **dados sintéticos** (seguros para repo público).

## CI

A cada push na `main`, o GitHub Actions:
- gera dados / roda o pipeline
- executa `pytest` nos dois projetos

## Live dashboards (Streamlit Cloud)

- **Ads ETL:** https://portfolio-data-engineering-dktms26fxjcscyufkdrkwq.streamlit.app/
- **E-commerce warehouse:** https://portfolio-data-engineering-as4n734uekubaxk4fknmqz.streamlit.app/

Guia: [`docs/STREAMLIT_CLOUD.md`](./docs/STREAMLIT_CLOUD.md)

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
