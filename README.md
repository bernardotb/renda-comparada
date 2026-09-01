# Renda Comparada

Aplicação para comparar a renda domiciliar por pessoa com distribuições de renda do Brasil e do mundo. O produto compara **renda**, não patrimônio.

## Estado atual

Os motores Brasil e Mundo estão integrados ao frontend a partir de pacotes canonizados, com metodologia, CDFs, alinhamentos temporais, manifestos, schemas e validação reproduzível. Existe uma versão pública em [https://rendacomparada.com.br](https://rendacomparada.com.br), servida pela Vercel. A produção observada não corresponde ao build do `HEAD` atual, e o commit de origem do deployment público permanece desconhecido (`PRODUCTION_COMMIT = UNKNOWN`). Portanto, conteúdo presente no checkout ou no GitHub não deve ser tratado automaticamente como deployed.

- Brasil: decisões D063, D065 e D071–D073 ativas; pacote de dados validado e integrado. O G2 foi registrado como PASS COM RESSALVAS, sem converter verificações dinâmicas ausentes em PASS.
- Mundo: D066–D070 ativas e canônicas; pacote de produção materializado e validado; integração autorizada pelo manifesto agregador.
- Frontend: Brasil e Mundo calculam resultados numéricos por loaders independentes, sob demanda e sem fallback legado.
- V1: Frontend Completion e Pre-Release Gap Closure concluídos no checkout.
- Release readiness: execução e resultado não comprovados no checkout ou no histórico Git inspecionado; essa ausência de registro não apaga a existência da versão pública observada.
- Produção: versão pública existente, diferente do build atual do `HEAD`; deployment ID e commit de origem não identificados.
- Analytics: Plausible Analytics está decidido e implementado no `HEAD`, mas sua implementação não está presente nem ativa na produção observada.

## Autoridade e navegação

Leia primeiro [AGENTS.md](AGENTS.md) e depois o [índice documental](docs/README.md). A metodologia está em [docs/04-metodologia-dados.md](docs/04-metodologia-dados.md), o escopo em [docs/02-prd-v1.md](docs/02-prd-v1.md) e as decisões em [docs/decisoes.md](docs/decisoes.md).

Este README é apenas a entrada do repositório. Ele não define fórmula, fonte estatística ou regra de produto de forma independente.

## Pacote Brasil

Contrato de produção:

```text
data/production/brazil/brazil-income-cdf-2025.json
data/production/brazil/brazil-price-alignment.json
data/production/brazil/brazil-income-engine-manifest.json
```

A CDF é histórica e imutável. A autorização posterior para integração está no manifesto do motor, não em alteração retroativa da CDF.

No frontend, `pnpm.cmd run sync:brazil-runtime` verifica hashes e tamanhos e copia os três arquivos canônicos para `public/data/brazil/`. Essa saída é ignorada pelo Git e recriada no desenvolvimento/build. O navegador carrega e valida os artefatos somente no primeiro cálculo e os reutiliza em memória.

Geração e validação determinística dos manifestos e relatórios:

```powershell
python scripts/data/brazil/production_package.py
python scripts/data/brazil/production_package.py --validate-only
```

## Desenvolvimento e testes

Dependências do frontend:

```powershell
pnpm.cmd install --frozen-lockfile
```

Validação estatística e do contrato Brasil:

```powershell
python -m pip install -r requirements-data.txt
python -m unittest discover -s tests/data/brazil -p "test_*.py" -v
python scripts/data/brazil/production_package.py --validate-only
```

Validação do frontend:

```powershell
pnpm.cmd run test:frontend
pnpm.cmd run typecheck
pnpm.cmd run build
```

Higiene Git:

```powershell
git diff --check
git status --short --branch
```

Não execute deploy sem avaliação de release readiness versionada e autorização explícita. Não use constantes antigas do frontend como fallback nem confunda integração local/build com publicação em produção.
