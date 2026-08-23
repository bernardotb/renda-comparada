---
title: Fase 2A — Metodologia Mundial
created: 2026-08-14T16:15:00-03:00
status: pesquisa em andamento — canonização parcial D066/D067 — revisão 0.5
canonical: false
---

# Fase 2A — Metodologia Mundial

> **RELATÓRIO DE PESQUISA — NÃO CANÔNICO.**
> Este documento organiza as evidências e a proposta metodológica para a comparação mundial da V1.
> Ele não altera `docs/04-metodologia-dados.md`, `docs/decisoes.md`, datasets de produção ou o frontend.

## 1. Resumo executivo

A comparação mundial não deve ser tratada como uma extensão direta da distribuição brasileira.

O Brasil utiliza uma distribuição reconstruída diretamente dos microdados da PNAD Contínua 2025. O Mundo, por sua vez, depende da arquitetura do **World Bank — Poverty and Inequality Platform (PIP)**, que combina pesquisas domiciliares de países diferentes, algumas baseadas em renda e outras em consumo, alinhadas a um ano de referência e expressas em dólares internacionais de PPP/PPC de 2021 por pessoa por dia.

### Evidências já suficientemente fortes

1. **Fonte mundial:** World Bank — Poverty and Inequality Platform (PIP).
2. **PPP vigente:** PPPs de 2021.
3. **Versão pesquisada:** `20260324_2021`; a interface atual do PIP identifica a produção como `20260324_2021_01_02_PROD`.
4. **Ano global recomendado para congelamento da V1:** **2024**.
   - O PIP declara que estimativas posteriores a 2024 são *nowcasts*.
   - Portanto, 2024 é o ano mais recente da versão atual que não deve ser rotulado como nowcast.
5. **Unidade internacional:** dólares internacionais de PPP 2021 por pessoa por dia.
6. **Agregado de bem-estar:** renda **ou** consumo domiciliar per capita, conforme a fonte utilizada pelo PIP em cada país.
7. **Interpretação:** o resultado mundial deve ser apresentado como uma **posição monetária global estimada**, e não como um ranking homogêneo de renda bruta mundial.
8. **Fonte candidata para construir a CDF global:** `1000 Binned Global Distribution`, atualizada com a vintage PIP de março de 2026.

### Pendências bloqueadoras

Ainda não devem ser canonizados:

1. o fator numérico exato para transformar BRL corrente em dólares internacionais PPP 2021 de maneira compatível com o PIP;
2. a série de inflação/CPI exata a ser usada na ponte Brasil atual → preços de 2021 para o cálculo mundial;
3. o erro introduzido pela distribuição em 1.000 faixas;
4. o tratamento exato das caudas;
5. os golden cases mundiais;
6. a precisão e microcopy da exibição.

---

## 2. Versão PIP

A página oficial do PIP informa como versão disponível baseada em PPPs de 2021:

```text
PIP_VERSION_CITATION = 20260324_2021
```

As páginas atuais de país e do calculador identificam a versão de produção como:

```text
PIP_PRODUCTION_VERSION = 20260324_2021_01_02_PROD
```

### Proposta

Congelar explicitamente essa versão para a V1.

Não consultar silenciosamente uma versão posterior em produção.

---

## 3. Ano global de referência

A página principal do PIP informa:

> estimativas posteriores a 2024 são nowcasts.

A base de distribuição em 1.000 faixas contém anos até 2026, mas isso não torna 2025 e 2026 observações equivalentes a 2024.

### Proposta metodológica

```text
GLOBAL_REFERENCE_YEAR = 2024
GLOBAL_ESTIMATION_TYPE = reference-year estimate / lineup, não nowcast
```

### Motivo

A V1 deve preferir um ano ligeiramente menos recente, mas metodologicamente mais sólido, a apresentar um nowcast como se fosse observação equivalente.

---

## 4. Conceito de bem-estar

O PIP não contém uma distribuição mundial homogênea de “salários” ou “renda bruta”.

As pesquisas nacionais utilizam:

- consumo domiciliar per capita, quando essa é a medida adotada;
- renda domiciliar per capita, quando consumo não está disponível ou não é a medida utilizada.

O Banco Mundial explicita que, para agregações globais e regionais, em princípio prefere consumo per capita quando disponível e renda quando consumo não está disponível.

### Consequência para a interface

Não escrever:

> “Sua renda é maior que a renda de X% da população mundial.”

Preferir algo conceitualmente equivalente a:

> **“Seu poder econômico por pessoa está aproximadamente acima do nível observado para X% da distribuição monetária global utilizada pelo Banco Mundial.”**

