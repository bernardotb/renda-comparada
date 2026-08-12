---
title: 04-metodologia-de-dados
created: 2026-08-12T17:07:15.000-03:00
modified: 2026-08-12T17:21:49.296-03:00
---

# 04-metodologia-de-dados

**Produto:** Renda Comparada  
**Versão do documento:** 1.0  
**Status:** Canônico — sujeito a validação estatística antes da produção  
**Última revisão:** 12/08/2026

**Documentos relacionados:**

- `01-visao-produto.md`
- `02-prd-v1.md`
- `03-jornada-ux-v1.md`
- `06-privacidade-seguranca.md`
- `09-fontes-referencias.md`
- `10-testes-validacao.md`

---

# 1. Autoridade Deste Documento

Este documento é a **fonte de autoridade do projeto para dados, fórmulas e metodologia estatística**.

Em caso de conflito entre este documento e qualquer outro documento do projeto, este documento prevalece para questões relacionadas a:

- definição de renda;
- composição do domicílio;
- número de moradores;
- renda domiciliar per capita;
- fontes estatísticas;
- pesos amostrais;
- percentis;
- distribuição de renda;
- inflação;
- PPP/PPC;
- comparação internacional;
- interpolação;
- arredondamento;
- versionamento dos datasets;
- atualização dos dados;
- limitações metodológicas.

O Codex **não deve alterar fórmulas, fontes ou tratamentos estatísticos por iniciativa própria**.

Quando alguma regra não estiver definida neste documento:

> **não adivinhar.**

Registrar a lacuna e solicitar decisão metodológica.

---

# 2. Objetivo Metodológico

O objetivo da calculadora principal é transformar:

1. renda mensal total do domicílio;
2. número total de moradores;

em duas estimativas:

### Brasil

> posição da renda domiciliar per capita do usuário dentro da distribuição brasileira.

### Mundo

> posição aproximada do poder econômico per capita do usuário dentro da distribuição monetária global utilizada pelo Banco Mundial.

Os dois resultados possuem metodologias diferentes e **não devem ser apresentados como estatisticamente idênticos**.

---

# 3. Princípios Permanentes

Toda implementação deve respeitar os seguintes princípios:

1. **Renda não é patrimônio.**
2. **Média não é percentil.**
3. **Percentil deve derivar de uma distribuição.**
4. **A amostra da PNAD deve respeitar seus pesos estatísticos.**
5. **Não tratar cada registro da PNAD como uma pessoa de peso igual.**
6. **Não utilizar médias estaduais para inferir percentis estaduais.**
7. **Não utilizar câmbio comercial para comparação internacional de padrão material de vida.**
8. **Não apresentar precisão maior que a suportada pelos dados.**
9. **Não atualizar resultados silenciosamente quando a fonte muda.**
10. **Toda versão em produção deve ser reproduzível.**
11. **Toda fonte utilizada deve possuir versão/data registrada.**
12. **Toda alteração metodológica deve gerar testes de regressão.**

---

# 4. Fontes Principais

A arquitetura metodológica atual utiliza:

|Finalidade|Fonte principal|
|---|---|
|Distribuição brasileira|IBGE — PNAD Contínua|
|Rendimento domiciliar|IBGE — PNAD Contínua|
|Inflação brasileira|IBGE — IPCA|
|Distribuição internacional|World Bank — Poverty and Inequality Platform|
|Paridade de poder de compra|World Bank — ICP / WDI PPP|
|Futuro orçamento familiar|IBGE — POF|
|Futuro crédito e juros|Banco Central do Brasil|

Fontes secundárias podem ser utilizadas para:

- conferência;
- interpretação;
- pesquisa;
- documentação.

Mas não devem substituir a fonte primária sem justificativa metodológica.

---

# PARTE I — BRASIL

# 5. Fonte Brasileira Vigente

A base brasileira inicial da V1 deve utilizar:

> **Pesquisa Nacional por Amostra de Domicílios Contínua — PNAD Contínua — Rendimento de Todas as Fontes 2025**

Os microdados correspondentes ao tema **Rendimento de Todas as Fontes 2025** foram atualizados pelo IBGE em 08/05/2026.

A versão exata dos arquivos utilizados deverá ser registrada no manifesto do dataset produzido pelo projeto.

---

# 6. Por Que Utilizar Microdados

A média nacional divulgada pelo IBGE não é suficiente para responder:

> **“Minha renda é maior que a de quantos brasileiros?”**

Por exemplo, o IBGE divulgou para 2025 rendimento nominal mensal domiciliar per capita médio de:

> **R$ 2.316**

Esse valor representa uma **média**, não um percentil, mediana ou corte de classe.

Portanto:

> **R$ 2.316 não pode ser utilizado diretamente para calcular a posição do usuário.**

