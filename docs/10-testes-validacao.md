---
title: 10-testes-validacao
created: 2026-08-12T17:52:04.000-03:00
modified: 2026-08-14T16:12:00.000-03:00
---

# 10-testes-validacao


# Testes e Validação — Renda Comparada

**Produto:** Renda Comparada  
**Documento:** `10-testes-validacao.md`  
**Status:** Canônico para qualidade, testes e validação  
**Versão:** 1.2
**Última revisão:** 14/08/2026

Documentos relacionados:

- `01-visao-produto.md`
    
- `02-prd-v1.md`
    
- `03-jornada-ux-v1.md`
    
- `04-metodologia-dados.md`
    
- `05-design-system.md`
    
- `06-privacidade-seguranca.md`
    
- `07-seo-analytics-crescimento.md`
    
- `08-roadmap-backlog.md`
    
- `09-fontes-referencias.md`

---

# 1. Função deste documento

Este documento define como o Renda Comparada deve ser testado e validado antes e depois de cada publicação.

Ele cobre:

- cálculos;
    
- metodologia;
    
- datasets;
    
- pipeline de dados;
    
- interface;
    
- formulários;
    
- resultados;
    
- compartilhamento;
    
- privacidade;
    
- segurança;
    
- analytics;
    
- SEO;
    
- acessibilidade;
    
- responsividade;
    
- performance;
    
- regressão;
    
- atualização de dados;
    
- deploy;
    
- monitoramento pós-publicação.

---

# 2. Princípio central

O Renda Comparada é uma ferramenta baseada em dados.

Por isso:

> # Um resultado bonito não é suficiente.

Precisamos validar:

```text
DADO
↓
TRANSFORMAÇÃO
↓
CÁLCULO
↓
INTERPRETAÇÃO
↓
INTERFACE
```

Cada camada deve estar correta.

---

# 3. Prioridade de qualidade

A ordem de prioridade é:

```text
CORREÇÃO ESTATÍSTICA
↓
PRIVACIDADE
↓
CORREÇÃO FUNCIONAL
↓
CLAREZA
↓
PERFORMANCE
↓
ESTÉTICA
```

Se houver conflito entre:

> publicar rapidamente;

e:

> saber se o resultado está correto;

prevalece:

> **não publicar até validar.**

---

# 4. Regra para valores esperados

Nenhum percentil deve ser transformado em valor de referência apenas porque:

> “a calculadora atual mostra isso.”

Antes de registrar:

```text
percentil esperado = X
```

é necessário confirmar:

- dataset;
    
- ano;
    
- variável de renda;
    
- peso;
    
- unidade estatística;
    
- referência de preços;
    
- tratamento de empates;
    
- versão metodológica.

---

# 5. Caso matemático básico

Entrada:

```text
Renda do domicílio = R$ 6.500
Moradores = 3
```

Resultado matemático obrigatório antes de qualquer alinhamento temporal:

```text
6500 / 3 = 2166,666666…
```

Apresentação monetária:

```text
R$ 2.166,67
```

Esse teste valida apenas a divisão por moradores. Ele não define sozinho o valor comparável com a CDF quando a renda digitada está em preços correntes.

---

# 6. Golden cases brasileiros já validados

A CDF brasileira 2025 e o alinhamento temporal canonizado por D065 permitem registrar fixtures brasileiras.

## Caso A — valor já expresso em preços médios de 2025

```text
renda_domiciliar_2025 = 6500
moradores = 3
RDPC_2025 = 2166.6666666667
shareBelow = 0.701561259093934
shareAtOrBelow = 0.701561259093934
topShare = 0.298438740906066
```

Esse caso testa diretamente a CDF e corresponde a aproximadamente **70,1561% abaixo** e **29,8439% no topo**.

## Caso B — renda nominal corrente com manifesto de julho/2026

Usando o manifesto canônico `brazil-price-alignment.json`, com:

```text
baseIndex = 7300.8416666666666667
currentIndex = 7657.73
priceIndexReferenceMonth = 2026-07
```

para renda corrente de R$ 6.500 e 3 moradores:

```text
renda_domiciliar_2025 = 6197.0676471139
RDPC_2025 = 2065.6892157046
shareBelow = 0.6866910622833815
shareAtOrBelow = 0.6866910622833815
topShare = 0.3133089377166185
```

Esse caso testa **alinhamento temporal + CDF**.

O contrato D070 referencia golden cases para o resultado mundial, e o runtime integrado calcula o resultado usando os artefatos Mundo autorizados. O conteúdo detalhado dos golden cases permanece fora do HEAD atual. Sua exibição depende do manifesto agregador autorizado e da validação local dos três artefatos runtime.

---


# 6A. Apresentação Brasileira — D071

Os testes de interface devem separar precisão interna de precisão visual.

## Caso A — golden case em preços médios de 2025

Entrada interna:

```text
shareBelow = 0.701561259093934
topShare = 0.298438740906066
```

Apresentação esperada:

```text
Percentil 70
TOP 30%
```

## Caso B — renda corrente R$ 6.500 / 3 com manifesto 2026-07

Entrada interna:

```text
shareBelow = 0.6866910622833815
topShare = 0.3133089377166185
```

Apresentação esperada:

```text
Percentil 69
TOP 31%
```

## Complementaridade visual

Para a faixa principal:

```text
percentil_exibido + top_exibido = 100
```

O código não deve arredondar ambos independentemente se isso puder produzir `99` ou `101` na soma visual.

## Cauda de 0,1% a 1%

Testar fixture sintética com:

```text
topShare = 0.006
```

Esperado:

```text
TOP 0,6%
Percentil 99,4
```

## Cauda abaixo de 0,1%

Testar fixture sintética com:

```text
topShare = 0.0005
```

Esperado conceitualmente:

```text
TOP < 0,1%
```

e nunca:

```text
TOP 0%
```

## Máximo observado

No RDPC máximo da CDF:

- `shareBelow < 1`;
- `shareAtOrBelow = 1`;
- a interface pode usar `TOP < 0,1%` conforme D071.

## Acima do máximo

Para RDPC estritamente acima do máximo:

- o lookup matemático pode retornar `shareBelow = 1`;
- a interface não mostra `TOP 0%`;
- deve informar que a renda supera o maior valor observado e que não há resolução para posição mais fina.

## Renda zero

Para `RDPC = 0`:

- `shareBelow = 0`;
- `shareAtOrBelow > 0`;
- não mostrar `TOP 100%` como headline;
- informar de forma neutra que zero é o menor nível observado e possui empates.

## Moeda

Quando exibida:

```text
2166.6666... → R$ 2.166,67
```

O arredondamento monetário de UI não pode voltar para as funções de domínio como input intermediário.

---

# 6B. Contrato De Produção Brasil

A integração brasileira deve ler os três artefatos explicitamente aprovados:

```text
data/production/brazil/brazil-income-cdf-2025.json
data/production/brazil/brazil-price-alignment.json
data/production/brazil/brazil-income-engine-manifest.json
```

O teste deve falhar se qualquer referência do manifesto de motor divergir.

Valores congelados:

```text
CDF_SHA256 = 5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5
CDF_SIZE_BYTES = 3955036
SOURCE_DATASET_SHA256 = 8A44A26C47F16BE54DE787D215145C60B82E33319F806A0F890411B799EDA469
PRICE_ALIGNMENT_SHA256 = 78A7F6E61C7327124743741F59F0F27715200AD1A17E9F712D34C6A5294F3948
```

Validar também:

```text
engine.status = CANONICAL_APPROVED_FOR_INTEGRATION
engine.decisionIds contém D063, D065, D071 e D072
engine.integration.brazilFrontendIntegrationAllowed = true
engine.integration.worldFrontendIntegrationAllowed = false
```

