---
title: Registro de Decisões — Renda Comparada
created: 2026-08-12T18:04:56.000-03:00
modified: 2026-08-13T18:30:00.000-03:00
---

# Registro de Decisões — Renda Comparada

**Produto:** Renda Comparada  
**Documento:** `decisoes.md`  
**Status:** Canônico para decisões de produto e metodologia  
**Versão:** 1.0  
**Última revisão:** 13/08/2026

Documentos relacionados:

- `README.md`
- `01-visao-produto.md`
- `02-prd-v1.md`
- `03-jornada-ux-v1.md`
- `04-metodologia-dados.md`
- `05-design-system.md`
- `06-privacidade-seguranca.md`
- `07-seo-analytics-crescimento.md`
- `08-roadmap-backlog.md`
- `09-fontes-referencias.md`
- `10-testes-validacao.md`

---

# 1. Função deste documento

Este documento registra decisões relevantes já tomadas no projeto.

Seu objetivo é evitar:

- rediscutir decisões já fechadas sem motivo;
- interpretações divergentes;
- implementação baseada em memória;
- conflito entre brainstorm e escopo;
- decisões silenciosas feitas pelo Codex.

Uma decisão pode ser revista, mas sua mudança deve ser explícita.

---

# 2. Formato das decisões

Cada decisão possui:

```text
ID
Data
Status
Decisão
Motivo
Consequências
Documentos afetados
```

Status possíveis:

- `ATIVA`
- `SUBSTITUÍDA`
- `REVOGADA`
- `EM REVISÃO`

---

# D001 — Tese Central Do Produto

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O Renda Comparada não será apenas uma calculadora de percentil de renda.

Sua tese é:

> **Ajudar uma família a entender onde está financeiramente, para onde seu dinheiro está indo e quais decisões podem melhorar sua situação.**

A comparação de renda é a porta de entrada.

## Consequências

O produto pode evoluir para:

- saúde financeira;
- orientação;
- ferramentas oficiais;
- simuladores;
- custos da vida familiar.

Mas não deve virar um portal genérico de calculadoras.

---

# D002 — Chamada Principal

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Usar como principal gancho:

> # Você é mais rico do que quantos brasileiros?

Subtítulo:

> **Descubra onde a renda da sua família está no Brasil — e onde ela estaria no mundo.**

## Limite Conceitual

A interface deve esclarecer:

> **A comparação é baseada em renda, não em patrimônio.**

---

# D003 — Renda versus Patrimônio

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O produto mede:

> **renda relativa**

e não:

- patrimônio;
- riqueza líquida;
- fortuna.

Nunca apresentar resultado de renda como se fosse uma medição de patrimônio.

---

# D004 — Entrada Principal

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A V1 pede apenas:

1. renda mensal total da casa;
2. número de moradores.

Não pedir antes do resultado:

- nome;
- CPF;
- e-mail;
- telefone;
- dívidas;
- patrimônio;
- gastos;
- cidade;
- profissão.

---

# D005 — Todos Os Moradores Entram no Cálculo Brasileiro

**Data:** 12/08/2026  
**Status:** `SUBSTITUÍDA POR D056`

## Decisão

O número de moradores deve incluir:

- adultos;
- crianças;
- pessoas sem renda;

conforme a metodologia do rendimento domiciliar per capita adotado.

A interface deve explicitar:

> **Inclua adultos e crianças, mesmo que não tenham renda.**

## Revisão

A regra permanece válida para adultos, crianças e pessoas sem renda que pertençam à população elegível. A formulação absoluta “todos os moradores” foi substituída por D056 após a Fase 1A identificar as exclusões específicas do indicador; a construção final foi canonizada posteriormente em D063.

---

# D006 — Conceito Brasileiro Principal

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Para o Brasil, utilizar:

> **rendimento domiciliar per capita**

Estrutura conceitual, conforme o universo metodológico vigente:

```text
renda do domicílio compatível com o indicador
÷
número de moradores elegíveis
```

A definição de população elegível é regida por D056.

---

# D007 — Fonte Brasileira

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A fonte primária brasileira será:

> **IBGE — PNAD Contínua**

A referência inicial da V1 será:

> **Rendimento de Todas as Fontes 2025**

até aprovação de edição metodologicamente equivalente mais recente.

---

# D008 — Média Não Calcula Percentil

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Não utilizar a renda média nacional como mecanismo para inferir percentil.

Percentis devem vir da:

> **distribuição ponderada da renda**

ou representação derivada validada.

---

# D009 — Uso De Microdados E Pesos

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A distribuição brasileira deve respeitar:

- microdados adequados;
- pesos amostrais oficiais;
- unidade estatística definida.

Não tratar registros da PNAD como observações de peso igual.

---

# D010 — Fonte Mundial

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A fonte principal mundial será:

> **World Bank — Poverty and Inequality Platform — PIP**

Não utilizar WID e PIP misturados no mesmo cálculo.

---

# D011 — Poder De Compra Internacional

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A comparação mundial deve utilizar:

> **PPP/PPC**

e não simplesmente câmbio BRL/USD.

A fonte principal será o Banco Mundial / ICP.

---

# D012 — Resultado Mundial É Estimativa

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O resultado mundial deve ser apresentado como:

> **posição estimada**

porque o PIP combina dados domiciliares de:

- renda;
- consumo;
- diferentes anos;
- diferentes países;
- interpolações ou nowcasts quando aplicáveis.

Não apresentar como ranking exato mundial de renda bruta.

---

# D013 — Atualização Dos Dados

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Não consultar IBGE e Banco Mundial em tempo real a cada cálculo.

Fluxo:

```text
fonte oficial
↓
download
↓
processamento
↓
validação
↓
dataset versionado
↓
produção
```

---

# D014 — Publicação De Nova Base

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Nova versão detectada não entra automaticamente em produção.

Fluxo:

```text
detectar
↓
baixar
↓
recalcular
↓
comparar
↓
validar
↓
aprovar
↓
publicar
```

---

# D015 — Ordem Da Jornada Principal

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Fluxo canônico:

```text
ENTRA
↓
RENDA + MORADORES
↓
RESULTADO BRASIL + MUNDO
↓
INTERPRETAÇÃO
↓
COMPARTILHAMENTO
↓
EXPERIÊNCIA PRINCIPAL COMPLETA
↓
CONTINUAÇÃO OPCIONAL
```

---

# D016 — Compartilhamento Vem Antes Do Check-up

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O usuário pode compartilhar imediatamente após o resultado.

Nenhum:

- questionário;
- cadastro;
- check-up;
- curso;

pode bloquear o compartilhamento.

---

# D017 — Compartilhamento Privado Por Padrão

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O compartilhamento padrão não mostra:

- renda;
- renda per capita;
- moradores.

Pode mostrar posição apenas mediante ação explícita.

---

# D018 — Check-up É Opcional

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O check-up financeiro não é parte obrigatória da experiência principal.

A mensagem de transição será conceitualmente:

> **Sua posição de renda conta apenas uma parte da história.**

---

# D019 — Não usar “O resultado te agradou?”

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Não perguntar:

> “O resultado te agradou?”

Motivo:

percentil de renda não equivale a saúde financeira.

Preferir:

> **Quer entender melhor sua vida financeira?**

---

# D020 — Check-up Sem Score Único

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Não criar inicialmente:

> **72/100**

ou score financeiro único.

Preferir dimensões separadas:

- renda;
- dívidas;
- reserva;
- orçamento;
- capacidade de poupança.

---

# D021 — Prioridades Antes De Produtos

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O sistema deve orientar prioridades gerais.

Exemplo:

```text
dívida cara
↓
reserva
↓
investimentos
```

