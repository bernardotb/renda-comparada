---
title: Fase 3 — Contrato de Interface da V1
created: 2026-08-14T16:28:00-03:00
status: proposta consolidada
canonical: false
depends_on:
  - D004
  - D015
  - D016
  - D017
  - D019
  - D030
  - D056
  - D063
  - D065
---

# Fase 3 — Contrato de Interface da V1

> **DOCUMENTO DE CONSOLIDAÇÃO — NÃO CANÔNICO.**
> Este contrato transforma decisões já tomadas em especificação operacional de interface.
> Não altera a metodologia estatística e não autoriza integração do resultado Mundo antes da conclusão da Fase 2A.

## 1. Objetivo

A V1 deve permitir que uma pessoa, sem cadastro, responda rapidamente:

> **Onde a renda da minha casa me posiciona no Brasil e, de forma mais aproximada, no mundo?**

A experiência principal termina depois de:

```text
entrada
↓
resultado
↓
interpretação
↓
compartilhamento
```

Qualquer continuação financeira é opcional.

---

## 2. Primeira dobra

### Identidade

**RENDA COMPARADA**

### H1

> **Você é mais rico do que quantos brasileiros?**

### Subtítulo

> **Descubra onde a renda da sua família está no Brasil — e onde ela estaria no mundo.**

### Esclarecimento

> **A comparação é baseada em renda, não em patrimônio.**

Não colocar antes do formulário:

- estatísticas de apoio;
- cursos;
- check-up;
- artigos;
- outras calculadoras;
- coleta de e-mail;
- cadastro.

---

## 3. Campo de renda

### Label

> **Qual é a renda mensal total da sua casa?**

### Conceito operacional

A entrada representa a **renda mensal nominal vigente** no momento do cálculo.

O cálculo brasileiro ajusta essa quantia automaticamente para preços médios de 2025, conforme D065.

### Ajuda curta

> **Use a renda bruta mensal, antes de impostos e despesas.**

### “O que devo incluir?”

Texto recomendado:

> **Some os rendimentos mensais da casa antes de impostos e despesas, como salários e trabalho por conta própria, aposentadorias, pensões, aluguéis recebidos e outras rendas abrangidas pela metodologia. Não desconte aluguel, financiamento, cartão, plano de saúde ou gastos do mês.**

Nota:

A redação deve permanecer subordinada ao conceito estatístico de `04-metodologia-dados.md`. A interface não deve prometer uma identidade perfeita entre uma pergunta simples ao usuário e todas as classificações operacionais da PNAD.

---

## 4. Campo de moradores

### Label

> **Quantas pessoas fazem parte deste domicílio?**

### Ajuda principal

> **Inclua adultos e crianças, mesmo que não tenham renda.**

### Ajuda expandida

> **Para manter o cálculo compatível com o indicador do IBGE, existem algumas exclusões técnicas: empregado doméstico residente, parente de empregado doméstico e “pensionista” na classificação da condição no domicílio. Nesse contexto, “pensionista” é uma categoria técnica do IBGE e não deve ser confundida automaticamente com quem recebe pensão.**

A interface principal não deve abrir com essas exceções. Elas ficam em ajuda contextual.

### Validação

Aceitar apenas:

```text
inteiro >= 1
```

Rejeitar:

```text
0
negativo
fração
texto inválido
```

---

## 5. CTA

Botão principal:

> **Descobrir minha posição**

Regras:

- uma única ação primária;
- sem resultado pré-preenchido;
- não calcular a cada tecla;
- validar antes do cálculo;
- não criar loading artificial se o resultado for instantâneo.

---

## 6. Estado inicial

A página abre sem renda fictícia e sem percentil fictício.

Antes do primeiro cálculo:

- os cards de resultado não devem exibir valores demonstrativos que possam parecer resultados;
- pode haver skeleton neutro apenas se houver necessidade visual;
- exemplos metodológicos devem ficar fora da área que o usuário interpreta como seu resultado.

---


## 6A. Carregamento do motor Brasil

