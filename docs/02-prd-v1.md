---
title: 02-prd-v1
created: 2026-08-12T17:05:56.000-03:00
modified: 2026-08-14T16:34:00.000-03:00
---

# 02-prd-v1

**Produto:** Renda Comparada  
**Versão:** V1  
**Status:** Canônico para o escopo da V1; integração final bloqueada pelo fechamento da metodologia Mundo
**Versão do documento:** 1.1
**Última revisão:** 14/08/2026
**Documento de visão:** `01-visao-produto.md`  
**Metodologia:** `04-metodologia-dados.md`  
**Jornada UX:** `03-jornada-ux-v1.md`

---

# 1. Objetivo Da V1

A V1 deve transformar a calculadora atual em uma experiência:

- estatisticamente confiável;
- simples;
- rápida;
- visualmente marcante;
- compreensível;
- compartilhável;
- adequada para celular;
- transparente sobre fontes e limitações.

A V1 responde principalmente:

> # Você é mais rico do que quantos brasileiros?

E complementa:

> **Descubra onde a renda da sua família está no Brasil — e onde ela estaria no mundo.**

A comparação realizada é de **renda**, e não de patrimônio.

---

# 2. Resultado Esperado

Ao final da V1, qualquer usuário deve conseguir:

1. acessar o site sem cadastro;
2. informar a renda mensal total da casa;
3. informar quantas pessoas fazem parte do domicílio segundo a orientação da metodologia;
4. receber sua posição aproximada na distribuição brasileira;
5. receber sua posição aproximada na distribuição mundial;
6. compreender o significado do resultado;
7. identificar as fontes e o ano dos dados;
8. compartilhar o resultado sem expor sua renda;
9. acessar a metodologia;
10. opcionalmente manifestar interesse em continuar para uma futura experiência de saúde financeira.

---

# 3. Hipótese Central

A principal hipótese de produto da V1 é:

> Uma pergunta de forte curiosidade pessoal, acompanhada de um resultado estatístico simples e compartilhável, pode gerar uso espontâneo e compartilhamento orgânico.

Fluxo esperado:

**curiosidade**

↓

**cálculo**

↓

**resultado**

↓

**surpresa / interpretação**

↓

**compartilhamento**

↓

**novo usuário**

O produto não deve inserir obstáculos entre o cálculo e o resultado.

---

# 4. Público Inicial

A V1 é destinada a adultos brasileiros interessados em compreender sua posição relativa de renda.

Não pressupõe:

- conhecimento financeiro;
- conhecimento estatístico;
- familiaridade com percentis;
- conta de usuário;
- experiência com investimentos.

A linguagem deve ser compreensível por um usuário comum.

---

# 5. Escopo Da V1

A V1 inclui:

## Calculadora Principal

- renda mensal nominal vigente do domicílio;
- número de moradores considerados conforme a metodologia;
- cálculo da renda domiciliar por pessoa;
- posição Brasil;
- posição Mundo.

## Resultado

- percentil;
- posição em formato `TOP X%`;
- explicação em linguagem natural;
- fontes;
- ano dos dados.

## Compartilhamento

- compartilhamento nativo quando disponível;
- WhatsApp;
- copiar link;
- card social;
- proteção da renda informada.

## Metodologia

- fontes;
- conceitos;
- anos;
- limitações;
- explicação Brasil × Mundo.

## Experiência

- mobile first;
- estados de carregamento;
- tratamento de erro;
- acessibilidade básica;
- responsividade.

## SEO

- metadata;
- conteúdo indexável;
- sitemap;
- robots;
- canonical;
- estrutura semântica.

## Analytics

- eventos essenciais da jornada;
- nenhuma renda enviada ao analytics.

## Ponte Para Próxima Experiência

Depois do resultado e compartilhamento, poderá existir um convite:

> **Sua posição de renda conta apenas uma parte da história.**

> **Quer entender melhor sua vida financeira?**

