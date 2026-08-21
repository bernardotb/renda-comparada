---
title: Registro De Decisões — Renda Comparada
created: 2026-08-12T18:04:56.000-03:00
modified: 2026-08-20T11:56:02.296-03:00
---

# Registro De Decisões — Renda Comparada

**Produto:** Renda Comparada  
**Documento:** `decisoes.md`  
**Status:** Canônico para decisões de produto e metodologia  
**Versão:** 1.9
**Última revisão:** 20/08/2026

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

# 1. Função Deste Documento

Este documento registra decisões relevantes já tomadas no projeto.

Seu objetivo é evitar:

- rediscutir decisões já fechadas sem motivo;
- interpretações divergentes;
- implementação baseada em memória;
- conflito entre brainstorm e escopo;
- decisões silenciosas feitas pelo Codex.

Uma decisão pode ser revista, mas sua mudança deve ser explícita.

---

# 2. Formato Das Decisões

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

# D019 — Não Usar “O resultado te agradou?”

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
**Status:** `SUBSTITUÍDA POR D074`

O texto abaixo preserva o registro histórico da pendência identificada em 13/08/2026. Ele não descreve o remoto vigente.

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
**Status:** `SUBSTITUÍDA POR D063 E D065`

### Decisão Original

```text
IBGE_PRICE_REFERENCE = preços médios de 2025
IBGE_DEFLATOR_RULE_FOR_VD5011 = pendência histórica da hipótese original; VD5011 foi rejeitada por D063
USER_INCOME_PRICE_ALIGNMENT = necessário; posteriormente confirmado
USER_INCOME_PRICE_ALIGNMENT_METHOD = resolvido posteriormente por D065
```

A renda do usuário e a distribuição devem estar na mesma referência monetária antes da comparação.

### Consequências

Não aplicar `CO1`, `CO2`, IPCA ou fórmula própria até comprovar a regra operacional para `VD5011`. A necessidade de alinhamento está decidida; o método não está.

### Revisão Após A Fase 1C

A parte relativa ao deflator da PNAD foi resolvida por D063: trabalho habitual usa `CO1` e outras fontes efetivas usam `CO1e`. A parte relativa ao alinhamento da renda corrente do usuário foi posteriormente resolvida por D065; D057 permanece apenas como registro histórico da pendência original.

---

## D058 — Zero, Missing E Valores Inválidos

**Data:** 13/08/2026
**Status:** `ATIVA — COMPLEMENTADA POR D064`

### Decisão

RDPC igual a zero é valor estatisticamente válido e deve permanecer na distribuição quando pertencer à população elegível.

Na decisão original, ainda faltava inspecionar:

```text
IBGE_RDPC_MISSING_CODES
IBGE_WEIGHT_MISSING_CODES
IBGE_RDPC_NEGATIVE_VALUES
IBGE_RDPC_MAX_OBSERVED
```

A inspeção da edição `20260508` foi posteriormente concluída na Fase 1C e consolidada por D064. Esses controles deixam de ser lacunas da edição vigente e passam a ser testes obrigatórios a repetir em qualquer atualização.

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
**Status:** `ATIVA — APRESENTAÇÃO COMPLEMENTADA POR D071`

### Decisão

A futura CDF brasileira será empírica e validada. Não utilizar extrapolação paramétrica arbitrária fora da distribuição observada.

Ficam proibidos sem nova decisão:

- extrapolação logarítmica ad hoc;
- fator 8;
- pisos artificiais;
- tetos inventados.

### Consequências

Na construção validada, foram observados P99,5 de aproximadamente R$ 20.507,98, P99,9 de aproximadamente R$ 38.991,66 e máximo de aproximadamente R$ 200.165,79. Esses valores são diagnósticos, não limites artificiais. A política de exibição da cauda foi posteriormente canonizada por D071: reduzir precisão visual na cauda, não exibir `TOP 0%` e não extrapolar acima do máximo observado. Outliers não serão removidos automaticamente.

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

