# Deploy no Streamlit Cloud

Você vai publicar **dois apps** (um por projeto), ambos a partir deste monorepo.

## Pré-requisito

1. Conta em https://share.streamlit.io (login com GitHub)
2. Este repo já no GitHub: `YMatheusRodriguesDaSilva/portfolio-data-engineering`

## App 1 — Ads ETL Dashboard

1. Em Streamlit Cloud → **Create app** → **Yup, I have an app**
2. Repository: `YMatheusRodriguesDaSilva/portfolio-data-engineering`
3. Branch: `main`
4. **Main file path:**
   ```text
   01-ads-etl-dashboard/dashboard/app.py
   ```
5. **Advanced settings:**
   - Python version: **3.11**
   - **Secrets:** deixe **vazio** (não coloque path de requirements aqui)
6. Save → **Deploy**

O Cloud usa automaticamente `01-ads-etl-dashboard/dashboard/requirements.txt`.

Na primeira abertura o app gera os dados sintéticos sozinho (pode levar ~30–60s).

## App 2 — E-commerce Warehouse

Repita com:

- Main file path:
  ```text
  02-ecommerce-analytics-warehouse/dashboard/app.py
  ```
- Advanced settings: Python **3.11**, Secrets vazio

## Depois do deploy

1. Copie as URLs (`https://....streamlit.app`)
2. Cole nos READMEs (seção Live demo) e/ou no LinkedIn Featured
3. Me avise os links se quiser que eu atualize os badges no repo

## Troubleshooting

| Problema | Solução |
|----------|---------|
| "Invalid format: please enter valid TOML" | Você colou o path no campo Secrets — apague tudo e Salve |
| ModuleNotFoundError | Confirme o Main file path (`dashboard/app.py`) e que o push com `dashboard/requirements.txt` já está no GitHub |
| App fica em branco na 1ª carga | Aguarde o bootstrap do warehouse; recarregue a página |
| Install lento | Normal na 1ª vez; deploys seguintes ficam mais rápidos |
