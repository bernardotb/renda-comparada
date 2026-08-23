---
title: Fase 2B — Protocolo de Validação da CDF Mundial
created: 2026-08-14T17:05:00-03:00
status: protocolo de validação
canonical: false
depends_on:
  - D066
  - D067
---

# Fase 2B — Protocolo de Validação da CDF Mundial

> **PROTOCOLO TÉCNICO — NÃO CANÔNICO.**
> Este documento define como a CDF mundial candidata deve ser testada antes de qualquer D068.
> Ele não aprova a base de 1.000 faixas nem define tolerâncias sem evidência empírica.

## 1. Objetivo

Avaliar se a `1000 Binned Global Distribution`, vintage PIP março/2026, é suficientemente fiel ao agregado mundial oficial do PIP para sustentar uma posição `TOP X%` na V1.

A pergunta não é:

> “a base parece plausível?”

A pergunta é:

> **“o erro introduzido pela representação em faixas é pequeno, estável, reproduzível e compatível com a precisão que pretendemos mostrar?”**

---

## 2. Fonte candidata

```text
World Bank — 1000 Binned Global Distribution
PIP vintage = March 2026
GLOBAL_REFERENCE_YEAR = 2024
PPP_BASE = 2021
```

Campos mínimos esperados:

```text
code
year
quantile
welf
pop
```

onde:

- `welf` é o bem-estar médio da faixa em dólares internacionais PPP 2021 por pessoa/dia;
- `pop` é a população representada pela faixa.

Antes do processamento, registrar:

```text
source_url
accessed_at
source_file_name
source_sha256
row_count_raw
economies_raw
years_available
```

---

#
## 2A. Arquivo exato identificado

O catálogo oficial expõe para a vintage congelada:

```text
resourceId = DR0094423
arquivo = GlobalDist1000bins_1990_2026_20260324_2021_01_02_PROD.csv
URL = https://datacatalogfiles.worldbank.org/ddh-published/0064304/DR0094423/GlobalDist1000bins_1990_2026_20260324_2021_01_02_PROD.csv
tamanho publicado = 948,8 MB
atualização = 30/03/2026
```

O próprio Data Catalog oferece um `API Service` associado ao recurso, com parâmetros de paginação, filtro e seleção. Para a V1, preferir consulta filtrada a `year = 2024` ou leitura em streaming, evitando download/processamento desnecessário de todos os anos.

A URL e o tamanho acima identificam o artefato; não substituem checksum local, que deve ser registrado na execução.

---

# 3. Filtro temporal

A CDF candidata da V1 usa somente:

```text
year = 2024
```

Não misturar:

```text
2023
2025
2026
```

Não substituir por `latest`.

Não misturar nowcast com o ano congelado por D066.

---

## 4. Validação estrutural da base

Antes de construir qualquer CDF, verificar:

### Quantile

Por economia/ano:

```text
1 <= quantile <= 1000
```

Verificar:

- faixa esperada;
- duplicatas;
- quantis ausentes;
- quantidade de bins por economia;
- variações justificadas.

### Welfare

```text
welf >= 0
finite(welf) = true
```

Registrar:

```text
min_welf
max_welf
missing_welf
zero_welf
negative_welf
nonfinite_welf
```

### Population

```text
pop > 0
finite(pop) = true
```

Registrar:

```text
total_pop
missing_pop
zero_pop
negative_pop
nonfinite_pop
```

### Chaves

A combinação adequada de:

```text
code + year + quantile
```

deve ser única, salvo documentação explícita em contrário.

---

## 5. População representada

Somar `pop` para 2024.

Comparar com a população do agregado mundial retornada pela mesma release PIP quando disponível.

Não usar população mundial de outra fonte para “corrigir” silenciosamente os pesos.

Registrar:

```text
population_binned
population_pip_wld
population_difference
population_difference_pct
```

Diferença material precisa ser explicada antes de qualquer CDF.

---

## 6. Construção da CDF candidata

Para todas as faixas válidas de 2024:

