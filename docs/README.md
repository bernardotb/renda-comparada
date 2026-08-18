# Renda Comparada — Índice da Documentação

**Última revisão:** 18/08/2026
**Estado:** V1 em preparação; motor Brasil integrado ao frontend; Mundo parcialmente canonizado, com D068 validada apenas como candidata e integração numérica bloqueada.

Este diretório contém a documentação de autoridade do projeto. Ele deve ser lido antes de alterações relevantes de produto, dados, UX ou implementação.

---

## 1. Regra principal

> **A fase determina o trabalho. O backlog não aumenta o escopo da V1.**

Não implementar uma ideia apenas porque ela aparece em documentação de visão ou roadmap.

Para a V1, o `02-prd-v1.md` define o escopo funcional. Para dados e fórmulas, `04-metodologia-dados.md` prevalece. Para decisões já tomadas, consultar `decisoes.md`.

Quando uma regra metodológica não estiver fechada:

> **não adivinhar, não reutilizar constante antiga e não preencher por plausibilidade.**

---

## 2. Ordem de leitura

1. `01-visao-produto.md` — tese e limites do produto;
2. `02-prd-v1.md` — escopo da V1;
3. `03-jornada-ux-v1.md` — sequência e comportamento da experiência;
4. `04-metodologia-dados.md` — fonte de autoridade para dados, fórmulas e estatística;
5. `05-design-system.md` — direção visual e hierarquia de apresentação;
6. `06-privacidade-seguranca.md` — regras de dados do usuário e segurança;
7. `07-seo-analytics-crescimento.md` — aquisição, medição e compartilhamento;
8. `08-roadmap-backlog.md` — ideias futuras; **não é escopo automático**;
9. `09-fontes-referencias.md` — fontes oficiais e classificação;
10. `10-testes-validacao.md` — contrato de qualidade e regressão;
11. `decisoes.md` — registro canônico de decisões e substituições.

O arquivo raiz `AGENTS.md` contém as regras operacionais para agentes que trabalham no repositório.

---

## 3. Produto V1

Fluxo canônico:

```text
renda mensal atual + moradores
↓
resultado Brasil
↓
resultado Mundo estimado
↓
interpretação
↓
compartilhamento
↓
fim da experiência principal
↓
continuação financeira opcional
```

Princípios:

- comparação de **renda**, não patrimônio;
- sem cadastro obrigatório;
- Brasil antes de Mundo;
- compartilhamento antes do check-up;
- renda não aparece no compartilhamento padrão;
- check-up financeiro completo está fora do escopo obrigatório da V1.

---

## 4. Brasil — estado

**Status: pacote de dados integrado ao frontend.** Isso não declara a aplicação completa pronta para produção nem autoriza deploy.

Fonte:

```text
IBGE — PNAD Contínua
Rendimento de Todas as Fontes 2025
release 20260508
```

Construção canônica — D063:

```text
RDPC_real_2025 =
    soma_domiciliar(
        VD4019 × CO1
        +
        VD4048 × CO1e
    )
    ÷ VD2003
```

Peso:

```text
V1032
```

A CDF brasileira foi construída, validada, testada e possui golden cases.

O artefato canônico está materializado em:

```text
data/production/brazil/brazil-income-cdf-2025.json
```

Verificação após promoção ao Drive em 14/08/2026:

```text
size = 3955036 bytes
SHA-256 = 5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5
```

O arquivo foi reproduzido a partir do dataset processado validado e coincidiu byte a byte com o SHA originalmente congelado.

O contrato atual de integração Brasil é:

```text
data/production/brazil/brazil-income-engine-manifest.json
```

Esse manifesto combina, sem modificar os artefatos originais:

- CDF imutável da PNAD 2025;
- alinhamento temporal D065;
- precisão visual D071.

A CDF original contém um flag histórico de integração bloqueada porque foi gerada antes de D065. **Não editar a CDF para mudar esse flag.** O manifesto de motor registra a promoção posterior e preserva o SHA da CDF.

O Gate G0 regenerou os manifestos por script determinístico e executou uma suíte nova e explícita de **44/44 checks PASS**. Os relatórios estão em `validation/brazil/brazil-production-package-validation.{json,md}`. A alegação histórica `21/21 PASS` não foi preservada, porque os 21 itens e os relatórios originais não foram encontrados. O Gate G1 adicionou a validação específica do contrato de integração frontend.

