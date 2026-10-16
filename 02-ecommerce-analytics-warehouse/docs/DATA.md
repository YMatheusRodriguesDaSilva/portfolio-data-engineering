# Sobre os dados (Data notes)

## Os dados são reais?

**Não.** Este projeto usa **dados sintéticos** de e-commerce gerados por `src/generate_sample_data.py`.

Arquivos gerados em `data/raw/`:

- `customers.csv`
- `products.csv`
- `orders.csv`
- `order_items.csv`

## Por que sintéticos?

1. Repo público sem risco de dado sensível
2. Sem depender de banco/API externa
3. Reproduzível: qualquer pessoa gera o warehouse localmente
4. Foco no **Analytics Engineering** (staging → marts → quality)

## O que o GitHub versiona?

| No repo | Só na sua máquina |
|---------|-------------------|
| SQL, Python, dashboard, docs, testes | `data/raw/*.csv` |
| | `data/warehouse/ecommerce.db` |
| | `.venv/` |

## Regras de negócio no fato

Pedidos com status `cancelled` **não entram** em `fact_order_items` — só `paid`, `shipped`, `delivered`.
