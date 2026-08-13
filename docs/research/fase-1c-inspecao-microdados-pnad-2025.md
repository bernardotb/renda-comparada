---
title: Fase 1C — Inspeção dos Microdados PNAD 2025
created: 2026-08-13T14:00:00.000-03:00
status: pesquisa concluída com bloqueio metodológico
canonical: false
---

# Fase 1C — Inspeção dos Microdados PNAD 2025

> **RELATÓRIO DE PESQUISA — NÃO CANÔNICO.** Este documento registra evidências empíricas. Ele não altera por si só `docs/04-metodologia-dados.md` nem as decisões vigentes.

## 1. Resumo executivo

A edição, o arquivo, a primeira visita, o universo elegível, o peso `V1032` e a estrutura dos microdados passaram na inspeção. A hipótese metodológica aprovada para validação na D054, porém, **não passou**: `VD5011 × CO1` produz média ponderada de R$ 2.331,67, arredondada para R$ 2.332, contra R$ 2.264 publicados pelo IBGE. A diferença é R$ 67,67, ou 2,9889%.

O diagnóstico encontrou uma alternativa oficial plausível que reproduz os agregados: somar, por domicílio, `VD4019 × CO1` (trabalho habitual) e `VD4048 × CO1e` (outras fontes efetivas), e dividir por `VD2003`. Essa reconstrução:

- reproduz exatamente `VD5007` antes do deflator;
- resulta em média de R$ 2.264,0378, arredondada para R$ 2.264;
- reproduz o Gini oficial de 0,511 a três casas;
- reproduz as médias das 27 UFs após arredondamento;
- reproduz 10 dos 12 limites nacionais publicados, com diferenças de apenas R$ 1 em P90 e P99.

Isso constitui evidência forte de que a distribuição publicada exclui rendimentos em cartão/tíquete e aplica deflatores separados aos componentes habitual e efetivo. Conforme a autorização, a alternativa **não foi canonizada nem transformada em pipeline**. A D054 deve ser reaberta antes de qualquer fase de produção.

## 2. Fonte e integridade

| Campo | Valor |
| --- | --- |
| Instituição | IBGE |
| Arquivo | `PNADC_2025_visita1_20260508.zip` |
| Edição | `20260508` |
| Visita | primeira visita |
| URL | [diretório oficial do IBGE](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Visita_1/Dados/) |
| Tamanho | 188.972.248 bytes |
| SHA-256 | `556C68467941FCF8FB1251CDBAD3E42F6912C7938D73FD75F900BEE1C79548A5` |
| Download concluído | 13/08/2026 13:31:20, America/Sao_Paulo |

Na verificação anterior ao download, o diretório oficial ainda apresentava essa edição como o único arquivo de 2025, datado de 08/05/2026 e sem sucessor explicitamente substitutivo. O ZIP foi preservado sem modificação sob `data/raw/`, ignorado pelo Git.

## 3. Arquivos encontrados no ZIP

O ZIP contém um único membro:

| Nome | Tamanho descomprimido | Tamanho comprimido |
| --- | ---: | ---: |
| `PNADC_2025_visita1.txt` | 1.508.496.616 bytes | 188.972.106 bytes |

O TXT integral não foi extraído; a inspeção foi feita por streaming seletivo diretamente do ZIP.

## 4. Ferramentas utilizadas

- Windows 11 (`Windows-11-10.0.26200-SP0`);
- Python 3.12.13;
- pandas 3.0.1;
- NumPy 2.3.5;
- `xlrd` 2.0.2, instalado no ambiente de pesquisa para leitura dos `.xls` legados;
- biblioteca padrão do Python para ZIP, JSON, CSV e HTTP.

Nenhuma dependência foi adicionada a `package.json`. O script reproduzível é `scripts/research/inspect-pnad-2025.py`.

## 5. Layout e parsing

O parsing usa exclusivamente o [layout oficial da edição](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Visita_1/Documentacao/input_PNADC_2025_visita1_20260508.txt). Foram lidas apenas as colunas necessárias, em arquivo de largura fixa.