```text
ordenar por welf crescente
↓
agrupar valores welf iguais
↓
somar pop em cada welf
↓
acumular pop
```

Definir:

```text
P_total = soma(pop)
```

Para valor `x`:

```text
shareBelow(x)
= soma(pop onde welf < x) / P_total
```

```text
shareAtOrBelow(x)
= soma(pop onde welf <= x) / P_total
```

```text
topShare(x)
= 1 - shareBelow(x)
```

### Regra

Não interpolar durante a primeira validação.

A primeira comparação deve medir o erro da CDF em degraus produzida diretamente pelos bins.

Qualquer interpolação posterior é uma nova hipótese e deve ser testada separadamente.

---

## 6A. Benchmark pré-registrado — US$ 3,00

Antes de construir a CDF candidata, fica registrado um benchmark oficial independente da representação em bins:

```text
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
GLOBAL_REFERENCE_YEAR = 2024
PPP_BASE = 2021
POVERTY_LINE = 3.00 intl$ / pessoa / dia
WORLD_POP_BELOW = 846.76 milhões
```

Fonte: tabela pública do Poverty and Inequality Platform do Banco Mundial, consultada em 14/08/2026.

Este benchmark **não deve ser usado para calibrar manualmente** a CDF. Ele é apenas um ponto de validação pré-registrado.

As linhas de US$ 4,20 e US$ 8,30 possuem códigos oficiais no WDI/PIP (`SI.POV.LMIC` e `SI.POV.UMIC`), mas os resultados públicos recuperados nesta etapa não identificaram de forma inequívoca o valor Mundo/2024 da mesma release. Portanto, esses números não são pré-preenchidos e devem ser obtidos diretamente por `pip wb`/`pip-grp` na execução.

---

## 7. Checkpoints oficiais

Obter do agregado oficial `pip wb` / `pip-grp`, na mesma release e ano, os headcounts em:

```text
3.00
4.20
5.00
8.30
10.00
30.00
```

em dólares internacionais PPP 2021 por pessoa/dia.

Os três pontos adicionais (`5`, `10`, `30`) são escolhidos antes de observar os resultados para reduzir risco de ajuste oportunista.

Para cada ponto `x`:

```text
official = headcount_PIP_WLD(x)
candidate = shareBelow_CDF_binned(x)
```

Registrar:

```text
error_signed = candidate - official
error_abs = abs(candidate - official)
error_pp = 100 * error_abs
```

---

## 8. Métricas de erro

Calcular no conjunto de checkpoints:

```text
max_error_pp
mean_error_pp
median_error_pp
rmse_pp
signed_mean_error_pp
```

Também registrar a direção dos erros.

Se todos os erros forem sistematicamente positivos ou negativos, investigar a construção antes de discutir tolerância.

---

## 9. Grade adicional de validação

Se o endpoint oficial permitir várias linhas monetárias, ampliar o teste para uma grade pré-definida, por exemplo:

```text
1
2
3
4.2
5
6
8.3
10
12
15
20
30
40
50
70
100
150
200
```

A grade deve ser definida antes da coleta da resposta final.

Objetivo:

- medir o erro ao longo da distribuição;
- detectar zonas em que a aproximação por bins degrada;
- verificar caudas;
- evitar que seis pontos escondam problemas intermediários.

---

## 10. Monotonicidade

Na CDF candidata:

```text
x1 < x2
=> CDF(x1) <= CDF(x2)
```

Nos headcounts oficiais:

```text
poverty_line_1 < poverty_line_2
=> headcount_1 <= headcount_2
```

Qualquer violação deve bloquear a execução e gerar relatório.

---

## 11. Quantis derivados

Somente depois de a CDF candidata passar na validação por linhas monetárias, calcular quantis diagnósticos:

```text
P1
P5
P10
P25
P50
P75
P90
P95
P99
P99.5
P99.9
```

Esses quantis são propriedades da **CDF candidata**, não valores oficiais diretamente publicados pelo PIP.

A documentação deve manter essa distinção.

---

