---
title: Fase 1A — Investigação Oficial PNAD Contínua 2025
created: 2026-08-13
status: pesquisa-concluida-aguardando-decisao
authority: investigacao-nao-canonica
---

# Fase 1A — Investigação Oficial PNAD Contínua 2025

> **Natureza deste documento:** relatório de investigação. Ele reúne evidências e recomendações, mas não altera nem substitui `docs/04-metodologia-dados.md` ou `docs/decisoes.md`.
>
> **Regra epistemológica:** `CONFIRMADO` significa afirmação direta de fonte oficial do IBGE; `INFERÊNCIA FORTE` combina evidências oficiais; `HIPÓTESE` ainda carece de comprovação; `PENDENTE` identifica lacuna; `DECISÃO DE PRODUTO/METODOLOGIA` exige aprovação na Fase 1B.

## 1. Resumo executivo

A investigação foi suficiente para identificar a edição, o arquivo anual, a visita, a estrutura de registros, o peso calibrado, a UF, os identificadores, as variáveis derivadas candidatas, a reponderação vigente, os deflatores disponíveis e benchmarks oficiais de 2025.

O achado mais importante é que o IBGE publica em 2025 pelo menos dois indicadores que podem parecer equivalentes, mas não são:

1. **R$ 2.264:** rendimento médio mensal **real** domiciliar per capita da publicação *Rendimento de todas as fontes 2025*, a preços médios de 2025. A distribuição oficial combina rendimento **habitual** do trabalho com rendimento **efetivo** de outras fontes, usa primeiras visitas e exclui pensionistas, empregados domésticos e parentes de empregados domésticos da composição e da população do indicador.
2. **R$ 2.316:** rendimento **nominal** mensal domiciliar per capita divulgado para a Lei Complementar 143/2013 e o FPE. Usa rendimentos brutos **efetivamente recebidos**, considera todos os moradores — inclusive aquelas três condições domiciliares — e também acumula primeiras visitas dos quatro trimestres de 2025.

Portanto, o valor de R$ 2.316 é **VALIDAÇÃO AUXILIAR**, não validação direta da distribuição recomendada preliminarmente para o produto.

`INFERÊNCIA FORTE` — Para reproduzir a distribuição publicada no SIDRA e no informativo de desigualdade, a melhor candidata é `VD5011`, com o peso calibrado `V1032`, no arquivo `PNADC_2025_visita1_20260508.zip`, formando uma distribuição de **pessoas elegíveis**, não de domicílios. Essa escolha ainda precisa ser aprovada na Fase 1B.

Permanecem pendentes: os códigos exatos de missing documentados no dicionário legado `.xls`; a regra operacional exata de junção e aplicação do deflator à variável mista `VD5011`; a confirmação por inspeção dos microdados de que não há valores negativos ou pesos inválidos; e as regras do produto para empates, caudas e atualização da renda corrente do usuário para preços de 2025.

## 2. Escopo e limitações

Esta fase foi limitada a fontes oficiais do IBGE e a arquivos técnicos pequenos. Não foram usados blogs, repositórios de terceiros, outras LLMs, Banco Mundial ou fontes externas para preencher lacunas.

Foram relidos os documentos internos obrigatórios. A lista inicial de perguntas brasileiras extraída deles foi:

- arquivo e versão da PNAD 2025;
- visita anual;
- variável de RDPC;
- peso amostral;
- UF e identificadores;
- unidade pessoa versus domicílio;
- população e condições domiciliares excluídas;
- missing e códigos especiais;
- renda zero e extremos;
- deflator e referência de preços;
- reponderação associada ao Censo 2022;
- benchmarks oficiais comparáveis.

Não foram baixados microdados integrais. Não foram construídos dataset, CDF, percentis, golden cases ou funções de cálculo. Os valores de percentis citados neste relatório são **valores publicados pelo SIDRA**, não resultados recalculados.

Limitação técnica: os arquivos oficiais `dicionario_...xls`, `Variaveis_PNADC_Anual_Visita.xls` e `deflator_PNADC_2025.xls` usam o formato binário legado `.xls`. Eles foram preservados temporariamente para inspeção, mas o leitor de planilhas disponível não conseguiu importá-los. O `input` oficial, as definições derivadas em PDF, as notas técnicas, o informativo e o SIDRA permitiram confirmar os pontos centrais. Detalhes que dependem exclusivamente das células desses `.xls` permaneceram `PENDENTE`.

## 3. Fontes oficiais consultadas

Foram consultados 18 conjuntos/documentos oficiais do IBGE, todos acessados em 13/08/2026:

1. página oficial da PNAD Contínua;
2. diretório FTP dos microdados anuais por visita;
3. histórico oficial de atualizações anuais;
4. `LEIA-ME.pdf` dos microdados anuais;
5. inventário de pesquisas suplementares anuais;
6. diretório da primeira visita de 2025;
7. `input_PNADC_2025_visita1_20260508.txt`;
8. dicionário da edição 2025;
9. definições das variáveis derivadas de rendimentos de outras fontes;
10. documento de chaves da PNAD Contínua;
11. documentação do deflator anual por visita;
12. arquivo de deflatores 2025;
13. Nota técnica 01/2025 sobre rendimentos de todas as fontes;
14. Nota técnica 02/2025 sobre reponderação;
15. informativo *Rendimento de todas as fontes 2025*;
16. tabelas SIDRA 7526, 7529, 7534 e 7564;
17. release oficial do RDPC nominal de R$ 2.316;
18. comunicado oficial sobre a reponderação em 2025.

O registro bibliográfico completo, com URLs, datas, páginas e finalidade, está na seção 31.

## 4. Edição oficial de 2025

`CONFIRMADO` — O produto estatístico é **Pesquisa Nacional por Amostra de Domicílios Contínua — Rendimento de todas as fontes 2025**.

`CONFIRMADO` — O informativo foi publicado pelo IBGE em 2026, ISBN 978-85-240-4707-7, e a divulgação ocorreu em 08/05/2026.

`CONFIRMADO` — O histórico oficial registra em 08/05/2026: “Atualização de microdados da PNAD Contínua Rendimento de Todas as Fontes 2025”.

`CONFIRMADO` — A versão atualmente localizada para a primeira visita é:

```text
PNADC_2025_visita1_20260508.zip
```

O diretório oficial informa data/hora `2026-05-08 10:00` e tamanho aproximado de `180 MB`.

`CONFIRMADO` — No mesmo diretório, dicionário e layout possuem o mesmo sufixo de versão `20260508`.

