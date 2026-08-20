---
title: 04-metodologia-dados
created: 2026-08-12T17:07:15.000-03:00
modified: 2026-08-14T16:49:00.000-03:00
---

# 04-metodologia-dados

**Produto:** Renda Comparada  
**Versão do documento:** 1.4
**Status:** Canônico — motores Brasil e Mundo validados e integrados; deploy não autorizado
**Última revisão:** 14/08/2026

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
|Paridade de poder de compra operacional do pipeline Mundo|World Bank PIP — tabelas auxiliares `aux/ppp` e `aux/cpi`|
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

A edição aprovada para validação é:

```text
IBGE_YEAR = 2025
IBGE_RELEASE = 20260508
IBGE_FILE = PNADC_2025_visita1_20260508.zip
```

A versão exata e seu SHA-256 foram registrados em `docs/research/artifacts/fase-1c-source-manifest.json`. O pacote Brasil está materializado, e `data/production/brazil/brazil-income-engine-manifest.json` referencia a CDF canônica por caminho, versão e SHA-256, preservando a proveniência documentada.

Se o IBGE substituir explicitamente essa edição por arquivo posterior, a atualização deve ser interrompida para comparação e nova decisão. Não utilizar automaticamente a versão mais nova.

---

# 6. Por Que Utilizar Microdados

A média nacional divulgada pelo IBGE não é suficiente para responder:

> **“Minha renda é maior que a de quantos brasileiros?”**

O IBGE publicou em 2025 dois valores médios com conceitos distintos que não podem ser confundidos.

Para a distribuição de **Rendimento de Todas as Fontes 2025**, o benchmark direto validado é:

> **R$ 2.264 por pessoa/mês, em valores reais a preços médios de 2025.**

Para o indicador nominal associado à LC 143/2013/FPE, o IBGE divulgou:

> **R$ 2.316**

Ambos representam **médias**, não percentis, medianas ou cortes de classe. Além disso, pertencem a universos e conceitos de renda diferentes.

Portanto:

> **Nenhuma média pode ser utilizada diretamente para calcular a posição do usuário.**

Precisamos da **distribuição completa** ou de uma representação estatisticamente equivalente dela.

---

# 7. Conceito Brasileiro De Renda

O conceito central adotado é o:

> **rendimento domiciliar per capita**

Para a distribuição principal da V1, o conceito aprovado é:

> **pessoas segundo o rendimento domiciliar per capita do domicílio em que vivem, dentro da população elegível do indicador oficial selecionado.**

A construção validada combina, no nível do domicílio:

- `VD4019`: rendimento habitual de todos os trabalhos;
- `VD4048`: rendimentos de outras fontes efetivamente recebidos.

Para reproduzir a distribuição específica de **Rendimento de Todas as Fontes 2025** selecionada pelo projeto, essa construção não utiliza os componentes adicionais de cartão/tíquete presentes em `VD5011`. Isso não significa afirmar genericamente que cartão/tíquete “não é renda”; é uma delimitação do indicador estatístico adotado.

O indicador exclui da soma e do denominador as pessoas classificadas na condição do domicílio como:

- pensionista;
- empregado doméstico;
- parente de empregado doméstico.

Não descrever a construção como “todos os rendimentos efetivamente recebidos”, porque o componente de trabalho é habitual.

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

A descrição operacional definitiva deve permanecer alinhada ao dicionário, às notas técnicas e às validações da Fase 1C.

A renda informada pelo usuário e a distribuição devem estar na mesma referência monetária antes da comparação. Para a V1, a renda nominal vigente é trazida para preços médios de 2025 pelo IPCA nacional, conforme a regra canônica das seções 27–30 e D065.

---

# 9. Renda Bruta

Para manter compatibilidade com a distribuição aprovada, a entrada inicial da V1 deve ser orientada para:

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

No componente de trabalho, “renda bruta” deve ser compreendida como rendimento habitualmente recebido; nas outras fontes, como rendimento efetivamente recebido no período de referência.

---

# 10. Moradores

A pergunta deve ser:

> **Quantas pessoas moram nesta casa?**

Devem ser considerados **os moradores que pertencem à população elegível segundo a metodologia oficial adotada**, inclusive:

- adultos;
- crianças;
- pessoas sem renda.

Na construção validada, pensionistas, empregados domésticos e parentes de empregados domésticos residentes são excluídos da soma e do denominador, conforme o universo representado por `VD2003`. Essa é uma qualificação estatística obrigatória da expressão “todos os moradores”.

Portanto:

> **não utilizar somente o número de adultos.**