O Gate G2 foi registrado como **PASS COM RESSALVAS** no histórico operacional. As verificações dinâmicas que não puderam ser executadas permanecem não verificadas e não são apresentadas como PASS. Esse registro não comprova deploy público.

Schemas verificáveis:

```text
config/schemas/brazil-price-alignment.schema.json
config/schemas/brazil-income-engine-manifest.schema.json
```

### D072 — entrega da CDF

A CDF possui 3.955.036 bytes brutos e 1.788.882 bytes em gzip -9 local. O lookup é barato; o custo relevante é a primeira transferência. Por isso, D072 determina:

- não embutir a CDF no bundle inicial;
- carregar o arquivo estático no primeiro cálculo;
- reutilizá-lo em memória nas simulações seguintes;
- nunca enviar renda/moradores na requisição do dataset;
- falhar com segurança, sem fallback antigo.

O frontend implementa esse contrato por um processo reproduzível que valida e copia os três artefatos canônicos para a área pública do build. Manifesto, alinhamento e CDF são solicitados no primeiro cálculo; hashes, tamanhos e consistência cruzada são verificados no navegador; o runtime compilado é então mantido em memória.

Os números de tamanho e o diagnóstico local de desempenho permanecem registrados em D072. Não existe relatório autônomo `brazil-cdf-delivery-performance` neste checkout; portanto, ele não é tratado como artefato de validação do Gate G0.

### D073 — metadata e share genérico

Também estão fechados para a home V1:

- `<title>`;
- meta description;
- `og:title`;
- `og:description`;
- texto padrão de compartilhamento sem posição.

Continuam abertos apenas `PRODUCTION_DOMAIN`, URL canônica, `DEFAULT_OG_IMAGE` e configuração de Search Console.

Alinhamento temporal — D065:

```text
renda nominal atual
↓
IPCA nacional oficial
↓
preços médios de 2025
↓
lookup na CDF 2025
```

O manifesto canônico de preços está em:

```text
data/production/brazil/brazil-price-alignment.json
```

### D071 — apresentação Brasil

A precisão visual brasileira também está fechada:

```text
faixa principal: percentil inteiro + TOP inteiro complementar
TOP entre 0,1% e 1%: uma casa decimal
TOP abaixo de 0,1%: mostrar < 0,1%
acima do máximo observado: sem extrapolação
RDPC zero: sem headline TOP 100%
```

Essa regra pertence somente à apresentação. A CDF conserva precisão interna completa.

### Proibido para produção Brasil

- `VD5011 × CO1` como construção principal;
- distribuição PIP usada como distribuição brasileira;
- médias nacionais usadas para inferir percentil;
- pesos iguais por registro;
- constantes hardcoded do protótipo antigo.

---

## 5. Mundo — estado

**Status: parcialmente canonizado; integração numérica bloqueada.** Pesquisa, scripts, testes e artefatos em `validation/world/` não equivalem a canonização, produção ou integração.

| Item | Estado no checkout | Autoridade/evidência |
|---|---|---|
| D066 | **ATIVA / CANÔNICA** | `decisoes.md` |
| D067 | **ATIVA / CANÔNICA** | `decisoes.md` |
| D068 | **EXECUTADA E VALIDADA COMO CANDIDATA; NÃO CANÔNICA** | `research/fase-2a-d068-execucao-2026-08-17.md` e `../validation/world/world-cdf-validation.md` |
| D069 | **NÃO EXECUTADA; NÃO CANÔNICA** | existe protocolo, mas não relatório de execução; a proveniência dos raws oficiais PIP `aux/ppp` e `aux/cpi` permanece pendente |
| D070 | **NÃO EXECUTADA; NÃO CANÔNICA** | existe molde/protocolo, sem relatório de execução ou decisão ativa |
| Produção Mundo | **BLOQUEADA** | não existe pacote autorizado em `data/production/world/` |
| Frontend Mundo | **BLOQUEADO / NÃO INTEGRADO** | nenhuma decisão ou manifesto autorizador permite resultado numérico |

D066 congela a versão/build PIP, o ano global de 2024 e a base PPP 2021. D067 define o resultado como **posição monetária global estimada**, baseada na distribuição harmonizada do PIP, que combina renda ou consumo domiciliar per capita conforme a fonte nacional.

