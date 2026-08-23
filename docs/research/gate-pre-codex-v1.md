---
title: Gate Pré-Codex — V1
created: 2026-08-14T16:52:00-03:00
status: controle de prontidão — revisão 0.2
canonical: false
---

# Gate Pré-Codex — Renda Comparada V1

> Documento operacional de prontidão. Não cria metodologia nova. Serve para impedir que pendências reais sejam confundidas com trabalho que pode ser delegado à implementação.

## 1. Princípio

O Codex deve receber um contrato suficientemente fechado para **implementar**, não para escolher metodologia.

A implementação pode decidir detalhes locais de engenharia somente quando eles não alterarem:

- conceito de renda;
- universo estatístico;
- fonte;
- referência temporal;
- percentil;
- linguagem de interpretação;
- privacidade;
- ordem da jornada;
- dados enviados a terceiros.

---

## 2. Pronto para implementação — Brasil

```text
Fonte PNAD 2025........................ PRONTO
Release 20260508....................... PRONTO
Construção RDPC........................ PRONTO — D063
Peso V1032............................. PRONTO
População elegível..................... PRONTO
CDF brasileira — método/validação...... PRONTO
CDF brasileira — arquivo materializado.. PRONTO; SHA reconfirmado após upload
Empates................................ PRONTO
Golden cases........................... PRONTO
Alinhamento renda atual → 2025......... PRONTO — D065
Manifesto IPCA......................... PRONTO
```

A implementação não deve reabrir esses itens sem evidência de conflito.

### Observação de artefato

O relatório validado registra o artefato:

```text
data/production/brazil/brazil-income-cdf-2025.json
SHA-256 = 5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5
tamanho = 3.955.036 bytes
```

Em 14/08/2026 o arquivo foi reconstruído deterministicamente a partir do dataset processado validado presente no próprio Drive. A reprodução coincidiu exatamente com os dois controles congelados:

```text
size = 3955036 bytes
SHA-256 = 5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5
```

O artefato foi então promovido para `data/production/brazil/`, baixado novamente do Drive e o mesmo tamanho/SHA-256 foi reconfirmado. Portanto, a ausência física da CDF deixou de ser bloqueio.

Não reconstruir uma CDF diferente nem substituir por thresholds manuais.

O `.gitignore` foi ajustado em 14/08/2026 para permitir explicitamente os artefatos aprovados do motor Brasil, mantendo `data/processed/` e outros artefatos de produção bloqueados por padrão.

### Validação do pacote de produção Brasil

Depois da materialização da CDF e criação do manifesto do motor, o pacote completo foi validado em 14/08/2026:

```text
21 checks
21 PASS
```

Foram verificados:

- hashes cruzados dos artefatos;
- tamanho e monotonicidade da CDF;
- semântica de zero, máximo e acima do máximo;
- D065 no golden case R$ 6.500 / 3;
- D071 com exibição Percentil 69 / TOP 31%;
- bloqueio explícito do Mundo.

Relatórios:

```text
validation/brazil/brazil-production-package-validation.json
validation/brazil/brazil-production-package-validation.md
```

Esse PASS encerra a validação do **pacote de dados Brasil**. Não substitui testes do frontend.

---

## 3. Parcialmente pronto — Mundo

```text
Fonte PIP.............................. PRONTO
Versão 20260324_2021................... PRONTO — D066
Build 20260324_2021_01_02_PROD......... PRONTO — D066
PPP-base 2021.......................... PRONTO conceitualmente
Ano global 2024........................ PRONTO — D066
Natureza renda/consumo................. PRONTO — D067
Linguagem “posição monetária estimada”. PRONTO — D067
CDF/quantis globais.................... BLOQUEADO — futura D068
PPP Brasil 2021 exata da versão PIP.... BLOQUEADO — futura D069
CPI/alinhamento até 2021............... BLOQUEADO — futura D069
Golden cases/caudas.................... BLOQUEADO — futura D070
```

### Direção aprovada para pesquisa, ainda não canônica

1. construir CDF mundial experimental a partir da `1000 Binned Global Distribution`;
2. validar a CDF contra o agregado oficial `pip wb` / `pip-grp` em múltiplas `povline`;
3. obter `ppp` e `cpi` da própria versão PIP/auxiliares;
4. usar WDI/ICP como validação secundária, não como substituição silenciosa do PIP;
5. não usar `popshare` no agregado mundial: o wrapper oficial restringe essa opção ao nível de país.

---

## 4. Pronto para implementação — produto/UX

Já há definição suficiente para:

- home sem valores fictícios;
- renda mensal nominal vigente;
- moradores inteiros >= 1;
- CTA explícito para calcular;
- Brasil antes de Mundo;
- `TOP X%` como leitura intuitiva principal;
- percentil como leitura estatística secundária;
- renda por pessoa como informação secundária;
- fonte e ano visíveis;
- metodologia acessível;
- simular novamente;
- compartilhamento antes de qualquer check-up;
- compartilhamento padrão genérico;
- posição somente após ação explícita;
- renda nunca no compartilhamento;
- continuação financeira opcional.