A redação final pertence à etapa de UX.

---

## 5. PPP/PPC

A comparação deve usar **Purchasing Power Parity / Paridade do Poder de Compra**, e não câmbio comercial.

A arquitetura metodológica do PIP leva os agregados monetários nacionais a:

```text
moeda local no período da pesquisa
↓
correção temporal por índice de preços
↓
moeda local em preços do ano-base PPP
↓
PPP de consumo
↓
dólares internacionais PPP 2021
```

Para o Renda Comparada, o problema equivalente é transformar a renda informada pelo usuário em uma unidade comparável com a distribuição mundial.

### Regra que ainda NÃO está aprovada

Não reutilizar as constantes antigas do `src/App.tsx`.

Em particular, nenhuma das seguintes constantes deve ser considerada canônica apenas por já existir no protótipo:

```text
PPP_2021_BRL
BRAZIL_CPI_2024
BRL_PER_INTL_2024
```

O fator deverá ser obtido de fonte oficial e validado numericamente.

---

## 6. Fonte candidata para a distribuição mundial

O World Bank Data Catalog publica:

> **1000 Binned Global Distribution**

Atualização:

```text
March 2026 PIP vintage
```

Cobertura:

```text
1990–2026
218 economias
1000 faixas por economia/ano
```

Variáveis principais:

```text
code
region
regionpcn
quantile
welf
pop
```

onde:

- `quantile` varia de 1 a 1000;
- `welf` é o bem-estar domiciliar per capita médio diário da faixa, em dólares PPP 2021;
- `pop` é a população representada pela faixa, em milhões.

### Vantagem

É muito superior ao vetor manual de aproximadamente 25 pontos presente no protótipo.

Permite construir uma distribuição global ponderada usando uma fonte oficial e versionada.

### Limitação crítica

O próprio Banco Mundial alerta que a base em faixas:

- não substitui os microdados ou as estatísticas calculadas diretamente pelo PIP;
- perde a desigualdade existente dentro de cada faixa;
- tende, por isso, a reduzir medidas de desigualdade dentro dos países.

Portanto:

> **a base de 1.000 faixas é candidata à CDF, não automaticamente a CDF canônica.**

---

## 7. Proposta de construção da CDF global

Para o ano 2024:

```text
filtrar year = 2024
↓
obter todas as faixas válidas das economias
↓
ordenar globalmente por welf
↓
usar pop como peso
↓
acumular população
↓
construir CDF global
```

Conceitualmente:

```text
W_total = soma(pop)

shareBelow(x)
= soma(pop das faixas com welf < x) / W_total

shareAtOrBelow(x)
= soma(pop das faixas com welf <= x) / W_total
```

Essa é apenas a primeira aproximação operacional.

Antes de canonizar, deve ser testada contra o PIP.

---

## 8. Validação obrigatória da distribuição candidata

A CDF derivada da base de 1.000 faixas deve reproduzir, dentro de tolerância previamente definida, os agregados globais oficiais do PIP.

Primeiros checkpoints:

```text
$ 3,00 / pessoa / dia
$ 4,20 / pessoa / dia
$ 8,30 / pessoa / dia
```

Também devem ser testadas linhas arbitrárias adicionais.

### Critério

Se o erro da distribuição em faixas for material para a experiência de percentil:

> rejeitar a base como mecanismo principal.

Não “corrigir” manualmente pontos individuais para fazê-los coincidir.

---

## 9. Conversão da entrada brasileira para PPP 2021

Este é o principal bloqueador restante.

A transformação conceitual deverá ter a forma:

```text
renda nominal brasileira atual
↓
renda brasileira em preços compatíveis com 2021
↓
divisão pelo fator PPP de consumo brasileiro de 2021
↓
dólares internacionais PPP 2021 por mês
↓
conversão para valor diário
```

Para mensal → diário:

```text
valor_diário = valor_mensal × 12 / 365
```

### Pendência

É necessário identificar e congelar:

```text
BRAZIL_2021_CONSUMPTION_PPP = [CONFIRMAR EXATAMENTE]
WORLD_USER_CPI_SOURCE = PIP aux / cpi [FONTE CONFIRMADA; RESPOSTA NUMÉRICA PENDENTE]
WORLD_USER_CPI_2021_REFERENCE = [PENDENTE DE INSPEÇÃO DA TABELA cpi]
WORLD_USER_CURRENT_PRICE_REFERENCE = [PENDENTE DE DEFINIÇÃO APÓS INSPEÇÃO DA FREQUÊNCIA/COBERTURA DO cpi]
```