Esse campo pertence ao manifesto do motor Brasil e impede que ele autorize o Mundo por acidente. Ele não representa o estado global vigente: a autorização posterior do motor Mundo está exclusivamente em `data/production/world/world-income-engine-manifest.json`, cujo contrato exige `worldFrontendIntegrationAllowed = true`.

### Metadado histórico da CDF

A CDF imutável foi gerada antes de D065 e contém originalmente:

```text
frontendIntegrationAllowed = false
userIncomePriceAlignmentMethod = null
```

Isso não é erro do arquivo e **não deve ser corrigido modificando a CDF**, pois quebraria o SHA canônico.

O teste deve confirmar que o `brazil-income-engine-manifest.json` registra explicitamente esse estado histórico e o resolve por referência a D065, sem alterar a CDF.

### Regressões proibidas

Falhar se:

- a aplicação consumir a CDF sem o manifesto de alinhamento vigente;
- o código alterar o JSON da CDF para trocar o flag histórico;
- o SHA da CDF não corresponder ao valor congelado;
- o SHA do manifesto de preços não corresponder ao valor referenciado;
- houver fallback para `BRAZIL_THRESHOLDS`.

### Suíte Reproduzível Do Gate G0

O Gate G0 não conseguiu reconstruir de forma inequívoca a suíte histórica alegada como `21/21 PASS`: os 21 checks individuais e os relatórios originais não estavam no checkout nem nos objetos Git recuperáveis. A validação canônica atual é uma suíte nova e explícita de 44 checks, reproduzida por:

```powershell
python scripts/data/brazil/production_package.py --validate-only
```

Relatórios atuais:

```text
validation/brazil/brazil-production-package-validation.json
validation/brazil/brazil-production-package-validation.md
```

---


# 6C. Entrega Da CDF Brasil — D072

Validar que a CDF canônica:

```text
brazil-income-cdf-2025.json
```

não esteja embutida no bundle JavaScript inicial.

### Primeiro cálculo

Quando a CDF ainda não estiver carregada:

- o CTA pode entrar em estado de processamento real;
- o arquivo estático deve ser requisitado sem qualquer renda/moradores na URL ou parâmetros;
- o resultado só aparece depois da disponibilidade dos artefatos válidos.

### Cálculos seguintes

Depois da primeira carga na mesma sessão:

- reutilizar a CDF em memória;
- não refazer download desnecessariamente por cálculo;
- não criar delay visual artificial.

### Falha de rede/artefato

Simular:

- 404 da CDF;
- JSON inválido;
- manifesto ausente;
- SHA/referência incompatível em testes de build/integração.

Esperado:

> **estado de indisponibilidade; nenhum resultado numérico.**

Falhar o teste se o código recorrer a:

```text
BRAZIL_THRESHOLDS
PIP brasileiro antigo
média nacional
resultado anterior silenciosamente preservado
```

### Performance

O diagnóstico local de 14/08/2026 registrou:

```text
raw = 3955036 bytes
gzip -9 local = 1788882 bytes
JSON.parse local Node ≈ 18,25 ms
100k lookups ≈ 7,50 ms
```

Esses números servem como baseline diagnóstico e **não como SLA de mobile**.

Na aplicação publicada, medir separadamente:

- transferência real da CDF;
- compressão efetiva;
- parse em dispositivos representativos;
- tempo CTA → resultado;
- efeito em LCP/INP e demais métricas pertinentes.

---

# 7. Categorias de teste

A V1 deve possuir, no mínimo:

1. testes unitários;
    
2. testes de domínio;
    
3. testes estatísticos;
    
4. testes do pipeline;
    
5. testes de integração;
    
6. testes de interface;
    
7. testes end-to-end;
    
8. testes de privacidade;
    
9. testes de segurança;
    
10. testes de compartilhamento;
    
11. testes de analytics;
    
12. testes SEO;
    
13. testes de acessibilidade;
    
14. testes de performance;
    
15. testes de regressão;
    
16. testes manuais de lançamento.

---

# PARTE I — TESTES UNITÁRIOS

# 8. Objetivo

Testes unitários devem validar funções pequenas e determinísticas.

Exemplos conceituais:

```text
calculatePerCapitaIncome()
formatCurrencyBRL()
getBrazilPercentile()
getGlobalPercentile()
convertToPPP()
calculateTopPercent()
```

---

# 9. Regra

Uma função matemática de domínio não deve precisar montar a interface para ser testada.

Preferência:

```text
input
↓
pure function
↓
output
```

---

# 10. Teste de renda per capita

### Caso 1

```text
renda = 6500
moradores = 3
```

Esperado:

```text
2166.666666…
```

---

# 11. Teste de um morador

```text
renda = 5000
moradores = 1
```

Esperado:

```text
5000
```

---

# 12. Teste de quatro moradores

```text
renda = 10000
moradores = 4
```

Esperado:

```text
2500
```

---

# 13. Teste de renda zero

RDPC zero é metodologicamente válido. A aceitação de renda zero como entrada do formulário é uma política de UX separada; quando aceita, testar:

```text
renda = 0
moradores = 4
```

Esperado:

```text
0
```

O comportamento de percentil e apresentação para RDPC zero deve seguir D071, preservando empates e sem usar `TOP 100%` como headline.

---

# 14. Divisão por zero

Entrada:

```text
renda = 5000
moradores = 0
```

A função não deve produzir:

```text
Infinity
NaN
```

como resultado de usuário.

A validação deve impedir o cálculo.

---

# 15. Moradores negativos

Entrada:

```text
moradores = -2
```

Resultado:

> entrada inválida.

---

# 16. Moradores fracionados

Entrada:

```text
moradores = 2.5
```

Resultado:

> entrada inválida.

---

# 17. Renda negativa

Entrada:

```text
renda = -5000
```

Resultado:

> entrada inválida.

---

# 18. Valores muito altos

Testar valores como:

```text
R$ 1.000.000
R$ 10.000.000
R$ 100.000.000
```

Objetivo:

- evitar overflow;
    
- evitar quebra de formatação;
    
- evitar percentis impossíveis;
    
- aplicar corretamente regra de extremos.

---

# 19. Precisão numérica

Cálculos internos devem preservar precisão suficiente.

Arredondamento visual deve acontecer:

> **na apresentação**

e não prematuramente durante todas as etapas matemáticas.

---

# 20. TOP percentual

Se:

```text
percentil = 67.9
```

então:

```text
top = 32.1
```

Testar coerência:

```text
percentil + top ≈ 100
```

considerando arredondamento.

---

# PARTE II — FORMATAÇÃO

# 21. Moeda brasileira

Testar:

```text
6500
```

→

```text
R$ 6.500
```

ou formato final definido pelo design system.

---

# 22. Valores com centavos

Entrada:

```text
6500.50
```

Apresentação:

```text
R$ 6.500,50
```

quando centavos forem exibidos.

---

# 23. Colagem de moeda

Testar entrada colada como:

```text
R$ 6.500
```

```text
6.500
```

```text
6500
```

```text
6.500,00
```

O comportamento deve ser consistente.

---

# 24. Ponto e vírgula

Testar:

```text
6500,50
```

e:

```text
6500.50
```

A aplicação deve interpretar segundo as regras definidas para o campo.

---

# 25. Caracteres inválidos

Testar:

```text
abc
```

```text
R$ abc
```

```text
6x500
```

O sistema deve:

- rejeitar;
    
- ou sanitizar de forma previsível.

Nunca produzir resultado silenciosamente incorreto.

---

# PARTE III — DISTRIBUIÇÃO BRASILEIRA

# 26. Teste da CDF

A distribuição acumulada brasileira deve cumprir:

```text
0 <= CDF(x) <= 1
```

para qualquer `x`.

---

# 27. Monotonicidade

Se:

```text
x1 < x2
```

então obrigatoriamente:

```text
CDF(x1) <= CDF(x2)
```

Qualquer violação bloqueia o dataset.

---

# 28. Limite inferior

Para valor muito abaixo da distribuição:

```text
CDF(x) ≈ 0
```

---

# 29. Limite superior

Para valor acima de todas as observações:

```text
CDF(x) ≈ 1
```

com tratamento específico para extremos conforme metodologia.

---

# 30. Pesos

Validar:

- peso presente;
    
- peso numérico;
    
- peso dentro dos valores admitidos;
    
- soma dos pesos;
    
- ausência de tratamento acidental como peso 1.

---

# 31. Distribuição ponderada versus não ponderada

Criar teste específico que demonstre que:

```text
weighted_result != unweighted_result
```

quando a amostra real produzir diferença.

Objetivo:

> detectar caso alguém remova acidentalmente os pesos.

---

# 32. Média ponderada

Calcular:

```text
weighted_mean_rdpc
```

e comparar com estatística oficial compatível.

Definir tolerância somente depois da confirmação exata de:

- variável;
    
- população;
    
- período;
    
- tratamento.

---

# 33. Mediana

Calcular a mediana ponderada.

Guardar como indicador de regressão após validação inicial.

---

# 34. Percentis de controle

Depois da primeira distribuição validada, congelar valores de referência para:

```text
P10
P25
P50
P75
P90
P95
P99
```

Esses valores passam a integrar os testes de regressão.

---

# 35. Empates

Criar fixture artificial:

```text
1000 → peso 20
2000 → peso 50
3000 → peso 30
```

Para usuário com:

```text
2000
```

testar separadamente:

```text
share_below
```

e:

```text
share_at_or_below
```

A frase:

> “maior que”

deve usar a regra estabelecida em metodologia.

---

# 36. Unidade estatística

Criar teste que impeça regressão para distribuição por domicílios quando a distribuição correta for por pessoas.

Exemplo artificial:

### Domicílio A

```text
RDPC = 1000
moradores representados = 1
```

### Domicílio B

```text
RDPC = 5000
moradores representados = 5
```

A distribuição por pessoa não pode produzir o mesmo resultado de uma distribuição simples de dois domicílios.

---

# PARTE IV — PIPELINE PNAD

# 37. Download

Validar:

- arquivo encontrado;
    
- tamanho plausível;
    
- extensão correta;
    
- checksum;
    
- data;
    
- origem oficial.

---

# 38. Mudança silenciosa da fonte

Se o mesmo URL produzir arquivo com checksum diferente:

> marcar para revisão.

Não substituir automaticamente produção.

---

# 39. Dicionário

O pipeline deve validar que as variáveis configuradas existem.

Exemplo:

```text
IBGE_WORK_INCOME_VARIABLE
IBGE_WORK_DEFLATOR
IBGE_OTHER_INCOME_VARIABLE
IBGE_OTHER_INCOME_DEFLATOR
IBGE_HOUSEHOLD_ELIGIBLE_COMPONENTS
IBGE_WEIGHT_VARIABLE
```

Se uma delas desaparecer:

> falhar.

Não procurar automaticamente “uma variável parecida”.

---

# 40. Tipos das colunas

Validar:

- renda numérica;
    
- peso numérico;
    
- UF quando utilizada;
    
- identificadores necessários.

---

# 41. Missing values

Validar quantidade e tratamento de:

- `null`;
    
- `NA`;
    
- códigos especiais;
    
- não aplicável;
    
- ignorado.

Mudanças grandes entre versões devem gerar alerta.

---

# 42. Contagem dos registros

Registrar:

```text
raw_rows
valid_rows
excluded_rows
```

Comparar entre versões.

Variações muito grandes precisam ser explicadas.

---

# 43. Soma dos pesos

Registrar:

```text
total_weight
```

e comparar com ordem de grandeza populacional esperada.

---

# 44. Reprodutibilidade

Executar o pipeline duas vezes com:

- mesmos inputs;
    
- mesma versão;
    
- mesmo código.

Resultado esperado:

> dataset derivado idêntico.

Preferencialmente:

```text
checksum_run_1 == checksum_run_2
```

---

# PARTE V — INFLAÇÃO

# 45. Fator 1

Se:

```text
reference_date = user_date
```

esperado:

```text
inflation_factor = 1
```

---

# 46. Sentido da correção

Criar teste para impedir inversão.

Se preços aumentaram entre período A e B:

> um valor nominal antigo atualizado para B deve aumentar.

---

# 47. Fonte temporal

Validar:

- série;
    
- período inicial;
    
- período final;
    
- fator calculado.

---

# 48. Atualização do IPCA

A regra canônica é definida por D065. Nova observação oficial do IPCA deve gerar atualização controlada do manifesto de preços, nunca consulta dinâmica silenciosa por cálculo.

Validar a cada atualização:

- continuidade mensal da série SIDRA 1737 / variável 2266;
- valor positivo e finito;
- mês efetivamente oficial;
- `baseIndex` de 2025 imutável;
- recomputação de `factorBaseToCurrent` e `multiplierCurrentToBase`;
- ida e volta da transformação;
- invariância de ranking entre deflacionar a entrada e inflacionar thresholds para teste;
- regressão dos golden cases dependentes do mês;
- aprovação antes de publicação.

Uma nova observação não altera retrospectivamente a CDF 2025 nem deve ser projetada para mês ainda não publicado.

---

# PARTE VI — COMPARAÇÃO GLOBAL

# 49. Conversão temporal

Conforme D069:

```text
daily = monthly * 12 / 365
```

criar teste direto.

Exemplo:

```text
monthly = 3650
```

Então:

```text
daily = 120
```

aproximadamente.

---

# 50. PPP

Criar testes com valores artificiais simples.

Exemplo:

Se:

```text
PPP = 2 BRL por intl$
valor = R$ 200
```

esperado conceitualmente:

```text
100 intl$
```

Este exemplo artificial não substitui a fórmula canônica; o cálculo definitivo é regido por D069.

---

# 51. Não usar câmbio

Criar teste de arquitetura/configuração que evite regressão para:

```text
USD exchange rate
```

quando o cálculo exigido for PPP.

---

# 52. Versão PIP

A V1 deve conhecer explicitamente os valores canonizados por D066:

```text
PIP_VERSION = 20260324_2021
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
PPP_BASE = 2021
GLOBAL_REFERENCE_YEAR = 2024
```

Ausência ou divergência:

> falha de validação.

Não permitir fallback silencioso para versão mais nova.

---

# 53. Ano global e nowcast

Exigir:

```text
GLOBAL_REFERENCE_YEAR = 2024
```

e testar que a V1 não troca silenciosamente para:

```text
current_year
latest
2025
2026
```

enquanto D066 estiver ativa.

O manifesto deve distinguir explicitamente ano de referência de `nowcast`.

---

# 54. CDF global — fonte canônica D068 e trava de `popshare`

A fonte operacional canonizada por D068 é:

> **1000 Binned Global Distribution — March 2026 PIP vintage**

O teste deve falhar se uma implementação tentar obter quantis globais canônicos por:

```text
pip wb + popshare
/pip-grp + popshare
```

O wrapper oficial restringe `popshare` ao nível de país (`pip cl`) e rejeita sua combinação com `wb`.

O contrato de construção e validação deve:

1. filtrar `year = 2024`;
2. validar chaves e cobertura;
3. usar `welf` como valor monetário da faixa;
4. usar `pop` como peso;
5. ordenar globalmente por `welf`;
6. construir a CDF empírica em degraus, agrupando empates;
7. validar contra o agregado oficial `pip wb` por `povline`;
8. preservar `shareBelow`, `shareAtOrBelow` e `topShare = 1 - shareBelow`;
9. proibir interpolação, extrapolação e fallback legado;
10. medir o erro sem transformar a tolerância técnica em precisão visual de D070.

