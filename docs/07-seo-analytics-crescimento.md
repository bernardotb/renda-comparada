---
title: 07-seo-analytics-crescimento
created: 2026-08-12T17:39:01.000-03:00
modified: 2026-08-22T11:51:41.324-03:00
---

# 07-seo-analytics-crescimento

# SEO, Analytics E Crescimento — Renda Comparada

**Produto:** Renda Comparada  
**Documento:** `07-seo-analytics-crescimento.md`  
**Status:** Canônico para aquisição, mensuração e crescimento  
**Versão:** 1.2
**Última revisão:** 22/08/2026

Documentos relacionados:

- `01-visao-produto.md`
- `02-prd-v1.md`
- `03-jornada-ux-v1.md`
- `04-metodologia-dados.md`
- `05-design-system.md`
- `06-privacidade-seguranca.md`
- `08-roadmap-backlog.md`
- `09-fontes-referencias.md`
- `10-testes-validacao.md`

---

# 1. Função Deste Documento

Este documento define a estratégia do Renda Comparada para:

- SEO;
- indexação;
- Search Console;
- conteúdo orgânico;
- compartilhamento;
- viralidade;
- analytics;
- eventos;
- atribuição;
- métricas;
- experimentação;
- divulgação;
- imprensa;
- criadores;
- crescimento.

Ele não define:

- metodologia estatística;
- design detalhado;
- regras de privacidade;
- funcionalidades da V1.

Para essas questões, prevalecem os documentos específicos.

---

# 2. Princípio Central

O crescimento do Renda Comparada deve nascer principalmente de três motores:

```text
BUSCA
+
CURIOSIDADE
+
COMPARTILHAMENTO
```

A ferramenta não deve depender inicialmente de aquisição paga para cada novo usuário.

O objetivo é criar um produto que consiga gerar parte da própria distribuição.

---

# 3. Mecanismo Central De Crescimento

O principal loop da V1 é:

```text
usuário recebe link
↓
entra no site
↓
faz cálculo
↓
recebe resultado
↓
resultado gera curiosidade/surpresa
↓
compartilha
↓
outra pessoa recebe
↓
entra no site
↓
faz cálculo
↓
compartilha
```

Resumidamente:

> **resultado → compartilhamento → novo usuário**

Esse é o principal mecanismo de crescimento a ser validado na V1.

---

# 4. O Compartilhamento Vem Antes Da Expansão Do Produto

Depois do resultado Brasil + Mundo:

```text
RESULTADO
↓
INTERPRETAÇÃO
↓
COMPARTILHAR
```

Somente depois:

```text
CHECK-UP OPCIONAL
CURSOS
SIMULADORES
OUTRAS FERRAMENTAS
```

Não inserir funcionalidades que desviem a atenção do compartilhamento no momento de maior interesse da jornada.

---

# 5. Objetivos De Crescimento Da V1

A V1 deve responder:

### Aquisição

As pessoas estão chegando?

### Ativação

Elas iniciam o cálculo?

### Valor

Elas concluem e entendem o resultado?

### Distribuição

Elas compartilham?

### Confiança

Elas consultam metodologia e fontes?

### Continuidade

Algumas desejam seguir para a próxima etapa do produto?

---

# 6. Funil Principal

O funil canônico será:

```text
VISITANTE
↓
INICIA CÁLCULO
↓
CONCLUI CÁLCULO
↓
VÊ RESULTADO
↓
COMPARTILHA
↓
NOVO USUÁRIO VIA COMPARTILHAMENTO
```

Depois:

```text
RESULTADO
↓
INTERESSE EM CHECK-UP
```

A segunda sequência é importante, mas não substitui o funil principal da V1.

---

# 7. Métrica Principal

A principal métrica comportamental inicial será:

> # Taxa de compartilhamento

Fórmula:

```text
share_rate =
usuários que iniciaram uma ação de compartilhamento
/
cálculos concluídos
```

Exemplo:

```text
1.000 cálculos concluídos
150 ações de compartilhamento

share_rate = 15%
```

O objetivo inicial não é definir uma meta arbitrária de 15%.

Primeiro devemos obter uma linha de base real.

---

# 8. Por Que Essa Métrica É Importante

Pageviews respondem:

> “Quantas pessoas chegaram?”

A taxa de compartilhamento responde:

> “Quantas consideraram o resultado interessante o suficiente para transmiti-lo?”

Para a tese atual do produto, essa segunda pergunta é especialmente importante.

---

# 9. Métricas Secundárias

Monitorar:

```text
visit → calculation_started
```

```text
calculation_started → calculation_completed
```

```text
calculation_completed → share_clicked
```

```text
calculation_completed → methodology_opened
```

```text
calculation_completed → recalculate_clicked
```

```text
calculation_completed → financial_checkup_interest
```

Além de:

- usuários;
- sessões/visitas disponíveis na ferramenta adotada;
- páginas;
- origem;
- referrer;
- dispositivo;
- país;
- performance;
- tráfego orgânico;
- consultas de busca.

---

# 10. Não Criar Metas Antes Da Linha De Base

