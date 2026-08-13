# Validação final da CDF brasileira — PNAD Contínua 2025

**Resultado:** `PASS`

**Versão da distribuição:** `2025-20260508-v1`

**Metodologia:** `1.0.0`

## Fonte e referência

- Dataset intermediário: `data/processed/brazil/pnad-2025/brazil-income-distribution-2025.csv`
- SHA-256 fonte: `8A44A26C47F16BE54DE787D215145C60B82E33319F806A0F890411B799EDA469`
- Referência monetária: **preços médios de 2025**.
- Unidade: pessoas elegíveis ponderadas por `V1032`.
- Integração ao frontend: **bloqueada** até definição do alinhamento temporal da renda digitada.

## Artefato

- Formato: JSON UTF-8 determinístico, representação agregada por RDPC único.
- Caminho: `data/production/brazil/brazil-income-cdf-2025.json`.
- SHA-256: `5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5`
- Tamanho: 3955036 bytes.
- Linhas fonte: 408243.
- Valores únicos: 83358.
- Redução de registros: 79.581279%.
- Redução de bytes: 69.390939%.

O artefato guarda `rdpc`, `weightAt` e `cumAtOrBelow`. Para um ponto observado, `cumBelow` é zero no primeiro ponto ou o acumulado do item anterior; não existe coluna redundante nem perda estatística.

## Distribuição reconstruída

- Peso total: 212624284.80064434.
- Média: 2264.0378278980.
- Gini: 0.5112237274.
- RDPC mínimo: 0.0000000000.
- RDPC máximo: 200165.7922757916.
- Peso com RDPC zero: 2365090.63973513 (1.112333%).

## Quantis empíricos

| Quantil | RDPC |
| --- | ---: |
| P5 | 298.6600188033 |
| P10 | 450.7467676623 |
| P20 | 693.9428296997 |
| P25 | 773.4762192254 |
| P30 | 905.8353909869 |
| P40 | 1154.1939357946 |
| P50 | 1489.9901921271 |
| P60 | 1697.1185281974 |
| P70 | 2158.1105828585 |
| P75 | 2483.5727017972 |
| P80 | 2958.3887369774 |
| P90 | 4610.1557817898 |
| P95 | 6899.6769528034 |
| P99 | 15214.5091425709 |
| P99.5 | 20507.9792045905 |
| P99.9 | 38991.6613583962 |

## P90 e P99

A investigação confirmou em documentação oficial do IBGE que pessoas com o mesmo rendimento são alocadas no mesmo percentil, ainda que a proporção final da classe seja apenas aproximada. Essa regra é compatível com a CDF empírica em degraus implementada.

Não foi localizada documentação oficial suficiente para reproduzir exatamente os R$ 1 residuais. A inversa empírica ponderada produz P90 = R$ 4610.1557817898 e P99 = R$ 15214.5091425709; após arredondamento usual, R$ 4.610 e R$ 15.215, enquanto o SIDRA publica R$ 4.609 e R$ 15.214. A diferença permanece pendente e não altera a CDF principal.

Foram testadas, sem canonização, três convenções adicionais. No P90, a fronteira por posto médio arredonda para 4609 e a interpolação centrada para 4610; no P99, elas arredondam para 15213 e 15214. Nenhuma reproduz simultaneamente os dois cortes publicados, portanto não há base para substituir a inversa empírica.

Fontes oficiais consultadas:

- Informativo IBGE 2024, que remete ao Anexo 10 das Notas técnicas versão 1.19 e explicita a regra de empates.
- Anexo 10 das Notas técnicas versão 1.7, consultado como histórico do procedimento anterior.
- SIDRA tabela 7526, com os limites publicados de 2025.

## Golden cases selecionados

| Caso | RDPC | shareBelow | shareAtOrBelow | topShare |
| --- | ---: | ---: | ---: | ---: |
| zero | 0.0000000000 | 0.000000000000000 | 0.011123332604987 | 1.000000000000000 |
| median | 1489.9901921271 | 0.499917073753765 | 0.500534597600019 | 0.500082926246235 |
| mean | 2264.0378278980 | 0.718028020883420 | 0.718028020883420 | 0.281971979116580 |
| P90 | 4610.1557817898 | 0.899993946255886 | 0.900019898306390 | 0.100006053744114 |
| P99 | 15214.5091425709 | 0.989990959522217 | 0.990020534930359 | 0.010009040477783 |
| householdIncome6500Residents3 | 2166.6666666667 | 0.701561259093934 | 0.701561259093934 | 0.298438740906066 |
| maximum | 200165.7922757916 | 0.999998074866125 | 1.000000000000000 | 0.000001925133875 |
| aboveMaximum | 200166.7922757916 | 1.000000000000000 | 1.000000000000000 | 0.000000000000000 |

O caso `R$ 6.500 / 3` usa RDPC exato registrado como `2166.666666666666666666666667`; ele é fixture da distribuição e não foi integrado ao site.

## Empates e limites

- `shareBelow(x)` usa exclusivamente `RDPC < x`.
- `shareAtOrBelow(x)` usa `RDPC <= x`.
- `topShare(x) = 1 - shareBelow(x)`.
- Entre valores observados, o resultado permanece constante; nenhuma interpolação é aplicada.
- Em `x = 0`, `shareBelow = 0` e `shareAtOrBelow > 0`.
- No máximo, `shareBelow < 1` e `shareAtOrBelow = 1`.
- Acima do máximo, ambas as participações acumuladas são 1.

## Reprodutibilidade

| Métrica | Run 1 | Run 2 |
| --- | ---: | ---: |
| Valores únicos | 83358 | 83358 |
| Peso | 212624284.80064434 | 212624284.80064434 |
| Média | 2264.0378278980 | 2264.0378278980 |
| Gini | 0.5112237274 | 0.5112237274 |
| CDF SHA-256 | `5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5` | `5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5` |

## Performance

- Algoritmo: busca binária.
- Consultas: 100000.
- Tempo observado: 4183.721 ms.
- Média observada: 41.837 µs por lookup.

O tempo é diagnóstico local e não integra o checksum determinístico.

## Testes e escopo

- Testes automatizados: `PASS`.
- Monotonicidade, limites, empates, média, Gini, quantis, determinismo e golden cases: `PASS`.
- Nenhum dado individual foi incluído.
- `src/` não foi alterado.
- Nenhuma CDF mundial, transformação temporal ou integração ao frontend foi executada.
