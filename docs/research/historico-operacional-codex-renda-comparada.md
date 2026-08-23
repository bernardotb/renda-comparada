---
title: "Histórico Operacional do Codex — Renda Comparada"
created: 2026-08-18
updated: 2026-08-18
status: "histórico operacional"
canonical: false
scope: "reconstrução da evolução técnica, documental e metodológica observada nas conversas históricas do Codex"
---

# Histórico Operacional do Codex — Renda Comparada

> **DOCUMENTO HISTÓRICO E OPERACIONAL — NÃO CANÔNICO**
>
> Este documento resume a evolução do projeto Renda Comparada observada nas conversas históricas do Codex.
>
> Seu objetivo é preservar a lógica de trabalho, os gates, as transições, os controles e as principais evidências técnicas sem exigir que agentes futuros leiam conversas brutas do Codex.
>
> Este documento não substitui:
>
> - `AGENTS.md`;
> - `docs/README.md`;
> - documentos canônicos temáticos;
> - `docs/decisoes.md`;
> - manifestos;
> - schemas;
> - relatórios de validação;
> - checkout Git/local.
>
> Em caso de divergência, prevalece a fonte de autoridade aplicável ao tema e o checkout para o estado real da implementação.

---

# 1. Objetivo deste documento

Durante o desenvolvimento do Renda Comparada, o Codex participou de várias etapas sucessivas:

```text
investigação metodológica
↓
pipeline Brasil
↓
CDF Brasil
↓
alinhamento temporal
↓
reconciliação documental
↓
pacote de produção Brasil
↓
integração frontend
↓
hardening
↓
validação dinâmica
↓
pesquisa e execução experimental Mundo
```

As conversas do Codex registraram estados intermediários diferentes.

Por isso, usar diretamente as conversas como contexto para uma LLM pode causar confusão entre:

- proposta;

- execução;

- validação;

- canonização;

- integração;

- produção.


Este documento consolida somente a lógica e os marcos relevantes.

---

# 2. Regra epistemológica central

Durante toda a evolução do projeto, uma distinção tornou-se essencial:

```text
PESQUISADO
≠
EXECUTADO
≠
VALIDADO
≠
CANONIZADO
≠
INTEGRADO
≠
PUBLICADO
```

Um resultado técnico pode estar correto e ainda não possuir autorização para produção.

Uma pesquisa pode produzir evidência forte e ainda permanecer em `docs/research/`.

Um script pode existir sem que sua metodologia tenha sido canonizada.

Um artefato pode ter sido validado sem estar integrado ao frontend.

Uma integração pode existir no checkout sem que o produto completo esteja pronto para deploy.

Essa separação deve permanecer permanente no projeto.

---

# 3. Modelo de trabalho que emergiu

A evolução do projeto consolidou um fluxo de trabalho preferencial:

```text
PESQUISA
↓
EVIDÊNCIA
↓
DECISÃO
↓
CANONIZAÇÃO
↓
IMPLEMENTAÇÃO
↓
TESTES
↓
AUDITORIA
↓
PRÓXIMO GATE
```

O projeto não deve pular etapas apenas porque a próxima solução parece evidente.

Especialmente:

> a disponibilidade de dados ou scripts não autoriza automaticamente o avanço de fase.

---

# 4. Separação entre ChatGPT e Codex

A experiência acumulada estabeleceu uma divisão operacional.

## ChatGPT

Deve resolver preferencialmente:

- pesquisa externa;

- leitura de fontes oficiais;

- metodologia;

- análise estatística independente;

- comparação de alternativas;

- produto;

- UX;

- copy;

- SEO;

- privacidade;

- riscos;

- critérios de aceite;

- planejamento de testes;

- preparação de decisões;

- preparação de prompts para Codex;

- auditoria das respostas do Codex.


## Codex

Deve ser utilizado quando o trabalho depender de:

- checkout real;

- código;

- arquivos locais;

- scripts;

- dependências;

- execução;

- testes;

- typecheck;

- build;

- Git;

- diff;

- commits;

- integração real.


Fluxo desejado:

```text
ChatGPT
pesquisa + análise + decisão + critérios
↓
Codex
implementação + execução + testes + diff
↓
ChatGPT
auditoria + decisão seguinte
```

Esse modelo existe para reduzir custo, contexto e uso desnecessário do Codex.

---

# 5. Princípios técnicos que se tornaram permanentes

