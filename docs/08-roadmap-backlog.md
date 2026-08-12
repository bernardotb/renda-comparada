---
title: 08-roadmap-backlog
created: 2026-08-12T17:43:00.000-03:00
modified: 2026-08-12T17:56:51.641-03:00
---

# 08-roadmap-backlog

# Roadmap E Backlog — Renda Comparada

**Produto:** Renda Comparada  
**Documento:** `08-roadmap-backlog.md`  
**Status:** Canônico para ideias futuras e priorização  
**Versão:** 1.0  
**Última revisão:** 12/08/2026

Documentos relacionados:

- `01-visao-produto.md`
- `02-prd-v1.md`
- `03-jornada-ux-v1.md`
- `04-metodologia-dados.md`
- `05-design-system.md`
- `06-privacidade-seguranca.md`
- `07-seo-analytics-crescimento.md`
- `09-fontes-referencias.md`
- `10-testes-validacao.md`

---

# 1. Função Deste Documento

Este documento registra:

- funcionalidades futuras;
- ideias;
- hipóteses;
- oportunidades;
- experimentos;
- novas calculadoras;
- expansões do produto;
- necessidades de pesquisa;
- funcionalidades adiadas;
- funcionalidades descartadas.

Seu objetivo é permitir que o projeto continue acumulando boas ideias **sem transformar cada ideia em requisito de desenvolvimento**.

---

# 2. Regra Fundamental

> # Um item estar neste documento não significa que deve ser implementado.

O Codex não deve implementar nenhum item deste backlog apenas porque ele está documentado.

Para entrar em desenvolvimento, o item deve ser:

1. avaliado;
2. priorizado;
3. promovido explicitamente para uma versão;
4. incluído no PRD correspondente.

---

# 3. Fonte De Autoridade Para Implementação

Para a versão atual:

> **`02-prd-v1.md` prevalece sobre este documento.**

Se houver conflito:

```text
PRD
↓
roadmap
↓
backlog
```

O backlog nunca aumenta silenciosamente o escopo de uma versão.

---

# 4. Diferença Entre Roadmap E Backlog

## Roadmap

Indica:

> **em que direção o produto provavelmente evoluirá.**

É estratégico.

---

## Backlog

Registra:

> **ideias específicas que talvez sejam implementadas.**

É um inventário de oportunidades.

---

# 5. Status Dos Itens

Todo item relevante deve possuir um dos seguintes status.

## `IDEIA`

Ainda não avaliado suficientemente.

## `PESQUISAR`

Precisa de pesquisa técnica, metodológica ou de usuário.

## `VALIDADO-CONCEITUALMENTE`

A ideia faz sentido para o produto, mas ainda não foi priorizada.

## `CANDIDATO`

Bom candidato para versão próxima.

## `PLANEJADO`

Aprovado para uma versão futura específica.

## `EM-DESENVOLVIMENTO`

Já promovido para PRD e sendo implementado.

## `ENTREGUE`

Já está em produção.

## `BLOQUEADO`

Depende de dados, tecnologia, metodologia ou decisão externa.

## `ADIADO`

Faz sentido, mas não agora.

## `REJEITADO`

Foi analisado e decidido que não pertence ao produto.

---

# 6. Regra De Promoção

Um item só deve sair de:

```text
IDEIA
```

para:

```text
PLANEJADO
```

quando soubermos:

- qual problema resolve;
- para quem;
- quais dados exige;
- qual metodologia utiliza;
- qual impacto esperado;
- qual complexidade;
- quais riscos;
- como será medido.

---

# 7. Critérios De Priorização

Cada funcionalidade deve ser avaliada por:

### Alinhamento

Ajuda a responder:

> **Onde estou financeiramente?**

ou:

> **O que posso fazer para melhorar?**

### Utilidade

Resolve uma decisão real?

### Demanda

Usuários demonstram interesse?

### Confiança

Temos dados confiáveis?

### Diferenciação

Melhora significativamente o produto?

### Compartilhamento

Possui potencial orgânico?

### Complexidade

Quanto custa implementar e manter?

### Privacidade

Exige dados pessoais adicionais?

### Risco

Pode gerar orientação errada ou interpretação equivocada?

---

# 8. Pergunta De Filtro

Antes de adicionar uma funcionalidade ao roadmap:

> **Ela ajuda uma família a compreender sua situação financeira, entender para onde seu dinheiro está indo ou tomar uma decisão financeira melhor?**

Se a resposta for:

> **não**

a funcionalidade provavelmente não pertence ao núcleo do Renda Comparada.

---

# 9. Estrutura Macro Do Roadmap

A direção atual do produto pode ser representada por:

```text
V1
Comparação de renda confiável e compartilhável
        ↓
V2
Exploração da própria renda
        ↓
V3
Saúde financeira
        ↓
V4
Orientação e ferramentas
        ↓
V5
Realidade financeira da família
        ↓
V6+
Decisões financeiras mais complexas
```

As versões são conceituais.

