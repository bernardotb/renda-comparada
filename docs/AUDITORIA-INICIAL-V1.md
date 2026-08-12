# AUDITORIA-INICIAL-V1

**Produto:** Renda Comparada  
**Data da auditoria:** 12/08/2026  
**Escopo:** documentação canônica, código-fonte local, artefato publicado na Vercel e verificações não destrutivas  
**Estado:** diagnóstico; nenhuma correção ou funcionalidade implementada

## A. Resumo executivo

O site atual é um protótipo visual funcional, mas **não pode ser considerado a V1 metodologicamente validada**.

A interface calcula localmente, é responsiva, apresenta Brasil e Mundo com boa hierarquia e não contém mecanismo de persistência ou analytics. Entretanto, os percentis de produção são gerados por constantes e vetores inseridos diretamente em `src/App.tsx`, sem pipeline, datasets versionados, manifestos, checksums ou testes.

Os principais bloqueadores são:

1. **P0 — Brasil:** o código não utiliza a distribuição ponderada da PNAD Contínua 2025 exigida pela documentação. Ele utiliza 99 cortes de uma distribuição PIP 2024 inseridos manualmente.
2. **P0 — conversão internacional:** a fórmula BRL → PPP está hardcoded e não possui validação ou proveniência reproduzível. Uma escolha alternativa plausível da série oficial altera materialmente os resultados, demonstrando que a decisão precisa ser fechada antes da produção.
3. **P0 — entrada monetária:** valores com ponto ou centavos podem ser multiplicados por 100. No teste real, `6500.50` virou `650.050`.
4. **P0 — moradores:** o campo aceita valor fracionado. No teste real, `2.5` foi calculado sem erro.
5. **P0 — caudas e interpolação:** existem extrapolações, pisos e tetos arbitrários não aprovados pela metodologia.
6. **P1 — jornada:** não existem CTA de cálculo, compartilhamento, página pública de metodologia, estados de erro ou continuação opcional.
7. **P1 — governança:** há duas cópias locais ligadas ao mesmo projeto Vercel. A pasta indicada como oficial contém a documentação e o código, mas não possui os manifestos de build na raiz; a pasta de trabalho que gerou o deploy possui os manifestos e Git, porém nenhum commit.
8. **P1/P2 — qualidade:** não existem testes, lint, CI/CD, datasets externos nem histórico Git utilizável.

**Recomendação:** não divulgar amplamente nem tratar os percentis atuais como oficiais do Renda Comparada. A primeira fase deve consolidar uma única raiz do projeto e fechar a metodologia; a interface deve permanecer congelada até existirem datasets validados e golden cases aprovados.

## B. Arquitetura atual

### B.1 Stack

| Camada | Implementação atual |
|---|---|
| Interface | React 19.2.8 + React DOM 19.2.8 |
| Linguagem | TypeScript 7.0.2 |
| Build | Vite 8.2.1 + `@vitejs/plugin-react` 6.0.5 |
| Ícones | `lucide-react` 1.31.0 |
| Gerenciador | pnpm; lockfile versão 9 |
| Hospedagem | Vercel, projeto `renda-familiar-brasil-mundo` |
| Arquitetura web | SPA estática, renderizada integralmente no cliente |
| Backend | inexistente |
| Banco de dados | inexistente |
| Router | inexistente |

As versões estão fixadas no lockfile, mas o `package.json` usa `latest` em todas as dependências, o que torna novas instalações menos previsíveis se o lockfile for perdido ou ignorado.

### B.2 Duas raízes locais

Foram encontradas duas cópias com `src/App.tsx`, `src/main.tsx`, `src/styles.css` e `public/favicon.svg` idênticos por SHA-256:

1. pasta indicada como oficial: `Tools and Knowlegde/Calculadora de renda`;
2. pasta de trabalho: `C:/Users/Usuario/OneDrive/Documentos/ChatGPT/3`.

As duas possuem o mesmo `projectId` e `orgId` da Vercel.

A pasta de trabalho contém:

- `package.json`;
- `pnpm-lock.yaml`;
- `index.html`;
- `vite.config.ts`;
- `tsconfig*`;
- `.git`;
- `.vercel`.

A pasta indicada como oficial não possui esses arquivos na raiz. Cópias aparecem indevidamente em `dist/assets`, misturadas a artefatos compilados. Por isso, executar `pnpm --dir <pasta-oficial> run build` falha por ausência de manifesto.