Na primeira fase:

> medir antes de otimizar.

Não definir arbitrariamente:

```text
30% precisam compartilhar
80% precisam calcular
10% precisam fazer check-up
```

Primeiro:

1. lançar;
2. medir;
3. identificar gargalos;
4. criar hipóteses;
5. testar melhorias.

---

# 11. Analytics Da V1

A V1 deve utilizar somente uma ferramenta de analytics que passe pela auditoria definida em `06-privacidade-seguranca.md`.

O fornecedor permanece uma decisão separada:

```text
ANALYTICS_PROVIDER = [DEFINIR]
```

A escolha deve considerar, no mínimo:

- cookies e identificadores;
- coleta automática;
- tratamento de IP;
- retenção;
- transferência internacional;
- eventos personalizados;
- impacto de performance.

A ausência de fornecedor aprovado não autoriza o código a adicionar tracking por iniciativa própria.

## Avaliação atual — Vercel Web Analytics

A pesquisa oficial realizada em 14/08/2026 registra:

```text
Hobby........... Web Analytics disponível; 50.000 eventos incluídos/mês; janela de 1 mês
Hobby........... custom events NÃO disponíveis
Pro............. custom events disponíveis; 2 propriedades por evento na configuração padrão
Enterprise...... custom events disponíveis
```

Fontes oficiais:

- https://vercel.com/docs/analytics/custom-events
- https://vercel.com/docs/analytics/limits-and-pricing
- https://vercel.com/docs/plans/hobby

Consequências:

1. Vercel Web Analytics continua **candidato**, não fornecedor canonizado;
2. a taxonomia completa definida abaixo exige custom events e, portanto, não pode ser prometida em Hobby;
3. se o projeto estiver em Hobby, pode lançar com mensuração reduzida a pageviews/tráfego em vez de ampliar coleta;
4. é proibido transformar rotas, query strings ou fragmentos em eventos artificiais para contornar a limitação de plano;
5. antes da implementação deve ser verificado:

```text
VERCEL_PLAN = [VERIFICAR]
```

---

# 12. Analytics Não Deve Medir Renda

O objetivo do analytics é descobrir:

> **o que o usuário fez**

e não:

> **quanto o usuário ganha.**

É proibido enviar:

```text
income
household_income
per_capita_income
household_size
brazil_percentile
world_percentile
```

para analytics, pixels ou ferramentas de marketing.

As regras completas estão em:

`06-privacidade-seguranca.md`

---

# 13. Taxonomia De Eventos

Usar nomes consistentes em inglês técnico no código.

## Entrada

```text
calculator_view
```

Quando a calculadora é visualizada.

---

## Início

```text
calculation_started
```

Registrar apenas uma vez por tentativa relevante.

Não disparar a cada tecla digitada.

---

## Conclusão

```text
calculation_completed
```

Quando um resultado válido é calculado.

---

## Resultado

```text
result_viewed
```

Quando o resultado efetivamente entra na área visível ou é apresentado.

---

## Metodologia

```text
methodology_opened
```

Quando o usuário abre a explicação metodológica.

---

## Compartilhamento

Evento genérico:

```text
share_clicked
```

Quando o usuário inicia a intenção de compartilhar.

Eventos específicos:

```text
share_native
```

```text
share_whatsapp
```

```text
copy_link
```

---

## Novo Cálculo

```text
recalculate_clicked
```

---

## Continuação

```text
financial_checkup_interest
```

Quando o usuário manifesta interesse em continuar para a segunda experiência.

---

# 14. Parâmetros Permitidos

Utilizar somente parâmetros que não revelem informações financeiras.

Exemplos possíveis:

```text
page
device_context
share_channel
share_mode
app_version
```

Somente quando realmente necessários.

---

# 15. Parâmetros Proibidos

Não utilizar:

```text
income
income_band
household_size
per_capita_income
percentile
top_percent
debt
savings
patrimony
```

Não tentar contornar a regra transformando renda em faixas.

Exemplo proibido:

```text
income_band = 10000_20000
```

Continua sendo informação financeira desnecessária para o objetivo da V1.

---

# 16. Analytics Não Deve Mudar a Experiência

Nunca atrasar:

- cálculo;
- resultado;
- compartilhamento;

porque um evento de analytics ainda não foi enviado.

Analytics é observação.

Não é dependência funcional.

---

# 17. Falha Do Analytics

Se analytics estiver indisponível:

> o produto continua funcionando normalmente.

Nunca bloquear o cálculo devido a:

- ad blocker;
- timeout;
- falha externa;
- script indisponível.

---

# 18. Performance

Performance também faz parte de aquisição e conversão.

Metas iniciais de Core Web Vitals:

```text
LCP ≤ 2,5 s
INP ≤ 200 ms
CLS ≤ 0,1
```

Esses são os limites que o Google atualmente recomenda para uma boa experiência nas três métricas de Core Web Vitals.

---

# 19. Speed Insights

Caso o projeto permaneça na Vercel, o **Speed Insights** pode ser utilizado para acompanhar Core Web Vitals reais.