A numeração definitiva poderá mudar.

---

# PARTE I — V1

# 10. V1 — Comparação De Renda

**Status:** `PLANEJADO / EM DESENVOLVIMENTO`

A V1 é definida em:

`02-prd-v1.md`

Seu núcleo é:

```text
RENDA + MORADORES
↓
BRASIL
↓
MUNDO
↓
INTERPRETAÇÃO
↓
COMPARTILHAMENTO
```

---

# 11. O Que Pertence à V1

A V1 deve concentrar esforço em:

- cálculo brasileiro;
- cálculo mundial;
- metodologia correta;
- resultado claro;
- compartilhamento;
- privacidade;
- mobile;
- SEO básico;
- analytics básico;
- fontes;
- confiança.

---

# 12. Regra De Congelamento Da V1

Até a V1 ser validada:

> **evitar adicionar novas grandes funcionalidades.**

Novas ideias devem ser colocadas neste arquivo.

Não diretamente no PRD.

---

# PARTE II — V2: EXPLORAÇÃO DA RENDA

# 13. Quanto Preciso Ganhar Para Estar no Top X%?

**ID:** `INC-001`  
**Status:** `CANDIDATO`

Pergunta:

> **Quanto minha família precisaria ganhar para estar entre os 50%, 20%, 10%, 5% ou 1% de maior renda?**

---

# 14. Experiência Proposta

Usuário informa:

> número de moradores.

Depois escolhe:

```text
50%
20%
10%
5%
1%
```

Resultado:

> **Para uma família de quatro pessoas estar aproximadamente entre os 10% de maior renda, a renda familiar correspondente seria aproximadamente R$ X.**

---

# 15. Dependência Metodológica

Essa funcionalidade deve utilizar:

> **a mesma distribuição brasileira validada da calculadora principal.**

Nunca utilizar:

- média;
- matéria jornalística;
- cortes encontrados em blogs;
- aproximação manual.

---

# 16. Valor Estratégico

Essa funcionalidade possui potencial elevado de:

- curiosidade;
- SEO;
- compartilhamento;
- conteúdo editorial.

---

# 17. E Se Minha Renda Fosse Diferente?

**ID:** `INC-002`  
**Status:** `CANDIDATO`

Criar simulador interativo:

> **E se minha renda fosse diferente?**

Controle:

```text
R$ 5 mil
R$ 10 mil
R$ 15 mil
R$ 20 mil
R$ 30 mil
…
```

O resultado muda em tempo real.

---

# 18. Objetivo Do Simulador

Permitir explorar:

> como mudanças de renda alteram a posição relativa.

Pode gerar perguntas como:

> “Quanto eu teria que ganhar para subir 10 pontos percentuais?”

---

# 19. Requisito

O simulador deve reutilizar:

- mesmo dataset;
- mesmas funções;
- mesma metodologia;
- mesma referência temporal.

Não criar um segundo cálculo independente.

---

# 20. Comparação De Cenários

**ID:** `INC-003`  
**Status:** `IDEIA`

Permitir comparar:

```text
Hoje
R$ 8.000

Cenário
R$ 12.000
```

Resultado:

```text
Hoje: Top X%
Cenário: Top Y%
```

Pode ajudar em:

- negociação salarial;
- planejamento;
- curiosidade.

---

# PARTE III — V3: CHECK-UP FINANCEIRO

# 21. Check-up Financeiro Completo

**ID:** `FIN-001`  
**Status:** `VALIDADO-CONCEITUALMENTE`

Objetivo:

> ajudar o usuário a compreender sua situação financeira além da renda relativa.

---

# 22. Dimensões Previstas

Primeira estrutura:

### Renda Relativa

### Dívidas

### Reserva De Emergência

### Orçamento

### Capacidade De Poupança

---

# 23. Resultado Do Check-up

Não utilizar inicialmente:

```text
82/100
```

Preferir:

```text
Renda relativa: estável
Dívidas: atenção
Reserva: insuficiente
Orçamento: apertado
Poupança: baixa
```

Depois:

> **Sua principal prioridade agora**

---

# 24. Dependência Crítica

Antes da implementação deve ser criado um:

> **modelo de decisão financeira**

que determine legitimamente quais conclusões podem ser feitas a partir de cada resposta.

Não permitir que a IA ou o código improvisem prioridades.

---

# 25. Perguntas Candidatas

O check-up poderá perguntar:

- possui dívidas?
- possui cartão parcelado?
- utiliza rotativo?
- utiliza cheque especial?
- possui empréstimos?
- quanto da renda vai para moradia?
- quanto consegue poupar?
- possui reserva?
- quantos meses de despesas a reserva cobre?
- possui objetivos financeiros?

As perguntas definitivas ainda precisam ser desenhadas.

---

# 26. Check-up Sem Cadastro

**ID:** `FIN-002`  
**Status:** `CANDIDATO`

Preferência:

> permitir diagnóstico completo sem criar conta.

As respostas podem ser processadas localmente sempre que possível.

