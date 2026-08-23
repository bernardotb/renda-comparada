---
title: Higiene do Repositório — Pré-Codex
created: 2026-08-14T18:25:00-03:00
status: auditoria
canonical: false
---

# Higiene do Repositório — Pré-Codex

## 1. Resultado

O `.gitignore` atual está coerente com a arquitetura do projeto.

Ele já exclui:

```text
node_modules/
dist/
coverage/
*.tsbuildinfo
.vercel/
.env
.env.*
data/raw/
data/processed/
__pycache__/
.pytest_cache/
```

Também bloqueia `data/production/*` por padrão e libera explicitamente apenas os artefatos Brasil já aprovados.

Portanto:

> **a presença desses itens no Google Drive não indica falha do `.gitignore`; indica que a pasta local foi sincronizada/copieda para o Drive com arquivos que não pertencem ao repositório.**

---

## 2. Itens que não devem fazer parte do repositório versionado

```text
node_modules/
dist/
.vercel/
.env.local
*.tsbuildinfo
.git/
```

`.git/` não precisa de regra no `.gitignore`, pois é a estrutura do próprio repositório. Mas também não deve ser tratado como arquivo de projeto para compartilhamento ou cópia por Drive.

---

## 3. `.env.local`

Existe um `.env.local` no Drive.

Ele não foi aberto nesta auditoria e nenhum segredo foi copiado para a documentação.

### Regra

Antes de ampliar compartilhamento da pasta ou entregar o repositório:

1. remover `.env.local` de cópias compartilhadas no Drive;
2. confirmar quais credenciais existem nele;
3. se houve compartilhamento além das pessoas autorizadas, avaliar rotação das credenciais;
4. manter apenas um `.env.example` sem segredos se a implementação precisar documentar variáveis de ambiente.

A remoção/rotação não foi executada automaticamente porque é uma ação operacional/destrutiva que exige decisão do responsável.

---

## 4. `node_modules`

Não deve ser sincronizado como parte da fonte.

Motivos:

- volume;
- duplicação do lockfile;
- arquivos dependentes de plataforma;
- manutenção ruim;
- nenhuma utilidade para revisão documental.

A fonte de reprodução deve ser:

```text
package.json
pnpm-lock.yaml
```

---

## 5. `dist`

É artefato derivado.

Não deve funcionar como fonte de verdade.

Regra:

```text
src/
+ configuração
+ lockfile
↓
build reproduzível
↓
dist/
```

Não editar `dist` manualmente.

---

## 6. `.vercel`

A pasta local contém `project.json`, que confirma:

```text
projectName = renda-familiar-brasil-mundo
```

Isso identifica o vínculo local com o projeto Vercel.

Não prova:

- domínio canônico;
- plano;
- configurações atuais do projeto remoto;
- analytics ativo;
- deploy atual.

`.vercel/` continua corretamente ignorado.

---

## 7. Produção Brasil

O `.gitignore` libera explicitamente:

```text
data/production/brazil/brazil-income-cdf-2025.json
data/production/brazil/brazil-price-alignment.json
data/production/brazil/brazil-income-engine-manifest.json
```

Isso é coerente com o estado metodológico atual.

---

## 8. Produção Mundo

Ainda **não** liberar no `.gitignore`:

```text
data/production/world/*
```

enquanto D068–D070 não forem canonizadas.

Durante pesquisa/validação, usar:

```text
validation/world/
docs/research/
```

ou artefatos locais ignorados conforme a política do projeto.

Depois da canonização, abrir somente os arquivos de produção explicitamente aprovados, pelo mesmo princípio usado no Brasil.

---

## 9. Ação pré-Codex recomendada

Antes da fase de implementação:

```text
1. escolher uma única raiz Git canônica
2. conferir git status
3. confirmar que .env* não está tracked
4. confirmar que node_modules/dist não estão tracked
5. remover cópias locais redundantes
6. preservar somente source/config/docs/tests/artefatos aprovados
7. criar baseline/commit limpo antes da refatoração
```

Não executar limpeza destrutiva a partir do Drive sem confirmar a raiz Git real.

---

## 10. Gate

A higiene do repositório não bloqueia pesquisa metodológica.

Ela bloqueia apenas uma passagem segura para implementação/commit caso a raiz técnica continue ambígua ou contenha segredos em cópias compartilhadas.
