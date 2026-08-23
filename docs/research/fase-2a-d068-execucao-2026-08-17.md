# Fase 2A — execução e evidência para D068

> Status: pesquisa não canônica. Este documento propõe uma decisão para revisão humana; não altera `docs/decisoes.md`, não promove artefatos a `data/production/` e não autoriza integração no frontend.

## Veredito técnico

**D068 — PRONTA COM RESSALVAS.**

A fonte, a build, a transformação e o contrato da CDF candidata estão identificados e reproduzíveis. Todos os checks estruturais passaram. Em 18 linhas de pobreza, a diferença máxima entre a CDF binned e os agregados oficiais do PIP foi de `0,0225169918` ponto percentual. A ressalva é intrínseca à fonte: cada bin representa sua população por um welfare médio e, portanto, elimina desigualdade dentro do bin. A aceitação dessa aproximação e a precisão de exibição pertencem à revisão humana de D068 e à futura D070.

## Estado encontrado

- **ATIVO:** D066 fixa PIP `20260324_2021`, build `20260324_2021_01_02_PROD`, PPP 2021 e ano mundial 2024; D067 fixa o conceito de posição monetária global estimada.
- **BLOQUEADO:** D068, D069 e D070; o frontend deve continuar sem número mundial.
- **EXPERIMENTAL:** protocolos de reprodução e validação em `docs/research/`, incluindo a direção de pesquisa para a base World Bank 1000 Binned Global Distribution.
- **LEGADO:** constantes e curvas antigas do protótipo, sem autoridade metodológica e proibidas como fallback.
- **LACUNA ANTERIOR:** não havia pipeline versionada, CDF candidata, provenance completa nem erro medido contra a API oficial para a build protegida.

## Fonte candidata e contrato

- Fornecedor: World Bank, Poverty and Inequality Platform.
- Dataset: `1000 Binned Global Distribution`.
- Recurso: `DR0094423`.
- Arquivo: `GlobalDist1000bins_1990_2026_20260324_2021_01_02_PROD.csv`.
- Build: `20260324_2021_01_02_PROD`.
- Ano isolado: 2024.
- Universo observado: 218 economias, 1.000 bins por economia.
- Unidade de `welf`: dólares internacionais PPP 2021 por pessoa por dia, no conceito de welfare domiciliar per capita harmonizado pelo PIP (renda ou consumo conforme a economia).
- Peso `pop`: milhões de pessoas representadas pelo bin.
- Licença declarada no catálogo: CC0.

A CDF é construída ordenando globalmente `welf` e acumulando `pop`. Valores empatados são agrupados antes da acumulação. Linhas com missing, valores não finitos, welfare negativo ou população não positiva fazem a pipeline falhar; não existe imputação. Zero é aceito e medido, mas a fatia de 2024 não contém bins em zero. Não há interpolação nem extrapolação: o lookup é uma função degrau.

## Pipeline reproduzível

```text
raw oficial preservado e conferido por tamanho/hash
→ filtrar exatamente year = 2024 e validar schema/build/chaves/bins
→ processed CSV determinístico
→ ordenar/agrupadar welfare empatado e acumular população
→ validar estrutura e comparar 18 checkpoints oficiais
→ candidate JSON + relatórios JSON/Markdown/CSV
```

Comando principal:

```powershell
python scripts/data/world/build_world_candidate.py
```

O raw completo e o intermediário processado ficam ignorados pelo Git; o candidato e os relatórios ficam em `validation/world/`. A pipeline usa apenas a biblioteca padrão do Python.

## Artefatos e hashes

| Artefato | Bytes | SHA-256 |
|---|---:|---|
| raw oficial | 994.875.992 | `99FC4B99BD6D77770DA78A5BFC90516F5FE35742C7A29968F2FD148B323B48A2` |
| processed 2024 | 8.196.471 | `2CA102013BDF9D3EA22C9642326544B32D45EF61407F81C6B71324BC5B072F52` |
| CDF candidata | 11.372.630 | `56C53483744176A50090E16058A0CF4FC6221C83D1D80A60060B931110C54DC2` |
| checkpoints CSV | — | `7B37EE3BEBFCDEF4CB3E9DE1767D24309C5E086FF1DCC9058E2044E0074F314E` |
| relatório JSON | — | `81D9671B81FA750A00A97E33D90542739AED99D416FCB785D447A915121D52B2` |

A candidata contém 216.790 pontos únicos derivados de 218.000 bins. A população acumulada é `8.141,808945` milhões; a API oficial reporta `8.141,8089` milhões, diferença de `0,000045` milhão causada pela precisão publicada. Suporte: mínimo `0,28` e máximo `3.822,84090639671` dólares internacionais PPP 2021 por pessoa por dia.

## Validação estrutural e estatística

Passaram: ano isolado; unicidade `(code, year, quantile)`; 1.000 bins em todas as 218 economias; welfare finito e não negativo; população finita e positiva; suporte estritamente ordenado após empates; peso cumulativo estritamente crescente; fechamento da população; probabilidades em `[0,1]`; integração frontend bloqueada.