Ao longo das fases, alguns princípios apareceram repetidamente.

## 5.1 Metodologia antes do código

O frontend não define metodologia.

A fórmula deve existir primeiro como contrato metodológico.

O código apenas a implementa.

## 5.2 Distribuição antes de percentil

Não inferir posição por:

- média;

- thresholds manuais;

- matéria jornalística;

- aproximação visual.


Percentil deve derivar de distribuição validada.

## 5.3 Reprodutibilidade

Uma transformação de dados de produção deve satisfazer conceitualmente:

```text
mesmo input
+
mesmo código
+
mesma configuração
=
mesmo output
```

Idealmente:

```text
mesmo SHA-256
```

## 5.4 Artefatos versionados

Datasets e manifestos importantes devem possuir:

- versão;

- proveniência;

- hash;

- schema;

- referência metodológica.


## 5.5 Falha segura

Ausência ou corrupção de artefato não deve produzir resultado aproximado.

O comportamento correto é:

```text
indisponibilidade
+
possibilidade de nova tentativa
```

e não:

```text
fallback legado
```

## 5.6 Privacidade por minimização

Renda e resultados financeiros individuais devem permanecer locais sempre que possível.

Não enviar esses valores para:

- URL;

- query;

- storage persistente;

- logs;

- analytics;

- headers;

- requisições de datasets.


---

# 6. Consolidação metodológica Brasil

A investigação brasileira resultou na construção protegida:

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

Unidade:

```text
pessoas elegíveis
```

Referência monetária:

```text
preços médios de 2025
```

Foram rejeitados como mecanismo principal:

```text
VD5011 × CO1
VD5008 × CO1
média nacional para inferir percentil
peso 1 por registro
thresholds manuais
```

A lógica metodológica resultou de investigação e falsificação de hipóteses anteriores, não de adaptação do código existente.

---

# 7. Higiene documental pós-validação metodológica

Antes da engenharia de dados, houve uma etapa de higiene.

Foram observados problemas como:

- movimentação acidental de README;

- timestamps externos;

- documentação com status antigo;

- README ainda dizendo que metodologia Brasil não estava validada.


A abordagem adotada foi conservadora:

1. identificar se a alteração era real ou apenas incidental;

2. restaurar o estado correto;

3. não incluir timestamp sem conteúdo;

4. atualizar somente informação legitimamente desatualizada;

5. criar commit documental isolado;

6. não iniciar a próxima fase automaticamente.


Commits históricos mencionados:

```text
44378e9
docs: update validation review date
```

e:

```text
11ee1a9
docs: update project status after Brazil validation
```

Esse episódio consolidou uma regra importante:

> documentação de estado deve acompanhar marcos reais, mas correção documental não autoriza automaticamente nova fase.

---

# 8. Fase 1D — pipeline Brasil reproduzível

A Fase 1D transformou a metodologia brasileira já validada em engenharia de dados.

Commit histórico:

```text
67c9a88
feat(data): build reproducible Brazil PNAD pipeline
```

Objetivo:

```text
PNAD oficial
↓
parsing controlado
↓
deflatores
↓
agregação domiciliar
↓
RDPC
↓
pessoas elegíveis
↓
dataset intermediário validado
```

Princípio central:

```text
mesmo raw
+
mesmo código
+
mesma configuração
=
mesmo dataset derivado
```

Foram utilizados controles como:

- SHA-256 do raw;

- validação de schema;

- variáveis explicitamente configuradas;

- chave domiciliar;

- join de deflatores;

- pesos;

- zeros;

- ausência de negativos;

- população;

- média;

- Gini;

- médias por UF;

- determinismo.


A Fase 1D não tinha autorização para:

- criar CDF de produção;

- integrar frontend;

- alterar `src/`;

- resolver Mundo.


---

# 9. Resultados importantes da Fase 1D

O dataset intermediário registrado historicamente possuía:

```text
408.243 registros
```

SHA-256:

```text
8A44A26C47F16BE54DE787D215145C60B82E33319F806A0F890411B799EDA469
```

Benchmarks:

```text
média ≈ 2264,0378278980
Gini ≈ 0,5112237274
população ≈ 212.624.284,8006
```

Foram relatadas:

```text
27/27 médias por UF reproduzidas
```

e duas execuções produziram o mesmo checksum.

Isso marcou a passagem de:

> metodologia comprovada em pesquisa

