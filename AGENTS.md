---
title: AGENTS.md
created: 2026-08-12T18:05:05.000-03:00
modified: 2026-08-20T11:17:07.549-03:00
---

# AGENTS.md

Instruções operacionais para agentes de código que trabalhem neste repositório, especialmente o Codex.

Leia este arquivo antes de modificar o projeto.

---

## 1. Função Deste Arquivo

Este `AGENTS.md` define regras permanentes de trabalho no projeto **Renda Comparada**.

Ele não deve funcionar como tracker de:

- fase atual;
- próximo gate;
- branch atual;
- commit atual;
- bloqueio temporário;
- status transitório de pesquisa;
- decisão operacional ainda não canonizada.

Essas informações envelhecem.

O estado corrente deve ser determinado a partir do prompt atual, do checkout, do Git e da documentação vigente.

Regra permanente:

> **Não avance de fase automaticamente.**

A existência de código, pesquisa, dados, scripts, artefatos ou oportunidade técnica não constitui autorização para executar a próxima etapa.

---

## 2. Raiz E Descoberta De Instruções

Considere como raiz operacional:

> **a raiz Git do checkout atual.**

Não dependa de um caminho absoluto específico do Windows para identificar o projeto.

Antes de trabalho material:

1. determine o diretório atual;
2. determine a raiz Git efetiva;
3. confirme quais arquivos de instrução estão realmente ativos;
4. respeite instruções mais específicas aplicáveis ao diretório trabalhado.

Não crie `AGENTS.md`, `AGENTS.override.md` ou instruções aninhadas adicionais apenas por preferência.

Só introduza instruções específicas por subtree quando houver diferenças reais de:

- stack;
- comandos;
- segurança;
- regras de domínio;
- validação;
- restrições operacionais.

---

## 3. Hierarquia De Verdade

Diferencie sempre:

- o que a tarefa deseja mudar;
- o que existe no checkout atual;
- o que está versionado remotamente;
- o que os documentos canônicos determinam;
- o que é apenas pesquisa, histórico, backup ou cópia.

Use esta ordem:

1. **prompt explícito da tarefa** — define objetivo e escopo autorizado;
2. **checkout Git/local atual** — define o estado real da implementação, inclusive mudanças ainda não commitadas;
3. **documentos canônicos do checkout** — definem contratos de produto, metodologia, UX, privacidade e demais regras;
4. **`docs/decisoes.md`** — registra decisões ativas, substituídas, revogadas ou em revisão;
5. **manifestos, schemas, artefatos e relatórios validados** — comprovam contratos técnicos específicos;
6. **GitHub remoto** — representa o estado remoto versionado;
7. **pesquisa, histórico e evidência auxiliar** — informam análise, mas não alteram contratos por si sós;
8. **Google Drive, Syncthing, arquivos enviados a projetos de IA, backups e outros espelhos** — podem estar defasados e não provam o estado atual.

O prompt atual define o objetivo e o escopo operacional autorizado. Para contratos de produto, os documentos canônicos prevalecem sobre prompts, handoffs, relatórios intermediários e memória. Se uma instrução intermediária exigir algo além ou em conflito com o contrato canônico, registrar a divergência antes de editar código; não resolver o conflito silenciosamente.

### Checkout versus GitHub

O GitHub não substitui o checkout para mudanças locais ainda não commitadas ou ainda não enviadas.

Portanto:

```text
checkout local mais novo
≠
GitHub remoto necessariamente mais novo
```

---

## 4. Skills Locais Do Projeto

As skills específicas do Renda Comparada ficam em:

`.agents/skills/`

Elas são auxiliares de execução e não substituem:

1. o prompt explícito da tarefa;
2. o estado real do checkout;
3. este `AGENTS.md`;
4. os documentos canônicos aplicáveis;
5. decisões, manifests, schemas, golden cases e demais contratos vigentes.

Uma skill nunca amplia o escopo ou a autorização da tarefa.

### CORE

As seguintes skills podem ser utilizadas quando a tarefa corresponder claramente ao seu domínio:

- `#121 — Debugger Sistemático (Causa Raiz)`;
- `#123 — Code Review Estruturado (Checklist)`;
- `#126 — Testes Unitários (Framework de Escrita)`.

### CONDITIONAL

Usar somente quando a tarefa envolver diretamente o respectivo domínio:

- `#128 — Acessibilidade Web (WCAG Checklist)`;
- `#070 — Mensagens de Erro Amigáveis`;
- `#107 — Auditoria de SEO On-Page`;
- `#124 — Pipeline CI/CD (GitHub Actions)`.

A existência de uma skill CONDITIONAL não constitui autorização para executar trabalho relacionado.

Em particular, `#124 — Pipeline CI/CD (GitHub Actions)` não autoriza automaticamente:

- deploy;
- staging;
- alteração de secrets;
- alteração de branch protection;
- configuração de environments;
- Vercel;
- domínio;
- publicação.

Essas ações exigem autorização explícita da tarefa corrente.

### Áreas Protegidas

Nenhuma skill autoriza alterar ou reinterpretar automaticamente:

- Brasil;
- Mundo;
- CDFs;
- pesos;
- PPP/PPC;
- alinhamento temporal;
- golden cases;
- manifests;
- schemas;
- contratos estatísticos;
- decisões canônicas.

Quando uma skill detectar possível problema nessas áreas:

- registrar o finding;
- consultar as fontes canônicas aplicáveis;
- não alterar automaticamente;
- respeitar o gate da tarefa.

### Disciplina De Uso

- Preferir nenhuma skill quando uma skill não agregar valor material.
- Não carregar skills por precaução.
- Não criar novas skills automaticamente.
- Não modificar `SKILL.md` durante tarefas não relacionadas à manutenção das skills.
- Quando relevante ao relatório da tarefa, registrar quais skills foram efetivamente utilizadas.
- A fase determina quais skills fazem sentido; as skills não determinam a fase.

---

## 5. Modo De Fechamento Econômico Da V1

Durante o fechamento da V1, operar por:

> **contrato canônico + bug material + evidência suficiente + validação proporcional ao risco**

- Não reabrir item já validado sem mudança posterior relevante, bug reproduzível, regressão concreta, violação de contrato canônico ou evidência nova material.
- Não transformar hipótese, possibilidade teórica ou preferência de implementação em blocker.
- Priorizar bugs materiais, regressões concretas e violações de contrato; não criar gates intermediários sem ganho material de segurança.
- Repetir testes ou auditorias somente quando houver mudança relevante ou motivo técnico concreto.
- Aplicar validação proporcional ao risco: pequenas correções locais exigem evidência suficiente para seu alcance, não necessariamente uma nova cadeia completa de gates.

Este modo não reduz áreas protegidas, disciplina de estado, segurança, privacidade ou hierarquia de fontes. Staging, commit, amend, push, merge, deploy e publicação continuam etapas separadas e proibidas sem autorização explícita; nunca avançar automaticamente para qualquer delas.
