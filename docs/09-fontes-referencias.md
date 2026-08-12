---
title: 09-fontes-referencias
created: 2026-08-12T17:40:00.000-03:00
modified: 2026-08-12T17:51:05.883-03:00
---

# 09-fontes-referencias

# Fontes E Referências — Renda Comparada

**Produto:** Renda Comparada  
**Documento:** `09-fontes-referencias.md`  
**Status:** Canônico para seleção de fontes externas  
**Versão:** 1.0  
**Última verificação das fontes:** 12/08/2026

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
$1

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
$1

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
$1

Não necessariamente entra no cálculo principal.

## `TÉCNICA`

Documentação oficial para:

- desenvolvimento;
- SEO;
- analytics;
- infraestrutura;
- segurança.
$1

## `LEGAL`

Legislação, regulamentação ou orientação oficial.

## `REFERÊNCIA`

Fonte útil para:

- inspiração;
- comparação;
- pesquisa;
- benchmark.
$1

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
$1

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
$1

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
$1

Fonte:

[PNAD Contínua — Microdados](https://www.ibge.gov.br/estatisticas/sociais/populacao/17270-pnad-continua.html)

---

# 7. Base Brasileira Vigente Da V1

A referência inicial aprovada é:

> **PNAD Contínua — Rendimento de Todas as Fontes 2025**

Na página oficial do IBGE consta a atualização:

> **08/05/2026 — Atualização dos microdados — Rendimento de Todas as Fontes 2025.**

Essa base deve ser auditada conforme:

`04-metodologia-dados.md`

antes de gerar o dataset definitivo.

---

# 8. Rendimento Domiciliar per Capita 2025

**Classificação:** `OFICIAL-AUXILIAR`

Utilizar para:

- validação;
- explicação pública;
- contextualização;
- sanity checks.
$1

Fonte:

[IBGE — Rendimento domiciliar per capita 2025](https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45942-ibge-divulga-rendimento-domiciliar-per-capita-2025-para-brasil-e-unidades-da-federacao)

Valor nacional divulgado:

> **R$ 2.316 por pessoa/mês em 2025.**

Esse valor é:

> **média**

e não:

> percentil;

> mediana;

> corte de classe.

Não utilizar diretamente para calcular a posição do usuário.

---

# 9. SIDRA

**Classificação:** `OFICIAL-AUXILIAR`

O SIDRA poderá ser utilizado para:

- tabelas agregadas;
- validação;
- séries históricas;
- recortes geográficos;
- conferência de estatísticas oficiais.
$1

Fonte:

[IBGE — SIDRA](https://sidra.ibge.gov.br/)

Uma tabela SIDRA não substitui automaticamente os microdados quando a pergunta exigir a distribuição completa.

---

# 10. IBGE — IPCA

**Classificação:** `CANÔNICA`

Uso:

> correção temporal de valores brasileiros quando necessária à metodologia.

Fonte:

[IBGE — IPCA](https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html)

Utilizar para:

- atualização monetária;
- comparação entre valores de anos diferentes;
- histórico futuro.
$1

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
$1

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
$1

O cálculo exato deve seguir:

`04-metodologia-dados.md`

---

# 17. PIP — API

**Classificação:** `CANÔNICA / TÉCNICA`

Documentação oficial:

[World Bank PIP API](https://pip.worldbank.org/api)

A API disponibiliza recursos relacionados a:

- estatísticas;
- versões;
- anos válidos;
- dados agrupados;
- agregações;
- curvas de Lorenz;
- parâmetros auxiliares.
$1

A API deve ser utilizada principalmente pelo:

> **pipeline de atualização**

e não consultada obrigatoriamente a cada cálculo do usuário.

---

# 18. Versão PIP

Na última verificação deste documento, o PIP apresentava para PPPs de 2021:

```text
20260324_2021
```

Antes de cada atualização do dataset:

> consultar novamente a versão oficial.

Nunca utilizar apenas:

```text
latest
```

sem registrar o identificador efetivamente processado.

---

# 19. Perfil Do Brasil no PIP

**Classificação:** `OFICIAL-AUXILIAR`

Pode ser utilizado para:

- validação;
- conferência;
- comparação;
- análise de tendências.
$1

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
$1

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
$1

---

# 23. PPP — Consumo Privado

Para comparação de renda/consumo familiar, investigar e validar preferencialmente a série:

```text
PA.NUS.PRVT.PP
```

Descrição:

> **PPP conversion factor, private consumption**

Referência oficial:

[World Bank DataBank — PA.NUS.PRVT.PP](https://databank.worldbank.org/metadataglossary/africa-development-indicators/series/PA.NUS.PRVT.PP)

A seleção definitiva deve permanecer registrada em:

`04-metodologia-dados.md`

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
$1

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
$1

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
$1

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
$1

Não deve:

- solicitar senha gov.br;
- receber credenciais;
- imitar o serviço;
- atuar como intermediário de autenticação.
$1

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
$1

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
$1

Entre os cálculos disponíveis:

- depósitos regulares;
- financiamento;
- valor futuro;
- correção monetária.
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

---

# 48. Sitemaps

Fonte:

[Google — Sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview?hl=pt-BR)

Uso:

- sitemap;
- descoberta de URLs;
- indexação técnica.
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

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
$1

### Média

- cursos;
- CVM;
- Senacon.
$1

### Técnica

- Google;
- Vercel;
- ANPD.
$1

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
$1

Muitas divergências aparentes são diferenças conceituais.

---

# 73. Fonte Mais Recente Não É Automaticamente Melhor

Uma base nova pode:

- alterar metodologia;
- mudar pesos;
- mudar definição;
- possuir quebra de série.
$1

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
$1

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
$1

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
$1

---

# 79. Checklist De Fontes V1

Antes do lançamento da V1:

- PNAD 2025 confirmada;
- microdados corretos baixados;
- dicionário confirmado;
- variável de renda confirmada;
- peso confirmado;
- IPCA definido;
- PIP versionado;
- ano global definido;
- PPP definida;
- manifestos gerados;
- URLs oficiais registradas;
- metodologia pública atualizada;
- fontes exibidas na interface;
- nenhuma fonte secundária sustentando cálculo principal.
$1

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