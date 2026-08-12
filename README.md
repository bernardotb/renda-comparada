---
title: README
created: 2026-08-12T17:00:21.000-03:00
modified: 2026-08-12T17:11:32.824-03:00
---

# Renda Comparada

Ferramenta brasileira para ajudar famílias a entender **onde sua renda está na distribuição econômica**, como está sua situação financeira e quais caminhos podem ajudá-las a tomar decisões melhores.

## Proposta Central

A porta de entrada do produto é uma pergunta simples e compartilhável:

> **Você é mais rico do que quantos brasileiros?**

O usuário informa:

- renda mensal total do domicílio;
- número total de moradores, incluindo adultos e crianças.
$1

A ferramenta apresenta sua posição aproximada:

- na distribuição de renda brasileira;
- na distribuição mundial.
$1

Depois do resultado e da possibilidade de compartilhamento, o usuário pode, **opcionalmente**, continuar para uma segunda experiência:

> **Onde estou financeiramente — e o que posso fazer para melhorar?**

Essa etapa poderá incluir check-up financeiro, orientação, simuladores e encaminhamento para ferramentas e conteúdos oficiais.

---

## Princípio Do Produto

O fluxo conceitual é:

**Curiosidade → Resultado → Compartilhamento → Compreensão → Diagnóstico opcional → Orientação → Ação**

A calculadora de renda deve continuar sendo uma experiência independente e completa.

O usuário **não precisa realizar check-up, cadastro ou fornecer outros dados** para receber e compartilhar o resultado principal.

---

## O Que O Produto Não É

O Renda Comparada não pretende ser:

- banco;
- instituição financeira;
- corretora;
- assessor de investimentos;
- consultoria financeira individual;
- recomendador de produtos financeiros;
- portal genérico de calculadoras.
$1

O produto oferece:

- informação;
- educação financeira;
- simulações;
- diagnóstico geral;
- orientação;
- acesso a fontes e ferramentas oficiais.
$1

---

# Estado Atual

**Status:** definição e evolução da primeira versão do produto.

Site atualmente publicado:

`https://renda-familiar-brasil-mundo.vercel.app/`

A implementação existente deve ser auditada antes de alterações relevantes nos cálculos ou na arquitetura.

---

# Documentação Do Projeto

A documentação canônica está em `/docs`.

## Ordem De Leitura

### `docs/01-visao-produto.md`

Explica:

- problema;
- proposta de valor;
- princípios;
- posicionamento;
- limites do produto;
- visão de longo prazo.
$1

Use este documento para entender **por que o produto existe**.

---

### `docs/02-prd-v1.md`

Define:

- funcionalidades da V1;
- requisitos;
- comportamento esperado;
- critérios de aceite;
- o que entra e o que não entra na primeira versão.
$1

Use este documento para saber **o que deve ser construído agora**.

---

### `docs/03-jornada-ux-v1.md`

Define:

- fluxo do usuário;
- sequência das telas;
- estados da interface;
- momento do resultado;
- compartilhamento;
- entrada opcional no check-up financeiro.
$1

Use este documento para saber **como a experiência deve funcionar**.

---

### `docs/04-metodologia-dados.md`

Documento de autoridade para:

- fontes estatísticas;
- fórmulas;
- PNAD Contínua;
- renda domiciliar per capita;
- pesos amostrais;
- percentis;
- World Bank PIP;
- PPP/PPC;
- versões dos datasets;
- atualização dos dados;
- limitações metodológicas.
$1

**Nenhuma fórmula ou fonte de dados deve ser alterada sem revisar este documento.**

---

### `docs/05-design-system.md`

Define:

- direção estética;
- tipografia;
- cores;
- espaçamento;
- componentes;
- gráficos;
- animações;
- responsividade;
- acessibilidade.
$1

Direção geral:

> **Uma reportagem interativa premium que também é uma calculadora.**

---

### `docs/06-privacidade-seguranca.md`

Define regras para:

- renda informada pelo usuário;
- armazenamento;
- analytics;
- URLs;
- compartilhamento;
- serviços externos;
- gov.br;
- Registrato;
- credenciais;
- dados financeiros sensíveis.
$1

---

### `docs/07-seo-analytics-crescimento.md`

Define:

- SEO;
- conteúdo;
- aquisição;
- compartilhamento;
- métricas;
- analytics;
- crescimento orgânico;
- estratégia de viralização.
$1

---

### `docs/08-roadmap-backlog.md`

Contém funcionalidades e ideias futuras.

Itens neste documento **não são requisitos de implementação**, salvo solicitação explícita.

Pode conter, entre outros:

- comparação por estado;
- histórico;
- padrões de consumo;
- custo real do carro;
- moradia;
- energia;
- água;
- assinaturas;
- investimentos;
- novas calculadoras.
$1

---

### `docs/09-fontes-referencias.md`

Centraliza fontes institucionais e referências do projeto:

- IBGE;
- Banco Mundial;
- Banco Central;
- CVM;
- Senacon;
- Enap/EVG;
- outras fontes aprovadas.
$1

Sempre que possível, priorizar **fontes primárias e oficiais**.

