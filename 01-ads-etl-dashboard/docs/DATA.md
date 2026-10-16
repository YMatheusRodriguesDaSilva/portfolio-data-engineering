# Sobre os dados (Data notes)

## Os dados são reais?

**Não.** Este projeto usa **dados sintéticos (mockados)** gerados localmente.

O módulo `src/generate_sample_data.py` cria arquivos CSV no formato típico de extratos diários de:

- Google Ads
- Meta Ads (Facebook/Instagram Ads)

## Por que dados sintéticos?

1. **Sem credenciais** — não precisa de token de API nem conta de anúncios
2. **Sem risco de vazamento** — nenhum dado de cliente/empresa entra no GitHub
3. **Reproduzível** — qualquer pessoa clona o repo, roda o pipeline e vê o mesmo fluxo
4. **Foco no engineering** — o valor do projeto está no ETL, modelagem, qualidade e dashboard

## O que o GitHub contém?

| Incluído no repo | Gerado na sua máquina (não versionado) |
|------------------|----------------------------------------|
| Código Python / SQL / Streamlit | `data/raw/*.csv` |
| Documentação e testes | `data/processed/warehouse.db` |
| Scripts para gerar os dados | Arquivos locais do `.venv` |

## Como os dados são gerados?

- Janela padrão: **90 dias**
- 2 canais × 4 campanhas × N dias
- Métricas: spend, impressions, clicks, conversions, revenue
- Comportamento realista o bastante para KPIs (CTR, CPC, CPA, ROAS)

Regenerar:

```bash
python -m src.pipeline --days 90
```

## Evolução futura (opcional)

Em um ambiente real, a camada `extract` poderia ler APIs oficiais (Google Ads / Meta Marketing API) ou arquivos exportados pelo time de mídia — mantendo transform/load/dashboard iguais.