Diagnósticos da candidata binned:

- média: `21,5678103926`;
- mediana: `9,2480887451`;
- Gini: `0,6072152956`;
- P10: `2,9328190651`;
- P25: `4,9655608620`;
- P50: `9,2480887451`;
- P75: `22,5330208180`;
- P90: `54,0372319230`;
- P95: `82,0069362895`;
- P99: `162,8278964437`;
- P99,5: `210,1466117406`;
- P99,9: `367,7771552459`.

Comparação com 18 agregados oficiais do PIP entre 1 e 200 dólares PPP/dia: erro absoluto máximo `0,0225169918` pp, erro absoluto médio `0,0067356194` pp, RMSE `0,0090217274` pp e viés médio `-0,0046578424` pp. O pior ponto foi 50 dólares/dia: PIP `88,89%`, candidata `88,867483%`. Como o endpoint publica `headcount` com quatro casas decimais, o erro observado também incorpora até `0,005` pp de arredondamento do comparador.

## Contrato para D069

D069 deverá entregar à função de lookup um número finito, não negativo, expresso em **dólares internacionais PPP 2021 por pessoa por dia**, temporal e conceitualmente compatível com a build PIP `20260324_2021_01_02_PROD` e o ano global 2024. Esta execução não define nem implementa a conversão de BRL corrente para essa unidade.

## Estados reservados a D070

D070 deverá testar: zero; abaixo do mínimo; exatamente no mínimo; entre pontos; empate; P10/P25/P50/P75/P90/P95/P99; cauda P99,5/P99,9; exatamente no máximo; acima do máximo. A semântica técnica disponível é `shareBelow` (peso com welfare estritamente menor) e `shareAtOrBelow` (peso com welfare menor ou igual); wording, arredondamento, TOP, golden cases e UX continuam bloqueados.

## Provenance e determinismo

O arquivo de configuração registra catálogo, recurso, URL, conteúdo esperado, data de acesso, versão, build, ano, PPP, unidade, caminhos e endpoints. Cada resposta oficial bruta possui SHA-256 no relatório. Duas reconstruções consecutivas com a mesma entrada produziram os mesmos hashes da candidata e do relatório. A dependência externa remanescente é a obtenção inicial do raw e dos checkpoints; depois de preservados, os inputs ficam auditáveis por hash.

## Riscos

- **BLOQUEADOR:** nenhum conhecido para decidir fonte e CDF de D068.
- **ALTO:** nenhum.
- **MÉDIO:** perda de desigualdade intrabin; a Data Catalog alerta que a base binned não substitui estatísticas diretas do PIP. A precisão aceitável deve ser aprovada, não presumida.
- **MÉDIO:** o endpoint oficial de agregados expõe a produção vigente, não um parâmetro público de build; o endpoint de citação confirmou a build esperada nesta execução, e as respostas foram preservadas por hash.
- **BAIXO:** os headcounts do comparador oficial são publicados com quatro casas decimais; parte do erro medido pode ser arredondamento, não discretização da candidata.
- **BAIXO:** a população difere em cerca de 45 pessoas por arredondamento entre bins e agregado publicado.
- **BAIXO:** o candidato JSON de pesquisa tem cerca de 11,4 MB; eventual formato de produção e estratégia de entrega pertencem a decisão posterior, sem alterar a metodologia.

## Proposta de decisão D068 — não ativa

> **D068 — Fonte operacional e construção da CDF mundial.** A distribuição mundial será derivada do dataset oficial World Bank/Poverty and Inequality Platform **1000 Binned Global Distribution**, recurso `DR0094423`, arquivo `GlobalDist1000bins_1990_2026_20260324_2021_01_02_PROD.csv`, build `20260324_2021_01_02_PROD`, PPP 2021 e ano de referência 2024, em conformidade com D066 e D067. Para 2024, selecionar exatamente as 218 economias e seus 1.000 bins, interpretar `welf` como dólares internacionais PPP 2021 por pessoa por dia e `pop` como milhões de pessoas, ordenar globalmente por `welf`, agrupar empates e acumular `pop` para formar uma CDF em degraus. Missing, valores não finitos, welfare negativo e população não positiva invalidam a construção; não há imputação, interpolação ou extrapolação. O lookup deverá expor separadamente `shareBelow` e `shareAtOrBelow`. A fonte, os inputs, a pipeline, os outputs e os checkpoints oficiais serão fixados por versão e SHA-256. A aproximação intrabin é aceita com base no erro observado nesta validação — máximo de `0,0225169918` ponto percentual em 18 checkpoints oficiais — sem transformar esse valor em regra de apresentação. D069 continua responsável pela conversão da entrada para PPP 2021 por pessoa por dia; D070 continua responsável por precisão, caudas, golden cases e linguagem. A canonização de D068 não habilita o motor Mundo no frontend.

## Recomendação

Revisar e, se a aproximação intrabin for aceita explicitamente, canonizar D068. Não iniciar D069 automaticamente.