D063 substitui D054 e resolve a parte do deflator que estava pendente em D057. `VD5011 × CO1` e `VD5008 × CO1` permanecem somente como diagnósticos e não devem ser usados como construção de produção. O alinhamento temporal da renda do usuário foi posteriormente canonizado por D065.

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

A média, o Gini, as 27 UFs e a população constituem validação forte da construção principal. Os resíduos pequenos não reabrem D063. O procedimento editorial dos cortes publicados permanece documentado como diferença residual; a política de exibição da cauda brasileira foi posteriormente fechada por D071 sem alterar a CDF.

---

# Alinhamento Temporal Brasileiro — Canonização Da Fase 1F-R

## D065 — Alinhamento Temporal Da Renda Corrente Para Preços Médios De 2025

**Data:** 14/08/2026
**Status:** `ATIVA`

### Decisão

Para a V1 nacional, que não coleta UF, canonizar o **IPCA nacional do IBGE**, tabela SIDRA 1737, variável 2266, como índice para alinhar a renda mensal nominal vigente informada pelo usuário à referência monetária da CDF brasileira.

A referência anual é a média aritmética dos 12 números-índice mensais de janeiro a dezembro de 2025:

```text
IPCA_MEDIO_2025 = 7300.8416666666666667
```

Sejam:

```text
B = IPCA_MEDIO_2025
M = número-índice do último mês oficialmente publicado e aprovado no manifesto de preços
```

Então:

```text
renda_domiciliar_2025 = renda_domiciliar_corrente × B / M
RDPC_usuario_2025 = renda_domiciliar_2025 / moradores_elegíveis
posição_brasil = lookup_CDF_2025(RDPC_usuario_2025)
```

A renda digitada é interpretada como **renda mensal nominal vigente na data do cálculo**. Não pedir mês histórico adicional na V1.

A CDF brasileira permanece imutável em preços médios de 2025. Não atualizar todos os thresholds para preços correntes como mecanismo de produção.

O índice `M` deve vir de manifesto versionado, validado e aprovado. A aplicação não consulta o IPCA mais recente silenciosamente a cada cálculo e não projeta mês ainda não publicado.

### Compromisso Nacional versus Regional

A PNAD utiliza tratamento regional de preços na construção dos microdados. Como a V1 não solicita UF, o IPCA nacional é adotado como aproximação oficial e transparente para o alinhamento da entrada.

O diagnóstico da Fase 1F encontrou, para o período analisado, diferenças aproximadas entre fatores regionais e o fator nacional de cerca de `-1,21%` a `+0,64%`. Essa evidência dimensiona a limitação, mas não transforma o IPCA nacional em deflator regional exato.

### Metadados Obrigatórios

O manifesto de preços deve registrar, no mínimo:

```text
source = IBGE SIDRA
sidraTable = 1737
sidraVariable = 2266
basePriceReference = preços médios de 2025
baseIndex = 7300.8416666666666667
priceIndexReferenceMonth = mês oficial efetivamente usado
currentIndex = número-índice desse mês
accessedAt = data de atualização do manifesto
```

### Consequências

- D065 resolve a parte de `USER_INCOME_PRICE_ALIGNMENT_METHOD` que permanecia aberta em D057.
- D057 fica integralmente substituída por D063, quanto à construção/deflatores da PNAD, e por D065, quanto ao alinhamento da renda corrente.
- A atualização do IPCA passa a ser um processo controlado de dados, não uma consulta dinâmica por cálculo.
- O mês de referência do IPCA deve ser acessível ao usuário na metodologia/fonte da versão em produção.
- A microcopy e a precisão visual não podem alterar a fórmula; para o resultado Brasil, a regra de exibição foi posteriormente canonizada por D071.
- A integração no frontend permanece uma etapa posterior; esta decisão não autoriza reutilizar as constantes metodológicas antigas do `src/App.tsx`.

---

# Metodologia Mundial — Decisões D066–D070

## D066 — Versão PIP E Ano Mundial De Referência

**Data:** 14/08/2026
**Status:** `ATIVA`

### Decisão

Para a comparação mundial da V1, congelar:

```text
PIP_VERSION = 20260324_2021
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
GLOBAL_REFERENCE_YEAR = 2024
GLOBAL_ESTIMATION_TYPE = reference-year aggregate; não nowcast
PPP_REFERENCE = 2021
```

O PIP vigente informa que estimativas posteriores a 2024 são nowcasts. Portanto, a V1 não utiliza automaticamente 2025 ou 2026 apenas para aproximar o ano da referência brasileira.

O ano 2024 continua sendo um agregado harmonizado do PIP e não deve ser descrito como se todos os países tivessem realizado pesquisa domiciliar naquele ano.

### Consequências

- nenhuma versão `latest` pode entrar automaticamente em produção;
- atualização de versão PIP exige comparação, validação e nova aprovação;
- 2025/2026 ficam fora da V1 mundial enquanto forem tratados como nowcasts na versão congelada;
- D066, isoladamente, não resolve a CDF mundial, a conversão monetária nem os golden cases.

---

## D067 — Conceito E Linguagem Da Comparação Mundial

**Data:** 14/08/2026
**Status:** `ATIVA`

### Decisão

O resultado mundial deve ser interpretado como:

> **posição monetária global estimada**

e não como distribuição homogênea mundial de salários ou renda bruta.

A fonte PIP utiliza agregados domiciliares per capita baseados em:

- consumo, em parte das economias;
- renda, em outras economias;

expressos em dólares internacionais de PPP/PPC de 2021 por pessoa por dia.

A interface deve explicar que a comparação global combina renda ou consumo e é ajustada por poder de compra.

Não utilizar como formulação principal:

> **“Você ganha mais do que X% do mundo.”**

sem nova decisão metodológica que demonstre que a simplificação é suportada.

### Consequências

- o resultado Mundo deve carregar linguagem de estimativa;
- a interface deve diferenciar a força metodológica do resultado Brasil e Mundo;
- a fonte e a construção de `WORLD_CDF` são regidas por D068, a conversão monetária por D069 e a apresentação e os golden cases por D070;
- D067 não autoriza integração do vetor mundial antigo do `src/App.tsx`.

---

## D068 — Fonte Operacional E Construção Da CDF Mundial

**Data:** 19/08/2026
**Status:** `ATIVA`

### Decisão

Para a comparação mundial da V1, construir a CDF a partir do dataset oficial do World Bank/Poverty and Inequality Platform **1000 Binned Global Distribution**, recurso `DR0094423`, usando:

```text
PIP_VERSION = 20260324_2021
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
GLOBAL_REFERENCE_YEAR = 2024
PPP_BASE = 2021
SOURCE_FILE = GlobalDist1000bins_1990_2026_20260324_2021_01_02_PROD.csv
```

Para 2024, selecionar exatamente as 218 economias e seus 1.000 bins. Interpretar:

```text
welf = dólares internacionais PPP 2021 por pessoa por dia
pop = milhões de pessoas representadas pelo bin
```

Ordenar globalmente por `welf`, agrupar valores empatados antes da acumulação e somar `pop` para formar uma CDF empírica em degraus. Missing, valores não numéricos ou não finitos, `welf` negativo e `pop` não positivo invalidam a construção; não há imputação, interpolação ou extrapolação.

O lookup deve preservar separadamente:

```text
shareBelow(x) = peso com welf < x / peso total
shareAtOrBelow(x) = peso com welf <= x / peso total
topShare(x) = 1 - shareBelow(x)
```

### Limitação Aceita

A representação usa a média de welfare de cada bin e perde desigualdade dentro do bin. Essa aproximação é aceita para a fonte e a construção da CDF mundial com restrição de precisão: não autoriza posição individual exata nem interpolação fina. A precisão visual, as caudas e os golden cases são regidos por D070.

### Evidência

O contrato versionado fixa 218.000 bins de origem, provenientes de 218 economias, 216.790 pontos únicos, população de `8.141,808945` milhões e suporte de `0,2799999999999999` a `3.822,84090639671` dólares internacionais PPP 2021 por pessoa/dia. Essas contagens e o total populacional são exigidos pelo pacote/teste de produção versionados.

