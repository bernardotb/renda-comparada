# Pipeline brasileiro — PNAD Contínua 2025

Este diretório implementa a metodologia brasileira canônica da V1 sem integração com o frontend.

## Ambiente reproduzível

Use Python 3.12 e instale somente as dependências fixadas:

```powershell
python -m pip install -r requirements-data.txt
```

As versões usadas na validação da Fase 1D foram Python 3.12.13, NumPy 2.3.5 e xlrd 2.0.2.

## Fonte local

O pipeline espera o ZIP oficial em:

```text
data/raw/ibge/pnadc/2025/20260508/PNADC_2025_visita1_20260508.zip
```

O raw e a documentação oficial dessa edição permanecem fora do Git. Antes de qualquer leitura, o pipeline valida nome, tamanho e SHA-256 contra `config/brazil-pnad-2025.json`.

## Execução

Para construir uma única saída intermediária:

```powershell
python scripts/data/brazil/build_brazil_dataset.py
```

Para executar testes, dois runs limpos, comparação de checksums e relatórios:

```powershell
python scripts/data/brazil/validate_brazil_dataset.py
```

Para gerar uma CDF isolada a partir do dataset intermediário já validado:

```powershell
python scripts/data/brazil/build_brazil_cdf.py
```

Para executar dois runs da CDF, comparar os hashes, validar o lookup e gerar os golden cases brasileiros:

```powershell
python scripts/data/brazil/validate_brazil_cdf.py
```

As saídas intermediárias ficam sob `data/processed/`, ignorado pelo Git. Os relatórios sem dados individuais são gravados em `validation/brazil/`.

## Fórmula protegida

```text
RDPC_real_2025 =
  soma_domiciliar(VD4019 × CO1 + VD4048 × CO1e)
  ÷ VD2003
```

O pipeline usa a chave domiciliar integral documentada, volta o RDPC agregado para cada pessoa elegível e preserva `V1032` como peso individual. Blanks estruturais de `VD4019` ou `VD4048` valem zero apenas para o componente correspondente; não são convertidos em RDPC final ausente.

## Falha segura

Nenhum artefato é promovido se falhar a fonte, o layout, o join de deflatores, a integridade da chave domiciliar, a reconstrução nominal contra `VD5007`, os pesos, o RDPC, os benchmarks ou a igualdade entre os dois runs.

O pipeline intermediário não cria CDF. A etapa separada da Fase 1E gera CDF, lookup e golden cases somente a partir do CSV validado, sem reler o ZIP. Nenhuma etapa implementa alinhamento temporal da entrada, altera `src/` ou integra o artefato ao site.
