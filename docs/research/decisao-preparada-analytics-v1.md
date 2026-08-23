---
title: Decisão Preparada — Analytics da V1
created: 2026-08-14T18:35:00-03:00
status: recomendação para decisão
canonical: false
---

# Decisão Preparada — Analytics da V1

## 1. Recomendação

Para a V1, a opção preferível é:

> **Vercel Web Analytics, com coleta mínima e sem dados financeiros em eventos.**

Alternativa conservadora:

> **lançar inicialmente apenas com page views agregados, sem eventos customizados, e adicionar eventos depois da validação da implementação.**

Não há necessidade de introduzir Google Analytics, pixels ou outra plataforma apenas para medir o funil básico.

---

## 2. Por que Vercel é um bom candidato

Segundo a documentação oficial vigente:

- Web Analytics está disponível nos planos Vercel;
- não utiliza cookies para identificar visitantes;
- armazena dados anonimizados/agregados;
- a identificação de visitante usa hash que é reiniciado diariamente;
- a sessão não é preservada indefinidamente;
- coleta automaticamente páginas e metadados como referrer, país aproximado, navegador, sistema operacional e dispositivo;
- permite `beforeSend` para redigir ou descartar eventos/URLs sensíveis;
- pode suportar eventos customizados conforme recursos/plano.

Isso é compatível com a arquitetura da V1 desde que a aplicação cumpra sua própria regra mais forte:

> renda, moradores, renda por pessoa e posição individual nunca entram em URL nem eventos.

---

## 3. Configuração mínima recomendada

### Page views

Permitidos, desde que as rotas sejam genéricas e não contenham resultados individuais.

### Eventos

Taxonomia aprovada do projeto:

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

### Parâmetros permitidos

```text
page
share_channel
share_mode
app_version
```

### Parâmetros proibidos

```text
income
income_band
household_size
per_capita_income
percentile
top_percent
brazil_percentile
world_percentile
```

Não enviar versões transformadas ou faixas desses valores para contornar a proibição.

---

## 4. Defesa em profundidade

Mesmo que a URL da V1 já seja projetada para não transportar renda:

1. configurar `beforeSend`;
2. descartar qualquer rota/evento que contenha parâmetros inesperados sensíveis;
3. manter testes automatizados garantindo ausência de renda em URL;
4. testar payloads de eventos;
5. não ativar Drains;
6. não ativar session replay de terceiros.

---

## 5. Opção A — Vercel Web Analytics completo da V1

**Prós**

- menor número de fornecedores;
- integração natural com a hospedagem;
- sem cookies do produto Web Analytics;
- dados agregados;
- page views e eventos no mesmo ecossistema;
- suficiente para o funil inicial.

**Contras**

- ainda é um terceiro processando telemetria;
- coleta metadados técnicos;
- exige atualização da política de privacidade;
- recursos de eventos/filtros podem depender de plano/configuração.

**Recomendação:** melhor escolha se os eventos necessários estiverem disponíveis no plano real.

---

## 6. Opção B — somente page views no lançamento

Ativar Web Analytics sem instrumentar inicialmente o funil customizado.

Medir:

- visitas;
- páginas;
- referrers;
- dispositivo;
- país aproximado.

Depois de validar privacidade e funcionamento, adicionar os eventos do funil.

**Vantagem:** menor risco de instrumentação errada antes do lançamento.

**Desvantagem:** menor capacidade de calcular conversão de cálculo/compartilhamento no início.

**Recomendação:** opção mais conservadora e perfeitamente aceitável.

---

## 7. Opção C — sem analytics no primeiro lançamento

Também é metodologicamente válida.

O produto funciona sem analytics.

**Vantagem:** mínimo absoluto de coleta e complexidade.

**Desvantagem:** perde a linha de base inicial de aquisição, conclusão do cálculo e compartilhamento.

Não é necessária apenas porque “privacidade é importante”; a opção B já preserva coleta bastante restrita.

---

## 8. Opções não recomendadas para a V1

Não introduzir agora, sem necessidade demonstrada:

- Google Analytics;
- Meta Pixel;
- TikTok Pixel;
- Hotjar;
- Microsoft Clarity;
- session replay;
- ferramentas de ad-tech.

Isso aumentaria fornecedores, coleta e superfície de privacidade sem benefício proporcional ao estágio atual.

---

## 9. Decisão sugerida

```text
ANALYTICS_PROVIDER = Vercel Web Analytics
LAUNCH_MODE = page views + eventos mínimos aprovados
SENSITIVE_FINANCIAL_ANALYTICS = prohibited
SESSION_REPLAY = prohibited
AD_PIXELS = prohibited
```

Se houver dúvida sobre disponibilidade de custom events no plano:

```text
LAUNCH_MODE = page views only
```

até a confirmação.

---

## 10. O que falta para canonizar

1. confirmar o plano/configuração efetivamente usados na Vercel;
2. decidir entre “page views only” e “eventos mínimos”;
3. registrar a decisão em `decisoes.md`;
4. atualizar `06-privacidade-seguranca.md`;
5. atualizar a política pública;
6. implementar e testar payloads.

Nenhuma dessas etapas exige coletar renda.