A interface não será alterada nesta fase. A futura microcopy deve explicar a composição sem tratar “família” e “domicílio” como sinônimos técnicos.

---

# 11. Fórmula Básica Do Usuário

Definir:

`R_domicilio`

como renda mensal total do domicílio.

Definir:

`N_moradores_elegiveis`

como número de moradores pertencentes à população elegível do indicador.

Então:

```text
RDPC_usuario = R_domicilio / N_moradores_elegiveis
```

Onde:

`RDPC_usuario`

significa:

> **renda domiciliar per capita do usuário.**

---

# 12. Exemplo

Domicílio:

- renda mensal: R$ 6.500;
- moradores: 3.

Então:

```text
RDPC_usuario = 6500 / 3
RDPC_usuario = 2166,666…
```

Valor aproximado:

> **R$ 2.166,67 por pessoa/mês.**

Esse valor é comparado com a CDF brasileira canônica materializada e autorizada para integração pelo manifesto de motor.

---

# 13. Unidade Estatística Brasileira

A distribuição deve responder à pergunta:

> **Qual proporção da população brasileira possui rendimento domiciliar per capita inferior ao do usuário?**

Isso significa que a unidade final de interpretação é a **pessoa**, posicionada segundo o rendimento domiciliar per capita do domicílio no qual reside.

Mais precisamente, é uma **pessoa elegível** segundo o universo do indicador selecionado.

Não é uma distribuição simples de domicílios.

Não é uma distribuição de salários individuais.

Não é uma distribuição de responsáveis pelo domicílio.

---

# 14. Estrutura Da Distribuição

Cada pessoa elegível da amostra recebe o rendimento domiciliar per capita correspondente ao seu domicílio.

Exemplo conceitual:

Domicílio A:

- renda: R$ 10.000;
- quatro moradores;
- RDPC: R$ 2.500.

Se os quatro moradores forem elegíveis, todos pertencem à faixa de:

> **R$ 2.500 per capita**

respeitando os pesos estatísticos aplicáveis.

---

# 15. Pesos Amostrais

A PNAD Contínua é uma pesquisa amostral.

Portanto:

> **os registros não podem receber peso 1.**

Deve ser utilizado:

```text
IBGE_WEIGHT_VARIABLE = V1032
```

`V1032` é o peso com calibração da edição selecionada e deve ser registrado no manifesto do dataset.

A Fase 1C confirmou que `V1032` não apresenta missing, zero, negativos ou valores não finitos na edição `20260508`, e que sua soma na população elegível reproduz a população oficial no nível de publicação. Esses testes devem ser repetidos em toda atualização. Não criar correções ad hoc nem substituir `V1032` por outro peso sem nova decisão.

### Regra

Se a inspeção da edição contradizer a documentação:

> **suspender o processamento e reabrir a decisão metodológica.**

---

# 16. Construção Do Rendimento

A Fase 1C falsificou empiricamente a hipótese de usar `VD5011` como variável principal. A construção brasileira canônica da V1 é:

```text
RDPC_real_2025 =
    soma_domiciliar(
        VD4019 × CO1
        +
        VD4048 × CO1e
    )
    ÷ VD2003
```

onde:

- `VD4019` é o rendimento habitual do trabalho;
- `CO1` é o deflator aplicável ao componente habitual;
- `VD4048` é o rendimento efetivamente recebido de outras fontes;
- `CO1e` é o deflator aplicável ao componente efetivo;
- `VD2003` é o número de componentes elegíveis do domicílio;
- `V1032` é o peso amostral aplicado às pessoas elegíveis.

Blanks estruturais em `VD4019` ou `VD4048` representam ausência daquele componente e entram como zero apenas na soma de componentes. Isso não converte missing do RDPC final em zero. Como validação independente, a soma domiciliar nominal de `VD4019 + VD4048` reproduziu `VD5007` sem diferenças nos 408.243 registros elegíveis analisados.

`VD5011 × CO1` e `VD5008 × CO1` não são construções oficiais da distribuição de produção. Podem permanecer somente como diagnósticos históricos ou auxiliares.

---

# 17. Registro Obrigatório Das Variáveis

Configuração canônica aprovada:

```text
IBGE_YEAR = 2025
IBGE_RELEASE = 20260508
IBGE_FILE = PNADC_2025_visita1_20260508.zip
IBGE_VISIT = primeira visita
IBGE_WORK_INCOME_VARIABLE = VD4019
IBGE_WORK_DEFLATOR = CO1
IBGE_OTHER_INCOME_VARIABLE = VD4048
IBGE_OTHER_INCOME_DEFLATOR = CO1e
IBGE_HOUSEHOLD_ELIGIBLE_COMPONENTS = VD2003
IBGE_WEIGHT_VARIABLE = V1032
IBGE_UF_VARIABLE = UF
IBGE_PRICE_REFERENCE = preços médios de 2025
IBGE_COMPONENT_BLANK_RULE = ausência estrutural do componente; zero somente na soma
IBGE_WEIGHT_MISSING_CODES = nenhum observado na edição 20260508
IBGE_RDPC_NEGATIVE_VALUES_OBSERVED = 0
IBGE_RDPC_MAX_OBSERVED_2025 = 200165.7922757916
USER_INCOME_PRICE_ALIGNMENT = aprovado
USER_INCOME_PRICE_ALIGNMENT_METHOD = deflacionar a renda nominal corrente para preços médios de 2025
USER_INCOME_PRICE_INDEX = IPCA nacional — SIDRA 1737, variável 2266
USER_INCOME_BASE_PRICE_INDEX_2025 = 7300.8416666666666667
USER_INCOME_CURRENT_PRICE_INDEX = último mês oficialmente publicado e aprovado no manifesto de preços
```

As constatações de missing, negativos e máximo valem para a edição `20260508` e devem ser testadas novamente em toda atualização. O alinhamento temporal da renda do usuário foi canonizado em 14/08/2026: a renda nominal vigente é trazida para preços médios de 2025 pelo IPCA nacional antes do lookup na CDF. O mês corrente do índice não é consultado silenciosamente a cada cálculo; ele vem de manifesto versionado e aprovado.

---

# 18. Visita Da PNAD

Para o rendimento domiciliar per capita oficial de 2025, utilizar as **primeiras visitas** realizadas ao longo dos quatro trimestres do ano.

A base utilizada pelo Renda Comparada deverá ser compatível com essa escolha.

A visita efetivamente usada no pipeline deve constar no manifesto como:

```text
IBGE_VISIT = primeira visita
```

---

# 19. Reponderação De 2025

A PNAD passou por atualização de estimativas populacionais e reponderação da série com base nas novas projeções associadas ao Censo 2022.

O IBGE publicou em 2025 nota técnica específica sobre atualização das estimativas populacionais para cálculo dos pesos.

Consequência:

> **não reutilizar pesos antigos ou datasets baixados anteriormente sem verificar se continuam sendo a versão oficial vigente.**

Utilizar o peso oficial da edição selecionada. Não recalibrar, reconstruir ou combinar pesos por conta própria.

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

# 25. Precisão Visual Brasileira

A CDF deve conservar precisão interna completa. O arredondamento acontece somente na apresentação.

A regra de exibição brasileira é canonizada por D071.

Definir:

```text
p = 100 × share_below
t = 100 - p
```

### Faixa Principal

Quando `t >= 1` e a renda estiver dentro do suporte observado:

```text
percentil_exibido = arredondar(p)
top_exibido = 100 - percentil_exibido
```

Exibir, por exemplo:

> **TOP 30%**

> **Percentil 70**

Não arredondar as duas leituras de forma independente se isso puder quebrar a complementaridade visual.

### Cauda Superior

Para `0,1 <= t < 1`, utilizar uma casa decimal.

Para `0 < t < 0,1`, preferir:

> **Entre menos de 0,1% de maior renda na distribuição observada.**

com leitura secundária equivalente a:

> **Acima do percentil 99,9.**

Não exibir `TOP 0%`.

### Renda Zero

Em `RDPC = 0`, não usar `TOP 100%` como headline. Informar que zero é o menor nível observado e que existem empates nesse valor.

### Acima Do Máximo

Acima do maior RDPC observado, não extrapolar. Informar que o valor supera o máximo observado na distribuição e que não há resolução suficiente para uma posição mais fina.

### Moeda

Valores monetários mostrados ao usuário podem usar duas casas decimais. Cálculos internos não devem sofrer arredondamento prematuro.

Evitar qualquer precisão visual como:

> **67,934728%**

porque ela não melhora a interpretação e sugere exatidão individual inexistente.

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

Princípio canônico:

> **a renda digitada pelo usuário e a distribuição precisam estar na mesma referência monetária antes da comparação.**

---

# 28. Referência De Preços

A referência canônica da distribuição escolhida é:

```text
IBGE_PRICE_REFERENCE = preços médios de 2025
```

“Preços médios de 2025” significam o nível de preços dado pela **média aritmética dos 12 números-índice mensais do IPCA nacional de janeiro a dezembro de 2025**, e não dezembro de 2025.

Para a série SIDRA 1737, variável 2266:

```text
IPCA_MEDIO_2025 = 7300.8416666666666667
```