`INFERÊNCIA FORTE` — Não foi localizada uma segunda versão posterior do arquivo de rendimento de 2025. O histórico geral recebeu atualizações posteriores de outros temas, mas o arquivo de rendimento permaneceu identificado por `20260508` na consulta de 13/08/2026.

## 5. Inventário de arquivos

| Item | Arquivo oficial | Tipo | Ano | Atualização | Função | Fonte |
| --- | --- | --- | ---: | --- | --- | --- |
| Microdados | `PNADC_2025_visita1_20260508.zip` | ZIP, ~180 MB | 2025 | 08/05/2026 | Registros anuais acumulados de primeira visita | [FTP — Dados da visita 1](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Visita_1/Dados/) |
| Dicionário | `dicionario_PNADC_microdados_2025_visita1_20260508.xls` | XLS, 245 KB no índice | 2025 | 08/05/2026 | Códigos, rótulos, tipos e categorias | [FTP — Documentação da visita 1](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Visita_1/Documentacao/) |
| Layout | `input_PNADC_2025_visita1_20260508.txt` | TXT, 27 KB no índice | 2025 | 08/05/2026 | Posições, larguras, tipos e rótulos das variáveis | [arquivo oficial](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Visita_1/Documentacao/input_PNADC_2025_visita1_20260508.txt) |
| Lista geral | `Variaveis_PNADC_Anual_Visita.xls` | XLS, 293 KB no índice | série | 08/05/2026 | Inventário de variáveis por ano/visita | [documentação geral](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/) |
| Definições derivadas | `06_Definicao_variaveis_derivadas_parte05_Rendimento_de_outras_fontes.pdf` | PDF, 697 KB no índice | série | 12/06/2026 | Fórmulas de `VD5001` a `VD5012` e universo | [arquivo oficial](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/Definicao_variaveis_derivadas_PNADC/06_Definicao_variaveis_derivadas_parte05_Rendimento_de_outras_fontes.pdf) |
| Chaves | `Chaves_PNADC.pdf` | PDF, 108 KB no índice | série | 02/03/2020 | Chaves de domicílio e pessoa | [arquivo oficial](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/Chaves_PNADC.pdf) |
| Deflatores | `deflator_PNADC_2025.xls` | XLS, 233 KB no índice | 2025 | 08/05/2026 | Fatores CO1/CO1e, CO2/CO2e e CO3 | [arquivo oficial](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/deflator_PNADC_2025.xls) |
| Manual do deflator | `PNADcIBGE_Deflator_Anual_Visita.pdf` | PDF, 483 KB no índice | série | 07/02/2022 | Forma de uso dos fatores anuais | [arquivo oficial](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/PNADcIBGE_Deflator_Anual_Visita.pdf) |
| Estrutura anual | `PNADC_Pesquisas_Suplementares_Anuais_20260702.pdf` | PDF | até 2025 | 02/07/2026 | Relação tema, ano, visita e trimestre | [arquivo oficial](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/PNADC_Pesquisas_Suplementares_Anuais_20260702.pdf) |
| Leia-me | `LEIA-ME.pdf` | PDF | série | consultado em 13/08/2026 | Estrutura de pastas, visitas e projeções | [arquivo oficial](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/LEIA-ME.pdf) |
| Atualizações | `atualizacoes_divulgacao_anual_20260702.txt` | TXT | série | 02/07/2026 | Histórico de substituições e atualizações | [arquivo oficial](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/atualizacoes_divulgacao_anual_20260702.txt) |

### Downloads técnicos temporários

Os seguintes arquivos pequenos foram baixados somente para uma pasta temporária fora do repositório. Nenhum foi commitado:

| Arquivo | Tamanho local | Finalidade |
| --- | ---: | --- |
| `atualizacoes_divulgacao_anual_20260702.txt` | 12.213 bytes | confirmar histórico da edição |
| `LEIA-ME.pdf` | 335.785 bytes | entender estrutura anual e visitas |
| `PNADC_Pesquisas_Suplementares_Anuais_20260702.pdf` | 286.240 bytes | confirmar alocação do tema |
| `input_PNADC_2025_visita1_20260508.txt` | 27.691 bytes | confirmar variáveis e layout |
| `dicionario_PNADC_microdados_2025_visita1_20260508.xls` | 250.368 bytes | tentativa de leitura do dicionário |
| `Variaveis_PNADC_Anual_Visita.xls` | 300.032 bytes | tentativa de inventário cruzado |
| `01_Lista_de_variaveis_derivadas.xlsx` | 8.316 bytes | inventário das derivadas |
| `06_Definicao_...Rendimento_de_outras_fontes.pdf` | 713.254 bytes | fórmulas e população das derivadas |
| `Chaves_PNADC.pdf` | 110.160 bytes | chaves estruturais |
| `deflator_PNADC_2025.xls` | 238.592 bytes | tentativa de inspeção dos fatores |
| `PNADcIBGE_Deflator_Anual_Visita.pdf` | 494.532 bytes | documentação dos deflatores |
| `liv102176.pdf` — Nota técnica 01/2025 | 278.248 bytes | visita e acumulação anual |
| `liv102194.pdf` — Nota técnica 02/2025 | 470.099 bytes | reponderação vigente |
| `liv102275_informativo.pdf` | 1.183.696 bytes | conceito e benchmarks 2025 |
| apresentação oficial da divulgação | 3.610.145 bytes | confirmação auxiliar de resultados |

## 6. Estrutura da pesquisa e visitas

`CONFIRMADO` — A PNAD Contínua usa o esquema de rotação `1-2(5)`: o domicílio é entrevistado uma vez no trimestre, sai por dois meses e repete o ciclo por cinco trimestres consecutivos, totalizando cinco visitas.

`CONFIRMADO` — Em cada trimestre existem domicílios em cada uma das cinco visitas. Um arquivo anual por visita acumula, ao longo dos quatro trimestres, as observações que estavam naquela visita específica.

`CONFIRMADO` — Rendimentos do trabalho são coletados em todas as visitas; outras fontes são coletadas na primeira e na quinta visita.

`CONFIRMADO` — Para os indicadores anuais de rendimento de todas as fontes de 2025, o IBGE usa a **primeira visita**.

`CONFIRMADO` — O arquivo anual não é “o primeiro trimestre”. Ele reúne as primeiras visitas realizadas no 1º, 2º, 3º e 4º trimestres de 2025.

`CONFIRMADO` — A exceção histórica foi 2020–2022, quando a quinta visita foi usada por causa da queda de aproveitamento das primeiras visitas na pandemia. A primeira visita voltou a ser referência a partir de 2023.