O WDI possui o indicador:

```text
PA.NUS.PRVT.PP
PPP conversion factor, households and NPISHs final consumption expenditure
```

mas o valor exato utilizado pelo pipeline deve ser obtido e registrado sem depender de valor arredondado exibido em página.

---

## 10. Relação com D065

D065 resolve o problema:

```text
renda brasileira corrente
→
preços médios de 2025
→
CDF brasileira 2025
```

Isso não resolve automaticamente o cálculo mundial.

Não devemos assumir que:

```text
renda_2025
÷
alguma PPP anual
```

é equivalente ao procedimento PIP sem validação.

Brasil e Mundo devem possuir transformações monetárias explicitamente separadas, mesmo partindo da mesma entrada nominal.

---

## 11. Precisão da linguagem

### Brasil

A base é reconstruída diretamente da PNAD 2025 e possui CDF empírica validada.

### Mundo

A comparação combina:

- renda e consumo;
- pesquisas de anos distintos;
- alinhamento temporal;
- PPP;
- população;
- interpolações/extrapolações;
- eventualmente representação em faixas.

Portanto:

> **o resultado Mundo deve carregar grau de aproximação maior que o Brasil.**

O design não deve sugerir simetria metodológica apenas porque os dois resultados aparecem lado a lado.

---

## 12. Fontes oficiais consultadas

### Poverty and Inequality Platform — About

https://pip.worldbank.org/about

Uso:

- versão PIP;
- governança;
- natureza das fontes.

### Poverty and Inequality Platform — Home

https://pip.worldbank.org/home

Uso:

- versão de produção;
- PPP 2021;
- indicação de que estimativas posteriores a 2024 são nowcasts.

### PIP — Brasil

https://pip.worldbank.org/country-profiles/BRA

Uso:

- versão de produção;
- referência 2024 para os indicadores mais recentes do Brasil.

### World Bank Data Catalog — 1000 Binned Global Distribution

https://datacatalog.worldbank.org/search/dataset/0064304/1000-binned-global-distribution

Arquivo CSV da vintage congelada identificado no catálogo:

```text
https://datacatalogfiles.worldbank.org/ddh-published/0064304/DR0094423/GlobalDist1000bins_1990_2026_20260324_2021_01_02_PROD.csv
```

Tamanho publicado: aproximadamente 948,8 MB. Para validação da V1, preferir API/filtragem por 2024 ou leitura em streaming; não é necessário carregar todos os anos em memória.

Uso:

- distribuição em 1.000 faixas;
- unidade `welf`;
- peso `pop`;
- cobertura temporal;
- vintage;
- limitações.

### World Bank — ICP 2021

https://www.worldbank.org/en/programs/icp/data

Uso:

- PPP 2021;
- metodologia e referência do ICP.

### WDI — PPP de consumo privado

https://data.worldbank.org/indicator/PA.NUS.PRVT.PP?locations=BR

Uso:

- indicador candidato para o fator PPP brasileiro.

---

## 13. Canonização parcial

Após a revisão das fontes oficiais, duas decisões independentes da CDF e do fator PPP numérico foram canonizadas em 14/08/2026:

```text
D066 — Versão PIP e ano mundial de referência
       PIP_VERSION = 20260324_2021
       PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
       GLOBAL_REFERENCE_YEAR = 2024
       GLOBAL_ESTIMATION_TYPE = reference-year aggregate; não nowcast

D067 — Conceito e linguagem da comparação mundial
       posição monetária global estimada
       renda ou consumo domiciliar per capita
       PPP/PPC 2021
```

Continuam futuras:

```text
D068 — Fonte e construção da CDF mundial
D069 — Conversão BRL corrente → PPP 2021
D070 — Empates, caudas e arredondamento mundial
```

A canonização parcial não autoriza integração do resultado Mundo.

---

## 14. Próximos passos da Fase 2A

1. obter via fonte oficial o valor exato da PPP de consumo do Brasil em 2021;
2. determinar a série CPI coerente com a transformação do PIP;
3. acessar a base `1000 Binned Global Distribution` filtrada para 2024;
4. construir CDF experimental;
5. reproduzir os headcounts globais oficiais em $3,00, $4,20 e $8,30;
6. medir erro em linhas adicionais;
7. testar extremos e empates;
8. criar golden cases;
9. somente então propor canonização.

---

## 15. Estado da fase