---

# 27. Salvar Diagnóstico

**ID:** `FIN-003`  
**Status:** `ADIADO`

Possibilidade futura:

> permitir ao usuário salvar seu diagnóstico e comparar evolução.

Isso exigiria:

- conta;
- persistência;
- segurança;
- privacidade;
- LGPD;
- exclusão;
- autenticação.

Não implementar enquanto o benefício não justificar a complexidade.

---

# PARTE IV — V4: ORIENTAÇÃO FINANCEIRA

# 28. Próximo Passo Recomendado

**ID:** `GUIDE-001`  
**Status:** `VALIDADO-CONCEITUALMENTE`

Após o check-up:

> mostrar até três prioridades.

Exemplo:

```text
1. Eliminar dívida cara
2. Criar reserva de emergência
3. Começar planejamento de longo prazo
```

---

# 29. Regra

Não recomendar:

> produto financeiro específico.

Preferir:

> categoria de ação.

---

# 30. Trilhas Financeiras

**ID:** `GUIDE-002`  
**Status:** `CANDIDATO`

Possíveis trilhas:

### Organizar Meu Dinheiro

### Sair Das Dívidas

### Criar Minha Reserva

### Planejar Meu Futuro

### Começar a Investir

### Conferir Se Estou Bem

---

# 31. Trilha — Sair Das Dívidas

Fluxo possível:

```text
identificar dívidas
↓
consultar Registrato
↓
entender taxa
↓
calcular custo
↓
comparar taxas
↓
avaliar renegociação
↓
educação financeira
```

---

# 32. Trilha — Construir Reserva

Fluxo possível:

```text
estimativa de despesas essenciais
↓
meta de reserva
↓
prazo
↓
aporte mensal
↓
acompanhamento
```

---

# 33. Recomendações De Cursos Públicos

**ID:** `EDU-001`  
**Status:** `CANDIDATO`

O site poderá indicar cursos gratuitos de:

- Banco Central;
- Enap;
- CVM;
- Senacon;
- outras instituições aprovadas.

---

# 34. Recomendação Contextual De Curso

Exemplo:

Usuário indica:

> dificuldade de controlar orçamento.

Resultado:

> **Curso recomendado: Gestão de Finanças Pessoais — Banco Central / Enap**

Outro usuário:

> endividamento relevante.

Resultado:

> material da Senacon sobre crédito e superendividamento.

---

# 35. Não Criar Curso Próprio Inicialmente

**ID:** `EDU-002`  
**Status:** `ADIADO`

O produto não precisa criar um curso próprio enquanto instituições públicas já oferecem materiais confiáveis.

Nosso valor é:

```text
diagnóstico
↓
contexto
↓
melhor recurso
```

---

# PARTE V — FERRAMENTAS OFICIAIS

# 36. Registrato

**ID:** `BC-001`  
**Status:** `CANDIDATO`

Criar página educativa:

> **Veja suas dívidas e relacionamentos financeiros no Registrato**

O site:

- explica;
- orienta;
- encaminha.

Não coleta credenciais.

---

# 37. Sistema De Informações De Créditos — SCR

**ID:** `BC-002`  
**Status:** `CANDIDATO`

Ajudar o usuário a compreender:

- o que aparece;
- como acessar;
- como interpretar;
- como utilizar a informação para organizar dívidas.

---

# 38. Valores a Receber

**ID:** `BC-003`  
**Status:** `CANDIDATO`

Página:

> **Você tem dinheiro esquecido?**

Encaminhamento direto ao serviço oficial.

Também incluir:

> alerta contra golpes.

---

# 39. Calculadora Do Cidadão

**ID:** `BC-004`  
**Status:** `CANDIDATO`

Duas possibilidades:

### Referência

Link para ferramenta oficial.

### Validação

Comparar resultados de nossos simuladores com lógica financeira equivalente.

---

# 40. Sua Taxa Está Cara?

**ID:** `BC-005`  
**Status:** `PESQUISAR`

Usuário informa:

```text
modalidade
taxa
prazo
```

Site compara com estatísticas do Banco Central.

Resultado:

> sua taxa está abaixo / próxima / acima das referências observadas.

---

# 41. Limitação

Não concluir:

> “Seu banco está cobrando juros abusivos.”

somente porque a taxa está acima da média.

Taxas variam por:

- perfil;
- garantia;
- prazo;
- risco;
- instituição.

---

# PARTE VI — SIMULADORES FINANCEIROS

# 42. Juros Compostos

**ID:** `SIM-001`  
**Status:** `CANDIDATO`

Entradas:

- valor inicial;
- aporte mensal;
- taxa;
- prazo.

Resultados:

- total aportado;
- rendimento;
- saldo final.

---

# 43. Investimento Mensal

**ID:** `SIM-002`  
**Status:** `CANDIDATO`

Objetivo:

> mostrar a diferença entre aportes e crescimento composto.

Evitar prometer retorno futuro.

---

# 44. Dívida