`INFERÊNCIA FORTE` — No arquivo selecionado, a visita deve ser controlada pelo **arquivo e sua versão**, não por um filtro adicional. A definição geral menciona `V1016 = 1`, mas `V1016` não aparece no `input` da edição anual de primeira visita de 2025; o próprio arquivo já é específico da visita.

## 7. Unidade estatística

`CONFIRMADO` — O layout contém variáveis de pessoa, como `V2003` (número de ordem) e `V2005` (condição no domicílio), além de variáveis domiciliares e derivadas de RDPC.

`CONFIRMADO` — As tabelas SIDRA 7526, 7529, 7534 e 7564 ordenam e agrupam **pessoas** por rendimento domiciliar per capita.

`INFERÊNCIA FORTE` — A unidade operacional para uma distribuição interpretada “entre brasileiros” deve ser um registro por pessoa elegível. O RDPC domiciliar é replicado entre os moradores elegíveis e cada registro contribui com `V1032` uma vez.

Não se deve criar uma linha por domicílio com peso único: isso responderia a uma pergunta sobre domicílios, não sobre pessoas. Também não se deve somar o peso para cada componente de renda dentro do mesmo domicílio.

## 8. População-alvo

`CONFIRMADO` — A distribuição oficial do tema *Rendimento de todas as fontes* representa a população residente, com as exclusões metodológicas abaixo.

`CONFIRMADO` — As fórmulas de `VD5002`, `VD5005`, `VD5008` e `VD5011` excluem pessoas cuja condição no domicílio (`V2005`) é:

- `17` — pensionista;
- `18` — empregado doméstico;
- `19` — parente de empregado doméstico.

Essas pessoas são excluídas tanto da soma dos rendimentos quanto do denominador das derivadas. As notas das tabelas SIDRA também registram a exclusão.

`CONFIRMADO` — Não há filtro de idade no denominador domiciliar. Crianças e pessoas sem rendimento próprio permanecem quando são moradores elegíveis. A restrição de 14 anos ou mais vale para a **captação do rendimento do trabalho**, não para a participação do morador no denominador.

`CONFIRMADO` — A abrangência da PNAD Contínua usada na calibração exclui população residente em setores censitários localizados em terras indígenas, conforme a Nota técnica 02/2025, página 2.

`PENDENTE` — O tratamento detalhado de todas as demais categorias de `V2005`, incluindo eventuais situações de morador ausente, deve ser confirmado célula a célula no dicionário 2025 antes do pipeline. Nenhuma outra exclusão foi localizada nas fontes específicas da variável candidata.

## 9. Conceito de rendimento

O informativo 2025 distingue:

- rendimento **efetivo do trabalho**: rendimento bruto recebido no mês de referência;
- rendimento **habitual do trabalho**: rendimento bruto normalmente recebido pelo trabalho;
- outras fontes: valor efetivamente recebido no mês de referência.

`CONFIRMADO` — A distribuição de rendimento domiciliar per capita publicada no informativo combina rendimento **habitualmente recebido de todos os trabalhos** e rendimento **efetivamente recebido de outras fontes**.

`CONFIRMADO` — Outras fontes incluem:

- aposentadoria e pensão de instituto de previdência oficial;
- programas sociais do governo, incluindo Bolsa Família/Auxílio Brasil e BPC-LOAS;
- aluguel e arrendamento;
- seguro-desemprego ou seguro-defeso;
- pensão alimentícia, doação e mesada de não morador;
- outros rendimentos, como aplicações financeiras, bolsas de estudo, direitos autorais e exploração de patentes.

`CONFIRMADO` — `VD5011` inclui rendimentos em cartão/tíquete de transporte ou alimentação.

`CONFIRMADO` — O rendimento de trabalho é bruto, não líquido de descontos. As fontes consultadas não autorizam interpretar a variável como “valor que sobra depois de impostos, previdência, empréstimos ou despesas”.

## 10. Variável candidata de RDPC

| Código | Nome oficial resumido | Descrição | Unidade/tipo no layout | Arquivo | Elegível? | Evidência |
| --- | --- | --- | --- | --- | --- | --- |
| `VD5002` | Rendimento efetivo domiciliar per capita | Trabalho e outras fontes efetivamente recebidos; exclui cartão/tíquete; exclui `V2005` 17–19 | número, largura 8; reais nominais antes do deflator | visita 1 2025 | Não para a distribuição publicada | definição derivada, pp. 1–2; input, linha da variável |
| `VD5005` | Rendimento efetivo domiciliar per capita | Efetivo; inclui cartão/tíquete; exclui `V2005` 17–19 | número, largura 8; reais nominais antes do deflator | visita 1 2025 | Alternativa legítima, mas não corresponde ao conceito habitual do informativo | definição derivada, pp. 3–4 |
| `VD5008` | Rendimento habitual domiciliar per capita | Trabalho habitual + outras fontes efetivas; exclui cartão/tíquete; exclui `V2005` 17–19 | número, largura 8; reais nominais antes do deflator | visita 1 2025 | Próxima do conceito, mas omite benefícios em cartão/tíquete | definição derivada, pp. 6–7 |
| `VD5011` | Rendimento domiciliar per capita habitual de todos os trabalhos e efetivo de outras fontes | Inclui cartão/tíquete; exclui `V2005` 17–19 | número, largura 8; reais nominais antes do deflator | visita 1 2025 | **Recomendação preliminar** | definição derivada, pp. 7–8; input; informativo 2025; notas SIDRA |

`INFERÊNCIA FORTE` — `VD5011` é a candidata mais aderente à distribuição publicada porque sua definição coincide simultaneamente com: trabalho habitual, outras fontes efetivas, inclusão de cartão/tíquete e exclusões registradas nas tabelas SIDRA.

`DECISÃO DE PRODUTO/METODOLOGIA` — A Fase 1B deve escolher entre reproduzir a distribuição oficial de desigualdade (`VD5011`) ou priorizar um conceito de caixa efetivamente recebido. Não existe autorização para trocar um pelo outro apenas porque ambos são chamados de RDPC.

## 11. Peso amostral

| Código | Nome oficial no layout | Definição | Versão | Adequação | Evidência |
| --- | --- | --- | --- | --- | --- |
| `V1030` | Projeção da população por níveis geográficos | Projeção/controle populacional | arquivo 2025 | Não é o peso de cada registro | `input_PNADC_2025...txt` |
| `V1031` | Peso SEM calibração | Peso não calibrado | arquivo 2025 | Não recomendado para reproduzir estimativas divulgadas | `input_PNADC_2025...txt` |
| `V1032` | Peso COM calibração | Fator de expansão calibrado | arquivo 2025, versão 20260508 | **Recomendação preliminar** | `input_PNADC_2025...txt`; Nota técnica 02/2025; `LEIA-ME.pdf` |
| `V1032001`–`V1032200` | Pesos replicados 1–200 | Replicações para estimação de variância | arquivo 2025 | Não substituir o peso pontual; úteis futuramente para incerteza | `input_PNADC_2025...txt` |

