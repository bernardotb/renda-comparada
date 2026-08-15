# Renda Comparada

Aplicação para comparar a renda domiciliar por pessoa com distribuições de renda do Brasil e, futuramente, do mundo. O produto compara **renda**, não patrimônio.

## Estado atual

O pacote de dados Brasil está **liberado para uma futura integração**, com metodologia, CDF histórica, alinhamento temporal, manifestos, schemas e validação reproduzível. Isso não significa que o frontend atual esteja integrado nem que a aplicação completa esteja pronta para produção.

- Brasil: decisões D063, D065, D071 e D072 ativas; pacote de dados validado.
- Mundo: D066 e D067 ativas; D068, D069 e D070 continuam bloqueadas.
- Frontend: protótipo visual/histórico com motor numérico legado; não é fonte metodológica.
- Deploy: fora do Gate G0 e não executado.

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

Validação do frontend sem modificar o protótipo:

```powershell
pnpm.cmd run typecheck
pnpm.cmd run build
```

Higiene Git:

```powershell
git diff --check
git status --short --branch
```

Não execute deploy, não use constantes antigas do frontend como fallback e não publique resultado mundial enquanto D068–D070 permanecerem bloqueadas.
