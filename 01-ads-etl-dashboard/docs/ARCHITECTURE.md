# Architecture — Ads ETL + Dashboard

## Overview

Pipeline de analytics de mídia paga pensado como portfolio profissional:

1. **Generate / Extract** — CSVs sintéticos no formato de extratos diários  
2. **Transform** — limpeza + modelo dimensional (star schema)  
3. **Quality** — gates de integridade e regras de negócio  
4. **Load** — SQLite local (pronto para migrar a PostgreSQL)  
5. **Serve** — Streamlit + Plotly para KPIs

```text
┌──────────────────┐
│ Sample generator │  (synthetic Google/Meta style CSVs)
└────────┬─────────┘
         ▼
┌──────────────────┐
│     Extract      │  validate columns + concatenate sources
└────────┬─────────┘
         ▼
┌──────────────────┐
│    Transform     │  dims + fact grain (date × channel × campaign)
└────────┬─────────┘
         ▼
┌──────────────────┐
│     Quality      │  FK, grain, non-negative metrics, clicks≤impressions
└────────┬─────────┘
         ▼
┌──────────────────┐
│       Load       │  sql/schema.sql → warehouse.db
└────────┬─────────┘
         ▼
┌──────────────────┐
│    Dashboard     │  Streamlit KPIs + charts
└──────────────────┘
```

## Dimensional model

| Table | Grain / role |
|-------|----------------|
| `dim_date` | 1 linha por dia (`date_id = YYYYMMDD`) |
| `dim_channel` | Google Ads / Meta Ads |
| `dim_campaign` | campaign + objective + status |
| `fact_ads_performance` | date × channel × campaign |

### Fact metrics

`spend`, `impressions`, `clicks`, `conversions`, `revenue`

### Derived KPIs

- CTR = clicks / impressions  
- CPC = spend / clicks  
- CPA = spend / conversions  
- ROAS = revenue / spend  

## Why SQLite in the portfolio?

Zero setup for anyone cloning the repo. The SQL is intentionally portable so the same model can move to PostgreSQL with small changes.

## Design choices for readability

- One module per ETL responsibility (`extract`, `transform`, `quality`, `load`, `pipeline`)
- Shared KPI functions (`metrics.py`) used by pipeline logs and dashboard
- Explicit logging instead of silent scripts
- Tests covering happy path + invalid dates