Precisamos da **distribuição completa** ou de uma representação estatisticamente equivalente dela.

---

# 7. Conceito Brasileiro De Renda

O conceito central adotado é o:

> **rendimento domiciliar per capita**

O IBGE define esse indicador como a razão entre:

> **total dos rendimentos domiciliares**

e

> **total dos moradores.**

São considerados rendimentos de trabalho e de outras fontes.

Para a divulgação de 2025, o IBGE informa que utiliza rendimentos brutos de trabalho e outras fontes efetivamente recebidos no mês de referência.

---

# 8. Renda Informada Pelo Usuário

A interface deve solicitar:

> **Qual é a renda mensal total da sua casa?**

O conceito apresentado ao usuário deve ser compatível com o conceito estatístico utilizado.

Em princípio, incluir:

- salários;
- rendimentos de trabalho autônomo;
- aposentadorias;
- pensões;
- aluguéis recebidos;
- benefícios e transferências consideradas pela metodologia;
- rendimentos de outras fontes incluídos pela PNAD;
- demais rendimentos abrangidos pela variável oficial selecionada.

A descrição definitiva deve ser derivada do dicionário e das notas técnicas da PNAD utilizada.

---

# 9. Renda Bruta

Para manter compatibilidade com o conceito atualmente adotado pelo IBGE para o rendimento domiciliar per capita divulgado oficialmente, a entrada inicial da V1 deve ser orientada para:

> **renda bruta mensal do domicílio**

e não renda líquida após:

- imposto de renda;
- plano de saúde;
- empréstimos;
- financiamento;
- cartão;
- aluguel;
- despesas pessoais.

A interface deve explicar esse conceito de maneira simples.

---

# 10. Moradores

A pergunta deve ser:

> **Quantas pessoas moram nesta casa?**

Devem ser consideradas **todas as pessoas que compõem o domicílio segundo a metodologia adotada**, inclusive:

- adultos;
- crianças;
- pessoas sem renda.

O IBGE informa explicitamente que todos os moradores entram no cálculo do rendimento domiciliar per capita.

Portanto:

> **não utilizar somente o número de adultos.**

---

# 11. Fórmula Básica Do Usuário

Definir:

`R_familiar`

como renda mensal total do domicílio.

Definir:

`N_moradores`

como número total de moradores.

Então:

```text
RDPC_usuario = R_familiar / N_moradores
```

Onde:

`RDPC_usuario`

significa:

> **renda domiciliar per capita do usuário.**

---

# 12. Exemplo

Família:

- renda mensal: R$ 6.500;
- moradores: 3.

Então:

```text
RDPC_usuario = 6500 / 3
RDPC_usuario = 2166,666…
```

Valor aproximado:

> **R$ 2.166,67 por pessoa/mês.**

Esse valor será comparado com a distribuição brasileira preparada para produção.

---

# 13. Unidade Estatística Brasileira

A distribuição deve responder à pergunta:

> **Qual proporção da população brasileira possui rendimento domiciliar per capita inferior ao do usuário?**

Isso significa que a unidade final de interpretação é a **pessoa**, posicionada segundo o rendimento domiciliar per capita do domicílio no qual reside.

Não é uma distribuição simples de domicílios.

Não é uma distribuição de salários individuais.

Não é uma distribuição de responsáveis pelo domicílio.

---

# 14. Estrutura Da Distribuição

Cada pessoa da amostra recebe o rendimento domiciliar per capita correspondente ao seu domicílio.

Exemplo conceitual:

Domicílio A:

- renda: R$ 10.000;
- quatro moradores;
- RDPC: R$ 2.500.

Na distribuição por pessoas, os quatro moradores pertencem à faixa de:

> **R$ 2.500 per capita**

respeitando os pesos estatísticos aplicáveis.

---

# 15. Pesos Amostrais

A PNAD Contínua é uma pesquisa amostral.

Portanto:

> **os registros não podem receber peso 1.**

Deve ser utilizado o fator de expansão/peso final correspondente à edição anual e visita selecionada.

O código exato da variável de peso deve ser confirmado no:

> **dicionário oficial dos microdados da PNAD Contínua 2025**

antes da implementação definitiva.

O identificador da variável deve então ser registrado neste documento e no manifesto do dataset.

### Regra

Enquanto o código oficial do peso não tiver sido confirmado:

> **Codex não deve escolher uma variável por semelhança de nome ou memória.**

---

# 16. Variável De Rendimento

A variável oficial utilizada para representar o rendimento domiciliar per capita também deve ser confirmada no dicionário oficial da versão 2025.

Preferência metodológica:

> utilizar a variável derivada oficial do IBGE correspondente ao conceito desejado, quando disponível e adequada.