O Git da pasta de trabalho está em branch `master`, sem nenhum commit, e todos os arquivos de origem estão não rastreados. Não existe baseline recuperável por controle de versão.

### B.3 Estrutura funcional

```text
index.html
  ↓
src/main.tsx
  ↓
src/App.tsx
  ├─ constantes metodológicas inline
  ├─ funções matemáticas
  ├─ estado do formulário
  ├─ ResultCard
  └─ toda a home
  ↓
src/styles.css
```

Toda a lógica, conteúdo e quase toda a interface estão concentrados em um único componente. Somente `ResultCard` foi separado internamente no mesmo arquivo.

### B.4 Páginas e rotas

Existe apenas a rota `/`.

Os links `#top` e `#metodologia` são âncoras na mesma página. A URL `/metodologia` retorna HTTP 404. Não existem rotas para `/sobre` ou `/privacidade`.

### B.5 Build e deploy

Na raiz técnica completa, o build executa:

```text
tsc -b && vite build
```

O build passou em 12/08/2026 e produziu:

- HTML: 0,69 kB;
- CSS: 11,94 kB, 3,28 kB gzip;
- JavaScript: 205,39 kB, 65,44 kB gzip.

O site publicado responde por HTTPS e possui HSTS. Não existe `vercel.json` na raiz técnica completa, integração Git funcional ou workflow de CI identificado. O vínculo local da Vercel existe, mas o fluxo atual é essencialmente manual.

## C. O que já está correto

### C.1 Produto e cálculo básico

- **P1:** a renda total é dividida pelo número de moradores.
- **P1:** Brasil aparece antes de Mundo.
- **P1:** percentil e TOP percentual são matematicamente complementares antes do arredondamento.
- **P1:** o resultado utiliza linguagem aproximada na maior parte da interface.
- **P1:** existe explicação de que renda não é patrimônio.
- **P1:** o cálculo acontece em memória no navegador.

### C.2 Privacidade

- **P0:** não há código da aplicação usando `localStorage`, `sessionStorage` ou cookies.
- **P0:** renda e moradores não aparecem em URL, query string ou hash.
- **P0:** não há analytics, pixels, error tracking ou session replay no código-fonte.
- **P0:** o bundle não contém compartilhamento que possa expor renda.
- **P0:** a resposta HTTP da home não definiu cookie.
- **P0:** não foi encontrado segredo no código cliente ou no bundle. O token local da Vercel permanece apenas em `.env.local`, ignorado pelo Git e não exposto no HTML.

### C.3 Interface

- **P2:** um único H1 é utilizado.
- **P2:** `lang="pt-BR"` está configurado.
- **P2:** os campos possuem labels HTML.
- **P2:** controles nativos permitem uso por teclado.
- **P2:** existe foco visível.
- **P2:** a preferência `prefers-reduced-motion` é respeitada.
- **P2:** os cards empilham no celular.
- **P2:** não foi detectado overflow horizontal pelo DOM em 320 px.
- **P2:** não há fotos genéricas, confete, cassino ou gamificação.
- **P2:** a distinção Brasil/Mundo não depende somente da cor; existem títulos textuais.

### C.4 Fonte mundial — sanity check limitado

O ponto mundial de US$ 10 internacionais por pessoa/dia no vetor atual possui headcount de 52,69%. A consulta à API oficial do PIP para Mundo, ano 2024 e linha 10 retornou os mesmos 52,69%.

Isso confirma apenas um ponto do vetor. Não substitui manifesto, versão congelada, regressão completa ou validação da interpolação.

### C.5 Dependências

`pnpm audit --prod --audit-level=moderate` não encontrou vulnerabilidades conhecidas nas dependências travadas em 12/08/2026.

## D. Divergências críticas

### D.1 P0 — fonte brasileira incompatível com a V1

**Documentação canônica:** PNAD Contínua — Rendimento de Todas as Fontes 2025, com microdados, variável oficial, pesos, unidade pessoa, validação contra indicadores do IBGE e dataset derivado versionado.

**Código atual:** array `BRAZIL_THRESHOLDS` com 99 valores diários em PPP e texto que declara usar a distribuição nacional 2024 harmonizada pelo PIP.

Consequências:

- não há microdados PNAD 2025;
- não há variável de RDPC confirmada;
- não há peso amostral;
- não há visita registrada;
- não há filtros ou missing values documentados;
- não há validação contra a média oficial 2025;
- a interface atribui a fonte ao IBGE, mas o mecanismo numérico imediato é uma distribuição do PIP.