A V1 pode registrar o interesse do usuário ou direcioná-lo a uma página informativa.

O check-up financeiro completo **não pertence ao escopo obrigatório da V1**.

---

# 6. Fora Do Escopo Da V1

Não implementar nesta versão:

- check-up financeiro completo;
- score financeiro;
- Registrato integrado;
- consulta automática de dívidas;
- Valores a Receber integrado;
- comparação de taxas de crédito;
- simulador de cartão;
- simulador de cheque especial;
- juros compostos;
- CDB × Tesouro × poupança;
- custo real do carro;
- comprar × alugar;
- custo de energia;
- custo de água;
- assinaturas;
- comparação por cidade;
- comparação por estado, salvo se a metodologia específica estiver validada;
- histórico da posição do usuário;
- POF e padrão de consumo;
- recomendações personalizadas de investimento;
- cadastro;
- login;
- armazenamento de histórico financeiro;
- dezenas de páginas SEO automáticas.

Esses itens devem permanecer em:

`08-roadmap-backlog.md`

até promoção explícita para outra versão.

---

# 7. Jornada Principal

A sequência obrigatória da V1 é:

**Entrada no site**

↓

**Pergunta principal**

↓

**Renda familiar**

↓

**Número de moradores**

↓

**Calcular**

↓

**Resultado Brasil + Mundo**

↓

**Interpretação**

↓

**Compartilhar**

↓

**Experiência principal concluída**

↓

**Convite opcional para continuar**

O compartilhamento deve estar disponível **antes de qualquer questionário adicional**.

Nenhum check-up deve bloquear:

- o resultado;
- a interpretação;
- o compartilhamento.

---

# 8. Requisitos Funcionais

## FR-001 — Informar Renda Familiar

O usuário deve conseguir informar a:

> **Renda mensal total da casa**

O campo deve aceitar valores em reais.

### Requisitos

- entrada numérica;
- formatação em moeda brasileira;
- funcionamento adequado em celular;
- teclado numérico quando suportado;
- impedir valores negativos;
- fornecer mensagem de erro compreensível.

### Texto De Apoio

> **Use a renda bruta mensal, antes de impostos e despesas.**

A entrada representa a renda mensal nominal vigente no momento do cálculo.

A interface deve possuir acesso fácil à explicação “O que devo incluir?”, subordinada a `04-metodologia-dados.md`.

Para o resultado brasileiro, a aplicação deve alinhar automaticamente a renda corrente à referência de preços médios de 2025 conforme D065 e o manifesto de preços aprovado.

---

# 9. FR-002 — Informar Número De Moradores

O usuário deve informar:

> **Quantas pessoas fazem parte deste domicílio?**

Texto de apoio:

> **Inclua adultos e crianças, mesmo que não tenham renda.**

A ajuda contextual deve explicar as exclusões técnicas do universo brasileiro — empregado doméstico residente, parente de empregado doméstico e “pensionista” na classificação da condição no domicílio — sem confundir a última categoria automaticamente com beneficiário de pensão.

### Requisitos

- valor inteiro;
- mínimo de 1;
- não aceitar zero;
- não aceitar número negativo;
- controles adequados para celular.

---

# 10. FR-003 — Calcular Renda Por Pessoa

O sistema deve calcular a renda domiciliar por pessoa conforme a metodologia vigente.

Exemplo matemático simples:

Renda familiar:

**R$ 6.500**

Moradores:

**3**

Renda mensal atual por pessoa:

**R$ 2.166,67**

Esse valor é a divisão nominal simples da entrada atual e pode ser exibido como informação secundária.

Para a posição brasileira, o sistema deve primeiro alinhar a renda nominal corrente para preços médios de 2025 conforme D065 e só então consultar a CDF brasileira canônica.

A fórmula exata e sua interpretação estatística devem obedecer ao:

`04-metodologia-dados.md`

O código não deve duplicar ou criar metodologias alternativas.

---

# 11. FR-004 — Calcular Posição Brasileira