---

### `docs/10-testes-validacao.md`

Define:

- casos de teste;
- valores de referência;
- testes estatísticos;
- regressão;
- limites;
- erros de entrada;
- testes mobile;
- compartilhamento;
- privacidade;
- atualização de datasets.
$1

Mudanças em cálculos devem ser acompanhadas de testes.

---

### `docs/decisoes.md`

Registro das principais decisões do produto.

Serve para evitar que decisões já tomadas sejam reinterpretadas ou reabertas sem necessidade.

---

# Hierarquia De Autoridade

Em caso de conflito entre documentos, utilizar esta ordem:

1. `docs/04-metodologia-dados.md` — para cálculos e dados;
2. `docs/02-prd-v1.md` — para requisitos da versão atual;
3. `docs/03-jornada-ux-v1.md` — para comportamento e fluxo;
4. `docs/06-privacidade-seguranca.md` — para tratamento de dados;
5. `docs/05-design-system.md` — para interface;
6. `docs/01-visao-produto.md` — para princípios e direção;
7. `docs/08-roadmap-backlog.md` — apenas ideias e futuro.
$1

O backlog **nunca prevalece sobre o PRD**.

---

# Fontes Principais De Dados

## Brasil

Fonte principal:

**IBGE — PNAD Contínua**

A versão vigente do projeto deve utilizar a base metodologicamente adequada mais recente aprovada e registrada em `docs/04-metodologia-dados.md`.

## Mundo

Fontes principais:

**World Bank — Poverty and Inequality Platform (PIP)**

e

**World Bank — PPP / International Comparison Program**

## Outras Fontes Previstas

- IBGE — IPCA;
- IBGE — POF;
- Banco Central do Brasil;
- CVM;
- Senacon;
- Enap/EVG.
$1

---

# Regra De Atualização Dos Dados

A calculadora não deve depender de consultas externas em tempo real a cada cálculo.

Fluxo desejado:

**Fonte oficial → importação → processamento → validação → dataset versionado → produção**

Uma nova versão de dados não deve substituir automaticamente a versão em produção sem validação.

A interface deve informar:

- fonte;
- ano;
- versão quando aplicável;
- data da última atualização.
$1

---

# Princípios Obrigatórios

- Não confundir **renda** com **patrimônio**.
- Não usar média como substituta de percentil.
- Não inventar percentis.
- Não inferir percentis estaduais somente a partir da renda média estadual.
- Todos os moradores relevantes para a metodologia brasileira devem ser considerados, inclusive crianças.
- Não modificar metodologia estatística silenciosamente.
- Não armazenar renda do usuário por padrão sem necessidade explícita.
- Não colocar renda em URLs ou query strings.
- Não enviar renda para ferramentas de analytics.
- Não revelar renda em compartilhamentos sem ação explícita do usuário.
- Não pedir senha ou credenciais do gov.br.
- Não transformar orientação financeira em recomendação de produto específico.
- Não implementar itens do backlog sem solicitação explícita.
$1

---

# Experiência Principal Da V1

O fluxo principal deve preservar esta ordem:

**Entrada no site**

↓

**“Você é mais rico do que quantos brasileiros?”**

↓

**Renda familiar + número de moradores**

↓

**Resultado Brasil + Mundo**

↓

**Compartilhamento**

↓

**Fim da experiência principal**

↓

**Convite opcional para continuar**

↓

**Check-up financeiro**

↓

**Orientação, ferramentas e conteúdos**

O check-up financeiro **não deve bloquear o resultado nem o compartilhamento**.

---

# Direção Visual

A interface deve ser:

- editorial;
- sóbria;
- clara;
- minimalista;
- baseada em dados;
- mobile first.
$1

Evitar:

- excesso de cores;
- gradientes chamativos;
- glassmorphism;
- sombras pesadas;
- confete;
- estética de cassino;
- clichês visuais financeiros;
- excesso de gamificação.
$1

A prioridade é transmitir:

**confiança + clareza + curiosidade.**

---

# Desenvolvimento Com Codex

Antes de implementar mudanças significativas:

1. ler este `README.md`;
2. ler `AGENTS.md`;
3. identificar os documentos relevantes em `/docs`;
4. auditar o código existente;
5. identificar a metodologia atualmente implementada;
6. apontar divergências entre código e documentação;
7. executar ou criar testes;
8. somente então modificar a implementação.
$1

Não assumir que uma funcionalidade mencionada em brainstorm ou backlog deve ser construída.

Em caso de dúvida sobre dados ou cálculos, **não improvisar**.

Registrar a dúvida antes de alterar comportamento estatístico.

---

# Próximas Etapas

Prioridade atual:

1. consolidar documentação canônica;
2. criar PRD da V1;
3. definir jornada UX;
4. especificar metodologia e datasets;
5. criar testes de referência;
6. criar `AGENTS.md`;
7. auditar a implementação existente;
8. implementar a V1 validada.
$1

---

## Norte Do Projeto

> **A pessoa entra querendo descobrir sua posição de renda.**
>
> **O produto pode ajudá-la a sair entendendo melhor sua própria vida financeira.**