Evitar reconstruir manualmente dezenas de componentes de renda caso o IBGE já disponibilize uma variável derivada validada.

---

# 17. Registro Obrigatório Das Variáveis

Antes de gerar o primeiro dataset de produção, preencher:

```text
IBGE_YEAR = 2025
IBGE_VISIT = [CONFIRMAR]
IBGE_RDPC_VARIABLE = [CONFIRMAR NO DICIONÁRIO]
IBGE_WEIGHT_VARIABLE = [CONFIRMAR NO DICIONÁRIO]
IBGE_UF_VARIABLE = [CONFIRMAR]
IBGE_DEFLATOR_SOURCE = [CONFIRMAR]
```

Nenhum `[CONFIRMAR]` pode permanecer antes do deploy de produção.

---

# 18. Visita Da PNAD

Para o rendimento domiciliar per capita oficial de 2025, o IBGE voltou a utilizar informações das **primeiras visitas** realizadas ao longo dos quatro trimestres do ano.

A base utilizada pelo Renda Comparada deverá ser compatível com essa escolha.

A visita efetivamente usada no pipeline deve constar no manifesto.

---

# 19. Reponderação De 2025

A PNAD passou por atualização de estimativas populacionais e reponderação da série com base nas novas projeções associadas ao Censo 2022.

O IBGE publicou em 2025 nota técnica específica sobre atualização das estimativas populacionais para cálculo dos pesos.

Consequência:

> **não reutilizar pesos antigos ou datasets baixados anteriormente sem verificar se continuam sendo a versão oficial vigente.**

---

# 20. Construção Da CDF Brasileira

A distribuição acumulada deve ser construída com os registros ponderados.

Ordenar as observações por:

```text
RDPC
```

e acumular seus pesos.

Definir:

```text
W_total = soma de todos os pesos válidos
```

Para renda `x`, definir:

```text
W_abaixo(x) = soma dos pesos das pessoas com RDPC < x
```

Então:

```text
share_below(x) = W_abaixo(x) / W_total
```

---

# 21. Pergunta Principal E Desigualdade Estrita

O slogan pergunta:

> **“Você é mais rico do que quantos brasileiros?”**

Como a comparação real é de renda, a interpretação estatística deve aproximar:

> **“Sua renda por pessoa é maior que a de aproximadamente X% da população considerada.”**

Por isso, para essa frase, utilizar preferencialmente:

```text
RDPC < RDPC_usuario
```

e não:

```text
RDPC <= RDPC_usuario
```

A diferença é relevante quando muitas observações possuem exatamente o mesmo valor.

---

# 22. Empates

Rendimentos possuem muitos valores repetidos.

Por isso, o sistema deve distinguir:

```text
share_below
```

proporção estritamente abaixo;

e, se necessário:

```text
share_at_or_below
```

proporção abaixo ou igual.

A interface não deve fingir uma ordenação individual exata entre pessoas que possuem o mesmo rendimento.

---

# 23. Percentil Brasileiro

O percentil exibido deverá ser derivado da CDF ponderada.

Definição recomendada para a linguagem principal:

```text
percentil_aprox = 100 × share_below
```

Exemplo:

```text
share_below = 0,679
percentil_aprox = 67,9
```

Interpretação:

> **Sua renda por pessoa é maior que a de aproximadamente 67,9% da população considerada.**

---

# 24. TOP Percentual

Uma leitura complementar poderá ser:

```text
top_aprox = 100 - percentil_aprox
```

Exemplo:

```text
percentil_aprox = 67,9
top_aprox = 32,1
```

Interface:

> **Você está aproximadamente entre os 32% de maior renda.**

Por causa de empates, essa representação deve ser tratada como aproximação.

---

# 25. Casas Decimais

Não mostrar precisão excessiva.

A recomendação inicial é:

### Resultado Principal

> **68%**

ou

> **67,9%**

A escolha final será validada em UX e testes.

Evitar:

> **67,934728%**

porque os dados não justificam esse nível de precisão perceptiva.

---

# 26. Distribuição Empírica versus Interpolação

Se o dataset de produção conseguir armazenar a distribuição empírica comprimida:

> utilizar busca monotônica diretamente na CDF.

Não interpolar apenas para produzir uma falsa sensação de precisão.

Caso seja necessária interpolação por motivo de tamanho/performance:

- utilizar método monotônico;
- documentar o método;
- testar erro máximo;
- comparar com resultados calculados diretamente dos microdados.

---

# 27. Preços E Inflação

Existe uma diferença temporal importante:

> o usuário poderá informar sua renda em 2026 enquanto a distribuição mais recente disponível pertence a 2025.

Não devemos comparar silenciosamente:

> **R$ 10.000 de agosto de 2026**