O sistema deve transformar a renda por pessoa em posição na distribuição brasileira.

A fonte vigente deve ser definida em:

`04-metodologia-dados.md`

A V1 deve utilizar a base brasileira validada e explicitamente aprovada para produção. A distribuição vigente é a CDF PNAD 2025 versionada pelo projeto; uma fonte mais nova não substitui essa versão automaticamente.

### O Resultado Deve Permitir Duas Leituras

**Percentil**

Exemplo:

> **Percentil 68**

E:

**TOP percentual**

Exemplo:

> **Entre aproximadamente os 32% de maior renda**

Essas duas representações devem ser matematicamente coerentes.

A apresentação brasileira deve seguir D071:

- na faixa principal, percentil e `TOP` são inteiros complementares;
- entre `TOP 0,1%` e `TOP 1%`, usar uma casa decimal;
- abaixo de `TOP 0,1%`, usar linguagem `< 0,1%` em vez de `TOP 0%`;
- acima do maior RDPC observado, não extrapolar uma posição mais fina;
- para renda zero, não usar `TOP 100%` como headline.

A regra de D071 altera apenas a exibição, nunca a CDF ou a precisão interna do cálculo.

---

# 12. FR-005 — Explicar O Resultado Brasileiro

O site não deve apresentar apenas um número.

Deve existir uma frase em linguagem natural.

Exemplo conceitual:

> **Sua renda por pessoa está acima da observada para aproximadamente 68 em cada 100 pessoas na distribuição brasileira utilizada.**

A redação final deve corresponder exatamente à unidade estatística efetivamente utilizada.

Não afirmar:

> “68% das famílias”

se a metodologia representa pessoas.

Não afirmar:

> “68% dos brasileiros”

se a base não suportar literalmente essa interpretação.

A linguagem deve ser validada em conjunto com `04-metodologia-dados.md`.

---

# 13. FR-006 — Calcular Posição Mundial

O sistema deve fornecer uma comparação internacional **somente depois de a metodologia Mundo ser canonizada**.

A metodologia deve considerar as conversões e ajustes definidos em:

`04-metodologia-dados.md`

Fonte principal aprovada conceitualmente:

- World Bank — Poverty and Inequality Platform;
- PPP/PPC de 2021, conforme a metodologia PIP.

O resultado deve possuir:

- posição global estimada;
- leitura percentual compatível com a CDF mundial aprovada;
- explicação;
- fonte;
- ano/versão;
- indicação explícita de que a comparação internacional é mais aproximada que a brasileira.

Enquanto `WORLD_CDF`, `WORLD_BRL_TO_2021_PPP` e os golden cases mundiais não estiverem aprovados, a integração do resultado Mundo permanece bloqueada.

---

# 14. FR-007 — Diferenciar Brasil E Mundo

Os dois resultados devem ser visualmente distintos sem parecer produtos separados.

Estrutura conceitual:

### Brasil

**Percentil X**

**TOP Y%**

explicação

### Mundo

**Percentil X**

**TOP Y%**

explicação

A diferenciação visual deve obedecer ao:

`05-design-system.md`

---

# 15. FR-008 — Mostrar Renda Por Pessoa

O resultado pode mostrar:

> **Sua renda mensal atual por pessoa: R$ X**

Isso ajuda o usuário a compreender a entrada.

Deve existir uma explicação acessível:

> renda mensal atual da casa ÷ número de moradores considerados.

Para o Brasil, a metodologia detalhada deve esclarecer que a posição é calculada após alinhamento do valor corrente para preços médios de 2025.

O valor não deve ser enviado para analytics nem incorporado automaticamente ao compartilhamento.

---

# 16. FR-009 — Compartilhamento

Após o resultado, deve existir CTA claro:

> **Compartilhar**

O modo padrão não inclui a posição individual. A posição só pode ser acrescentada após escolha explícita do usuário.

### Canais Mínimos

- Web Share API, quando disponível;
- WhatsApp;
- copiar link.

