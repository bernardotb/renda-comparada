---
title: Visão Do Projeto
created: 2026-08-12T16:37:36.000-03:00
modified: 2026-08-13T09:50:34.315-03:00
---

> [!WARNING] ARQUIVO HISTÓRICO — NÃO CANÔNICO
> Este arquivo preserva a visão e o brainstorm originais do projeto. Ele não deve orientar diretamente a implementação. Em caso de conflito, prevalecem os documentos canônicos atuais; a visão oficial está em `docs/01-visao-produto.md`.

Claro. Vou consolidar o projeto como ele está **até agora**, separando o que já ficou decidido do que ficou para uma etapa posterior.

# Visão Do Projeto

A ideia deixou de ser apenas uma calculadora de percentil de renda.

O produto passa a ter duas grandes perguntas:

> **1. Onde estou financeiramente em relação aos outros?**  
> **2. E o que posso fazer para melhorar minha própria vida financeira?**

A calculadora de renda continua sendo a **porta de entrada simples, curiosa e compartilhável**. Depois do resultado, o site conduz o usuário para educação e organização financeira.

---

## 1. Chamada Principal

Ficou escolhida a abordagem:

> **Você é mais rico do que quantos brasileiros?**  
> **Descubra onde a renda da sua família está no Brasil — e onde ela estaria no mundo.**

Apesar de usar “rico” como gancho, o site deve deixar claro discretamente que:

> **A comparação é baseada em renda, não em patrimônio.**

Isso preserva o impacto da frase sem cometer erro conceitual.

---

## 2. O Que O Usuário Informa

O cálculo começa com apenas duas informações:

**Renda mensal total da casa**

e

**Número de pessoas que vivem dessa renda.**

Aqui entram **todos os moradores**, inclusive crianças e pessoas sem renda.

A formulação que considero mais clara é:

> **Quantas pessoas moram nesta casa?**  
> _Inclua adultos e crianças, mesmo que não tenham renda._

Exemplo:

Renda familiar: R$ 6.500  
Moradores: 3

Resultado intermediário:

**R$ 6.500 ÷ 3 = R$ 2.166,67 por pessoa.**

---

## 3. Brasil: Usar Sempre O Dado Mais Recente Do IBGE

Decidimos abandonar a base 2024 quando houver base metodologicamente equivalente mais recente.

Neste momento, o núcleo brasileiro deve usar:

> **PNAD Contínua — Rendimento de Todas as Fontes 2025 — IBGE**

Não queremos comparar apenas com a renda média brasileira.

Precisamos da **distribuição de renda**, para responder corretamente:

> “Sua renda é maior que a de X% dos brasileiros.”

Portanto:

**PNAD/IBGE → distribuição → percentis brasileiros.**

A média é apenas informação contextual.

---

## 4. Mundo

A inspiração original veio da calculadora **Global Income Percentile**, da AllTools.

Para o lado mundial, nossa arquitetura ficou:

**renda familiar**

→ dividir pelos moradores

→ renda per capita

→ ajustar por **paridade do poder de compra — PPC/PPP**

→ comparar com a distribuição mundial

→ calcular percentil global.

Fonte principal:

**World Bank — Poverty and Inequality Platform (PIP).**

Para PPP/PPC:

**World Bank — International Comparison Program / indicadores PPP.**

---

## 5. Fontes Oficiais Do Projeto

O núcleo ficou bem definido:

|Finalidade|Fonte|
|---|---|
|Distribuição de renda no Brasil|**IBGE — PNAD Contínua**|
|Percentis brasileiros|Calculados a partir da PNAD|
|Comparação por estados|**IBGE/PNAD**, quando houver distribuição adequada|
|Distribuição global|**World Bank — PIP**|
|Poder de compra internacional|**World Bank — PPP/ICP**|
|Inflação e séries históricas|**IBGE — IPCA**|
|Orçamento e padrão de consumo familiar|**IBGE — POF**|
|Crédito, juros e dívidas|**Banco Central do Brasil**|

O Our World in Data pode ser usado para pesquisa e conferência, mas **não precisa ser nossa fonte primária** quando o dado original vem do Banco Mundial.

---

## 6. Atualização Automática Dos Dados

Outra decisão importante:

**não consultar IBGE e Banco Mundial toda vez que alguém fizer um cálculo.**

Arquitetura desejada:

> Fontes oficiais  
> ↓  
> rotina periódica de atualização  
> ↓  
> validação  
> ↓  
> dataset próprio versionado  
> ↓  
> calculadora

Quando surgir uma nova base:

> detectar → baixar → recalcular → comparar diferenças → validar → publicar.

Nada de atualizar silenciosamente resultados de milhares de usuários porque uma API mudou.

A página de metodologia deve mostrar algo como:

> Brasil: PNAD Contínua 2025 — IBGE  
> Mundo: World Bank PIP — versão X  
> PPP: versão X  
> Última atualização: XX/XX/XXXX

---

# 7. Resultado Principal

O resultado precisa ser o grande momento visual.

Algo próximo ao que você já mostrou:

### 🇧🇷 No Brasil

**67,9%**

> Sua renda por pessoa é maior que a de aproximadamente 68 em cada 100 pessoas da população considerada.

E uma leitura mais intuitiva:

> **Você está entre aproximadamente os 32% de maior renda.**

Depois:

### 🌎 No Mundo

**76,6%**

> Você está entre aproximadamente os 23% de maior renda.

Os dois modos são úteis porque:

**percentil 68** é estatisticamente preciso;

**top 32%** é mais intuitivo.

Eu mostraria os dois.

---

# 8. Compartilhamento

Essa ficou como feature essencial.

Depois do resultado:

### **Compartilhar Minha posição**

Com:

WhatsApp  
compartilhamento nativo  
copiar link

Por padrão, **não mostrar renda em reais**.

Dois modos:

**Privado**

> Descobri onde minha renda está na distribuição brasileira. E você?

**Mostrar posição**

> Minha renda está entre os 12% mais altos da distribuição brasileira.

Nunca colocar automaticamente:

> “Minha família ganha R$ 18.000.”

Também não colocar renda em:

URL  
query string  
analytics  
Open Graph  
logs desnecessários.

---

# 9. Card Compartilhável

Imagem automática minimalista:

**RENDA COMPARADA**

### TOP 12%

> Minha posição na distribuição de renda brasileira.

**E você?**

Sem revelar o valor da renda.

Essa é uma das principais ferramentas de viralização.

---

# 10. Segunda Grande Calculadora

Depois da principal:

## **Quanto Preciso Ganhar Para Estar Entre os…**

Opções:

**50% · 20% · 10% · 5% · 1%**

A pessoa informa o número de moradores e recebe:

> Para uma família de quatro pessoas estar aproximadamente entre os 10% de maior renda, a renda familiar seria de aproximadamente R$ X.

Isso deve usar a **mesma distribuição validada da PNAD**, e não aproximações por média.

---

# 11. Simulador De Renda

Outra feature definida:

## **E Se Minha Renda Fosse diferente?**

Um controle permite variar:

R$ 5 mil  
R$ 10 mil  
R$ 15 mil  
R$ 20 mil  
R$ 30 mil…

E observar a posição mudar em tempo real.

Isso aumenta muito a exploração.

---

# 12. Comparação Por Estado

Entrará posteriormente.

Resultado futuro:

**Brasil:** Top X%  
**São Paulo:** Top Y%  
**Mundo:** Top Z%

Mas ficou uma regra importante:

> **Nunca calcular percentil estadual usando apenas a renda média do estado.**

Precisamos de distribuição por UF adequada.

---

# 13. Histórico

Feature posterior:

## **Como Sua Posição Mudou Ao Longo Do tempo?**

Exemplo:

2015  
2020  
2025

Corrigindo valores por inflação e usando distribuições históricas comparáveis.

Fonte:

**PNAD + IPCA.**

---

# 14. “Como vIvem fAmílias pArecidas cOm a mInha?”

Essa ideia entrou e ficou muito boa.

Mas não vamos dizer:

> “Com R$ 15 mil você consegue ter dois carros, escola particular e duas viagens.”

Isso seria arbitrário.

A abordagem será:

## **Como Famílias De Renda Semelhante Costumam gastar?**

Usando a **POF — Pesquisa de Orçamentos Familiares do IBGE**.

Mostrar, quando houver dados adequados:

Moradia  
Alimentação  
Transporte  
Saúde  
Educação  
Lazer  
Outros

