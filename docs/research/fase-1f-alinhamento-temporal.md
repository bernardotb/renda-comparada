---
title: Fase 1F — Alinhamento Temporal da Renda do Usuário
created: 2026-08-13T00:00:00.000-03:00
status: proposta validada, pendente de canonização
canonical: false
---

# Fase 1F — Alinhamento Temporal da Renda do Usuário

> **RELATÓRIO DE PESQUISA — NÃO CANÔNICO.** Este documento investiga e testa uma proposta. Ele não altera `docs/04-metodologia-dados.md`, `docs/decisoes.md`, a CDF ou o frontend.

## 1. Resumo executivo

**CONFIRMADO:** na metodologia anual da PNAD Contínua, “preços médios de 2025” significam o nível de preços dado pela **média aritmética dos números-índice mensais de janeiro a dezembro de 2025**. Não significam dezembro de 2025. Para cada trimestre, o IBGE usa a média dos três meses correspondentes no rendimento habitual; no rendimento efetivo, desloca a referência em um mês. `CO1` e `CO1e` levam esses componentes à média do próprio ano.

**CONFIRMADO:** a série nacional oficial mais direta para um fator sem UF é o IPCA, tabela SIDRA 1737, variável 2266, “IPCA — Número-índice (base: dezembro de 1993 = 100)”. A média dos 12 números-índice de 2025 é:

```text
IPCA_médio_2025 = 7300,8416666666666667
```

**CONFIRMADO:** em 13/08/2026, o último mês oficial disponível era julho de 2026, com número-índice `7657,73`. O IPCA de agosto ainda não estava publicado e não foi projetado.

**DECISÃO METODOLÓGICA PROPOSTA:** para a V1 nacional, que não pergunta UF, deflacionar a renda mensal corrente pelo IPCA nacional até a média de 2025:

```text
renda_comparável_2025
= renda_corrente × IPCA_médio_2025 / IPCA_último_mês_oficial
```

Para julho de 2026:

```text
fator_2025_para_2026-07 = 7657,73 / 7300,8416666666666667
                          = 1,0488831767113609

multiplicador_2026-07_para_2025 = 0,9533950226329038
```

**PENDENTE:** a documentação oficial sustenta o cálculo dos níveis de preços, mas não escolhe pelo produto entre pedir UF e usar o IPCA nacional. O fator nacional é uma aproximação oficial, transparente e adequada ao formulário atual; não é o mesmo que aplicar o deflator regional exato que seria usado para um morador de UF conhecida. A recomendação requer aprovação humana e canonização posterior.

O problema não está bloqueado por falta de dados ou fórmula. Está **resolvido como proposta validada**, mas ainda bloqueado para integração por decisão e canonização.

## 2. O que significa “preços médios de 2025”

### CONFIRMADO

O Anexo 3 das Notas técnicas da PNAD Contínua define:

1. rendimento habitual do trimestre: média aritmética dos números-índice dos três meses do trimestre;
2. rendimento efetivo: mesma construção, com defasagem de um mês no período de referência;
3. nível de preços do ano: média aritmética dos números-índice de janeiro a dezembro;
4. correção anual: razão entre o nível de preços representativo do ano e o do trimestre.

O pacote oficial de deflatores da edição confirma:

- `CO1`: preços médios do próprio ano para rendimento habitual;
- `CO1e`: preços médios do próprio ano para rendimento efetivo;
- a variável nominal deve ser multiplicada pelo deflator associado.

Assim, a referência canônica da CDF é uma média anual de níveis de preços, não o fechamento do ano e não a variação acumulada de 2025.

## 3. Fontes oficiais

