---
name: 124-pipeline-cicd-github-actions
description: Projeta ou revisa workflows de CI do Renda Comparada quando a tarefa autorizar GitHub Actions para testes e build; não autoriza deploy, secrets, environments ou publicação.
---

## Objetivo

Criar ou revisar um pipeline de CI com GitHub Actions para executar os checks já existentes do projeto, como testes, typecheck, lint e build, sem introduzir deploy ou publicação.

## Quando usar

* Ao configurar CI pela primeira vez no projeto
* Para automatizar testes que a equipe esquece de rodar
* Na padronização dos checks executados em pull requests
* Quando o CI existente apresenta falhas concretas ou trabalho duplicado

## Como usar

1. Copie o prompt abaixo no Claude ou ChatGPT
2. Descreva o projeto, stack e comandos de validação existentes
3. Receba uma proposta de workflow de CI proporcional à tarefa
4. Altere `.github/workflows/` somente quando a tarefa autorizar explicitamente essa edição

## O Prompt

    Você é um engenheiro DevOps que configura pipelines de CI robustos e simples. Seus princípios: (1) pipeline rápido, (2) feedback claro, (3) execução reproduzível dos checks existentes, (4) permissões mínimas.

    Não inclua CD, deploy, previews, secrets, environments, branch protection, migrations ou publicação sem autorização explícita e separada da tarefa.

    Crie o pipeline de CI para:

    **Projeto:** [tipo — web app, API, mobile, monorepo]
    **Stack:** [ex: Next.js, Node.js, Python/Django, Go]
    **Repositório:** [GitHub — monorepo ou single]
    **Testes:** [Jest, pytest, Go test — quais existem]
    **Linting:** [ESLint, Prettier, Black — quais usa]
    **Build:** [como faz build — npm run build, docker build, etc.]
    **Gerenciador de pacotes:** [npm, pnpm, yarn, pip, outro]
    **Gatilhos autorizados:** [pull_request, push ou execução manual]

    Entregue:

    **1. Estratégia de CI** - Checks, ordem e gatilhos
    **2. Workflow de CI** - YAML para `.github/workflows/ci.yml`
    **3. Permissões** - Escopo mínimo necessário
    **4. Diagnóstico de falhas** - Como tornar erros acionáveis
    **5. Otimizações** - Cache e paralelização somente quando justificadas

## Exemplo de uso

### Input

Projeto: React + ViteGerenciador: pnpmTestes: pnpm run test:frontendTypecheck: pnpm run typecheckBuild: pnpm run buildGatilho: pull_request para main

### Output

```yaml
name: CI

on:
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm run test:frontend
      - run: pnpm run typecheck
      - run: pnpm run build
```

* * *

**Tags:** Intermediário | Template | Código, Dev & Automação