Outros canais poderão ser adicionados se não aumentarem significativamente a complexidade.

---

# 17. FR-010 — Compartilhamento Privado Por Padrão

O compartilhamento padrão **não deve incluir renda, moradores, renda por pessoa nem posição individual**.

Modelo conceitual:

> **Descobri onde minha renda está na distribuição brasileira. E você?**

ou:

> **Descubra onde a renda da sua família está no Brasil e no mundo.**

O usuário não deve expor informações financeiras por acidente.

---

# 18. FR-011 — Compartilhar Posição

Deve existir forma explícita de optar por:

> **Incluir minha posição — sem mostrar minha renda**

Exemplo:

> **Minha renda está aproximadamente entre os 12% mais altos da distribuição brasileira.**

Não incluir:

- renda informada;
- renda per capita;
- número de moradores;

salvo decisão futura explícita e consentimento inequívoco.

---

# 19. FR-012 — Card Compartilhável

O sistema deve possuir representação social visual consistente.

Exemplo conceitual:

**RENDA COMPARADA**

**TOP 12%**

> Minha posição na distribuição de renda brasileira.

**E você?**

O card deve:

- preservar privacidade;
- ser compreensível fora do site;
- conter identidade visual;
- incentivar curiosidade;
- funcionar adequadamente nas principais redes e mensageiros.

---

# 20. FR-013 — Repetir Cálculo

O usuário deve conseguir:

> **Simular outra renda**

sem recarregar obrigatoriamente o site.

Ao voltar à edição:

- os campos podem manter os valores existentes;
- o novo resultado deve substituir o anterior;
- eventos de analytics devem distinguir novos cálculos quando adequado.

---

# 21. FR-014 — Metodologia Resumida

Perto do resultado deve existir acesso fácil a:

> **Como calculamos isso?**

A explicação resumida deve informar:

- conceito de renda;
- moradores;
- fonte Brasil;
- fonte Mundo;
- ano;
- PPP/PPC quando aplicável;
- natureza aproximada do resultado.

---

# 22. FR-015 — Página Completa De Metodologia

Deve existir uma página ou seção própria contendo:

- fontes;
- definições;
- metodologia brasileira;
- metodologia mundial;
- versões dos dados;
- atualização;
- arredondamentos;
- interpolação;
- limitações;
- diferenças entre Brasil e Mundo;
- renda versus patrimônio.

Essa página deve ser construída a partir de:

`04-metodologia-dados.md`

e não de textos improvisados na interface.

---

# 23. FR-016 — Fonte E Atualização Visíveis

A interface deve mostrar algo equivalente a:

> **Brasil: IBGE — PNAD Contínua 2025**

> **Mundo: World Bank — PIP**

> **Última atualização: DD/MM/AAAA**

Para o Brasil, a metodologia/fonte também deve permitir identificar o mês do IPCA efetivamente utilizado no alinhamento temporal da renda corrente.

A versão exata da fonte e a referência monetária devem vir dos manifestos/datasets em produção.

Não escrever manualmente um ano que possa ficar desatualizado em múltiplos pontos do código.

Preferencialmente, a aplicação deve consumir essa informação dos metadados do dataset.

---

# 24. FR-017 — Aviso Renda × Patrimônio

Deve existir uma explicação discreta:

> **A comparação é baseada em renda, não em patrimônio.**

Não é necessário enfraquecer a chamada principal.

O esclarecimento deve aparecer em local facilmente acessível.

---

# 25. FR-018 — Ponte Para Saúde Financeira

Depois do resultado e da área de compartilhamento, pode existir:

> ## Sua posição de renda conta apenas uma parte da história.

> Estar acima de grande parte da população não significa necessariamente possuir uma vida financeira saudável.

Pergunta:

> **Quer entender melhor sua vida financeira?**

CTA:

> **Quero entender melhor**

Na V1, esse CTA pode:

- direcionar para uma página de apresentação;
- registrar interesse;
- apontar para uma funcionalidade experimental;