para:

> metodologia reproduzível automaticamente por software.

---

# 10. Fase 1E — CDF brasileira

A Fase 1E transformou o dataset intermediário em uma representação compacta da distribuição brasileira.

Commit histórico:

```text
fc8f028
feat(data): build validated Brazil income CDF
```

Artefato:

```text
data/production/brazil/brazil-income-cdf-2025.json
```

SHA-256:

```text
5FC02C5F328EA1DAD334BDE7E3921AEF17793E1F6BA4739A334276B2D6E609E5
```

Tamanho:

```text
3.955.036 bytes
```

Valores únicos:

```text
83.358
```

A CDF foi construída como distribuição empírica em degraus.

Semântica:

```text
shareBelow(x)
=
peso com RDPC < x
/
peso total
```

```text
shareAtOrBelow(x)
=
peso com RDPC <= x
/
peso total
```

```text
topShare(x)
=
1 - shareBelow(x)
```

---

# 11. Tratamento de empates e limites

Uma decisão importante da CDF foi não inventar ordem entre pessoas empatadas.

Se existe peso exatamente em `x`:

```text
shareBelow(x)
```

exclui esse peso.

```text
shareAtOrBelow(x)
```

inclui esse peso.

Para valores entre dois pontos observados:

> a CDF permanece constante.

Não usar:

- interpolação linear;

- spline;

- Pareto;

- extrapolação estatística;

- correções manuais.


---

# 12. Golden case brasileiro inicial

Caso histórico em preços médios de 2025:

```text
renda domiciliar = 6500
moradores = 3
RDPC = 2166,666666...
```

Resultado registrado:

```text
shareBelow = 0,701561259093934
shareAtOrBelow = 0,701561259093934
topShare = 0,298438740906066
```

Esse caso testa diretamente a CDF.

Ele não representa renda nominal corrente sem alinhamento temporal.

---

# 13. Estado histórico da CDF

A CDF foi criada antes da resolução do alinhamento temporal.

Por isso seus metadados registravam historicamente:

```text
frontendIntegrationAllowed = false
userIncomePriceAlignmentMethod = null
```

A decisão posterior foi:

> não reescrever a CDF para alterar esses campos.

Modificar o arquivo quebraria sua identidade e seu SHA canônico.

A autorização posterior de integração deveria ser expressa em um manifesto superior.

Essa separação entre:

```text
artefato histórico imutável
```

e:

```text
contrato atual de integração
```

tornou-se um princípio importante do projeto.

---

# 14. Fase 1F — alinhamento temporal Brasil

A CDF representa:

```text
preços médios de 2025
```

mas o usuário informa:

```text
renda nominal corrente
```

Era necessário colocá-los na mesma referência.

A Fase 1F estudou esse problema.

Commit histórico:

```text
0f0625c
research(data): define Brazil income price alignment
```

A solução recomendada e posteriormente canonizada foi baseada em:

```text
IPCA nacional
SIDRA tabela 1737
variável 2266
```

Referência:

```text
IPCA médio de 2025
=
média aritmética dos 12 números-índice mensais de 2025
```

Valor registrado:

```text
7300,8416666666666667
```

Para julho de 2026:

```text
IPCA = 7657,73
```

Multiplicador corrente → preços médios de 2025:

```text
≈ 0,9533950226329038
```

---

# 15. Fluxo Brasil após alinhamento

O fluxo conceitual passou a ser:

```text
renda nominal atual
↓
alinhamento D065
↓
renda comparável em preços médios de 2025
↓
divisão por moradores elegíveis
↓
CDF brasileira
↓
shareBelow
↓
apresentação
```

Golden case corrente registrado:

```text
renda = 6500
moradores = 3
```

Resultado comparável:

```text
renda domiciliar 2025
≈ 6197,0676471139
```

```text
RDPC comparável
≈ 2065,6892157046
```

```text
shareBelow
= 0,6866910622833815
```

```text
topShare
= 0,3133089377166185
```

---

# 16. Crise de governança encontrada depois da Fase 1F

Em uma inspeção posterior do checkout, o Codex encontrou um estado documental inconsistente.

Havia historicamente sinais como:

- `AGENTS.md` deletado no working tree;

- `README.md` deletado;

- `AGENTS.md.md` não rastreado;

- `docs/README.md` não rastreado;

- documentos canônicos modificados;

- arquivos de research não rastreados;