| Fonte | Uso nesta fase | Estado |
| --- | --- | --- |
| [PNAD Contínua — Notas técnicas, Anexo 3](https://www.ibge.gov.br/biblioteca/visualizacao/livros/liv101548_notas_tecnicas.pdf) | definição dos níveis trimestral e anual | `CONFIRMADO` |
| [Documentação geral dos microdados anuais por visita](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/Documentacao_Geral/) | `CO1`, `CO1e` e `deflator_PNADC_2025.xls` | `CONFIRMADO` |
| [SIDRA 1737 — IPCA nacional](https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2266/p/202501-202607?formato=json) | números-índice nacionais mensais | `CONFIRMADO` |
| [SIDRA 7060 — IPCA por área](https://apisidra.ibge.gov.br/values/t/7060/n7/all/v/63/p/202501-202607/c315/7169?formato=json) | diagnóstico regional, com taxas mensais publicadas | `CONFIRMADO` como fonte; diagnóstico é aproximado |
| [Nota técnica do deflacionamento mensal](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Mensal/Notas_tecnicas/nota_tecnica_02_pnadc_mensal.pdf) | construção de índices para UFs com e sem cobertura direta | `CONFIRMADO` |
| [Calendário de divulgações conjunturais](https://www.ibge.gov.br/calendario/conjunturais.html) | confirma divulgação de julho/2026 em 11/08/2026 | `CONFIRMADO` |

Data de acesso: **13/08/2026**.

Não foram usados IGP-M, CDI, salário mínimo, projeção de mercado ou calculadora privada.

## 4. Série de preços e reprodução da base

Série: tabela SIDRA `1737`, variável `2266`, Brasil.

| Mês | Número-índice |
| --- | ---: |
| 2025-01 | 7111,86 |
| 2025-02 | 7205,03 |
| 2025-03 | 7245,38 |
| 2025-04 | 7276,54 |
| 2025-05 | 7295,46 |
| 2025-06 | 7312,97 |
| 2025-07 | 7331,98 |
| 2025-08 | 7323,91 |
| 2025-09 | 7359,06 |
| 2025-10 | 7365,68 |
| 2025-11 | 7378,94 |
| 2025-12 | 7403,29 |

Fórmula reproduzida com `Decimal`:

```text
IPCA_médio_2025
= (7111,86 + 7205,03 + ... + 7403,29) / 12
= 7300,8416666666666666666666666666666666666666666667
```

A série versionada inclui também janeiro a julho de 2026. Ela está em `validation/brazil/brazil-price-alignment-proposal.json`, identificada como proposta pendente de canonização e com integração ao frontend proibida.

## 5. Nacional versus regional

### Estratégia A — IPCA nacional

**INFERÊNCIA:** é a alternativa coerente com uma experiência nacional que não coleta UF. Usa uma série oficial, reproduzível e uniforme; preserva a privacidade e a simplicidade do formulário. A aproximação ocorre porque o usuário real vive em uma região específica.

### Estratégia B — fator regional/UF

**CONFIRMADO:** a PNAD aplica índices das áreas cobertas pelo SNIPC às UFs correspondentes e constrói índices regionais ponderados para as demais UFs. Essa alternativa seria mais alinhada ao tratamento original do microdado, mas exige localização e uma tabela de correspondência atualizada.

**PENDENTE DE PRODUTO:** perguntar UF acrescentaria um campo e mudaria a jornada. Não foi autorizado nesta fase.

### Diagnóstico da diferença

Para dimensionar o trade-off, as taxas mensais publicadas na tabela 7060 foram encadeadas, por área, desde dezembro de 2024; calculou-se a média dos níveis relativos de 2025 e a razão julho/2026 ÷ média/2025. Como as taxas publicadas têm duas casas decimais, este é um **diagnóstico aproximado**, não um substituto dos deflatores oficiais.

Nas dez regiões metropolitanas retornadas nesse recorte, o fator variou de:

```text
Curitiba: 1,0361517
Recife:   1,0555601
Brasil:   1,0488832
```

Em relação ao fator nacional, a diferença aproximada variou de `-1,21%` a `+0,64%`. Isso comprova que o fator nacional não é regionalmente exato, embora a ordem de grandeza do desvio observado seja limitada neste período.

### Recomendação

**DECISÃO METODOLÓGICA PROPOSTA:** usar o IPCA nacional na V1 e declarar a limitação. Manter UF como possível refinamento futuro, não como requisito atual.

## 6. Alternativas avaliadas

### A — Deflacionar a renda corrente

```text
x_2025 = x_corrente × I_médio_2025 / I_corrente
```

Vantagens:

- CDF e SHA permanecem imutáveis;
- uma única conversão por cálculo;
- golden cases estruturais da CDF não mudam;
- manifesto mensal é pequeno e auditável.

### B — Atualizar todos os thresholds da CDF

```text
y_corrente = y_2025 × I_corrente / I_médio_2025
```

Produz o mesmo ranking com fator uniforme positivo, mas cria um artefato derivado variável, aumenta o trabalho de validação e pode sugerir incorretamente que a distribuição social foi atualizada.

### Recomendação

**DECISÃO METODOLÓGICA PROPOSTA:** adotar A. B permanece uma equivalência matemática e pode ser usada apenas para teste ou apresentação, sem modificar a CDF canônica.

## 7. Fórmula recomendada

Sejam:

```text
B = média aritmética dos 12 números-índice do IPCA nacional de 2025
M = número-índice do último mês oficial disponível
F = M / B
```

Então:

```text
renda_domiciliar_2025 = renda_domiciliar_corrente / F
RDPC_2025 = renda_domiciliar_2025 / moradores_elegíveis
posição = lookup_CDF_2025(RDPC_2025)
```

Forma equivalente:

```text
renda_domiciliar_2025
= renda_domiciliar_corrente × B / M
```

O cálculo interno deve preservar precisão decimal. Arredondamento monetário e percentual de apresentação pertencem à futura camada de UI.

## 8. Referência temporal da entrada e defasagem

### DECISÃO METODOLÓGICA PROPOSTA

Interpretar o campo futuro como:

> renda mensal nominal vigente informada na data do cálculo.

Usar, para o nível de preços, o último IPCA mensal oficialmente publicado na data do cálculo. Não pedir mês adicional na V1.

Registrar separadamente:

```text
calculationDate = data da consulta
priceIndexReferenceMonth = mês efetivamente usado
priceIndexLatestAvailableMonth = último mês oficial incorporado
```

Em 13/08/2026:

```text
calculationDate = 2026-08-13
priceIndexReferenceMonth = 2026-07
priceIndexLatestAvailableMonth = 2026-07
```

**CONFIRMADO:** usar julho em agosto não é projetar julho para agosto; é usar o dado oficial mais recente com sua defasagem explicitada.

**PENDENTE:** se o usuário quiser informar renda histórica, a V1 proposta não oferece essa modalidade. Um seletor de mês seria outra funcionalidade.

## 9. Exemplo experimental — R$ 6.500 / 3

Este exemplo **não substitui** o golden case de R$ 6.500 em preços médios de 2025.

Entrada corrente em 13/08/2026, usando o IPCA oficial de julho/2026:

```text
renda corrente = R$ 6.500,00
moradores = 3
B = 7300,8416666666666667
M = 7657,73
F = 1,0488831767113609

renda comparável em 2025 = R$ 6.197,0676471139
RDPC comparável em 2025 = R$ 2.065,6892157046
shareBelow = 0,6866910622833815
shareAtOrBelow = 0,6866910622833815
topShare = 0,3133089377166185
```

Para apresentação monetária, a renda comparável seria aproximadamente **R$ 6.197,07** e a RDPC, **R$ 2.065,69**. O percentil ainda não está autorizado para o site.

## 10. Invariância de ranking

Considere um fator uniforme `F > 0`, renda corrente `x` e qualquer threshold da CDF de 2025 `y`.

```text
y < x / F
```

Multiplicando os dois lados por `F`, que é positivo:

```text
y × F < x
```

Portanto, consultar a CDF original com `x / F` seleciona exatamente o mesmo peso abaixo que consultar thresholds multiplicados por `F` com `x`. O mesmo vale para `<=`, porque a multiplicação por fator positivo preserva igualdade e ordem.

O teste automatizado cobre valores abaixo do mínimo, exatamente empatados, entre thresholds e acima do máximo, verificando simultaneamente `shareBelow` e `shareAtOrBelow`.

## 11. Atualização e versionamento

Arquitetura recomendada após aprovação:

```text
CDF PNAD 2025 imutável
        +
manifesto pequeno do IPCA nacional
        ↓
renda corrente convertida para a média de 2025
        ↓
lookup na CDF canônica
```

Fluxo mensal futuro:

```text
novo IPCA oficial
↓
importação da tabela 1737 / variável 2266
↓
validação de continuidade, positividade e mês oficial
↓
novo manifesto de preços versionado
↓
testes de fórmula, ida e volta e invariância
↓
aprovação
↓
publicação controlada
```

Não deve haver `latest` consultado silenciosamente em produção. O artefato deve registrar fonte, data de acesso, último mês, base, índice corrente e fator. Nenhum job externo foi criado nesta fase.

## 12. Limitações

1. O IPCA corrige apenas a referência monetária; não transforma a distribuição de 2025 em uma distribuição estatística de 2026.
2. O fator nacional não reproduz o fator regional exato de cada UF.
3. O valor de renda digitado pode ter reajustes salariais próprios; isso não muda o fato de que ele é uma quantia nominal corrente a ser posta na mesma unidade monetária da CDF.
4. O IPCA possui defasagem de divulgação; a aplicação deve exibir o mês efetivamente usado.
5. A base de dezembro de 1993 do número-índice é apenas uma normalização. Ela se cancela nas razões.
6. O diagnóstico regional baseado em taxas com duas casas é aproximado.

## 13. Decisões necessárias

### PENDENTE DE APROVAÇÃO HUMANA

1. aprovar o IPCA nacional como compromisso da V1 sem UF;
2. aprovar que a entrada signifique renda mensal nominal vigente;
3. aprovar o uso do último IPCA oficial disponível, com mês explicitado;
4. aprovar a estratégia de deflacionar a entrada e preservar a CDF;
5. definir, na integração, a microcopy e a precisão visual;
6. canonizar a regra em `docs/04-metodologia-dados.md` e `docs/decisoes.md` numa etapa 1F-R;
7. promover somente depois o manifesto proposto para `data/production/brazil/brazil-price-alignment.json`.

## 14. Testes

Implementação experimental independente do frontend:

- `scripts/data/brazil/price_alignment.py`;
- `scripts/research/validate-brazil-price-alignment.py`;
- `tests/data/brazil/test_price_alignment.py`;
- `validation/brazil/brazil-price-alignment-proposal.json`.

Comando:

```powershell
python -m unittest discover -s tests/data/brazil -p "test_price_alignment.py" -v
python scripts/research/validate-brazil-price-alignment.py
```

Resultado em 13/08/2026:

```text
11 testes executados
11 testes aprovados
validação reproduzível: PASS
```

Cobertura:

- média oficial de 2025;
- referência contra ela própria igual a 1;
- fator positivo;
- conversão de ida e volta;
- zero preservado;
- ausência de mês oficial falha sem projeção;
- mês posterior à data de acesso é rejeitado;
- ausência ou incompletude da série falha com segurança;
- invariância de `<` e `<=` sob escala uniforme;
- determinismo decimal;
- integridade do checksum da CDF.

O SHA-256 da CDF permaneceu:

```text
5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5
```

## 15. Recomendação para integração futura

Depois da aprovação e da canonização 1F-R:

1. promover um manifesto pequeno e versionado do IPCA;
2. implementar a mesma aritmética no módulo de domínio do frontend;
3. validar a implementação do browser contra os casos `Decimal` deste relatório;
4. informar “PNAD Contínua 2025, valores ajustados pelo IPCA até julho de 2026” ou formulação equivalente;
5. manter a CDF canônica intacta;
6. não afirmar que o ajuste atualiza a estrutura social ou a distribuição de renda para 2026.

Até essa aprovação, `frontendIntegrationAllowed` permanece `false`.