O resultado Brasil atual não atende D006–D009 nem a parte Brasil de `04-metodologia-de-dados.md`.

### D.2 P0 — conversão PPP/PPC não validada

O código define:

```text
PPP_2021_BRL = 2,4499
BRAZIL_CPI_2024 = 1,1929
BRL_PER_INTL_2024 = 2,4499 × 1,1929 = 2,92248571
```

Não há metadado, URL de origem, data de acesso, série ou teste que explique por que essa multiplicação é a transformação correta para a versão PIP usada.

A série oficial `PA.NUS.PRVT.PP` consultada para 2024 retorna aproximadamente `2,5244965` BRL por dólar internacional. Isso não prova sozinho qual fator a V1 deve usar, pois a compatibilização com preços e PPP 2021 precisa seguir a metodologia PIP. Porém, demonstra que existem alternativas oficiais conceitualmente diferentes e que a constante atual não pode ser aceita sem validação.

Análise de sensibilidade, **não resultado recomendado**:

| Entrada | Fator atual | Percentil BR atual | Percentil Mundo atual | Fator anual WDI 2024 | Percentil BR simulado | Percentil Mundo simulado |
|---|---:|---:|---:|---:|---:|---:|
| R$ 6.500 / 3 | 2,92249 | 67,90 | 76,63 | 2,52450 | 73,47 | 79,48 |
| R$ 12.000 / 3 | 2,92249 | 86,65 | 87,28 | 2,52450 | 89,41 | 89,43 |

A diferença material torna essa decisão bloqueadora.

### D.3 P0 — parsing monetário produz resultados incorretos

`readCurrency()` remove todos os caracteres que não sejam dígitos.

Teste na produção:

```text
entrada digitada: 6500.50
valor interpretado: 650.050
renda por pessoa com 3 moradores: R$ 216.683
```

O sistema não apresenta erro. Uma entrada comum pode gerar percentil quase máximo.

### D.4 P0 — moradores fracionados são calculados

O campo `type="number"` não possui validação de integridade aplicada ao estado. O teste com `2.5` foi aceito e alterou o cálculo sem mensagem.

Também não existe formulário, submissão, `required`, `aria-invalid` ou erro próximo ao campo.

### D.5 P0 — tratamento arbitrário das caudas

Brasil:

- abaixo do primeiro corte: escala linear com piso de 0,1%;
- acima do P99: extrapolação logarítmica baseada em fator 8;
- teto: 99,9%.

Mundo:

- abaixo de US$ 0,50/dia: escala proporcional com piso de 0,1%;
- acima de US$ 1.200/dia: retorno fixo de 99,99%.

Essas regras não constam como decisões aprovadas. A documentação exige não extrapolar silenciosamente e preferir falha segura.

### D.6 P0 — interpolação sem erro medido

Brasil interpola em log-renda entre 99 cortes. Mundo interpola em log-renda entre apenas 25 pontos.

Não existe:

- justificativa estatística registrada;
- comparação contra CDF direta;
- erro máximo;
- tolerância;
- regressão;
- teste de monotonicidade automatizado.

Os vetores são monotônicos na inspeção estática, mas isso não valida a aproximação.

### D.7 P0 — produção ativa com bloqueios metodológicos abertos

A documentação mantém `[CONFIRMAR]` ou `[DEFINIR]` para:

- visita PNAD;
- variável RDPC;
- peso;
- UF;
- deflator;
- referência de preços;
- ano global;
- tipo de estimativa global;
- conversão PPP;
- tratamento de renda zero;
- extremos;
- casas decimais.

Apesar disso, o site retorna números como se a cadeia estivesse fechada. Isso contraria a política de falha segura da própria especificação.

### D.8 P0/P1 — linguagem mundial mais forte que a evidência

O card mundial afirma:

> “Sua renda por pessoa é maior que a de...”

O PIP combina renda e consumo domiciliar, diferentes pesquisas e estimativas. O resultado deveria ser explicitamente uma posição monetária global estimada, não uma comparação homogênea de renda.

## E. Divergências importantes

### E.1 Jornada e funcionalidade — P1

- resultados aparecem imediatamente com renda fictícia predefinida de R$ 12.000 e 3 moradores;
- não existe estado inicial vazio;
- não existe botão “Descobrir minha posição”;
- o resultado muda a cada digitação;
- não existem mensagens de validação;
- não existe estado de processamento;
- não existe estado de indisponibilidade do dataset;
- não existe “Simular outra renda”;
- não existe compartilhamento nativo;
- não existe WhatsApp;
- não existe copiar link;
- não existe card social;
- não existe a frase “Sua renda não será mostrada” no momento de share;
- não existe continuação opcional pós-share.