A estratégia canônica da V1 é **preservar a CDF em preços médios de 2025 e trazer a renda nominal corrente do usuário para essa mesma referência monetária**. Não atualizar os thresholds da CDF a cada mês.

---

# 29. Fonte De Inflação

Para o alinhamento temporal nacional da V1, a fonte canônica é:

> **IPCA nacional — IBGE, SIDRA tabela 1737, variável 2266, número-índice.**

A V1 não solicita UF. Por isso, o IPCA nacional é adotado como compromisso metodológico transparente entre simplicidade da jornada e precisão regional. Ele não deve ser descrito como equivalente ao deflator regional exato de um usuário cuja UF fosse conhecida.

Não utilizar:

- inflação informal;
- estimativas de blogs;
- variação do salário mínimo;
- CDI;
- Selic;
- projeção de IPCA ainda não publicada;

como substitutos do índice oficial.

---

# 30. Regra Operacional Canônica

A regra operacional canônica para a distribuição brasileira é:

```text
IBGE_WORK_INCOME_VARIABLE = VD4019
IBGE_WORK_DEFLATOR = CO1
IBGE_OTHER_INCOME_VARIABLE = VD4048
IBGE_OTHER_INCOME_DEFLATOR = CO1e
IBGE_HOUSEHOLD_ELIGIBLE_COMPONENTS = VD2003
USER_INCOME_PRICE_ALIGNMENT = aprovado
USER_INCOME_PRICE_INDEX = IPCA nacional — SIDRA 1737, variável 2266
USER_INCOME_BASE_INDEX_2025 = 7300.8416666666666667
USER_INCOME_CURRENT_INDEX = último mês oficial aprovado no manifesto de preços
```

Aplicar `CO1` ao componente habitual `VD4019` e `CO1e` ao componente efetivo `VD4048`, usando a chave ano, trimestre e UF do arquivo oficial de deflatores. Somar no nível correto de domicílio e dividir por `VD2003`.

Para a renda informada pelo usuário, definir:

```text
B = IPCA médio de 2025
M = número-índice do último mês oficial disponível e aprovado

renda_domiciliar_2025 = renda_domiciliar_corrente × B / M
RDPC_usuario_2025 = renda_domiciliar_2025 / moradores_elegíveis
posição_brasil = lookup_CDF_2025(RDPC_usuario_2025)
```

A entrada da V1 é interpretada como **renda mensal nominal vigente na data do cálculo**. A aplicação deve registrar e tornar acessível o mês do IPCA efetivamente utilizado. Não projetar mês ainda não publicado.

A CDF de 2025 permanece imutável. Atualizações mensais de IPCA geram apenas um manifesto pequeno, versionado, validado e aprovado; a aplicação não consulta “latest” silenciosamente a cada cálculo.

Não aplicar um fator único sobre `VD5011` ou `VD5008`. Fatores, componentes e referência devem constar nos metadados.

---

# 31. Validação Obrigatória — Brasil

O pipeline brasileiro deve ser validado contra resultados oficiais publicados pelo IBGE.

Um teste obrigatório é reconstruir, a partir da base e pesos escolhidos, estatísticas oficiais conhecidas do mesmo universo.

Benchmark direto validado:

```text
BRAZIL_VALIDATION_MEAN_2025 = 2264
BRAZIL_VALIDATION_MEAN_TYPE = real, preços médios de 2025
BRAZIL_VALIDATION_STATUS = direto validado na Fase 1C
BRAZIL_VALIDATION_RECONSTRUCTED_MEAN = 2264.0378279
```

A Fase 1C também obteve:

- Gini calculado de aproximadamente `0,511224`, compatível com `0,511` publicado;
- 27 de 27 médias de UF reproduzidas após arredondamento;
- 10 de 12 cortes nacionais reproduzidos exatamente após arredondamento;
- diferença de R$ 1 em P90 e P99;
- população ponderada de `212.624.284,8006`, compatível com `212.624 mil` publicados.

Os resíduos de R$ 1 nos cortes e de até R$ 2 em algumas médias acumuladas não autorizam ajuste artificial da fórmula. O procedimento exato de partição e arredondamento deverá ser documentado antes dos golden cases de cortes.

Diferenças relevantes indicam problema em:

- visita;
- variável;
- pesos;
- filtros;
- deflator;
- unidade estatística.

---

# 32. R$ 2.316 É Validação Auxiliar

R$ 2.316 pertence ao indicador nominal de rendimento domiciliar per capita divulgado para finalidades relacionadas à LC 143/2013/FPE. Ele usa renda efetivamente recebida e população distinta da distribuição principal validada para o projeto.