D068 prevê validação contra checkpoints oficiais PIP da mesma vintage. O pacote e o manifesto de produção versionados preservam o limite operacional abaixo, sem comprovar aqui a quantidade detalhada desses checkpoints:

```text
max_absolute_error = 0.022516991848920 ponto percentual
```

Artefatos de evidência:

- raw `data/raw/world/pip-20260324-2021/GlobalDist1000bins_1990_2026_20260324_2021_01_02_PROD.csv` — SHA-256 `99FC4B99BD6D77770DA78A5BFC90516F5FE35742C7A29968F2FD148B323B48A2`;
- processado `data/processed/world/pip-20260324-2021/world-bins-2024.csv` — SHA-256 `2CA102013BDF9D3EA22C9642326544B32D45EF61407F81C6B71324BC5B072F52`;
- candidata D068 referenciada como `validation/world/world-income-cdf-2024-candidate.json` — SHA-256 `56C53483744176A50090E16058A0CF4FC6221C83D1D80A60060B931110C54DC2`, hash exigido pelo script de produção versionado;
- `validation/world/world-cdf-validation.json` está versionado no HEAD atual; `validation/world/world-cdf-validation.md` permanece como registro local fora do HEAD. Nenhum deles é usado aqui, isoladamente, como prova de execução.

### Consequências

- D068 deixa de ser bloqueio metodológico para a fonte e a construção da CDF mundial;
- a candidata referenciada por SHA permanece como referência de evidência e não é promovida automaticamente a `data/production/world/`;
- toda materialização de produção deve preservar versão, provenance, checksums, semântica de empates e ausência de fallback legado;
- D068 não autorizou por si só precisão visual, caudas ou integração numérica; esses temas foram posteriormente tratados por D070, sem autorização automática de frontend ou produção Mundo.

### Documentos Afetados

- `04-metodologia-dados.md`;
- `09-fontes-referencias.md`;
- `10-testes-validacao.md`;
- `README.md`;
- `02-prd-v1.md`.

---

## D069 — Conversão De BRL Corrente Para PPP 2021 Compatível Com O PIP

**Data:** 19/08/2026
**Status:** `ATIVA`

### Decisão

Converter a renda domiciliar nominal corrente em BRL para **dólares internacionais de PPP 2021 por pessoa por dia**, compatíveis com a build PIP congelada, usando:

```text
PIP_VERSION = 20260324_2021
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
GLOBAL_REFERENCE_YEAR = 2024
PPP_BASE = 2021

BRAZIL_PIP_PPP_2021 = 2.44986319541931
BRAZIL_PIP_CPI_2024_BASE_2021 = 1.192919586578344
BRL_PER_INTL_2024 = BRAZIL_PIP_PPP_2021 × BRAZIL_PIP_CPI_2024_BASE_2021
                  = 2.92248979025310406149724542264
```

`BRL_PER_INTL_2024` é derivado dos dois fatores PIP observados, não uma terceira fonte independente. O CPI de 2024 está presente diretamente no raw (`CPI_DERIVATION = DIRECT`).

Para a perna temporal brasileira do pipeline Mundo, usar o IPCA nacional do IBGE, SIDRA tabela 1737, variável 2266, número-índice:

```text
IPCA_AVG_2024 = média aritmética dos 12 números-índice mensais de janeiro a dezembro de 2024
IPCA_CURRENT = número-índice do mês corrente explicitamente aprovado e versionado para o contrato Mundo
```

A fórmula canônica é:

```text
dailyPPP = (householdIncomeCurrent / residents)
         × (IPCA_AVG_2024 / IPCA_CURRENT)
         ÷ (BRAZIL_PIP_PPP_2021 × BRAZIL_PIP_CPI_2024_BASE_2021)
         × 12 / 365
```

Ordem obrigatória: dividir a renda domiciliar pelos moradores; alinhar BRL corrente a preços médios de 2024 pelo IPCA; dividir pelo fator PIP compatível com 2024 e PPP 2021; converter o valor mensal para diário por `× 12 / 365`. Não há arredondamento intermediário.