| Variável | Posição inicial | Largura | Tipo | Descrição resumida |
| --- | ---: | ---: | --- | --- |
| `Ano` | 1 | 4 | caractere | ano de referência |
| `Trimestre` | 5 | 1 | caractere | trimestre |
| `UF` | 6 | 2 | caractere | Unidade da Federação |
| `UPA` | 12 | 9 | caractere | unidade primária de amostragem |
| `Estrato` | 21 | 7 | caractere | estrato |
| `V1008` | 28 | 2 | caractere | número do domicílio |
| `V1014` | 30 | 2 | caractere | painel |
| `V1032` | 58 | 15 | numérico | peso anual calibrado |
| `V2003` | 90 | 2 | caractere | número de ordem da pessoa |
| `V2005` | 92 | 2 | caractere | condição no domicílio |
| `V2009` | 103 | 3 | numérico | idade |
| `VD2003` | 517 | 2 | numérico | componentes elegíveis do domicílio |
| `VD4019` | 560 | 8 | numérico | trabalho habitual |
| `VD4048` | 609 | 8 | numérico | outras fontes efetivas |
| `VD5011` | 684 | 8 | numérico | RDPC com cartão/tíquete |

As 408.364 linhas possuem exatamente 3.692 caracteres. O arquivo contém 152.488 domicílios, 408.364 chaves de pessoa únicas e nenhuma duplicata de chave de pessoa.

## 6. VD5011

O dicionário define `VD5011` como rendimento domiciliar per capita composto por trabalho habitual e outras fontes efetivas, **incluindo** cartão/tíquete e excluindo as condições domiciliares 17 a 19.

| Métrica | Resultado |
| --- | ---: |
| registros totais | 408.364 |
| `VD5011` preenchido | 408.243 |
| `VD5011` missing | 121 |
| `VD5011 = 0` | 4.682 |
| `VD5011 < 0` | 0 |
| mínimo válido | R$ 0 |
| máximo válido nominal | R$ 201.518 |
| valores distintos | 7.361 |

A escala é monetária mensal em reais nominais inteiros no arquivo, antes da aplicação do deflator anual.

## 7. População elegível

`V2005` representa a condição no domicílio. Os 121 registros excluídos pelo conceito coincidem exatamente com os 121 registros sem `VD5011`:

| Código | Condição | Registros | Peso | `VD5011` presente |
| --- | --- | ---: | ---: | ---: |
| 17 | pensionista | 15 | 5.978,7581 | 0 |
| 18 | empregado doméstico | 100 | 48.873,4490 | 0 |
| 19 | parente de empregado doméstico | 6 | 3.819,9980 | 0 |

Não há pessoa elegível sem `VD5011` nem pessoa excluída com `VD5011`. Isso confirma operacionalmente o universo descrito na D056.

Sanity checks agregados:

- 73.846 crianças elegíveis com menos de 14 anos possuem `VD5011`; 73.259 têm RDPC positivo;
- 131.066 pessoas com renda individual `VD4052` vazia ou zero vivem em domicílios com `VD5011` positivo;
- RDPC zero permanece válido e observado.

## 8. V1032

| Métrica | Todos os registros | População elegível |
| --- | ---: | ---: |
| registros | 408.364 | 408.243 |
| válidos | 408.364 | 408.243 |
| missing/não finitos | 0 | 0 |
| zero | 0 | 0 |
| negativos | 0 | 0 |
| mínimo | 2,7467906 | 2,7467906 |
| máximo | 23.894,31976887 | 23.894,31976887 |
| média | 520,8171068110 | 520,8277540598 |
| soma | 212.682.957,0058 | 212.624.284,8006 |

O peso é numérico, positivo e integralmente preenchido. Nenhuma correção ad hoc foi aplicada.

## 9. UF e identificadores

`UF` está presente e foi usada apenas para junção com os deflatores e validação de médias oficiais. As chaves de domicílio foram formadas por ano, trimestre, UF, UPA, estrato, `V1008` e `V1014`; a chave de pessoa acrescentou `V2003`. Não foram gerados resultados identificáveis nem percentis estaduais.

## 10. Missing