A ferramenta da Vercel mede métricas de experiência em campo e atualmente apresenta dados de Core Web Vitals no painel da plataforma.

Sua ativação deve continuar obedecendo às regras de privacidade do projeto.

---

# 20. SEO — Objetivo

SEO deve permitir que pessoas encontrem o produto quando pesquisarem dúvidas que naturalmente levam à calculadora.

Exemplos de intenção:

```text
quanto precisa ganhar para ser rico no Brasil
```

```text
quanto ganha o top 10% no Brasil
```

```text
renda familiar Brasil
```

```text
renda per capita
```

```text
renda média brasileira
```

```text
quanto é uma renda alta no Brasil
```

O conteúdo deve responder primeiro à pergunta pesquisada.

A calculadora entra como continuação natural.

---

# 21. SEO Não É Escrever Para Robôs

O princípio será:

> **produzir a melhor resposta possível para uma pergunta real.**

Não:

> repetir keywords artificialmente.

Não criar páginas apenas para ocupar resultados de pesquisa.

---

# 22. Página Principal

A home deve possuir conteúdo HTML que explique claramente:

- o que a ferramenta faz;
- o que o usuário deve informar;
- o que significa o resultado;
- de onde vêm os dados;
- diferença entre renda e patrimônio;
- acesso à metodologia.

A calculadora pode ser interativa.

A informação essencial não deve depender exclusivamente de uma sequência complexa de JavaScript para existir.

---

# 23. JavaScript E Indexação

O Google consegue processar páginas JavaScript por etapas de rastreamento, renderização e indexação, mas a aplicação deve facilitar a descoberta do conteúdo essencial.

Por isso, como decisão arquitetural do projeto:

> **conteúdo SEO importante deve preferencialmente estar disponível em HTML renderizado no servidor ou gerado estaticamente quando apropriado.**

Não depender de uma interação do usuário para revelar todo o conteúdo textual indexável.

---

# 24. H1 Da home

O H1 principal será:

> # Você é mais rico do que quantos brasileiros?

A página deve possuir hierarquia semântica clara.

Evitar múltiplos títulos gigantes visualmente concorrentes.

---

# 25. Title Da Home — D073

Canônico para a V1:

```html
<title>Você é mais rico do que quantos brasileiros? | Renda Comparada</title>
```

O texto preserva a chamada principal do produto e não deve ser trocado silenciosamente pelo Codex.

---

# 26. Meta Description Da Home — D073

Canônica para a V1:

```html
<meta
  name="description"
  content="Descubra onde a renda da sua casa está na distribuição do Brasil e, de forma estimada, no mundo. Comparação de renda, não de patrimônio."
/>
```

A redação:

- distingue renda de patrimônio;
- preserva o caráter estimado do Mundo exigido por D067;
- não promete precisão individual inexistente.

---

# 27. Títulos De Páginas

Cada página indexável deve possuir título específico.

Não usar:

```text
Renda Comparada
Renda Comparada
Renda Comparada
```

em todas as páginas.

Exemplo:

```text
Como calculamos sua posição de renda | Renda Comparada
```

```text
Renda per capita: o que é e como calcular | Renda Comparada
```

---

# 28. Datas Nos Títulos

Não adicionar ano apenas para parecer atualizado.

Quando o ano for essencial à intenção:

```text
Renda média no Brasil em 2026
```

o conteúdo e os dados precisam realmente estar atualizados.

O Google cita títulos desatualizados como um problema comum em páginas recorrentes.

---

# 29. URLs

Preferir URLs:

- curtas;
- legíveis;
- persistentes;
- descritivas.

Exemplos:

```text
/metodologia
```

```text
/renda-per-capita
```

```text
/renda-top-10-brasil
```

Evitar:

```text
/page?id=1284
```

quando uma rota semântica fizer sentido.

---

# 30. URLs Evergreen

Para conteúdos recorrentes, preferir quando apropriado:

```text
/renda-media-brasil
```

em vez de criar todo ano:

```text
/renda-media-brasil-2025
/renda-media-brasil-2026
/renda-media-brasil-2027
```

Atualizar:

- dados;
- título;
- data;
- fontes;

na página canônica.

Criar nova URL anual somente quando houver valor editorial real em preservar cada edição.

---

# 31. Canonical

Cada página indexável deve possuir uma estratégia canônica clara.

Quando existirem versões duplicadas ou muito semelhantes, usar adequadamente:

```html
<link rel="canonical" href="…" />
```

O Google utiliza sinais como redirecionamentos, `rel="canonical"` e presença no sitemap na seleção de URLs canônicas.

---

# 32. Domínio Próprio

Quando o domínio definitivo for adotado:

- definir uma única versão canônica;
- redirecionar versões antigas;
- atualizar sitemap;
- atualizar canonical;
- atualizar Open Graph;
- configurar Search Console;
- preservar redirects relevantes.

Não manter deliberadamente duas versões públicas equivalentes competindo pela indexação.

---

# 33. Sitemap

Manter:

```text
/sitemap.xml
```

O sitemap deve conter somente URLs canônicas que desejamos indexar.