```text
VERSÃO PIP.................. CANONIZADA — D066
PPP 2021.................... CANONIZADA CONCEITUALMENTE — D066/D067
ANO 2024.................... CANONIZADO — D066
CONCEITO RENDA/CONSUMO...... CANONIZADO — D067
CPI PIP (fonte/metodologia). CONFIRMADO
1000-BIN COMO FONTE......... CANDIDATA OPERACIONAL PRINCIPAL
POPshare GLOBAL............. REJEITADO PELO WRAPPER OFICIAL
CDF GLOBAL.................. PENDENTE — futura D068
PPP BRASIL 2021 EXATA....... PENDENTE — futura D069
ALINHAMENTO ENTRADA→2021.... PENDENTE — futura D069
GOLDEN CASES................ PENDENTE — futura D070
INTEGRAÇÃO FRONTEND......... BLOQUEADA
```


---

## 16. Revisão 0.2 — CPI oficial do PIP

### CONFIRMADO

A metodologia oficial do PIP estabelece que:

1. a fonte primária de inflação é a série mensal de **Consumer Price Index do IMF International Financial Statistics (IFS)**;
2. o CPI anual é a **média aritmética simples dos 12 índices mensais** do ano-calendário;
3. quando IFS não está disponível, o PIP pode recorrer ao IMF WEO, institutos nacionais de estatística e outras fontes;
4. as séries de CPI são **rebaseadas ao ano de referência do ICP, atualmente 2021**;
5. depois de colocar o agregado de bem-estar em moeda local a preços de 2021, o PIP aplica a **PPP de consumo de 2021**.

Fonte primária metodológica: repositório oficial `worldbank/PIP-Methodology`, documento `03-Converting-welfare-aggregates.Rmd`.

### Consequência

A cadeia mundial não deve reutilizar automaticamente o IPCA nacional aprovado em D065. D065 continua correto para alinhar a entrada com a CDF brasileira em preços médios de 2025. Para a comparação mundial, a cadeia canônica futura deve seguir o CPI/PPP do PIP ou demonstrar numericamente a equivalência de qualquer substituto brasileiro.

Portanto, neste estágio:

```text
BRAZIL_INPUT_PRICE_ALIGNMENT = IPCA nacional → preços médios de 2025
WORLD_INPUT_PRICE_ALIGNMENT  = CPI compatível com PIP → preços de 2021
```

São cadeias diferentes partindo da mesma renda nominal digitada.

---

## 17. Revisão 0.2 — PPP de consumo

### CONFIRMADO

O PIP informa que as PPPs usadas na medição global de pobreza são, em regra, as **PPPs de consumo do ICP**. A metodologia registra exceções específicas para alguns países; o Brasil não aparece na lista de exceções documentadas no capítulo de conversão consultado.

Assim, para o Brasil, a hipótese operacional forte é:

```text
PPP_BRAZIL_2021 = PPP de consumo ICP 2021 usada pela versão PIP congelada
```

### AINDA NÃO CANONIZAR O VALOR NUMÉRICO

O antigo protótipo contém `PPP_2021_BRL = 2.4499`, e páginas públicas do WDI arredondam a PPP de consumo brasileira de 2021 para aproximadamente `2,4`/`2,45`. Isso é compatível em ordem de grandeza, mas **não é evidência suficiente para promover 2,4499 a constante canônica da versão 20260324_2021**.

A fonte exata deve ser a tabela auxiliar `ppp` exposta pelo PIP/pipr ou outra saída oficial não arredondada da mesma vintage.

---

---

## 18. Revisão 0.5 — método operacional da distribuição mundial

### CONFIRMADO — `popshare` não existe no agregado mundial do wrapper oficial

A inspeção do wrapper oficial `worldbank/pip` corrigiu uma hipótese anterior deste relatório.

A ajuda de `pip cl` / `pip wb` define `popshare(#)` como opção exclusiva do subcomando de nível de país (`pip cl`). O próprio `pip_wb.ado` rejeita explicitamente a combinação `pip wb, popshare(...)`.

### Consequência

A estratégia anteriormente cogitada de obter diretamente P10, P50, P90 etc. do agregado mundial por `popshare` está **REJEITADA** para a V1.

Não enviar `popshare` manualmente ao endpoint agregado `pip-grp` como atalho não documentado.

---

## 19. Hierarquia revisada das alternativas para D068

### Alternativa A — 1000 Binned Global Distribution

**Status:** `CANDIDATA OPERACIONAL PRINCIPAL`

Construção experimental:

```text
vintage PIP de março de 2026
↓
year = 2024
↓
todas as faixas válidas
↓
ordenar globalmente por welf
↓
usar pop como peso
↓
CDF acumulada
```