Assim, a jornada para em `RESULTADO + INTERPRETAÇÃO` e não completa `COMPARTILHAMENTO`.

### E.2 Fonte, ano e conteúdo — P1

- a interface usa 2024; a especificação brasileira exige PNAD 2025;
- o nome da marca é “Renda em Duas Escalas”, não “Renda Comparada”;
- o H1 não segue a decisão D002;
- “Pessoas sustentadas por essa renda” diverge de “Quantas pessoas moram nesta casa?”;
- a média brasileira R$ 2.069 está hardcoded;
- populações Brasil e Mundo estão hardcoded;
- ano, versão e atualização não vêm de metadados;
- Our World in Data aparece como fonte operacional sem ser fonte primária do cálculo;
- não há página pública de metodologia.

### E.3 Arredondamento — P1/P2

O caso canônico `6500 / 3` é calculado internamente como `2166,666...`, mas a função monetária exibe zero casas decimais:

```text
R$ 2.167
```

A documentação exige `R$ 2.166,67` para esse caso.

O percentil mundial 99,99 é exibido com uma casa como `100,0%`, embora ainda existam pessoas calculadas acima. Isso cria contradição entre número e texto.

### E.4 SEO — P1/P2

Existe:

- `lang="pt-BR"`;
- `<title>`;
- meta description;
- um H1.

Falta:

- title canônico do PRD;
- canonical;
- Open Graph;
- Twitter Card;
- imagem social;
- `robots.txt`;
- `sitemap.xml`;
- rota `/metodologia`;
- página `/privacidade`;
- conteúdo principal no HTML inicial.

O HTML entregue contém apenas `<div id="root"></div>`. Todo o conteúdo indexável depende da renderização JavaScript no cliente.

### E.5 Analytics — P1

Não há provider nem eventos. Isso preserva privacidade, mas impede medir a métrica principal da V1:

```text
ações de compartilhamento / cálculos concluídos
```

Como `ANALYTICS_PROVIDER` permanece `[DEFINIR]`, a ausência deve ser tratada como bloqueio, não corrigida por instalação automática.

### E.6 Acessibilidade — P2

Resultados da inspeção:

- botões do stepper têm 42 × 42 px, abaixo do padrão interno de 48–56 px;
- link mobile de metodologia tem 40 px de altura;
- marca clicável tem 34 px de altura;
- link “Voltar ao topo” tem apenas 16 px de altura;
- textos auxiliares usam 11–12 px, abaixo da direção de leitura da V1;
- `.rank-note` apresentou contraste aproximado de 4,38:1 para texto de 11 px;
- texto do footer apresentou contraste aproximado de 4,24:1 para texto de 11 px;
- o nome acessível do campo de moradores é “Número de pessoas”, enquanto o label visível é “Pessoas sustentadas por essa renda”;
- a região inteira de resultados usa `aria-live="polite"` e é atualizada a cada digitação, com potencial de anúncios excessivos;
- não existem erros associados aos campos;
- o botão de metodologia usa `aria-expanded`, mas não referencia o painel por `aria-controls`.

Pontos positivos: elementos interativos nativos, foco visível, labels e texto equivalente aos gráficos.

### E.7 Design — P2

O layout acerta a hierarquia editorial, o uso de espaço, a proeminência dos números e o empilhamento mobile. As divergências relevantes são:

- Bricolage Grotesque + DM Sans em vez de Source Serif 4 + Inter;
- azul saturado `#1246C4` em vez do azul petróleo definido;
- verde e lime mais promocionais que a paleta canônica;
- sombra deslocada forte no bloco principal;
- radius de 28 px e uso recorrente de pílulas;
- cards de resultado totalmente preenchidos por cores saturadas;
- aparência mais próxima de produto digital promocional que de reportagem econômica sóbria.

Em 320 px, a linha de moradores comprime o label em várias linhas e aumenta a carga visual, embora não tenha sido detectado overflow horizontal pelo DOM.

### E.8 Segurança e infraestrutura — P2

A produção envia HSTS. Não foram encontrados nos headers da home:

- Content-Security-Policy;
- X-Content-Type-Options;
- Referrer-Policy;
- Permissions-Policy.

As fontes são carregadas do Google Fonts por `@import`, criando requisição externa e dependência de renderização. Isso não envia a renda digitada, mas precisa constar no inventário de terceiros e na política real.