mas **não deve iniciar automaticamente um questionário**.

---

# 26. Requisitos De UX

## UX-001 — Resultado Sem Cadastro

O usuário nunca deve precisar criar conta para receber o resultado.

## UX-002 — Baixo Atrito

A experiência principal deve exigir apenas os dados indispensáveis.

## UX-003 — Resultado Acima Da Dobra Quando Possível

Após calcular, o usuário deve perceber imediatamente que algo aconteceu.

## UX-004 — Mobile First

A experiência em celular é prioritária.

## UX-005 — Linguagem Comum

Evitar exigir conhecimento sobre:

- percentis;
- PPP;
- PNAD;
- distribuições estatísticas.

Os conceitos podem ser explicados progressivamente.

---

# 27. Estados Da Interface

A V1 deve prever pelo menos:

## Estado Inicial

Campos vazios.

## Estado Preenchendo

Entradas válidas ou parcialmente preenchidas.

## Estado Inválido

Erro específico e compreensível.

## Estado Processando

Feedback visual curto quando necessário.

## Estado De Resultado

Brasil + Mundo + interpretação + compartilhamento.

## Estado De Erro De Cálculo

Mensagem clara sem apagar desnecessariamente os dados inseridos.

## Estado De Indisponibilidade De Dados

Caso algum dataset necessário esteja indisponível ou inválido, não inventar resultado.

---

# 28. Validação De Entrada

O sistema deve tratar explicitamente:

- campo vazio;
- renda zero;
- renda negativa;
- valores muito elevados;
- caracteres inválidos;
- zero moradores;
- número fracionado de moradores;
- número negativo de moradores;
- formatação com ponto;
- formatação com vírgula;
- colagem de valores monetários.

As regras exatas devem constar em:

`10-testes-validacao.md`

---

# 29. Privacidade

A V1 deve obedecer ao princípio de coleta mínima.

Não deve enviar a renda informada para:

- Google Analytics;
- Vercel Analytics;
- pixels;
- ferramentas de marketing;
- logs desnecessários;
- URLs;
- query strings.

Não deve colocar automaticamente renda ou número de moradores em:

- links compartilhados;
- Open Graph;
- cards sociais;
- histórico público.

As regras completas ficam em:

`06-privacidade-seguranca.md`

---

# 30. Analytics

A V1 deve medir comportamento, não informações financeiras.

Eventos mínimos sugeridos:

`calculator_view`

`calculation_started`

`calculation_completed`

`result_viewed`

`methodology_opened`

`share_clicked`

`share_native`

`share_whatsapp`

`copy_link`

`recalculate_clicked`

`financial_checkup_interest`

Nenhum evento deve conter:

- renda;
- renda per capita;
- número de moradores;
- percentil individual como dado pessoal, salvo avaliação específica de privacidade.

---

# 31. Métricas Da V1

## Métrica Principal

> **Compartilhamentos ÷ cálculos concluídos**

Ela mede a capacidade do resultado de gerar propagação espontânea.

## Outras Métricas

- visitantes → cálculo iniciado;
- cálculo iniciado → cálculo concluído;
- resultado → compartilhamento;
- resultado → metodologia;
- resultado → novo cálculo;
- resultado → interesse no check-up;
- retorno ao site.

Não otimizar apenas para pageviews.

---

# 32. SEO

A V1 deve possuir conteúdo suficiente para ser compreendida por usuários e mecanismos de busca.

Requisitos mínimos:

- `<title>` descritivo;
- meta description;
- canonical;
- Open Graph;
- metadata social;
- `robots.txt`;
- `sitemap.xml`;
- `lang="pt-BR"`;
- headings semânticos;
- conteúdo essencial disponível no HTML renderizado;
- URL estável para metodologia.

Título inicial sugerido:

> **Você é mais rico do que quantos brasileiros? | Renda Comparada**

Meta description sugerida:

> **Compare a renda da sua família com a distribuição de renda do Brasil e do mundo e descubra sua posição aproximada.**