- alegações de artefatos que não existiam no checkout naquele momento.


Isso levou a uma mudança de prioridade.

Antes de integrar qualquer coisa:

> primeiro era necessário reconciliar governança e proveniência.

Esse foi o motivo do Gate G0.

---

# 17. Gate G0 — reconciliação de governança

O G0 teve como objetivo:

> fazer o estado documental e o pacote de produção Brasil voltarem a possuir correspondência verificável.

Resultado registrado:

```text
GATE G0 = CONCLUÍDO
MOTOR DE DADOS BRASIL = LIBERADO PARA INTEGRAÇÃO
```

O G0:

- reconciliou `AGENTS.md`;

- reconciliou README raiz;

- estabeleceu `docs/README.md` como índice documental;

- revisou documentos canônicos;

- reconciliou decisões;

- regenerou manifestos;

- criou schemas;

- preservou a CDF histórica;

- construiu validação explícita do pacote Brasil.


Commits:

```text
b0cf49ca24c080940ae6798a59ebe774e12082e4
docs(governance): reconcile canonical project state
```

```text
eb768c59d7e1404305f972581374a8f9c9ed2fcb
feat(data): rebuild verified Brazil production package
```

---

# 18. Contrato de produção Brasil após G0

O pacote passou a ter três elementos principais:

```text
data/production/brazil/
    brazil-income-cdf-2025.json
    brazil-price-alignment.json
    brazil-income-engine-manifest.json
```

O manifesto de preços passou a registrar:

```text
CANONICAL_APPROVED
```

O manifesto do motor:

```text
CANONICAL_APPROVED_FOR_INTEGRATION
```

A autorização de integração pertence ao manifesto do motor.

A CDF histórica continua imutável.

---

# 19. Validação G0 — substituição do antigo 21/21

Durante a reconciliação, não foi possível reconstruir de maneira inequívoca a alegação histórica:

```text
21/21 PASS
```

Os checks e relatórios correspondentes não estavam disponíveis de forma reproduzível.

A resposta adotada foi:

> não preservar uma validação não reproduzível apenas porque havia sido citada anteriormente.

Foi construída uma nova suíte explícita:

```text
44/44 checks PASS
```

Relatórios:

```text
validation/brazil/
brazil-production-package-validation.json

validation/brazil/
brazil-production-package-validation.md
```

Isso consolidou outro princípio:

> validação deve ser reproduzível, não apenas registrada narrativamente.

---

# 20. Decisões registradas após G0

O G0 registrou como ativas/canonizadas, naquele estágio:

```text
D063
D064
D065
D066
D067
D071
D072
D073
```

Naquele momento:

```text
D068
D069
D070
```

continuavam bloqueadas.

Esse estado é histórico e deve ser confirmado em `docs/decisoes.md` para uso atual.

---

# 21. Gate G1 — integração Brasil

Depois de o pacote Brasil estar reconciliado e validado, foi autorizada a integração controlada ao frontend.

Commit:

```text
ac2acdd81a1a0d4853d7bc39b700f90e03837263
feat(frontend): integrate verified Brazil income engine
```

Fluxo implementado:

```text
renda mensal atual
↓
D065
↓
RDPC comparável
↓
CDF Brasil
↓
D071
↓
resultado
```

---

# 22. Carregamento runtime Brasil

No primeiro cálculo, o frontend passou a carregar:

```text
brazil-income-engine-manifest.json
brazil-price-alignment.json
brazil-income-cdf-2025.json
```

Antes do cálculo, foram adicionadas verificações de:

- SHA-256;

- tamanho;

- versão;

- autorização;

- bloqueio Mundo;

- referências cruzadas;

- cardinalidade;

- ordenação;

- peso total;

- referência monetária.


Depois de validado:

> o runtime pode permanecer em memória durante a sessão.

---

# 23. D072 — entrega sob demanda

A CDF possui aproximadamente 3,95 MB brutos.

A estratégia escolhida foi:

```text
não entrar no bundle inicial
↓
carregar no primeiro cálculo
↓
validar
↓
manter em memória
```

A requisição não deve conter:

- renda;

- moradores;

- resultado;

- percentil.


Em erro:

```text
indisponibilidade
↓
nova tentativa
```

Não:

```text
fallback legado
```

---

# 24. Remoção do motor legado do caminho ativo

Após G1, deixaram de participar do cálculo ativo:

```text
BRAZIL_THRESHOLDS
WORLD_CURVE
PPP_2021_BRL
BRAZIL_CPI_2024
BRL_PER_INTL_2024
interpolateLog
```

Também deixaram de ser usados:

- percentis sintéticos;

- extrapolações antigas;

- fallback Mundo.


O princípio foi:

> código legado pode existir historicamente, mas não deve continuar ativo em paralelo ao motor validado.

---

# 25. Correção do parser de renda

O frontend antigo possuía um problema onde entradas como:

```text
6500.50
```

podiam se transformar em:

```text
650050
```

A integração corrigiu o parser.

Também passaram a ser rejeitados:

- moradores zero;

- moradores negativos;

- moradores fracionários.


---

# 26. Estado Mundo após G1

Mundo não foi ativado.

A interface passou a mostrar apenas:

```text
Indisponível nesta versão
```

Sem:

- curva provisória;

- percentil;

- TOP;

- fallback antigo.


Essa foi uma escolha deliberada:

> indisponibilidade explícita é preferível a precisão falsa.

---

# 27. Hardening de D071

Depois de G1, foi identificado um problema de apresentação.

A interface possuía um cap artificial próximo de:

```text
99,7%
```

Isso podia limitar visualmente posições estatísticas reais mais altas.

A correção separou:

```text
estatística
```

de:

```text
geometria do marcador
```

O percentil real não deveria ser limitado.

Somente a posição física do marcador precisava respeitar os limites da barra.

Exemplo testado:

```text
99,98%
```

permaneceu:

```text
99,98%
```

---

# 28. Política de cauda D071

Foram protegidas fronteiras como:

```text
TOP >= 1%
```

```text
0,1% <= TOP < 1%
```

```text
0 < TOP < 0,1%
```

Para a cauda extrema:

```text
TOP < 0,1%
```

e nunca:

```text
TOP 0%
```

Para valores acima do máximo observado:

> não fabricar percentil mais fino.

Para renda zero:

> evitar `TOP 100%` como headline.

---

# 29. D073 — metadata

A metadata foi implementada seguindo `docs/decisoes.md`, mesmo quando um resumo de prompt divergente sugeria outra formulação.

Isso reafirmou:

> documento canônico prevalece sobre resumo operacional quando o prompt não autoriza mudar a decisão.

Valores registrados:

```text
<title>
Você é mais rico do que quantos brasileiros? | Renda Comparada
```

```text
Description:
Descubra onde a renda da sua casa está na distribuição do Brasil e, de forma estimada, no mundo. Comparação de renda, não de patrimônio.
```

```text
og:title:
Você é mais rico do que quantos brasileiros?
```

```text
og:description:
Descubra onde a renda da sua casa está no Brasil e, de forma estimada, no mundo.
```

---

# 30. G2 — validação dinâmica

Foi realizada uma etapa posterior de validação em navegador.

Veredito registrado:

```text
G2 DINÂMICO — PASS COM RESSALVAS
```

Foram testados dinamicamente:

- caso-base;

- renda válida;

- renda inválida;

- moradores;

- renda zero;

- resultado comum;

- cauda intermediária;

- cauda extrema;

- acima do máximo;

- falha e retry;

- metadata;

- responsividade.


Viewports:

```text
360 px
390 px
430 px
1280 px
```

---

# 31. Correções encontradas durante G2

## 31.1 Marcador visual

Problema:

> marcador ultrapassava a régua nas caudas.

Correção:

> `clamp()` exclusivamente geométrico.

Nenhuma alteração estatística.

## 31.2 Erros e acessibilidade

Problema:

- foco permanecia no botão;

- erros não possuíam anúncio semântico adequado.


Correções:

- foco no primeiro campo inválido;

- `role="alert"`;

- associações ARIA.


---

# 32. Evidências G2

Foram relatadas como aprovadas:

- labels;

- associações;

- `aria-invalid`;

- `aria-describedby`;

- foco após erro;

- `role="alert"`;

- responsividade;

- retry;

- falha segura;

- ausência de percentil Mundo;

- URLs sem renda;

- requests estáticos sem dados do usuário.


Foram preservadas como NÃO VERIFICADAS dinamicamente:

- sequência completa de Tab;

- acionamento por Enter;

- retry exclusivamente por teclado;

- ausência de keyboard trap em navegação integral;

- instante visual exato de loading;

- conteúdo efetivo de todos os storages/cookies;