E sempre dizer:

> São padrões observados em famílias semelhantes, não uma recomendação de gastos nem uma previsão individual.

---

# 15. A Grande Evolução: Saúde Financeira

Esse foi provavelmente o desenvolvimento conceitual mais importante.

Depois de descobrir:

> “Minha renda está acima da de 68% dos brasileiros.”

a pessoa pode pensar:

> “Então por que meu dinheiro não sobra?”

Essa pergunta vira a ponte para a segunda parte do site.

Eu **não usaria**:

> “O resultado te agradou?”

A melhor transição ficou:

> ### Sua posição de renda conta apenas uma parte da história.
>
> Estar acima de grande parte da população não significa necessariamente ter uma vida financeira saudável.

E então:

# **Quer Descobrir Como Está Sua Vida Financeira De verdade?**

**Fazer meu check-up financeiro →**

---

# 16. Check-up Financeiro

Não queremos um falso “score 82/100”.

Vamos avaliar dimensões separadamente.

As cinco principais:

**Renda relativa**

**Dívidas**

**Reserva de emergência**

**Orçamento**

**Capacidade de poupança/construção de patrimônio**

O resultado pode ser:

> **Renda relativa:** boa  
> **Endividamento:** atenção  
> **Reserva:** insuficiente  
> **Orçamento:** apertado  
> **Capacidade de poupança:** baixa

E depois:

### Sua Prioridade Agora

> Reduzir dívida cara antes de aumentar investimentos.

Isso é muito melhor que um número arbitrário.

---

# 17. Caminhos Depois Do Check-up

O usuário poderá dizer:

**Tenho dívidas**

**Quero saber se gasto demais**

**Não tenho reserva**

**Quero organizar minha vida financeira**

**Quero começar a investir**

**Acho que estou bem e quero conferir**

O site abre um percurso diferente conforme a situação.

---

# 18. Banco Central

Decidimos incorporar ferramentas oficiais do BC como parte importante da educação financeira.

### Registrato / SCR

Ensinar:

1. entrar com gov.br;
2. requisitos da conta;
3. acessar Registrato;
4. consultar **Empréstimos e Financiamentos — SCR**;
5. verificar dívidas e compromissos.

Com botão levando **diretamente ao domínio oficial do Banco Central**.

O nosso site nunca pede senha gov.br.

---

### Valores a Receber

Área:

## **Você Tem Dinheiro esquecido?**

Direcionar ao **Sistema Valores a Receber — SVR**.

Também aproveitar para alertar contra golpes.

---

### Taxas De Juros Do Banco Central

Criar futuramente:

## **Sua Taxa Está cara?**

Usuário informa:

> Meu empréstimo cobra 4,5% a.m.

Nosso site compara com referências do BC para aquela modalidade.

Sempre deixando claro que as taxas variam por cliente, instituição, garantia e perfil de risco.

---

### Calculadora Do Cidadão

Você já usa bastante e decidimos aproveitá-la de duas maneiras.

Primeiro:

> link para a ferramenta oficial.

Segundo — e mais importante:

**criar nossos próprios simuladores mais simples**, utilizando a mesma lógica financeira e citando o Banco Central como referência.

---

# 19. Simuladores Financeiros

A seção poderá ter:

### Juros Compostos

Quanto seu dinheiro pode virar.

### Investimento Mensal

Aporte inicial + aportes mensais.

### Financiamento

Parcela, juros e total pago.

### Dívida

Quanto uma dívida cresce.

### Cartão De Crédito

Custo do saldo não pago.

### Cheque Especial

Quanto custa usar por determinado período.

### Correção Monetária

Quanto um valor antigo representa hoje.

### Comparação De Crédito

Rotativo × cheque especial × crédito pessoal × consignado etc.

Sempre com fonte/metodologia transparente.

---

# 20. Estrutura Maior Do Produto

A arquitetura conceitual passou a ser:

### **Onde estou?**

Renda Brasil × mundo.

### **Como Famílias Como a Minha vivem?**

POF, consumo e orçamento.

### **Como Está Minha Vida financeira?**

Check-up.

### **O Que Posso Fazer Para melhorar?**

Orientação financeira.

### **Simuladores**

Juros, dívidas, financiamento, investimentos.