`CONFIRMADO` — `V1032` é explicitamente rotulado “Peso COM calibração” no layout específico da edição.

`INFERÊNCIA FORTE` — `V1032` é o peso pontual adequado para reproduzir os totais e distribuições oficiais. A série reponderada usa calibração com as projeções populacionais atualizadas; o `LEIA-ME` informa que as projeções atuais já estão agregadas aos microdados de todos os anos.

`PENDENTE` — Regras de integridade como peso nulo, zero, negativo ou não finito só poderão ser verificadas com o arquivo integral na Fase 1C.

## 12. Reponderação

`CONFIRMADO` — A Nota técnica 02/2025 atualizou os totais populacionais usados na calibração com as Projeções da População — Revisão 2024, que incorporam resultados do Censo Demográfico 2022.

`CONFIRMADO` — Os indicadores anuais usam estimativas populacionais para 1º de julho.

`CONFIRMADO` — A série histórica desde 2012 foi reponderada para manter comparabilidade temporal.

`CONFIRMADO` — Temas anuais já divulgados antes de 31/07/2025 seriam reponderados em seu ciclo de divulgação de 2026. *Rendimento de todas as fontes 2025* foi divulgado em 08/05/2026, portanto já pertence a esse ciclo.

`CONFIRMADO` — O `LEIA-ME` afirma que, nos microdados de todos os anos, já estão agregadas as projeções atuais utilizadas para expansão da amostra.

`INFERÊNCIA FORTE` — O arquivo `PNADC_2025_visita1_20260508.zip` e seu `V1032` incorporam a reponderação vigente em 2026. Não se deve combinar esse arquivo com pesos preservados de uma versão anterior.

## 13. Variável de UF

`CONFIRMADO` — A variável é `UF`, descrita no layout como **Unidade da Federação**, caractere, largura 2.

Ela permite controles para Brasil, Grandes Regiões derivadas e Unidades da Federação. Comparações estaduais permanecem fora do escopo funcional da V1 atual.

## 14. Identificadores estruturais

| Papel | Variável(is) | Evidência e uso futuro |
| --- | --- | --- |
| Ano | `Ano` | ano de referência |
| Trimestre | `Trimestre` | trimestre de referência dentro do acumulado anual |
| UF | `UF` | Unidade da Federação |
| UPA | `UPA` | Unidade Primária de Amostragem |
| Estrato | `Estrato` | estrato amostral; necessário para desenho/variância quando aplicável |
| Seleção do domicílio | `V1008` | número de seleção do domicílio |
| Painel | `V1014` | painel |
| Pessoa | `V2003` | número de ordem da pessoa |
| Condição domiciliar | `V2005` | define, entre outros, os códigos 17–19 excluídos |

`CONFIRMADO` — Chave de domicílio: `UPA + V1008 + V1014`.

`CONFIRMADO` — Chave de pessoa: `UPA + V1008 + V1014 + V2003`.

`CONFIRMADO` — O documento de chaves alerta que a chave de pessoa não deve ser usada como identificador longitudinal de uma mesma pessoa.

`CONFIRMADO` — Os arquivos de microdados são compostos apenas por entrevistas realizadas.

## 15. Missing e códigos especiais

| Código/valor | Significado | Tratamento oficial conhecido | Decisão necessária? |
| --- | --- | --- | --- |
| vazio/blank no campo numérico | `PENDENTE` | o layout fixa largura e tipo, mas não descreve sozinho todas as categorias de ausência | Sim; confirmar no dicionário e no arquivo integral |
| `0` em `VD5011` | valor válido de RDPC | incluído explicitamente na primeira faixa de `VD5012` | Não como missing; sim para regra de produto |
| `17`, `18`, `19` em `V2005` | pensionista, empregado doméstico, parente de empregado doméstico | excluídos da soma e do denominador de `VD5011` | Sim; aprovar filtro aderente ao indicador |
| missing em `V1032` | não localizado documentalmente | não há autorização para imputar ou substituir por `V1031` | Sim; falhar validação e investigar |

`PENDENTE` — A lista exata de códigos “não aplicável”, “ignorado”, “sem declaração” ou equivalentes para `VD5011` e `V1032` não pôde ser extraída de forma confiável do dicionário binário `.xls` nesta fase.

Recomendação para a Fase 1C: ler o dicionário com ferramenta compatível, registrar as células/abas e inspecionar frequências antes de definir filtros. Missing nunca deve ser convertido em zero.

## 16. Renda zero e valores extremos

`CONFIRMADO` — Zero é um valor possível na variável candidata: a variável de faixa `VD5012` define sua primeira classe como `0 <= VD5011 <= SM_h / 4`.

`INFERÊNCIA FORTE` — Pessoas elegíveis em domicílios sem qualquer rendimento entram na base da distribuição com RDPC zero; pessoas sem rendimento próprio podem ter RDPC positivo devido à renda dos demais moradores.

`INFERÊNCIA FORTE` — Valores negativos não fazem parte do domínio documentado de `VD5011`: as faixas começam em zero e todas as parcelas da fórmula são rendimentos. Porém, a ausência de negativos no arquivo real só pode ser confirmada após inspeção da base integral.

`PENDENTE` — Máximo observado, outliers, truncamentos, top-coding e frequência de zeros dependem dos microdados integrais e não foram investigados por cálculo nesta fase.

`DECISÃO DE PRODUTO/METODOLOGIA` — A Fase 1B deve aprovar como exibir renda zero, como tratar empates extensos em zero e qual política adotar nas caudas, sem alterar ou censurar os dados silenciosamente.

## 17. Referência temporal

`CONFIRMADO` — O rendimento efetivo do trabalho é o bruto recebido no mês de referência da pesquisa.

`CONFIRMADO` — O rendimento habitual do trabalho é o bruto normalmente recebido, investigado para pessoas ocupadas de 14 anos ou mais.

`CONFIRMADO` — Outras fontes usam o valor efetivamente recebido no mês de referência.

`CONFIRMADO` — A base anual acumula observações das primeiras visitas realizadas nos quatro trimestres. Ela não representa a soma dos doze meses nem a renda anual de cada família.