### E.9 Repositório e build — P1

- pasta oficial não compila isoladamente;
- pasta técnica não contém documentação canônica;
- ambas apontam para o mesmo projeto Vercel;
- Git não possui commits;
- não há branch de produção rastreável;
- não há CI/CD;
- não há proteção contra deploy da pasta errada.

## F. Divergências menores

- **P3:** classe CSS `.period-switch` existe sem componente correspondente.
- **P3:** o texto “Cerca de X pessoas estão acima nesta régua” usa populações fixas sem versão visível.
- **P3:** o ícone do botão de metodologia permanece “+” quando os detalhes estão abertos.
- **P3:** `site-shell` usa `overflow: hidden`, o que pode mascarar overflow em vez de evidenciá-lo.
- **P3:** `compact()` pode produzir traduções pouco precisas como “1 bi”.
- **P3:** a documentação contém resíduos `$1`, referências a nomes de arquivos inexistentes e cercas Markdown inconsistentes.
- **P3:** o projeto alterna “renda familiar”, “renda da casa”, “pessoas sustentadas” e “moradores”; a terminologia precisa ser normalizada.

## G. Metodologia atual

### G.1 Entrada

Estado inicial:

```text
renda = 12.000
moradores = 3
```

Renda é lida por:

```text
Number(valor.replace(/\D/g, ""))
```

e limitada a:

```text
0 ≤ renda ≤ 100.000.000
```

Moradores são limitados nominalmente a:

```text
1 ≤ moradores ≤ 30
```

mas não são forçados a inteiro.

### G.2 Renda por pessoa

```text
perPerson = renda / max(1, moradores)
```

### G.3 Conversão utilizada para Brasil e Mundo

```text
PPP_2021_BRL = 2,4499
CPI_2024 = 1,1929
BRL_PER_INTL_2024 = 2,92248571
DAYS_PER_MONTH = 365 / 12

dailyIntl =
  perPerson
  / BRL_PER_INTL_2024
  / DAYS_PER_MONTH
```

Ou:

```text
dailyIntl = perPerson × 12 / 365 / 2,92248571
```

### G.4 Brasil

Dados:

- 99 cortes ordenados;
- primeiro: 1,8079 PPP$/dia;
- corte 50 aproximado: 16,9121 PPP$/dia;
- último: 173,5652 PPP$/dia;
- código e interface os associam à distribuição Brasil PIP 2024.

Entre dois cortes, o código interpola linearmente o percentil no logaritmo da renda:

```text
t = (ln(x) - ln(x1)) / (ln(x2) - ln(x1))
percentil = y1 + clamp(t, 0, 1) × (y2 - y1)
```

Abaixo do primeiro corte:

```text
percentil = clamp(x / P1, 0,1, 1)
```

Acima do P99:

```text
percentil = clamp(
  99 + ln(x / P99) / ln(8),
  99,
  99,9
)
```

### G.5 Mundo

Dados:

- 25 pares `[linha monetária diária, headcount mundial %]`;
- faixa de 0,50 a 1.200 PPP$/dia;
- headcount de 0,25% a 100%;
- população fixa: 8.141.808.945.

Entre pontos, utiliza a mesma interpolação logarítmica.

Abaixo do primeiro ponto:

```text
percentil = clamp(x / 0,5 × 0,25, 0,1, 0,25)
```

Acima do último:

```text
percentil = 99,99
```

### G.6 TOP e população acima

```text
top = 100 - percentil
pessoas_acima = round(top / 100 × população_fixa)
```

Populações usadas:

```text
Brasil = 211.998.573
Mundo = 8.141.808.945
```

### G.7 Arredondamento

- percentis: uma casa decimal;
- TOP: zero casas quando ≥ 10%; uma casa quando < 10%;
- renda por pessoa: zero casas decimais;
- pessoas acima: notação compacta com uma casa;
- cálculos internos usam `number` sem arredondamento intermediário explícito.

## H. Dados e fontes atuais

### H.1 Dados efetivamente usados pelo código

| Item | Local | Proveniência disponível |
|---|---|---|
| 99 cortes Brasil | `src/App.tsx` | comentário/texto de UI: PIP/PNAD 2024; sem arquivo-fonte ou manifesto |
| 25 pontos Mundo | `src/App.tsx` | compatível com headcounts PIP 2024 em sanity check parcial |
| PPP 2,4499 | `src/App.tsx` | sem metadado no repositório |
| CPI 1,1929 | `src/App.tsx` | sem metadado no repositório |
| população Brasil | `src/App.tsx` | coincide com reporting population PIP 2024 consultada |
| população Mundo | `src/App.tsx` | coincide com reporting population PIP 2024 consultada |
| média Brasil R$ 2.069 | JSX hardcoded | link IBGE 2024 |