Classificação:

> **VALIDAÇÃO AUXILIAR / CONTEXTO OFICIAL**

O pipeline brasileiro não deve ser obrigado a reproduzir R$ 2.316, e a diferença para R$ 2.264 não constitui erro.

Nenhuma média deve ser usada para calcular percentis.

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

A fonte principal é:

> **World Bank — Poverty and Inequality Platform — PIP**

O PIP reúne estimativas de pobreza, desigualdade e prosperidade compartilhada para mais de 170 economias e utiliza dados de pesquisas domiciliares, incluindo microdados ou dados agrupados.

---

# 34. Versão Internacional Da V1

Para a V1, congelar a versão PIP baseada em PPPs de 2021 identificada como:

```text
PIP_VERSION = 20260324_2021
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
```

Essa escolha é regida por D066.

Nunca consultar simplesmente:

> **latest**

em produção sem registrar e aprovar nova versão.

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

A formulação canônica deve tratá-lo como:

> **posição monetária global estimada**

A explicação deve informar, em linguagem acessível:

> **A comparação global utiliza dados de renda ou consumo domiciliar por pessoa, conforme a metodologia disponível para cada país, ajustados por poder de compra.**

Não usar como afirmação principal:

> **“Você ganha mais do que X% do mundo.”**

sem nova decisão metodológica que demonstre que essa simplificação é defensável.

Essa regra é regida por D067.

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

# 39. PPP E CPI Operacionais Da Build PIP

D069 canoniza as tabelas auxiliares `ppp` e `cpi` da própria build PIP congelada como fontes operacionais da conversão Mundo:

```text
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
BRAZIL_PIP_PPP_2021 = 2.44986319541931
BRAZIL_PIP_CPI_2024_BASE_2021 = 1.192919586578344
BRL_PER_INTL_2024 = BRAZIL_PIP_PPP_2021 × BRAZIL_PIP_CPI_2024_BASE_2021
                  = 2.92248979025310406149724542264
```

`BRL_PER_INTL_2024` é fator derivado, não terceira fonte independente. O valor CPI de 2024 aparece diretamente no raw da tabela auxiliar. ICP e WDI, inclusive `PA.NUS.PRVT.PP`, permanecem apenas como cross-check e não substituem os fatores observados na build PIP.

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

# 41. Conversão Internacional — Estrutura Canônica

D069 define a seguinte estrutura:

```text
BRL corrente por domicílio/mês
↓
divisão pelo número de moradores
↓
alinhamento pelo IPCA nacional para preços médios de 2024
↓
divisão pelo fator PPP × CPI da build PIP
↓
dólares internacionais PPP 2021 por pessoa/mês
↓
conversão mensal para diária
↓
distribuição global PIP
```

---

# 42. Conversão Mensal Para Diária

Como o PIP utiliza unidade por dia, definir explicitamente a conversão.

Regra canônica da V1, conforme D069:

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

# 43. Conversão PPP — Regra Canônica D069

Para o pipeline Mundo, definir:

```text
IPCA_AVG_2024 = média aritmética dos 12 números-índice mensais de janeiro a dezembro de 2024
IPCA_AVG_2024 = 6952.07333333333333333333333333333333333333333333333333333333
CURRENT_PRICE_REFERENCE_MONTH = 2026-07
IPCA_CURRENT = 7657.7300000000000

dailyPPP = (householdIncomeCurrent / residents)
         × (IPCA_AVG_2024 / IPCA_CURRENT)
         ÷ (BRAZIL_PIP_PPP_2021 × BRAZIL_PIP_CPI_2024_BASE_2021)
         × 12 / 365
```

Saída:

```text
international_2021_ppp_per_person_per_day
```

A primeira perna é uma extensão brasileira do Renda Comparada: ela alinha a renda nominal corrente a preços médios de 2024 pelo IPCA nacional, SIDRA tabela 1737, variável 2266. O PIP não deflaciona diretamente a renda digitada.

Regras do contrato:

- dividir a renda domiciliar corrente pelo número de moradores antes da comparação;
- usar os valores completos de PPP e CPI observados nos raws da build congelada;
- não fazer arredondamento intermediário;
- não usar câmbio comercial;
- não usar constantes legadas;
- não usar WDI ou ICP como substitutos dos fatores `PIP aux`;
- não reutilizar D065 automaticamente: D065 alinha Brasil a preços médios de 2025, enquanto D069 alinha Mundo ao ano global de 2024;
- tratar julho/2026 como referência versionada desta versão, não como constante corrente eterna; atualização exige nova evidência oficial preservada, regeneração dos golden cases, testes e promoção explícita em artefato ou manifesto Mundo.