**ID:** `SIM-003`  
**Status:** `CANDIDATO`

Mostrar:

> quanto uma dívida cresce ao longo do tempo.

Resultado deve enfatizar:

- juros pagos;
- saldo;
- prazo.

---

# 45. Cartão De Crédito

**ID:** `SIM-004`  
**Status:** `CANDIDATO`

Objetivo:

> explicar custo de não pagar a fatura integral.

Usar taxas inseridas pelo usuário ou referências oficiais claramente identificadas.

---

# 46. Cheque Especial

**ID:** `SIM-005`  
**Status:** `CANDIDATO`

Mostrar custo de utilização por:

- dias;
- valor;
- taxa.

---

# 47. Financiamento

**ID:** `SIM-006`  
**Status:** `CANDIDATO`

Mostrar:

- parcela;
- juros;
- total pago;
- custo efetivo quando disponível.

---

# 48. SAC × Price

**ID:** `SIM-007`  
**Status:** `IDEIA`

Comparar:

- primeira parcela;
- evolução;
- total de juros;
- saldo devedor.

---

# 49. Amortização Adicional

**ID:** `SIM-008`  
**Status:** `IDEIA`

Pergunta:

> **O que acontece se eu amortizar R$ X por mês?**

Mostrar:

- redução de prazo;
- redução de juros.

---

# 50. Correção Monetária

**ID:** `SIM-009`  
**Status:** `CANDIDATO`

Pergunta:

> **Quanto R$ X de um ano equivalem hoje?**

Fonte:

> IPCA / outros índices oficialmente definidos.

---

# 51. Custo Real Do Crédito

**ID:** `SIM-010`  
**Status:** `IDEIA`

Comparar:

```text
valor recebido
↓
parcelas
↓
total pago
↓
juros
↓
CET
```

---

# PARTE VII — COMO FAMÍLIAS SEMELHANTES VIVEM

# 52. Padrão De Gastos Por Renda

**ID:** `POF-001`  
**Status:** `BLOQUEADO / PESQUISAR`

Pergunta:

> **Como famílias com renda semelhante costumam gastar?**

Fonte:

> **IBGE — POF**

---

# 53. Categorias Previstas

- moradia;
- alimentação;
- transporte;
- saúde;
- educação;
- lazer;
- outros.

---

# 54. Linguagem Obrigatória

Não dizer:

> “Você deveria gastar X% em alimentação.”

se os dados apenas mostram comportamento observado.

Preferir:

> **Famílias desse grupo costumam destinar aproximadamente X% a essa categoria.**

---

# 55. Limitação Temporal

A adoção plena deverá avaliar a edição mais recente disponível da POF e sua defasagem.

Não apresentar dados antigos como comportamento atual sem contexto.

---

# 56. Comparação Usuário × Famílias Semelhantes

**ID:** `POF-002`  
**Status:** `IDEIA`

Exemplo:

```text
Sua família
Moradia: 38%

Famílias semelhantes
Moradia: ~27%
```

Resultado:

> **Sua moradia representa uma parcela maior da renda que a observada nesse grupo.**

Não afirmar automaticamente que isso é errado.

---

# PARTE VIII — COMPARAÇÕES REGIONAIS

# 57. Comparação Por Estado

**ID:** `REG-001`  
**Status:** `PESQUISAR`

Resultado possível:

```text
Brasil: Top 20%
São Paulo: Top 28%
Mundo: Top 12%
```

---

# 58. Dependência

Precisa existir:

> distribuição adequada para cada UF.

É proibido inferir percentil estadual utilizando somente:

> renda média estadual.

---

# 59. Incerteza Estadual

Avaliar:

- tamanho amostral;
- pesos;
- erros;
- caudas da distribuição;
- estabilidade.

Pode ser necessário apresentar menos precisão.

---

# 60. Comparação Municipal

**ID:** `REG-002`  
**Status:** `BLOQUEADO`

Pergunta futura:

> **Onde minha renda está em Ribeirão Preto?**

Não assumir que a PNAD oferece precisão municipal adequada.

Exige metodologia e fonte próprias.

---

# 61. Custo De Vida Regional

**ID:** `REG-003`  
**Status:** `PESQUISAR`

Objetivo:

> mostrar como a mesma renda pode significar realidades diferentes dependendo da localização.

Essa funcionalidade exige fonte confiável e metodologicamente consistente.

---

# PARTE IX — HISTÓRICO

# 62. Como Minha Posição Mudou Ao Longo Do Tempo?

**ID:** `HIST-001`  
**Status:** `PESQUISAR`

Pergunta:

> **Onde uma renda equivalente estaria em 2015, 2020 e 2025?**

---

# 63. Dependências

Precisa considerar:

- PNAD histórica;
- pesos;
- mudanças metodológicas;
- inflação;
- comparabilidade;
- quebras de série.

Não apenas aplicar IPCA sobre a distribuição atual.

---

# 64. Visualização Histórica

Possível:

```text
2015 ─ Top 35%
2020 ─ Top 30%
2025 ─ Top 25%
```

A interpretação deve deixar claro que se trata de comparação entre distribuições históricas.

---

# PARTE X — CARRO E MOBILIDADE

# 65. Custo Real Do Carro

**ID:** `CAR-001`  
**Status:** `VALIDADO-CONCEITUALMENTE`

Objetivo:

> mostrar quanto um automóvel realmente custa à família.

---

# 66. Componentes

- combustível;
- IPVA;
- licenciamento;
- seguro;
- manutenção;
- pneus;
- estacionamento;
- financiamento;
- depreciação.

---

# 67. Resultado

Não apenas:

> **Seu carro custa R$ 2.180/mês.**

Também:

> **Isso representa 18% da renda mensal da sua família.**

---

# 68. Custo Por Quilômetro

**ID:** `CAR-002`  
**Status:** `IDEIA`

Resultado:

> **R$ X/km**

Útil para comparar:

- carro;
- aplicativo;
- transporte público;
- segundo carro.

---

# 69. Gasolina × Etanol

**ID:** `CAR-003`  
**Status:** `IDEIA`

Não utilizar simplesmente:

> regra fixa de 70%.

Considerar:

- preço atual;
- consumo real do veículo.

---

# 70. Elétrico × Combustão

**ID:** `CAR-004`  
**Status:** `PESQUISAR`

Comparar:

- preço de compra;
- energia;
- combustível;
- manutenção;
- seguro;
- impostos;
- depreciação;
- horizonte de uso.

---

# 71. Trocar Ou Manter O Carro

**ID:** `CAR-005`  
**Status:** `IDEIA`

Pergunta:

> **É financeiramente melhor continuar com meu carro ou trocar?**

Complexidade maior.

Exige premissas transparentes.

---

# PARTE XI — MORADIA

# 72. Custo Real Da Moradia

**ID:** `HOME-001`  
**Status:** `VALIDADO-CONCEITUALMENTE`

Mostrar:

- aluguel/prestação;
- condomínio;
- IPTU;
- seguro;
- manutenção;
- reformas;
- juros;
- outros custos recorrentes.

---

# 73. Percentual Da Renda

Resultado principal:

> **Sua moradia consome aproximadamente X% da renda familiar.**

A interpretação precisa evitar regra universal arbitrária.

---

# 74. Comprar × Alugar

**ID:** `HOME-002`  
**Status:** `PESQUISAR`

Comparar:

- aluguel;
- preço do imóvel;
- financiamento;
- entrada;
- juros;
- manutenção;
- valorização;
- custo de oportunidade.

---

# 75. Amortizar × Investir

**ID:** `HOME-003`  
**Status:** `PESQUISAR`

Ferramenta potencialmente útil, porém mais complexa.

Precisa deixar claro:

- premissas;
- risco;
- tributação;
- retornos hipotéticos.

Não transformar em recomendação personalizada de investimento.

---

# 76. Preço De Imóvel Para Aluguel

**ID:** `HOME-004`  
**Status:** `IDEIA`

Calcular:

- aluguel;
- yield bruto;
- custos;
- yield líquido aproximado.

---

# PARTE XII — CONTAS DA CASA

# 77. Energia

**ID:** `UTIL-001`  
**Status:** `IDEIA`

Objetivo:

> compreender o peso da conta de energia na renda.

Pode mostrar:

```text
R$ 600/mês
R$ 7.200/ano
6% da renda familiar
```

---

# 78. Economia De Energia

**ID:** `UTIL-002`  
**Status:** `IDEIA`

Exemplo:

> **Uma redução de 15% representaria aproximadamente R$ X por ano.**

---

# 79. Energia Solar

**ID:** `UTIL-003`  
**Status:** `PESQUISAR`

Calcular retorno potencial considerando:

- consumo;
- tarifa;
- investimento;
- geração;
- localização;
- regras vigentes.

Essa funcionalidade depende fortemente de dados e regulamentação atualizados.

---

# 80. Água

**ID:** `UTIL-004`  
**Status:** `IDEIA`

Mostrar:

- gasto mensal;
- anual;
- percentual da renda;
- economia potencial.

---

# 81. Internet E Telefonia

**ID:** `UTIL-005`  
**Status:** `IDEIA`

Mostrar:

```text
mensal
anual
5 anos
% da renda
```

---

# 82. Assinaturas

**ID:** `UTIL-006`  
**Status:** `IDEIA`

Somar:

- streaming;
- software;
- academias;
- clubes;
- outros recorrentes.

Resultado:

> **Suas assinaturas custam R$ X por ano.**

---

# PARTE XIII — FAMÍLIA

# 83. Educação

**ID:** `FAM-001`  
**Status:** `IDEIA`

Ferramenta futura para entender:

> peso da educação no orçamento familiar.

Não avaliar automaticamente se escola particular é “cara demais”.

---

# 84. Saúde

**ID:** `FAM-002`  
**Status:** `IDEIA`