### H.2 Links exibidos

- Banco Mundial — PIP;
- Our World in Data — limiares mundiais;
- IBGE — divulgação de rendimento domiciliar per capita 2024.

### H.3 Datasets e pipeline

Não existem no repositório:

- microdados raw;
- scripts de download;
- scripts de processamento;
- datasets processed;
- datasets production;
- manifestos;
- checksums;
- relatórios de validação;
- diffs de versões.

## I. Privacidade

### I.1 Dados financeiros que saem do processamento local

**Não foi encontrado envio de renda, moradores, renda per capita ou percentis pelo código da aplicação.**

O estado existe somente em memória React e desaparece no reload.

### I.2 Superfícies auditadas

| Superfície | Resultado |
|---|---|
| URL/query/hash | sem dados financeiros |
| localStorage | nenhum uso no código |
| sessionStorage | nenhum uso no código |
| cookies da aplicação | nenhum uso; home sem `Set-Cookie` |
| analytics | inexistente |
| logs do cliente | nenhum `console.log` da aplicação |
| error tracking | inexistente |
| requests de cálculo | inexistentes; cálculo local |
| Open Graph personalizado | inexistente |
| compartilhamento | inexistente |

### I.3 Terceiros e lacunas

- Vercel recebe as requisições normais de hospedagem e pode manter metadados técnicos, como IP e user-agent, conforme configuração da plataforma. Os painéis e prazos de retenção não são auditáveis apenas pelo repositório.
- Google Fonts recebe requisição para folhas/fontes. Nenhum valor digitado é anexado.
- não existe inventário de fornecedores implementado;
- não existe Política de Privacidade pública;
- `CONTROLADOR`, `PRIVACY_CONTACT` e `SECURITY_CONTACT` permanecem `[DEFINIR]`.

Conclusão: a arquitetura atual é favorável à privacidade, mas ainda não satisfaz a documentação operacional/jurídica da V1.

## J. Testes

### J.1 Testes existentes

Nenhum.

Não existem:

- arquivos `*.test.*` ou `*.spec.*`;
- Vitest/Jest;
- Playwright/Cypress;
- script `test`;
- script `lint`;
- CI;
- fixtures;
- golden cases;
- testes estatísticos;
- testes de privacidade automatizados.

### J.2 Verificações executadas nesta auditoria

- build da raiz técnica completa: passou;
- build da pasta indicada como oficial: falhou por ausência de `package.json`;
- auditoria de dependências de produção: nenhuma vulnerabilidade conhecida;
- produção `/`: HTTP 200;
- `/metodologia`, `/robots.txt` e `/sitemap.xml`: HTTP 404;
- viewport 320, 390 e 1280 px: inspecionados;
- parsing decimal: falhou;
- moradores fracionados: falhou;
- renda zero: retorna percentil mínimo 0,1% sem erro;
- contraste de textos críticos: dois casos abaixo de 4,5:1;
- sanity check PIP Mundo a US$ 10/dia: coincidiu em 52,69%.

Essas verificações não constituem suíte de regressão.

### J.3 Cálculos desprotegidos

Todos os cálculos estão desprotegidos, especialmente:

- parsing monetário;
- validação de moradores;
- renda por pessoa;
- conversão BRL → PPP;
- conversão mensal → diária;
- busca Brasil;
- interpolação Brasil;
- caudas Brasil;
- busca Mundo;
- interpolação Mundo;
- caudas Mundo;
- TOP percentual;
- população acima;
- arredondamento;
- consistência entre frase e número.

## K. Dívida técnica

1. **P0:** metodologia e dados dentro do componente visual.
2. **P0:** constantes sem versão/proveniência.
3. **P0:** nenhum pipeline reproduzível.
4. **P0:** nenhum teste estatístico.
5. **P1:** duas raízes ligadas ao mesmo deploy.
6. **P1:** Git sem commits.
7. **P1:** pasta oficial não compilável.
8. **P1:** toda a aplicação em `App.tsx`.
9. **P1:** ausência de domínio separado e funções exportáveis.
10. **P1:** ausência de tratamento de erro e indisponibilidade.
11. **P1:** ausência de share, SEO técnico e metodologia pública.
12. **P2:** dependências declaradas como `latest`.
13. **P2:** ausência de security headers além de HSTS.
14. **P2:** fonte externa por `@import`.
15. **P2:** conteúdo SEO exclusivamente client-side.
16. **P2:** documentação referencia nomes de arquivos diferentes dos existentes.
17. **P3:** CSS não utilizado e terminologia inconsistente.

