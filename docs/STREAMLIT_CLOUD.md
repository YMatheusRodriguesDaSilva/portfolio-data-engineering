# Deploy no Streamlit Cloud

Você vai publicar **dois apps** (um por projeto), ambos a partir deste monorepo.

## Pré-requisito

1. Conta em https://share.streamlit.io (login com GitHub)
2. Este repo já no GitHub: `YMatheusRodriguesDaSilva/portfolio-data-engineering`

## App 1 — Ads ETL Dashboard

1. Em Streamlit Cloud → **New app**
2. Repository: `YMatheusRodriguesDaSilva/portfolio-data-engineering`
3. Branch: `main`
4. **Main file path:**
   ```text
   01-ads-etl-dashboard/dashboard/app.py
   ```
5. Advanced settings → **Python version:** 3.11  
6. Advanced settings → **Requirements file:**
   ```text
   01-ads-etl-dashboard/requirements.txt
   ```
7. Deploy

Na primeira abertura o app gera os dados sintéticos sozinho (pode levar ~30–60s).

## App 2 — E-commerce Warehouse

Repita com:

- Main file path:
  ```text
  02-ecommerce-analytics-warehouse/dashboard/app.py
  ```
- Requirements file:
  ```text
  02-ecommerce-analytics-warehouse/requirements.txt
  ```

## Depois do deploy

1. Copie as URLs (`https://....streamlit.app`)
2. Cole nos READMEs (seção Live demo) e/ou no LinkedIn Featured
3. Me avise os links se quiser que eu atualize os badges no repo

## Troubleshooting

| Problema | Solução |
|----------|---------|
| ModuleNotFoundError `src` | Confirme o Main file path (tem que ser o `dashboard/app.py` do projeto) |
| App fica em branco na 1ª carga | Aguarde o bootstrap do warehouse; recarregue a página |
| Install lento | Normal na 1ª vez; deploys seguintes ficam mais rápidos |
