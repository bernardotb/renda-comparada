---
title: AGENTS
created: 2026-08-12T18:05:05.000-03:00
modified: 2026-08-12T18:16:47.438-03:00
---

# AGENTS

Este arquivo contém as instruções operacionais para agentes de código que trabalhem neste repositório, especialmente o Codex.

Leia este documento **antes de modificar o projeto**.

---

# 1. Contexto

O Renda Comparada é uma ferramenta brasileira cuja porta de entrada é responder:

> **Você é mais rico do que quantos brasileiros?**

O usuário informa:

1. renda mensal total da casa;
2. número de moradores.

A ferramenta apresenta sua posição de renda:

- no Brasil;
- no mundo.

A visão mais ampla do produto é ajudar a pessoa a responder:

> **Onde estou financeiramente — e o que posso fazer para melhorar?**

Entretanto, essa visão é evolutiva.

A V1 possui escopo deliberadamente menor.

Não implementar automaticamente toda a visão futura.

---

# 2. Ordem Obrigatória De Leitura

Antes de alterações relevantes, leia:

1. `README.md`
2. `docs/01-visao-produto.md`
3. `docs/02-prd-v1.md`
4. `docs/03-jornada-ux-v1.md`
5. `docs/04-metodologia-dados.md`
6. `docs/05-design-system.md`
7. `docs/06-privacidade-seguranca.md`
8. `docs/07-seo-analytics-crescimento.md`
9. `docs/08-roadmap-backlog.md`
10. `docs/09-fontes-referencias.md`
11. `docs/10-testes-validacao.md`
12. `docs/decisoes.md`

Se algum arquivo não existir:

- registre a ausência;
- não invente seu conteúdo;
- continue com o que puder ser verificado.

---

# 3. Hierarquia De Autoridade

Em caso de conflito entre documentos, aplicar as seguintes regras.

## Dados E Cálculos

Prevalece:

`docs/04-metodologia-dados.md`

## Escopo Da V1

Prevalece:

`docs/02-prd-v1.md`

## Fluxo E UX

Prevalece:

`docs/03-jornada-ux-v1.md`

## Design

Prevalece:

`docs/05-design-system.md`

## Privacidade E Segurança

Prevalece:

`docs/06-privacidade-seguranca.md`

## SEO, Analytics E Crescimento

Prevalece:

`docs/07-seo-analytics-crescimento.md`

## Futuro Do Produto

Consultar:

`docs/08-roadmap-backlog.md`

Mas backlog não aumenta automaticamente o escopo.

## Decisões Já Tomadas

Consultar:

`docs/decisoes.md`

Não reabrir silenciosamente decisões registradas.

---

# 4. Regra Fundamental De Escopo

> **Backlog não é requisito.**

Não implementar itens futuros apenas porque:

- parecem úteis;
- seriam fáceis;
- melhorariam teoricamente o produto;
- já estão descritos no roadmap;
- poderiam ser aproveitados durante outra alteração.

Uma funcionalidade futura precisa ser promovida explicitamente para o escopo ativo antes da implementação.

Não transformar brainstorm em requisito.

---

# 5. Primeira Tarefa Ao Receber O Repositório

Antes de grandes alterações, audite o projeto existente.

Identifique:

1. stack;
2. framework;
3. estrutura de diretórios;
4. dependências;
5. páginas e rotas;
6. componentes;
7. lógica de cálculo;
8. datasets;
9. APIs externas;
10. analytics;
11. mecanismos de armazenamento;
12. compartilhamento;
13. SEO e metadata;
14. testes existentes;
15. configuração de deploy.

Depois produza um diagnóstico contendo:

- arquitetura atual;
- metodologia atualmente implementada;
- fontes atualmente utilizadas;
- localização dos cálculos;
- divergências entre código e documentação;
- riscos técnicos;
- riscos metodológicos;
- riscos de privacidade;
- testes existentes;
- testes faltantes;
- arquivos provavelmente afetados pelas mudanças necessárias.

Não começar reescrevendo o projeto antes dessa auditoria.