O motor Mundo continua bloqueando a apresentação de um número mundial real, não a estrutura visual do card.

---

## 5. Pronto para implementação — privacidade

Regras já fechadas:

```text
sem cadastro obrigatório
sem renda em URL
sem renda em analytics
sem renda em localStorage/sessionStorage
sem persistência de cálculo por padrão
sem renda em logs/error tracking
sem renda em compartilhamento automático
sem percentil/top em analytics
cálculo individual preferencialmente no navegador
```

---

## 6. Pendências legítimas que NÃO devem ser preenchidas por inferência

### Produto / operação

```text
PRODUCTION_DOMAIN = [DEFINIR]
ANALYTICS_PROVIDER = [DEFINIR]
SEARCH_CONSOLE_PROPERTY = [CONFIGURAR]
```

### Privacidade / responsabilidade

```text
CONTROLADOR = [DEFINIR]
PRIVACY_CONTACT = [DEFINIR]
SECURITY_CONTACT = [DEFINIR]
```

Esses campos dependem de decisão operacional do responsável pelo produto e não devem ser preenchidos automaticamente por IA.

---


## 6A. P0 operacional — permissões do Google Drive

Em 14/08/2026, a pasta raiz do projeto `Calculadora de renda` foi verificada via metadados do Google Drive e apresentou:

```text
permission.type = anyone
permission.role = writer
allowFileDiscovery = false
```

Isto significa que qualquer pessoa que obtenha o link pode editar o conteúdo da pasta.

### Estado

```text
DRIVE_PUBLIC_WRITE_ACCESS = P0 — RESOLVER ANTES DE PUBLICAÇÃO / USO COMO FONTE CANÔNICA COMPARTILHADA
```

### Regra

- não alterar permissões automaticamente sem decisão do responsável;
- não depender de compartilhamento público de escrita para integrações ou agentes;
- após a restrição, verificar se os conectores autorizados continuam acessando normalmente;
- revisar se arquivos sensíveis como `.env.local` ou credenciais continuam expostos pela pasta compartilhada;
- considerar rotação de qualquer segredo que tenha ficado acessível a terceiros.

---

## 7. Analytics — estado

Vercel Web Analytics foi avaliado como candidato compatível com a arquitetura de privacidade da V1. A documentação oficial confirma que o plano Hobby oferece Web Analytics/pageviews, mas **não oferece custom events**; Pro e Enterprise oferecem custom events.

Portanto:

```text
VERCEL_PLAN = [VERIFICAR]
ANALYTICS_PROVIDER = NÃO CANONIZADO
```

A taxonomia completa de interações exige um fornecedor/plano com eventos personalizados. Se a V1 permanecer em Hobby, é aceitável lançar com mensuração reduzida; não codificar eventos em URLs para contornar a limitação.

A taxonomia de eventos pode ser implementada por uma camada própria desacoplada do fornecedor, para que a decisão de ferramenta não contamine o domínio.

---

## 7A. Higiene documental executada

Cinco cópias antigas que ainda estavam associadas a `docs/` foram movidas para `docs/archive/` e renomeadas com prefixo `historico-2026-08-13-`:

- `04-metodologia-dados.md`;
- `09-fontes-referencias.md`;
- `10-testes-validacao.md`;
- `decisoes.md`;
- `README.md`.

Nenhuma foi apagada. A medida reduz risco de busca recuperar versão antiga como se fosse canônica.

---

## 8. Não exige Codex

Ainda pode ser feito em ChatGPT + Drive:

1. concluir pesquisa D068/D069/D070 quando os valores oficiais puderem ser obtidos;
2. revisar e atualizar fontes;
3. ajustar microcopy;
4. revisar página pública de metodologia;
5. revisar política de privacidade;
6. definir controlador/contatos quando o responsável decidir;
7. escolher analytics após confirmar plano e requisitos;
8. definir domínio e Search Console;
9. auditar consistência documental.

---

## 9. Exige ou beneficia fortemente de ambiente de execução

Deixar para Codex/repositório:

1. substituir constantes do protótipo antigo;
2. decompor `App.tsx`;
3. integrar CDF Brasil e manifesto de preços;
4. integrar motor Mundo depois de D068–D070;
5. implementar parser monetário robusto;
6. implementar validações dos inputs;
7. implementar compartilhamento;
8. implementar analytics escolhido;
9. adicionar rotas públicas;
10. rodar unit/integration/E2E;
11. lint/build/typecheck;
12. conferir bundle;
13. CI/CD;
14. commit/push/deploy.

---

## 10. Bloqueadores para entregar a V1 completa

### P0

- D068 — distribuição/quantis Mundo;
- D069 — conversão BRL corrente → PPP 2021;
- D070 — golden cases, caudas e regras finais de exibição Mundo;
- substituição do motor antigo no código;
- validação de inputs.

### P1 antes de divulgação pública ampla

- domínio/canonical;
- analytics ou decisão explícita de lançar sem analytics;
- política pública de privacidade preenchida;
- página pública de metodologia;
- compartilhamento;
- SEO técnico básico;
- testes de acessibilidade e E2E.