---

# 44. Fonte E Método Canônicos Para A CDF Mundial

O PIP permite calcular indicadores para países, regiões ou agregados em diferentes linhas monetárias.

A API oficial possui endpoints para:

- estatísticas;
- agregações;
- curvas de Lorenz;
- dados agrupados;
- versões;
- anos válidos.

D068 canoniza a construção **offline** a partir do dataset oficial **1000 Binned Global Distribution**, recurso `DR0094423`, arquivo `GlobalDist1000bins_1990_2026_20260324_2021_01_02_PROD.csv`.

Para 2024, a fonte contém 218 economias e 1.000 bins por economia. `welf` representa dólares internacionais PPP 2021 por pessoa por dia; `pop` representa milhões de pessoas no bin.

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

Definir, conforme D068:

```text
GlobalCDF(x)
```

como proporção da população mundial com `welf` estritamente menor que o nível de bem-estar monetário `x`.

Então:

```text
percentil_global = 100 × GlobalCDF(x)
```

Preservar também:

```text
shareBelow(x) = peso com welf < x / peso total
shareAtOrBelow(x) = peso com welf <= x / peso total
topShare(x) = 1 - shareBelow(x)
```

Valores empatados de `welf` são agrupados em um único degrau. A CDF não interpola entre pontos e não extrapola além do suporte observado.

---

# 46A. Precisão, Caudas E Golden Cases Mundiais — D070

D070 congela o contrato de golden cases reproduzíveis. O teste versionado espera 11 casos, e o manifesto Mundo registra `validation/world/world-income-golden-cases-d070-candidate.json` por caminho, versão, SHA-256 e tamanho; o conteúdo detalhado do artefato permanece fora do HEAD atual. O contrato usa a CDF D068 e a conversão D069 sem arredondamento intermediário.

Definir:

```text
topPercent = 100 × topShare
maxErrorPp = 0.022516991848920
```

Dentro do suporte observado:

```text
topShare >= 0,01
    → percentil inteiro e TOP inteiro complementar

0,001 <= topShare < 0,01
    → TOP com uma casa decimal

topPercent < 0,1 e topPercent + maxErrorPp < 0,1
    → "menos de 0,1%"

topPercent < 0,1 e topPercent + maxErrorPp >= 0,1
    → "aproximadamente 0,1%"
```

A decisão da cauda extrema usa valores internos não arredondados. A margem de erro D068 impede afirmar “menos de 0,1%” quando o limite de 0,1 ponto percentual ainda estiver dentro da incerteza medida.

Regras de suporte:

- no mínimo, preservar o primeiro degrau e empates, sem `TOP 100%` como headline;
- abaixo do mínimo, informar fora do suporte inferior, sem extrapolação;
- no máximo, preservar o último degrau observado;
- acima do máximo, informar fora do suporte superior, sem extrapolação;
- nunca exibir `TOP 0%`;
- preservar `shareBelow` com `<` e `shareAtOrBelow` com `<=`;
- usar sempre a linguagem **posição monetária global estimada**, conforme D067.

Essa política é exclusiva do Mundo e não altera D071.

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

# 48. Construção Offline Mundial Canonizada Por D068

Pipeline canônico:

```text
raw oficial DR0094423 com hash verificado
↓
filtrar exatamente year = 2024 e build 20260324_2021_01_02_PROD
↓
validar schema, chaves, 218 economias e 1.000 bins por economia
↓
ordenar por welf, agrupar empates e acumular pop
↓
CDF empírica em degraus
↓
validar contra checkpoints oficiais PIP da mesma vintage
↓
artefato versionado, somente após autorização de produção
```

Missing, campos não numéricos ou não finitos, `welf` negativo e `pop` não positivo invalidam a construção. Não imputar, interpolar, extrapolar nem usar fallback legado.

A base binned perde desigualdade dentro de cada faixa. D068 prevê validação contra checkpoints oficiais PIP da mesma vintage; o pacote e o manifesto versionados preservam `0,022516991848920` ponto percentual como erro absoluto máximo operacional, sem comprovar aqui a quantidade detalhada desses checkpoints. D070 usa esse limite para restringir a precisão visual e a linguagem da cauda extrema; ele não autoriza posição individual exata.

Na etapa de D068, a aplicação futura deveria responder localmente ou pela infraestrutura própria do projeto; D068, isoladamente, não autorizava integração nem promoção da candidata. Posteriormente, o pacote foi promovido e a integração foi autorizada pelo manifesto agregador `data/production/world/world-income-engine-manifest.json`, sem alterar a metodologia ou os hashes históricos.