A CDF brasileira não pertence ao bundle inicial da home.

No primeiro cálculo:

```text
CTA
↓
obter/validar manifestos pequenos
↓
carregar brazil-income-cdf-2025.json se necessário
↓
calcular no navegador
```

Regras:

- nenhuma renda ou número de moradores entra na URL da CDF;
- manter a CDF em memória para “Simular outra renda”;
- cache HTTP do dataset estático é permitido e não constitui persistência de dado financeiro pessoal;
- se os artefatos falharem, mostrar indisponibilidade; não ativar fallback antigo;
- o estado de loading deve ser acessível e corresponder a trabalho real.

Diagnóstico local da CDF atual: 3.955.036 bytes brutos e 1.788.882 bytes em gzip -9 local. Esses números não são promessa de transferência em produção.

---

## 7. Resultado Brasil

### Hierarquia recomendada

A leitura mais intuitiva deve vir antes da nomenclatura estatística.

Exemplo conceitual:

> **Você está entre aproximadamente os 30% de maior renda no Brasil.**

Secundário:

> **Percentil 70**

Explicação:

> **Sua renda por pessoa está acima da observada para aproximadamente 70 em cada 100 pessoas consideradas na distribuição brasileira utilizada.**

Não afirmar que:

- 70% das famílias ganham menos;
- 70% dos salários são menores;
- a posição mede patrimônio;
- a posição é exata.

### Fonte

Exibir de forma acessível:

> **Brasil: IBGE — PNAD Contínua 2025**

E, em detalhes:

> **A renda informada é ajustada pelo IPCA oficial para a mesma referência monetária da distribuição: preços médios de 2025.**

O mês do IPCA utilizado deve vir do manifesto de produção, não de texto hardcoded.

---

## 8. Renda por pessoa

A renda por pessoa fica como **informação secundária dentro do resultado**.

Exemplo:

> **Sua renda mensal atual por pessoa: R$ 2.166,67**

Abaixo ou em “Como calculamos”:

> **Para comparar com a PNAD 2025, o valor atual é ajustado automaticamente pela inflação para preços médios de 2025.**

Não destacar o valor monetário ajustado como se fosse uma nova “renda real” do usuário.

O valor ajustado pode aparecer na metodologia detalhada para auditabilidade.

---

## 9. Resultado Mundo

A estrutura visual pode ser semelhante, mas a linguagem não pode sugerir equivalência metodológica com o Brasil.

Título:

> **Mundo**

Resultado:

> **Posição global estimada**

Exemplo conceitual, somente após a Fase 2A fechar a CDF:

> **Você está aproximadamente entre os X% de maior nível monetário por pessoa na distribuição global utilizada pelo Banco Mundial.**

Explicação curta:

> **A comparação mundial é mais aproximada: o Banco Mundial combina pesquisas de países que usam renda ou consumo e ajusta os valores por poder de compra.**

Não usar como frase canônica:

> “Você ganha mais do que X% do mundo.”

antes de demonstrar que essa simplificação é metodologicamente defensável.

---

## 10. Brasil e Mundo

### Mobile

Ordem vertical:

```text
Brasil
↓
Mundo
```

### Desktop

Cards podem ficar lado a lado se:

- Brasil continuar primeiro na ordem semântica;
- a leitura não sugerir que ambos têm a mesma precisão;
- a versão mobile não for prejudicada.

---

## 11. Precisão visual

### Brasil — canônico por D071

A precisão visual brasileira está fechada e não depende mais da Fase 2A.

Para a faixa principal:

```text
percentil_exibido = arredondar(100 × shareBelow)
TOP_exibido = 100 - percentil_exibido
```

Exemplo:

```text
Percentil 69
TOP 31%
```

Para a cauda superior:

```text
TOP >= 1%        → inteiro
0,1% <= TOP < 1% → uma casa decimal
TOP < 0,1%       → “TOP < 0,1%” / frase editorial equivalente
```

Regras especiais:

- nunca `TOP 0%`;
- acima do maior RDPC observado, mostrar limite da pesquisa e não extrapolar;
- para renda zero, não usar `TOP 100%` como headline;
- valores monetários exibidos podem usar duas casas;
- cálculo interno permanece sem arredondamento prematuro.

### Mundo — ainda bloqueado

A precisão visual do Mundo permanece pendente de D070 e deverá ser derivada do erro efetivamente medido em D068/D069.

Não copiar automaticamente a regra brasileira para o resultado mundial.

---

## 12. Interpretação

Depois dos cards:

### O que isso significa?

Brasil:

> **O número mostra a posição da sua renda domiciliar por pessoa dentro da distribuição brasileira utilizada. Pessoas com renda igual podem ocupar o mesmo ponto da distribuição.**

Mundo:

> **O resultado mundial é uma estimativa de posição monetária comparável por poder de compra e possui limitações maiores que o resultado brasileiro.**

---

## 13. Compartilhamento

O compartilhamento vem antes de qualquer check-up, cadastro ou conteúdo adicional.

Título:

> **Compartilhar**

Garantia visível:

> **Sua renda não será mostrada.**

### Modo padrão

O compartilhamento padrão é **genérico**.

Texto recomendado:

> **Descobri onde minha renda está na distribuição brasileira. E você?**

Não contém:

- renda;
- moradores;
- renda por pessoa;
- percentil;
- `TOP`.

### Revelar posição

A posição só entra no compartilhamento após uma ação explícita do usuário.

Modelo:

> **Minha renda está aproximadamente entre os X% de maior renda na distribuição brasileira. E você?**

Mesmo nesse modo, nunca incluir:

- renda;
- moradores;
- renda por pessoa.

---

## 14. Interação de compartilhamento

Recomendação de UX:

1. botão principal **Compartilhar**;
2. ao abrir a ação de compartilhamento, o modo padrão permanece genérico;
3. opção explícita e inicialmente desmarcada:

> **Incluir minha posição — sem mostrar minha renda**

4. canais:
   - Web Share API, quando disponível;
   - WhatsApp;
   - copiar link.

O link permanece público e genérico. O resultado individual entra apenas no texto visível do compartilhamento quando o usuário escolhe incluí-lo.

---

## 15. URL compartilhada

Nunca codificar no link:

```text
renda
moradores
renda_per_capita
percentil
top_percent
```

A URL pode utilizar UTMs genéricos, por exemplo:

```text
utm_source=share
utm_medium=whatsapp
```

desde que não carreguem dado pessoal ou financeiro.

---

## 16. Card social

### Open Graph padrão

Genérico:

```text
RENDA COMPARADA

Você é mais rico do que
quantos brasileiros?

Descubra sua posição.
```

### Card individual

Se a V1 oferecer card com `TOP X%`:

- somente após escolha explícita;
- preferir geração no cliente;
- não criar URL pública individual com o resultado;
- fallback para texto se o compartilhamento de imagem não estiver disponível.

---

## 17. Privacidade operacional

Na V1:

```text
renda + moradores
↓
estado em memória
↓
cálculo no navegador
↓
resultado
```

Por padrão:

- sem banco de dados;
- sem persistência da renda;
- sem `localStorage` da renda;
- sem `sessionStorage` da renda;
- sem renda em URL;
- sem renda em logs;
- sem renda em analytics;
- sem renda em error tracking;
- sem session replay capturando campos.

Recarregar a página pode apagar os valores.

---

## 18. Analytics mínimo

Eventos:

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

Somente quando necessários:

```text
page
share_channel
share_mode
app_version
```

`share_mode` pode ser:

```text
generic
position
```

### Proibido

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

Não transformar renda ou resultado em faixas para burlar a regra.

---

## 19. Fornecedor de analytics

Continua aberto:

```text
ANALYTICS_PROVIDER = [DEFINIR]
```

O fornecedor deve ser escolhido somente depois de auditoria de:

- cookies;
- coleta automática;
- IP;
- transferência internacional;
- eventos customizados;
- política de retenção;
- impacto de performance.

