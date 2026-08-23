---
title: Avaliação — Analytics V1
created: 2026-08-14T16:44:00-03:00
status: avaliação — revisão 0.2
canonical: false
---

# Avaliação — Analytics V1

## Resultado

**Vercel Web Analytics é um candidato tecnicamente compatível com os princípios de privacidade da V1, mas não está canonizado como fornecedor.**

A decisão final depende de:

- plano efetivamente utilizado;
- necessidade de eventos personalizados;
- inventário de fornecedores;
- revisão de privacidade/conformidade da versão publicada.

## Evidências oficiais

A documentação da Vercel informa que o Web Analytics:

- não utiliza cookies;
- trabalha com dados anonimizados/agregados;
- não associa os dados a um indivíduo ou endereço IP para reconstrução de navegação individual;
- descarta o identificador de sessão após 24 horas;
- coleta dados como URL, referrer, localização aproximada, sistema operacional, navegador e tipo de dispositivo;
- permite usar `beforeSend` para redigir ou descartar eventos/rotas com dados sensíveis;
- permite eventos personalizados em planos compatíveis.

Fontes:

- https://vercel.com/docs/analytics
- https://vercel.com/docs/analytics/privacy-policy
- https://vercel.com/docs/analytics/redacting-sensitive-data
- https://vercel.com/docs/analytics/custom-events
- https://vercel.com/docs/analytics/limits-and-pricing

## Compatibilidade com o Renda Comparada

O projeto já proíbe renda e resultado individual em URL.

Isso reduz um risco importante, porque Web Analytics coleta automaticamente informações de página e URL.

Mesmo assim, se Vercel Web Analytics for adotado:

1. não enviar renda ou resultado em eventos customizados;
2. não colocar dados financeiros em URL/query/hash;
3. usar `beforeSend` como defesa adicional;
4. limitar eventos customizados à taxonomia aprovada;
5. permitir apenas parâmetros categóricos não financeiros;
6. não habilitar Drains sem decisão específica;
7. registrar o fornecedor na política pública e no inventário de terceiros.

## Taxonomia compatível

```text
calculator_view
calculation_started
calculation_completed
result_viewed
methodology_opened
share_clicked
share_native
share_whatsapp
copy_link
recalculate_clicked
financial_checkup_interest
```

Parâmetros máximos recomendados:

```text
page
share_channel
share_mode
app_version
```

Nunca:

```text
income
income_band
household_size
per_capita_income
percentile
top_percent
```

## Limitação de plano — confirmada

A documentação oficial consultada em 14/08/2026 diferencia claramente os planos:

```text
Hobby................ Web Analytics disponível; 50.000 eventos incluídos/mês; janela de 1 mês
Hobby................ custom events NÃO disponíveis
Pro.................. custom events disponíveis; até 2 propriedades por evento na configuração padrão
Enterprise........... custom events disponíveis
```

Fontes oficiais:

- https://vercel.com/docs/analytics/custom-events
- https://vercel.com/docs/analytics/limits-and-pricing
- https://vercel.com/docs/plans/hobby

Consequência:

> **a taxonomia de interações prevista pelo Renda Comparada exige Pro/Enterprise se for implementada integralmente por Vercel Web Analytics.**

Antes da implementação ainda é necessário verificar:

```text
VERCEL_PLAN = [VERIFICAR]
```

Se o projeto estiver em Hobby, existem apenas opções metodologicamente limpas:

1. lançar com analytics reduzido a pageviews/tráfego disponível no plano;
2. migrar para plano que suporte custom events;
3. avaliar outro fornecedor em auditoria própria.

É proibido simular eventos customizados por rotas, query strings ou fragmentos contendo dados do cálculo. A URL continua proibida de carregar renda, moradores, renda per capita, percentil ou `TOP`.

A falta de custom events não justifica ampliar a coleta ou escolher outro fornecedor sem nova auditoria.

## Estado

```text
VERCEL_WEB_ANALYTICS_COMPATIBILITY = candidato_aprovável
CUSTOM_EVENTS_REQUIRE = Pro_or_Enterprise
VERCEL_PLAN = [VERIFICAR]
ANALYTICS_PROVIDER = [NÃO CANONIZADO]
```