`INFERÊNCIA FORTE` — Um `VD5011 = 2000` é uma estimativa mensal nominal do conceito misto daquele registro antes da aplicação do deflator anual; não significa R$ 24.000 anuais e não deve ser multiplicado por 12 para formar a distribuição.

## 18. Nominal versus real

`CONFIRMADO` — As variáveis `VD5002`, `VD5005`, `VD5008` e `VD5011` no microdado são valores monetários a serem combinados com o arquivo de deflatores quando se pretende produzir valores reais comparáveis.

`CONFIRMADO` — O informativo e as tabelas 7526/7534 usam rendimento **real**, a preços médios de 2025.

`CONFIRMADO` — O indicador de R$ 2.316 usa rendimento **nominal** e efetivamente recebido.

Consequência: nominal e real não podem ser misturados na mesma validação, ainda que ambos sejam expressos em reais de 2025 e usem a mesma visita.

## 19. Deflatores

`CONFIRMADO` — O arquivo oficial é `deflator_PNADC_2025.xls`.

`CONFIRMADO` — A documentação do IBGE oferece três famílias:

- `CO1` para rendimento habitual e `CO1e` para efetivo, a preços médios do próprio ano;
- `CO2` para habitual e `CO2e` para efetivo, a preços médios do último ano coberto pelo arquivo (`YYYY`);
- `CO3` para indicadores associados à linha internacional de pobreza do ODS 1.

`CONFIRMADO` — A orientação é multiplicar a variável nominal pelo fator correspondente. O IPCA calculado pelo IBGE é usado no deflacionamento dos rendimentos.

`INFERÊNCIA FORTE` — Como o layout classifica `VD5011` como “Rend habitual domiciliar per capita”, `CO1`/`CO2` é o par mais provável para a variável derivada completa. Entretanto, a variável contém componentes efetivos de outras fontes.

`PENDENTE` — A documentação localizada não afirma em uma única passagem como o IBGE aplica fatores habitual/efetivo à composição mista de `VD5011`. Antes do pipeline, é necessário confirmar a chave e a regra exata do `deflator_PNADC_2025.xls` e reproduzir os benchmarks do SIDRA.

`PENDENTE` — A chave geográfica e temporal exata do `.xls` de deflatores deve ser registrada após leitura das abas. Não foi inferida por memória.

## 20. Referência de preços

`CONFIRMADO` — A publicação *Rendimento de todas as fontes 2025* e as tabelas SIDRA consultadas apresentam os valores **a preços médios de 2025**.

`CONFIRMADO` — Para séries, `CO1/CO1e` põe cada ano a preços médios do próprio ano; `CO2/CO2e` põe toda a série a preços médios do último ano do arquivo, neste caso 2025.

`INFERÊNCIA FORTE` — Para uma distribuição composta somente por registros de 2025, a referência-alvo é preços médios de 2025. A diferença operacional entre CO1 e CO2 precisa ser confirmada no arquivo, mas ambos apontam para 2025 quando o ano observado e o último ano são 2025.

`DECISÃO DE PRODUTO/METODOLOGIA` — Uma renda informada pelo usuário em 2026 não é automaticamente comparável a uma distribuição em preços médios de 2025. A Fase 1B deve escolher e documentar entre deflacionar a entrada para 2025 ou atualizar a distribuição para uma referência corrente, sempre com fonte oficial e data visível.

## 21. Compatibilidade com a entrada do usuário

Classificação: **COMPATÍVEL COM AJUSTES DE EXPLICAÇÃO**.

Razões:

- a entrada “renda mensal total da casa ÷ moradores” corresponde à estrutura geral de RDPC;
- o conceito estatístico é de **domicílio**, não necessariamente de família por parentesco;
- a renda de trabalho é bruta e habitual na distribuição recomendada;
- outras fontes são efetivamente recebidas;
- `VD5011` inclui cartão/tíquete de transporte ou alimentação;
- pensionistas, empregados domésticos e parentes de empregados domésticos são excluídos do conceito da distribuição publicada;
- a referência de preços precisa ser compatível com a data da renda informada.

`DECISÃO DE PRODUTO/METODOLOGIA` — A Fase 1B deve aprovar uma definição operacional simples o bastante para o usuário e fiel ao indicador. Não se recomenda usar “renda líquida disponível” nem prometer que qualquer soma intuitiva de entradas reproduz exatamente `VD5011`.

## 22. Benchmarks oficiais de validação

### 22.1 Distribuição recomendada preliminarmente

Todos os valores abaixo são publicações oficiais, não cálculos desta fase.

| Benchmark | Valor 2025 | Comparabilidade | Fonte |
| --- | ---: | --- | --- |
| Média real mensal domiciliar per capita | R$ 2.264 | **VALIDAÇÃO DIRETA**, se `VD5011` for aprovado e deflacionado como o IBGE | Informativo 2025 e SIDRA 7534 |
| Índice de Gini do RDPC | 0,511 | **VALIDAÇÃO DIRETA** da distribuição completa | Informativo 2025 |
| População elegível publicada | 212,624 milhões no SIDRA; 212,7 milhões arredondados no informativo | **VALIDAÇÃO DIRETA** do total ponderado | SIDRA 7564 e informativo 2025 |
| P5 | R$ 299 | **VALIDAÇÃO DIRETA** do limite publicado | SIDRA 7526 |
| P10 | R$ 451 | **VALIDAÇÃO DIRETA** | SIDRA 7526 |
| P20 | R$ 694 | **VALIDAÇÃO DIRETA** | SIDRA 7526 |
| P30 | R$ 906 | **VALIDAÇÃO DIRETA** | SIDRA 7526 |
| P40 | R$ 1.154 | **VALIDAÇÃO DIRETA** | SIDRA 7526 |
| P50 | R$ 1.490 | **VALIDAÇÃO DIRETA** | SIDRA 7526 |
| P60 | R$ 1.697 | **VALIDAÇÃO DIRETA** | SIDRA 7526 |
| P70 | R$ 2.158 | **VALIDAÇÃO DIRETA** | SIDRA 7526 |
| P80 | R$ 2.958 | **VALIDAÇÃO DIRETA** | SIDRA 7526 |
| P90 | R$ 4.609 | **VALIDAÇÃO DIRETA** | SIDRA 7526 |
| P95 | R$ 6.900 | **VALIDAÇÃO DIRETA** | SIDRA 7526 |
| P99 | R$ 15.214 | **VALIDAÇÃO DIRETA** | SIDRA 7526 |

As tabelas SIDRA 7529 e 7564 permitem validar populações e proporções por classes simples e acumuladas. A tabela 7534 permite validar médias acumuladas. UFs podem ser usadas como controles adicionais, sem criar uma funcionalidade estadual.