- máximo estatístico exato pelo input monetário limitado a duas casas.


Essas limitações não devem ser reinterpretadas como PASS.

---

# 33. Suítes registradas após hardening/G2

Historicamente foram registrados:

```text
frontend = 17/17 PASS
Brasil = 41/41 PASS
pacote Brasil = 44/44 PASS
typecheck = PASS
build = PASS
git diff --check = PASS
```

Esses números descrevem aquele estado histórico.

O estado atual deve ser reexecutado no checkout quando necessário.

---

# 34. Metodologia Mundo — decisões iniciais

Antes da implementação numérica Mundo, duas decisões já haviam sido fechadas.

## D066

Definia:

```text
PIP_VERSION = 20260324_2021
PIP_PRODUCTION_BUILD = 20260324_2021_01_02_PROD
GLOBAL_REFERENCE_YEAR = 2024
PPP_BASE = 2021
```

## D067

Definia o resultado como:

> **posição monetária global estimada**

Não como:

- ranking exato de salário;

- renda bruta homogênea;

- patrimônio;

- riqueza.


Isso reconhece que o PIP combina diferentes conceitos nacionais de welfare.

---

# 35. Bloqueios Mundo

Mesmo com D066/D067, ainda faltavam:

```text
D068
D069
D070
```

Conceitualmente:

```text
D068
fonte operacional e CDF mundial
```

```text
D069
renda corrente BRL
→
PPP 2021 compatível com PIP
```

```text
D070
golden cases
+
caudas
+
precisão
+
linguagem final
```

Enquanto esses gates não estivessem fechados:

> nenhum percentil Mundo deveria ser exibido.

---

# 36. Execução experimental de D068

Uma tarefa posterior foi autorizada para investigar e construir uma candidata técnica para D068.

Fonte:

```text
World Bank
Poverty and Inequality Platform
1000 Binned Global Distribution
```

Recurso:

```text
DR0094423
```

Build:

```text
20260324_2021_01_02_PROD
```

Ano:

```text
2024
```

PPP:

```text
2021
```

---

# 37. Pipeline candidato Mundo

Fluxo registrado:

```text
raw oficial
↓
year = 2024
↓
validar schema/build
↓
218 economias
↓
1.000 bins por economia
↓
ordenar globalmente por welf
↓
ponderar por pop
↓
agrupar empates
↓
CDF global candidata
```

Não foram utilizados:

- imputação manual;

- interpolação;

- extrapolação;

- correção manual de checkpoints.


---

# 38. Artefato candidato D068

Foi gerado experimentalmente:

```text
validation/world/world-income-cdf-2024-candidate.json
```

Status:

```text
CANDIDATE
```

Integração:

```text
frontendIntegrationAllowed = false
```

Propriedades registradas:

```text
218.000 bins de origem
216.790 pontos únicos
população = 8.141,808945 milhões
```

Tamanho:

```text
11.372.630 bytes
```

SHA-256:

```text
56C53483744176A50090E16058A0CF4FC6221C83D1D80A60060B931110C54DC2
```

Nenhum artefato Mundo foi promovido para `data/production/world`.

---

# 39. Validação da candidata Mundo

A candidata foi comparada com 18 checkpoints oficiais do PIP.

Faixa de comparação:

```text
US$ 1
até
US$ 200 PPP/pessoa/dia
```

Resultados registrados:

```text
erro absoluto máximo
≈ 0,02251699 ponto percentual
```

```text
erro absoluto médio
≈ 0,00673562 pp
```

```text
RMSE
≈ 0,00902173 pp
```

```text
viés médio
≈ -0,00465784 pp
```

A diferença de população ficou em aproximadamente:

```text
45 pessoas
```

dentro de uma população global de bilhões.

---

# 40. Limitação metodológica da 1000 Binned

A principal ressalva encontrada foi:

> perda de desigualdade dentro de cada bin.

A própria fonte do Banco Mundial alerta que a representação binned não substitui integralmente os cálculos do PIP sobre dados mais detalhados.

O Codex classificou a solução como:

```text
D068 — PRONTA COM RESSALVAS
```

A recomendação foi aceitar ou rejeitar explicitamente essa aproximação antes da canonização.

---

# 41. Por que D068 não virou automaticamente decisão

Apesar dos bons resultados técnicos, ao final daquela tarefa:

- `docs/decisoes.md` não foi alterado;

