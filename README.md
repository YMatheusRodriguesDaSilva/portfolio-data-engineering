# Portfolio — Data Engineering & Analytics Engineering

Dois projetos de portfolio para GitHub / LinkedIn (Featured).

| Projeto | Status | O que mostra |
|---------|--------|--------------|
| [`01-ads-etl-dashboard`](./01-ads-etl-dashboard) | **Pronto** | ETL de mídia paga + modelo dimensional + quality gates + dashboard Streamlit |
| [`02-ecommerce-analytics-warehouse`](./02-ecommerce-analytics-warehouse) | Em evolução | Staging → marts SQL + data quality |

## Projeto 1 (comece por aqui)

```bash
cd 01-ads-etl-dashboard
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline
streamlit run dashboard/app.py
```

- Dados **sintéticos** (seguros para repo público) — detalhes em `01-ads-etl-dashboard/docs/DATA.md`
- Ideal para recrutadores e para quem está começando na área

## Author

Matheus Rodrigues da Silva — Data Engineer | Analytics Engineer  
[LinkedIn](https://www.linkedin.com/in/mmatheusrodrigues/)