Mostrar:

- plano;
- medicamentos;
- consultas;
- outros gastos;
- percentual da renda.

---

# 85. Reserva Familiar

**ID:** `FAM-003`  
**Status:** `CANDIDATO`

Pergunta:

> **Quantos meses sua família conseguiria viver se a renda parasse hoje?**

Fórmula simples:

```text
reserva disponível
/
despesas essenciais mensais
```

---

# PARTE XIV — PATRIMÔNIO

# 86. Patrimônio Líquido

**ID:** `WEALTH-001`  
**Status:** `PESQUISAR`

O produto começa comparando renda.

Futuramente pode explicar:

> **renda é diferente de patrimônio.**

Possível cálculo:

```text
ativos
-
dívidas
=
patrimônio líquido
```

---

# 87. Comparação Patrimonial

**ID:** `WEALTH-002`  
**Status:** `ADIADO`

Comparar patrimônio do usuário com distribuições populacionais exigiria:

- fonte adequada;
- metodologia própria;
- alta cautela.

Não reutilizar a metodologia de renda.

---

# PARTE XV — CONTEÚDO E SEO

# 88. Quanto Ganha O Top 1%?

**ID:** `SEO-001`  
**Status:** `CANDIDATO`

Página baseada na distribuição validada.

---

# 89. Quanto Ganha O Top 10%?

**ID:** `SEO-002`  
**Status:** `CANDIDATO`

Mesma regra.

---

# 90. O Que É Renda per Capita?

**ID:** `SEO-003`  
**Status:** `CANDIDATO`

Conteúdo educativo evergreen.

---

# 91. Média × Mediana

**ID:** `SEO-004`  
**Status:** `CANDIDATO`

Importante para combater interpretações erradas.

---

# 92. R$ 10 Mil É Uma Renda Alta?

**ID:** `SEO-005`  
**Status:** `CANDIDATO`

A resposta deve considerar composição familiar.

CTA:

> **Calcule para sua família.**

---

# 93. R$ 20 Mil É Rico?

**ID:** `SEO-006`  
**Status:** `CANDIDATO`

Mesmo princípio.

---

# 94. Classe Média

**ID:** `SEO-007`  
**Status:** `PESQUISAR`

“Classe média” possui múltiplas definições.

Não criar uma classificação arbitrária.

---

# 95. Conteúdo Automático Em Escala

**ID:** `SEO-008`  
**Status:** `ADIADO`

Não produzir automaticamente centenas de páginas alterando apenas valores.

Conteúdo deve possuir valor editorial próprio.

---

# PARTE XVI — FUNCIONALIDADES DE CONTA

# 96. Conta Do Usuário

**ID:** `ACCOUNT-001`  
**Status:** `ADIADO`

Não necessária na V1.

Só considerar se existir benefício real em:

- histórico;
- acompanhamento;
- metas;
- sincronização.

---

# 97. Histórico De Cálculos

**ID:** `ACCOUNT-002`  
**Status:** `ADIADO`

Depende de:

`ACCOUNT-001`

e revisão de privacidade.

---

# 98. Metas Financeiras

**ID:** `ACCOUNT-003`  
**Status:** `IDEIA`

Exemplo:

> reserva de emergência;

> entrada do imóvel;

> viagem;

> aposentadoria.

Pode existir futuramente sem necessariamente virar gestão patrimonial completa.

---

# PARTE XVII — IA

# 99. Orientação Por IA

**ID:** `AI-001`  
**Status:** `PESQUISAR`

Possibilidade:

> explicar o diagnóstico em linguagem natural.

Exemplo:

> “Seu principal ponto de atenção parece ser o custo da dívida.”

---

# 100. Limite Da IA

A IA não deve decidir sozinha:

- qual produto comprar;
- qual ativo vender;
- qual empréstimo contratar;
- qual instituição escolher.

O motor de prioridades deve ter regras documentadas.

A IA pode explicar as regras.

---

# 101. IA E Privacidade

Qualquer uso futuro deve respeitar:

`06-privacidade-seguranca.md`

Não enviar toda a vida financeira do usuário para serviços externos sem necessidade e transparência.

---

# PARTE XVIII — IDEIAS FORA DO NÚCLEO

# 102. Calculadoras Técnicas De Construção

Exemplos:

- litros de tinta;
- dimensionamento elétrico;
- BTU;
- volume de piscina;
- concreto;
- telhas.

**Status:** `REJEITADO COMO NÚCLEO`

Motivo:

> são ferramentas úteis, mas não pertencem diretamente à missão financeira familiar do Renda Comparada.

---

# 103. Conversores Genéricos

Exemplos:

- metros para pés;
- Celsius para Fahrenheit;
- cronômetros;
- calculadoras matemáticas genéricas.

**Status:** `REJEITADO`

Motivo:

> transformariam o projeto em um portal genérico de ferramentas.

---

# 104. Portal Genérico Estilo AllTools