- nenhum arquivo Mundo foi promovido para produção;

- frontend não foi ativado;

- D069 não foi executada;

- D070 não foi executada;

- nenhum deploy foi realizado.


Portanto:

```text
D068 executada
```

não significava:

```text
D068 canonizada
```

Essa distinção deve ser preservada.

---

# 42. D069 ainda necessária

D069 deve resolver uma transformação diferente da brasileira.

A entrada final esperada pela CDF mundial é:

```text
dólares internacionais
PPP 2021
por pessoa
por dia
```

D069 deve transformar:

```text
renda domiciliar nominal corrente em BRL
```

nessa unidade de forma compatível com o pipeline PIP.

D065 não resolve esse problema automaticamente.

Brasil e Mundo possuem transformações monetárias distintas.

---

# 43. D070 ainda necessária

D070 deve fechar, entre outros pontos:

- golden cases;

- zero;

- mínimo;

- máximo;

- acima do máximo;

- empates;

- caudas;

- precisão;

- TOP;

- percentil;

- wording;

- grau de aproximação apresentado ao usuário.


Não deve simplesmente copiar D071, porque a distribuição Mundo possui características e incertezas diferentes.

---

# 44. Estado no encerramento das conversas analisadas

O último estado material registrado nas conversas era aproximadamente:

## Brasil

```text
metodologia validada
CDF validada
alinhamento temporal canonizado
pacote Brasil validado
frontend Brasil integrado
D071 endurecida
D073 implementada
G2 = PASS COM RESSALVAS
```

## Mundo

```text
D066 = canonizada
D067 = canonizada
D068 = executada tecnicamente / candidata validada
D068 = canonização ainda necessária segundo aquela conversa
D069 = pendente
D070 = pendente
frontend Mundo = bloqueado
```

## Deploy

As conversas analisadas não estabelecem evidência de deploy final de produção.

---

# 45. Git — observação histórica importante

Várias tarefas posteriores foram executadas sem commit imediato.

Por exemplo:

- hardening D071/D073;

- parte do G2;

- execução experimental D068.


Isso significa que:

> a existência da mudança numa conversa do Codex não prova que ela tenha sido posteriormente commitada ou permaneça no checkout atual.

Sempre consultar Git/local quando isso importar.

---

# 46. Princípio de commits

Ao longo do projeto, a intenção foi manter mudanças separadas por finalidade:

```text
documentação
≠
metodologia
≠
dados
≠
frontend
```

Evitar commits que misturem:

- pesquisa;

- decisão;

- implementação;

- cleanup não relacionado.


A menor mudança suficiente deve ser preferida.

---

# 47. Regra de preservação de alterações externas

O checkout apresentou em diferentes momentos:

- timestamps externos;

- documentos não rastreados;

- notas fora de escopo;

- arquivos duplicados;

- possíveis resíduos de sincronização.


A regra adotada foi:

> não apagar, restaurar, mover ou commitar algo sem compreender sua origem.

Alteração incidental não deve entrar em commit apenas por estar presente.

---

# 48. Pesquisa não é produção

A experiência com Mundo reforçou a função de:

```text
docs/research/
```

Esse diretório pode conter:

- relatório;

- candidato;

- protocolo;

- benchmark;

- experimento;

- proposta;

- execução.


Mas isso não concede automaticamente autoridade ao conteúdo.

Promoção exige decisão explícita.

---

# 49. Canonização

Quando uma pesquisa produz uma solução aprovada, o fluxo desejado é:

```text
research
↓
decisão humana
↓
docs/decisoes.md
↓
documento temático
↓
contrato técnico
↓
implementação
↓
testes
```

Não deixar conhecimento relevante preso apenas em uma conversa do Codex.

---

# 50. Papel dos READMEs

A evolução da governança levou à separação conceitual:

## `/README.md`

Entrada do repositório.

Deve ser conciso.

Não deve redefinir metodologia.

## `docs/README.md`

Índice da documentação e fotografia documental de alto nível.

## `docs/research/README.md`

Deve explicar o caráter não canônico da área de pesquisa.

## READMEs técnicos locais

Devem explicar o uso de um pacote ou diretório específico sem competir com a documentação canônica.

---

# 51. O que agentes futuros não devem fazer

Não:

- reabrir D063 por conveniência;

- alterar CDF para resolver UI;

- substituir manifesto congelado por dado mais novo;

