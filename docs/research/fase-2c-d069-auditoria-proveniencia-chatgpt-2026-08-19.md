---
title: "Fase 2C — D069 — Auditoria de Proveniência realizada no ChatGPT"
date: 2026-08-19
status: "pesquisa auditada — gate de proveniência não fechado"
canonical: false
decision: "D069 permanece BLOQUEADA / PENDENTE"
scope: "proveniência da conversão BRL corrente → PPP 2021 compatível com PIP"
---

# Fase 2C — D069 — Auditoria de Proveniência realizada no ChatGPT

> **DOCUMENTO DE PESQUISA — NÃO CANÔNICO**
>
> Este documento preserva o resultado curado da pesquisa e auditoria realizadas no Projeto ChatGPT Renda Comparada em 19/08/2026.
>
> Ele **não canoniza D069**, não altera `docs/decisoes.md`, não autoriza D070 e não autoriza integração do motor Mundo.

## 1. Objetivo

Auditar o gate de proveniência da D069:

> conversão de renda domiciliar nominal corrente em BRL para dólares internacionais PPP/PPC 2021 por pessoa por dia, em unidade compatível com a distribuição mundial do World Bank Poverty and Inequality Platform — PIP.

O trabalho foi executado fora do Codex para reduzir pesquisa e análise que não dependiam do checkout.

## 2. Estado de entrada

O estado mais recente do checkout/documentação recebido pelo ChatGPT indicava:

- D066: canônica/ativa;
- D067: canônica/ativa;
- D068: candidata executada e validada, ainda não canônica;
- D069: não executada no checkout e não canônica;
- D070: não executada no checkout e não canônica;
- motor Mundo: bloqueado para produção e frontend.

Consequentemente, o resultado desta auditoria não deve ser descrito como “reabertura de uma decisão canônica já fechada”.

## 3. Trabalho realizado

Foram analisados:

1. dois relatórios independentes de Pesquisa Aprofundada produzidos a partir do prompt específico do Gate D069;
2. documentação oficial do World Bank/PIP;
3. implementação oficial dos clientes PIP;
4. metodologia oficial PIP para CPI e PPP;
5. ICP 2021 como cross-check;
6. IBGE/SIDRA/IPCA como fonte candidata para a ponte renda corrente → referência 2024;
7. cálculos independentes de coerência dimensional, round-trip e sensibilidade.

## 4. Fatos confirmados

### 4.1 Release e build PIP

Confirmados para o trabalho:

```text
PIP_VERSION = 20260324_2021
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
GLOBAL_REFERENCE_YEAR = 2024
PPP_BASE = 2021
```

A documentação oficial consultada sustenta o uso de PPPs 2021 e a interpretação de 2024 como referência anterior aos nowcasts posteriores.

### 4.2 Estrutura da API auxiliar

Foi confirmada, por documentação/código oficial, a existência do recurso:

```text
/pip/v1/aux
```

e o padrão de consulta equivalente a:

```text
aux?table=ppp&version=20260324_2021&format=csv
aux?table=cpi&version=20260324_2021&format=csv
```

A estrutura da consulta foi confirmada.

### 4.3 Ordem metodológica CPI → PPP

A metodologia oficial PIP confirma a sequência conceitual:

```text
welfare em moeda nacional
↓
CPI para comparação temporal dentro do país
↓
PPP para comparação internacional
↓
dólares internacionais PPP 2021
```

Também foi confirmado conceitualmente que:

- CPI é utilizado para expressar welfare em preços comparáveis dentro do país;
- o CPI anual é construído, em regra, pela média simples da série mensal;
- a série é rebaseada ao ano de referência do ICP, atualmente 2021;
- a principal fonte de CPI do PIP é IMF IFS, com fontes alternativas quando necessário;
- PPPs de consumo do ICP são a regra para medição global de pobreza, salvo exceções documentadas;
- Brasil não apareceu entre as exceções metodológicas consultadas.

## 5. Hipóteses numéricas auditadas

A pesquisa anterior havia produzido como candidatos:

```text
PPP_BRA_2021 ≈ 2.4499
CPI_BRA_2024_BASE_2021 ≈ 1.1929
BRL_PER_INTL_2024 ≈ 2.92248571
```

e, para a ponte de preços corrente → 2024:

```text
IPCA_MEDIO_2024 ≈ 6952.073333333333...
IPCA_2026_07 ≈ 7657.73
```

Fórmula candidata:

```text
dailyPPP =
    (householdIncomeCurrent / residents)
    × (IPCA_AVG_2024 / IPCA_CURRENT)
    ÷ (PPP_2021 × CPI_2024_BASE_2021)
    × 12 / 365
```

## 6. O que a auditoria confirmou sobre a fórmula

Condicionada aos fatores acima, a fórmula é:

- linear em relação à renda;
- monotônica;
- positiva para renda positiva;
- zero para renda zero;
- inversamente proporcional ao número de moradores;
- dimensionalmente coerente;
- reversível dentro do erro numérico de arredondamento.

A identidade:

```text
PPP_2021 × CPI_2024_BASE_2021
```

é conceitualmente compatível com a sequência PIP CPI → PPP, desde que os dois fatores efetivamente correspondam aos valores da mesma vintage PIP utilizada.

## 7. Reprodução numérica condicional

Com os candidatos:

```text
PPP = 2.4499
CPI_2024_BASE_2021 = 1.1929
IPCA_MEDIO_2024 = 6952.073333333333
IPCA_2026_07 = 7657.73
```

temos:

```text
BRL_PER_INTL_2024
= 2.4499 × 1.1929
= 2.92248571
```

Para:

```text
renda domiciliar mensal atual = R$ 6.500
moradores = 3
```