---

# 55. CDF global — propriedades e proibições

Qualquer representação derivada para produção deve cumprir:

```text
0 <= CDF_GLOBAL(x) <= 1
```

e monotonicidade obrigatória.

Também deve haver teste de regressão que falhe se o frontend reintroduzir:

```text
WORLD_CURVE
vetor manual antigo
interpolação logarítmica antiga
teto arbitrário 99,99%
```

Nenhum desses mecanismos pode funcionar como fallback.

---

# 56. Validação contra linhas monetárias PIP

Para a **mesma versão congelada**, obter do PIP os headcounts globais de 2024 em linhas oficiais e adicionais.

No mínimo:

```text
US$ 3,00 / pessoa / dia
US$ 4,20 / pessoa / dia
US$ 8,30 / pessoa / dia
```

e pelo menos três linhas adicionais não usadas na construção.

Então verificar:

```text
CDF_GLOBAL(poverty_line)
≈
PIP_HEADCOUNT_SAME_VERSION(poverty_line)
```

A comparação deve preservar:

- release `20260324`;
- PPP 2021;
- agregado mundial;
- ano 2024;
- convenção de `<` versus `<=`.

Não usar valor de outra vintage do WDI/PIP como golden case canônico.

O WDI pode funcionar apenas como sanity check auxiliar.

---

# 56A. Contrato validado D068 — 1.000 faixas

Validar a fonte operacional oficial:

> **1000 Binned Global Distribution — March 2026 PIP vintage**

Em toda reprodução ou futura materialização:

1. filtrar 2024;
2. ponderar por `pop`;
3. ordenar por `welf`;
4. agrupar empates e construir CDF empírica em degraus;
5. comparar com os headcounts oficiais da mesma vintage;
6. medir erro absoluto e relativo em múltiplas linhas;
7. medir erro nos quantis;
8. documentar o efeito da perda de desigualdade dentro das faixas;
9. reproduzir os hashes e os checks estruturais canonizados por D068.

Evidência de referência da canonização:

```text
sourceRows2024 = 218000
economies2024 = 218
uniqueWelfarePoints = 216790
totalPopulationMillions = 8141.808945
candidateSha256 = 56C53483744176A50090E16058A0CF4FC6221C83D1D80A60060B931110C54DC2
maxAbsoluteErrorPp = 0.022516991848920
```

O disclaimer oficial continua aplicável: a base binned perde desigualdade intrabin e não equivale às estatísticas calculadas diretamente pelo PIP. D068 aceita a construção com restrição de precisão; D070 usa o erro medido para limitar apresentação e caudas, sem converter a posição estimada em ranking individual exato.

---

# 56B. PPP/CPI exatos da versão PIP

D069 está ativa. Seu contrato de validação usa as tabelas auxiliares da build congelada:

```text
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
BRAZIL_PIP_PPP_2021 = 2.44986319541931
BRAZIL_PIP_CPI_2024_BASE_2021 = 1.192919586578344
BRL_PER_INTL_2024 = 2.92248979025310406149724542264 (derivado)
```

Raws de proveniência:

```text
data/raw/world/pip/20260324_2021/pip-20260324_2021_01_02_PROD-ppp.raw.csv
SHA-256 792476948DA84A005CC9C61C359CB586B42866F850F55973EF7BDC2693347EB6

data/raw/world/pip/20260324_2021/pip-20260324_2021_01_02_PROD-cpi.raw.csv
SHA-256 E2F558A28FBBD91F69EDB5FEF4BC10DED19F17D315090CB70031F2C993408ABE
```

Testar:

- hashes, schema e registros Brasil dos raws preservados;
- versão/build, ano global 2024 e base PPP 2021;
- positividade e finitude de PPP, CPI e fator combinado;
- fator combinado recalculado a partir dos dois fatores exatos, nunca como terceira constante independente;
- fórmula canônica `dailyPPP = (householdIncomeCurrent / residents) × (IPCA_AVG_2024 / IPCA_CURRENT) ÷ (PPP × CPI) × 12 / 365`;
- ausência de arredondamento intermediário;
- linearidade na renda e monotonicidade para entradas válidas;
- resultado zero para renda zero;
- proporcionalidade inversa pelo número de moradores;
- referência temporal Mundo de 2024 separada do alinhamento Brasil de D065;
- fórmula de ida e volta;
- comparação com ICP/WDI apenas como cross-check oficial.

Uma divergência entre PIP aux e ICP/WDI deve ser registrada, mas o cross-check não pode substituir o valor operacional observado no raw da build PIP congelada. Não inventar explicação causal.

Esses checks D069 não criam por si sós golden cases, política de caudas ou precisão visual. Esses contratos são definidos separadamente por D070.

---

# 56C. D070 — golden cases e fronteiras de apresentação

O manifesto Mundo versionado referencia o artefato de golden cases do contrato D070 por caminho, versão, SHA-256 e tamanho:

```text
validation/world/world-income-golden-cases-d070-candidate.json
SHA-256 6EA8FB10D9BCE16380E5F311EFA789AC22EEA44BEFF119C33C61B1B0578FF779
```

O teste versionado espera 11 golden cases. O conteúdo detalhado do artefato permanece fora do HEAD atual; portanto, essa contagem descreve o contrato esperado, não a presença dos 11 casos no repositório nem um resultado de execução. Golden cases não devem ser confundidos com testes executados.

Usar:

```text
topPercent = 100 × topShare
maxErrorPp = 0.022516991848920
```

Os testes de apresentação devem cobrir explicitamente:

1. `TOP > 1%`;
2. `TOP = 1%`;
3. `TOP` imediatamente abaixo de `1%`;
4. `TOP > 0,1%`;
5. `TOP = 0,1%`;
6. `TOP` imediatamente abaixo de `0,1%` sem margem suficiente para afirmar “menos de 0,1%”;
7. `topPercent + maxErrorPp < 0,1`, permitindo “menos de 0,1%”;
8. ausência de `TOP 0%`;
9. ausência de `TOP 100%` como headline;
10. valor acima do máximo sem extrapolação;
11. valor abaixo do mínimo sem extrapolação;
12. empate com `shareBelow < shareAtOrBelow`.

O manifesto versionado comprova o contrato D070, a referência ao artefato de golden cases, sua versão, SHA-256 e tamanho, mas não a contagem detalhada da regressão local. Os checks executados devem passar sem alterar os golden cases, a CDF, D068 ou D069.

O pacote operacional Mundo adiciona validações próprias de schema, hashes, tamanhos, referências cruzadas, monotonicidade, determinismo, falha fechada e runtime. A execução reproduzível é:

```text
python scripts/data/world/production_package.py
python -m unittest discover -s tests/data/world -p "test_*.py" -v
pnpm run test:frontend
```

Esses checks D070, isoladamente, não autorizaram publicação em `public/**` nem integração em `src/App.tsx`. A autorização e a integração posteriores são comprovadas pelo manifesto agregador do motor Mundo, pelo loader/runtime e pelos testes de contrato; integração continua sem equivaler a deploy.

---

# 56D. Erro Medido E Limite De Apresentação

O contrato versionado preserva o limite operacional `maxAbsoluteErrorPp = 0.022516991848920`, associado a D068. D070 utiliza esse limite no contrato de apresentação e caudas. Não existe plano B ativo, e esta seção não introduz nova tolerância.

Nunca usar:

> “parece perto o suficiente”

como critério.

---

# PARTE VII — DATASET DE PRODUÇÃO

# 57. Manifesto brasileiro

Validar presença de:

```text
source
source_year
release
processed_at
price_reference
income_variable
weight_variable
methodology_version
checksum
```

---

# 58. Manifesto mundial

Validar:

```text
source
pip_version
reference_year
ppp_basis
proveniência operacional PIP `aux/ppp` e `aux/cpi`
processed_at
methodology_version
checksum
```