com

> **R$ 10.000 em preços de 2025**

como se possuíssem o mesmo poder de compra.

---

# 28. Referência De Preços

O pipeline deverá escolher uma referência monetária explícita.

Abordagem preferencial:

1. construir a distribuição da PNAD em preços comparáveis;
2. utilizar os deflatores oficiais correspondentes;
3. converter a renda atual do usuário para a mesma referência de preços;

ou, matematicamente equivalente:

1. atualizar os cortes da distribuição para preços atuais.

A opção escolhida deve ser documentada e produzir resultados reproduzíveis.

---

# 29. Fonte De Inflação

Para atualizações monetárias brasileiras, utilizar preferencialmente:

> **IPCA — IBGE**

quando metodologicamente compatível.

Não utilizar:

- inflação informal;
- estimativas de blogs;
- variação do salário mínimo;
- CDI;
- Selic;

como substitutos de inflação.

---

# 30. Regra Operacional Recomendada

A aplicação não precisa baixar IPCA em cada cálculo.

O pipeline periódico deverá manter:

```text
PRICE_REFERENCE_DATE
INFLATION_FACTOR
```

dentro do dataset/metadados de produção.

O cálculo do usuário utiliza o fator já validado.

---

# 31. Validação Obrigatória — Brasil

O pipeline brasileiro deve ser validado contra resultados oficiais publicados pelo IBGE.

Um teste obrigatório é reconstruir, a partir da base e pesos escolhidos, estatísticas oficiais conhecidas.

Por exemplo:

> rendimento domiciliar per capita médio nacional de 2025 divulgado oficialmente como R$ 2.316 no indicador nominal correspondente.

Diferenças relevantes indicam problema em:

- visita;
- variável;
- pesos;
- filtros;
- deflator;
- unidade estatística.

---

# 32. Não Usar O Valor De R$ 2.316 Como Distribuição

A validação contra a média oficial serve para verificar o pipeline.

Ela **não significa** que a média será usada para calcular percentis.

A sequência correta é:

```text
microdados + pesos
↓
distribuição
↓
CDF
↓
percentil
```

e não:

```text
renda do usuário / média nacional
↓
percentil
```

Esse segundo método é proibido.

---

# PARTE II — MUNDO

# 33. Fonte Internacional

A fonte principal será:

> **World Bank — Poverty and Inequality Platform — PIP**

O PIP reúne estimativas de pobreza, desigualdade e prosperidade compartilhada para mais de 170 economias e utiliza dados de pesquisas domiciliares, incluindo microdados ou dados agrupados.

---

# 34. Versão Internacional Atualmente Pesquisada

Na data desta revisão, o PIP informa como versão disponível baseada em PPPs de 2021:

```text
20260324_2021
```

O site de produção do PIP também apresenta identificadores completos de build relacionados a essa versão.

O Renda Comparada deve congelar a versão utilizada.

Nunca consultar simplesmente:

> **latest**

em produção sem registrar qual versão foi recebida.

---

# 35. Unidade Do PIP

O PIP trabalha com valores de:

> **consumo ou renda per capita**

expressos em:

> **dólares internacionais de PPP de 2021 por pessoa por dia.**

O próprio Banco Mundial esclarece que alguns países utilizam consumo e outros utilizam renda como agregado de bem-estar.

Esse ponto é metodologicamente essencial.

---

# 36. Consequência Para a Linguagem

O resultado mundial **não deve ser descrito como uma distribuição mundial perfeitamente homogênea de salários ou renda bruta familiar**.

A formulação deve ser mais cautelosa.

Exemplo:

> **Sua posição aproximada na comparação mundial**

e:

> **A comparação global utiliza dados de renda ou consumo domiciliar por pessoa, conforme a metodologia disponível para cada país.**

---

# 37. Por Que Isso Ainda É Útil

Apesar da heterogeneidade entre renda e consumo, o PIP foi construído especificamente para permitir comparações internacionais de bem-estar monetário e pobreza.

Portanto, continua sendo uma fonte adequada para:

> **uma estimativa mundial de posição econômica relativa**

desde que as limitações sejam transparentes.

---

# 38. PPP/PPC

Não utilizar câmbio comercial BRL/USD.

A comparação internacional deve utilizar:

> **Purchasing Power Parity — PPP**

ou:

> **Paridade do Poder de Compra — PPC.**

Isso busca ajustar diferenças de nível de preços entre países.

---

# 39. PPP De Consumo Das Famílias

Para uma renda familiar, a série conceitualmente mais adequada é a PPP ligada ao consumo das famílias.

Indicador do World Bank WDI:

```text
PA.NUS.PRVT.PP
```

Descrição:

> PPP conversion factor, households and NPISHs final consumption expenditure.