Não recomendar produtos específicos.

---

# D022 — Orientação, Não Consultoria Financeira

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O produto será apresentado como:

> **orientação e educação financeira**

e não como:

- consultoria financeira individual;
- assessoria de investimentos;
- recomendação de ativos.

---

# D023 — Uso De Ferramentas Públicas

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O produto poderá orientar o usuário a ferramentas oficiais como:

- Registrato;
- SCR;
- Valores a Receber;
- Calculadora do Cidadão;
- taxas do Banco Central.

O site explica e encaminha.

Não pede credenciais gov.br.

---

# D024 — Cursos Públicos

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Antes de criar cursos próprios, priorizar curadoria contextual de conteúdos públicos de:

- Banco Central;
- Enap;
- CVM;
- Senacon;
- outras instituições aprovadas.

---

# D025 — POF Para Padrões De Gasto

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A futura funcionalidade:

> **Como famílias semelhantes costumam gastar?**

deve utilizar dados adequados da:

> **IBGE — POF**

Não inventar estilo de vida a partir da renda.

---

# D026 — Não Prescrever Estilo De Vida

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Não afirmar:

> “Com R$ 15 mil você consegue ter dois carros, escola particular e viajar.”

Preferir:

> padrões observados em famílias comparáveis.

---

# D027 — Custo Real Das Escolhas

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Ferramentas futuras devem mostrar:

> custo financeiro completo

e, sempre que útil:

> **percentual da renda familiar consumido pela decisão.**

Exemplo:

> “Seu carro custa R$ X/mês e representa Y% da renda.”

---

# D028 — Não Virar Portal Genérico De Calculadoras

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Calculadoras como:

- tinta;
- BTU;
- conversores genéricos;

não pertencem ao núcleo.

Uma nova ferramenta deve contribuir para:

- compreensão financeira;
- orçamento;
- decisão econômica familiar.

---

# D029 — Estética

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Direção visual:

> **uma reportagem interativa premium que também é uma calculadora.**

Evitar aparência de:

- fintech;
- dashboard;
- portal de calculadoras;
- cassino.

---

# D030 — Mobile First

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Fluxo prioritário:

```text
WhatsApp
↓
celular
↓
cálculo
↓
resultado
↓
WhatsApp
```

Mobile é prioridade de design e teste.

---

# D031 — SEO Progressivo

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Não criar dezenas de páginas SEO automaticamente na V1.

Primeiro:

- produto confiável;
- metodologia;
- compartilhamento;
- indexação.

Depois:

> páginas de alta intenção com valor real.

---

# D032 — Métrica Principal Da V1

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Métrica inicial central:

```text
ações de compartilhamento
/
cálculos concluídos
```

Não usar apenas pageviews como medida de sucesso.

---

# D033 — Analytics Sem Renda

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Analytics mede comportamento.

Não enviar:

- renda;
- moradores;
- renda per capita;
- percentis individuais;
- faixas de renda.

---

# D034 — Coleta Mínima

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Na V1:

> **se não precisamos guardar, não guardamos.**

A renda não deve ser persistida por padrão.

---

# D035 — Renda Fora De URLs

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Não colocar renda em:

- query string;
- pathname;
- hash;
- Open Graph;
- URLs compartilhadas.

---

# D036 — Preferência Por Cálculo Local

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Quando tecnicamente adequado, processar a renda no navegador.

Evitar transmitir valores financeiros desnecessariamente ao servidor.

---

# D037 — Backlog Não É Escopo

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Itens do:

`08-roadmap-backlog.md`

não devem ser implementados sem promoção explícita para um PRD ativo.

---

# D038 — V1 Congelada Em Torno Do Núcleo

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A V1 prioriza:

- Brasil;
- Mundo;
- interpretação;
- compartilhamento;
- metodologia;
- privacidade;
- SEO técnico;
- analytics;
- mobile.

Não ampliar escopo sem decisão explícita.

