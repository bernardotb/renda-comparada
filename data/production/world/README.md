# Pacote de produção Mundo

Pacote canônico do motor Mundo, derivado exclusivamente de D066–D070 e integrado ao frontend por meio do manifesto agregador autorizado.

Artefatos:

- `world-income-cdf-2024.json` — 216.790 pontos; SHA-256 `5225C58933C76FF657A4515D6A3B17CB38F0C34E0F01563C2950E50D3DD6CFD1`; 8.379.914 bytes;
- `world-price-alignment.json` — SHA-256 `E0117227FE0F4AB2C2F220467CE93CAEF482507DE7213AF4E3C57841E119D4F0`; 2.145 bytes;
- `world-income-engine-manifest.json` — SHA-256 `7DFE725F032D97098EF3BA71950DB9A60AEF24DF7EDA0770423A1B9DBF049C56`; 2.407 bytes.

O manifesto agregador registra `worldFrontendIntegrationAllowed = true`. A CDF e o alinhamento de preços preservam seus flags históricos bloqueados e seus hashes originais.

`predev` e `prebuild` validam e sincronizam exatamente os três artefatos acima para `public/data/world/`; o build os publica em `dist/data/world/`. Os golden cases permanecem como evidência de regressão e não são copiados para a área pública. O loader solicita os três artefatos sob demanda, valida integridade e referências cruzadas, mantém o runtime em memória e falha fechado, sem fallback numérico.

Regeneração e validação:

```powershell
python scripts/data/world/production_package.py
python -m unittest discover -s tests/data/world -p "test_*.py" -v
cmd /c pnpm run test:frontend
cmd /c pnpm run typecheck
cmd /c pnpm run build
```

Uma atualização de fonte, build PIP, ano global, base PPP ou mês de preços exige evidência preservada, regeneração dos golden cases, regressão e promoção explícita. Não editar os JSONs derivados manualmente.