Unidade:

> moeda local por dólar internacional.

O Banco Mundial informa que os valores mais recentes são extrapolados a partir dos benchmarks do ICP utilizando índices de preços.

---

# 40. Não Usar PPP Do PIB Automaticamente

Existe também:

```text
PA.NUS.PPP
```

para PIB.

Não substituir automaticamente a PPP de consumo privado pela PPP do PIB.

A escolha deve refletir o conceito que estamos tentando comparar:

> **bem-estar econômico do domicílio.**

---

# 41. Conversão Internacional — Estrutura

Primeiro calcular:

```text
RDPC_usuario_BRL
```

Depois convertê-lo para a unidade monetária compatível com a versão do PIP utilizada.

Estrutura conceitual:

```text
BRL por pessoa/mês
↓
ajuste temporal/preços
↓
PPP de consumo
↓
dólares internacionais 2021 por pessoa
↓
valor diário
↓
distribuição global PIP
```

---

# 42. Conversão Mensal Para Diária

Como o PIP utiliza unidade por dia, definir explicitamente a conversão.

Abordagem recomendada:

```text
valor_anual = valor_mensal × 12
```

Depois:

```text
valor_diario = valor_anual / 365
```

Portanto:

```text
valor_diario = valor_mensal × 12 / 365
```

Não misturar arbitrariamente:

- 30 dias;
- 30,4 dias;
- 365 dias;

em diferentes pontos do código.

A constante utilizada deve ser única e testada.

---

# 43. Conversão PPP — Regra Final Deve Ser Validada

O pipeline deve determinar, com base na versão do PIP e na série PPP selecionada, a conversão exata entre:

```text
BRL no período do usuário
```

e

```text
2021 PPP international dollars
```

Essa conversão deverá ser validada numericamente contra dados oficiais do Banco Mundial.

O Codex não deve criar essa transformação por tentativa ou aproximação.

---

# 44. Método Recomendado Para O Percentil Mundial

O PIP permite calcular indicadores para países, regiões ou agregados em diferentes linhas monetárias.

A API oficial possui endpoints para:

- estatísticas;
- agregações;
- curvas de Lorenz;
- dados agrupados;
- versões;
- anos válidos.

A abordagem recomendada para a V1 é construir **offline** uma função acumulada global a partir do PIP.

---

# 45. Interpretação Como Linha Monetária

Para um valor do usuário:

```text
x = renda/consumo equivalente em 2021 PPP $ por pessoa/dia
```

podemos interpretar:

> qual proporção da população mundial está abaixo de `x`.

Essa proporção corresponde conceitualmente à posição acumulada do usuário.

---

# 46. CDF Global

Definir:

```text
GlobalCDF(x)
```

como proporção da população mundial abaixo do nível de bem-estar monetário `x`.

Então:

```text
percentil_global = 100 × GlobalCDF(x)
```

E:

```text
top_global = 100 - percentil_global
```

---

# 47. Não Consultar PIP Em Cada Cálculo

Não executar:

```text
usuário calcula
↓
API World Bank
↓
espera resposta
↓
resultado
```

A aplicação deve utilizar dataset preparado previamente.

---

# 48. Construção Offline Mundial

Pipeline desejado:

```text
PIP
↓
versão fixa
↓
ano de referência
↓
CDF mundial
↓
validação
↓
lookup table versionada
↓
aplicação
```

A aplicação deve responder localmente ou através da infraestrutura própria do projeto.

---

# 49. Ano Mundial De Referência

O ano mundial não deve ser escolhido automaticamente apenas porque é o maior ano retornado pela API.

Precisamos distinguir:

- observação de pesquisa;
- interpolação;
- extrapolação;
- nowcast.

O PIP informa explicitamente quando dados são interpolados e possui nowcasts para anos recentes.

---

# 50. Decisão Inicial Recomendada

Para a V1, utilizar:

> **o ano global mais recente que tenha sido explicitamente aprovado e congelado pelo projeto.**

O manifesto deve possuir:

```text
GLOBAL_REFERENCE_YEAR = [DEFINIR]
GLOBAL_ESTIMATION_TYPE = [DEFINIR]
PIP_VERSION = 20260324_2021
```

Não deixar o ano variar automaticamente.

---

# 51. Opção 2025

Como Brasil utiliza 2025, existe uma vantagem comunicacional em utilizar uma estimativa mundial referente também a 2025.

Porém:

> dados globais de 2025 podem envolver interpolação/nowcast.

Se essa opção for adotada, a interface deverá informar:

> **Estimativa mundial 2025 — Banco Mundial PIP**

e não sugerir que todos os países realizaram pesquisas domiciliares em 2025.

---

# 52. Cobertura Mundial