## L. Plano recomendado

Nenhuma fase abaixo deve começar automaticamente. A fase escolhida precisa ser autorizada.

### Fase 0 — Consolidar a fonte de verdade do repositório

**Objetivo:** escolher uma única raiz compilável, preservar documentação e criar baseline Git antes de qualquer mudança funcional.

**Arquivos afetados:** raiz do projeto, manifestos, `.gitignore`, `/docs`; nenhum cálculo precisa mudar.

**Dependências:** decisão sobre qual pasta será canônica e como o deploy Vercel será vinculado.

**Riscos:** sobrescrever a cópia mais completa ou perder vínculo de deploy.

**Testes:** comparação de hashes, build limpo, preview local, confirmação do projectId.

**Critério de conclusão:** uma única raiz contém código, docs, manifestos e Git; build reproduzível; primeiro commit criado; nenhuma divergência entre cópias.

### Fase 1 — Fechar metodologia Brasil e construir pipeline PNAD 2025

**Objetivo:** produzir a CDF brasileira ponderada e validada.

**Arquivos afetados:** novos diretórios de pipeline/data/validation, configuração metodológica e atualização explícita de `04-metodologia-de-dados.md` e `decisoes.md`.

**Dependências:** arquivo PNAD, visita, variável RDPC, peso, filtros, missing, renda zero, deflator e referência de preços aprovados.

**Riscos:** unidade estatística errada, peso incorreto, quebra de comparabilidade, exposição acidental de microdados no bundle.

**Testes:** schema, pesos, média ponderada, mediana, P10–P99, reprodução de indicadores IBGE, monotonicidade, checksum e reprodutibilidade.

**Critério de conclusão:** pipeline reproduz R$ 2.316 no conceito compatível dentro de tolerância documentada; CDF possui manifesto/checksum; revisão metodológica aprovada.

### Fase 2 — Fechar metodologia Mundo e construir lookup PIP

**Objetivo:** congelar versão/ano/tipo de estimativa, validar PPP e gerar CDF mundial reproduzível.

**Arquivos afetados:** pipeline PIP, configuração PPP, dataset global, manifestos, validação e documentação metodológica.

**Dependências:** decisão sobre `GLOBAL_REFERENCE_YEAR`, `GLOBAL_ESTIMATION_TYPE`, série PPP e tratamento temporal.

**Riscos:** mistura renda/consumo, nowcast não declarado, fator PPP invertido, cobertura global incompleta.

**Testes:** linhas de pobreza conhecidas, monotonicidade, headcounts PIP, conversão mensal/diária, limites e tolerâncias.

**Critério de conclusão:** lookup reproduz headcounts oficiais selecionados dentro de tolerância aprovada e possui manifesto/checksum.

### Fase 3 — Extrair domínio e criar golden cases

**Objetivo:** retirar fórmulas da UI e criar funções puras.

**Arquivos afetados:** módulos de domínio, adaptadores de dataset, fixtures e testes unitários.

**Dependências:** fases 1 e 2 concluídas.

**Riscos:** alterar silenciosamente resultados durante refactor.

**Testes:** renda por pessoa, moeda, percentis, TOP, monotonicidade, empates, extremos e golden cases versionados.

**Critério de conclusão:** UI consome apenas API de domínio; nenhuma constante metodológica permanece em componente; suíte passa.

### Fase 4 — Corrigir formulário e estados da jornada

**Objetivo:** implementar estado inicial vazio, CTA, parsing pt-BR e erros acessíveis.

**Arquivos afetados:** componentes de formulário, estilos e testes de interação.

**Dependências:** decisão sobre renda zero, centavos e limites máximos.

**Riscos:** regressão mobile, interpretação ambígua de ponto/vírgula.

**Testes:** colagem, centavos, ponto, vírgula, vazio, negativo, extremos, moradores inteiros e foco em erro.

**Critério de conclusão:** casos de `10-testes-validacao.md` passam; nenhum input ambíguo produz resultado silencioso.

### Fase 5 — Resultado, interpretação e compartilhamento privado

**Objetivo:** alinhar linguagem Brasil/Mundo e completar a jornada até o share.