Os fatores PPP e CPI são os valores completos dos raws `aux/ppp` e `aux/cpi` da build `20260324_2021_01_02_PROD`. Esses raws constituem a fonte operacional de D069. ICP/WDI servem apenas como cross-check; eventual divergência não autoriza substituir os fatores PIP nem sustenta explicação causal não demonstrada.

### Separação De D065

D065 alinha a entrada corrente à CDF brasileira em preços médios de 2025. D069 possui pipeline temporal próprio para Mundo, alinhado ao ano global de 2024. Uma decisão não reutiliza automaticamente a referência, o manifesto ou o fator temporal da outra.

### Consequências

- D069 deixa de ser bloqueio metodológico e passa a reger a futura conversão `WORLD_BRL_TO_2021_PPP`;
- `IPCA_CURRENT` deve ser materializado futuramente em artefato ou manifesto Mundo versionado; esta decisão não cria nem autoriza uma constante corrente eterna;
- câmbio comercial, constantes legadas, WDI/ICP como substitutos e arredondamento intermediário permanecem proibidos;
- D069 não autoriza, isoladamente ou em conjunto com a canonização documental de D070, integração numérica do frontend Mundo nem artefato de produção Mundo.

### Evidência

- `data/raw/world/pip/20260324_2021/pip-20260324_2021_01_02_PROD-ppp.raw.csv` — SHA-256 `792476948DA84A005CC9C61C359CB586B42866F850F55973EF7BDC2693347EB6` — `BRA,national,2021,2.44986319541931`;
- `data/raw/world/pip/20260324_2021/pip-20260324_2021_01_02_PROD-cpi.raw.csv` — SHA-256 `E2F558A28FBBD91F69EDB5FEF4BC10DED19F17D315090CB70031F2C993408ABE` — `BRA,national,2021,1` e `BRA,national,2024,1.192919586578344`;
- `validation/world/d069-pip-aux-provenance-production-build-retry.json` — registro da aquisição versionado no HEAD atual; os fatores operacionais e sua proveniência exigida permanecem preservados no alinhamento de preços e no pacote de produção versionados.

### Documentos Afetados

- `04-metodologia-dados.md`;
- `09-fontes-referencias.md`;
- `10-testes-validacao.md`;
- `README.md`.

---

## D070 — Golden Cases, Precisão E Caudas Do Mundo

**Data:** 19/08/2026
**Status:** `ATIVA`

### Decisão

Congelar para esta versão do contrato Mundo:

```text
CURRENT_PRICE_REFERENCE_MONTH = 2026-07
IPCA_CURRENT = 7657.7300000000000
IPCA_AVG_2024 = 6952.07333333333333333333333333333333333333333333333333333333
MAX_ABSOLUTE_ERROR_PP = 0.022516991848920
```

O índice corrente provém do IPCA nacional, SIDRA tabela 1737, variável 2266, número-índice. Julho/2026 é referência operacional versionada desta decisão, não constante corrente eterna. Uma atualização exige nova evidência oficial preservada, atualização explícita do mês e do manifesto aplicável, regeneração dos golden cases, testes e promoção autorizada; a publicação de mês posterior não altera o contrato automaticamente.

O teste versionado espera 11 golden cases. O manifesto registra o artefato `validation/world/world-income-golden-cases-d070-candidate.json` por versão `D070-v1`, SHA-256 `6EA8FB10D9BCE16380E5F311EFA789AC22EEA44BEFF119C33C61B1B0578FF779` e tamanho de 6.956 bytes; o conteúdo detalhado dos casos está versionado no HEAD atual.

O contrato preserva a fórmula e os fatores exatos de D069, a CDF em degraus de D068, precisão interna integral e ausência de arredondamento intermediário.

### Empates E Posição

Preservar:

```text
shareBelow(x) = população com welf < x / população total
shareAtOrBelow(x) = população com welf <= x / população total
topShare(x) = 1 - shareBelow(x)
topPercent(x) = 100 × topShare(x)
```

O resultado deve permanecer subordinado a D067 e ser descrito como **posição monetária global estimada**, nunca como ranking exato de salário, renda bruta homogênea, patrimônio ou riqueza.

