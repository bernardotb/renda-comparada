---
title: 09-fontes-referencias
created: 2026-08-12T17:40:00.000-03:00
modified: 2026-08-14T16:12:00.000-03:00
---

# 09-fontes-referencias

# Fontes E Referências — Renda Comparada

**Produto:** Renda Comparada  
**Documento:** `09-fontes-referencias.md`  
**Status:** Canônico para seleção de fontes externas  
**Versão:** 1.2
**Última verificação das fontes:** 14/08/2026

Documentos relacionados:

- `01-visao-produto.md`
- `02-prd-v1.md`
- `03-jornada-ux-v1.md`
- `04-metodologia-dados.md`
- `05-design-system.md`
- `06-privacidade-seguranca.md`
- `07-seo-analytics-crescimento.md`
- `08-roadmap-backlog.md`
- `10-testes-validacao.md`

---

# 1. Função Deste Documento

Este documento centraliza as fontes externas aprovadas ou relevantes para o Renda Comparada.

Ele serve para responder:

> **Qual fonte deve ser utilizada para cada dado, cálculo, conteúdo ou ferramenta?**

O objetivo é evitar:

- fontes contraditórias;
- estatísticas sem origem;
- uso de blogs como base metodológica;
- duplicação de referências;
- troca silenciosa de fontes;
- utilização de dados desatualizados;
- mistura entre fonte primária e inspiração.

---

# 2. Regra De Autoridade

Sempre que possível, utilizar a seguinte hierarquia:

```text
FONTE PRIMÁRIA OFICIAL
↓
DOCUMENTAÇÃO OFICIAL
↓
PUBLICAÇÃO ACADÊMICA / METODOLÓGICA
↓
FONTE SECUNDÁRIA CONFIÁVEL
↓
IMPRENSA
↓
BLOG / SITE COMERCIAL
```

Para cálculos de produção:

> **priorizar sempre a fonte primária oficial.**

---

# 3. Classificação Das Fontes

As fontes deste documento recebem uma classificação.

## `CANÔNICA`

Pode sustentar diretamente cálculo ou dado de produção.

## `OFICIAL-AUXILIAR`

Fonte oficial utilizada para:

- interpretação;
- educação;
- validação;
- ferramentas;
- conteúdo.

Não necessariamente entra no cálculo principal.

## `TÉCNICA`

Documentação oficial para:

- desenvolvimento;
- SEO;
- analytics;
- infraestrutura;
- segurança.

## `LEGAL`

Legislação, regulamentação ou orientação oficial.

## `REFERÊNCIA`

Fonte útil para:

- inspiração;
- comparação;
- pesquisa;
- benchmark.

Não é fonte primária do cálculo.

---

# 4. Regra Para O Codex

O Codex não deve substituir uma fonte `CANÔNICA` por outra fonte sem:

1. identificar a necessidade;
2. justificar tecnicamente;
3. verificar metodologia;
4. comparar resultados;
5. atualizar `04-metodologia-dados.md`;
6. atualizar este documento;
7. executar testes de regressão;
8. obter aprovação explícita.

---

# PARTE I — BRASIL

# 5. IBGE — PNAD Contínua

**Classificação:** `CANÔNICA`

**Uso principal:**

> distribuição de renda no Brasil.

Também utilizada para:

- renda domiciliar;
- renda domiciliar per capita;
- distribuição;
- percentis;
- recortes futuros;
- séries históricas quando metodologicamente comparáveis.

Fonte:

