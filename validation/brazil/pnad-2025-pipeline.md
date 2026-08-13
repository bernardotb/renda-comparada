# Validação do pipeline brasileiro — PNAD Contínua 2025

**Resultado:** `PASS`

**Metodologia:** `1.0.0`
**Referência monetária:** preços médios de 2025

## Fonte e configuração

- Arquivo: `PNADC_2025_visita1_20260508.zip`
- Release: `20260508`
- SHA-256: `556C68467941FCF8FB1251CDBAD3E42F6912C7938D73FD75F900BEE1C79548A5`
- Configuração: `config/brazil-pnad-2025.json`
- SHA-256 da configuração: `E59072300295303097867BC8D1D0A78BCE9A942E050AA33FB4DE408AED5B55F1`

## Fórmula implementada

```text
RDPC_real_2025 =
  soma_domiciliar(VD4019 × CO1 + VD4048 × CO1e)
  ÷ VD2003
```

A distribuição final preserva uma linha por pessoa elegível e usa `V1032` como peso. O join dos deflatores usa `Ano + Trimestre + UF`.

## Reprodutibilidade

| Métrica | Run 1 | Run 2 |
| --- | ---: | ---: |
| Registros | 408243 | 408243 |
| Média | 2264.0378278980 | 2264.0378278980 |
| Gini | 0.5112237274 | 0.5112237274 |
| População ponderada | 212624284.8006 | 212624284.8006 |
| SHA-256 dataset | `8A44A26C47F16BE54DE787D215145C60B82E33319F806A0F890411B799EDA469` | `8A44A26C47F16BE54DE787D215145C60B82E33319F806A0F890411B799EDA469` |
| SHA-256 manifesto | `78768286699B8F230E686008E340EF4A1F79400BFE0568EE338D066F9B5CF9EC` | `78768286699B8F230E686008E340EF4A1F79400BFE0568EE338D066F9B5CF9EC` |

Os dois runs limpos produziram datasets e manifestos byte a byte idênticos.

## Benchmarks

- Média nacional: 2264.0378278980; arredondada: R$ 2264 — `PASS`.
- Gini: 0.5112237274; publicado em três casas: 0.511 — `PASS`.
- População ponderada: 212624284.8006; publicação em milhares: 212624 — `PASS`.
- Médias por UF: 27 de 27 reproduzidas após arredondamento — `PASS`.
- Rendas zero: 4682 registros preservados.
- Rendas negativas: 0.
- Máximo observado: R$ 200165.7923.

## Quantis diagnósticos

| Quantil | Calculado | Publicado | Diferença arredondada |
| --- | ---: | ---: | ---: |
| P5 | 299 | 299 | +0 |
| P10 | 451 | 451 | +0 |
| P20 | 694 | 694 | +0 |
| P30 | 906 | 906 | +0 |
| P40 | 1154 | 1154 | +0 |
| P50 | 1490 | 1490 | +0 |
| P60 | 1697 | 1697 | +0 |
| P70 | 2158 | 2158 | +0 |
| P80 | 2958 | 2958 | +0 |
| P90 | 4610 | 4609 | +1 |
| P95 | 6900 | 6900 | +0 |
| P99 | 15215 | 15214 | +1 |

Os resíduos conhecidos de R$ 1 em P90 e P99 foram reproduzidos e permanecem documentados; nenhuma correção artificial foi aplicada.

## Validações estruturais

- Registros brutos: 408364.
- Pessoas elegíveis: 408243.
- Domicílios elegíveis: 152488.
- Chaves de pessoa únicas: 408364.
- Divergências na reconstrução nominal contra `VD5007`: 0.
- Join de deflatores: 108 de 108 chaves oficiais.
- Peso final: numérico, finito e estritamente positivo.
- RDPC final: finito, não negativo e com zeros preservados.

## Testes e ambiente

- Testes automatizados: `PASS`.
- Python: `3.12.13`.
- NumPy: `2.3.5`.
- xlrd: `2.0.2`.

## Limites desta fase

Não foram criados CDF, lookup, golden cases ou integração com o frontend. O alinhamento temporal da renda digitada e a metodologia Mundo continuam pendentes. O dataset intermediário permanece local e ignorado pelo Git; somente o manifesto e os relatórios sem dados individuais são versionados.