o resultado reproduzido foi aproximadamente:

```text
22.1280111755 int$ PPP 2021 / pessoa / dia
```

O round-trip reconstrói aproximadamente R$ 6.500/mês, com diferença apenas de ponto flutuante/arredondamento.

### Importante

Essa reprodução valida a **aritmética da hipótese**.

Ela **não valida a proveniência dos fatores**.

## 8. Divergência material encontrada

O principal achado de falsificação foi:

```text
PPP candidata PIP = 2.4499
ICP 2021 — households + NPISH final consumption = ~2.379
```

Diferença aproximada:

```text
0.0709 BRL/int$
≈ 2.98%
```

Essa diferença é grande demais para ser tratada como simples arredondamento.

### Interpretação correta

O valor ICP de aproximadamente `2.379` **não deve substituir automaticamente** o candidato `2.4499`.

Ele funciona como cross-check e sinaliza que a origem do valor PIP precisa ser provada diretamente.

Possibilidades ainda não demonstradas incluem:

- vintage específica do PIP;
- transformação específica;
- conceito de PPP distinto;
- revisão de série;
- campo interno diferente;
- erro na hipótese anterior.

Nenhuma dessas explicações deve ser promovida a fato sem a resposta efetiva de `aux/ppp`.

## 9. Evidência que continua faltando

Não foi possível preservar, nesta investigação, o corpo efetivamente retornado das duas consultas congeladas:

```text
https://api.worldbank.org/pip/v1/aux?table=ppp&version=20260324_2021&format=csv
https://api.worldbank.org/pip/v1/aux?table=cpi&version=20260324_2021&format=csv
```

Portanto continuam não confirmados:

- schema real de `aux/ppp`;
- linha Brasil de `aux/ppp`;
- nome literal do campo PPP;
- valor PIP exato para o Brasil;
- unidade exata registrada na tabela;
- schema real de `aux/cpi`;
- linha Brasil de `aux/cpi`;
- nome literal do campo CPI;
- valor 2024/base 2021;
- explicação oficial da divergência `2.4499` versus `2.379`.

## 10. Ponte renda corrente → referência 2024

Foi considerada defensável, mas ainda não canonizada, a seguinte ponte:

```text
BRL corrente
↓
IPCA IBGE
↓
BRL em preços médios de 2024
↓
CPI/PPP PIP
↓
int$ PPP 2021
```

Essa primeira etapa não deve ser descrita como regra do PIP.

É uma possível decisão metodológica específica do Renda Comparada.

Antes de canonizar, recomenda-se comparar quantitativamente:

```text
IPCA IBGE 2021→2024
versus
CPI efetivamente utilizado pelo PIP 2021→2024
```

Se a divergência for material, a ponte deve ser reavaliada.

## 11. Veredito auditado

### Estado da decisão

```text
D069 = BLOQUEADA / PENDENTE
```

### Resultado desta tentativa de gate

```text
Gate de proveniência D069 = FAIL nesta tentativa
```

### Razão

A arquitetura matemática é plausível e a aritmética foi reproduzida, mas faltam os raws oficiais congelados que provem os fatores numéricos centrais.

### Decisão humana recomendada neste ponto

```text
CANONIZAR D069? NÃO
```

## 12. O que não deve ser feito ainda

Não:

- canonizar D069;
- editar `docs/decisoes.md` para marcar D069 como ativa;
- executar ou promover D070;
- recalcular percentis mundiais de produção;
- substituir `2.4499` por `2.379` por conveniência;
- integrar Mundo no frontend;
- modificar o motor Brasil;
- reusar constantes legadas do protótipo;
- tratar os valores condicionais como produção.

## 13. Próximo gate recomendado

O próximo passo deve ser operacional e mínimo:

1. capturar a resposta bruta de `aux/ppp` na release `20260324_2021`;
2. capturar a resposta bruta de `aux/cpi` na mesma release;
3. preservar cada arquivo integralmente;
4. registrar URL/query utilizada;
5. registrar timestamp de acesso;
6. registrar tamanho;
7. calcular SHA-256;
8. registrar schema/cabeçalhos reais;
9. extrair a linha do Brasil;
10. devolver os valores e campos sem reinterpretá-los;
11. não canonizar nada automaticamente.

Depois dessa execução, o resultado deve voltar ao ChatGPT para auditoria antes de qualquer decisão posterior.

## 14. Artefatos futuros esperados da execução

Nomes sugeridos:

```text
docs/research/artifacts/world/pip-20260324_2021-ppp.raw.csv
docs/research/artifacts/world/pip-20260324_2021-cpi.raw.csv
docs/research/artifacts/world/pip-20260324_2021-aux-provenance.json
```

O manifesto de proveniência deveria registrar pelo menos:

- source;
- endpoint;
- query;
- release;
- accessedAt;
- sha256;
- sizeBytes;
- table;
- schema;
- countryCode;
- row/field utilizado.

Esses arquivos permanecem **evidência de pesquisa**, não produção, até decisão explícita posterior.

## 15. Fontes primárias centrais

- World Bank — Poverty and Inequality Platform (PIP)
- World Bank — PIP API
- `worldbank/pipr`
- `worldbank/pip`
- `worldbank/PIP-Methodology`
- World Bank — International Comparison Program (ICP) 2021
- World Bank — WDI `PA.NUS.PRVT.PP` apenas como cross-check
- IBGE — SIDRA tabela 1737 / IPCA

## 16. Regra epistemológica

Preservar a distinção:

```text
pesquisado
≠
executado
≠
validado
≠
canonizado
≠
integrado
≠
publicado
```

Este documento registra **pesquisa auditada**.

Não constitui decisão canônica.