A redação poderá ser refinada posteriormente sem alterar a funcionalidade.

---

# 33. Conteúdo Mínimo Da home

Além da calculadora, a V1 deve responder de forma concisa:

## Como Funciona?

Explicar renda da casa ÷ moradores.

## O Que É Percentil?

Explicação simples.

## Por Que Crianças Entram no Cálculo?

Explicação alinhada à metodologia.

## Renda É a Mesma Coisa Que Riqueza?

Não.

## De Onde Vêm Os Dados?

IBGE e Banco Mundial.

## Por Que Brasil E Mundo Podem Apresentar Posições Diferentes?

Explicação introdutória.

## O Resultado É Exato?

Explicar que é uma estimativa baseada nas distribuições disponíveis.

O conteúdo deve ser útil, não preenchimento artificial para SEO.

---

# 34. Performance

A calculadora deve responder rapidamente.

O cálculo do usuário **não deve depender de consultas em tempo real ao IBGE ou Banco Mundial**.

Arquitetura esperada:

**dados oficiais**

↓

**processamento periódico**

↓

**dataset validado e versionado**

↓

**aplicação**

O cálculo individual deve ocorrer sobre dados preparados para produção.

Para Brasil, seguir D072:

```text
home/formulário
↓
usuário aciona “Descobrir minha posição”
↓
carregar/validar artefatos Brasil se ainda não estiverem disponíveis
↓
calcular localmente
↓
manter a CDF em memória para novas simulações
```

A CDF brasileira de aproximadamente 3,95 MB **não deve entrar no bundle JavaScript inicial**. Ela deve ser servida como artefato estático e carregada sob demanda no primeiro cálculo.

A requisição do arquivo é igual para todos os usuários e nunca inclui renda, moradores, percentil ou qualquer outro dado individual.

Se o artefato não estiver disponível, a aplicação deve falhar de forma segura; não usar thresholds ou constantes antigas como fallback.

---

# 35. Dados Externos

A V1 não deve:

- baixar microdados durante a interação do usuário;
- depender de disponibilidade instantânea de APIs públicas;
- alterar resultados automaticamente quando uma fonte externa mudar.

Atualizações do dataset devem passar pelo processo definido em:

`04-metodologia-dados.md`

---

# 36. Acessibilidade

A V1 deve considerar pelo menos:

- navegação por teclado;
- labels associados aos campos;
- contraste adequado;
- foco visível;
- textos alternativos relevantes;
- não depender exclusivamente de cor;
- tamanhos de toque adequados em celular;
- resultados compreensíveis por leitores de tela quando possível.

A implementação detalhada deve obedecer ao design system.

---

# 37. Direção Visual

A V1 deve seguir:

> **Uma reportagem interativa premium que também é uma calculadora.**

Características:

- editorial;
- limpa;
- sóbria;
- orientada a dados;
- bastante espaço;
- números de resultado com forte hierarquia;
- tipografia adequada à leitura;
- animações discretas.

Evitar:

- visual de fintech genérica;
- excesso de cards;
- gamificação;
- confete;
- clichês de dinheiro;
- excesso de ícones;
- estética de cassino.

Detalhes pertencem a:

`05-design-system.md`

---

# 38. Dependência Metodológica

O PRD define **o comportamento do produto**, mas não tem autoridade para definir fórmulas estatísticas.

Para questões como:

- variável da PNAD;
- pesos;
- interpolação;
- cortes;
- PPP;
- conversões;
- distribuição global;
- arredondamento;

prevalece:

`04-metodologia-dados.md`

Caso o documento ainda não defina determinado cálculo:

> **não implementar por suposição.**

Registrar a lacuna metodológica.

---

# 39. Critérios De Aceite Da Calculadora

A funcionalidade principal será aceita quando:

- aceitar renda familiar válida;
- aceitar quantidade válida de moradores;
- incluir adultos e crianças conforme metodologia;
- calcular corretamente a renda por pessoa;
- retornar posição brasileira usando dataset aprovado;
- retornar posição mundial usando dataset aprovado;
- apresentar percentil;
- apresentar TOP percentual coerente;
- explicar o significado do resultado;
- informar fontes;
- informar ano/versão;
- permitir novo cálculo;
- funcionar adequadamente em celular.

---

# 40. Critérios De Aceite Do Compartilhamento

O compartilhamento será aceito quando:

- aparecer imediatamente após o resultado;
- funcionar no celular;
- possuir fallback quando Web Share não estiver disponível;
- permitir WhatsApp;
- permitir copiar link;
- não revelar renda por padrão;
- não revelar número de moradores;
- possuir card social adequado;
- preservar privacidade;
- gerar link funcional para novo usuário.

---

# 41. Critérios De Aceite De Metodologia E Confiança

- página de metodologia disponível;
- fonte Brasil identificada;
- fonte Mundo identificada;
- ano/versão identificado;
- diferença entre renda e patrimônio explicada;
- conceito de moradores explicado;
- limitações descritas;
- resultado não promete precisão inexistente;
- nenhuma média é apresentada como percentil;
- nenhuma estatística é inventada.

---

# 42. Critérios De Aceite De Privacidade

- renda não enviada para analytics;
- renda não incluída na URL;
- renda não incluída em query string;
- renda não aparece no card padrão;
- renda não é persistida sem necessidade;
- nenhum cadastro obrigatório;
- nenhum CPF solicitado;
- nenhuma credencial financeira solicitada.

---

# 43. Critérios De Aceite De SEO

- title configurado;
- description configurada;
- canonical configurada;
- Open Graph configurado;
- sitemap disponível;
- robots disponível;
- conteúdo principal indexável;
- estrutura de headings adequada;
- página de metodologia acessível por URL estável.

---

# 44. Critérios De Aceite De Qualidade

Antes da V1 ser considerada pronta:

- testes unitários dos cálculos aprovados;
- casos extremos testados;
- dataset validado;
- testes de regressão aprovados;
- desktop testado;
- Android testado;
- iPhone testado;
- compartilhamento testado;
- acessibilidade básica revisada;
- performance revisada;
- conteúdo metodológico revisado;
- nenhuma divergência conhecida entre código e documentação.

Detalhes ficam em:

`10-testes-validacao.md`

---

# 45. Definition of Done Da V1

A V1 estará concluída quando um novo usuário conseguir:

> entrar no site,

> entender imediatamente a proposta,

> informar somente renda e moradores,

> receber um resultado Brasil + Mundo metodologicamente validado,

> compreender o que esse resultado significa,

> confiar na origem dos dados,

> compartilhar sua posição sem revelar sua renda,

> e sair da experiência sem precisar criar conta ou responder qualquer pergunta adicional.

Se ele quiser continuar, deve existir uma porta clara para a futura experiência de saúde financeira.

Mas essa continuidade não pode prejudicar a simplicidade da experiência principal.

---

# 46. Próxima Versão

Após validar a V1 com uso real, as próximas funcionalidades candidatas incluem:

- “Quanto preciso ganhar para estar no Top X%?”;
- simulador de outras rendas;
- check-up financeiro;
- ferramentas oficiais;
- orientação contextual;
- simuladores financeiros;
- POF;
- comparação regional;
- custos reais da família.

A priorização deve depender de:

- comportamento dos usuários;
- qualidade dos dados;
- complexidade;
- impacto esperado;
- alinhamento à visão do produto.

Nada desta seção constitui requisito da V1.

---

# 47. Norte Da V1

A V1 deve fazer **uma coisa central extraordinariamente bem**:

> # transformar a renda familiar informada pelo usuário em uma comparação confiável, compreensível e compartilhável com o Brasil e o mundo.

Todo elemento que não contribua para:

**calcular**

**compreender**

**confiar**

ou

**compartilhar**

deve ser questionado antes de entrar na V1.