**ID:** `CORE-001`  
**Status:** `REJEITADO`

O Renda Comparada não deve evoluir para:

> “qualquer calculadora que possa gerar tráfego.”

A tese é:

> **compreensão financeira da família.**

---

# 105. Recomendação De Produtos Financeiros Específicos

Exemplos:

> “Compre CDB do banco X.”

> “Invista no fundo Y.”

> “Contrate empréstimo Z.”

**Status:** `REJEITADO COMO DIREÇÃO ATUAL`

O produto fornece:

- educação;
- contexto;
- simulação;
- orientação geral.

---

# 106. Marketplace Financeiro

**ID:** `CORE-002`  
**Status:** `REJEITADO COMO DIREÇÃO ATUAL`

Não transformar automaticamente o produto em:

- marketplace de crédito;
- comparador com venda de leads;
- distribuidor de investimentos.

Qualquer mudança desse princípio exigiria nova decisão estratégica.

---

# PARTE XIX — DEPENDÊNCIAS IMPORTANTES

# 107. Dependência — PNAD

Afeta:

- percentis;
- Top X%;
- slider;
- estados;
- histórico.

Sem metodologia brasileira validada:

> não promover essas funcionalidades.

---

# 108. Dependência — PIP

Afeta:

- mundo;
- comparações internacionais;
- histórico global.

---

# 109. Dependência — POF

Afeta:

- famílias semelhantes;
- padrão de gasto;
- benchmarks familiares.

---

# 110. Dependência — Banco Central

Afeta:

- taxas;
- crédito;
- dívida;
- Registrato;
- simuladores contextuais.

---

# 111. Dependência — Modelo De Saúde Financeira

Afeta:

- check-up;
- diagnóstico;
- prioridades;
- recomendações;
- cursos.

Esse é um dos maiores blocos metodológicos ainda não construídos.

---

# PARTE XX — ORDEM RECOMENDADA

# 112. Fase A — Terminar Muito Bem a V1

Antes de expandir:

- metodologia;
- compartilhamento;
- mobile;
- confiança;
- privacidade;
- analytics;
- SEO básico.

---

# 113. Fase B — Explorar a Pergunta De Renda

Candidatos:

1. Top X%;
2. simulador de renda;
3. conteúdos de alta intenção;
4. pequenos refinamentos de compartilhamento.

Baixa mudança conceitual.

Alto alinhamento com o núcleo atual.

---

# 114. Fase C — Check-up

Construir:

1. perguntas;
2. dimensões;
3. critérios;
4. prioridades;
5. linguagem;
6. testes.

Só depois implementar a interface.

---

# 115. Fase D — Orientação

Adicionar:

- ferramentas oficiais;
- cursos;
- trilhas;
- simuladores relacionados ao problema detectado.

---

# 116. Fase E — Realidade Da Família

Adicionar progressivamente:

- POF;
- moradia;
- carro;
- contas;
- saúde;
- educação.

---

# 117. Fase F — Decisões Complexas

Somente depois considerar:

- comprar × alugar;
- amortizar × investir;
- elétrico × combustão;
- patrimônio;
- IA;
- histórico persistente.

---

# PARTE XXI — MATRIZ DE PRIORIDADE ATUAL

# 118. Alta Prioridade Após a V1

|ID|Funcionalidade|Status|
|---|---|---|
|INC-001|Quanto preciso ganhar para Top X%|CANDIDATO|
|INC-002|E se minha renda fosse diferente?|CANDIDATO|
|FIN-001|Check-up financeiro|VALIDADO-CONCEITUALMENTE|
|GUIDE-001|Próximo passo recomendado|VALIDADO-CONCEITUALMENTE|
|EDU-001|Cursos oficiais contextuais|CANDIDATO|
|FAM-003|Reserva familiar|CANDIDATO|

---

# 119. Prioridade Intermediária

|ID|Funcionalidade|Status|
|---|---|---|
|BC-001|Registrato|CANDIDATO|
|BC-003|Valores a Receber|CANDIDATO|
|BC-004|Calculadora do Cidadão|CANDIDATO|
|SIM-001|Juros compostos|CANDIDATO|
|SIM-003|Dívida|CANDIDATO|
|SIM-004|Cartão|CANDIDATO|
|SIM-006|Financiamento|CANDIDATO|
|SIM-009|Correção monetária|CANDIDATO|
|CAR-001|Custo real do carro|VALIDADO-CONCEITUALMENTE|
|HOME-001|Custo real da moradia|VALIDADO-CONCEITUALMENTE|

---

# 120. Dependentes De pesquisa/dados

|ID|Funcionalidade|Status|
|---|---|---|
|POF-001|Famílias semelhantes|BLOQUEADO/PESQUISAR|
|REG-001|Percentil estadual|PESQUISAR|
|REG-002|Percentil municipal|BLOQUEADO|
|REG-003|Custo de vida regional|PESQUISAR|
|HIST-001|Histórico|PESQUISAR|
|CAR-004|Elétrico × combustão|PESQUISAR|
|HOME-002|Comprar × alugar|PESQUISAR|
|HOME-003|Amortizar × investir|PESQUISAR|
|WEALTH-001|Patrimônio líquido|PESQUISAR|