---

# 6. Metodologia É Área Protegida

Não alterar por iniciativa própria:

- conceito de renda;
- fórmula de renda per capita;
- variável da PNAD;
- pesos amostrais;
- unidade estatística;
- distribuição;
- cálculo de percentis;
- tratamento de empates;
- PPP/PPC;
- PIP;
- referência temporal;
- inflação;
- arredondamento estatístico;
- tratamento dos extremos.

Se encontrar:

[CONFIRMAR]
[DEFINIR]
TODO
TBD

em uma decisão metodológica relevante:

> não invente uma resposta.

Pode:

- localizar a documentação oficial;
- analisar alternativas;
- explicar o problema;
- propor solução.

Não deve escolher silenciosamente.

---

# 7. Fontes

As fontes de produção devem seguir:

`docs/09-fontes-referencias.md`

Prioridade:

fonte oficial
↓
documentação oficial
↓
literatura acadêmica
↓
fonte secundária confiável

Principais fontes previstas:

## Brasil

IBGE — PNAD Contínua.

## Mundo

Banco Mundial — Poverty and Inequality Platform (PIP).

## PPP/PPC

Banco Mundial / International Comparison Program.

## Inflação Brasileira

IBGE — IPCA.

Não utilizar como fonte estatística final:

- blogs;
- snippets de busca;
- matérias jornalísticas;
- redes sociais;
- respostas de LLM;
- calculadoras concorrentes.

Essas fontes podem ajudar na pesquisa ou inspiração, mas não devem determinar os percentis de produção.

---

# 8. AllTools

A AllTools pode ser utilizada como:

> referência de produto e inspiração.

Não deve ser tratada como fonte metodológica dos resultados.

A implementação brasileira precisa utilizar dados e critérios próprios documentados.

---

# 9. Regra De Renda Brasileira

A entrada principal é:


renda mensal total do domicílio
número total de moradores

Todos os moradores relevantes devem ser considerados, inclusive:

- adultos;
- crianças;
- pessoas sem renda.

Não trocar `moradores` por:

> adultos com renda.

---

# 10. Renda Não É Patrimônio

O produto utiliza como gancho:

> **Você é mais rico do que quantos brasileiros?**

Mas a variável medida é:

> **renda relativa.**

O produto não mede diretamente:

- patrimônio;
- fortuna;
- riqueza líquida;
- ativos;
- patrimônio financeiro.

Não introduzir textos ou cálculos que confundam essas grandezas.

A interface deve deixar essa limitação compreensível.

---

# 11. Jornada Protegida

A jornada principal da V1 é:

```text
ENTRA NO SITE
↓
RENDA + MORADORES
↓
RESULTADO BRASIL + MUNDO
↓
INTERPRETAÇÃO ESSENCIAL
↓
COMPARTILHAMENTO
↓
EXPERIÊNCIA PRINCIPAL CONCLUÍDA
↓
CONTINUAÇÃO OPCIONAL



O usuário deve receber o resultado rapidamente.

Não inserir antes do compartilhamento:

- cadastro;
    
- e-mail;
    
- telefone;
    
- questionário financeiro;
    
- check-up;
    
- dívida;
    
- reserva;
    
- investimentos;
    
- cursos;
    
- simuladores adicionais.

---

# 12. Continuação é opcional

Depois de entregar o resultado e permitir compartilhamento, o produto pode convidar o usuário a continuar.

A ideia conceitual é:

> **Sua posição de renda conta apenas uma parte da história.**

A partir daí podem existir futuramente:

- diagnóstico financeiro;
    
- orçamento;
    
- dívidas;
    
- reserva;
    
- educação financeira;
    
- ferramentas oficiais;
    
- simuladores.

Essas funcionalidades não fazem automaticamente parte da V1.

---

# 13. Compartilhamento

Compartilhamento é parte importante da experiência principal.

O compartilhamento padrão deve preservar privacidade.

Não incluir automaticamente:

- renda familiar;
    
- renda per capita;
    
- número de moradores.

Se existir opção para compartilhar a posição:

> compartilhar somente o que o usuário escolher explicitamente.

Não criar URL contendo dados financeiros individuais.

---

# 14. Privacidade

Princípio:

> **Se não precisamos guardar, não guardamos.**

Na V1, não persistir renda por padrão.

Não colocar renda ou dados derivados desnecessários em:

- URL;
    
- query string;
    
- pathname;
    
- hash;
    
- localStorage;
    
- sessionStorage;
    
- cookies;
    
- analytics;
    
- logs;
    
- Open Graph;
    
- error tracking.

Consultar sempre:

`docs/06-privacidade-seguranca.md`

antes de alterar qualquer fluxo que envolva dados do usuário.

---

# 15. Preferência por processamento local

Quando tecnicamente adequado:

> realizar os cálculos no navegador.

Não criar backend de persistência apenas por conveniência.

Dados estatísticos derivados e públicos podem ser distribuídos para cálculo local quando isso for compatível com:

- tamanho;
    
- performance;
    
- segurança;
    
- metodologia.

---

# 16. Analytics

Analytics deve medir comportamento do produto, não a situação financeira individual do usuário.

Eventos possíveis incluem:

```text
calculator_view
calculation_started
calculation_completed
result_viewed
share_clicked
share_native
share_whatsapp
copy_link
methodology_opened
recalculate_clicked
financial_checkup_interest
```

Não enviar:

```text
income
household_size
per_capita_income
percentile
top_percent
```

Nem criar faixas de renda apenas para contornar essa regra sem decisão explícita.

---

# 17. Tracking

Não adicionar por iniciativa própria:

- Google Analytics;
- Meta Pixel;
- TikTok Pixel;
- Hotjar;
- session replay;
- CRM;
- remarketing;
- fingerprinting;
- pixels publicitários.

Qualquer nova tecnologia de tracking exige revisão de:

`docs/06-privacidade-seguranca.md`

e:

`docs/07-seo-analytics-crescimento.md`

---

# 18. Direção De Design

Seguir:

`docs/05-design-system.md`

Direção conceitual:

> **Uma reportagem interativa premium que também é uma calculadora.**

Evitar aparência de:

- fintech;
- banco digital;
- dashboard corporativo;
- cassino;
- portal genérico de calculadoras.

Evitar excesso de:

- cards;
- gradientes;
- glassmorphism;
- neon;
- confete;
- troféus;
- moedas;
- gamificação.

O resultado deve parecer importante sem parecer promocional.

---

# 19. Mobile First

A experiência prioritária é:

```text
WhatsApp
↓
celular
↓
cálculo
↓
resultado
↓
compartilhamento
↓
WhatsApp
```

Testar prioritariamente:

```text
360px
390px
430px
```

Depois expandir validação para:

- tablet;
- notebook;
- desktop.

---

# 20. Arquitetura

Preferir separação clara:

```text
fontes oficiais
↓
pipeline de dados
↓
dataset derivado validado
↓
funções de domínio
↓
interface
```

A interface não deve ser a fonte de verdade da metodologia.

---

# 21. Funções De Domínio

Funções matemáticas devem ser, sempre que possível:

- puras;
- determinísticas;
- testáveis;
- independentes da interface.

Exemplos conceituais:

```text
calculatePerCapitaIncome()
getBrazilPercentile()
convertToPPP()
getGlobalPercentile()
calculateTopPercent()
```

Evitar esconder fórmulas estatísticas diretamente dentro de componentes visuais.

---

# 22. Configuração Metodológica

Não espalhar pelo código valores metodológicos como:

```text
ano da PNAD
versão do PIP
ano global
base PPP
referência de preços
versão metodológica
```

Preferir:

- configuração central;
- manifestos;
- metadata dos datasets.

---

# 23. Datasets

Não editar manualmente datasets derivados de produção.

Fluxo desejado:

```text
raw
↓
pipeline
↓
processed
↓
validated
↓
production
```

Toda transformação deve ser reproduzível.

---

# 24. Atualização Dos Dados

Não consultar automaticamente a versão `latest` de uma fonte e colocá-la diretamente em produção.

Fluxo:

```text
detectar nova versão
↓
baixar
↓
registrar versão/checksum
↓
processar
↓
validar
↓
executar regressão
↓
comparar resultados
↓
aprovar
↓
publicar
```

Nova base não significa automaticamente nova base de produção.

---

# 25. Testes

Seguir:

`docs/10-testes-validacao.md`

Antes de concluir uma alteração:

## Cálculos

Executar testes unitários.

## Distribuições E Datasets

Executar testes estatísticos e regressão.

## UX

Executar jornada principal.

## Compartilhamento

Executar testes funcionais e de privacidade.

## Analytics

Inspecionar payloads.

## SEO

Validar metadata e renderização.

## Design

Validar:

- mobile;
- responsividade;
- acessibilidade.

---

# 26. Golden Cases

Não modificar resultados esperados apenas para fazer testes passarem.

Quando um golden case falhar:

1. investigar o código;
2. verificar dataset;
3. verificar versão;
4. verificar metodologia;
5. entender a causa;
6. documentar a mudança.

Somente depois atualizar o valor esperado, caso a mudança seja legítima.

---

# 27. Caso Matemático Conhecido

Este cálculo pode ser considerado canônico:

```text
renda = 6500
moradores = 3