O Google recomenda usar URLs absolutas e permite o envio do sitemap pelo Search Console; o sitemap também pode ser referenciado no `robots.txt`.

---

# 34. `lastmod`

Usar `lastmod` somente quando refletir uma atualização significativa da página.

Exemplos:

- mudança relevante de conteúdo;
- atualização dos dados;
- atualização de metodologia.

Não atualizar diariamente apenas para aparentar novidade.

O Google orienta que `lastmod` represente alteração significativa.

---

# 35. robots.txt

Disponibilizar:

```text
/robots.txt
```

Ele deve permitir o rastreamento das páginas públicas importantes e indicar o sitemap quando apropriado.

Importante:

> `robots.txt` não é mecanismo de privacidade nem método confiável para impedir uma página de aparecer nos resultados.

O próprio Google orienta usar `noindex` ou proteção de acesso quando o objetivo é impedir indexação de uma página.

---

# 36. Preview E Staging

Ambientes:

```text
preview
staging
development
```

não devem competir com produção nos mecanismos de busca.

Implementar estratégia deliberada de:

- acesso restrito;
- `noindex`;

ou mecanismo equivalente adequado ao ambiente.

Não depender apenas de obscuridade do URL.

---

# 37. Search Console

O domínio de produção deve ser verificado no:

> **Google Search Console**

Usá-lo para:

- acompanhar indexação;
- enviar e monitorar sitemap;
- inspecionar URLs;
- acompanhar consultas;
- acompanhar páginas;
- acompanhar cliques;
- acompanhar impressões;
- acompanhar Core Web Vitals;
- identificar problemas de dados estruturados.

Essas são funções suportadas atualmente pelo Search Console.

---

# 38. Rotina De Search Console

Após lançamento:

### Semanal Inicialmente

Verificar:

- páginas indexadas;
- erros;
- consultas emergentes;
- CTR;
- posições;
- Core Web Vitals.

### Depois

A frequência pode diminuir quando o site estabilizar.

---

# 39. Métricas Orgânicas

Monitorar:

```text
impressions
```

```text
clicks
```

```text
CTR
```

```text
average position
```

por:

- consulta;
- página;
- período.

Não otimizar posição isoladamente.

Uma página em posição menor para uma busca altamente relevante pode valer mais que grande volume irrelevante.

---

# 40. Indexação Não É Objetivo Final

Não celebrar apenas:

> “Temos 100 páginas indexadas.”

A pergunta é:

> **Essas páginas respondem dúvidas reais e trazem usuários que utilizam o produto?**

---

# 41. Dados Estruturados

Podemos avaliar dados estruturados como:

```text
WebSite
```

e, quando tecnicamente aplicável e todos os campos exigidos estiverem corretos:

```text
SoftwareApplication
```

O Google possui suporte específico a `SoftwareApplication`, mas a marcação deve corresponder ao conteúdo real da página e cumprir os requisitos aplicáveis.

Não adicionar schema apenas para tentar forçar rich results.

---

# 42. Validação De Dados Estruturados

Antes de produção:

- testar sintaxe;
- verificar propriedades obrigatórias;
- conferir conteúdo real;
- testar no Rich Results Test quando aplicável;
- acompanhar Search Console.

Dados estruturados inválidos não devem permanecer em produção.

---

# 43. Open Graph

Toda página importante deve possuir metadados sociais adequados.

Home:

```text
og:title
og:description
og:image
og:url
```

A imagem padrão deve comunicar a proposta da ferramenta.

---

# 44. Open Graph Da Home — D073

Texto canônico:

```text
og:title = Você é mais rico do que quantos brasileiros?
og:description = Descubra onde a renda da sua casa está no Brasil e, de forma estimada, no mundo.
```

Conceito visual da imagem padrão:

```text
RENDA COMPARADA

Você é mais rico do que
quantos brasileiros?
```

Sem:

- renda de exemplo que pareça real;
- percentil fictício;
- excesso de texto;
- qualquer resultado individual.

`DEFAULT_OG_IMAGE` continua pendente de criação; o texto não está pendente.

---

# 45. Resultado Individual E Open Graph

Não colocar renda do usuário em:

```text
og:title
og:description
og:image
og:url
```

O card de resultado personalizado, caso exista, deve seguir as regras de `06-privacidade-seguranca.md`.

---

# 46. Conteúdo Da V1

A V1 não precisa começar com dezenas de páginas.

Prioridade inicial:

```text
/
```

Home/calculadora.

```text
/metodologia
```

Metodologia completa.

```text
/sobre
```

Quando necessário.

```text
/privacidade
```

Documento público apropriado.

Depois:

> conteúdo editorial orientado por demanda real.

---

# 47. Estratégia De Conteúdo Futura

O objetivo não é:

> “transformar uma calculadora em 30 páginas rapidamente.”

O objetivo é:

> **construir autoridade temática progressivamente.**

Cada nova página deve existir porque responde bem a uma pergunta relevante.

---

# 48. Cluster — Posição De Renda

Candidatos futuros:

```text
quanto precisa ganhar para estar no top 1%
```

```text
quanto precisa ganhar para estar no top 10%
```

```text
renda top 5% Brasil
```

```text
pirâmide de renda Brasil
```

---

# 49. Cluster — Conceitos

Candidatos:

```text
o que é renda per capita
```

```text
renda familiar
```

```text
média x mediana
```

```text
o que é percentil
```

```text
renda x patrimônio
```

---

# 50. Cluster — Perguntas De Linguagem Natural

Exemplos:

```text
R$ 5 mil por mês é muito?
```

```text
R$ 10 mil por mês é uma renda alta?
```

```text
R$ 20 mil por mês é rico?
```

```text
quanto uma família precisa ganhar?
```

Essas páginas só devem ser criadas quando pudermos responder com metodologia defensável.

---

# 51. Regra Para Conteúdos Sobre Valores

Nunca publicar:

> “Com R$ 10 mil você está no Top X%”

sem especificar variáveis relevantes.

O resultado pode depender de:

- número de moradores;
- período;
- referência de preços;
- distribuição utilizada.

A página deve explicar isso e levar para a calculadora.

---

# 52. CTA Editorial

Conteúdos relacionados à renda devem terminar naturalmente com:

> **Veja onde a renda da sua família está →**

O CTA não deve parecer anúncio.

Ele é continuação da pergunta do artigo.

---

# 53. Conteúdo Baseado Em Fonte

Todo conteúdo estatístico deve informar:

- fonte;
- ano;
- metodologia;
- atualização.

Não publicar estatísticas sem origem identificável.

---

# 54. Atualização De Conteúdo

Quando um novo dataset for aprovado:

verificar páginas que dependem dele.

Fluxo:

```text
novo dataset
↓
identificar conteúdos afetados
↓
recalcular dados
↓
atualizar texto
↓
atualizar data
↓
revisar title quando necessário
↓
publicar
```

Não deixar artigo 2024 aparentando utilizar dados 2026.

---

# 55. Thin Content

Não gerar automaticamente centenas de páginas mudando apenas:

```text
R$ 5.000
R$ 6.000
R$ 7.000
R$ 8.000
```

Cada página indexável precisa possuir valor editorial real.

---

# 56. Conteúdo Gerado Por IA

IA pode auxiliar:

- pesquisa;
- estrutura;
- revisão;
- edição;
- atualização.

Mas estatísticas e afirmações factuais devem ser verificadas.

Não publicar conteúdo em escala simplesmente porque pode ser produzido automaticamente.

---

# 57. Links Internos

Criar caminhos naturais:

```text
artigo
↓
conceito relacionado
↓
metodologia
↓
calculadora
```

A home também pode apontar para conteúdos importantes.

Não criar links internos artificiais em excesso.

---

# 58. Compartilhamento Orgânico

A principal mensagem compartilhável deve provocar:

> **“E eu?”**

Exemplo:

> Descobri onde minha renda está na distribuição brasileira. E você?

Essa pergunta deve levar diretamente à calculadora.

---

# 59. Card De Resultado

Quando o usuário optar por revelar sua posição:

```text
RENDA COMPARADA

TOP 12%

Minha posição na distribuição
de renda brasileira.

E você?
```

O card deve funcionar como:

> resultado + convite.

---

# 60. WhatsApp Como Fluxo Prioritário

O produto deve considerar especialmente:

```text
WhatsApp
↓
celular
↓
calculadora
↓
resultado
↓
WhatsApp
```

Por isso:

- página rápida;
- preview social bom;
- CTA de share simples;
- formulário mobile excelente;
- link compartilhado direto.

---

# 61. UTMs

Campanhas controladas podem utilizar UTMs genéricos.

Exemplo:

```text
utm_source=instagram
utm_medium=social
utm_campaign=launch
```

Para compartilhamento:

```text
utm_source=share
utm_medium=whatsapp
```

quando houver valor analítico real.

---

# 62. Dados Proibidos Em UTMs

Nunca:

```text
utm_income=15000
```

```text
utm_percentile=92
```

```text
utm_user=fred
```

UTMs podem aparecer em:

- URLs;
- logs;
- analytics;
- históricos;
- ferramentas externas.

Portanto, não são lugar para dados financeiros ou pessoais.

---

# 63. Atribuição Do Loop Viral

Podemos estimar em nível agregado:

```text
visitas originadas de links compartilhados
/
ações de compartilhamento
```

Isso ajuda a entender quantos novos acessos cada ação de share parece gerar.

Não é necessário identificar individualmente:

> quem compartilhou com quem.

---

# 64. Coeficiente Viral Aproximado

Conceito futuro:

```text
K ≈
share_rate
×
novos visitantes por compartilhamento
×
taxa de cálculo desses visitantes
```

Não precisa ser tratado como métrica exata.

Serve para entender se o produto apresenta crescimento autossustentado ou depende quase totalmente de aquisição externa.

---

# 65. Crescimento Por Imprensa

Depois de validar a ferramenta:

abordar jornalistas e veículos relacionados a:

- economia;
- desigualdade;
- finanças pessoais;
- carreira;
- dados;
- comportamento econômico.

A proposta não deve ser:

> “Divulgue meu site.”

Melhor:

> **“Criamos uma ferramenta que transforma uma estatística abstrata de distribuição de renda em uma comparação pessoal compreensível.”**

---

# 66. Material Para Imprensa

Preparar futuramente:

```text
/media
```

ou página equivalente contendo:

- descrição do produto;
- metodologia;
- fontes;
- contato;
- screenshots;
- identidade visual;
- exemplos estatísticos validados;
- data de atualização.

Isso facilita referência por jornalistas.

---

# 67. Jornalistas Devem Conseguir Auditar

Uma matéria pode gerar muito tráfego.

Mas jornalistas também podem questionar:

> “Como esse número foi calculado?”

Portanto:

> **metodologia transparente é parte da estratégia de crescimento.**

Credibilidade é distribuição.

---

# 68. Criadores De Conteúdo

Possíveis áreas:

- finanças pessoais;
- economia;
- carreira;
- negócios;
- educação;
- dados;
- desigualdade.

Priorizar criadores cujo público tenha afinidade real com a pergunta.

Não buscar apenas tamanho de audiência.

---

# 69. Conteúdo Para Redes Sociais

A ferramenta gera naturalmente perguntas como:

```text
Quanto uma família precisa ganhar
para estar no Top 10%?
```

```text
R$ 10 mil é muito no Brasil?
```

```text
Por que sua renda pode ser alta
e mesmo assim o dinheiro não sobrar?
```

Cada conteúdo deve levar novamente ao produto.

---

# 70. Não Produzir Conteúdo Sensacionalista

Evitar:

> “Você é pobre e não sabe!”

> “O segredo dos ricos!”

> “Descubra se você fracassou financeiramente!”

> “Você não vai acreditar quanto ganha o Top 1%!”

Curiosidade pode ser forte sem destruir confiança.

---

# 71. Notícias Como Gancho

Quando uma nova estatística relevante de renda for divulgada:

podemos produzir rapidamente conteúdo que explique:

> o que significa;

e oferecer:

> “Veja onde sua família está.”

Mas toda estatística precisa ser verificada na fonte original antes de publicação.

---

# 72. Crescimento Por Ferramentas Oficiais

A evolução do produto pode gerar tráfego recorrente por conteúdos úteis sobre:

- Registrato;
- crédito;
- juros;
- orçamento;
- reserva;
- cursos gratuitos;
- serviços públicos.

Mas essas áreas só devem crescer quando fizerem parte do escopo aprovado.

---

# 73. Cursos Públicos

Conteúdos futuros poderão responder:

> “Onde aprender finanças pessoais gratuitamente?”

e encaminhar para:

- Banco Central;
- Enap;
- CVM;
- Senacon;
- outras instituições oficiais adequadas.

Esse conteúdo deve apoiar a missão do produto, não virar um catálogo desorganizado de links.

---

# 74. Crescimento Por Utilidade

Regra:

> **cada nova ferramenta precisa resolver uma decisão real.**

Ferramentas úteis podem gerar:

- busca;
- backlinks;
- compartilhamento;
- retorno direto.

Mas crescimento não justifica adicionar calculadoras fora da tese do produto.

---

# 75. Não Virar AllTools

O projeto não deve tentar capturar tráfego criando:

- calculadora de tinta;
- conversor aleatório;
- cronômetro;
- calculadora técnica sem relação com finanças familiares.

SEO não deve desviar a identidade do produto.

---

# 76. Experimentação

Toda mudança de crescimento deve começar com hipótese.

Formato:

```text
HIPÓTESE
↓
MUDANÇA
↓
MÉTRICA
↓
PERÍODO
↓
RESULTADO
↓
DECISÃO
```

---

# 77. Exemplo De Experimento

Hipótese:

> “Mostrar explicitamente que a renda não será compartilhada aumenta o uso do botão de share.”

Mudança:

```text
Sua renda não será mostrada.
```

Métrica:

```text
share_clicked / calculation_completed
```

Comparar com a linha de base.

---

# 78. Não Testar Tudo Ao Mesmo Tempo

Evitar simultaneamente:

- novo H1;
- nova cor;
- novo CTA;
- novo card;
- novo share;
- nova metodologia.

Depois não será possível entender o que causou a mudança.

---

# 79. Metodologia Nunca É Experimento De Marketing

Não testar:

> uma fórmula que produz percentis maiores

porque aumenta compartilhamento.

A metodologia pertence a:

`04-metodologia-dados.md`

e nunca deve ser alterada para melhorar métricas de crescimento.

---

# 80. Privacidade Não É Variável De Conversão

Não testar esconder:

> “Sua renda não será armazenada”

porque o aviso reduz cliques.

Transparência não é opcional.

---

# 81. Dark Patterns Proibidos

Não usar:

- contagem regressiva falsa;
- urgência falsa;
- botão fechar escondido;
- cadastro obrigatório disfarçado;
- compartilhamento automático;
- permissão pré-selecionada;
- manipulação por vergonha;
- falsa escassez;
- notificações enganosas.