---

# D039 — Golden Cases Somente Após Auditoria

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Não transformar percentis da versão atual do site em testes canônicos antes da auditoria metodológica.

O caso:

```text
6500 / 3 = 2166,666…
```

já é válido.

Os percentis ainda precisam ser validados.

---

# D040 — Falhar Com Segurança

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Quando houver dúvida entre:

> mostrar resultado possivelmente incorreto

e:

> não mostrar resultado,

preferir:

> **não mostrar o resultado.**

---

# D041 — Fonte Primária Antes De Conveniência

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Hierarquia:

```text
fonte oficial
↓
documentação oficial
↓
pesquisa acadêmica
↓
fontes secundárias
```

Calculadoras concorrentes e matérias são referências, não fonte do cálculo.

---

# D042 — AllTools Como Inspiração, Não Fonte

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A AllTools é:

> **referência de produto e inspiração original.**

Dados de produção devem vir de:

- IBGE;
- Banco Mundial;
- outras fontes oficiais aprovadas.

---

# D043 — Hierarquia Documental

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Para temas específicos:

### Cálculos E Dados

`04-metodologia-dados.md`

### Escopo Da Versão

`02-prd-v1.md`

### Jornada

`03-jornada-ux-v1.md`

### Privacidade

`06-privacidade-seguranca.md`

### Design

`05-design-system.md`

### Crescimento

`07-seo-analytics-crescimento.md`

### Futuro

`08-roadmap-backlog.md`

---

# D044 — Codex Não Decide Escopo

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O Codex pode:

- analisar;
- propor;
- apontar divergências;
- implementar requisitos aprovados.

Não pode, por iniciativa própria:

- adicionar grandes features;
- trocar metodologia;
- instalar tracking;
- persistir renda;
- promover backlog.

---

# D045 — Primeiro Trabalho Do Codex

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Antes de grandes alterações, o Codex deve:

1. ler a documentação;
2. auditar o repositório;
3. identificar stack;
4. localizar cálculos atuais;
5. identificar fontes atuais;
6. comparar código × documentação;
7. relatar divergências;
8. só então propor implementação.

---

# D046 — Testes Antes De Mudança Estatística

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Toda mudança em:

- dataset;
- fórmula;
- PPP;
- peso;
- percentil;

deve passar por testes e regressão.

---

# D047 — Documentação É Parte Do Produto

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Mudanças relevantes devem atualizar os documentos correspondentes.

O código não deve divergir silenciosamente da documentação canônica.

---

# 3. Como Revisar Uma Decisão

Para revisar uma decisão:

1. não apagar a decisão antiga;
2. marcar como `SUBSTITUÍDA` ou `REVOGADA`;
3. criar nova decisão;
4. registrar motivo;
5. atualizar documentos afetados;
6. atualizar testes quando necessário.

---

# 4. Modelo Para Nova Decisão

```markdown
# decisoes

**Data:** DD/MM/AAAA  
**Status:** `ATIVA`

## Decisão

Descrição objetiva.

## Motivo

Por que isso foi decidido?

## Consequências

O que muda?

## Documentos afetados

- arquivo A
- arquivo B
```

---

# 5. Regra Final

Este documento existe para preservar:

> **coerência**

> **memória de projeto**

> **intenção**

> **responsabilidade pelas decisões**

Uma decisão nova deve ser consciente.

Não deve surgir apenas porque:

> “o Codex achou melhor fazer assim.”

---

# Consolidação Técnica — Fase 0

## D048 — Raiz Canônica Do Projeto

**Data:** 12/08/2026  
**Status:** aprovada e executada

A raiz canônica do projeto Renda Comparada passa a ser:

`C:\Users\Usuario\Downloads\Novos Vaults\vault-template-main\vault-template-main\Tools and Knowlegde\Calculadora de renda`

Ela reúne código-fonte, documentação canônica, manifestos, configurações de build, Git e vínculo local com o projeto Vercel existente.