---

## 11. Regra de passagem para Codex

O projeto pode ir ao Codex antes de D068–D070 para preparar arquitetura e integrar **Brasil**, desde que:

- o resultado Mundo permaneça feature-flagged/bloqueado;
- nenhuma constante antiga seja preservada como fallback;
- nenhum número mundial provisório seja mostrado ao usuário.

Para uma implementação completa Brasil + Mundo em um único ciclo, esperar D068–D070.

---

## 12. Estado geral

```text
PRODUTO/UX.................. PRONTO PARA IMPLEMENTAÇÃO
BRASIL...................... PRONTO PARA IMPLEMENTAÇÃO
PRIVACIDADE................. PRONTA COMO CONTRATO
MUNDO....................... ~60–70% FECHADO; NÚCLEO NUMÉRICO PENDENTE
SEO/ANALYTICS............... ESPECIFICADO; OPERAÇÃO PENDENTE
FRONTEND.................... PROTÓTIPO ANTIGO / NÃO CANÔNICO NUMERICAMENTE
V1 COMPLETA................. AINDA BLOQUEADA PELO MUNDO + IMPLEMENTAÇÃO
```

## Coleta reprodutível do Mundo — Fase 2A

A execução que falta para D068–D070 já possui um coletor de pesquisa preparado em:

```text
scripts/research/world/collect-pip-world-evidence.R
```

O script usa o cliente oficial `pipr`, congela `20260324_2021_01_02_PROD`, ano 2024 e PPP 2021, captura benchmarks `pip wb` por `povline`, PPP e CPI, salva checksums e não canoniza decisões automaticamente.

Saída prevista:

```text
validation/world/pip-20260324-2021/
```

Esse caminho elimina nova pesquisa quando houver um ambiente com R + internet; a próxima etapa será executar, revisar as respostas e somente então decidir D068–D070.



---

# Anexo — Gate executivo para o motor Mundo

Este anexo consolida a sequência obrigatória antes de qualquer integração mundial no frontend.

## Ordem de execução

```text
fase-2a-metodologia-mundo.md
        ↓
fase-2b-protocolo-validacao-cdf-mundo.md
        ↓
fase-2c-protocolo-conversao-brl-ppp2021.md
        ↓
moldes-decisoes-d068-d070.md
        ↓
D068 + D069 + D070 ATIVAS
        ↓
integração Mundo liberada
```

Documento de navegação:

```text
pacote-execucao-mundo.md
```

## Gate D068 — distribuição mundial

Só marcar como `PASS` quando:

- [ ] o arquivo oficial `DR0094423` tiver sido processado para 2024;
- [ ] `welf` e `pop` tiverem unidade e domínio confirmados;
- [ ] a CDF candidata for monotônica e determinística;
- [ ] os headcounts derivados forem comparados contra `pip wb` em múltiplos `povline`;
- [ ] o erro tiver sido medido antes da escolha da precisão visual;
- [ ] o benchmark pré-registrado de US$ 3,00 / 2024 / Mundo = 846,76 milhões tiver sido reproduzido dentro da tolerância justificada;
- [ ] a representação por bins tiver sido aceita ou rejeitada explicitamente;
- [ ] o artefato derivado possuir manifesto e checksum.

## Gate D069 — conversão BRL → PPP 2021

Só marcar como `PASS` quando:

- [ ] `ppp` e `cpi` forem obtidos da mesma release PIP congelada;
- [ ] o Brasil for identificado explicitamente nas tabelas;
- [ ] unidades e referências temporais estiverem documentadas;
- [ ] a fórmula final tiver sido reproduzida com ida e volta;
- [ ] linearidade e monotonicidade passarem;
- [ ] a equivalência ou não com qualquer etapa de D065 estiver demonstrada;
- [ ] `PA.NUS.PRVT.PP`/ICP forem usados apenas como sanity check;
- [ ] nenhuma constante antiga do `src/App.tsx` entrar por herança.

## Gate D070 — golden cases e apresentação

Só marcar como `PASS` quando:

- [ ] D068 estiver ativa;
- [ ] D069 estiver ativa;
- [ ] golden cases estiverem congelados;
- [ ] empates estiverem definidos;
- [ ] cauda inferior estiver documentada;
- [ ] cauda superior estiver documentada;
- [ ] precisão visual resultar do erro observado em D068;
- [ ] nenhuma extrapolação arbitrária for utilizada;
- [ ] linguagem permanecer subordinada a D067;
- [ ] testes de regressão estiverem especificados.

## Regra de transição

Enquanto qualquer um destes gates estiver aberto:

```text
WORLD_FRONTEND_INTEGRATION_ALLOWED = false
```

Quando D068, D069 e D070 estiverem ativas e os respectivos gates passarem:

```text
WORLD_FRONTEND_INTEGRATION_ALLOWED = true
```

Essa mudança deve ser explícita em manifesto/decisão. Não inferir autorização apenas porque existem arquivos de dados disponíveis.