### Precisão Visual

Dentro do suporte observado:

1. para `topShare >= 0,01`, exibir percentil inteiro e `TOP` inteiro complementar, derivando um do outro para preservar soma visual de 100;
2. para `0,001 <= topShare < 0,01`, exibir `TOP` com uma casa decimal;
3. para `topPercent < 0,1`, não arredondar os valores usados na decisão e aplicar:

```text
se topPercent + MAX_ABSOLUTE_ERROR_PP < 0,1:
    exibir "menos de 0,1%"
senão:
    exibir "aproximadamente 0,1%"
```

A condição estrita incorpora o erro máximo medido em D068. Não se pode usar automaticamente “menos de 0,1%” apenas porque a estimativa pontual ficou abaixo desse limite.

### Limites Do Suporte

- no mínimo observado, preservar o primeiro degrau e os empates; não usar `TOP 100%` como headline;
- abaixo do mínimo, informar que o valor está fora do suporte inferior observado, sem extrapolar;
- no máximo observado, preservar o último degrau real;
- acima do máximo, informar que o valor está fora do suporte superior observado, sem extrapolar;
- nunca exibir `TOP 0%`;
- nunca criar pisos, tetos ou posições por interpolação/extrapolação arbitrária.

### Evidência E Consequências

O contrato D070 é coberto pelos testes versionados, que esperam 11 golden cases. `validation/world/world-d070-validation.json` está versionado no HEAD atual; `validation/world/world-d070-validation.md` permanece como registro local fora do HEAD. A presença do JSON versionado não deve ser confundida com nova execução de testes nesta reconciliação.

D070 deixa de ser bloqueio metodológico para golden cases, precisão, empates e caudas. Esta canonização não cria artefato de produção Mundo, não integra resultado Mundo ao frontend, não altera Brasil e não autoriza reativar `WORLD_CURVE` ou qualquer fallback legado. Produção e integração exigem tarefa e auditoria posteriores explícitas.

### Estado Posterior Comprovado No Checkout

O limite acima descreve o alcance da decisão D070 no momento de sua canonização. A autorização posterior foi materializada sem reescrever os artefatos históricos: `data/production/world/world-income-engine-manifest.json` registra `status = CANONICAL_APPROVED_FOR_INTEGRATION`, inclui D066–D070 e define `worldFrontendIntegrationAllowed = true`. A CDF e o alinhamento de preços preservam seus flags históricos bloqueados; o loader valida a autorização agregadora antes de calcular.

O histórico Git registra separadamente a validação do pacote (`50efadb`), a integração do resultado Mundo (`74d0117`), a conclusão do frontend V1 (`a63535d`) e o fechamento das lacunas pré-release (`d5b893a`). Esses estados comprovam `VALIDADO` e `INTEGRADO`, não `PUBLICADO`; nenhum deles autoriza deploy.

### Documentos Afetados

- `04-metodologia-dados.md`;
- `10-testes-validacao.md`;
- `README.md`;
- `02-prd-v1.md`.

---

# Apresentação Brasileira — Precisão E Caudas

## D071 — Precisão Visual E Tratamento Da Cauda Brasileira

**Data:** 14/08/2026
**Status:** `ATIVA`

### Decisão

A CDF brasileira continua sendo consultada com precisão interna completa. O arredondamento pertence somente à apresentação.

Para a leitura principal da V1, utilizar `TOP` como linguagem intuitiva e percentil como leitura estatística secundária, conforme a hierarquia já definida no design system.

Definir:

```text
p = 100 × shareBelow
t = 100 - p
```

### Faixa Principal

Quando:

```text
1 <= t
```

e a renda comparável estiver dentro do suporte observado da CDF, exibir os dois números como inteiros complementares:

```text
percentil_exibido = arredondar(p)
top_exibido = 100 - percentil_exibido
```

Exemplo do golden case brasileiro em preços médios de 2025:

```text
p = 70.1561...
percentil exibido = 70
TOP exibido = 30%
```