Vantagens:

- fonte oficial do Banco Mundial;
- mesma vintage PIP da V1;
- 1.000 faixas por economia/ano;
- reproduzível e versionável;
- permite lookup local sem consulta em tempo real.

Limitação:

- `welf` representa a média de bem-estar da faixa;
- a desigualdade interna à faixa não é preservada;
- portanto a CDF derivada não pode ser aceita sem erro medido.

### Validação obrigatória

Comparar a CDF experimental contra o agregado oficial `pip wb` / `pip-grp`, usando `povline` em uma grade definida antes de olhar os resultados.

Checkpoints mínimos:

```text
3.00
4.20
5.00
8.30
10.00
30.00
```

A tolerância só pode ser definida **depois** de medir o erro.

Se a aproximação alterar materialmente a posição exibida ao usuário, rejeitar a CDF por bins ou reduzir a precisão da interface de forma compatível com o erro medido.

### Alternativa B — reconstrução mais fina a partir de fontes oficiais

**Status:** `RESERVA METODOLÓGICA`

Só investigar se a base de 1.000 faixas falhar nos critérios de aceitação.

### Alternativa C — vetor `WORLD_CURVE` do protótipo

**Status:** `REJEITADA`

Não possui densidade, proveniência, versionamento e validação suficientes para produção.

---

## 20. Fonte operacional para validar a CDF

O wrapper oficial mostra que o agregado mundial utiliza:

```text
endpoint = pip-grp
group_by = wb
```

e aceita linhas monetárias por `povline`. O código também preserva `WLD` entre os agregados oficiais.

Portanto a validação deve seguir:

```text
CDF experimental em bins
        versus
PIP agregado oficial WLD em linhas monetárias idênticas
```

---

## 21. PPP e CPI — fonte preferencial

Permanece válida a conclusão das seções 16 e 17:

```text
PPP exata do Brasil → tabela auxiliar `ppp` da release PIP
CPI usado pelo PIP  → tabela auxiliar `cpi` da mesma release
```

O wrapper Stata monta tabelas auxiliares por:

```text
aux?table=<table>&version=<PIP_VERSION>&format=csv
```

e o cliente `pipr` expõe `get_ppp()` e `get_cpi()` como atalhos dessas tabelas.

A série WDI serve como conferência externa, não como substituição automática da vintage congelada.

---

## 22. Bloqueios numéricos remanescentes

```text
WORLD_PIP_BRA_PPP_2021_EXACT = [OBTER DA TABELA AUXILIAR PIP]
WORLD_PIP_BRA_CPI_SERIES      = [OBTER DA TABELA AUXILIAR PIP]
WORLD_BINNED_2024_ARTIFACT    = [OBTER DA FONTE OFICIAL]
WORLD_BINNED_ERROR_PROFILE    = [MEDIR CONTRA pip wb / povline]
```

Enquanto esses itens estiverem abertos:

- D066 e D067 permanecem ativas;
- D068–D070 não devem ser ativadas;
- nenhum golden case mundial é canônico;
- Mundo permanece bloqueado no frontend;
- `WORLD_CURVE`, `PPP_2021_BRL` e `BRAZIL_CPI_2024` do protótipo não podem retornar à produção.

---

## 23. Estado após revisão 0.5

```text
VERSÃO PIP.................. CANONIZADA — D066
ANO GLOBAL 2024............. CANONIZADO — D066
PPP BASE 2021............... CANONIZADA — D066
CONCEITO RENDA/CONSUMO...... CANONIZADO — D067
LINGUAGEM MUNDO............. CANONIZADA — D067
CPI PIP: fonte/método....... CONFIRMADO
PPP PIP: fonte/método....... CONFIRMADO
POPshare GLOBAL............. REJEITADO PELO WRAPPER OFICIAL
1000-BIN COMO FONTE......... CANDIDATA OPERACIONAL PRINCIPAL
VALIDAÇÃO pip wb / povline.. PENDENTE DE EXECUÇÃO
PPP BRASIL 2021 EXATA....... PENDENTE — futura D069
CPI BRASIL EXATO............ PENDENTE — futura D069
CDF GLOBAL.................. PENDENTE — futura D068
GOLDEN CASES................ PENDENTE — futura D070
INTEGRAÇÃO FRONTEND......... BLOQUEADA
```

## 24. Documentos operacionais derivados

A execução futura deve seguir:

- `fase-2a-api-reproducao.md`;
- `fase-2b-protocolo-validacao-cdf-mundo.md`;
- `fase-2c-protocolo-conversao-brl-ppp2021.md`.
