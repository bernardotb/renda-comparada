---
title: Fase 2A — Reprodução da API PIP
created: 2026-08-14T16:50:00-03:00
status: procedimento de reprodução — revisão 0.2
canonical: false
---

# Fase 2A — Reprodução da API PIP

> **PROCEDIMENTO TÉCNICO — NÃO CANÔNICO.**
> Este arquivo não define D068, D069 ou D070. Ele apenas fixa as consultas e evidências necessárias para que essas decisões possam ser tomadas sem improvisação.

## 1. Objetivo

Fechar os três bloqueios restantes do motor Mundo da V1:

```text
D068 — fonte e construção operacional da distribuição mundial
D069 — conversão BRL corrente → dólares internacionais PPP 2021
D070 — empates, caudas, golden cases e precisão de exibição
```

A versão já congelada por D066 é:

```text
PIP_VERSION_CITATION = 20260324_2021
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
GLOBAL_REFERENCE_YEAR = 2024
PPP_BASE = 2021
```

A interpretação já congelada por D067 é:

> **posição monetária global estimada**, baseada em renda ou consumo domiciliar per capita harmonizados pelo Banco Mundial.

---

## 2. Fonte de verdade

API oficial:

```text
https://api.worldbank.org/pip/v1
```

Cliente oficial de referência:

```text
World Bank — pacote R `pipr`
```

Não utilizar como fonte numérica de produção:

- `WORLD_CURVE` do protótipo;
- vetor manual de aproximadamente 25 pontos;
- `PPP_2021_BRL` hardcoded no frontend antigo;
- `BRAZIL_CPI_2024` hardcoded no frontend antigo;
- WDI atual como substituto automático das tabelas auxiliares da release PIP.

---

# PARTE I — D068: distribuição mundial

## 3. Resultado da verificação do cliente oficial

A primeira hipótese deste procedimento era obter quantis mundiais diretamente com `popshare`.

Essa hipótese foi **rejeitada** após inspeção do cliente oficial `worldbank/pip`, versão atual do wrapper Stata.

A ajuda oficial de `pip cl` / `pip wb` estabelece que:

```text
popshare(#)
```

é uma opção **somente de nível de país** (`pip cl`).

O código de `pip_wb.ado` reforça explicitamente:

```text
option popshare() can't be combined with subcommand wb
```

Portanto:

> **não existe no wrapper oficial um comando `pip wb, popshare(...)` para obter diretamente P10, P50, P90 etc. da distribuição mundial.**

A tentativa anteriormente proposta de enviar `popshare` ao endpoint agregado `pip-grp` não deve ser usada como contrato de produção sem evidência adicional da API.

### Evidência primária

Repositório oficial:

```text
https://github.com/worldbank/pip
```

Arquivos verificados:

```text
pip_cl.sthlp
pip_wb.ado
```

---

## 4. Endpoint agregado oficial para validação por linha monetária

O código oficial de `pip_wb.ado` constrói consultas ao endpoint:

```text
pip-grp
```

com:

```text
group_by=wb
```

e aceita `povline`, não `popshare`.

O próprio wrapper preserva `WLD` entre os códigos oficiais do agregado mundial.

### Validação obrigatória

Consultar 2024 nas seguintes linhas PPP 2021:

```text
$ 3.00
$ 4.20
$ 8.30
```

e em linhas pré-definidas adicionais:

```text
$ 5.00
$ 10.00
$ 30.00
```

Guardar:

```text
poverty_line
headcount
population
pop_in_poverty
estimate_type
version
```

Objetivo: validar qualquer CDF derivada, testar monotonicidade e medir erro em vários pontos.

---

## 5. Estratégia preferencial para construir a CDF mundial

Como `popshare` global não está disponível pelo wrapper oficial, a candidata principal passa a ser:

> **World Bank — 1000 Binned Global Distribution, vintage PIP março/2026**

Procedimento experimental para 2024:

```text
filtrar ano = 2024
↓
usar economias/faixas válidas da vintage congelada
↓
ordenar globalmente por welf
↓
usar pop como peso
↓
acumular população
↓
produzir CDF global experimental
```

Campos centrais:

```text
code
quantile
welf
pop
```

### Limitação obrigatória

A base em faixas perde desigualdade dentro de cada faixa.

Logo:

> **a CDF derivada só poderá virar produção se o erro contra `pip wb` for pequeno e documentado.**

---

## 6. Critério quantitativo para D068

Para cada linha monetária validada:

```text
erro_abs = |CDF_binned(linha) - headcount_PIP(linha)|
erro_pp  = erro_abs × 100
```

A tolerância final será definida **depois** de medir os erros, não antes.

Regras:

1. registrar erro máximo, médio e por checkpoint;
2. verificar se o erro pode alterar materialmente um `TOP X%` mostrado;
3. rejeitar a CDF se o erro for incompatível com a precisão de exibição;
4. nunca corrigir pontos individualmente por hardcode.

---

## 7. Artefato recomendado se a CDF passar

Somente após validação:

```text
data/production/world/world-income-cdf-2024.json
```

Metadados mínimos:

```json
{
  "pipVersion": "20260324_2021",
  "productionBuild": "20260324_2021_01_02_PROD",
  "referenceYear": 2024,
  "pppBase": 2021,
  "source": "World Bank 1000 Binned Global Distribution",
  "validationEndpoint": "pip-grp / group_by=wb",
  "method": "global population-weighted CDF from 1000-bin distribution",
  "validation": {"status": "PENDING"}
}
```

Nenhum artefato mundial está aprovado por este documento.

---

# PARTE II — D069: PPP e CPI

## 8. Tabelas auxiliares da própria PIP

Usar o cliente oficial:

```r
library(pipr)

ppp <- get_ppp(
  release_version = "20260324"
)

cpi <- get_cpi(
  release_version = "20260324"
)
```

O parâmetro `ppp_version` é aceito pela interface pública do cliente, mas a implementação pesquisada do helper auxiliar não deve ser presumida: registrar os campos retornados e a versão efetivamente usada.

---

## 9. Extrair Brasil

Depois de obter as tabelas:

1. localizar Brasil pelo identificador oficial retornado;
2. registrar o fator PPP pertinente à base 2021;
3. registrar CPI/índice de preços necessário à transformação temporal;
4. registrar anos/meses e unidades das colunas;
5. comparar com a série WDI `PA.NUS.PRVT.PP` apenas como sanity check;
6. não substituir automaticamente um valor PIP por um valor WDI se houver divergência.

Campos canônicos futuros:

```text
WORLD_BRAZIL_PPP_2021 = [RESULTADO DA API]
WORLD_BRAZIL_PPP_SOURCE = PIP aux / ppp
WORLD_CPI_SOURCE = PIP aux / cpi
WORLD_CPI_REFERENCE = [RESULTADO DA API]
```

---

## 10. Transformação a validar

A arquitetura conceitual é:

```text
renda nominal brasileira corrente
↓
alinhamento temporal para a referência monetária exigida pela PIP
↓
PPP de consumo compatível com a base 2021
↓
dólares internacionais PPP 2021 por mês
↓
× 12 / 365
↓
dólares internacionais PPP 2021 por pessoa por dia
```

A fórmula numérica definitiva só pode ser escrita depois de inspecionar as tabelas auxiliares da mesma release.

D065 não deve ser reaproveitada mecanicamente como fórmula mundial.

---

# PARTE III — D070: validação e golden cases

## 11. Golden cases mínimos

Depois de D068 e D069:

```text
renda domiciliar R$ 0 / 1 morador
renda domiciliar R$ 6.500 / 3 moradores
renda domiciliar R$ 12.000 / 3 moradores
renda domiciliar R$ 20.000 / 4 moradores
renda domiciliar R$ 50.000 / 4 moradores
valor exatamente em um ponto da distribuição
valor entre dois pontos
valor abaixo do mínimo representado
valor acima do máximo representado
```

Cada fixture deve registrar:

```text
entrada nominal
mês de referência monetária
renda por pessoa
valor PPP diário
shareBelow
shareAtOrBelow, se aplicável
topShare
versão PIP
ano global
```

---

## 12. Tolerância

Não definir `allowed_delta` antes de medir empiricamente:

- erro da representação escolhida contra respostas diretas do PIP;
- erro em vários pontos da distribuição;
- comportamento nas caudas.

Se a solução usar apenas valores diretamente derivados da API e sem aproximação relevante, a tolerância poderá ser muito pequena.

Se usar bins/interpolação, a tolerância deverá ser explicitamente justificada.

---

## 13. Evidências a guardar

Para cada execução de validação:

```text
calculationDate
endpoint
queryParams
releaseVersion
pppVersion
referenceYear
rawResponseSha256
processedArtifactSha256
runtime/tool version
```

Guardar respostas brutas necessárias à auditoria fora do bundle público quando apropriado.

---

## 14. Critério para canonizar D068–D070

Só promover as decisões quando todos os itens abaixo passarem:

- [ ] mesma release PIP em todas as consultas;
- [ ] ano 2024 confirmado nas respostas;
- [ ] Mundo identificado explicitamente;
- [ ] `popshare` reproduzível;
- [ ] linhas monetárias de controle reproduzíveis;
- [ ] PPP do Brasil obtida da tabela auxiliar da release;
- [ ] CPI/ponte temporal obtida da tabela auxiliar da release;
- [ ] transformação BRL → PPP validada;
- [ ] golden cases congelados;
- [ ] caudas e empates documentados;
- [ ] tolerância baseada em erro medido;
- [ ] nenhum uso de `WORLD_CURVE` antigo;
- [ ] nenhum uso de constantes PPP/CPI antigas sem proveniência;
- [ ] artefatos possuem checksum e manifesto.

---

## 15. Limitação do ambiente atual

Em 14/08/2026, a pesquisa conseguiu confirmar a sintaxe e os endpoints por meio de documentação e código-fonte oficial do Banco Mundial, mas as chamadas parametrizadas à API `api.worldbank.org/pip/v1` sofreram timeout no ambiente de navegação disponível.

Isso é uma limitação de execução, não evidência de indisponibilidade da API pública.

Portanto:

> **não transformar timeout local em decisão metodológica.**

A próxima execução deve apenas reproduzir este roteiro em um ambiente com acesso direto ao endpoint.