---

# 82. Fase 0 — Preparação

Antes de divulgação relevante:

- produto funcional;
- metodologia auditada;
- privacidade auditada;
- analytics funcionando;
- Open Graph funcionando;
- Search Console configurado;
- sitemap;
- canonical;
- domínio definitivo quando decidido;
- mobile testado;
- compartilhamento testado.

---

# 83. Fase 1 — Validar Produto

Objetivo:

> descobrir se as pessoas naturalmente calculam e compartilham.

Aquisição inicial pode vir de:

- contatos;
- WhatsApp;
- redes sociais;
- grupos;
- usuários convidados.

Sem grande investimento.

---

# 84. Fase 2 — Validar Mensagem

Comparar hipóteses como:

```text
Você é mais rico do que quantos brasileiros?
```

versus formulações alternativas somente se houver motivo real para teste.

Métrica:

- início de cálculo;
- conclusão;
- compartilhamento.

---

# 85. Fase 3 — SEO

Depois da calculadora estar confiável:

começar a publicar páginas de alta intenção.

Não esperar produzir 30 artigos antes de lançar.

---

# 86. Fase 4 — Imprensa E Criadores

Com:

- produto estável;
- metodologia pública;
- números validados;
- card social;
- domínio adequado;

começar divulgação ativa.

---

# 87. Fase 5 — Expansão Do Produto

Dados de uso podem ajudar a decidir qual caminho merece prioridade:

```text
Top X%
```

```text
simulador de renda
```

```text
check-up
```

```text
dívidas
```

```text
orçamento
```

```text
cursos
```

A expansão deve responder ao comportamento real dos usuários.

---

# 88. Mídia Paga

Mídia paga não é prioridade inicial da V1.

Antes de investir significativamente, entender:

- quantos visitantes calculam;
- quantos compartilham;
- quanto tráfego compartilhado gera;
- quais buscas convertem;
- quais conteúdos atraem usuários adequados.

Depois disso, aquisição paga poderá ser testada conscientemente.

---

# 89. Dashboard Mínimo

Criar visão simples contendo:

```text
VISITANTES
```

```text
CÁLCULOS INICIADOS
```

```text
CÁLCULOS CONCLUÍDOS
```

```text
SHARES
```

```text
SHARE RATE
```

```text
INTERESSE NO CHECK-UP
```

e tráfego por:

```text
direct
organic
social
referral
share
```

quando tecnicamente disponível.

---

# 90. Dashboard SEO

Separadamente acompanhar:

```text
impressions
clicks
CTR
average_position
indexed_pages
```

e principais:

```text
queries
pages
```

Não misturar ranking de busca com métricas de produto.

---

# 91. Métricas De Confiança

Abertura de metodologia pode ser acompanhada.

Mas:

> methodology_opened alto

não significa necessariamente problema.

Pode representar:

- curiosidade;
- confiança;
- jornalistas;
- usuários técnicos.

Interpretar junto com outras métricas.

---

# 92. Recalculações

`recalculate_clicked` pode indicar:

- exploração;
- curiosidade;
- comparação de cenários.

É um comportamento potencialmente valioso.

Não tratá-lo automaticamente como erro de UX.

---

# 93. Métrica De Continuidade

```text
financial_checkup_interest
/
calculation_completed
```

pode revelar a demanda pela segunda grande etapa do produto.

Essa métrica ajudará a decidir quando priorizar o check-up.

---

# 94. Guardrails

Crescimento nunca pode prejudicar:

### Metodologia

Não alterar números para gerar reação.

### Privacidade

Não coletar renda para segmentação.

### Performance

Não adicionar scripts excessivos.

### UX

Não inserir pop-ups antes do resultado.

### Confiança

Não produzir clickbait contraditório com os dados.

---

# 95. Regra Para Dependências De Marketing

Antes de instalar:

- Google Analytics;
- Meta Pixel;
- TikTok Pixel;
- Hotjar;
- session replay;
- CRM;
- plataforma de marketing;

consultar:

`06-privacidade-seguranca.md`

A ferramenta não entra apenas porque facilita marketing.

---

# 96. SEO E Performance Devem Ser Testados

Antes de produção:

- validar metadata;
- inspecionar HTML;
- testar canonical;
- testar sitemap;
- testar robots;
- testar Open Graph;
- testar dados estruturados quando existentes;
- testar mobile;
- medir Core Web Vitals;
- inspecionar indexação.

---

# 97. Checklist SEO V1

- H1 único e claro;
- title definido;
- meta description definida;
- canonical correto;
- Open Graph;
- HTML indexável;
- sitemap.xml;
- robots.txt;
- lang `pt-BR`;
- links internos;
- metodologia indexável;
- página de privacidade;
- Search Console configurado;
- domínio canônico consistente;
- previews/staging fora do índice;
- Core Web Vitals revisados.

---

# 98. Checklist Analytics V1