O missing de `VD5011` aparece como campo vazio. O dicionário rotula esse estado como “Não aplicável” e não documenta código numérico especial. Conclusão de pesquisa:

```text
IBGE_RDPC_MISSING_CODES = campo vazio/blank; sem código numérico especial observado
IBGE_WEIGHT_MISSING_CODES = campo vazio/blank; nenhuma ocorrência observada
```

Essas conclusões ainda não alteram o documento canônico.

## 11. Zeros

Foram encontrados 4.682 registros elegíveis com `VD5011 = 0`, peso de 2.365.090,6397 pessoas, equivalente a 1,112333% da população elegível. Os zeros foram preservados em todos os diagnósticos.

## 12. Negativos

Não foi encontrado nenhum `VD5011 < 0`. O peso associado a valores negativos é zero. Nenhum registro foi excluído por esse critério.

## 13. Extremos

Para a hipótese direta `VD5011 × CO1`, os valores diagnósticos são:

| Corte | Valor real aproximado |
| --- | ---: |
| P90 | R$ 4.761,02 |
| P95 | R$ 7.014,00 |
| P99 | R$ 15.314,59 |
| P99,5 | R$ 20.828,24 |
| P99,9 | R$ 39.312,97 |
| máximo | R$ 200.013,33 |

Na reconstrução compatível com os agregados oficiais, P99,5 é R$ 20.507,98, P99,9 é R$ 38.991,66 e o máximo é R$ 200.165,79. Nenhum outlier foi removido e nenhuma extrapolação foi criada. A lista agregada dos 15 maiores valores, suas frequências e pesos consta no resumo JSON.

## 14. Deflator

O `deflator_PNADC_2025.xls` contém 1.620 linhas; 108 pertencem a 2025, cobrindo 4 trimestres × 27 UFs. A chave operacional é ano, trimestre e UF.

| Fator | Uso documentado | Intervalo observado em 2025 |
| --- | --- | ---: |
| `CO1` | rendimento habitual, preços médios do próprio ano | 0,9842591262–1,0188724165 |
| `CO1e` | rendimento efetivo, preços médios do próprio ano | 0,9872816970–1,0257473430 |
| `CO2` | habitual, preços médios do último ano | igual a `CO1` em 2025 |
| `CO2e` | efetivo, preços médios do último ano | igual a `CO1e` em 2025 |
| `CO3` | pobreza | 1 em todas as linhas de 2025 |

O [manual oficial do deflator](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/PNADcIBGE_Deflator_Anual_Visita.pdf) orienta multiplicar o rendimento nominal pelo fator correspondente. Como `VD5011` mistura componentes habituais e efetivos, aplicar um único fator ao total não preserva as duas referências.

## 15. Referência de preços

Os testes usaram os fatores `CO1` e `CO1e`, que convertem os respectivos componentes para preços médios de 2025. O valor armazenado no microdado é nominal. A referência “preços médios de 2025” foi empiricamente reproduzida pela deflação separada dos componentes, mas essa fórmula ainda precisa de aprovação metodológica formal.

## 16. Média R$ 2.264

### Hipótese aprovada para validação: `VD5011 × CO1`

| Medida | Resultado |
| --- | ---: |
| média não arredondada | R$ 2.331,668828 |
| média arredondada | R$ 2.332 |
| benchmark | R$ 2.264 |
| diferença absoluta | +R$ 67,668828 |
| diferença relativa | +2,988906% |

Resultado: **falhou**.

### Diagnóstico alternativo oficial plausível

```text
RDPC_real =
  soma_domiciliar(VD4019 × CO1 + VD4048 × CO1e)
  ÷ VD2003
```

| Medida | Resultado |
| --- | ---: |
| média não arredondada | R$ 2.264,037828 |
| média arredondada | R$ 2.264 |
| diferença absoluta | +R$ 0,037828 |
| diferença relativa | +0,001671% |

A soma nominal `VD4019 + VD4048`, agregada ao domicílio, reproduziu `VD5007` sem nenhuma diferença nos 408.243 registros elegíveis. Isso fornece justificativa independente para a alternativa; não foi um ajuste de filtro para “bater” o benchmark.

