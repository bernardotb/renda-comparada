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

### Checkout versus GitHub

O GitHub não substitui o checkout para mudanças locais ainda não commitadas ou ainda não enviadas.

Portanto:

```text
checkout local mais novo
≠
GitHub remoto necessariamente mais novo
```
