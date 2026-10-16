# Architecture — Ads ETL + Dashboard

## Overview

This project simulates a paid-media analytics stack:

1. **Extract** raw daily performance files (Google Ads / Meta Ads style CSVs)
2. **Transform** into a star-schema dimensional model
3. **Quality-check** grain, FKs and metric sanity rules
4. **Load** into SQLite (swap-friendly to PostgreSQL)
5. **Serve** KPIs via Streamlit

```text
┌──────────────┐     ┌───────────┐     ┌────────────┐     ┌──────────┐     ┌────────────┐
│ Sample / API │ --> │  Extract  │ --> │ Transform  │ --> │ Quality  │ --> │   Load     │
│  CSV files   │     │ validate  │     │ dims+fact  │     │  gates   │     │  SQLite    │
└──────────────┘     └───────────┘     └────────────┘     └──────────┘     └─────┬──────┘
                                                                                 │
                                                                                 v
                                                                          ┌────────────┐
                                                                          │ Streamlit  │
                                                                          │ Dashboard  │
                                                                          └────────────┘
```

## Dimensional model

| Table | Grain / role |
|-------|----------------|
| `dim_date` | One row per calendar day (`date_id = YYYYMMDD`) |
| `dim_channel` | Google Ads / Meta Ads |
| `dim_campaign` | Campaign + objective + status |
| `fact_ads_performance` | date × channel × campaign |

### Fact metrics

`spend`, `impressions`, `clicks`, `conversions`, `revenue`

### Derived KPIs

- CTR = clicks / impressions
- CPC = spend / clicks
- CPA = spend / conversions
- ROAS = revenue / spend

## Quality gates

- Fact not empty
- `clicks <= impressions`
- Non-negative metrics
- FK integrity to all dimensions
- Unique grain `(date_id, channel_id, campaign_id)`

## Why SQLite here

Zero-setup for portfolio demos. The SQL schema is intentionally plain so it can be moved to PostgreSQL with minimal changes.