- usar Mundo antigo como fallback;

- usar câmbio comercial no lugar de PPP;

- tratar D068 experimental como produção sem decisão;

- inventar D069;

- inventar D070;

- alterar golden cases para fazer teste passar;

- colocar renda em URL;

- colocar renda em analytics;

- embutir CDF Brasil no bundle inicial para simplificar;

- transformar research em requisito;

- avançar automaticamente de fase.


---

# 52. O que deve ser verificado antes de qualquer nova tarefa

Antes de nova implementação:

1. identificar o gate atual;

2. consultar `AGENTS.md`;

3. consultar `docs/README.md`;

4. consultar `docs/decisoes.md`;

5. consultar somente os documentos temáticos relevantes;

6. verificar se a tarefa depende de checkout;

7. verificar se existe lacuna humana;

8. definir escopo;

9. definir não escopo;

10. definir critérios de aceite;

11. somente então implementar.


---

# 53. Como usar este documento

Este documento deve ser usado quando for necessário compreender:

- por que determinada arquitetura existe;

- de onde vieram determinados gates;

- como o motor Brasil evoluiu;

- por que a CDF histórica não deve ser editada;

- por que o manifesto é uma camada superior;

- por que Mundo está separado de Brasil;

- por que research não é decisão;

- como surgiu a divisão ChatGPT ↔ Codex;

- quais erros de processo já aconteceram.


Não deve ser usado sozinho para responder:

> “qual é o estado atual do projeto?”

Para isso, consultar as fontes vigentes.

---

# 54. Regra para conflitos com este histórico

Se este documento disser:

```text
X estava bloqueado
```

mas `docs/decisoes.md` atual disser:

```text
X está ativo
```

prevalece o documento canônico atual.

Se este documento disser:

```text
arquivo X foi criado
```

mas o checkout atual não o possuir:

> o estado atual do checkout prevalece.

Se este documento registrar um hash histórico e um manifesto atual registrar outro após promoção legítima:

> investigar a versão e a decisão correspondente.

Este arquivo serve para explicar a evolução.

Não para congelar o projeto no passado.

---

# 55. Linha do tempo resumida

```text
VALIDAÇÃO METODOLÓGICA BRASIL
↓
D063 / D064
↓
HIGIENE DOCUMENTAL
↓
FASE 1D
pipeline reproduzível
↓
FASE 1E
CDF Brasil
↓
FASE 1F
alinhamento temporal
↓
D065
↓
CRISE / DIVERGÊNCIA DE GOVERNANÇA
↓
G0
reconciliação documental + pacote Brasil
↓
44/44 validações
↓
G1
integração Brasil
↓
HARDENING
D071 + D073
↓
G2
validação dinâmica
PASS COM RESSALVAS
↓
D066 + D067
Mundo parcialmente definido
↓
EXECUÇÃO EXPERIMENTAL D068
CDF candidata World Bank 1000 Binned
↓
D068 PRONTA COM RESSALVAS
↓
DECISÃO/CANONIZAÇÃO AINDA NECESSÁRIA
↓
D069
pendente no último estado histórico analisado
↓
D070
pendente no último estado histórico analisado
```

---

# 56. Síntese final

A linha de raciocínio construída ao longo do projeto pode ser resumida assim:

> **Nunca colocar a interface à frente da metodologia.**

> **Nunca colocar implementação à frente da decisão.**

> **Nunca colocar pesquisa diretamente em produção.**

> **Nunca trocar uma fonte ou versão silenciosamente.**

> **Nunca usar uma aproximação quando o produto pode falhar explicitamente.**

> **Nunca deixar uma conversa do Codex se tornar a única fonte de uma decisão importante.**

> **Toda transformação importante deve ser reproduzível.**

> **Todo artefato importante deve ser versionado.**

> **Toda decisão importante deve estar em fonte canônica.**

> **Brasil e Mundo são motores metodologicamente distintos.**

> **O motor Brasil validado deve ser tratado como área protegida.**

> **Mundo só pode ser ativado quando seus gates forem explicitamente fechados.**

> **ChatGPT deve reduzir a incerteza antes de Codex tocar no checkout.**

> **Codex deve executar o mínimo necessário e devolver evidência auditável.**

> **Depois de cada gate, primeiro auditar; somente depois decidir o próximo passo.**

Esse é o modelo operacional que deve orientar a continuação do Renda Comparada.