---

# 49. Ano Mundial De Referência

O ano mundial não deve ser escolhido automaticamente apenas porque é o maior ano retornado pela API.

Precisamos distinguir:

- observação de pesquisa;
- interpolação;
- extrapolação;
- nowcast.

A versão PIP vigente informa que estimativas posteriores a 2024 são nowcasts.

---

# 50. Ano Mundial Canonizado Para A V1

Conforme D066, a V1 congela:

```text
GLOBAL_REFERENCE_YEAR = 2024
GLOBAL_ESTIMATION_TYPE = reference-year aggregate; não nowcast
PIP_VERSION = 20260324_2021
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
```

A expressão `reference-year aggregate; não nowcast` não significa que todos os países realizaram pesquisa domiciliar em 2024. O agregado mundial continua sendo construído pelo PIP a partir de pesquisas, interpolações e alinhamentos entre países.

Não deixar o ano variar automaticamente.

---

# 51. Anos Posteriores A 2024

Para a V1, não utilizar 2025 ou 2026 como ano global apenas para aproximar visualmente o ano brasileiro.

Na versão PIP congelada, estimativas posteriores a 2024 são nowcasts.

Uma futura adoção de ano posterior exige:

1. nova versão metodológica;
2. validação;
3. decisão explícita;
4. linguagem que identifique corretamente o uso de nowcast.

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
    distribution-2024-pip-20260324_2021.json
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
  "source_release_id": "20260508",
  "source_file": "PNADC_2025_visita1_20260508.zip",
  "visit": "primeira visita",
  "downloaded_at": "YYYY-MM-DD",
  "processed_at": "YYYY-MM-DD",
  "price_reference": "preços médios de 2025",
  "methodology_version": "1.0.0",
  "weight_variable": "V1032",
  "work_income_variable": "VD4019",
  "work_deflator": "CO1",
  "other_income_variable": "VD4048",
  "other_income_deflator": "CO1e",
  "household_eligible_components": "VD2003",
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
  "reference_year": 2024,
  "ppp_basis": 2021,
  "ppp_source": "PIP aux/ppp",
  "cpi_source": "PIP aux/cpi",
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

O resultado esperado deste caso deve ser obtido dos golden cases Brasil referenciados, com seu SHA-256, por `data/production/brazil/brazil-income-engine-manifest.json`; não preencher um percentil manualmente.

---

# 65. Renda Zero

RDPC igual a zero é estatisticamente válido e, quando pertencente à população elegível, deve permanecer na distribuição.

Na edição `20260508`, a construção validada encontrou 4.682 registros de RDPC zero, representando 2.365.090,64 pessoas ponderadas ou 1,112333% da população elegível.

Não excluir renda zero para melhorar a aparência da CDF.

Isso não decide se o formulário aceitará renda zero. Essa decisão permanece em UX/produto.

---

# 66. Renda Negativa

A interface não deve aceitar renda domiciliar negativa.

Para os microdados:

```text
IBGE_RDPC_NEGATIVE_VALUES_OBSERVED_2025 = 0
```

Esse resultado vale para a edição `20260508` e deve ser testado novamente em toda atualização. Se uma edição futura contiver valores negativos ou códigos especiais:

> quantificar, verificar o significado e voltar à decisão metodológica antes da CDF definitiva.

Não excluir automaticamente.

---

# 67. Missing Values

Valores:

- ausentes;
- ignorados;
- não aplicáveis;
- códigos especiais;

não devem ser convertidos automaticamente em zero.

Configuração validada para a edição `20260508`:

```text
IBGE_COMPONENT_BLANK_RULE = ausência estrutural do componente; zero somente na soma
IBGE_WEIGHT_MISSING_CODES = nenhum observado
```

Blanks de `VD4019` e `VD4048` representam ausência daquele componente e não missing do RDPC final. Seguir o dicionário oficial e repetir a inspeção a cada edição. Missing de peso, zero, negativos, infinitos, valores não numéricos ou extremos anômalos não autorizam correções ad hoc.

---

# 68. Rendas Extremas

A PNAD pode sub-representar rendas extremamente elevadas.

Esse é um limite conhecido de pesquisas domiciliares.

Regra canônica:

> **não utilizar extrapolação paramétrica arbitrária fora da distribuição observada.**

Ficam proibidos sem nova decisão:

- extrapolação logarítmica ad hoc;
- fator 8;
- pisos artificiais;
- tetos inventados.

Para rendas muito altas:

- evitar falsa precisão;
- considerar limitar a apresentação;
- indicar quando o usuário está acima da faixa em que o dataset oferece boa resolução.