Para a entrada nominal corrente de R$ 6.500 / 3 com manifesto de julho/2026:

```text
p = 68.6691...
percentil exibido = 69
TOP exibido = 31%
```

Não arredondar percentil e `TOP` separadamente se isso puder produzir soma visual diferente de 100.

### Cauda Superior

Quando:

```text
0.1 <= t < 1
```

exibir uma casa decimal e manter complementaridade visual entre as duas leituras.

Quando:

```text
0 < t < 0.1
```

não exibir `TOP 0%`. Exibir:

> **Entre menos de 0,1% de maior renda na distribuição observada.**

A leitura secundária pode usar:

> **Acima do percentil 99,9.**

sem criar casas adicionais.

### Acima Do Máximo Observado

Se o RDPC comparável do usuário for estritamente maior que:

```text
IBGE_RDPC_MAX_OBSERVED_2025 = 200165.7922757916
```

não extrapolar um percentil mais fino e não exibir `TOP 0%`.

Exibir conceitualmente:

> **Sua renda por pessoa está acima do maior valor observado na distribuição da PNAD 2025 utilizada. A pesquisa não permite estimar com segurança uma posição mais fina nessa cauda.**

A CDF pode retornar `shareBelow = 1` para fins matemáticos internos; isso não autoriza transformar o resultado em uma posição individual exata além do suporte observado.

### Renda Zero

Para RDPC igual a zero, não apresentar `TOP 100%` como resultado principal.

A CDF validada possui massa em zero de aproximadamente:

```text
1.112333% da população ponderada
```

A interface deve usar linguagem neutra, por exemplo:

> **R$ 0 é o menor nível de renda por pessoa observado na distribuição utilizada e há outras pessoas empatadas nesse valor.**

O detalhe da participação empatada pode aparecer em “Como calculamos”, não precisa ser headline.

### Valores Monetários

- renda mensal atual por pessoa: moeda brasileira com duas casas decimais quando exibida;
- renda ajustada para preços médios de 2025: informação metodológica secundária, com duas casas decimais quando mostrada;
- cálculos internos: sem arredondamento prematuro.

### Proibições

Não utilizar:

- `67,934728%` na interface;
- arredondamento para múltiplos de 5 ou 10 apenas por estética;
- `TOP 0%`;
- extrapolação logarítmica ou paramétrica além do máximo observado;
- pisos ou tetos artificiais não derivados da CDF.

### Consequências

- a política de exibição da cauda brasileira deixa de estar pendente;
- a CDF e seus golden cases não são alterados;
- D071 vale somente para Brasil;
- a precisão e as caudas do Mundo são regidas separadamente por D070.

---

## D072 — Entrega E Carregamento Da CDF Brasileira

**Data:** 14/08/2026
**Status:** `ATIVA`

### Evidência

A CDF canônica brasileira possui:

```text
3955036 bytes em JSON bruto
1788882 bytes em gzip -9 local
83358 pontos únicos
```

Em diagnóstico local com Node v22.16.0:

```text
JSON.parse ≈ 18,25 ms
100.000 lookups binários ≈ 7,50 ms
```

Esses tempos são diagnósticos locais e **não representam performance de celular ou rede de produção**. A evidência serve apenas para separar custos: o lookup é barato; a transferência inicial do arquivo é o custo relevante a evitar na primeira dobra mobile.

### Decisão

A CDF brasileira:

- não deve ser incorporada ao bundle JavaScript inicial;
- deve permanecer como artefato estático versionado;
- deve ser carregada sob demanda no primeiro cálculo;
- pode permanecer em memória para novas simulações na mesma sessão;
- pode utilizar cache HTTP normal de conteúdo estático;
- nunca recebe renda, moradores ou qualquer dado individual como parâmetro de requisição.

Os manifestos pequenos do motor e do alinhamento de preços devem ser obtidos/validados conforme o contrato de produção antes do cálculo. Como o manifesto de preços pode mudar após nova publicação mensal aprovada, ele e o manifesto de motor **não devem ser tratados como imutáveis por prazo longo** sem versionamento adicional.

