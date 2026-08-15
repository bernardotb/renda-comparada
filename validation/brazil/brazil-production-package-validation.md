# Validação do pacote de produção Brasil — Gate G0

**Versão:** `g0-2026-08-15-v1`
**Gerado em:** 2026-08-15
**Resultado:** **PASS — 44/44 checks**

A alegação histórica `21/21 PASS` não foi preservada: os 21 checks individuais e os relatórios originais não foram encontrados. Este relatório deriva de uma suíte nova, explícita e reproduzível.

| Check | Esperado | Observado | Status | Evidência |
|---|---|---|---|---|
| `artifact.cdf.exists` | `true` | `true` | **PASS** | C:\Users\Usuario\Downloads\Novos Vaults\vault-template-main\vault-template-main\Tools and Knowlegde\Calculadora de renda\data\production\brazil\brazil-income-cdf-2025.json |
| `artifact.price.exists` | `true` | `true` | **PASS** | C:\Users\Usuario\Downloads\Novos Vaults\vault-template-main\vault-template-main\Tools and Knowlegde\Calculadora de renda\data\production\brazil\brazil-price-alignment.json |
| `artifact.engine.exists` | `true` | `true` | **PASS** | C:\Users\Usuario\Downloads\Novos Vaults\vault-template-main\vault-template-main\Tools and Knowlegde\Calculadora de renda\data\production\brazil\brazil-income-engine-manifest.json |
| `cdf.sha256` | `"5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5"` | `"5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5"` | **PASS** | data/production/brazil/brazil-income-cdf-2025.json |
| `cdf.size` | `3955036` | `3955036` | **PASS** | data/production/brazil/brazil-income-cdf-2025.json |
| `cdf.uniqueValues` | `83358` | `83358` | **PASS** | vetor rdpc |
| `cdf.sourceSha256` | `"8A44A26C47F16BE54DE787D215145C60B82E33319F806A0F890411B799EDA469"` | `"8A44A26C47F16BE54DE787D215145C60B82E33319F806A0F890411B799EDA469"` | **PASS** | metadados CDF |
| `cdf.historicalFrontendFlag` | `false` | `false` | **PASS** | metadados CDF |
| `cdf.historicalPriceAlignment` | `null` | `null` | **PASS** | metadados CDF |
| `price.schemaVersion` | `"1.0.0"` | `"1.0.0"` | **PASS** | config/schemas/brazil-price-alignment.schema.json |
| `price.schemaSha256` | `"A5531D86FFAE5AC4D319414C8C854DA4F1E67974FA36308C269B11DE1FCD57BB"` | `"A5531D86FFAE5AC4D319414C8C854DA4F1E67974FA36308C269B11DE1FCD57BB"` | **PASS** | config/schemas/brazil-price-alignment.schema.json |
| `price.sourceProposalSha256` | `"A302237DB4B4637C815F54B2E63170A9204FB741966E82251F6A40D0C4E5553B"` | `"A302237DB4B4637C815F54B2E63170A9204FB741966E82251F6A40D0C4E5553B"` | **PASS** | validation/brazil/brazil-price-alignment-proposal.json |
| `price.cdfSha256` | `"5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5"` | `"5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5"` | **PASS** | data/production/brazil/brazil-price-alignment.json |
| `price.index` | `"IPCA"` | `"IPCA"` | **PASS** | D065 |
| `price.sidraTable` | `1737` | `1737` | **PASS** | D065 |
| `price.sidraVariable` | `2266` | `2266` | **PASS** | D065 |
| `price.referenceMonth` | `"2026-07"` | `"2026-07"` | **PASS** | manifesto congelado |
| `price.baseIndex` | `"7300.8416666666666666666666666666666666666666666667"` | `"7300.8416666666666666666666666666666666666666666667"` | **PASS** | série mensal versionada |
| `price.currentIndex` | `"7657.73"` | `"7657.73"` | **PASS** | série mensal versionada |
| `price.status` | `"CANONICAL_APPROVED"` | `"CANONICAL_APPROVED"` | **PASS** | D065 |
| `engine.schemaVersion` | `"1.0.0"` | `"1.0.0"` | **PASS** | config/schemas/brazil-income-engine-manifest.schema.json |
| `engine.schemaSha256` | `"F40FF4731EACA9AADD4FE5FED73422AE259A21B22366613D842CE401D221AB04"` | `"F40FF4731EACA9AADD4FE5FED73422AE259A21B22366613D842CE401D221AB04"` | **PASS** | config/schemas/brazil-income-engine-manifest.schema.json |
| `engine.status` | `"CANONICAL_APPROVED_FOR_INTEGRATION"` | `"CANONICAL_APPROVED_FOR_INTEGRATION"` | **PASS** | contrato de produção |
| `engine.decisions` | `["D063", "D065", "D071", "D072"]` | `["D063", "D065", "D071", "D072"]` | **PASS** | docs/decisoes.md |
| `engine.cdfSha256` | `"5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5"` | `"5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5"` | **PASS** | data/production/brazil/brazil-income-engine-manifest.json |
| `engine.priceSha256` | `"78A7F6E61C7327124743741F59F0F27715200AD1A17E9F712D34C6A5294F3948"` | `"78A7F6E61C7327124743741F59F0F27715200AD1A17E9F712D34C6A5294F3948"` | **PASS** | data/production/brazil/brazil-income-engine-manifest.json |
| `engine.brazilIntegration` | `true` | `true` | **PASS** | manifesto de motor |
| `engine.worldIntegration` | `false` | `false` | **PASS** | D068-D070 bloqueadas |
| `delivery.initialBundle` | `false` | `false` | **PASS** | D072 |
| `delivery.loadTrigger` | `"primeiro cálculo"` | `"primeiro cálculo"` | **PASS** | D072 |
| `price.factor` | `"1.0488831767113609047358694944989219279512293673903"` | `"1.0488831767113609047358694944989219279512293673903"` | **PASS** | IPCA mensal versionado |
| `price.multiplier` | `"0.95339502263290383268496887023526118923841225358776"` | `"0.95339502263290383268496887023526118923841225358776"` | **PASS** | inverso do fator |
| `price.roundTrip` | `"6500"` | `"6500.0000000000000000000000000000000000000000000000"` | **PASS** | aritmética Decimal |
| `golden.base.shareBelow` | `0.701561259093934` | `0.701561259093934` | **PASS** | validation/brazil/brazil-income-golden-cases.json |
| `golden.current.householdComparable` | `"6197.0676471138749124522976565291977300496796483204"` | `"6197.0676471138749124522976565291977300496796483204"` | **PASS** | D065 |
| `golden.current.rdpcComparable` | `"2065.6892157046249708174325521763992433498932161068"` | `"2065.6892157046249708174325521763992433498932161068"` | **PASS** | D065 |
| `golden.current.shareBelow` | `0.6866910622833815` | `0.6866910622833815` | **PASS** | CDF + D065 |
| `lookup.tieSemantics` | `"shareBelow < shareAtOrBelow"` | `{"shareAtOrBelow": 0.5005345976000194, "shareBelow": 0.49991707375376493}` | **PASS** | CDF empírica |
| `lookup.lowerTail` | `{"shareAtOrBelowGreaterThan": 0.0, "shareBelow": 0.0}` | `{"shareAtOrBelow": 0.011123332604987381, "shareBelow": 0.0, "topShare": 1.0}` | **PASS** | D071 |
| `lookup.maximum` | `{"shareAtOrBelow": 1.0, "shareBelowLessThan": 1.0}` | `{"shareAtOrBelow": 1.0, "shareBelow": 0.9999980748661246, "topShare": 1.9251338754244784e-06}` | **PASS** | D071 |
| `lookup.aboveMaximum` | `{"shareAtOrBelow": 1.0, "shareBelow": 1.0}` | `{"shareAtOrBelow": 1.0, "shareBelow": 1.0, "topShare": 0.0}` | **PASS** | D071 |
| `failure.negativeIncome` | `"rejeitar"` | `"Renda corrente não pode ser negativa"` | **PASS** | price_alignment.py |
| `failure.missingArtifact` | `"rejeitar"` | `"Artefato obrigatório ausente: C:\\Users\\Usuario\\Downloads\\Novos Vaults\\vault-template-main\\vault-template-main\\Tools and Knowlegde\\Calculadora de renda\\validation\\brazil\\__g0_missing__.json"` | **PASS** | production_package.py |
| `failure.invalidSchema` | `"rejeitar"` | `"$: campos ausentes: ['accessedAt', 'baseCalculation', 'baseIndex', 'basePriceReference', 'baseYear', 'cdfSha256', 'conversion', 'currentIndex', 'dataset', 'decisionId', 'factorBaseToCurrent', 'generatedAt', 'generatedBy', 'index', 'indexDescription', 'inputIncomePeriod', 'integration', 'monthlyIndex', 'multiplierCurrentToBase', 'precision', 'priceIndexReferenceMonth', 'schema', 'schemaSha256', 'schemaVersion', 'sidraTable', 'sidraVariable', 'source', 'sourceProposal', 'sourceProposalSha256', 'sourceUrl', 'status', 'territory', 'version']"` | **PASS** | config/schemas/brazil-price-alignment.schema.json |

## Reprodução

```powershell
python scripts/data/brazil/production_package.py --validate-only
```

O validador não altera a CDF histórica e falha se hash, schema, golden cases ou referências cruzadas divergirem.