### **Ferramentas oficiais**

Registrato, Valores a Receber, Banco Central etc.

Isso já é muito mais que uma calculadora.

---

# 21. Orientação, Não “Consultoria fInanceira”

Outra decisão importante.

Eu não chamaria a área de:

> “Consultoria financeira”.

Melhor:

> **Orientação financeira**

ou

> **Cuide melhor do seu dinheiro**

Porque nosso objetivo é:

educação  
simulação  
diagnóstico geral  
orientação

e não:

> “Compre ação X.”

> “Venda fundo Y.”

> “Faça empréstimo no banco Z.”

---

# 22. Estética

A direção estética ficou bastante clara:

> **uma reportagem interativa premium que também é uma calculadora.**

Não uma “calculadora genérica bonita”.

Referências conceituais:

**Financial Times / Economist** — sobriedade  
**Nexo / Our World in Data** — dados e clareza  
**Apple** — espaço e simplicidade

Paleta:

off-white / creme  
quase preto  
verde profundo para Brasil  
azul petróleo/azul profundo para mundo

Sem verde-amarelo exagerado.

---

# 23. Tipografia

Direção escolhida:

**serifada editorial nos grandes títulos**

**sans-serif limpa em interface, números e controles.**

A pergunta:

> **Você é mais rico do que quantos brasileiros?**

deve parecer uma manchete.

Já:

**R$ 6.500**

**67,9%**

**TOP 32%**

precisam ser extremamente legíveis.

---

# 24. Interface

Poucos elementos.

Muito espaço.

Sem:

gradientes chamativos  
glassmorphism  
sombras pesadas  
cifrões decorativos  
cofrinhos  
fotos de família  
confete  
visual de cassino  
gamificação excessiva.

Animações leves:

percentil aparece suavemente;  
marcador desliza;  
Brasil e mundo entram com pequena transição.

---

# 25. Mobile First

Essa ficou essencial.

A principal hipótese de compartilhamento é:

> **WhatsApp → celular → cálculo → resultado → WhatsApp.**

Portanto:

campo monetário simples;  
teclado numérico;  
botões grandes;  
resultado imediatamente visível;  
compartilhamento em um toque.

---

# 26. SEO E Conteúdo

O site não deve depender apenas da calculadora.

Teremos páginas como, futuramente:

`/quanto-ganha-top-1-brasil`

`/renda-top-10-brasil`

`/renda-familiar`

`/renda-per-capita`

`/metodologia`

`/brasil`

`/mundo`

e conteúdos:

> R$ 10 mil é uma renda alta?

> Quanto precisa ganhar para estar no 1%?

> O que é renda per capita?

> Média e mediana são a mesma coisa?

Essas páginas levam novamente para a calculadora.

---

# 27. Métrica De Sucesso

Não queremos medir apenas visitas.

Funil:

**visitou**

→ **começou cálculo**

→ **concluiu**

→ **compartilhou**

→ **voltou/explorou**

→ **fez check-up**

→ **utilizou simulador**

Um indicador particularmente importante:

> **compartilhamentos ÷ cálculos concluídos**

---

# Prioridade De Implementação

Eu resumiria agora assim:

### **P0 — Transformar a Calculadora atual**

Slogan novo, PNAD 2025, metodologia correta, resultado visual, privacidade, compartilhamento, SEO e mobile.

### **P1 — Aumentar Curiosidade E viralização**

“Quanto preciso ganhar para estar no X%?”, simulador de renda, card compartilhável e páginas de busca.

### **P2 — Transformar Em Ferramenta financeira**

Check-up, Registrato, juros do BC, simuladores, educação financeira.

### **P3 — Aprofundar a Realidade Da família**

POF, estilo de consumo, comparação estadual, custo de vida e histórico.

---

## E a Ideia Central Que Eu Preservaria

A pessoa entra querendo responder:

> **“Sou mais rico que quantos brasileiros?”**

Mas o site não termina aí.

Ele provoca uma segunda pergunta muito mais importante:

> **“Se minha renda é relativamente boa, por que minha situação financeira talvez não seja?”**

E então entrega:

> **“Onde estou financeiramente — e o que posso fazer para melhorar?”**

Para mim, **esse é o projeto que construímos até agora**.