A antiga raiz técnica em `C:\Users\Usuario\OneDrive\Documentos\ChatGPT\3` foi preservada sem exclusão e não deve receber novas alterações do projeto. Sua remoção ou arquivamento exige decisão posterior.

Esta consolidação não altera funcionalidades, metodologia, percentis, textos da interface ou resultados estatísticos.

---

# Governança Do Repositório — Fase 0.5

## D049 — Git Como Fonte De Verdade

**Data:** 13/08/2026
**Status:** `ATIVA`

### Decisão

O Git é a fonte de verdade para código, documentação versionada e histórico de alterações do projeto Renda Comparada.

### Consequências

Alterações relevantes devem ser registradas no repositório Git da raiz canônica. Cópias sincronizadas ou arquivos avulsos não substituem o histórico versionado.

---

## D050 — Google Drive Como Backup

**Data:** 13/08/2026
**Status:** `ATIVA`

### Decisão

O Google Drive pode manter cópia ou backup documental, mas não é a fonte de verdade para o versionamento do projeto e não deve ser usado como raiz paralela de desenvolvimento.

### Consequências

Arquivos sincronizados não devem substituir silenciosamente arquivos da raiz canônica. O modelo definitivo de backup ainda deverá definir o tratamento de `.git`, `.vercel`, `node_modules`, `dist` e arquivos `*.tsbuildinfo`.

---

## D051 — Uma Única Raiz Ativa De Desenvolvimento

**Data:** 13/08/2026
**Status:** `ATIVA`

### Decisão

Existe somente uma raiz ativa de desenvolvimento:

`C:\Users\Usuario\Downloads\Novos Vaults\vault-template-main\vault-template-main\Tools and Knowlegde\Calculadora de renda`

Outras cópias devem ser tratadas como backup, legado ou arquivo e não devem receber desenvolvimento paralelo.

### Consequências

A cópia legada em `C:\Users\Usuario\OneDrive\Documentos\ChatGPT\3` permanece preservada, mas não é uma raiz ativa.

---

## D052 — Repositório Git Remoto Privado

**Data:** 13/08/2026
**Status:** `EM REVISÃO`

### Decisão Operacional Pendente

Criar futuramente um repositório Git remoto privado como backup e fonte remota do histórico.

### Limite

Nenhum remoto deve ser configurado sem autorização específica. A Fase 0.5 apenas registra a pendência.

---

# Metodologia Brasileira — Fase 1B

## D053 — Base Brasileira Da V1

**Data:** 13/08/2026
**Status:** `ATIVA`

### Decisão

A distribuição brasileira da V1 terá como referência **PNAD Contínua — Rendimento de Todas as Fontes 2025**, usando:

```text
IBGE_YEAR = 2025
IBGE_RELEASE = 20260508
IBGE_FILE = PNADC_2025_visita1_20260508.zip
IBGE_VISIT = primeira visita
```

As primeiras visitas dos quatro trimestres formam a base anual. Versão oficial posterior não deve substituir automaticamente essa edição; exige comparação e nova decisão.

### Consequências

A Fase 1C preservou o arquivo oficial fora do Git e registrou seu SHA-256 no manifesto da fonte. A edição permanece congelada; eventual substituição oficial exige nova decisão.

---

## D054 — Variável Brasileira De RDPC

**Data:** 13/08/2026
**Status:** `SUBSTITUÍDA POR D063`

### Decisão

```text
IBGE_RDPC_VARIABLE = VD5011
IBGE_RDPC_VARIABLE_STATUS = aprovada para validação na Fase 1C
```

`VD5011` é a melhor candidata encontrada para reproduzir a distribuição oficial: rendimento habitual de todos os trabalhos combinado com outras fontes efetivamente recebidas, inclusive cartão/tíquete de transporte ou alimentação.

### Consequências