---

# PARTE XXII — COMO USAR ESTE DOCUMENTO

# 121. Ao Surgir Uma Nova Ideia

Adicionar:

```text
ID:
Nome:
Problema:
Hipótese:
Status:
Dependências:
Riscos:
Métrica:
Observações:
```

---

# 122. Modelo De Novo Item

```markdown
## [ID] Nome da funcionalidade

**Status:** `IDEIA`

### Problema

Que problema isso resolve?

### Hipótese

Por que acreditamos que ajudará?

### Experiência

Como funcionaria aproximadamente?

### Dependências

Quais dados, APIs ou funcionalidades são necessárias?

### Riscos

Quais erros ou problemas pode gerar?

### Métrica

Como saberemos se funciona?
```

---

# 123. Ao Promover Para Desenvolvimento

Passos:

```text
BACKLOG
↓
PESQUISA
↓
DECISÃO
↓
PRD DA VERSÃO
↓
UX
↓
TESTES
↓
IMPLEMENTAÇÃO
```

Não pular diretamente:

```text
IDEIA
↓
CODEX
```

---

# 124. Quando Remover Do Backlog

Um item pode ser removido ou arquivado quando:

- já foi entregue;
- deixou de fazer sentido;
- outra solução resolveu o problema;
- dados necessários deixaram de existir;
- contradiz a visão atual.

---

# 125. Registro De Rejeições

Não apagar simplesmente ideias rejeitadas que provavelmente reaparecerão.

Registrar:

> **REJEITADO — motivo**

Isso evita discutir repetidamente a mesma decisão.

---

# 126. Regra Para O Codex

Ao ler este documento, o Codex deve interpretar:

```text
IDEIA
PESQUISAR
VALIDADO-CONCEITUALMENTE
CANDIDATO
BLOQUEADO
ADIADO
REJEITADO
```

como:

> **não implementar sem instrução explícita.**

Somente:

```text
PLANEJADO
```

e incluído no PRD ativo

pode ser considerado parte do escopo.

---

# 127. Não Implementar Por Proximidade

Se o Codex estiver criando:

> simulador de juros compostos

não deve automaticamente adicionar:

- Tesouro Direto;
- CDB;
- aposentadoria;
- inflação;
- comparador de bancos;

porque “faz sentido”.

Cada funcionalidade possui escopo próprio.

---

# 128. Não Implementar Placeholders Futuros

A interface da V1 não precisa mostrar:

```text
Carro — em breve
Casa — em breve
Investimentos — em breve
Energia — em breve
```

apenas porque essas ideias existem.

O backlog é interno.

Não é menu de produto.

---

# 129. Roadmap Público

Se futuramente houver roadmap público:

> criar versão separada e deliberada.

Não publicar este documento interno automaticamente.

---

# 130. Métricas Antes Da Priorização

Após V1, decisões devem usar dados como:

- taxa de cálculo;
- taxa de compartilhamento;
- recalculações;
- buscas orgânicas;
- interesse no check-up;
- perguntas de usuários;
- abandono.

O backlog deve reagir a evidências reais.

---

# 131. Não Priorizar Apenas SEO

Uma ferramenta pode ter grande volume de busca e ainda assim não pertencer ao produto.

Critério:

```text
demanda
+
alinhamento
+
utilidade
+
dados
+
confiança
```

e não:

```text
volume de busca
```

sozinho.

---

# 132. Não Priorizar Apenas Facilidade

Uma funcionalidade não deve entrar porque:

> “é fácil para o Codex construir.”

Facilidade técnica não substitui valor para o usuário.

---

# 133. Não Priorizar Apenas Novidade

Evitar adicionar:

- IA;
- chat;
- dashboard;
- blockchain;
- gamificação;

somente porque são tecnologias ou tendências interessantes.

---

# 134. Norte Do Roadmap

A evolução desejada é:

```text
Onde estou?
↓
Como estou?
↓
Onde está indo meu dinheiro?
↓
O que merece atenção?
↓
O que posso fazer?
↓
Qual ferramenta pode me ajudar?
```

Cada nova etapa deve aprofundar a anterior.

---

# 135. Norte Do Backlog

O backlog existe para proteger duas coisas ao mesmo tempo:

> **a criatividade do projeto**

e

> **o foco do produto.**

Podemos continuar tendo muitas ideias.

Mas o produto só cresce quando existe razão para transformar uma delas em funcionalidade.

---

# 136. Regra Final

> # Ideia não é requisito.

> # Backlog não é PRD.

> # Futuro não é V1.

> # E o Codex não decide sozinho o que entra no produto.

O roadmap deve permitir que o Renda Comparada cresça sem perder sua pergunta central:

> **Onde estou financeiramente — e o que posso fazer para melhorar?**