A execução D068 construiu uma CDF candidata reproduzível a partir da `1000 Binned Global Distribution` e mediu seu erro contra 18 checkpoints oficiais. A aceitação da aproximação intrabin ainda exige revisão humana e decisão explícita. Nenhum valor mundial provisório deve entrar no frontend.

---

## 6. Frontend atual

O `src/App.tsx` preserva a direção visual do protótipo, mas o caminho ativo Brasil usa os módulos testáveis de domínio e carregamento em `src/brazil/`. O código continua subordinado à metodologia canônica.

Constantes antigas como:

```text
BRAZIL_THRESHOLDS
WORLD_CURVE
PPP_2021_BRL
BRAZIL_CPI_2024
```

não participam mais do caminho ativo e não são usadas como fallback. Mundo aparece apenas em estado explícito de indisponibilidade, sem número provisório.

---

## 7. Privacidade V1

Contrato atual:

- cálculo individual preferencialmente no navegador;
- sem renda em URL;
- sem renda em analytics;
- sem renda em `localStorage` ou `sessionStorage`;
- sem persistência do cálculo por padrão;
- sem renda em logs ou error tracking;
- compartilhamento padrão genérico;
- posição individual somente mediante ação explícita.

Pendências operacionais legítimas:

```text
CONTROLADOR = [DEFINIR]
PRIVACY_CONTACT = [DEFINIR]
SECURITY_CONTACT = [DEFINIR]
```

Não preencher esses campos por inferência.

---

## 8. SEO e analytics

A taxonomia e as restrições de analytics estão especificadas, mas o fornecedor ainda não foi canonizado.

```text
ANALYTICS_PROVIDER = [DEFINIR]
PRODUCTION_DOMAIN = [DEFINIR]
SEARCH_CONSOLE_PROPERTY = [CONFIGURAR]
```

Vercel Web Analytics foi estudado como candidato. A documentação oficial confirma que Web Analytics existe no Hobby, mas eventos personalizados são recurso de Pro/Enterprise. Portanto, a escolha depende do plano efetivamente utilizado e da decisão operacional final.

---

## 8A. Registro histórico externo — acesso do Google Drive

Em 14/08/2026, uma pesquisa externa registrou que os metadados da pasta então inspecionada e do arquivo `.env.local` indicavam:

```text
permission.type = anyone
permission.role = writer
allowFileDiscovery = false
```

Esse achado não foi revalidado pelo Gate G0 e não descreve o checkout Git atual. Se ainda vigente no sistema externo, significaria que qualquer pessoa com o link poderia editar o material e que o `.env.local` herdaria esse acesso.

### Regra de segurança

- tratar como **P0 operacional**;
- restringir o acesso antes de usar o Drive como fonte canônica compartilhada em produção;
- não assumir que compartilhamento público é necessário para ChatGPT, Codex ou conectores autorizados;
- não abrir nem copiar segredos do `.env.local` para documentação;
- após restringir o acesso, avaliar rotação de credenciais que possam ter ficado expostas;
- verificar se os conectores autorizados continuam funcionando com acesso restrito.

O agente não deve alterar permissões por conta própria sem decisão explícita do responsável.

---

## 9. Pesquisa e artefatos auxiliares

`research/` contém investigações que podem ser não canônicas.

Um relatório de pesquisa **não altera** automaticamente metodologia ou decisões.

`research/artifacts/` preserva evidências e manifestos de pesquisa.

Documento de prontidão atual:

```text
research/gate-pre-codex-v1.md
```

---

## 10. Regra para implementação futura

Antes de usar o Codex ou outro agente de código:

1. ler esta ordem documental;
2. não reabrir D063/D065 sem evidência;
3. não mostrar Mundo enquanto D068–D070 estiverem bloqueadas;
4. manter Brasil e Mundo como pipelines metodologicamente distintos;
5. preservar e ampliar os testes do contrato Brasil ao alterar a integração;
6. preservar privacidade como requisito de domínio, não como detalhe de UI;
7. não promover itens do backlog sem decisão explícita.

---

## 11. Próximo gate

O próximo gate recomendado é **fechar a execução e a proveniência de D069**. Depois disso, D068 e D069 candidatas devem passar por revisão humana e eventual canonização explícita antes da execução de D070. Este índice apenas identifica a sequência; não autoriza nenhuma dessas etapas.

O motor Brasil está integrado. A experiência completa Brasil + Mundo continua bloqueada para produção enquanto as decisões e os manifests autorizadores do Mundo não existirem.