A variável ainda deve ser confirmada no arquivo real quanto a existência, tipo, domínio, missing, zeros, negativos e extremos. Evidência incompatível suspende sua adoção e reabre a decisão.

### Resultado Da Validação

A Fase 1C falsificou essa hipótese: `VD5011 × CO1` resultou em média de R$ 2.331,6688, 0 de 12 cortes nacionais e 0 de 27 médias de UF reproduzidos. A decisão permanece registrada como hipótese histórica submetida a teste; não deve ser usada na produção.

---

## D055 — Peso, Reponderação E UF

**Data:** 13/08/2026
**Status:** `ATIVA`

### Decisão

```text
IBGE_WEIGHT_VARIABLE = V1032
IBGE_UF_VARIABLE = UF
```

Usar o peso calibrado oficial da edição selecionada, que deve incorporar a reponderação vigente associada às projeções populacionais que consideram o Censo 2022. Não recalibrar nem construir peso próprio.

### Consequências

`UF` será usada na V1 nacional para controles e validação, sem autorizar percentis estaduais. A Fase 1C confirmou a integridade operacional de `V1032`: nenhum missing, zero, negativo ou valor não finito foi observado na edição `20260508`.

---

## D056 — Pessoa E População Elegível

**Data:** 13/08/2026
**Status:** `ATIVA`

### Decisão

A distribuição final é interpretada por **pessoa elegível**, posicionada segundo o rendimento domiciliar per capita do domicílio em que vive.

O universo deve seguir a população elegível da construção brasileira, operacionalizada por `VD2003`. Ficam excluídas as pessoas classificadas como:

- pensionista;
- empregado doméstico;
- parente de empregado doméstico.

Adultos, crianças e pessoas sem renda própria entram quando pertencem à população elegível.

### Consequências

Esta decisão substitui a formulação absoluta de D005. A distribuição não é de salários, trabalhadores, responsáveis ou domicílios simples.

---

## D057 — Referência De Preços E Alinhamento Monetário

**Data:** 13/08/2026
**Status:** `PARCIALMENTE SUBSTITUÍDA POR D063`

### Decisão Original

```text
IBGE_PRICE_REFERENCE = preços médios de 2025
IBGE_DEFLATOR_RULE_FOR_VD5011 = [PENDENTE]
USER_INCOME_PRICE_ALIGNMENT = [DECIDIDO COMO NECESSÁRIO]
USER_INCOME_PRICE_ALIGNMENT_METHOD = [PENDENTE]
```

A renda do usuário e a distribuição devem estar na mesma referência monetária antes da comparação.

### Consequências

Não aplicar `CO1`, `CO2`, IPCA ou fórmula própria até comprovar a regra operacional para `VD5011`. A necessidade de alinhamento está decidida; o método não está.

### Revisão Após A Fase 1C

A pendência do deflator foi resolvida por D063: trabalho habitual usa `CO1` e outras fontes efetivas usam `CO1e`. Permanece ativa somente a exigência de alinhar a renda do usuário e a distribuição na mesma referência monetária; `USER_INCOME_PRICE_ALIGNMENT_METHOD` continua pendente.

---

## D058 — Zero, Missing E Valores Inválidos

**Data:** 13/08/2026
**Status:** `ATIVA — COMPLEMENTADA POR D064`

### Decisão

RDPC igual a zero é valor estatisticamente válido e deve permanecer na distribuição quando pertencer à população elegível.

Permanecem pendentes de inspeção:

```text
IBGE_RDPC_MISSING_CODES
IBGE_WEIGHT_MISSING_CODES
IBGE_RDPC_NEGATIVE_VALUES
IBGE_RDPC_MAX_OBSERVED
```

### Consequências

Missing não pode virar zero. Negativos, pesos inválidos e outliers não podem ser corrigidos ou excluídos automaticamente. A aceitação de renda zero no formulário continua sendo decisão separada de UX/produto.