O PIP não representa uma pesquisa única realizada simultaneamente em todos os países.

Ele harmoniza:

- pesquisas de países diferentes;
- anos diferentes;
- renda ou consumo;
- interpolação;
- PPP;
- populações.

Por isso:

> **o resultado mundial é intrinsecamente mais aproximado que o resultado brasileiro baseado diretamente na PNAD.**

---

# 53. Não Misturar WID E PIP

O projeto pesquisou metodologias do World Inequality Database durante o desenvolvimento conceitual.

Entretanto, a V1 decidiu estruturar o lado mundial em:

> **World Bank PIP**

e não no WID.

Não misturar:

- unidade adulta do WID;
- metodologia do WID;
- distribuição PIP;
- PPP do Banco Mundial;

dentro do mesmo cálculo.

Se futuramente o WID for adotado, deverá existir uma nova versão metodológica.

---

# PARTE III — DATASET DE PRODUÇÃO

# 54. Dataset Derivado

A aplicação não deverá carregar microdados brutos.

O pipeline gerará datasets derivados pequenos e auditáveis.

Exemplo:

```text
/data
  /brasil
    distribution-2025.json
    metadata.json

  /world
    distribution-2025-pip-20260324_2021.json
    metadata.json
```

A estrutura definitiva poderá mudar, preservando os princípios deste documento.

---

# 55. Manifesto Obrigatório

Todo dataset deve possuir metadados.

Exemplo:

```json
{
  "dataset": "brazil-income-distribution",
  "source": "IBGE PNAD Contínua",
  "source_year": 2025,
  "source_release": "Rendimento de Todas as Fontes",
  "downloaded_at": "YYYY-MM-DD",
  "processed_at": "YYYY-MM-DD",
  "price_reference": "YYYY-MM",
  "methodology_version": "1.0.0",
  "weight_variable": "…",
  "income_variable": "…",
  "checksum": "…"
}
```

---

# 56. Manifesto Mundial

Exemplo:

```json
{
  "dataset": "global-welfare-distribution",
  "source": "World Bank PIP",
  "pip_version": "20260324_2021",
  "reference_year": 2025,
  "ppp_basis": 2021,
  "ppp_indicator": "PA.NUS.PRVT.PP",
  "processed_at": "YYYY-MM-DD",
  "methodology_version": "1.0.0",
  "checksum": "…"
}
```

---

# 57. Versionamento Metodológico

Utilizar versão semântica interna:

```text
methodology_version = MAJOR.MINOR.PATCH
```

### MAJOR

Mudança que pode alterar significativamente resultados.

Exemplos:

- trocar PNAD por outra fonte;
- trocar PIP por WID;
- mudar conceito de renda;
- mudar unidade estatística.

### MINOR

Melhoria metodológica compatível.

### PATCH

Correção de bug sem mudança conceitual.

---

# 58. Atualização Automática

O projeto poderá verificar automaticamente se existem novas versões das fontes.

Mas:

> **detecção automática não significa publicação automática.**

Fluxo:

```text
detectar
↓
baixar
↓
processar
↓
validar
↓
comparar com produção
↓
aprovar
↓
publicar
```

---

# 59. Comparação Entre Versões

Antes de promover novo dataset:

calcular diferenças em:

- percentil 10;
- percentil 25;
- mediana;
- percentil 75;
- percentil 90;
- percentil 95;
- percentil 99;
- valores de teste definidos.

Se houver alterações inesperadas:

> bloquear atualização.

---

# 60. Checksums

Arquivos de origem e datasets derivados devem possuir hashes.

Objetivo:

- detectar alterações;
- permitir reprodução;
- identificar arquivos substituídos pelas fontes;
- evitar mudanças silenciosas.

---

# 61. Fonte versus Transformação

O repositório deve distinguir:

### Raw

arquivo oficial baixado.

### Processed

arquivo intermediário normalizado.

### Production

lookup utilizado pela aplicação.

Nunca editar manualmente dados de produção sem regenerá-los pelo pipeline.

---

# 62. Reprodutibilidade

Dado:

- versão do código;
- arquivos raw;
- manifesto;
- configuração;

deve ser possível reconstruir exatamente o dataset de produção.

---

# PARTE IV — VALIDAÇÃO

# 63. Testes Brasileiros Obrigatórios

O pipeline deverá verificar:

- soma dos pesos;
- ausência de pesos negativos;
- RDPC não negativo quando aplicável;
- distribuição ordenada;
- CDF monotônica;
- CDF final próxima de 1;
- média ponderada;
- mediana;
- percentis selecionados;
- reprodução de indicadores oficiais.

---

# 64. Casos De Teste Da Aplicação

Exemplos obrigatórios:

### Caso A

```text
renda = 6500
moradores = 3
```