### 22.2 Média oficial de R$ 2.316

Classificação: **VALIDAÇÃO AUXILIAR**.

| Dimensão | R$ 2.316 | Distribuição R$ 2.264 | Coincide? |
| --- | --- | --- | --- |
| Ano | 2025 | 2025 | Sim |
| Visita | primeiras visitas, quatro trimestres | primeiras visitas, quatro trimestres | Sim |
| Preços | nominal | real, preços médios de 2025 | Não |
| Trabalho | efetivamente recebido | habitualmente recebido | Não |
| Outras fontes | efetivamente recebidas | efetivamente recebidas | Sim, em linhas gerais |
| População | todos os moradores, inclusive `V2005` 17–19 | exclui `V2005` 17–19 | Não |
| Finalidade | FPE/LC 143 e CDR | análise da distribuição de rendimentos | Não |

O release de R$ 2.316 foi publicado em 27/02/2026 e atualizado em 27/03/2026. Ele é excelente controle de uma apuração nominal efetiva própria, mas não deve ser usado para forçar o pipeline de `VD5011` a produzir R$ 2.316.

## 23. Dicionário consolidado de variáveis

| Papel | Código | Nome oficial | Tipo | Unidade | Confirmado? | Fonte |
| --- | --- | --- | --- | --- | --- | --- |
| RDPC recomendado | `VD5011` | Rendimento domiciliar per capita habitual de todos os trabalhos e efetivo de outras fontes, inclusive cartão/tíquete, exclusive condições 17–19 | numérico, largura 8 | R$ nominais antes do deflator | `INFERÊNCIA FORTE` como escolha; definição `CONFIRMADA` | input e definição derivada pp. 7–8 |
| Peso | `V1032` | Peso COM calibração | numérico, largura 15 | fator de expansão | `CONFIRMADO` | input 2025 |
| Visita | arquivo `Visita_1`; referência geral `V1016 = 1` | primeira visita | seleção de arquivo; `V1016` não consta no input específico | visita 1 | `CONFIRMADO` | Nota 01/2025, informativo, nome do arquivo |
| UF | `UF` | Unidade da Federação | caractere, largura 2 | código UF | `CONFIRMADO` | input 2025 |
| Domicílio | `UPA + V1008 + V1014` | chave de domicílio | composta | identificador | `CONFIRMADO` | Chaves PNADC |
| Pessoa | `UPA + V1008 + V1014 + V2003` | chave de pessoa no arquivo | composta | identificador | `CONFIRMADO` | Chaves PNADC |
| Condição | `V2005` | Condição no domicílio | caractere, largura 2 | código | `CONFIRMADO` | input e definição derivada |
| Trimestre | `Trimestre` | Trimestre de referência | caractere, largura 1 | 1–4, a confirmar no dicionário | `CONFIRMADO` como campo | input 2025 |
| Deflator habitual próprio ano | `CO1` | fator para rendimento habitual a preços médios do próprio ano | `PENDENTE` no `.xls` | multiplicador | `CONFIRMADO` no manual | manual do deflator |
| Deflator efetivo próprio ano | `CO1e` | fator para rendimento efetivo a preços médios do próprio ano | `PENDENTE` no `.xls` | multiplicador | `CONFIRMADO` no manual | manual do deflator |
| Deflator habitual último ano | `CO2` | fator habitual a preços médios do último ano | `PENDENTE` no `.xls` | multiplicador | `CONFIRMADO` no manual | manual do deflator |
| Deflator efetivo último ano | `CO2e` | fator efetivo a preços médios do último ano | `PENDENTE` no `.xls` | multiplicador | `CONFIRMADO` no manual | manual do deflator |
| Deflator pobreza | `CO3` | fator para indicadores associados à linha de pobreza | `PENDENTE` no `.xls` | multiplicador | `CONFIRMADO`, não elegível para o ranking geral | manual do deflator |

## 24. Contradições e ambiguidades

| Tema | Fonte A | Fonte B | Diferença | Interpretação | Decisão necessária |
| --- | --- | --- | --- | --- | --- |
| Média 2025 | release RDPC: R$ 2.316 | informativo/SIDRA: R$ 2.264 | nominal efetivo e todos os moradores versus real, trabalho habitual e exclusões | não é erro; são indicadores distintos | escolher o conceito do produto |
| “Renda familiar” | linguagem atual do produto | conceito IBGE de domicílio e moradores elegíveis | família não é sinônimo estatístico de domicílio | microcopy pode induzir composição errada | aprovar terminologia na Fase 1B |
| Deflator de `VD5011` | layout chama a derivada de habitual | fórmula contém outras fontes efetivas | manual separa fatores habitual e efetivo | regra operacional da variável mista não foi localizada de forma explícita | confirmar antes do pipeline |
| Visita como campo | definição geral usa `V1016` | input anual específico não lista `V1016` | arquivo já está particionado por visita | controlar pela versão do arquivo | registrar no manifesto |
| População 2025 | informativo: 212,7 milhões | SIDRA 7564: 212,624 milhões | arredondamento editorial | compatível | usar SIDRA no teste numérico |
| Nota de apresentação | uma lâmina extraída contém rodapé 2012/2024 e preços de 2024 em gráfico sobre 2025 | informativo e demais lâminas usam 2025 | provável resíduo editorial da apresentação | não usar a lâmina isolada como autoridade | priorizar informativo e SIDRA |

Não foi localizada contradição que impeça a escolha metodológica. As diferenças principais são conceitos distintos ou resíduos editoriais que devem ser registrados para evitar validação cruzada indevida.

## 25. Fatos confirmados

1. A edição anual de rendimento de todas as fontes de 2025 foi disponibilizada em 08/05/2026.
2. O arquivo vigente localizado é `PNADC_2025_visita1_20260508.zip`.
3. A divulgação de 2025 usa primeiras visitas acumuladas dos quatro trimestres.
4. O arquivo contém registros de pessoas e variáveis domiciliares derivadas.
5. `V1032` é o peso com calibração; `V1031` é o peso sem calibração.
6. `UF` identifica a Unidade da Federação.
7. A chave domiciliar é `UPA + V1008 + V1014`; a chave de pessoa acrescenta `V2003`.
8. `VD5011` combina trabalho habitual, outras fontes efetivas e cartão/tíquete, excluindo `V2005` 17–19.
9. Crianças e pessoas sem renda própria não são excluídas do denominador por idade ou ausência de renda.
10. Zero está no domínio documentado de `VD5011`.
11. A edição incorpora a reponderação baseada nas projeções que incorporam o Censo 2022.
12. A distribuição oficial é por pessoas em ordem crescente de RDPC.
13. A publicação de desigualdade está a preços médios de 2025.
14. A média diretamente comparável dessa distribuição é R$ 2.264, não R$ 2.316.