A CDF `2025-20260508-v1`, por outro lado, é imutável enquanto essa versão estiver em produção e não deve ser sobrescrita silenciosamente.

### Falha Segura

Se qualquer artefato necessário estiver ausente, incompatível ou falhar ao carregar:

> **não calcular posição brasileira com constantes antigas ou aproximação.**

A interface deve exibir estado de indisponibilidade e permitir nova tentativa.

Não utilizar como fallback:

- `BRAZIL_THRESHOLDS`;
- PIP para Brasil;
- média nacional;
- CDF parcial criada ad hoc.

### Consequências

- loading após o CTA é legítimo quando corresponde ao primeiro carregamento real da CDF;
- não criar loading artificial quando a CDF já estiver disponível em memória/cache e o cálculo for imediato;
- a validação final de rede, cache e Core Web Vitals pertence ao frontend publicado;
- D072 não autoriza alteração da CDF ou de sua metodologia.

---

## D073 — Metadata Pública E Compartilhamento Genérico Da Home

**Data:** 14/08/2026
**Status:** `ATIVA`

### Decisão

Canonizar para a home da V1:

```text
HOME_TITLE = "Você é mais rico do que quantos brasileiros? | Renda Comparada"
HOME_META_DESCRIPTION = "Descubra onde a renda da sua casa está na distribuição do Brasil e, de forma estimada, no mundo. Comparação de renda, não de patrimônio."
HOME_OG_TITLE = "Você é mais rico do que quantos brasileiros?"
HOME_OG_DESCRIPTION = "Descubra onde a renda da sua casa está no Brasil e, de forma estimada, no mundo."
DEFAULT_SHARE_TEXT = "Descobri onde minha renda está na distribuição brasileira. E você?"
```

O texto padrão de compartilhamento é genérico e não contém:

- renda;
- moradores;
- renda por pessoa;
- percentil;
- `TOP`.

A posição individual só pode ser acrescentada mediante ação explícita do usuário, conforme D017.

### Limites

D073 **não define**:

```text
PRODUCTION_DOMAIN
CANONICAL_URL
DEFAULT_OG_IMAGE
SEARCH_CONSOLE_PROPERTY
```

Esses itens continuam dependentes de domínio/design/configuração.

A metadata não deve descrever o resultado mundial como ranking exato. A expressão **“de forma estimada, no mundo”** preserva D067.

### Consequências

- o Codex não deve improvisar outra promessa comercial na metadata;
- nenhuma informação individual entra em `og:title`, `og:description`, `og:image` ou `og:url`;
- a imagem OG padrão pode ser criada depois, mas deve respeitar o texto e a privacidade já aprovados;
- alterações futuras nesses textos exigem decisão explícita ou revisão documentada de produto/SEO.

---

## D074 — Estado Factual Do Remoto GitHub

**Data:** 20/08/2026
**Status:** `ATIVA`

### Evidência

- o remoto `origin` aponta para `https://github.com/bernardotb/renda-comparada.git`;
- o repositório GitHub está público no momento da inspeção;
- a branch padrão remota é `main`;
- o checkout local pode conter commits e alterações ainda não incorporados à branch padrão remota.

### Consequências

- D052 fica substituída quanto ao estado vigente do remoto, mas permanece preservada como registro histórico;
- a visibilidade pública do repositório não autoriza `push`, merge, release ou deploy;
- o checkout local continua sendo a fonte do estado real das alterações ainda não publicadas no GitHub.

---

# Pendências De Segurança

## SEC-001 — Remover `.env.local` Da Cópia Sincronizada

**Status:** `PENDENTE`

Remover o arquivo da cópia sincronizada quando o caminho local exato do backup for fornecido. Seu conteúdo não deve ser aberto, exibido, copiado ou registrado.

## SEC-002 — Revogar E Renovar O Token Vercel Sincronizado

**Status:** `PENDENTE`

Qualquer token ou segredo anteriormente sincronizado deve ser considerado potencialmente exposto. A revogação e a renovação deverão ocorrer quando a autenticação da Vercel for refeita. O token antigo não deve ser reutilizado ou testado.

---