### Evidência Da Edição 20260508

A Fase 1C encontrou 4.682 registros de RDPC zero, nenhum RDPC negativo e nenhum peso inválido. Blanks estruturais de componentes significam ausência daquele componente, não missing do RDPC final. Essas constatações devem ser testadas novamente em futuras edições.

---

## D059 — Empates E Desigualdade Estrita

**Data:** 13/08/2026
**Status:** `ATIVA`

### Decisão

Para a frase “Sua renda por pessoa é maior que a de aproximadamente X%”, usar:

```text
share_below(x) = peso das pessoas com RDPC < x / peso total
```

`share_at_or_below` pode ser mantido separadamente para análise.

### Consequências

Pessoas com RDPC idêntico não recebem ordenação individual fictícia. Percentil, TOP e precisão visual devem ser apresentados como aproximados.

---

## D060 — Extremos E Caudas Empíricas

**Data:** 13/08/2026
**Status:** `ATIVA`

### Decisão

A futura CDF brasileira será empírica e validada. Não utilizar extrapolação paramétrica arbitrária fora da distribuição observada.

Ficam proibidos sem nova decisão:

- extrapolação logarítmica ad hoc;
- fator 8;
- pisos artificiais;
- tetos inventados.

### Consequências

Na construção validada, foram observados P99,5 de aproximadamente R$ 20.507,98, P99,9 de aproximadamente R$ 38.991,66 e máximo de aproximadamente R$ 200.165,79. Esses valores são diagnósticos, não limites artificiais. A política de exibição das caudas permanece pendente e outliers não serão removidos automaticamente.

---

## D061 — Benchmarks Brasileiros De 2025

**Data:** 13/08/2026
**Status:** `ATIVA — COMPLEMENTADA POR D064`

### Decisão

```text
BRAZIL_VALIDATION_MEAN_2025 = 2264
BRAZIL_VALIDATION_MEAN_TYPE = real, preços médios de 2025
BRAZIL_VALIDATION_STATUS = direto validado na Fase 1C
```

R$ 2.316 é `VALIDAÇÃO AUXILIAR / CONTEXTO OFICIAL`, pois pertence ao indicador nominal relacionado à LC 143/2013/FPE, com conceito e população distintos.

### Consequências

O futuro pipeline da construção definida em D063 deverá reproduzir R$ 2.264 e outros agregados compatíveis do SIDRA. A Fase 1C obteve R$ 2.264,0378279, Gini de aproximadamente 0,511224, 27 de 27 médias de UF e 10 de 12 cortes nacionais após arredondamento. A diferença para R$ 2.316 não é erro.

---

## D062 — Domicílio E Família

**Data:** 13/08/2026
**Status:** `ATIVA`

### Decisão

Na documentação metodológica, usar preferencialmente **domicílio** e **moradores**. “Família” pode permanecer na comunicação geral quando não funcionar como definição estatística.

### Consequências

Família e domicílio não são sinônimos técnicos. A futura microcopy deve explicar a população elegível sem complexidade desnecessária; nenhuma alteração de interface está autorizada nesta fase.

---

# Metodologia Brasileira — Revisão Pós-validação Da Fase 1C

## D063 — Construção Brasileira Do RDPC Real

**Data:** 13/08/2026
**Status:** `ATIVA`

### Decisão

Canonizar para a distribuição brasileira da V1:

```text
RDPC_real_2025 =
    soma_domiciliar(
        VD4019 × CO1
        +
        VD4048 × CO1e
    )
    ÷ VD2003

WORK_INCOME_VARIABLE = VD4019
WORK_DEFLATOR = CO1
OTHER_INCOME_VARIABLE = VD4048
OTHER_INCOME_DEFLATOR = CO1e
HOUSEHOLD_ELIGIBLE_COMPONENTS = VD2003
WEIGHT_VARIABLE = V1032
PRICE_REFERENCE = preços médios de 2025
```