## 26. Inferências fortes

1. `VD5011 + V1032` é a combinação mais aderente à distribuição do informativo e das tabelas SIDRA.
2. A CDF futura deve contar uma observação ponderada por pessoa elegível, mantendo o mesmo RDPC para moradores elegíveis do domicílio.
3. O arquivo de 08/05/2026 já contém o peso recalibrado vigente; misturar versões quebraria a reprodução.
4. Não se espera RDPC negativo, mas isso ainda deve ser testado nos microdados.
5. Missing deve ser excluído ou tratado conforme dicionário, nunca convertido em zero.
6. A renda corrente do usuário exige alinhamento temporal com preços médios de 2025.

## 27. Hipóteses

1. `CO1` ou `CO2` aplicado à derivada classificada como habitual reproduzirá a média e os percentis SIDRA; a hipótese precisa ser testada contra os benchmarks.
2. Os campos de `VD5011` ausentes aparecem como blank no arquivo fixo; isso não foi comprovado no dicionário.
3. Não existem valores negativos ou pesos não positivos no arquivo; isso depende de inspeção integral.

Nenhuma hipótese acima deve virar configuração de produção sem confirmação.

## 28. Pendências

1. Ler integralmente as abas do dicionário 2025 e registrar códigos de missing/especiais de `VD5011`, `V1032`, `UF`, `Trimestre` e `V2005`.
2. Ler as abas e chaves de `deflator_PNADC_2025.xls`.
3. Confirmar a regra de deflacionamento da composição mista de `VD5011`.
4. Verificar nos microdados frequências, nulos, zeros, negativos, máximos e pesos inválidos.
5. Confirmar se `VD5011` é repetida apenas para pessoas elegíveis ou para todos os registros, aplicando o filtro de população de forma explícita.
6. Reproduzir média, população, Gini e limites SIDRA sem ajustar o método para “fazer bater”.
7. Definir tratamento de empate no percentil.
8. Definir política de caudas e precisão exibida.
9. Definir alinhamento entre renda corrente do usuário e preços médios de 2025.

## 29. Decisões necessárias para a Fase 1B

| ID | Tema | Evidência encontrada | Alternativas | Recomendação | Confiança | Precisa aprovação? |
| --- | --- | --- | --- | --- | --- | --- |
| 1B-01 | Edição/arquivo | versão 20260508, primeira visita, edição 2025 | arquivo atual ou versão anterior | fixar `PNADC_2025_visita1_20260508.zip` e checksum na Fase 1C | Alta | Sim |
| 1B-02 | Visita | Nota 01/2025 e informativo usam primeira visita | primeira ou quinta visita | primeira visita | Alta | Sim |
| 1B-03 | Conceito de RDPC | informativo/SIDRA usam trabalho habitual + outras efetivas e exclusões | distribuição oficial; RDPC nominal efetivo/FPE | reproduzir a distribuição oficial de desigualdade | Alta | Sim |
| 1B-04 | Variável RDPC | `VD5011` coincide com o conceito publicado | `VD5002`, `VD5005`, `VD5008`, `VD5011`, reconstrução | `VD5011`, condicionada à validação SIDRA | Média/Alta | Sim |
| 1B-05 | Peso | `V1032` é peso com calibração; reponderação vigente | `V1031`, `V1032`, replicados | `V1032` para estimativa pontual | Alta | Sim |
| 1B-06 | Unidade | SIDRA distribui pessoas; microdado tem registro individual | pessoa ou domicílio | pessoa elegível ponderada | Alta | Sim |
| 1B-07 | População | fórmula e SIDRA excluem `V2005` 17–19 | excluir ou incluir todos | excluir 17–19 para aderir ao indicador | Alta | Sim |
| 1B-08 | Missing | códigos exatos pendentes | exclusão documentada, erro ou imputação | proibir imputação; decidir após dicionário e frequências | Baixa | Sim |
| 1B-09 | Renda zero | domínio oficial começa em zero | aceitar, rejeitar ou separar | manter zero na distribuição; definir apresentação e empates | Média/Alta | Sim |
| 1B-10 | Referência de preços | publicação em preços médios de 2025 | deflacionar entrada ou atualizar distribuição | escolher uma referência única, visível e versionada | Média | Sim |
| 1B-11 | Deflator | CO1/CO1e e CO2/CO2e documentados | fator na derivada ou reconstrução de componentes | só aprovar após reprodução de benchmarks | Média | Sim |
| 1B-12 | Benchmark | R$ 2.264/SIDRA é comparável; R$ 2.316 é outro conceito | direta ou auxiliar | R$ 2.264 + população + percentis SIDRA como validação direta; R$ 2.316 auxiliar | Alta | Sim |
| 1B-13 | Empates | percentis oficiais podem conter massas no mesmo valor | `<`, `<=`, ponto médio da massa | documentar convenção e testar contra classes SIDRA; não decidir nesta fase | Baixa | Sim |
| 1B-14 | Extremos | PNAD pode sub-representar topo; máximo não inspecionado | extrapolar, limitar ou reportar cauda | não extrapolar sem decisão; limitar afirmação à base observada | Média | Sim |
| 1B-15 | Linguagem de entrada | domicílio não é sinônimo perfeito de família | “família”, “casa”, “domicílio” | manter linguagem simples, mas explicar moradores e renda bruta/habitual | Média | Sim |

## 30. Recomendação metodológica preliminar

Sem canonizar, a configuração preliminar mais defensável é:

```text
IBGE_YEAR = 2025
IBGE_EDITION = Rendimento de todas as fontes 2025
IBGE_FILE = PNADC_2025_visita1_20260508.zip
IBGE_VISIT = primeira visita, acumulada nos quatro trimestres
IBGE_RDPC_VARIABLE = VD5011
IBGE_WEIGHT_VARIABLE = V1032
IBGE_UF_VARIABLE = UF
IBGE_PERSON_UNIT = pessoa elegível
IBGE_EXCLUDED_HOUSEHOLD_CONDITIONS = V2005 em {17, 18, 19}
IBGE_PRICE_REFERENCE = preços médios de 2025
IBGE_DIRECT_VALIDATION = SIDRA 7526, 7529, 7534, 7564 + informativo 2025
IBGE_AUXILIARY_VALIDATION = RDPC nominal R$ 2.316
```

