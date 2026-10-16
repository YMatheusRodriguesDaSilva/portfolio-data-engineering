# Architecture — E-commerce Analytics Warehouse

## Layers (medallion-style)

```text
raw_customers / raw_products / raw_orders / raw_order_items
        ↓
stg_* views   (typed, trimmed, filtered)
        ↓
dim_customer / dim_product
fact_order_items
mart_daily_revenue
mart_category_revenue
mart_top_customers
        ↓
data quality gates
        ↓
Streamlit dashboard
```

## Marts

| Mart | Pergunta de negócio |
|------|---------------------|
| `mart_daily_revenue` | Quanto vendemos por dia? |
| `mart_category_revenue` | Qual categoria performa melhor? |
| `mart_top_customers` | Quem são os clientes de maior receita? |

## Quality gates

- e-mail de cliente não nulo / único
- FKs de produto e cliente no fato
- receita ≥ 0
- cancelados fora do fato
- marts não vazios
- reconciliação: `SUM(fact.item_revenue) ≈ SUM(mart_daily_revenue.revenue)`

## Why SQL-first?

A modelagem mora em `.sql` (staging/marts). O Python orquestra geração, load e quality — padrão próximo do que se vê com dbt + orchestrator em produção.