[IBGE — PNAD Contínua](https://www.ibge.gov.br/estatisticas/sociais/populacao/17270-pnad-continua.html)

---

# 6. PNAD — Microdados

Os percentis brasileiros devem ser calculados a partir de:

> **microdados e pesos amostrais adequados**

ou de estrutura derivada desses microdados validada pelo projeto.

A página oficial da PNAD disponibiliza:

- microdados;
- dicionários;
- documentação;
- informações técnicas;
- edições anuais.

Fonte:

[PNAD Contínua — Microdados](https://www.ibge.gov.br/estatisticas/sociais/populacao/17270-pnad-continua.html)

---

# 7. Base Brasileira Vigente Da V1

A referência inicial aprovada é:

> **PNAD Contínua — Rendimento de Todas as Fontes 2025**

Na página oficial do IBGE consta a atualização:

> **08/05/2026 — Atualização dos microdados — Rendimento de Todas as Fontes 2025.**

Arquivo e versão aprovados para validação:

```text
IBGE_RELEASE = 20260508
IBGE_FILE = PNADC_2025_visita1_20260508.zip
IBGE_VISIT = primeira visita
```

Fontes específicas:

- [microdados anuais da primeira visita](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Visita_1/Dados/);
- [layout da edição 2025](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Visita_1/Documentacao/input_PNADC_2025_visita1_20260508.txt);
- [dicionário da edição 2025](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Visita_1/Documentacao/dicionario_PNADC_microdados_2025_visita1_20260508.xls);
- [definições das variáveis derivadas de rendimento](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/Definicao_variaveis_derivadas_PNADC/06_Definicao_variaveis_derivadas_parte05_Rendimento_de_outras_fontes.pdf);
- [arquivo oficial de deflatores 2025](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/deflator_PNADC_2025.xls);
- [manual oficial dos deflatores anuais por visita](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/PNADcIBGE_Deflator_Anual_Visita.pdf).

Essa base deve ser validada conforme:

`04-metodologia-dados.md`

antes de gerar o dataset definitivo.

---

# 8. Benchmarks Brasileiros De 2025

## Distribuição De Rendimento De Todas As Fontes

**Classificação:** `CANÔNICA PARA VALIDAÇÃO DIRETA`

Fonte:

[IBGE — Rendimento de todas as fontes 2025](https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf)

Benchmark médio:

> **R$ 2.264 por pessoa/mês, em valores reais a preços médios de 2025.**

Esse valor foi reproduzido nos microdados pela construção definida em D063:

```text
soma_domiciliar(VD4019 × CO1 + VD4048 × CO1e) ÷ VD2003
```

Resultado não arredondado: R$ 2.264,0378279. `VD5011 × CO1` foi rejeitada como construção principal após resultar em R$ 2.331,6688.

Evidência interna reproduzível:

- `docs/research/fase-1c-inspecao-microdados-pnad-2025.md`;
- `docs/research/artifacts/fase-1c-source-manifest.json`;
- `docs/research/artifacts/fase-1c-validation-summary.json`;
- `scripts/research/inspect-pnad-2025.py`.

## RDPC Nominal Para LC 143/2013/FPE

**Classificação:** `OFICIAL-AUXILIAR`

Utilizar para:

- validação auxiliar;
- explicação pública;
- contextualização;
- sanity checks.

Fonte:

[IBGE — Rendimento domiciliar per capita 2025](https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45942-ibge-divulga-rendimento-domiciliar-per-capita-2025-para-brasil-e-unidades-da-federacao)

Valor nacional divulgado:

> **R$ 2.316 por pessoa/mês em 2025.**

O valor de R$ 2.316 é uma média nominal baseada em rendimentos efetivamente recebidos e considera população distinta da distribuição principal.

Ele é:

> **média**

e não:

> percentil;

> mediana;

> corte de classe.

Não utilizar diretamente para calcular a posição do usuário e não exigir que o pipeline brasileiro o reproduza. A diferença entre R$ 2.264 e R$ 2.316 não é erro.

---

# 9. SIDRA

**Classificação:** `CANÔNICA PARA VALIDAÇÃO` quando a tabela representar o mesmo universo; caso contrário, `OFICIAL-AUXILIAR`.

O SIDRA poderá ser utilizado para:

- tabelas agregadas;
- validação;
- séries históricas;
- recortes geográficos;
- conferência de estatísticas oficiais.

Fonte:

[IBGE — SIDRA](https://sidra.ibge.gov.br/)

Uma tabela SIDRA não substitui automaticamente os microdados quando a pergunta exigir a distribuição completa.

Tabelas candidatas aprovadas para validação da distribuição de 2025:

| Tabela | Finalidade | Classificação |
| --- | --- | --- |
| [7526](https://sidra.ibge.gov.br/tabela/7526) | limites superiores P5–P99 | direta |
| [7529](https://sidra.ibge.gov.br/tabela/7529) | população e proporções em classes simples | direta |
| [7534](https://sidra.ibge.gov.br/tabela/7534) | médias acumuladas e média total de R$ 2.264 | direta |
| [7564](https://sidra.ibge.gov.br/tabela/7564) | população e proporções em classes acumuladas | direta |

Médias por UF e outros agregados só serão diretos quando conceito, visita, população e referência de preços coincidirem. Caso contrário, serão auxiliares ou contextuais.

---

# 10. IBGE — IPCA

**Classificação:** `CANÔNICA`

Uso na V1:

> alinhar a renda mensal nominal vigente informada pelo usuário à referência de **preços médios de 2025** da CDF brasileira.

Fonte geral:

[IBGE — IPCA](https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html)

Série operacional canonizada por D065:

> **SIDRA tabela 1737, variável 2266 — IPCA, número-índice, Brasil.**

URL da série usada na Fase 1F:

[SIDRA — IPCA nacional 2025 a julho/2026](https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2266/p/202501-202607?formato=json)

Referência anual:

```text
IPCA_MEDIO_2025 = média aritmética dos 12 números-índice mensais de 2025
                = 7300.8416666666666667
```

Regra:

```text
renda_domiciliar_2025 = renda_domiciliar_corrente × IPCA_MEDIO_2025 / IPCA_mes_oficial
```

A V1 usa o índice nacional porque não coleta UF. O mês corrente deve vir de manifesto versionado e aprovado; não consultar `latest` silenciosamente e não projetar IPCA ainda não publicado.

---

# 11. IPCA Não Substitui Distribuição

O IPCA serve para:

> corrigir valores monetários ao longo do tempo.

Não serve para:

> calcular percentis.

Fluxo correto:

```text
PNAD → distribuição

IPCA → referência de preços
```

As duas fontes possuem funções diferentes.

---

# 12. IBGE — POF

**Classificação:** `CANÔNICA FUTURA`

Uso planejado:

> entender como famílias distribuem seus gastos.

Fonte principal:

[IBGE — Pesquisa de Orçamentos Familiares](https://www.ibge.gov.br/estatisticas/sociais/saude/9050-pesquisa-de-orcamentos-familiares.html)

A POF permite estudar:

- composição dos gastos;
- alimentação;
- habitação;
- transporte;
- saúde;
- educação;
- outras despesas;
- classes de rendimento;
- condições de vida.

---

# 13. POF Disponível Para Análise

A edição publicada disponível atualmente para análise detalhada continua sendo:

> **POF 2017-2018**

Fonte:

[IBGE — POF 2017-2018](https://www.ibge.gov.br/estatisticas/sociais/saude/24786-pof-2017-2018.html)

Ela poderá ser usada em pesquisa e prototipagem, respeitando a defasagem temporal.

---

# 14. POF 2024-2025

Existe uma nova edição:

> **POF 2024-2025**

Página oficial:

[IBGE — POF 2024-2025](https://www.ibge.gov.br/pof2024/)

Essa edição deverá ser monitorada para futura adoção.

### Regra

Não utilizar:

> “POF 2024-2025”

como se seus resultados completos já estivessem incorporados ao produto antes da publicação oficial dos datasets e resultados necessários.

Quando houver divulgação:

```text
detectar
↓
baixar
↓
auditar
↓
comparar
↓
validar
↓
aprovar
↓
substituir versão anterior
```

---

# PARTE II — MUNDO

# 15. Banco Mundial — Poverty and Inequality Platform

**Classificação:** `CANÔNICA`

Fonte principal da comparação mundial:

> **Poverty and Inequality Platform — PIP**

Página:

[World Bank — Poverty and Inequality Platform](https://pip.worldbank.org/)

Sobre:

[PIP — About](https://pip.worldbank.org/about)

---

# 16. Função Do PIP

O PIP será utilizado para:

- distribuição monetária internacional;
- pobreza;
- desigualdade;
- dados agregados;
- curvas distributivas;
- comparação global.

O cálculo exato deve seguir:

`04-metodologia-dados.md`

---

# 17. PIP — API

**Classificação:** `CANÔNICA / TÉCNICA`

Documentação oficial:

[World Bank PIP API](https://pip.worldbank.org/api)

Base de produção utilizada pelos clientes oficiais:

```text
https://api.worldbank.org/pip/v1
```

O cliente oficial `pipr` do Banco Mundial confirma a construção direta dessa base e dos endpoints. Recursos relevantes para a V1:

```text
/pip
/pip-grp
/aux
/versions
/citation
/valid-params
/valid-years
```

A API disponibiliza:

- estatísticas por país;
- agregações globais e regionais;
- consulta por `povline`;
- consulta inversa por `popshare` **no nível de país**;
- versões;
- anos válidos;
- tabelas auxiliares;
- curvas distributivas e parâmetros.

### Rota para D068 — revisão após inspeção do cliente oficial

A hipótese de usar `popshare` diretamente no agregado mundial foi rejeitada.

O wrapper oficial `worldbank/pip` documenta `popshare(#)` somente para `pip cl` e o código de `pip_wb.ado` rejeita explicitamente sua combinação com o subcomando `wb`.

Portanto, a candidata operacional principal para construir a CDF mundial passa a ser:

```text
1000 Binned Global Distribution
↓
vintage PIP março/2026
↓
ano 2024
↓
ordenar por welf
↓
pesar por pop
↓
CDF global experimental
```

A validação deve ser feita contra o endpoint agregado oficial:

```text
/pip-grp
group_by = wb
povline = <linha monetária>
```

em múltiplos pontos de controle.

A base em faixas não é automaticamente canônica: só poderá ser usada se o erro contra `pip wb` for compatível com a precisão exibida ao usuário.

### Rota preferencial para D069

As tabelas auxiliares oficiais:

```text
/aux?table=ppp
/aux?table=cpi
```

são as fontes preferenciais para os fatores PPP e CPI efetivamente usados nos cálculos do PIP.

Não substituir silenciosamente esses fatores por série WDI semelhante sem validação.

---

# 18. Versão PIP

A versão mundial canonizada para a V1 é:

```text
PIP_VERSION = 20260324_2021
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
PPP_BASE = 2021
GLOBAL_REFERENCE_YEAR = 2024
```

O PIP informa que estimativas posteriores a 2024 são `nowcasts`. Por isso a V1 congela 2024 enquanto D066 permanecer ativa.

Antes de qualquer atualização futura:

> consultar novamente a versão oficial, comparar metodologias e exigir aprovação explícita.

Nunca utilizar apenas:

```text
latest
```

sem registrar o identificador efetivamente processado.

---

# 18A. Distribuição Global Em 1.000 Faixas

**Classificação:** `OFICIAL-AUXILIAR / PLANO B`

Fonte:

[World Bank Data Catalog — 1000 Binned Global Distribution](https://datacatalog.worldbank.org/search/dataset/0064304/1000-binned-global-distribution)

A edição publicada em março de 2026:

- usa a vintage PIP de março de 2026;
- cobre 1990–2026;
- contém 1.000 faixas por economia/ano;
- registra `welf` em dólares internacionais PPP 2021 por pessoa/dia;
- registra `pop` como peso populacional.

O próprio Banco Mundial alerta que essa base:

- não substitui os microdados;
- não substitui as estatísticas estimadas diretamente pelo PIP;
- perde desigualdade dentro de cada faixa.

Consequência:

> usar como candidata operacional principal para a CDF mundial, sempre com validação contra `pip wb` / `pip-grp` por `povline`; rejeitar se o erro medido for material para a precisão da V1.

Não canonizar automaticamente como CDF de produção.

---

# 19. Perfil Do Brasil no PIP

**Classificação:** `OFICIAL-AUXILIAR`

Pode ser utilizado para:

- validação;
- conferência;
- comparação;
- análise de tendências.

Fonte:

[World Bank PIP — Brazil](https://pip.worldbank.org/country-profiles/BRA)

Não substituir automaticamente a PNAD brasileira pelo PIP para a posição nacional.

### Regra

```text
BRASIL → IBGE / PNAD

MUNDO → World Bank / PIP
```

---

# 20. Banco Mundial — ICP

**Classificação:** `CANÔNICA`

O:

> **International Comparison Program — ICP**

é a referência institucional para as paridades de poder de compra utilizadas pelo Banco Mundial.

Fonte:

[World Bank — International Comparison Program](https://www.worldbank.org/en/programs/icp)

---

# 21. ICP — Dados

Fonte:

[World Bank ICP — Data](https://www.worldbank.org/en/programs/icp/data)

Utilizar para:

- ciclos PPP;
- dados de referência;
- metodologia;
- revisão das paridades;
- validação.

O ciclo internacional mais recente consolidado é:

> **ICP 2021**

até nova atualização oficial.

---

# 22. ICP — Conceitos De PPP

Referência:

[World Bank ICP — FAQ](https://www.worldbank.org/en/programs/icp/faq)

Utilizar para entender:

- o que é PPP;
- como funciona;
- por que difere do câmbio;
- comparação de preços;
- interpretação internacional.

---

# 23. PPP — Consumo Privado

Indicador WDI relevante para conferência:

```text
PA.NUS.PRVT.PP
```

Descrição:

> **PPP conversion factor, households and NPISHs final consumption expenditure — LCU per international dollar**

Referência oficial:

[World Bank Data — PA.NUS.PRVT.PP](https://data.worldbank.org/indicator/PA.NUS.PRVT.PP?locations=BR)

### Regra da V1

Para D069, a prioridade é obter o PPP diretamente da tabela auxiliar da **mesma versão PIP congelada**:

```text
PIP /aux → table=ppp
```

A série WDI `PA.NUS.PRVT.PP` deve ser utilizada como:

```text
CROSS-CHECK OFICIAL
```

e não como substituto automático da tabela PIP.

Se os valores divergirem, suspender a conversão mundial até explicar conceitualmente e numericamente a diferença.

---

# 24. PPP — PIB

Existe também:

```text
PA.NUS.PPP
```

Descrição:

> **PPP conversion factor, GDP**

Fonte:

[World Bank DataBank — PA.NUS.PPP](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/PA.NUS.PPP)

Não substituir automaticamente:

```text
PPP consumo
```

por:

```text
PPP PIB
```

apenas porque a segunda série é mais fácil de encontrar.

---

# PARTE III — BANCO CENTRAL

# 25. Banco Central — Cidadania Financeira

**Classificação:** `OFICIAL-AUXILIAR`

Portal principal:

[Banco Central — Cidadania Financeira](https://www.bcb.gov.br/cidadaniafinanceira)

Será uma das principais fontes para a futura área:

> **Entenda melhor seu dinheiro**

O portal reúne:

- educação financeira;
- orçamento;
- crédito;
- reserva;
- investimentos;
- golpes;
- ferramentas;
- cursos.

---

# 26. Banco Central — Cursos

**Classificação:** `OFICIAL-AUXILIAR`

Fonte:

[Banco Central — Cursos Online](https://www.bcb.gov.br/cidadaniafinanceira/cursos)

Entre os cursos disponíveis estão:

### Gestão De Finanças Pessoais

Carga horária:

> **20 horas**

### Educação Financeira Pessoal

Carga horária:

> **40 horas**

Esses cursos poderão ser recomendados contextualmente pelo Renda Comparada.

---

# 27. Escola Virtual De Governo — Gestão De Finanças Pessoais

**Classificação:** `OFICIAL-AUXILIAR`

Página do curso:

[EV.G — Gestão de Finanças Pessoais](https://www.escolavirtual.gov.br/curso/170)

Conteudista:

> **Banco Central do Brasil**

Certificador:

> **Enap**

Uso futuro:

- orçamento;
- crédito;
- dívida;
- consumo;
- poupança;
- proteção financeira.

---

# 28. Banco Central — Biblioteca

**Classificação:** `OFICIAL-AUXILIAR`

Fonte:

[BC — Biblioteca de Cidadania Financeira](https://www.bcb.gov.br/cidadaniafinanceira/cidadania_biblioteca)

Pode ser utilizada para indicar:

- cartilhas;
- vídeos;
- Caderno de Educação Financeira;
- glossários;
- materiais sobre orçamento;
- crédito;
- poupança;
- proteção.

---

# 29. Registrato

**Classificação:** `OFICIAL-AUXILIAR`

Fonte:

[Banco Central — Registrato](https://www.bcb.gov.br/cidadaniafinanceira/registrato?hidemenu=true)

Uso futuro:

> ajudar o usuário a localizar informações sobre sua própria vida financeira.

O Renda Comparada deve:

- explicar;
- orientar;
- encaminhar.

Não deve:

- solicitar senha gov.br;
- receber credenciais;
- imitar o serviço;
- atuar como intermediário de autenticação.

---

# 30. SCR — Sistema De Informações De Créditos

**Classificação:** `OFICIAL-AUXILIAR`

Fonte institucional:

[Banco Central — SCR](https://www.bcb.gov.br/estabilidadefinanceira/scr)

Relatório para o cidadão:

[Banco Central — Relatório de Empréstimos e Financiamentos](https://www.bcb.gov.br/meubc/relatorioemprestimofinanciamento?modalAberto=scr-modal)

FAQ:

[BC — FAQ SCR](https://www.bcb.gov.br/meubc/faqs/s/relatorio-de-emprestimos-e-financiamentos-scr)

Uso futuro:

- identificar empréstimos;
- financiamentos;
- compromissos financeiros;
- apoiar organização de dívidas.

---

# 31. Valores a Receber

**Classificação:** `OFICIAL-AUXILIAR`

Fonte:

[BC — FAQ Valores a Receber](https://www.bcb.gov.br/meubc/faqs/s/valores-a-receber)

Serviço oficial:

[Valores a Receber — Banco Central](https://valoresareceber.bcb.gov.br/)

### Regra De Segurança

Ao mencionar Valores a Receber:

> direcionar somente ao serviço oficial do Banco Central.

Não reproduzir páginas de consulta.

---

# 32. Calculadora Do Cidadão

**Classificação:** `OFICIAL-AUXILIAR`

Fonte:

[Banco Central — Calculadora do Cidadão](https://www.bcb.gov.br/acessoinformacao/calculadoradocidadao?hidemenu=true)

Pode servir para:

- conferência;
- referência;
- educação;
- validação de simuladores próprios.

Entre os cálculos disponíveis:

- depósitos regulares;
- financiamento;
- valor futuro;
- correção monetária.

---

# 33. Taxas De Juros Do Banco Central

**Classificação:** `CANÔNICA FUTURA`

Fonte:

[Banco Central — Taxas de Juros](https://www.bcb.gov.br/estatisticas/txjuros?modalAberto=txjuros-modal-olho)

Uso futuro:

> **Sua taxa está cara?**

A ferramenta poderá comparar uma taxa informada pelo usuário com estatísticas do BC para a modalidade correspondente.

Sempre explicar:

> taxas variam conforme cliente, instituição, garantia, prazo e perfil de risco.

---

# PARTE IV — CVM

# 34. CVM — Educação Financeira

**Classificação:** `OFICIAL-AUXILIAR`

Fonte:

[CVM — Educação](https://www.gov.br/cvm/pt-br/assuntos/educacao)

Utilizar especialmente para:

- planejamento financeiro;
- investimentos;
- riscos;
- educação do investidor;
- formação de patrimônio.

---

# 35. Portal Do Investidor

**Classificação:** `OFICIAL-AUXILIAR`

Fonte:

[Portal do Investidor](https://www.gov.br/investidor/pt-br)

Utilizar como referência preferencial para materiais educacionais relacionados ao mercado de capitais.

---

# 36. Guia De Planejamento Financeiro

**Classificação:** `OFICIAL-AUXILIAR`

Fonte:

[CVM — Guia de Planejamento Financeiro](https://www.gov.br/investidor/pt-br/educacional/publicacoes-educacionais/guias/guia-de-planejamento-financeiro)

Pode ser recomendado para usuários interessados em:

- objetivos;
- organização;
- planejamento;
- acompanhamento financeiro.

---

# 37. Livro TOP — Planejamento Financeiro Pessoal

**Classificação:** `OFICIAL-AUXILIAR`

Fonte:

[CVM — TOP Planejamento Financeiro Pessoal](https://www.gov.br/investidor/pt-br/educacional/publicacoes-educacionais/livros-cvm/livro-top-planejamento-financeiro-pessoal/)

Pode ser utilizado como material de aprofundamento para:

- planejamento financeiro;
- investimentos;
- aposentadoria;
- gestão de riscos;
- patrimônio;
- sucessão.

---

# 38. Programa Bem-Estar Financeiro

**Classificação:** `OFICIAL-AUXILIAR`

Fonte:

[CVM — Programa Bem-Estar Financeiro](https://www.gov.br/investidor/pt-br/educacional/publicacoes-educacionais/programa-bem-estar-financeiro)

Temas particularmente alinhados ao Renda Comparada:

- bem-estar financeiro;
- crédito e endividamento;
- controle financeiro;
- objetivos;
- comportamento;
- investimentos.

---

# PARTE V — SENACON E DEFESA DO CONSUMIDOR

# 39. Senacon — Educação Financeira

**Classificação:** `OFICIAL-AUXILIAR`

Fonte institucional:

[Ministério da Justiça — Escola Nacional de Defesa do Consumidor](https://www.gov.br/mj/pt-br/assuntos/seus-direitos/consumidor/escola-nacional-endc)

Uso:

- direitos do consumidor;
- crédito;
- endividamento;
- superendividamento;
- relações financeiras.

---

# 40. Educação Financeira Em Cena

**Classificação:** `OFICIAL-AUXILIAR`

Fonte:

[Senacon — Educação Financeira em Cena](https://www.gov.br/mj/pt-br/assuntos/seus-direitos/consumidor/escola-nacional-endc/cursos-endc/Curso-Educacao-financeira-em-cena)

Uso futuro:

- crédito responsável;
- economia doméstica;
- planejamento;
- direitos do consumidor.

---

# 41. Superendividamento

**Classificação:** `OFICIAL-AUXILIAR`

Fonte institucional:

[Senacon — Superendividamento](https://www.gov.br/mj/pt-br/assuntos/seus-direitos/consumidor/defesadoconsumidor/Superendividamento)

Curso:

[Consumo de Crédito, Prevenção e Tratamento do Superendividamento](https://www.gov.br/mj/pt-br/assuntos/seus-direitos/consumidor/escola-nacional-endc/cursos-endc/Curso-consumo-de-credito-prevencao-e-tratamento-do-superendividamento)

Pode ser recomendado quando o check-up futuro identificar necessidade relacionada a:

- dívidas;
- crédito;
- renegociação;
- superendividamento.

---

# PARTE VI — PRIVACIDADE E SEGURANÇA

# 42. LGPD

**Classificação:** `LEGAL`

Lei:

> **Lei nº 13.709/2018 — Lei Geral de Proteção de Dados Pessoais**

Fonte oficial:

[Planalto — LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm)

É a referência jurídica principal para o tratamento de dados pessoais pelo produto.

---

# 43. ANPD

**Classificação:** `LEGAL / OFICIAL-AUXILIAR`

Fonte:

[Autoridade Nacional de Proteção de Dados](https://www.gov.br/anpd/pt-br)

Utilizar para:

- regulamentação;
- guias;
- segurança;
- cookies;
- incidentes;
- direitos dos titulares;
- agentes de tratamento.

---

# 44. Guias Da ANPD

Fonte central:

[ANPD — Materiais Educativos e Publicações](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes)

Referências relevantes:

- segurança da informação;
- cookies;
- controlador e operador;
- encarregado;
- legítimo interesse;
- direitos dos titulares.

---

# 45. Segurança Da Informação

**Classificação:** `LEGAL / TÉCNICA`

Fonte:

[ANPD — Guia de Segurança da Informação](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte)

Utilizar como uma das referências para:

`06-privacidade-seguranca.md`

---

# PARTE VII — SEO E INFRAESTRUTURA

# 46. Google Search Central

**Classificação:** `TÉCNICA`

Fonte principal:

[Google Search Central](https://developers.google.com/search)

Não utilizar blogs de SEO como autoridade quando a documentação oficial responder à questão.

---

# 47. SEO Em JavaScript

Fonte:

[Google — JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=pt-BR)

Uso:

- indexação;
- renderização;
- conteúdo JavaScript;
- troubleshooting.

---

# 48. Sitemaps

Fonte:

[Google — Sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview?hl=pt-BR)

Uso:

- sitemap;
- descoberta de URLs;
- indexação técnica.

---

# 49. Search Console

Fonte:

[Google — Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start?hl=pt-br)

Uso:

- indexação;
- consultas;
- cliques;
- impressões;
- erros;
- inspeção de URLs.

---

# 50. Vercel

**Classificação:** `TÉCNICA`

Utilizar documentação oficial para assuntos relacionados à infraestrutura atual do projeto.

Fonte:

[Vercel Docs](https://vercel.com/docs)

---

# 51. Vercel Web Analytics

**Classificação:** `TÉCNICA — CANDIDATA`

Fonte:

[Vercel — Web Analytics](https://vercel.com/docs/analytics)

Uso possível:

- visitantes;
- páginas;
- referrers;
- eventos personalizados.

A adoção definitiva deve respeitar:

`06-privacidade-seguranca.md`

---

# 52. Vercel Speed Insights

**Classificação:** `TÉCNICA`

Fonte:

[Vercel — Speed Insights](https://vercel.com/docs/speed-insights)

Uso:

- Core Web Vitals;
- performance real;
- acompanhamento de experiência.

---

# PARTE VIII — FONTES DE REFERÊNCIA E INSPIRAÇÃO

# 53. AllTools — Global Income Percentile

**Classificação:** `REFERÊNCIA`

Fonte:

[AllTools — Global Income Percentile](https://alltools.dev/tools/finance/global-income-percentile/)

Uso:

- inspiração inicial;
- UX;
- comparação metodológica;
- benchmark de produto.

Não utilizar seus números como fonte primária quando os dados originais puderem ser obtidos no Banco Mundial.

---

# 54. World Inequality Database — WID

**Classificação:** `REFERÊNCIA`

Fonte:

[World Inequality Database](https://wid.world/)

Metodologia do comparador:

[WID — Income Comparator Methodology](https://wid.world/how-does-our-income-comparator-work/)

Uso:

- pesquisa metodológica;
- comparação de alternativas;
- estudos sobre desigualdade.

### Regra

Não misturar automaticamente:

```text
WID
+
PIP
```

na mesma metodologia.

---

# 55. Our World in Data

**Classificação:** `REFERÊNCIA`

Fonte:

[Our World in Data](https://ourworldindata.org/)

Pode ser usada para:

- exploração;
- compreensão;
- visualização;
- localização de estudos;
- conferência.

Quando a estatística tiver origem no Banco Mundial, IBGE ou outra fonte primária:

> citar preferencialmente a fonte original.

---

# 56. Giving What We Can

**Classificação:** `REFERÊNCIA`

Fonte metodológica:

[Giving What We Can — How Rich Am I? Methodology](https://www.givingwhatwecan.org/how-rich-am-i-methodology)

Uso:

- pesquisa de comparadores globais;
- abordagem de PPP;
- UX;
- comunicação de percentis.

Não é fonte primária do Renda Comparada.

---

# 57. Imprensa

**Classificação:** `REFERÊNCIA / AQUISIÇÃO`

Veículos jornalísticos podem ser utilizados para:

- identificar assuntos relevantes;
- notícias;
- contexto;
- oportunidades editoriais;
- comportamento de busca.

Não devem ser utilizados como fonte principal do dataset quando a origem oficial estiver disponível.

Fluxo:

```text
matéria
↓
localizar fonte original
↓
verificar dado
↓
usar fonte original
```

---

# 58. Sites Comerciais E Calculadoras Concorrentes

**Classificação:** `REFERÊNCIA`

Utilizar para estudar:

- UX;
- posicionamento;
- linguagem;
- funcionalidades;
- compartilhamento;
- concorrência.

Não utilizar automaticamente seus números como verdade estatística.

---

# PARTE IX — REGRAS DE USO

# 59. Uma Fonte, Uma Finalidade

Sempre registrar:

```text
fonte
+
finalidade
```

Exemplo:

```text
PNAD
→ percentil brasileiro
```

```text
IPCA
→ correção temporal
```

```text
POF
→ padrões de gasto
```

```text
PIP
→ comparação mundial
```

```text
BCB
→ crédito e educação financeira
```

---

# 60. Não Misturar Conceitos

Exemplo proibido:

```text
renda média IBGE
+
média estadual
+
PIP
+
WID
↓
percentil inventado
```

Uma fonte precisa ser utilizada dentro do conceito estatístico que ela mede.

---

# 61. Fonte De Cálculo versus Fonte De Conteúdo

Distinguir:

### Fonte De Cálculo

Determina número produzido pelo sistema.

### Fonte De Conteúdo

Ajuda a explicar um assunto.

Exemplo:

```text
PNAD
= cálculo Brasil
```

```text
Caderno de Educação Financeira do BC
= conteúdo educativo
```

---

# 62. Fonte Primária Sempre Que Disponível

Se uma matéria disser:

> “O rendimento domiciliar per capita foi R$ X.”

e o IBGE publicou o dado:

> utilizar IBGE.

Se um artigo disser:

> “A linha internacional do Banco Mundial é X.”

e o PIP possui o valor:

> utilizar PIP.

---

# 63. Datas De Acesso

Para fontes dinâmicas, registrar:

```text
accessed_at
```

Exemplo:

```json
{
  "source": "World Bank PIP",
  "version": "20260324_2021",
  "accessed_at": "2026-08-12"
}
```

Isso é especialmente importante para APIs e datasets que recebem atualizações.

---

# 64. Versão É Mais Importante Que URL

Uma URL pode permanecer igual enquanto os dados mudam.

Portanto, para datasets:

registrar também:

- versão;
- ano;
- release;
- checksum;
- data do download.

---

# 65. Fontes Citadas Na Interface

A interface não precisa mostrar uma bibliografia enorme.

Resultado pode mostrar:

```text
Brasil
IBGE — PNAD Contínua 2025
```

e:

```text
Mundo
Banco Mundial — PIP
```

Com link:

> **Ver metodologia completa**

---

# 66. Página Pública De Metodologia

A página `/metodologia` deve detalhar:

- fontes;
- anos;
- versões;
- definições;
- limitações.

Ela deve refletir este documento e:

`04-metodologia-dados.md`

---

# 67. Conteúdo Editorial

Todo artigo que utilizar estatística deve registrar pelo menos:

```text
Fonte
Ano
```

Quando necessário:

```text
Versão
Data de acesso
```

---

# 68. Cursos E Recursos Educacionais

Antes de recomendar um curso:

1. verificar se ainda existe;
2. verificar público;
3. verificar disponibilidade;
4. verificar carga horária;
5. verificar entidade responsável;
6. verificar se o link continua oficial.

Cursos podem mudar com mais frequência que datasets.

---

# 69. Links Oficiais

Quando encaminhar para serviços financeiros públicos:

preferir links contendo:

```text
bcb.gov.br
gov.br
ibge.gov.br
worldbank.org
```

conforme a instituição.

Não direcionar por intermediários sem necessidade.

---

# 70. Monitoramento De Links

Links críticos devem ser revisados periodicamente.

Prioridade:

### Alta

- PNAD;
- PIP;
- PPP;
- Registrato;
- Valores a Receber.

### Média

- cursos;
- CVM;
- Senacon.

### Técnica

- Google;
- Vercel;
- ANPD.

---

# 71. Fonte Descontinuada

Se uma fonte desaparecer:

> não substituí-la automaticamente.

Registrar:

```text
fonte anterior
↓
problema
↓
fonte candidata
↓
comparação metodológica
↓
decisão
```

---

# 72. Fonte Contraditória

Se duas fontes oficiais apresentarem números diferentes:

não escolher simplesmente a maior ou mais recente.

Investigar:

- conceito;
- período;
- unidade;
- população;
- preço corrente/constante;
- amostra;
- metodologia.

Muitas divergências aparentes são diferenças conceituais.

---

# 73. Fonte Mais Recente Não É Automaticamente Melhor

Uma base nova pode:

- alterar metodologia;
- mudar pesos;
- mudar definição;
- possuir quebra de série.

Portanto:

> **mais recente ≠ automaticamente comparável.**

Toda nova versão passa por auditoria.

---

# 74. Registro De Fonte no Código

Evitar:

```javascript
const SOURCE = "IBGE";
```

sem contexto suficiente.

Preferir estrutura semelhante a:

```json
{
  "institution": "IBGE",
  "dataset": "PNAD Contínua",
  "release": "Rendimento de Todas as Fontes",
  "year": 2025,
  "methodologyVersion": "1.0.0"
}
```

---

# 75. Registro De Referência Em Artigos

Modelo:

```text
Instituição:
IBGE

Pesquisa:
PNAD Contínua

Referência:
Rendimento de Todas as Fontes 2025

Consultado em:
DD/MM/AAAA
```

---

# 76. Fontes Proibidas Para Percentis De Produção

Não utilizar diretamente como fonte definitiva:

- ChatGPT;
- outra LLM;
- blog;
- matéria jornalística;
- post de rede social;
- Reddit;
- calculadora concorrente;
- snippet do Google;
- resumo automático de buscador.

Esses recursos podem ajudar a localizar:

> **a fonte original.**

---

# 77. IA Não É Fonte Estatística

Uma LLM pode:

- localizar;
- interpretar;
- programar;
- comparar;
- verificar documentação.

Ela não pode ser registrada como:

> fonte do percentil.

A fonte continua sendo:

> dataset oficial + metodologia do projeto.

---

# 78. Checklist Para Inclusão De Nova Fonte

Antes de adicionar:

- Qual instituição publica?
- É fonte primária?
- Qual dado contém?
- Para que será utilizada?
- Qual metodologia?
- Qual ano?
- Qual unidade?
- Existe versão?
- Existe documentação?
- É atualizada?
- A atualização quebra comparabilidade?
- Há API?
- Há licença ou condição de uso relevante?
- Substitui alguma fonte existente?
- Exige atualização do `04-metodologia-dados.md`?

---

# 79. Checklist De Fontes V1

Antes do lançamento da V1:

- PNAD Rendimento de Todas as Fontes 2025 confirmada;
- arquivo `PNADC_2025_visita1_20260508.zip` aprovado e preservado;
- checksum do arquivo registrado;
- microdados corretos baixados;
- dicionário inspecionado;
- construção `VD4019 × CO1 + VD4048 × CO1e`, agregada por domicílio e dividida por `VD2003`, validada no arquivo real;
- `VD5011` rejeitada como variável principal e preservada apenas como hipótese histórica;
- `V1032` validado no arquivo real;
- missing, zeros, negativos e extremos inspecionados;
- regra operacional do deflator comprovada;
- alinhamento da renda do usuário com preços médios de 2025 canonizado em D065, usando IPCA nacional SIDRA 1737 / variável 2266;
- média de R$ 2.264 e agregados compatíveis reproduzidos;
- CDF brasileira, empates, extremos e golden cases validados; resíduos de R$ 1 em P90 e P99 permanecem documentados sem correção artificial;
- PIP versionado;
- ano global definido;
- PPP definida;
- manifestos brasileiros de fonte, CDF e alinhamento temporal gerados/versionados; manifestos globais permanecem pendentes;
- URLs oficiais registradas;
- metodologia pública atualizada;
- fontes exibidas na interface;
- nenhuma fonte secundária sustentando cálculo principal.

---

# 80. Mapa Rápido De Autoridade

|Pergunta|Fonte|
|---|---|
|Onde minha renda está no Brasil?|**IBGE — PNAD**|
|Quanto é a renda média?|**IBGE — PNAD**|
|Como corrigir renda no tempo?|**IBGE — IPCA**|
|Como famílias gastam?|**IBGE — POF**|
|Onde estou no mundo?|**World Bank — PIP**|
|Como ajustar poder de compra?|**World Bank — ICP / PPP**|
|Quais dívidas aparecem em meu nome?|**BC — Registrato / SCR**|
|Como comparar juros?|**Banco Central**|
|Simular juros e financiamento?|**BC — Calculadora do Cidadão**|
|Educação financeira geral?|**BC / Enap**|
|Planejamento e investimentos?|**CVM**|
|Superendividamento?|**Senacon**|
|Privacidade?|**LGPD / ANPD**|
|SEO?|**Google Search Central**|
|Infraestrutura Vercel?|**Vercel Docs**|

---

# 81. Norte Das Fontes

A política do projeto é:

> **Fonte primária antes de conveniência.**

> **Metodologia antes de manchete.**

> **Versão registrada antes de “dados atualizados”.**

> **Documento oficial antes de resumo de terceiros.**

Quando alguém perguntar:

> **“De onde saiu esse número?”**

o Renda Comparada deve conseguir responder exatamente:

> **qual instituição, qual pesquisa, qual edição, qual variável, qual versão e qual transformação produziram o resultado.**
