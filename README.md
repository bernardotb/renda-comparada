# Renda Comparada

Aplicação para comparar a renda domiciliar por pessoa com distribuições de renda do Brasil e, futuramente, do mundo. O produto compara **renda**, não patrimônio.

## Estado atual

O motor Brasil está integrado ao frontend a partir do pacote canonizado, com metodologia, CDF histórica, alinhamento temporal, manifestos, schemas e validação reproduzível. A aplicação completa ainda não está pronta para produção porque Mundo permanece bloqueado e não houve gate de publicação.

- Brasil: decisões D063, D065, D071 e D072 ativas; pacote de dados validado.
- Mundo: D066 e D067 ativas; D068, D069 e D070 continuam bloqueadas.
- Frontend: cálculo Brasil usa o pacote canônico; Mundo não exibe resultado numérico.
- Deploy: fora do Gate G1 e não executado.

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

Não execute deploy, não use constantes antigas do frontend como fallback e não publique resultado mundial enquanto D068–D070 permanecerem bloqueadas.