---

# 59. Sem placeholders

Produção deve falhar se houver:

```text
[CONFIRMAR]
[DEFINIR]
TODO
TBD
```

em campos metodológicos obrigatórios.

---

# 60. Versão metodológica

Toda distribuição deve indicar:

```text
methodology_version
```

A aplicação deve conseguir mostrar/registrar qual versão está em uso.

---

# PARTE VIII — TESTES DE REGRESSÃO

# 61. Objetivo

Uma atualização futura não deve mudar resultados silenciosamente.

Depois da primeira validação, congelar fixtures.

---

# 62. Casos de renda

Criar conjunto cobrindo:

```text
muito baixa
baixa
mediana
média
alta
P90
P95
P99
extremamente alta
```

---

# 63. Diferentes tamanhos de família

Testar:

```text
1
2
3
4
5
6
8
10
```

moradores.

---

# 64. Fixtures canônicas

A parte brasileira possui golden cases derivados da CDF validada. Para a parte global, o manifesto Mundo versionado referencia o artefato de golden cases D070 por caminho, versão, SHA-256 e tamanho.

|Entrada|Referência da entrada|Moradores|RDPC comparável 2025|shareBelow BR|topShare BR|Global|
|---:|---|--:|--:|--:|--:|---|
|R$ 6.500|preços médios de 2025|3|R$ 2.166,6667|0,7015612591|0,2984387409|não aplicável a esta entrada Brasil|
|R$ 6.500|nominal corrente; manifesto 2026-07|3|R$ 2.065,6892|0,6866910623|0,3133089377|referência ao contrato D070 no manifesto; conteúdo detalhado fora do HEAD|

Nunca preencher a coluna global por estimativa manual. O documento deve referenciar somente o contrato D070 e os metadados versionados no manifesto Mundo; o conteúdo detalhado do artefato de golden cases permanece fora do HEAD. Esta regra de fixture não concede autorização; o frontend e o pacote Mundo vigentes dependem da autorização separada do manifesto agregador e de sua validação de integridade.

---

# 65. Comparação após mudança

Para cada atualização:

```text
old_result
vs
new_result
```

Gerar relatório.

---

# 66. Threshold de mudança

Definir após linha de base:

```text
allowed_delta
```

Mudanças maiores que o limite:

> exigem revisão humana.

---

# 67. Mudança legítima

Uma mudança pode ser aceita quando decorre de:

- nova PNAD;
    
- novos pesos;
    
- inflação;
    
- nova versão PIP;
    
- correção metodológica.

Mas deve ser explicada.

---

# PARTE IX — FORMULÁRIO E UX

# 68. Estado inicial

Validar:

- nenhum resultado fictício;
    
- campos vazios;
    
- CTA conforme regra;
    
- headline visível.

---

# 69. Campo de renda

Testar:

- digitação;
    
- backspace;
    
- seleção;
    
- colagem;
    
- mobile;
    
- valores longos.

---

# 70. Moradores

Testar:

```text
-
+
```

quando esse controle existir.

O botão `-` não deve permitir valor inferior ao mínimo.

---

# 71. Pressionar Enter

Se apropriado:

> Enter deve iniciar cálculo quando o formulário estiver válido.

---

# 72. Erros

Verificar:

- mensagem próxima ao campo;
    
- conteúdo compreensível;
    
- foco;
    
- leitor de tela;
    
- preservação dos outros valores.

---

# 73. Recalcular

Fluxo:

```text
calcular
↓
resultado
↓
simular outra renda
↓
alterar
↓
novo resultado
```

Sem necessidade de reload completo.

---

# 74. Resultado substituído

Novo cálculo deve substituir corretamente o resultado anterior.

Não misturar:

> Brasil do cálculo 1

com:

> Mundo do cálculo 2.

---

# PARTE X — RESULTADO

# 75. Coerência Brasil

Validar que:

- `shareBelow` corresponde à frase “acima de aproximadamente X em cada 100”;
- `topShare = 1 - shareBelow`;
- `TOP X%` é a leitura visual principal;
- o percentil/leitura estatística secundária é matematicamente coerente;
- nenhuma frase troca pessoas por famílias, salários ou patrimônio.

---

# 76. Coerência TOP

Se:

```text
percentile = 90
```

não exibir:

```text
Top 90%
```

O resultado intuitivo deve refletir aproximadamente:

```text
Top 10%
```

---

# 77. Percentil extremo inferior

Testar apresentação de:

```text
0%
0,1%
1%
```

---

# 78. Percentil extremo superior

Testar:

```text
99%
99,5%
99,9%
```

A UI não deve quebrar.

---

# 79. Arredondamento

Verificar casos próximos a limites:

```text
89,94
89,95
89,99
```

A regra de arredondamento deve ser única.

---

# 80. Fonte exibida

Metadados exibidos devem vir dos artefatos versionados.

Brasil deve permitir verificar:

- PNAD Contínua 2025;
- referência de preços médios de 2025;
- mês do IPCA usado por D065.

Mundo, já integrado, deve permitir verificar:

- PIP `20260324_2021`;
- ano global 2024;
- PPP 2021;
- indicação de posição global estimada.

Essa integração não equivale a publicação. Deploy e release continuam dependentes de gate e autorização específicos.

Teste:

> trocar fixture de metadados e confirmar que a UI atualiza a fonte sem texto hardcoded.

---

# 81. Renda × patrimônio

Verificar presença do aviso definido:

> **A comparação é baseada em renda, não em patrimônio.**

---

# PARTE XI — COMPARTILHAMENTO

# 82. Posição na jornada

Validar que o share aparece:

```text
resultado
↓
interpretação essencial
↓
share
↓
check-up
```

e nunca:

```text
resultado
↓
questionário obrigatório
↓
share
```

---

# 83. Share privado

Testar mensagem padrão.

Verificar ausência de:

- renda;
    
- moradores;
    
- renda per capita.

---

# 84. Share com posição

A posição só pode aparecer após ação explícita do usuário.

Testar que:

- a opção começa desativada;
- ativá-la altera apenas o texto/card visível;
- `share_mode = position` pode ser registrado sem o valor da posição;
- renda, moradores e renda per capita permanecem ausentes;
- a URL compartilhada continua genérica e não codifica o resultado.

Não considerar a simples visualização do resultado como consentimento para divulgar a posição.

---

# 85. WhatsApp

Testar:

- Android;
    
- iPhone quando possível;
    
- desktop;
    
- WhatsApp Web.

---

# 86. Copiar link

Após ação:

- clipboard contém URL válida;
    
- feedback “Link copiado” aparece;
    
- nenhum dado financeiro aparece na URL.

---

# 87. Web Share API

Testar:

- navegador suportado;
    
- navegador sem suporte;
    
- cancelamento pelo usuário;
    
- sucesso quando tecnicamente detectável.

---

# 88. Cancelar compartilhamento

Cancelar o share não deve:

- gerar erro;
    
- apagar resultado;
    
- navegar para tela errada.

---

# 89. Open Graph

Compartilhar URL padrão e verificar:

- imagem;
    
- título;
    
- descrição;
    
- URL;
    
- ausência de renda.

---

# PARTE XII — PRIVACIDADE

# 90. Teste sentinela de renda

Usar valor facilmente pesquisável:

```text
R$ 12.345.678
```

Moradores:

```text
7
```

Depois pesquisar em:

- Network;
    
- console;
    
- URL;
    
- localStorage;
    
- sessionStorage;
    
- cookies;
    
- logs;
    
- analytics;
    
- error tracking.

Resultado esperado:

> não existir fora do processamento necessário.

---

# 91. URL

Confirmar ausência de:

```text
renda=
income=
household=
percentile=
```

com dados individuais.

---

# 92. Reload