## 12. Empates

Se várias faixas/economias possuírem o mesmo `welf`:

- agregar o peso no mesmo ponto;
- preservar o degrau;
- não repartir artificialmente o peso empatado.

Registrar:

```text
weightAt
cumBelow
cumAtOrBelow
```

A política final de linguagem deve escolher explicitamente entre `shareBelow` e `shareAtOrBelow`.

---

## 13. Cauda inferior

Testar:

```text
x = 0
x < min_positive_welf
x = min_welf
```

Não criar piso artificial como:

```text
0.1%
```

Se a base não sustentar precisão na cauda inferior, a UI deve degradar a precisão ou usar linguagem de limite.

---

## 14. Cauda superior

Testar:

```text
x = max_welf
x > max_welf
x muito acima do max_welf
```

Não permitir:

- extrapolação logarítmica inventada;
- teto arbitrário 99,99%;
- criação de percentis fora da evidência.

Se o usuário estiver além da cobertura representada, a UI deve usar regra explícita de limite.

---

## 15. Determinismo

Executar duas vezes com:

- mesmo arquivo;
- mesma versão;
- mesmo código;
- mesma ordenação.

Esperado:

```text
cdf_sha256_run_1 == cdf_sha256_run_2
```

Também:

```text
metrics_sha256_run_1 == metrics_sha256_run_2
```

---

## 16. Manifesto da CDF candidata

Artefato mínimo:

```json
{
  "status": "CANDIDATE",
  "source": "World Bank 1000 Binned Global Distribution",
  "pipVersion": "20260324_2021",
  "productionBuild": "20260324_2021_01_02_PROD",
  "referenceYear": 2024,
  "pppBase": 2021,
  "sourceSha256": "...",
  "cdfSha256": "...",
  "population": "...",
  "uniqueWelfarePoints": 0,
  "validation": {
    "checkpoints": [],
    "maxErrorPp": null,
    "meanErrorPp": null,
    "rmsePp": null
  },
  "frontendIntegrationAllowed": false
}
```

---

## 17. Como decidir a tolerância

A tolerância não deve ser escolhida para “fazer a base passar”.

A sequência correta é:

```text
medir erro
↓
observar padrão
↓
comparar com precisão desejada na UI
↓
definir tolerância
↓
aceitar ou rejeitar
```

Exemplo conceitual:

Se o produto pretende mostrar:

```text
TOP 12%
```

e o método pode deslocar o resultado entre:

```text
TOP 11%
e
TOP 14%
```

a precisão de inteiro pode ser enganosa.

Nesse caso as opções legítimas seriam:

- melhorar a fonte/método;
- reduzir a precisão da apresentação;
- mostrar intervalo;
- rejeitar a funcionalidade mundial na V1.

Não mascarar a incerteza com arredondamento conveniente.

---

## 18. Gate para D068

D068 só pode ser proposta como `ATIVA` quando:

- [ ] fonte de 1.000 bins identificada e congelada;
- [ ] checksum da fonte registrado;
- [ ] ano 2024 isolado;
- [ ] estrutura da base validada;
- [ ] população reconciliada;
- [ ] CDF determinística;
- [ ] `pip wb` reproduzido na mesma release;
- [ ] pelo menos seis checkpoints comparados;
- [ ] grade ampliada testada quando operacional;
- [ ] erro máximo e médio medidos;
- [ ] caudas verificadas;
- [ ] empates definidos;
- [ ] tolerância decidida depois dos resultados;
- [ ] precisão de UI compatível com o erro;
- [ ] nenhum hardcode corretivo;
- [ ] nenhum fallback para `WORLD_CURVE`.

---

## 19. Saídas esperadas da execução

Quando houver ambiente capaz de baixar a base e chamar a API PIP:

```text
validation/world/world-cdf-validation.md
validation/world/world-cdf-validation.json
validation/world/world-cdf-checkpoints.csv
validation/world/world-income-cdf-candidate.json
```

Nenhum desses arquivos deve ser marcado como produção até aprovação de D068.