A Fase 1C registrou, para a construção validada:

```text
IBGE_RDPC_P99_5_OBSERVED_2025 = 20507.98
IBGE_RDPC_P99_9_OBSERVED_2025 = 38991.66
IBGE_RDPC_MAX_OBSERVED_2025 = 200165.79
```

Esses valores são diagnósticos, não pisos, tetos ou pontos automáticos de truncamento. A exibição da cauda brasileira é regida por D071: não extrapolar acima do máximo observado, não exibir `TOP 0%` e reduzir a precisão visual na cauda. Não remover outliers automaticamente.

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

- preservar e verificar `PNADC_2025_visita1_20260508.zip` — **feito na Fase 1C**;
- registrar checksum da edição `20260508` — **feito na Fase 1C**;
- validar a construção `VD4019 × CO1 + VD4048 × CO1e` no arquivo real — **feito na Fase 1C**;
- validar `V1032` no arquivo real — **feito na Fase 1C**;
- confirmar tratamento dos blanks estruturais dos componentes — **feito na Fase 1C**;
- confirmar domínio de renda zero — **feito na Fase 1C**;
- confirmar valores negativos e extremos — **feito na Fase 1C; exibição da cauda Brasil canonizada por D071**;
- confirmar regra operacional do deflator — **feito na Fase 1C e canonizado na Fase 1C-R**;
- definir alinhamento da renda do usuário com preços médios de 2025 — **feito e canonizado por D065**;
- documentar o procedimento de CDF/empates — **feito; resíduos de R$ 1 em P90/P99 permanecem documentados sem ajuste artificial**;
- reproduzir indicadores oficiais do IBGE — **feito na Fase 1C, com resíduos documentados**;
- gerar CDF brasileira — **feito; CDF materializada com SHA-256 protegido e integração autorizada pelo manifesto de motor; futuras regenerações não podem substituir silenciosamente o artefato canônico**;
- validar percentis brasileiros — **feito com golden cases**;
- definir precisão visual Brasil — **feito por D071**;
- congelar versão PIP — **feito por D066**;
- definir ano mundial — **feito por D066: 2024**;
- definir tratamento de nowcast — **feito por D066: anos posteriores a 2024 não entram automaticamente**;
- validar PPP utilizada — **feito e canonizado por D069**;
- validar conversão BRL → PPP — **feito e canonizado por D069; fator IPCA Mundo materializado em artefato versionado**;
- construir CDF/representação mundial — **contrato definido por D068; artefato de produção posteriormente materializado e integração habilitada pelo manifesto agregador**;
- reproduzir headcounts em múltiplas linhas na mesma release PIP — **contrato definido por D068; o HEAD versionado preserva o limite operacional de erro, enquanto a evidência detalhada de execução permanece fora do HEAD**;
- definir limites, empates e precisão do Mundo — **feito por D070**;
- gerar manifestos/checksums de produção — **Brasil e Mundo materializados; manifesto agregador Mundo autorizado para integração, com CDF e price alignment históricos preservados**;
- executar testes de regressão metodológicos — **Brasil definido; contrato D070 referenciado pelo manifesto Mundo e pacote/runtime integrado com regressões próprias**.

## Validações Formais Executadas Na Fase 1C

```text
BR-VAL-001 — domínio real de VD5011: passou com ressalva; variável inadequada como construção principal
BR-VAL-002 — missing de VD5011: passou
BR-VAL-003 — integridade de V1032: passou
BR-VAL-004 — RDPC negativos: passou; nenhuma ocorrência
BR-VAL-005 — zeros: passou
BR-VAL-006 — máximo e extremos: passou com ressalva sobre exibição futura
BR-VAL-007 — regra operacional do deflator: passou com ressalva e levou à construção por componentes
BR-VAL-008 — VD5011 reproduzir R$ 2.264: falhou; construção por componentes reproduziu
BR-VAL-009 — população ponderada: passou
BR-VAL-010 — agregados com VD5011: falhou; construção por componentes reproduziu os benchmarks
```

As evidências completas permanecem em `docs/research/fase-1c-inspecao-microdados-pnad-2025.md`. Esses resultados não autorizam por si só pipeline, dataset derivado ou CDF.

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

> Utilizamos dados da PNAD Contínua do IBGE e comparamos pessoas segundo a renda por morador do domicílio, dentro da população considerada pela metodologia oficial.

A explicação completa deve esclarecer que adultos, crianças e pessoas sem renda própria entram quando elegíveis, enquanto condições domiciliares específicas são excluídas pelo indicador adotado.

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