Depois de inserir renda:

> recarregar página.

Com política atual:

> valor não deve reaparecer por persistência automática.

---

# 93. LocalStorage

Inspecionar manualmente:

```text
localStorage
```

Resultado esperado:

> nenhuma renda.

---

# 94. SessionStorage

Mesmo teste.

---

# 95. Cookies

Nenhum cookie deve conter:

- renda;
    
- moradores;
    
- percentil;
    
- resultado.

---

# 96. Analytics

Inspecionar payloads dos eventos.

Esperado:

```text
calculation_completed
```

Parâmetros categóricos permitidos quando necessários:

```text
share_channel
share_mode
app_version
```

Sem:

```text
6500
3
2166.67
67.9
income_band
top_percent
```

ou faixas/equivalentes que revelem informação financeira.

Se Vercel Web Analytics for adotado, testar também `beforeSend` e confirmar que URL/query não carregam dados financeiros.

---

# 97. Error tracking

Forçar erro proposital.

Verificar que o relatório não contém:

- estado completo;
    
- renda;
    
- screenshot com formulário preenchido.

---

# PARTE XIII — SEGURANÇA

# 98. HTTPS

Produção deve redirecionar corretamente para:

```text
https://
```

---

# 99. Headers

Verificar headers definidos em:

`06-privacidade-seguranca.md`

incluindo quando aplicável:

```text
Content-Security-Policy
X-Content-Type-Options
Referrer-Policy
Permissions-Policy
Strict-Transport-Security
```

---

# 100. XSS

Testar entradas maliciosas em campos que aceitem texto futuramente.

Exemplo de fixture:

```html
<script>alert(1)</script>
```

O conteúdo nunca deve ser executado.

---

# 101. Secrets

Executar busca no repositório por padrões de:

- API keys;
    
- tokens;
    
- passwords;
    
- private keys.

---

# 102. Dependências

Antes do release:

- revisar dependências;
    
- vulnerabilidades conhecidas;
    
- pacotes obsoletos relevantes.

---

# PARTE XIV — ANALYTICS

# 103. Eventos únicos

Verificar que um clique não dispara:

```text
share_clicked
```

três vezes por acidente.

---

# 104. calculation_started

Não deve disparar:

> uma vez por tecla.

Definir gatilho consistente.

---

# 105. calculation_completed

Só disparar quando:

> resultado válido foi produzido.

Não disparar em:

- erro;
    
- input inválido;
    
- loading abortado.

---

# 106. result_viewed

Se for usado Intersection Observer ou equivalente:

> validar que o evento não dispara repetidamente sem intenção.

---

# 107. Analytics indisponível

Bloquear script de analytics.

Resultado esperado:

> calculadora continua funcionando.

---

# PARTE XV — SEO

# 108. Title

Verificar título definido no PRD.

---

# 109. Description

Verificar:

- presente;
    
- específica;
    
- sem dados de usuário.

---

# 110. H1

A página principal deve possuir hierarquia semântica coerente.

---

# 111. Canonical

Verificar URL canônica em produção.

---

# 112. Sitemap

Testar:

```text
/sitemap.xml
```

- status 200;
    
- XML válido;
    
- apenas URLs canônicas desejadas.

---

# 113. robots.txt

Testar:

```text
/robots.txt
```

- status 200;
    
- regras coerentes;
    
- sitemap quando apropriado.

---

# 114. Preview

Ambientes de preview não devem competir com produção.

Validar:

- `noindex`;
    
- proteção;
    
- ou estratégia adotada.

---

# 115. HTML sem JavaScript

Inspecionar HTML inicial/renderizado.

Conteúdo essencial de SEO deve existir segundo a arquitetura escolhida.

---

# 116. Open Graph

Testar:

```text
og:title
og:description
og:image
og:url
```

---

# 117. Structured data

Se implementado:

- sintaxe válida;
    
- conteúdo real;
    
- nenhum dado inventado.

---

# PARTE XVI — ACESSIBILIDADE

# 118. Teclado

Executar jornada inteira usando apenas teclado:

```text
abrir
↓
renda
↓
moradores
↓
calcular
↓
resultado
↓
share
```

---

# 119. Ordem de foco

A ordem deve seguir a ordem visual e lógica.

---

# 120. Focus visible

Todo elemento interativo precisa possuir foco perceptível.

---

# 121. Labels

Campos precisam possuir labels programáticos.

Placeholder não substitui label.

---

# 122. Erros acessíveis

Mensagens de erro devem ser associadas ao campo.

---

# 123. Gráficos

Toda visualização deve possuir alternativa textual.

O usuário não pode depender da posição do marcador para saber seu percentil.

---

# 124. Cor

Desativar mentalmente a distinção verde/azul.

Ainda deve ser possível entender:

- Brasil;
    
- Mundo;
    
- erro;
    
- estado.

---

# 125. Zoom

Testar em:

```text
200%
```

Sem:

- conteúdo cortado;
    
- sobreposição;
    
- botão inacessível.

---

# 126. Reduced motion

Ativar:

```text
prefers-reduced-motion
```

Verificar redução das animações.

---

# 127. Leitor de tela

Validar pelo menos jornada básica com ferramenta disponível.

Prioridade:

- campos;
    
- erros;
    
- resultado;
    
- share.

---

# PARTE XVII — RESPONSIVIDADE

# 128. Larguras mínimas

Testar pelo menos:

```text
320px
360px
390px
430px
768px
1024px
1280px+
```

---

# 129. Mobile

Validar especialmente:

- teclado monetário;
    
- campos;
    
- CTA;
    
- scroll para resultado;
    
- cards empilhados;
    
- compartilhamento.

---

# 130. Orientação

Testar:

- portrait;
    
- landscape.

---

# 131. Conteúdo extremo

Testar números como:

```text
99,9%
R$ 100.000.000,00
```

Sem overflow.

---

# PARTE XVIII — NAVEGADORES

# 132. Cobertura mínima

Testar versões modernas disponíveis de:

- Chrome;
    
- Safari;
    
- Edge;
    
- Firefox.

---

# 133. Mobile

Prioridade especial:

- Chrome Android;
    
- Safari iOS.

---

# 134. Web Share

Como suporte varia:

> sempre validar fallback.

---

# PARTE XIX — PERFORMANCE

# 135. Objetivos

A V1 deve buscar:

```text
LCP ≤ 2,5 s
INP ≤ 200 ms
CLS ≤ 0,1
```

como referência de boa experiência.

---

# 136. Primeira carga

Avaliar:

- JavaScript;
    
- CSS;
    
- fontes;
    
- imagens;
    
- datasets.

---

# 137. Dataset

O dataset enviado ao browser deve possuir tamanho compatível com experiência mobile.

Não enviar:

> microdados PNAD completos.

---

# 138. Cálculo

Percentil deve responder rapidamente.

Testar milhares de lookups locais.

Objetivo:

> cálculo individual praticamente instantâneo.

---

# 139. Fontes

Testar fallback tipográfico.

Página deve permanecer utilizável se webfont demorar ou falhar.

---

# 140. JavaScript desnecessário

Revisar bundles.

Remover dependências sem utilidade real.

---

# PARTE XX — TESTES END-TO-END

# 141. Fluxo E2E principal

Automatizar:

```text
abrir home
↓
preencher renda
↓
preencher moradores
↓
calcular
↓
resultado Brasil
↓
resultado Mundo
↓
share disponível
```

---

# 142. Fluxo inválido

```text
abrir
↓
renda vazia
↓
moradores válidos
↓
calcular
```

Esperado:

> erro adequado.

---

# 143. Fluxo recalcular

```text
calcular A
↓
resultado A
↓
editar renda
↓
calcular B
↓
resultado B
```

---

# 144. Fluxo metodologia

```text
resultado
↓
Como calculamos?
↓
/metodologia
```