`RECOMENDAÇÃO` — A Fase 1B deve aprovar essa configuração com duas reservas explícitas: missing/códigos especiais e regra exata do deflator ainda precisam ser fechados antes da aquisição e do pipeline.

`RECOMENDAÇÃO` — A futura implementação deve falhar se não reproduzir simultaneamente média R$ 2.264, população publicada e limites SIDRA dentro de tolerâncias justificadas. Não se deve alterar a variável, o peso ou os valores esperados apenas para fazer um teste passar.

## 31. Registro completo de fontes

Todas as fontes são do **Instituto Brasileiro de Geografia e Estatística — IBGE** e foram acessadas em **13/08/2026**.

| ID | Título/arquivo | Publicação/atualização | Localização | O que comprova |
| --- | --- | --- | --- | --- |
| F01 | PNAD Contínua — página oficial | atualização corrente | [produto 17270](https://www.ibge.gov.br/estatisticas/sociais/populacao/17270-pnad-continua.html) | página canônica, divulgações, notas, microdados e erratas |
| F02 | Diretório anual por visita | corrente | [FTP](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/) | organização por visita e documentação geral |
| F03 | `atualizacoes_divulgacao_anual_20260702.txt` | 02/07/2026; entrada de rendimento em 08/05/2026 | [TXT](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/atualizacoes_divulgacao_anual_20260702.txt) | data da atualização de Rendimento de Todas as Fontes 2025 |
| F04 | `LEIA-ME.pdf` | versão disponível em 13/08/2026 | [PDF](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/LEIA-ME.pdf), pp. 1–2 | rotação, arquivos anuais por visita, entrevistas realizadas e projeções atuais incorporadas |
| F05 | Pesquisas suplementares anuais 2012–2025 | 02/07/2026 | [PDF](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/PNADC_Pesquisas_Suplementares_Anuais_20260702.pdf), tabela de rendimento | alocação de rendimentos de outras fontes e visita anual usada |
| F06 | Diretório `Visita_1/Dados` | arquivo 08/05/2026 | [FTP](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Visita_1/Dados/) | nome, versão, data e tamanho aproximado do microdado 2025 |
| F07 | Dicionário 2025 | 08/05/2026 | [XLS](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Visita_1/Documentacao/dicionario_PNADC_microdados_2025_visita1_20260508.xls) | documento canônico de códigos; leitura integral pendente por formato legado |
| F08 | `input_PNADC_2025_visita1_20260508.txt` | 08/05/2026 | [TXT](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Visita_1/Documentacao/input_PNADC_2025_visita1_20260508.txt), linhas das variáveis | campos, tipos, larguras e rótulos de `UF`, pesos, chaves e `VD50xx` |
| F09 | Definição das variáveis derivadas — Rendimento de outras fontes | 12/06/2026 | [PDF](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/Definicao_variaveis_derivadas_PNADC/06_Definicao_variaveis_derivadas_parte05_Rendimento_de_outras_fontes.pdf), pp. 1–8 | definições, fórmulas, universo, exclusões, visita e zero válido |
| F10 | `Chaves_PNADC.pdf` | 02/03/2020 | [PDF](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/Chaves_PNADC.pdf), p. 1 | chaves de domicílio e pessoa e limite longitudinal |
| F11 | Deflator anual por visita — documentação de apoio | 07/02/2022 | [PDF](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/PNADcIBGE_Deflator_Anual_Visita.pdf), pp. 1–2 | CO1/CO1e, CO2/CO2e, CO3 e multiplicação |
| F12 | `deflator_PNADC_2025.xls` | 08/05/2026 | [XLS](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/deflator_PNADC_2025.xls) | arquivo oficial de fatores para 2025; abas/chaves pendentes |
| F13 | Nota técnica 01/2025 — Sobre os rendimentos de todas as fontes | 08/05/2025 | [PDF](https://www.ibge.gov.br/biblioteca/visualizacao/livros/liv102176.pdf), pp. 1–2 | esquema 1-2(5), primeira visita e exceção 2020–2022 |
| F14 | Nota técnica 02/2025 — Atualização das estimativas populacionais e reponderação | 31/07/2025 | [PDF](https://biblioteca.ibge.gov.br/visualizacao/livros/liv102194.pdf), pp. 1–3 | Censo 2022, projeções 2024, 1º de julho, domínios e cronograma de reponderação |
| F15 | *Rendimento de todas as fontes 2025* | 2026; divulgação 08/05/2026 | [PDF](https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf), pp. 1–16 | conceito, visita, preços de 2025, média, Gini, população e distribuição |
| F16 | SIDRA 7526 | atualizado em 08/05/2026 | [tabela](https://sidra.ibge.gov.br/tabela/7526) | limites superiores P5–P99, população/exclusões e referência de preços |
| F17 | SIDRA 7529 | atualizado em 08/05/2026 | [tabela](https://sidra.ibge.gov.br/tabela/7529) | população e proporções em classes simples |
| F18 | SIDRA 7534 | atualizado em 08/05/2026 | [tabela](https://sidra.ibge.gov.br/tabela/7534) | média real acumulada e total de R$ 2.264 |
| F19 | SIDRA 7564 | atualizado em 08/05/2026 | [tabela](https://sidra.ibge.gov.br/tabela/7564) | população e proporções em classes acumuladas; total 212,624 milhões |
| F20 | Release — RDPC 2025 para Brasil e UFs | 27/02/2026; atualizado em 27/03/2026 | [Agência de Notícias](https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45942-ibge-divulga-rendimento-domiciliar-per-capita-2025-para-brasil-e-unidades-da-federacao) | R$ 2.316, nominal, efetivo, todos os moradores, primeira visita |
| F21 | PNAD Contínua: Reponderação em 2025 | 31/07/2025 | [comunicado](https://www.ibge.gov.br/novo-portal-destaques/44067-pnad-continua-reponderacao-em-2025.html) | entrada em vigor da série reponderada e vínculo com Censo 2022 |
| F22 | Apresentação oficial — Rendimento de todas as fontes 2025 | 08/05/2026 | [PDF](https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/01a76679f450b86e5fff76c6887b0b2b.pdf) | confirmação auxiliar da visita, preços e indicadores; contém um rodapé editorial inconsistente registrado na seção 24 |

---

## Encerramento da Fase 1A

A investigação documental está encerrada. Este relatório não autoriza a Fase 1B, aquisição dos microdados, pipeline, CDF ou alteração da aplicação.

Próximo gate: aprovação humana das decisões `1B-01` a `1B-15` e autorização explícita para a Fase 1B.