6500 / 3
=
2166.666666…
```

Apresentação monetária:

```text
R$ 2.166,67
```

Não assumir automaticamente um percentil Brasil ou Mundo para esse caso.

Esses percentis só devem virar golden cases depois da validação metodológica.

---

# 28. Política De Erro

Quando houver escolha entre:

> mostrar um resultado possivelmente incorreto;

e:

> informar que o resultado não pode ser calculado com segurança;

preferir a segunda opção.

Nunca inventar fallback estatístico.

Nunca substituir silenciosamente:

- dataset;
- variável;
- peso;
- PPP;
- ano;
- metodologia.

---

# 29. SEO

Seguir:

`docs/07-seo-analytics-crescimento.md`

Garantir quando aplicável:

- title;
- description;
- canonical;
- sitemap;
- robots;
- Open Graph;
- HTML indexável;
- página/metodologia acessível.

Não gerar dezenas ou centenas de páginas SEO automaticamente sem requisito explícito.

---

# 30. Conteúdo Estatístico

Toda frase estatística precisa refletir corretamente:

- variável;
- população;
- unidade;
- fonte;
- ano;
- metodologia.

Não escrever:

> **X% das famílias**

se a distribuição efetivamente calculada representar pessoas.

Não trocar termos estatísticos apenas porque parecem mais simples para marketing.

Simplificar a linguagem sem alterar o significado.

---

# 31. Precisão Visual

Mais casas decimais não significam maior verdade.

Se o nível de precisão justificável for:

```text
68%
```

não apresentar:

```text
67,934872%
```

A precisão exibida deve ser compatível com a metodologia e com as limitações dos dados.

---

# 32. Segurança

Não adicionar segredos ao repositório.

Nunca expor:

- API keys;
- tokens;
- passwords;
- private keys;

em:

- código cliente;
- bundle;
- logs;
- commits;
- arquivos públicos.

---

# 33. Dependências

Antes de adicionar uma dependência:

1. verificar se o projeto já resolve o problema;
2. avaliar se a dependência é realmente necessária;
3. avaliar tamanho;
4. avaliar manutenção;
5. avaliar segurança;
6. avaliar impacto no bundle.

Não instalar biblioteca grande para resolver uma função simples.

---

# 34. Mudanças Pequenas

Não ampliar escopo durante correções ou refactors.

Exemplo:

Se a tarefa for:

> melhorar o campo monetário,

não adicionar automaticamente:

- login;
- persistência;
- novo simulador;
- novo analytics;
- cadastro;
- banco de dados.

---

# 35. Mudanças Grandes

Antes de uma alteração estrutural relevante, apresentar:

- problema encontrado;
- diagnóstico;
- arquivos afetados;
- solução proposta;
- riscos;
- impacto metodológico;
- impacto de privacidade;
- plano de implementação;
- testes necessários.

Evitar grandes reescritas sem justificativa.

---

# 36. Documentação

Documentação é parte do produto.

Se uma alteração mudar:

- comportamento;
- metodologia;
- jornada;
- privacidade;
- design;
- analytics;
- escopo;

atualizar o documento canônico correspondente.

Código e documentação não podem divergir silenciosamente.

---

# 37. Decisões

Antes de reabrir uma decisão importante, consultar:

`docs/decisoes.md`

Se houver motivo para alterar uma decisão:

1. identificar a decisão existente;
2. explicar por que precisa ser revista;
3. propor nova decisão;
4. avaliar documentos afetados;
5. avaliar testes afetados.

Não substituir silenciosamente uma decisão anterior.

---

# 38. Backlog

`docs/08-roadmap-backlog.md`

é um repositório controlado de possibilidades futuras.

Não significa:

> implementar tudo.

Não criar automaticamente:

- telas;
- rotas;
- placeholders;
- botões “em breve”;

para funcionalidades do backlog.

---

# 39. Ferramentas Futuras

O produto poderá futuramente trabalhar com temas como:

- custo real do carro;
- comprar versus alugar imóvel;
- financiamento;
- investimentos;
- inflação;
- assinaturas;
- energia;
- água;
- consumo;
- orçamento;
- dívidas.

Mas essas ferramentas devem responder a uma questão financeira real da família.

O produto não deve virar:

> um AllTools brasileiro genérico.

Ferramentas desconectadas da tese financeira central não pertencem ao núcleo.

---

# 40. Educação Financeira

Quando conteúdos educacionais forem incorporados, priorizar:

- fontes oficiais;
- ferramentas públicas;
- cursos públicos confiáveis.

Podem ser utilizados, conforme validação:

- Banco Central;
- Enap;
- CVM;
- Senacon;
- outras instituições públicas adequadas.

O produto deve contextualizar e encaminhar.

Não precisa recriar conteúdo público de qualidade apenas para mantê-lo dentro do site.

---

# 41. Ferramentas Governamentais

O produto poderá futuramente orientar o usuário sobre ferramentas como:

- Registrato;
- SCR;
- Valores a Receber;
- Calculadora do Cidadão.

Quando isso ocorrer:

- usar links oficiais;
- explicar finalidade;
- explicar caminho de acesso;
- não pedir credenciais gov.br;
- não imitar telas oficiais;
- não atuar como intermediário de autenticação.

---

# 42. Recomendações Financeiras

O produto deve priorizar:

> educação e orientação.

Não introduzir automaticamente:

- recomendação de ações;
- fundos;
- criptomoedas;
- produtos bancários;
- corretoras;
- carteiras;
- seguros;
- crédito.

Qualquer evolução para recomendação individual exige nova decisão de produto, regulatória e de privacidade.

---

# 43. IA Futura

Se houver integração futura de IA:

- minimizar dados enviados;
- preservar privacidade;
- documentar o fluxo;
- não permitir que a IA substitua a metodologia estatística;
- não usar LLM para inventar percentis;
- não enviar renda para terceiros sem necessidade e decisão explícita.

A metodologia deve continuar determinística e auditável.

---

# 44. Estilo De Código

Respeitar:

- padrões existentes;
- formatter;
- lint;
- TypeScript quando existente;
- convenções do framework;
- estrutura atual do projeto.

Não impor nova arquitetura ou estilo apenas por preferência pessoal.

---

# 45. Refactors

Refactors devem preservar comportamento salvo quando a mudança de comportamento fizer parte explícita da tarefa.

Um refactor não pode alterar silenciosamente:

- percentil;
- arredondamento;
- renda per capita;
- dataset;
- share;
- analytics;
- privacidade.

---

# 46. Comentários

Comentários devem explicar principalmente:

> **por que algo existe**

quando isso não for evidente.

Evitar comentários que apenas traduzem o código para português.

Para decisões metodológicas complexas, referenciar:

`docs/04-metodologia-dados.md`

---

# 47. Controle De Versão

Quando aplicável, preferir mudanças pequenas e compreensíveis.

Separar quando possível:

- metodologia;
- dados;
- UI;
- conteúdo;
- refactor;
- testes.

Mudanças estatísticas não devem ficar escondidas dentro de grandes alterações visuais.

---

# 48. Pull Requests

Quando houver PR, o resumo deve informar:

- o que mudou;
- por que mudou;
- arquivos principais;
- riscos;
- testes realizados;
- documentação atualizada;
- impacto em resultados estatísticos;
- impacto em privacidade.

Se percentis mudarem:

> declarar explicitamente.

---

# 49. Definition of Done

Uma tarefa só deve ser considerada concluída quando:

- o código funciona;
- os testes relevantes passam;
- a metodologia foi preservada ou a mudança foi documentada;
- a privacidade foi preservada;
- mobile foi verificado quando aplicável;
- acessibilidade básica foi considerada;
- documentação foi atualizada quando necessário;
- não existem divergências conhecidas ignoradas;
- nenhuma feature fora do escopo foi adicionada.

---

# 50. Quando Perguntar

Não interromper o trabalho por questões triviais que possam ser resolvidas lendo:

- código;
- documentação;
- testes;
- configuração.

Solicitar decisão quando houver:

- lacuna metodológica real;
- conflito entre documentos;
- decisão nova de produto;
- risco de segurança;
- risco de privacidade;
- alteração relevante de escopo;
- necessidade de credencial inexistente;
- duas alternativas legítimas com consequências relevantes.

---

# 51. Quando Propor

É permitido identificar oportunidades de melhoria.

Mas apresentar como:

> **proposta**

e não implementar automaticamente.

Uma proposta deve explicar:

- problema;
- solução;
- benefício;
- risco;
- complexidade;
- impacto no escopo.

---

# 52. O Que Não Fazer

Não:

- inventar dados;
- inventar fontes;
- inventar percentis;
- trocar metodologia silenciosamente;
- persistir renda sem necessidade;
- adicionar tracking sem autorização;
- ampliar escopo;
- criar cadastro sem requisito;
- criar score financeiro sem decisão;
- recomendar ativos financeiros;
- alterar golden cases apenas para deixar CI verde;
- tratar backlog como PRD;
- ignorar documentação;
- usar média nacional como substituto da distribuição;
- usar câmbio comercial quando a metodologia exigir PPP/PPC;
- misturar metodologias incompatíveis sem documentar.

---

# 53. Prioridade De Decisão

Quando houver tensão entre objetivos, usar esta ordem:

```text
CORREÇÃO METODOLÓGICA
↓
PRIVACIDADE
↓
CORREÇÃO FUNCIONAL
↓
CLAREZA
↓
CONFIABILIDADE
↓
ACESSIBILIDADE
↓
PERFORMANCE
↓
CRESCIMENTO
↓
ESTÉTICA
↓
CONVENIÊNCIA DE IMPLEMENTAÇÃO
```

---

# 54. Norte Técnico

O projeto deve permanecer:

- simples;
- auditável;
- testável;
- reproduzível;
- privado por padrão;
- rápido;
- acessível;
- fácil de manter.

Complexidade precisa ser justificada por benefício real.

---

# 55. Norte Do Produto

A pessoa entra perguntando:

> **Você é mais rico do que quantos brasileiros?**

A V1 deve responder isso de forma:

> **confiável, compreensível e compartilhável.**

Tudo que não ajuda diretamente a:

- calcular;
- compreender;
- confiar;
- compartilhar;

deve ser questionado antes de entrar no escopo atual.

---

# 56. Regra Final Para Agentes

> **Leia antes de alterar.**

> **Audite antes de reescrever.**

> **Valide antes de publicar.**

> **Não improvise metodologia.**

> **Não invente dados.**

> **Não colete o que não precisa.**

> **Não transforme backlog em requisito.**

> **Não implemente o futuro dentro da V1.**