ou disclosure equivalente.

---

# 145. Fluxo check-up

Na V1:

```text
resultado
↓
share
↓
convite opcional
```

Verificar que o convite não aparece antes de entregar o valor principal.

---

# PARTE XXI — TESTES DE CONTEÚDO

# 146. Unidade da frase

Se metodologia é por pessoas:

não exibir:

> **X% das famílias**

por acidente.

---

# 147. Renda versus riqueza

Pesquisar interface por usos de:

```text
rico
riqueza
patrimônio
```

Garantir que contexto seja conceitualmente correto.

---

# 148. Ano

Pesquisar por:

```text
2024
2025
2026
```

Garantir que nenhum ano antigo tenha ficado hardcoded indevidamente.

---

# 149. Fonte

Verificar que:

```text
Brasil → IBGE/PNAD
Mundo → World Bank/PIP
```

quando aplicável.

---

# 150. Precisão

Evitar frases absolutas como:

> “Você é mais rico exatamente que 67,93% dos brasileiros.”

Preferir linguagem definida pela metodologia.

---

# PARTE XXII — ATUALIZAÇÃO DE DADOS

# 151. Detectar nova versão

Quando nova PNAD/PIP surgir:

> não publicar imediatamente.

---

# 152. Pipeline de atualização

Executar:

```text
download
↓
checksum
↓
processamento
↓
validação
↓
regressão
↓
diff
↓
aprovação
```

---

# 153. Relatório de diferenças

Gerar tabela:

|Caso|Produção|Nova versão|Diferença|
|---|--:|--:|--:|
|P10|X|Y|Δ|
|P50|X|Y|Δ|
|P90|X|Y|Δ|
|P99|X|Y|Δ|

---

# 154. Casos de usuário

Também comparar fixtures:

|Renda|Pessoas|Percentil antigo|Novo|Δ|
|--:|--:|--:|--:|--:|

---

# 155. Mudança excessiva

Se uma renda comum mudar:

```text
Top 30%
```

para:

```text
Top 8%
```

sem explicação metodológica:

> bloquear atualização.

---

# PARTE XXIII — CI/CD

# 156. Pull request

Antes do merge:

- unit tests;
    
- lint;
    
- type check;
    
- regression tests;
    
- build.

---

# 157. Mudança metodológica

Se arquivos de:

- pipeline;
    
- distribuição;
    
- fórmula;
    
- conversão;

forem modificados:

> executar suíte estatística ampliada.

---

# 158. Mudança visual

Se apenas CSS mudar:

ainda executar:

- build;
    
- E2E principal;
    
- snapshots/visual checks quando existentes.

---

# 159. Mudança de privacidade

Alterações em:

- analytics;
    
- share;
    
- cookies;
    
- storage;
    
- logs;

exigem testes específicos de privacidade.

---

# 160. Preview

Toda alteração relevante deve possuir ambiente de preview quando infraestrutura permitir.

---

# 161. Produção

Deploy somente após:

```text
CI verde
+
preview validado
+
dados aprovados
```

---

# PARTE XXIV — SEVERIDADE DE BUGS

# 162. P0 — bloqueador

Exemplos:

- percentis incorretos;
    
- renda vazando;
    
- cálculo indisponível para todos;
    
- dataset errado;
    
- XSS grave;
    
- compartilhamento expondo renda.

Ação:

> não publicar ou retirar versão afetada.

---

# 163. P1 — crítico

Exemplos:

- resultado Mundo incorreto;
    
- mobile inutilizável;
    
- formulário falha em navegador majoritário;
    
- fonte/ano errado.

---

# 164. P2 — relevante

Exemplos:

- share secundário falha;
    
- layout quebrado em tamanho específico;
    
- texto confuso;
    
- evento analytics ausente.

---

# 165. P3 — menor

Exemplos:

- pequeno desalinhamento;
    
- detalhe visual;
    
- microcopy sem impacto funcional.

---

# PARTE XXV — TESTE MANUAL PRÉ-LANÇAMENTO

# 166. Calculadora

-  renda válida;
    
-  moradores válidos;
    
-  renda per capita correta;
    
-  Brasil correto;
    
-  Mundo correto;
    
-  novo cálculo funciona.

---

# 167. Metodologia

-  PNAD correta;
    
-  peso correto;
    
-  variável correta;
    
-  PIP correto;
    
-  PPP correta;
    
-  ano correto;
    
-  referência de preços correta.

---

# 168. Interface

-  headline;
    
-  formulário;
    
-  resultado;
    
-  Brasil;
    
-  Mundo;
    
-  gráfico;
    
-  fontes;
    
-  metodologia;
    
-  share;
    
-  ponte opcional.

---

# 169. Privacidade

-  renda não está na URL;
    
-  renda não está no analytics;
    
-  renda não está em cookies;
    
-  renda não está no storage;
    
-  renda não está no console;
    
-  renda não está nos logs;
    
-  share padrão não revela renda.

---

# 170. SEO

-  title;
    
-  description;
    
-  canonical;
    
-  Open Graph;
    
-  sitemap;
    
-  robots;
    
-  HTML indexável;
    
-  metodologia indexável.

---

# 171. Mobile

-  iPhone;
    
-  Android;
    
-  renda;
    
-  moradores;
    
-  teclado;
    
-  resultado;
    
-  share;
    
-  scroll;
    
-  nenhuma quebra de layout.

---

# 172. Acessibilidade

-  teclado;
    
-  foco;
    
-  labels;
    
-  contraste;
    
-  erros;
    
-  gráficos com texto;
    
-  reduced motion.

---

# 173. Performance

-  primeira carga;
    
-  bundle;
    
-  dataset;
    
-  Core Web Vitals;
    
-  cálculo instantâneo.

---

# PARTE XXVI — VALIDAÇÃO COM USUÁRIOS

# 174. Teste de usabilidade

Antes de ampla divulgação, realizar testes com usuários reais.

Não é necessário grande volume inicialmente.

Objetivo:

> identificar problemas óbvios de compreensão.

---

# 175. Tarefas

Pedir ao usuário:

> “Descubra onde uma família que ganha R$ X e possui Y moradores está.”

Observar sem explicar.

---

# 176. Perguntas depois do resultado

Perguntar:

> O que esse número significa para você?

> Você entende a diferença entre Percentil e Top X%?

> Você sabe de onde vieram os dados?

> Você compartilharia?

> O que acha que será compartilhado?

---

# 177. Teste de privacidade percebida

Perguntar:

> Você acha que o site guardou sua renda?

> Você acha que sua renda aparecerá se clicar em compartilhar?

Se houver confusão:

> melhorar UX.

---

# 178. Teste da palavra “rico”

Perguntar:

> O que você entende por “rico” nesta página?

Verificar se o aviso:

> renda ≠ patrimônio

é suficiente.

---

# 179. Teste da pergunta de moradores

Observar se o usuário inclui:

- filhos;
    
- pessoas sem renda.

Se muitos errarem:

> melhorar microcopy.

---

# PARTE XXVII — MONITORAMENTO PÓS-LANÇAMENTO

# 180. Primeiras horas

Após deploy relevante:

verificar:

- erros;
    
- analytics;
    
- cálculos;
    
- performance;
    
- share;
    
- logs técnicos.

---

# 181. Primeiros dias

Monitorar:

- taxa de erro;
    
- abandono;
    
- suporte;
    
- dúvidas metodológicas;
    
- compartilhamento;
    
- dispositivos problemáticos.

---

# 182. Reclamações sobre resultado

Se usuário disser:

> “Essa calculadora está errada.”

não assumir imediatamente:

> usuário está errado.

Registrar:

- input relatado;
    
- metodologia em produção;
    
- dataset;
    
- versão;
    
- resultado esperado;
    
- possível explicação.

---

# 183. Reprodução