A ausência do fornecedor não bloqueia a especificação da taxonomia.

---

## 20. Continuação opcional

Depois do compartilhamento:

Título:

> **Sua posição de renda conta apenas uma parte da história.**

Pergunta:

> **Quer entender melhor sua vida financeira?**

CTA:

> **Quero entender melhor**

O check-up completo continua fora do escopo obrigatório da V1.

Não usar:

> “O resultado te agradou?”

---

## 21. Simular novamente

Ação secundária:

> **Simular outra renda**

Pode preservar os valores atuais enquanto a página permanecer aberta.

Não exige reload.

Analytics:

```text
recalculate_clicked
```

sem valores financeiros.

---

## 22. Estados de erro

### Renda vazia

> **Informe a renda mensal da sua casa.**

### Renda inválida

> **Digite um valor válido em reais.**

### Renda negativa

> **A renda não pode ser negativa.**

### Moradores vazios

> **Informe quantas pessoas fazem parte do domicílio.**

### Zero

> **O número de pessoas deve ser pelo menos 1.**

### Fração

> **Use um número inteiro de pessoas.**

### Dataset indisponível

> **Não foi possível calcular sua posição agora. Tente novamente.**

Não mostrar resultado antigo ou aproximado como fallback silencioso.

---

## 23. Renda zero

Se renda zero for informada e validada:

- não bloquear por moralismo;
- calcular segundo a regra do dataset;
- preservar empates na CDF;
- usar linguagem neutra;
- não sugerir situação financeira individual a partir disso.

---

## 24. Acessibilidade

Obrigatório:

- labels reais;
- erros associados aos campos;
- foco visível;
- operação por teclado;
- boa área de toque;
- `aria-live` para feedback de erro/resultado quando adequado;
- não depender apenas de cor;
- respeitar `prefers-reduced-motion`;
- não animar números de modo que impeça leitura por tecnologia assistiva.

---

## 25. O que fica bloqueado

Este contrato não resolve:

```text
WORLD_CDF
WORLD_BRL_TO_2021_PPP
WORLD_GOLDEN_CASES
WORLD_DISPLAY_PRECISION_FINAL
ANALYTICS_PROVIDER
PRODUCTION_DOMAIN
DEFAULT_OG_IMAGE
```

Também não autoriza alterar `src/App.tsx` antes de o motor Mundo e os fixtures correspondentes estarem fechados.

---

## 26. Definition of Done do contrato

Antes de enviar a implementação ao Codex:

- [x] entrada Brasil conceitualmente definida;
- [x] alinhamento temporal Brasil canonizado;
- [x] moradores e exceções documentados;
- [x] jornada principal definida;
- [x] resultado Brasil textual especificado;
- [x] renda por pessoa posicionada como secundária;
- [x] compartilhamento padrão privado definido;
- [x] compartilhamento de posição exige ação explícita;
- [x] dados proibidos em URL/analytics definidos;
- [x] taxonomia mínima de eventos definida;
- [x] continuação opcional definida;
- [ ] metodologia Mundo canonizada;
- [ ] golden cases Mundo criados;
- [x] precisão final Brasil definida por D071;
- [ ] precisão final Mundo definida por D070;
- [ ] fornecedor de analytics aprovado;
- [ ] domínio de produção definido.

---

## 27. Resumo do fluxo

```text
[HOME]
  H1
  renda atual
  moradores
  Descobrir minha posição
        ↓
[VALIDAÇÃO]
        ↓
[CÁLCULO LOCAL]
        ↓
[BRASIL]
  TOP
  percentil
  interpretação
        ↓
[MUNDO]
  posição estimada
  ressalva metodológica
        ↓
[FONTES / COMO CALCULAMOS]
        ↓
[COMPARTILHAR]
  padrão genérico
  opção explícita de incluir posição
        ↓
[FIM DA EXPERIÊNCIA PRINCIPAL]
        ↓
[CONTINUAÇÃO OPCIONAL]
  Quer entender melhor sua vida financeira?
```