## 17. População ponderada

| Medida | Resultado |
| --- | ---: |
| soma de `V1032` elegível | 212.624.284,8006 |
| SIDRA publicado | 212.624.000 |
| diferença absoluta | +284,8006 |
| diferença relativa | +0,000133946% |
| ambos em milhares, arredondados | 212.624 |

A diferença é compatível com a publicação do SIDRA em milhares de pessoas. A população passa no teste.

## 18. Validação SIDRA

Foram consultadas as tabelas oficiais [7526](https://apisidra.ibge.gov.br/values/t/7526/n1/all/v/10838/p/2025/c1019/all), [7529](https://apisidra.ibge.gov.br/values/t/7529/n1/all/v/606/p/2025/c1019/all), [7534](https://apisidra.ibge.gov.br/values/t/7534/n1/all/v/10816/p/2025/c1042/all) e [7564](https://apisidra.ibge.gov.br/values/t/7564/n1/all/v/606/p/2025/c1042/all).

A hipótese `VD5011 × CO1` reproduziu 0 dos 12 limites nacionais publicados e 0 das 27 médias por UF após arredondamento. A reconstrução por componentes reproduziu:

- 10 de 12 limites nacionais exatamente; P90 e P99 diferem em R$ 1;
- 27 de 27 médias por UF exatamente;
- população total publicada após arredondamento em milhares;
- 8 de 12 médias acumuladas exatamente; as demais diferem entre R$ 1 e R$ 2.

Esses resíduos mínimos provavelmente decorrem do procedimento exato de construção/partição das classes e do arredondamento editorial, não de diferença material no universo ou no conceito.

## 19. Outros benchmarks

O [informativo Rendimento de todas as fontes 2025](https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf) publica Gini de 0,511. A hipótese direta resulta em 0,509312, ou 0,509 a três casas. A reconstrução por componentes resulta em 0,511224, ou 0,511 a três casas.

`VD5008 × CO1`, que já exclui cartão/tíquete mas usa um único deflator, chegou perto da publicação: média de R$ 2.261,99 e Gini de 0,511283. A diferença residual de cerca de R$ 2 na média desaparece quando trabalho habitual e outras fontes efetivas recebem seus fatores próprios.

## 20. BR-VAL-001 a BR-VAL-010

| ID | Questão | Resultado | Status | Evidência | Bloqueia próxima fase? |
| --- | --- | --- | --- | --- | --- |
| BR-VAL-001 | domínio `VD5011` | variável existe e foi integralmente perfilada | PASSOU COM RESSALVA | 408.243 válidos, 7.361 distintos, intervalo 0–201.518 nominal; conceito não reproduz publicação | Sim, quanto à escolha como variável principal |
| BR-VAL-002 | missing `VD5011` | blank/“Não aplicável”, exatamente condições 17–19 | PASSOU | 121 missing e nenhuma divergência de elegibilidade | Não |
| BR-VAL-003 | integridade `V1032` | sem missing, zero, negativo ou não finito | PASSOU | 408.364 pesos válidos | Não |
| BR-VAL-004 | negativos | nenhuma ocorrência | PASSOU | contagem e peso iguais a zero | Não |
| BR-VAL-005 | zeros | 4.682 registros; 2.365.090,64 pessoas; 1,112333% | PASSOU | zeros preservados | Não |
| BR-VAL-006 | extremos | máximo e quantis extremos medidos sem exclusão | PASSOU COM RESSALVA | máximo compatível R$ 200.165,79; cauda futura ainda requer regra de exibição | Não para decisão; sim para produção até política posterior |
| BR-VAL-007 | deflator | fatores e chave confirmados; `VD5011` não aceita corretamente um único fator | PASSOU COM RESSALVA | `CO1` habitual e `CO1e` efetivo reproduzem publicação quando aplicados aos componentes | Sim, exige canonização da fórmula |
| BR-VAL-008 | média R$ 2.264 | `VD5011 × CO1` = R$ 2.331,67; reconstrução = R$ 2.264,04 | FALHOU | diferença direta +2,9889%; alternativa arredonda para o benchmark | Sim |
| BR-VAL-009 | população | 212.624.284,80 versus 212.624.000 | PASSOU | igualdade após arredondamento em milhares | Não |
| BR-VAL-010 | agregados | hipótese direta falha; reconstrução reproduz Gini, UFs e quase todos os cortes | FALHOU | 0/12 cortes e 0/27 UFs para `VD5011`; 10/12 e 27/27 para alternativa | Sim |

## 21. Divergências encontradas

1. D054 aponta `VD5011`, que inclui cartão/tíquete; os agregados oficiais de desigualdade são compatíveis com o conceito sem cartão/tíquete.
2. Um único deflator aplicado a uma variável mista não reproduz a média, os cortes ou o Gini.
3. A fórmula por componentes reproduz a publicação, mas ainda não é decisão canônica.
4. P90 e P99 da reconstrução diferem em R$ 1 dos limites SIDRA, e quatro médias acumuladas diferem em até R$ 2; o procedimento exato de partição/arredondamento das classes deve ser documentado antes de golden cases de cortes.

## 22. Bloqueios metodológicos

- reabrir D054 para decidir entre `VD5008` e reconstrução auditável com `VD4019`, `VD4048`, `VD2003`, `CO1` e `CO1e`;
- canonizar a exclusão ou inclusão de cartão/tíquete de acordo com o indicador oficial escolhido;
- canonizar a regra operacional de deflação dos componentes;
- decidir como tratar os resíduos de arredondamento dos cortes oficiais;
- não iniciar pipeline de produção enquanto essas decisões não forem aprovadas.

## 23. Recomendações para a próxima fase

Antes da Fase 1D, executar uma etapa curta de decisão metodológica:

1. substituir ou revogar a parte da D054 que escolhe `VD5011`;
2. aprovar explicitamente a fórmula por componentes, se o objetivo continuar sendo reproduzir *Rendimento de todas as fontes 2025*;
3. atualizar `docs/04-metodologia-dados.md`, `docs/09-fontes-referencias.md` e `docs/decisoes.md` em commit documental próprio;
4. somente depois autorizar o pipeline reproduzível.

## 24. Decisões que precisam de aprovação

| Decisão | Alternativas observadas | Recomendação técnica desta pesquisa |
| --- | --- | --- |
| variável/construção da renda | `VD5011`; `VD5008`; componentes | componentes `VD4019 + VD4048`, pois reproduzem integralmente o conceito e os benchmarks |
| cartão/tíquete | incluir; excluir | excluir para manter compatibilidade com a distribuição publicada |
| deflator | único fator; fatores separados | `CO1` no trabalho habitual e `CO1e` nas outras fontes efetivas |
| implementação futura | variável pronta; reconstrução domiciliar | reconstrução domiciliar auditável, com validação contra `VD5007` nominal |
| tolerância de validação | ainda não definida | definir apenas após aprovação do procedimento e análise dos resíduos editoriais |

## 25. Arquivos e artefatos gerados

- `scripts/research/inspect-pnad-2025.py` — inspeção reproduzível;
- `docs/research/artifacts/fase-1c-source-manifest.json` — proveniência e checksum;
- `docs/research/artifacts/fase-1c-validation-summary.json` — resultados agregados detalhados;
- `docs/research/artifacts/fase-1c-variable-profile.csv` — perfil agregado compacto;
- `docs/research/fase-1c-inspecao-microdados-pnad-2025.md` — este relatório;
- `.gitignore` — proteção de `data/raw/`.

O ZIP, os documentos oficiais baixados e o TXT de microdados não são versionados.

## 26. Observação futura fora do escopo — estimativa de impostos

Durante a Fase 1C foi registrado o requisito futuro de mostrar uma **estimativa de quanto a família paga de impostos**. Ele não foi implementado nem misturado ao percentil de renda. Antes de entrar no produto, esse módulo precisará de decisão própria sobre conceito — impostos diretos, indiretos ou carga total estimada —, fontes oficiais, faixas de consumo, referência temporal, linguagem de incerteza e privacidade. Trata-se de estimativa distinta da PNAD e não altera os resultados desta fase.