`VD4019` representa o componente habitual do trabalho e recebe `CO1`. `VD4048` representa outras fontes efetivamente recebidas e recebe `CO1e`. A agregação ocorre no nível de domicílio validado na Fase 1C, antes da divisão pelo número de componentes elegíveis `VD2003`.

Blanks estruturais dos componentes representam ausência daquele componente e entram como zero apenas na soma. Missing do RDPC final não pode ser convertido em zero.

### Delimitação De Cartão/Tíquete

Para reproduzir a distribuição específica de **Rendimento de Todas as Fontes 2025** selecionada pelo projeto, não utilizar os componentes adicionais de cartão/tíquete presentes em `VD5011`. Esta decisão não afirma genericamente que cartão/tíquete não seja renda; delimita o indicador estatístico adotado.

### Evidência

A recomposição nominal domiciliar de `VD4019 + VD4048` reproduziu `VD5007` sem diferenças nos 408.243 registros elegíveis. Após os deflatores próprios, a média resultante foi R$ 2.264,0378279. A construção não foi escolhida apenas para coincidir com a média.

### Consequências

D063 substitui D054 e resolve a parte do deflator que estava pendente em D057. `VD5011 × CO1` e `VD5008 × CO1` permanecem somente como diagnósticos e não devem ser usados como construção de produção. O método de alinhamento temporal da renda do usuário continua pendente.

---

## D064 — Evidências Empíricas Da Edição Brasileira 20260508

**Data:** 13/08/2026
**Status:** `ATIVA`

### Decisão

Registrar como validação da construção definida em D063:

```text
BRAZIL_VALIDATION_MEAN_2025 = 2264
BRAZIL_RECONSTRUCTED_MEAN_2025 = 2264.0378279
BRAZIL_RECONSTRUCTED_GINI_2025 = 0.5112237274
BRAZIL_UF_MEANS_ROUNDED_MATCHES = 27/27
BRAZIL_NATIONAL_CUTS_ROUNDED_MATCHES = 10/12
BRAZIL_WEIGHTED_POPULATION_2025 = 212624284.8006
RDPC_ZERO_RECORDS = 4682
RDPC_ZERO_WEIGHT = 2365090.6397
RDPC_ZERO_WEIGHT_SHARE = 1.112333%
RDPC_NEGATIVE_VALUES_OBSERVED = 0
RDPC_P99_5_OBSERVED = 20507.98
RDPC_P99_9_OBSERVED = 38991.66
RDPC_MAX_OBSERVED = 200165.79
```

Esses valores descrevem somente a edição `20260508` e devem ser recalculados em toda atualização de dados.

### Resíduos SIDRA

P90 e P99 diferiram em R$ 1 dos cortes publicados; algumas médias acumuladas diferiram em até R$ 2. Esses resíduos devem ser investigados como diferença de procedimento de partição ou arredondamento antes de criar golden cases de cortes. Não ajustar a fórmula para eliminá-los artificialmente.

### Consequências

A média, o Gini, as 27 UFs e a população constituem validação forte da construção principal. Os resíduos pequenos não reabrem D063, mas o procedimento exato de cortes, a tolerância de golden cases e a política de exibição da cauda permanecem pendentes.

---

# Pendências De Segurança

## SEC-001 — Remover `.env.local` Da Cópia Sincronizada

**Status:** `PENDENTE`

Remover o arquivo da cópia sincronizada quando o caminho local exato do backup for fornecido. Seu conteúdo não deve ser aberto, exibido, copiado ou registrado.

## SEC-002 — Revogar E Renovar O Token Vercel Sincronizado

**Status:** `PENDENTE`

Qualquer token ou segredo anteriormente sincronizado deve ser considerado potencialmente exposto. A revogação e a renovação deverão ocorrer quando a autenticação da Vercel for refeita. O token antigo não deve ser reutilizado ou testado.

---