**Arquivos afetados:** cards, interpretação, `ShareActions`, textos e card social genérico.

**Dependências:** texto padrão de share e nível de precisão aprovados.

**Riscos:** exposição de renda/resultado, afirmação estatística incorreta, falhas Web Share.

**Testes:** Web Share, WhatsApp, copiar link, cancelamento, ausência de renda/moradores, coerência percentil/TOP.

**Critério de conclusão:** share aparece após interpretação, funciona com fallback e não revela dados financeiros.

### Fase 6 — Metodologia pública, SEO, analytics e segurança

**Objetivo:** criar rotas públicas, metadata e mensuração mínima privada.

**Arquivos afetados:** roteamento/geração estática, `/metodologia`, `/privacidade`, metadata, robots, sitemap, headers e analytics aprovado.

**Dependências:** domínio, provider, controlador, contatos, OG e política pública definidos.

**Riscos:** indexação de preview, tracking excessivo, políticas jurídicas divergentes do sistema.

**Testes:** HTML inicial, canonical, OG, sitemap, robots, payloads analytics, falha de analytics, headers e teste sentinela.

**Critério de conclusão:** requisitos SEO/privacidade passam e nenhum evento contém dado financeiro.

### Fase 7 — Alinhar design, acessibilidade e performance

**Objetivo:** aplicar o design system canônico sem alterar resultados.

**Arquivos afetados:** tokens, tipografia, componentes, CSS e fontes.

**Dependências:** identidade visual final e arquitetura de fontes aprovadas.

**Riscos:** perda da personalidade atual, regressão mobile ou contraste.

**Testes:** 320/360/390/430/768/1024/1280+, zoom 200%, teclado, leitor de tela, contraste, reduced motion e Core Web Vitals.

**Critério de conclusão:** checklist visual e WCAG básico aprovado; jornada principal permanece rápida.

### Fase 8 — Release controlada da V1

**Objetivo:** publicar somente a cadeia validada.

**Arquivos afetados:** configuração de CI/CD, evidências de validação e release.

**Dependências:** fases anteriores aprovadas.

**Riscos:** deploy da pasta errada, mudança silenciosa de dataset, preview indexável.

**Testes:** CI completo, preview, regressão, privacidade, SEO, E2E e smoke pós-deploy.

**Critério de conclusão:** versão, datasets, metodologia, testes e deploy são rastreáveis; produção reproduz o preview aprovado.

## M. Bloqueios

### M.1 Metodologia Brasil — P0

- `IBGE_VISIT`;
- `IBGE_RDPC_VARIABLE`;
- `IBGE_WEIGHT_VARIABLE`;
- `IBGE_UF_VARIABLE`;
- filtros/população-alvo;
- tratamento de missing e códigos especiais;
- renda zero;
- deflator;
- referência de preços;
- regra de empates;
- extremos;
- precisão exibida.

### M.2 Metodologia Mundo — P0

- versão completa PIP a congelar;
- ano global;
- survey/interpolação/nowcast/projeção;
- série e fórmula PPP/PPC;
- referência temporal dos BRL informados;
- método de construção da CDF;
- densidade do lookup;
- interpolação e tolerância;
- caudas;
- linguagem final renda/consumo.

### M.3 Produto e conteúdo — P1

- nome final da marca no código;
- aplicação da decisão D002 ao H1;
- modo único ou duplo de compartilhamento;
- texto padrão de share;
- precisão percentil/TOP;
- CTA pós-resultado;
- conteúdo e escopo da ponte opcional.

### M.4 Governança e infraestrutura — P1

- pasta canônica;
- estratégia Git/branch;
- integração/deploy Vercel;
- domínio de produção;
- ambientes preview e produção;
- provider de analytics;
- propriedade Search Console.

### M.5 Privacidade e segurança — P1/P2

- controlador;
- contato de privacidade;
- contato de segurança;
- Política de Privacidade pública;
- inventário de terceiros;
- retenção de logs Vercel;
- headers de segurança;
- política para Google Fonts;
- imagem Open Graph padrão.

## Conclusão

O protótipo comprova a direção visual e a viabilidade de cálculo local, mas o número produzido hoje não possui a cadeia de evidência exigida pela própria V1.

A ordem segura é:

```text
consolidar repositório
↓
fechar metodologia
↓
construir e validar datasets
↓
isolar domínio e criar testes
↓
completar jornada, share, SEO e acessibilidade
↓
publicar
```

Nenhuma fase foi implementada nesta auditoria.