- ferramenta definida;
- `calculator_view`;
- `calculation_started`;
- `calculation_completed`;
- `result_viewed`;
- `methodology_opened`;
- `share_clicked`;
- `share_native`;
- `share_whatsapp`;
- `copy_link`;
- `recalculate_clicked`;
- `financial_checkup_interest`;
- renda não enviada;
- moradores não enviados;
- percentis individuais não enviados;
- falha do analytics não quebra o produto;
- eventos testados em produção.

---

# 99. Checklist Compartilhamento V1

- botão visível após resultado;
- WhatsApp funcionando;
- Web Share funcionando quando suportado;
- copiar link funcionando;
- mensagem compreensível;
- renda não revelada;
- moradores não revelados;
- preview social correto;
- URL correta;
- mobile testado;
- evento registrado sem dados financeiros.

---

# 100. Checklist Pré-divulgação

Não iniciar divulgação ampla enquanto houver problema conhecido em:

- cálculo;
- metodologia;
- mobile;
- compartilhamento;
- privacidade;
- fontes;
- domínio;
- performance;
- analytics;
- indexação.

Viralizar um resultado errado é pior do que crescer devagar.

---

# 101. Regra Para O Codex

Ao trabalhar em SEO ou crescimento, o Codex deve:

1. consultar este documento;
2. respeitar `06-privacidade-seguranca.md`;
3. não adicionar tracking sem autorização;
4. não enviar dados financeiros;
5. manter conteúdo essencial indexável;
6. preservar canonical;
7. atualizar sitemap quando criar páginas indexáveis;
8. verificar metadata;
9. preservar performance;
10. não criar páginas SEO em massa sem solicitação;
11. não alterar metodologia para aumentar conversão;
12. adicionar ou atualizar testes relevantes.

---

# 102. Decisões Operacionais E Questões Abertas

Para a V1, ficam canonizados:

```text
PRODUCTION_DOMAIN = rendacomparada.com.br
CANONICAL_URL = https://rendacomparada.com.br
```

Esta decisão documental não implementa `rel="canonical"`, redirecionamentos, sitemap, `robots.txt`, Open Graph nem configuração de deploy.

Antes da divulgação ampla ainda devem ser definidos ou configurados:

```text
ANALYTICS_PROVIDER = [DEFINIR]
```

```text
SEARCH_CONSOLE_PROPERTY = [CONFIGURAR]
```

O texto padrão de compartilhamento já está fechado por D073:

```text
DEFAULT_SHARE_TEXT = "Descobri onde minha renda está na distribuição brasileira. E você?"
```

A posição só pode ser acrescentada por escolha explícita do usuário, conforme D017.

Continua aberto:

```text
DEFAULT_OG_IMAGE = [CRIAR]
```

Nenhum desses pontos deve ser inventado pelo Codex sem decisão explícita.

---

# 103. Definition of Done — SEO

SEO V1 estará pronto quando:

- Google puder acessar o conteúdo principal;
- metadata estiver correta;
- URL canônica estiver definida;
- sitemap estiver disponível;
- Search Console estiver configurado;
- página de metodologia estiver indexável;
- previews não competirem com produção;
- Open Graph estiver correto;
- performance estiver adequada;
- nenhuma renda estiver presente em URLs indexáveis.

---

# 104. Definition of Done — Analytics

Analytics V1 estará pronto quando for possível responder:

> Quantas pessoas chegaram?

> Quantas começaram o cálculo?

> Quantas concluíram?

> Quantas compartilharam?

> Qual canal de share escolheram?

> Quantas recalcularam?

> Quantas demonstraram interesse em continuar?

Sem saber:

> quanto essas pessoas ganham.

---

# 105. Definition of Done — Crescimento

A infraestrutura inicial de crescimento estará pronta quando o produto conseguir realizar este ciclo:

```text
PESSOA A
↓
CALCULA
↓
COMPARTILHA
↓
PESSOA B RECEBE
↓
ENTRA
↓
CALCULA
↓
COMPARTILHA
```

e conseguirmos medir esse comportamento de forma agregada sem criar rastreamento financeiro individual.

---

# 106. Norte De SEO

> **Não queremos aparecer para qualquer busca.**

Queremos aparecer quando alguém fizer uma pergunta que o Renda Comparada consegue responder melhor, com dados confiáveis e uma ferramenta útil.

---

# 107. Norte De Analytics

> **Medir comportamento, não a vida financeira do usuário.**

Precisamos saber:

> “Ele calculou?”

Não precisamos saber:

> “Ele ganha R$ 17.300?”

---

# 108. Norte De Crescimento

O crescimento ideal acontece porque uma pessoa pensa:

> **“Isso é interessante.”**

Depois:

> **“Vou descobrir o meu.”**

Depois:

> **“Vou mandar para alguém.”**

E a próxima pessoa repete o ciclo.

A estratégia de crescimento do Renda Comparada deve ser construída sobre:

> # utilidade + curiosidade + confiança + compartilhamento

e não sobre:

> publicidade agressiva + coleta excessiva + clickbait.

O objetivo não é apenas gerar tráfego.

É construir uma ferramenta que as pessoas tenham motivo para usar, confiar e transmitir.
