---
title: Fase 2C — Protocolo de Conversão BRL para PPP 2021
created: 2026-08-14T17:18:00-03:00
status: protocolo de validação
canonical: false
depends_on:
  - D066
  - D067
---

# Fase 2C — Protocolo de Conversão BRL Corrente para PPP 2021

> **PROTOCOLO TÉCNICO — NÃO CANÔNICO.**
> Este documento define como fechar D069 sem reutilizar constantes do protótipo.
> Ele não fixa ainda o valor da PPP brasileira de 2021 nem o CPI usado pelo PIP.

## 1. Objetivo

Transformar:

```text
renda mensal nominal corrente em BRL
```

em:

```text
dólares internacionais PPP 2021
por pessoa por dia
```

de forma:

- reproduzível;
- compatível com a versão PIP congelada;
- auditável;
- independente das constantes antigas do frontend.

---

## 2. Regra de fonte

A primeira fonte para os fatores usados pelo cálculo mundial deve ser a **mesma versão PIP** definida em D066.

Não reutilizar por inércia:

```text
PPP_2021_BRL = 2.4499
BRAZIL_CPI_2024
BRL_PER_INTL_2024
```

do protótipo.

Não substituir silenciosamente a tabela PIP por WDI.

WDI/ICP pode ser usado como:

```text
sanity check
comparação
diagnóstico
```

mas qualquer divergência precisa ser explicada.

---


## 2A. Cliente oficial atual e semântica dos parâmetros

A implementação oficial atual deve ser tomada do repositório:

```text
worldbank/pipr
```

No arquivo `R/get_aux.R`, os helpers:

```r
get_ppp()
get_cpi()
```

chamam respectivamente:

```r
get_aux("ppp")
get_aux("cpi")
```

### Nuance importante

Embora as assinaturas públicas exponham `ppp_version`, a implementação atual de `get_aux()` não repassa esse argumento para a construção da requisição auxiliar quando uma tabela é solicitada.

A requisição é construída com os campos efetivamente encaminhados, entre eles:

```text
table
version
release_version
format
```

Consequência:

> **não assumir que `get_ppp(ppp_version = 2021)` ou `get_cpi(ppp_version = 2021)` filtra a tabela auxiliar pela PPP desejada.**

A reprodução correta deve:

1. congelar a release PIP;
2. baixar a tabela auxiliar dessa release;
3. inspecionar seu schema e seus campos de versão/base;
4. selecionar a linha/coluna correta somente a partir da resposta observada.

Isso é especialmente importante porque o argumento existir na interface da função não prova que ele altera o endpoint auxiliar.

Fonte técnica primária:

```text
https://github.com/worldbank/pipr
R/get_aux.R
```

---

## 3. Evidência do cliente oficial

O wrapper oficial Stata do Banco Mundial, repositório:

```text
https://github.com/worldbank/pip
```

constrói a consulta de tabelas auxiliares como:

```text
aux?table=<tabela>&version=<pip_version>&format=csv
```

O pacote `pipr` também expõe `get_aux()` e atalhos específicos.

O código do pacote confirma:

```r
get_cpi(...)
→ get_aux("cpi", ...)

get_ppp(...)
→ get_aux("ppp", ...)
```

Portanto, as tabelas preferenciais para D069 são:

```text
aux / ppp
aux / cpi
```

na mesma release PIP.

---

## 4. Versão a congelar nas consultas

As consultas devem ser vinculadas à versão canonizada:

```text
PIP_VERSION_CITATION = 20260324_2021
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
PPP_BASE = 2021
```

Não usar:

```text
latest
current
versão descoberta automaticamente
```

sem uma nova decisão.

---

## 5. Extração da PPP

Da tabela:

```text
aux?table=ppp
```

localizar a linha do Brasil pelo código oficial retornado.

Antes de usar o valor, registrar:

```text
country_code
country_name, se houver
ppp field name
ppp value
ppp base/year
version
unit
```

### Regra

Não adivinhar o nome da coluna.

O schema efetivamente retornado pela release deve ser armazenado no relatório de validação.

---

## 6. Extração do CPI

Da tabela:

```text
aux?table=cpi
```

localizar todas as observações necessárias do Brasil.

Registrar:

```text
country_code
time/year/month fields
cpi field name
cpi values
reference/base metadata
version
```

A transformação temporal deve seguir o significado das colunas retornadas pela PIP, não uma fórmula genérica escolhida antecipadamente.

---

## 7. Pergunta metodológica central

Precisamos demonstrar exatamente a ponte:

```text
BRL corrente
→
BRL em referência monetária compatível com a PPP 2021
→
PPP 2021 internacional
```

Há duas possibilidades conceituais que devem ser testadas, sem canonização antecipada.

### Caminho A — fator direto derivado das auxiliares PIP

Se a release fornecer combinação operacional suficiente para levar diretamente o valor corrente ao ano/base exigido:

```text
BRL_corrente × temporal_factor_PIP / PPP_2021
```

### Caminho B — reconstrução explícita do alinhamento temporal

Se o CPI for uma série de níveis:

```text
BRL_2021_equiv
=
BRL_corrente × CPI_2021_reference / CPI_current_reference
```

e:

```text
PPP_monthly_2021
=
BRL_2021_equiv / PPP_BRA_2021
```

### Regra

A e B só podem ser considerados equivalentes depois de comprovação numérica com os campos reais da release.

---

## 8. Conversão mensal para diária

Depois de obter o valor mensal por pessoa em dólares internacionais PPP 2021:

```text
daily_ppp
=
monthly_ppp × 12 / 365
```

Essa regra deve ser aplicada uma única vez.

Não usar simultaneamente:

```text
30 dias
365/12
12/365
```

em diferentes partes do sistema.

O projeto deve escolher uma única constante canônica:

```text
DAYS_PER_MONTH_EQUIVALENT = 365 / 12
```

ou a forma algébrica equivalente:

```text
daily = monthly × 12 / 365
```

---

## 9. Ordem correta do cálculo

Entrada:

```text
household_income_current_brl
eligible_residents
```

Primeiro:

```text
per_capita_current_brl
=
household_income_current_brl / eligible_residents
```

Depois, transformação monetária mundial:

```text
per_capita_current_brl
↓
temporal alignment PIP
↓
PPP conversion
↓
daily PPP 2021
```

Como todos os fatores monetários são uniformes e positivos, aplicar o fator antes ou depois da divisão por moradores deve ser matematicamente equivalente.

Criar teste de invariância.

---

## 10. Relação com D065

D065 é a regra **Brasil**:

```text
BRL corrente
→
preços médios de 2025
→
CDF PNAD 2025
```

D069 será uma regra **Mundo**:

```text
BRL corrente
→
referência exigida pela PIP
→
PPP 2021
→
CDF mundial 2024
```

Não encadear automaticamente:

```text
D065
↓
D069
```

a menos que se demonstre que a transformação composta é numericamente equivalente ao procedimento PIP.

A separação conceitual deve permanecer explícita.

---

## 11. Testes numéricos obrigatórios

Depois de obter as tabelas auxiliares, criar fixtures para:

```text
R$ 0 / 1
R$ 1.000 / 1
R$ 6.500 / 3
R$ 12.000 / 3
R$ 20.000 / 4
R$ 50.000 / 4
R$ 100.000 / 1
```

Cada caso deve registrar:

```text
input_household_brl
residents
input_per_capita_brl
price_reference_used
ppp_factor_used
monthly_ppp_2021
daily_ppp_2021
```

Ainda sem percentil mundial até D068.

---

## 12. Teste de ida e volta

Se a transformação corrente → PPP puder ser invertida:

```text
BRL_current
→
PPP_2021
→
BRL_current_reconstructed
```

Esperado:

```text
abs(original - reconstructed) <= tolerance_numeric
```

A tolerância deve cobrir apenas erro numérico, não erro metodológico.

---

## 13. Teste de monotonicidade

Para fator monetário positivo:

```text
income_1 < income_2
=>
ppp_daily_1 < ppp_daily_2
```

Criar teste com ampla faixa de renda.

Qualquer violação significa erro de implementação.

---

## 14. Teste de escala

Se moradores forem constantes:

```text
income × 2
```

deve produzir:

```text
daily_ppp × 2
```

antes de consultar a CDF.

A transformação monetária é linear.

---

## 15. Teste de equivalência da ordem

Comparar:

```text
A = convert_to_ppp(household_income) / residents
```

com:

```text
B = convert_to_ppp(household_income / residents)
```

Esperado:

```text
A ≈ B
```

dentro de tolerância numérica.

---

## 16. Sanity check externo

Comparar a PPP brasileira de 2021 obtida da release PIP com fonte oficial externa compatível, por exemplo:

```text
World Bank / ICP / WDI
PA.NUS.PRVT.PP
```

Registrar:

```text
pip_value
external_value
absolute_difference
relative_difference
```

### Regra

Se houver divergência:

> **não escolher o valor que “parece melhor”.**

Investigar:

- vintage;
- revisão;
- conceito;
- ano-base;
- unidade;
- arredondamento;
- série.

---

## 17. Atualização temporal

O manifesto do cálculo mundial deve informar qual observação CPI é usada para a renda corrente.

Não consultar “último CPI” silenciosamente a cada cálculo.

Fluxo futuro:

```text
nova observação aprovada
↓
importação
↓
validação
↓
manifesto novo
↓
testes
↓
aprovação
↓
publicação
```

A CDF mundial 2024 e a referência PPP 2021 podem permanecer congeladas enquanto o pequeno manifesto temporal é atualizado controladamente.

---

## 18. Manifesto candidato de conversão

Estrutura conceitual:

```json
{
  "status": "CANDIDATE",
  "pipVersion": "20260324_2021",
  "productionBuild": "20260324_2021_01_02_PROD",
  "pppBase": 2021,
  "country": "BRA",
  "pppSource": "PIP aux/ppp",
  "cpiSource": "PIP aux/cpi",
  "pppValue": null,
  "priceReference": null,
  "formula": null,
  "sourceChecksums": {
    "ppp": null,
    "cpi": null
  },
  "frontendIntegrationAllowed": false
}
```

---

## 19. Gate para D069

D069 só pode ser proposta como `ATIVA` quando:

- [ ] tabela `ppp` da release congelada foi obtida;
- [ ] tabela `cpi` da release congelada foi obtida;
- [ ] schema das duas respostas foi preservado;
- [ ] Brasil foi identificado sem ambiguidade;
- [ ] valor PPP exato registrado;
- [ ] unidade PPP confirmada;
- [ ] observações CPI necessárias identificadas;
- [ ] fórmula temporal derivada do significado real dos campos;
- [ ] conversão mensal → diária definida;
- [ ] teste de ida e volta passou;
- [ ] monotonicidade passou;
- [ ] linearidade passou;
- [ ] equivalência da ordem passou;
- [ ] sanity check externo documentado;
- [ ] nenhum uso das constantes antigas do frontend;
- [ ] manifesto e checksums gerados.

---

## 20. Saídas esperadas da execução

Quando houver ambiente com acesso à API:

```text
validation/world/pip-ppp-brazil-2021.csv
validation/world/pip-cpi-brazil.csv
validation/world/world-price-conversion-validation.md
validation/world/world-price-conversion-validation.json
validation/world/world-price-alignment-candidate.json
```

Nenhum desses arquivos deve ser promovido a produção antes de D069.