Todo bug de cálculo deve ser reproduzível com:

```text
input
dataset_version
methodology_version
app_version
```

sem precisar identificar o usuário.

---

# PARTE XXVIII — GOLDEN DATASET

# 184. Dataset brasileiro de referência

A primeira CDF brasileira validada já possui conjunto de golden cases versionado em:

```text
validation/brazil/brazil-income-golden-cases.json
```

Ele deve permanecer pequeno, determinístico e derivado da mesma CDF cujo SHA-256 é registrado no manifesto.

O teste versionado espera 11 golden cases. O manifesto Mundo referencia o conjunto global D070 em `validation/world/world-income-golden-cases-d070-candidate.json`, versão `D070-v1`, SHA-256 `6EA8FB10D9BCE16380E5F311EFA789AC22EEA44BEFF119C33C61B1B0578FF779` e tamanho de 6.956 bytes; o conteúdo detalhado desse artefato permanece fora do HEAD atual.

---

# 185. Estrutura mínima dos casos

Para Brasil, os casos devem preservar ao menos:

```json
{
  "methodologyVersion": "1.0.0",
  "brazilDatasetVersion": "2025-20260508-v1",
  "cases": [
    {
      "name": "householdIncome6500Residents3",
      "rdpc": 2166.6666666667,
      "shareBelow": 0.701561259093934,
      "shareAtOrBelow": 0.701561259093934,
      "topShare": 0.298438740906066
    }
  ]
}
```

Casos que dependem de renda **corrente** devem registrar também a versão/mês do manifesto de preços utilizado. Os resultados globais canônicos alimentam o runtime integrado somente após validação do manifesto, hashes, tamanhos e referências cruzadas. Os golden cases permanecem restritos à regressão e não são publicados no caminho do navegador.

---

# 186. Golden cases não mudam silenciosamente

Se uma atualização alterar os casos:

> o diff precisa ser revisado.

Não atualizar snapshots automaticamente apenas para “fazer o teste passar”.

---

# PARTE XXIX — TESTES DE PROPRIEDADE

# 187. Monotonicidade da renda

Mantendo moradores fixos:

se:

```text
renda_A < renda_B
```

então:

```text
percentil_A <= percentil_B
```

Obrigatório.

---

# 188. Efeito de moradores

Mantendo renda familiar fixa:

se:

```text
moradores_A < moradores_B
```

então:

```text
RDPC_A > RDPC_B
```

e, consequentemente, o percentil não deveria aumentar ao adicionar moradores.

---

# 189. Limites

Percentis nunca podem ser:

```text
< 0
> 100
NaN
Infinity
```

---

# 190. Determinismo

Mesmo:

```text
input
+
dataset
+
methodology_version
```

deve sempre produzir:

> mesmo resultado.

---

# PARTE XXX — O QUE NÃO TESTAR COMO VERDADE

# 191. Não testar marketing como estatística

Não transformar slogans como:

> “rico”

em regra matemática independente.

---

# 192. Não testar média como corte

Não criar:

```text
if income > average:
  rich = true
```

---

# 193. Não testar números de matérias

Não copiar cortes de:

- jornais;
    
- blogs;
    
- redes sociais;

como fixtures.

Fixtures de cálculo devem vir do pipeline validado.

---

# 194. Não testar a implementação contra ela mesma

Evitar:

```text
expected = functionUnderTest(input)
actual = functionUnderTest(input)
```

Testes precisam possuir uma referência independente.

---

# PARTE XXXI — EVIDÊNCIAS DE VALIDAÇÃO

# 195. Registro de validação

Para cada release metodológica, gerar documento ou artefato com:

```text
methodology_version
dataset_version
tests_run
results
date
reviewer
```

---

# 196. Relatório de produção

Estrutura possível:

```text
validation/
  methodology-1.0.0.md
  brazil-2025.md
  global-pip-xxxx.md
```

---

# 197. Evidência

Registrar:

- indicadores reproduzidos;
    
- diferenças;
    
- tolerâncias;
    
- decisões;
    
- limitações.

---

# PARTE XXXII — DEFINITION OF DONE

# 198. Cálculo brasileiro pronto quando

-  PNAD identificada;
    
-  variável confirmada;
    
-  peso confirmado;
    
-  filtros confirmados;
    
-  CDF validada;
    
-  indicadores oficiais reproduzidos;
    
-  casos canônicos criados;
    
-  regressão automatizada.

---

# 199. Cálculo mundial pronto quando

-  versão PIP congelada;
    
-  ano global definido;
    
-  PPP definida;
    
-  conversão validada;
    
-  CDF validada;
    
-  sanity checks contra PIP aprovados;
    
-  casos canônicos criados.

---

# 200. Interface pronta quando

-  inputs funcionam;
    
-  erros funcionam;
    
-  resultado é claro;
    
-  share funciona;
    
-  mobile funciona;
    
-  acessibilidade básica aprovada;
    
-  conteúdo é coerente com metodologia.

---

# 201. Privacidade pronta quando

-  renda não persiste;
    
-  renda não está na URL;
    
-  renda não está no analytics;
    
-  renda não está nos logs;
    
-  renda não aparece no share padrão;
    
-  teste sentinela aprovado.

---

# 202. SEO pronto quando

-  title;
    
-  description;
    
-  canonical;
    
-  sitemap;
    
-  robots;
    
-  Open Graph;
    
-  conteúdo indexável;
    
-  ambientes não produtivos tratados.

---

# 203. V1 pronta quando

Todos os blocos críticos acima estiverem aprovados.

Não basta:

> “funciona no meu navegador”.

É necessário saber que:

> **o cálculo é correto, a interpretação é correta, a privacidade é preservada e a experiência funciona nos contextos principais.**

---

# 204. Regra para o Codex

Sempre que modificar código relacionado a:

### Matemática

Adicionar ou atualizar testes unitários.

### Distribuição

Executar regressão estatística.

### Dataset

Gerar diff de versões.

### Formulário

Atualizar testes de interação.

### Compartilhamento

Executar testes de privacidade.

### Analytics

Inspecionar payload.

### SEO

Validar metadata/renderização.

### Design

Verificar responsividade e acessibilidade.

---

# 205. Codex não deve “consertar” o teste alterando a referência

Quando um teste estatístico falhar:

> investigar primeiro o código ou a mudança do dataset.

Não alterar automaticamente:

```text
expected = novo_resultado
```

apenas para deixar o CI verde.

---

# 206. Quando atualizar um valor esperado

Somente quando houver justificativa documentada, como:

- nova edição da PNAD;
    
- nova versão PIP;
    
- correção metodológica;
    
- nova referência de preços.

Registrar a causa.

---

# 207. Regra de lançamento

Nenhuma release que altere percentis deve ser considerada “mudança pequena”.

Ela deve passar por:

```text
AUDITORIA
↓
TESTES
↓
DIFF
↓
APROVAÇÃO
↓
PRODUÇÃO
```

---

# 208. Norte de testes

O objetivo dos testes não é apenas impedir que o site quebre.

É impedir que o site:

> **continue funcionando perfeitamente enquanto mostra um número errado.**

---

# 209. Norte de validação

Para qualquer resultado do Renda Comparada, devemos conseguir responder:

> Qual input foi usado?

> Qual dataset?

> Qual versão?

> Qual metodologia?

> Qual transformação?

> Qual função produziu o resultado?

> Quais testes comprovam que essa cadeia está funcionando?

---

# 210. Regra final

> # Resultado financeiro sem teste não é resultado de produção.

> # Dataset sem validação não é dataset de produção.

> # Mudança estatística sem regressão não é mudança segura.

> # E um teste só é útil quando é capaz de falhar se estivermos errados.

O padrão de qualidade do Renda Comparada deve ser:

> **reproduzir → comparar → validar → publicar.**
