---
title: Decisoes
created: 2026-08-12T18:04:56.000-03:00
modified: 2026-08-12T18:09:55.798-03:00
---
````markdown
# Registro de Decisões — Renda Comparada

**Produto:** Renda Comparada  
**Documento:** `decisoes.md`  
**Status:** Canônico para decisões de produto e metodologia  
**Versão:** 1.0  
**Última revisão:** 12/08/2026

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
````

Status possíveis:

- `ATIVA`
    
- `SUBSTITUÍDA`
    
- `REVOGADA`
    
- `EM REVISÃO`

---

# D001 — Tese central do produto

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

# D002 — Chamada principal

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Usar como principal gancho:

> # Você é mais rico do que quantos brasileiros?

Subtítulo:

> **Descubra onde a renda da sua família está no Brasil — e onde ela estaria no mundo.**

## Limite conceitual

A interface deve esclarecer:

> **A comparação é baseada em renda, não em patrimônio.**

---

# D003 — Renda versus patrimônio

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

# D004 — Entrada principal

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

# D005 — Todos os moradores entram no cálculo brasileiro

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O número de moradores deve incluir:

- adultos;
    
- crianças;
    
- pessoas sem renda;

conforme a metodologia do rendimento domiciliar per capita adotado.

A interface deve explicitar:

> **Inclua adultos e crianças, mesmo que não tenham renda.**

---

# D006 — Conceito brasileiro principal

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Para o Brasil, utilizar:

> **rendimento domiciliar per capita**

Estrutura:

```text
renda total da casa
÷
número de moradores
```

---

# D007 — Fonte brasileira

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A fonte primária brasileira será:

> **IBGE — PNAD Contínua**

A referência inicial da V1 será:

> **Rendimento de Todas as Fontes 2025**

até aprovação de edição metodologicamente equivalente mais recente.

---

# D008 — Média não calcula percentil

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Não utilizar a renda média nacional como mecanismo para inferir percentil.

Percentis devem vir da:

> **distribuição ponderada da renda**

ou representação derivada validada.

---

# D009 — Uso de microdados e pesos

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A distribuição brasileira deve respeitar:

- microdados adequados;
    
- pesos amostrais oficiais;
    
- unidade estatística definida.

Não tratar registros da PNAD como observações de peso igual.

---

# D010 — Fonte mundial

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A fonte principal mundial será:

> **World Bank — Poverty and Inequality Platform — PIP**

Não utilizar WID e PIP misturados no mesmo cálculo.

---

# D011 — Poder de compra internacional

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A comparação mundial deve utilizar:

> **PPP/PPC**

e não simplesmente câmbio BRL/USD.

A fonte principal será o Banco Mundial / ICP.

---

# D012 — Resultado mundial é estimativa

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

# D013 — Atualização dos dados

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

# D014 — Publicação de nova base

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

# D015 — Ordem da jornada principal

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

# D016 — Compartilhamento vem antes do check-up

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

# D017 — Compartilhamento privado por padrão

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

O compartilhamento padrão não mostra:

- renda;
    
- renda per capita;
    
- moradores.

Pode mostrar posição apenas mediante ação explícita.

---

# D018 — Check-up é opcional

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

# D020 — Check-up sem score único

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

# D021 — Prioridades antes de produtos

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

# D022 — Orientação, não consultoria financeira

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

# D023 — Uso de ferramentas públicas

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

# D024 — Cursos públicos

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

# D025 — POF para padrões de gasto

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

A futura funcionalidade:

> **Como famílias semelhantes costumam gastar?**

deve utilizar dados adequados da:

> **IBGE — POF**

Não inventar estilo de vida a partir da renda.

---

# D026 — Não prescrever estilo de vida

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Não afirmar:

> “Com R$ 15 mil você consegue ter dois carros, escola particular e viajar.”

Preferir:

> padrões observados em famílias comparáveis.

---

# D027 — Custo real das escolhas

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

# D028 — Não virar portal genérico de calculadoras

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

# D030 — Mobile first

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

# D031 — SEO progressivo

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

# D032 — Métrica principal da V1

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

# D033 — Analytics sem renda

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

# D034 — Coleta mínima

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Na V1:

> **se não precisamos guardar, não guardamos.**

A renda não deve ser persistida por padrão.

---

# D035 — Renda fora de URLs

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

# D036 — Preferência por cálculo local

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Quando tecnicamente adequado, processar a renda no navegador.

Evitar transmitir valores financeiros desnecessariamente ao servidor.

---

# D037 — Backlog não é escopo

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Itens do:

`08-roadmap-backlog.md`

não devem ser implementados sem promoção explícita para um PRD ativo.

---

# D038 — V1 congelada em torno do núcleo

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

# D039 — Golden cases somente após auditoria

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

# D040 — Falhar com segurança

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

# D041 — Fonte primária antes de conveniência

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

# D042 — AllTools como inspiração, não fonte

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

# D043 — Hierarquia documental

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Para temas específicos:

### Cálculos e dados

`04-metodologia-dados.md`

### Escopo da versão

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

# D044 — Codex não decide escopo

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

# D045 — Primeiro trabalho do Codex

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

# D046 — Testes antes de mudança estatística

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

# D047 — Documentação é parte do produto

**Data:** 12/08/2026  
**Status:** `ATIVA`

## Decisão

Mudanças relevantes devem atualizar os documentos correspondentes.

O código não deve divergir silenciosamente da documentação canônica.

---

# 3. Como revisar uma decisão

Para revisar uma decisão:

1. não apagar a decisão antiga;
    
2. marcar como `SUBSTITUÍDA` ou `REVOGADA`;
    
3. criar nova decisão;
    
4. registrar motivo;
    
5. atualizar documentos afetados;
    
6. atualizar testes quando necessário.

---

# 4. Modelo para nova decisão

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

# 5. Regra final

Este documento existe para preservar:

> **coerência**

> **memória de projeto**

> **intenção**

> **responsabilidade pelas decisões**

Uma decisão nova deve ser consciente.

Não deve surgir apenas porque:

> “o Codex achou melhor fazer assim.”
# Consolidação Técnica — Fase 0

## D012 — Raiz Canônica Do Projeto

**Data:** 12/08/2026  
**Status:** aprovada e executada

A raiz canônica do projeto Renda Comparada passa a ser:

`C:\Users\Usuario\Downloads\Novos Vaults\vault-template-main\vault-template-main\Tools and Knowlegde\Calculadora de renda`

Ela reúne código-fonte, documentação canônica, manifestos, configurações de build, Git e vínculo local com o projeto Vercel existente.

A antiga raiz técnica em `C:\Users\Usuario\OneDrive\Documentos\ChatGPT\3` foi preservada sem exclusão e não deve receber novas alterações do projeto. Sua remoção ou arquivamento exige decisão posterior.

Esta consolidação não altera funcionalidades, metodologia, percentis, textos da interface ou resultados estatísticos.

---
