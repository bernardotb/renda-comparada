# Pacote de produção Mundo

Pacote canônico e isolado do motor Mundo, derivado exclusivamente de D066–D070. Ele não é publicado em `public/**`, não é importado por `src/App.tsx` e não participa de `predev`, `prebuild` ou `build`.

Artefatos:

- `world-income-cdf-2024.json` — 216.790 pontos; SHA-256 `5225C58933C76FF657A4515D6A3B17CB38F0C34E0F01563C2950E50D3DD6CFD1`; 8.379.914 bytes;
- `world-price-alignment.json` — SHA-256 `E0117227FE0F4AB2C2F220467CE93CAEF482507DE7213AF4E3C57841E119D4F0`; 2.145 bytes;
- `world-income-engine-manifest.json` — SHA-256 `E9F3B291A4231A860FD6194017E8A82EF2134AE7C3D1B1AA5141BBBF29BE902B`; 2.411 bytes.

O manifesto registra `worldFrontendIntegrationAllowed = false`.

Regeneração e validação:

```powershell
python scripts/data/world/production_package.py
python -m unittest discover -s tests/data/world -p "test_*.py" -v
cmd /c pnpm run test:frontend
cmd /c pnpm run typecheck
cmd /c pnpm run build
```

Uma atualização de fonte, build PIP, ano global, base PPP ou mês de preços exige evidência preservada, regeneração dos golden cases, regressão e promoção explícita. Não editar os JSONs derivados manualmente.