Verificar:

```text
RDPC = 2166,666…
```

O percentil esperado será preenchido somente após a construção validada da distribuição.

---

# 65. Renda Zero

Renda zero é conceitualmente possível.

Não rejeitar automaticamente sem avaliar a distribuição oficial.

O tratamento final deve constar nos testes.

---

# 66. Renda Negativa

A interface não deve aceitar renda familiar negativa.

Se houver valores negativos ou códigos especiais nos microdados:

> tratá-los conforme documentação oficial, não como renda econômica real.

---

# 67. Missing Values

Valores:

- ausentes;
- ignorados;
- não aplicáveis;
- códigos especiais;

não devem ser convertidos automaticamente em zero.

Seguir o dicionário oficial.

---

# 68. Rendas Extremas

A PNAD pode sub-representar rendas extremamente elevadas.

Esse é um limite conhecido de pesquisas domiciliares.

Portanto, para rendas muito altas:

- evitar falsa precisão;
- considerar limitar a apresentação;
- indicar quando o usuário está acima da faixa em que o dataset oferece boa resolução.

A regra operacional será definida após análise dos microdados.

---

# 69. Extremos Globais

O mesmo cuidado se aplica ao PIP.

Não extrapolar além dos limites confiáveis do modelo/CDF sem aviso.

---

# 70. Testes Mundiais

Validar:

- conversão BRL → PPP;
- unidade mensal → diária;
- ano PPP;
- versão PIP;
- monotonicidade da CDF;
- valores de referência;
- resultados contra o PIP oficial em linhas monetárias conhecidas.

---

# 71. Teste De Pobreza Como Sanity Check

Uma forma importante de validação mundial:

utilizar uma linha internacional conhecida do PIP.

Se o nosso lookup global for consultado exatamente naquela linha, deve reproduzir aproximadamente o headcount mundial publicado pelo PIP para:

- mesmo ano;
- mesma versão;
- mesma PPP.

Caso contrário:

> existe problema na construção da distribuição.

---

# PARTE V — LINGUAGEM DOS RESULTADOS

# 72. Brasil

Formulação preferida:

> **Sua renda por pessoa é maior que a de aproximadamente X% da população brasileira considerada pela distribuição.**

Versão curta:

> **Você está aproximadamente no percentil X de renda no Brasil.**

---

# 73. Mundo

Formulação preferida:

> **Sua posição estimada está aproximadamente no percentil X da distribuição monetária mundial utilizada.**

Explicação:

> **A comparação global combina dados de renda ou consumo por pessoa de diferentes países, ajustados por poder de compra.**

---

# 74. Palavra “Rico”

O slogan pode utilizar:

> **Você é mais rico do que quantos brasileiros?**

como mecanismo de comunicação.

Entretanto, a metodologia deve esclarecer:

> **o cálculo mede renda relativa, não riqueza patrimonial.**

Não usar “patrimônio”, “riqueza líquida” ou “fortuna” como sinônimos dos resultados.

---

# 75. Média

Quando a média nacional for mostrada:

> deixar claro que é uma média.

Nunca sugerir:

> “R$ 2.316 representa o brasileiro do meio.”

Isso não decorre da estatística.

---

# 76. Mediana

A mediana pode futuramente ser mostrada como informação adicional, desde que calculada diretamente da distribuição ponderada validada.

---

# 77. Percentil

Explicação simples:

> **Percentil 68 significa que sua renda está aproximadamente acima da observada para 68% da distribuição considerada.**

Evitar definições excessivamente técnicas na interface principal.

---

# 78. TOP Percentual

Explicação:

> **TOP 32% significa que sua renda está aproximadamente dentro dos 32% superiores da distribuição.**

Usar “aproximadamente” quando necessário.

---

# PARTE VI — FUNCIONALIDADES FUTURAS

# 79. Comparação Por Estado

Não implementar usando:

```text
renda do usuário / renda média estadual
```

Isso é metodologicamente inválido como percentil.

Para cada UF será necessário:

- filtrar amostra;
- respeitar pesos;
- construir distribuição;
- avaliar tamanho amostral;
- avaliar incerteza;
- validar resultados.

---

# 80. Municípios

A PNAD Contínua não deve ser utilizada automaticamente para gerar distribuições municipais detalhadas sem verificar a representatividade estatística do recorte.

Município exige projeto metodológico próprio.

---

# 81. Histórico

Para comparar:

> “onde essa renda estaria em 2015?”

será necessário:

- dataset daquele ano;
- pesos correspondentes;
- compatibilidade metodológica;
- correção monetária;
- tratamento de quebras de série.

Não simplesmente aplicar IPCA à distribuição atual.

---

# 82. POF

A Pesquisa de Orçamentos Familiares será usada futuramente para:

> **Como famílias semelhantes costumam gastar?**

Ela não deve ser usada para alterar os percentis de renda da PNAD.

Cada fonte mantém seu papel específico.

---

# 83. Crédito E Banco Central

Dados do Banco Central serão utilizados para:

- juros;
- modalidades de crédito;
- comparações financeiras;
- educação.

Não entram no cálculo da posição de renda.

---

# PARTE VII — QUESTÕES QUE PRECISAM SER FECHADAS

# 84. Checklist Metodológico Pré-produção

Antes do deploy definitivo da V1, resolver:

- confirmar arquivo exato da PNAD 2025;
- confirmar primeira visita;
- confirmar variável oficial de RDPC;
- confirmar variável oficial de peso;
- confirmar tratamento de missing;
- confirmar tratamento de renda zero;
- confirmar deflator;
- definir referência de preços;
- reproduzir indicadores oficiais do IBGE;
- gerar CDF brasileira;
- validar percentis;
- definir casas decimais;
- congelar versão PIP;
- definir ano mundial;
- definir tratamento de nowcast;
- validar PPP utilizada;
- validar conversão BRL → PPP;
- construir CDF mundial;
- reproduzir headcounts conhecidos do PIP;
- documentar limites de renda extrema;
- gerar manifestos;
- gerar checksums;
- executar testes de regressão.

---

# 85. Regra Para O Codex

Ao encontrar qualquer item `[CONFIRMAR]`:

> **não implementar uma escolha arbitrária.**

O Codex pode:

1. localizar a documentação oficial;
2. identificar as alternativas;
3. demonstrar evidências;
4. propor a opção tecnicamente correta;

mas a escolha deve ser registrada explicitamente neste documento.

---

# 86. Proibição De Hardcode Silencioso

Não espalhar no código:

```text
2025
2316
PPP
percentis
limites
versões
```

sem metadados centralizados.

Datasets devem carregar suas próprias versões e metadados.

---

# 87. Separação Entre Cálculo E Interface

A UI não deve conter a lógica estatística principal.

Preferência arquitetural:

```text
data pipeline
↓
dataset validado
↓
função de domínio
↓
UI
```

Não:

```text
React component
↓
fórmulas improvisadas
↓
resultado
```

---

# 88. Pure Functions

As funções centrais devem ser determinísticas.

Exemplos conceituais:

```text
calculatePerCapitaIncome()
getBrazilPercentile()
convertBRLToPPP()
getGlobalPercentile()
```

Com testes independentes da interface.

---

# 89. Resultado Reproduzível

Para qualquer cálculo, deve ser possível registrar tecnicamente:

```text
metodologia
dataset
versão
data de preços
input
resultado
```

sem necessariamente armazenar o input do usuário em produção.

---

# 90. Política De Falha

Quando houver dúvida entre:

> mostrar um número possivelmente errado

e

> não mostrar o resultado,

preferir:

> **não mostrar o resultado.**

Mensagem:

> **Não conseguimos calcular sua posição com segurança agora.**

Confiabilidade tem prioridade sobre disponibilidade absoluta.

---

# 91. Política De Transparência

A página pública de metodologia deve explicar em linguagem comum:

### Brasil

> Utilizamos dados da PNAD Contínua do IBGE e consideramos a renda total da casa dividida pelo número de moradores.

### Mundo

> Convertemos o valor para uma medida internacional de poder de compra e o comparamos com dados globais do Banco Mundial.

### Limitação

> O resultado é uma estimativa estatística e não representa patrimônio, riqueza acumulada ou padrão individual de vida.

---

# 92. Norte Metodológico

A ferramenta não precisa produzir o número mais impressionante.

Precisa produzir o número **mais defensável**.

A prioridade é:

> **correto antes de viral**

> **reproduzível antes de sofisticado**

> **transparente antes de aparentemente preciso**

> **fonte oficial antes de conveniência**

---

# 93. Definition of Done Metodológica Da V1

A metodologia estará pronta para produção somente quando:

- a base brasileira estiver identificada;
- as variáveis estiverem confirmadas;
- os pesos estiverem confirmados;
- o pipeline reproduzir estatísticas oficiais;
- a distribuição ponderada estiver validada;
- a inflação/referência de preços estiver resolvida;
- a versão mundial estiver congelada;
- PPP estiver validada;
- a CDF mundial estiver reproduzível;
- testes contra PIP estiverem aprovados;
- limites forem documentados;
- datasets tiverem manifestos;
- datasets tiverem checksums;
- regressões estiverem automatizadas;
- a página pública de metodologia refletir exatamente o cálculo executado pelo código.

Somente depois disso os valores devem ser tratados como resultados oficiais do **Renda Comparada**.