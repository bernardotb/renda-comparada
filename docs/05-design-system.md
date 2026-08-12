---
title: 05-design-system
created: 2026-08-12T17:23:10.000-03:00
modified: 2026-08-12T17:28:42.575-03:00
---

# 05-design-system

# Design System — Renda Comparada

**Produto:** Renda Comparada  
**Documento:** `05-design-system.md`  
**Status:** Canônico para interface e apresentação visual  
**Versão:** 1.0  
**Última revisão:** 12/08/2026

Documentos relacionados:

- `01-visao-produto.md`
- `02-prd-v1.md`
- `03-jornada-ux-v1.md`
- `04-metodologia-dados.md`
- `06-privacidade-seguranca.md`

---

# 1. Função Deste Documento

Este documento define a linguagem visual e os princípios de interface do Renda Comparada.

Ele é a principal referência para:

- cores;
- tipografia;
- espaçamento;
- hierarquia;
- layout;
- formulários;
- botões;
- resultados;
- gráficos;
- cards;
- compartilhamento;
- animações;
- responsividade;
- acessibilidade visual;
- estados de interface.

Este documento não define:

- fórmulas estatísticas;
- fontes de dados;
- regras de privacidade;
- textos metodológicos;
- escopo funcional.

---

# 2. Conceito Visual Central

O Renda Comparada deve parecer:

> # Uma reportagem interativa premium que também é uma calculadora.

Não deve parecer:

> uma calculadora genérica;

> uma fintech promocional;

> um painel administrativo;

> um portal de ferramentas;

> um aplicativo de investimento;

> um jogo.

A experiência precisa transmitir simultaneamente:

**curiosidade + confiança + clareza + sobriedade**

---

# 3. Referências Conceituais

A linguagem visual deve buscar características presentes em:

### Jornalismo Econômico Premium

- sobriedade;
- leitura confortável;
- hierarquia editorial;
- confiança.

### Visualização De Dados

- números como protagonistas;
- gráficos funcionais;
- explicações próximas aos dados;
- ausência de decoração desnecessária.

### Produtos Digitais Minimalistas

- espaço;
- foco;
- simplicidade;
- poucas ações por tela;
- excelente comportamento no celular.

As referências são conceituais.

Não copiar a identidade visual de nenhuma publicação ou produto específico.

---

# 4. Princípios De Design

## 4.1 Clareza Antes De Decoração

Todo elemento deve ajudar o usuário a:

- entender;
- preencher;
- interpretar;
- decidir;
- compartilhar.

Se não fizer nenhuma dessas coisas, deve ser questionado.

---

## 4.2 Dados São Protagonistas

Percentis, valores e comparações devem possuir mais destaque que elementos decorativos.

Exemplo:

> **TOP 12%**

deve chamar mais atenção que:

> “Resultado da sua análise”.

---

## 4.3 Uma Ação Principal Por Momento

Na entrada:

> **Descobrir minha posição**

No resultado:

> **Compartilhar minha posição**

Depois:

> **Entender melhor minha vida financeira**

Não competir com três CTAs igualmente fortes na mesma área.

---

## 4.4 Informação Progressiva

Mostrar primeiro:

> o que o usuário precisa saber agora.

Mostrar detalhes:

> quando ele quiser entender mais.

A metodologia completa não deve ocupar a primeira dobra.

---

## 4.5 Sobriedade

Renda e desigualdade são temas sensíveis.

Evitar qualquer estética que transforme o resultado em prêmio, competição ou ostentação.

---

# 5. Personalidade Visual

A interface deve parecer:

- inteligente;
- contemporânea;
- brasileira sem caricatura;
- editorial;
- confiável;
- calma;
- sofisticada;
- humana.

Não deve parecer:

- bancária;
- burocrática;
- governamental;
- luxuosa;
- ostentatória;
- infantil;
- gamificada.

---

# 6. Paleta Principal

A paleta deve ser reduzida.

## Fundo Principal

```css
--color-bg: #F7F5F0;
```

Uso:

- fundo geral da página;
- grandes áreas editoriais.

Objetivo:

> fugir do branco absoluto e produzir sensação de papel/editorial.

---

## Superfície

```css
--color-surface: #FFFFFF;
```

Uso:

- cards;
- formulário;
- áreas elevadas;
- modais quando necessários.

---

## Texto Principal

```css
--color-text-primary: #181A18;
```

Uso:

- títulos;
- corpo;
- números importantes.

Evitar preto absoluto quando não necessário.

---

## Texto Secundário

```css
--color-text-secondary: #62665F;
```

Uso:

- explicações;
- metadados;
- fontes;
- legendas.

---

## Bordas

```css
--color-border: #DDDCD6;
```

Uso:

- inputs;
- divisórias;
- cards discretos.

---

# 7. Cor Brasil

A identidade brasileira deve utilizar um verde profundo e sóbrio.

```css
--color-brazil: #1F5A46;
--color-brazil-soft: #E7F0EB;
```

Uso:

- resultado Brasil;
- marcadores;
- gráficos;
- destaques pontuais.

Não utilizar verde bandeira saturado como cor dominante.

---

# 8. Cor Mundo

Para o resultado internacional, utilizar azul petróleo / azul profundo.

```css
--color-world: #28536B;
--color-world-soft: #E8EFF3;
```

Uso:

- resultado Mundo;
- gráficos internacionais;
- destaques complementares.

---

# 9. Cores De Estado

## Sucesso

```css
--color-success: #2E6A4E;
```

Usar com moderação.

Não utilizar para indicar:

> “renda boa”.

Sucesso deve significar:

- ação concluída;
- link copiado;
- dado salvo;
- operação realizada.

---

## Atenção

```css
--color-warning: #9A6B20;
```

Uso futuro:

- avisos;
- limitações;
- atenção financeira.

---

## Erro

```css
--color-error: #A13C36;
```

Uso:

- entrada inválida;
- falha de processamento;
- erro técnico.

---

# 10. Regra Para Cores De Renda

Nunca usar automaticamente:

```text
verde = rico
vermelho = pobre
```

Percentil não é um indicador moral ou de saúde financeira.

A posição deve ser comunicada de forma neutra.

---

# 11. Tipografia

O sistema deverá utilizar duas famílias tipográficas:

## Editorial

Para:

- H1;
- headlines;
- chamadas;
- frases conceituais.

## Interface

Para:

- formulários;
- números;
- botões;
- gráficos;
- labels;
- textos corridos;
- navegação.

---

# 12. Família Editorial Recomendada

Opção inicial:

> **Source Serif 4**

Fallback:

```css
font-family:
  "Source Serif 4",
  Georgia,
  "Times New Roman",
  serif;
```

Razões:

- boa leitura;
- aparência editorial;
- adequada para títulos;
- não transmite luxo excessivo.

---

# 13. Família De Interface Recomendada

Opção inicial:

> **Inter**

Fallback:

```css
font-family:
  Inter,
  system-ui,
  -apple-system,
  BlinkMacSystemFont,
  "Segoe UI",
  sans-serif;
```

Usar para:

- inputs;
- botões;
- números;
- textos;
- gráficos.

---

# 14. Regra Tipográfica

Não utilizar mais de:

> **duas famílias tipográficas principais.**

Não misturar fontes decorativas.

---

# 15. Escala Tipográfica

Valores de referência.

## Display

```css
--font-display-desktop: 64px;
--font-display-mobile: 42px;
```

Uso:

> “Você é mais rico do que quantos brasileiros?”

---

## H1

```css
--font-h1-desktop: 48px;
--font-h1-mobile: 36px;
```

---

## H2

```css
--font-h2-desktop: 34px;
--font-h2-mobile: 28px;
```

---

## H3

```css
--font-h3: 22px;
```

---

## Corpo Grande

```css
--font-body-lg: 20px;
```

---

## Corpo

```css
--font-body: 17px;
```

---

## Corpo Pequeno

```css
--font-body-sm: 14px;
```

---

## Metadados

```css
--font-meta: 13px;
```

---

# 16. Line Height

Títulos:

```css
line-height: 1.05–1.15;
```

Corpo:

```css
line-height: 1.5–1.7;
```

Números grandes:

```css
line-height: 0.95–1.05;
```

---

# 17. Números

Resultados numéricos devem usar:

- Inter;
- peso 600–700;
- números tabulares quando disponível;
- excelente contraste.

Exemplo:

> **67,9%**

> **TOP 32%**

> **R$ 2.166**

Números são conteúdo, não decoração.

---

# 18. Resultado Principal

O número mais importante da página deve ser visualmente maior que qualquer texto secundário.

Exemplo:

```text
BRASIL

67,9%

Percentil aproximado

TOP 32%
```

A hierarquia visual deve permitir compreender o resultado antes de ler o parágrafo explicativo.

---

# 19. Espaçamento

Adotar escala consistente baseada em múltiplos de 4.

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 24px;
--space-6: 32px;
--space-7: 48px;
--space-8: 64px;
--space-9: 96px;
--space-10: 128px;
```

Não utilizar valores aleatórios sem necessidade.

---

# 20. Espaço Editorial

A página deve possuir bastante espaço vertical.

Seções importantes devem respirar.

Desktop:

```text
64–128 px entre grandes blocos
```

Mobile:

```text
48–80 px entre grandes blocos
```

Evitar densidade de dashboard.

---

# 21. Largura De Conteúdo

## Conteúdo Editorial

```css
max-width: 720px;
```

Uso:

- textos;
- metodologia;
- FAQ.

## Área De Produto

```css
max-width: 1120px;
```

Uso:

- formulário;
- Brasil × Mundo;
- gráficos.

---

# 22. Grid

Desktop:

> grid de até 12 colunas.

Tablet:

> 6–8 colunas.

Mobile:

> uma coluna predominante.

Não manter dois cards lado a lado no celular apenas para preservar simetria.

---

# 23. Breakpoints

Valores iniciais:

```css
--bp-sm: 640px;
--bp-md: 768px;
--bp-lg: 1024px;
--bp-xl: 1280px;
```

O layout deve responder ao conteúdo, não apenas aos breakpoints.

---

# 24. Mobile First

O produto deve ser projetado primeiro para celular.

Cenário prioritário:

```text
WhatsApp
↓
abre link
↓
digita renda
↓
calcula
↓
vê resultado
↓
compartilha
```

Esse fluxo precisa ser excelente.

---

# 25. Hero

A primeira dobra deve ser simples.

Estrutura:

```text
RENDA COMPARADA

Você é mais rico do que
quantos brasileiros?

Descubra onde a renda da sua família
está no Brasil — e onde ela estaria
no mundo.

[FORMULÁRIO]
```

Não colocar:

- foto;
- ilustração;
- gráfico complexo;
- estatística enorme;
- vídeo;
- animação decorativa.

A pergunta é o elemento visual principal.

---

# 26. Nome Da Marca

`RENDA COMPARADA`

Pode aparecer em:

- caixa alta;
- tamanho pequeno;
- tracking discreto;
- peso médio.

A marca não deve competir com o headline.

---

# 27. Formulário

O formulário deve parecer simples, quase editorial.

Evitar aparência de:

> cadastro bancário.

Campos grandes, claros e confortáveis.

---

# 28. Input Monetário

Estrutura:

```text
Qual é a renda mensal total da sua casa?

R$  6.500
──────────────────
```

ou variação com borda discreta.

O valor deve possuir destaque suficiente para leitura imediata.

---

# 29. Campo De Moradores

Preferência inicial:

```text
Quantas pessoas moram nesta casa?

−      3      +
```

Texto:

> Inclua adultos e crianças, mesmo que não tenham renda.

O componente deve possuir área de toque ampla.

---

# 30. Altura Mínima De Controles

Botões e controles:

```css
min-height: 48px;
```

Preferencialmente:

```css
48–56px
```

em mobile.

---

# 31. Botão Principal

CTA:

> **Descobrir minha posição**

Características:

- preenchimento sólido;
- contraste forte;
- largura generosa;
- texto objetivo.

Cor inicial:

```css
background: var(--color-text-primary);
color: white;
```

ou verde profundo quando houver justificativa.

Evitar botão fluorescente.

---

# 32. Botão Secundário

Utilizar:

- fundo transparente;
- borda discreta;
- menor hierarquia.

Exemplos:

> Como calculamos

> Simular outra renda

---

# 33. Links

Links editoriais devem ser reconhecíveis sem parecer banners.

Preferência:

- sublinhado;
- mudança discreta de peso/cor.

Não depender apenas de cor para acessibilidade.

---

# 34. Border Radius

Sistema inicial:

```css
--radius-sm: 6px;
--radius-md: 12px;
--radius-lg: 20px;
```

Evitar:

> todos os componentes com 32px de arredondamento.

O produto não deve parecer uma fintech genérica baseada em “pílulas”.

---

# 35. Sombras

Usar raramente.

Preferência:

> borda + contraste de superfície.

Quando necessário:

```css
box-shadow:
  0 8px 30px rgba(0, 0, 0, 0.05);
```

Evitar sombras fortes e múltiplas camadas.

---

# 36. Cards

Cards são permitidos quando representam unidades conceituais reais.

Exemplo:

```text
BRASIL
TOP 32%
```

e:

```text
MUNDO
TOP 23%
```

Não colocar cada parágrafo dentro de um card.

---

# 37. Resultado Brasil × Mundo

## Desktop

Pode usar dois painéis:

```text
┌─────────────────┐  ┌─────────────────┐
│ BRASIL          │  │ MUNDO           │
│                 │  │                 │
│ 67,9%           │  │ 76,6%           │
│ TOP 32%         │  │ TOP 23%         │
└─────────────────┘  └─────────────────┘
```

## Mobile

Preferência:

```text
BRASIL
↓
MUNDO
```

em sequência vertical.

---

# 38. Hierarquia Dentro Do Resultado

Ordem:

1. contexto: Brasil/Mundo;
2. número principal;
3. TOP percentual;
4. interpretação;
5. visualização;
6. fonte;
7. metodologia.

---

# 39. Brasil

Utilizar:

```css
--color-brazil
```

em:

- marcador;
- linha;
- pequeno detalhe;
- número secundário;
- badge discreto.

Não pintar todo o card de verde saturado.

---

# 40. Mundo

Utilizar:

```css
--color-world
```

com a mesma lógica.

A distinção deve ser perceptível, mas discreta.

---

# 41. Visualização Percentílica

Uma visualização recomendada:

```text
menor renda                       maior renda
│──────────────────────●────────────────│
                       você
```

Ela deve mostrar:

> posição.

Não apenas ser bonita.

---

# 42. Barra Percentílica

Pode usar:

- linha fina;
- marcador circular;
- labels nos extremos;
- tooltip opcional.

Não usar:

- velocímetro;
- gauge semicircular;
- ponteiro de carro;
- medalhas;
- troféus.

---

# 43. Curva De Distribuição

Pode ser utilizada futuramente se:

- representar corretamente os dados;
- ajudar na interpretação;
- for legível no celular.

Não usar curva genérica sem relação com a distribuição real.

---

# 44. Gráficos

Todo gráfico deve responder a uma pergunta.

Antes de implementar, perguntar:

> **O que o usuário aprende com isso que não aprenderia lendo o número?**

Se a resposta for:

> “fica mais bonito”

o gráfico provavelmente não deve existir.

---

# 45. Legendas

Usar linguagem simples.

Preferir:

> **Você**

> **Metade da população**

> **Top 10%**

em vez de nomenclatura estatística excessivamente técnica quando não necessária.

---

# 46. Precisão Visual

Não fazer a interface parecer mais precisa que os dados.

Se a metodologia recomenda:

```text
68%
```

não desenhar um marcador em:

```text
67,9324%
```

com precisão de pixel como se essa exatidão fosse real.

---

# 47. Compartilhamento

O bloco deve aparecer imediatamente após o resultado principal.

Estrutura:

```text
Compartilhe sua posição

Sua renda não será mostrada.

[ Compartilhar ]
[ WhatsApp ]
[ Copiar link ]
```

A frase de privacidade é parte da UX.

---

# 48. CTA De Compartilhamento

Pode ter mais destaque que ações secundárias.

Não precisa competir com o resultado.

Hierarquia:

```text
resultado
↓
interpretação
↓
compartilhamento
```

---

# 49. Card Social

O card social deve ser minimalista.

Formato conceitual:

```text
RENDA COMPARADA

TOP 12%

Minha posição na distribuição
de renda brasileira.

E você?
```

Não incluir por padrão:

- renda;
- número de moradores;
- nome;
- localização;
- patrimônio.

---

# 50. Identidade Do Card Social

Usar:

- fundo off-white;
- tipografia editorial;
- número grande;
- verde Brasil;
- marca discreta.

O card deve ser reconhecível como parte do mesmo produto.

---

# 51. Ponte Para Saúde Financeira

Depois do compartilhamento:

```text
Sua posição de renda conta
apenas uma parte da história.

Quer entender melhor sua
vida financeira?
```

Essa área deve possuir separação visual clara.

Não deve parecer parte obrigatória do cálculo.

---

# 52. Tom Visual Da Ponte

A transição deve parecer:

> aprofundamento.

Não:

> alerta.

Evitar vermelho, ícones de perigo ou mensagens dramáticas.

---

# 53. Conteúdo Editorial

Seções como:

- Como funciona;
- Renda × patrimônio;
- O que é percentil;
- Fontes;
- FAQ;

devem utilizar largura de leitura reduzida.

Exemplo:

```css
max-width: 720px;
```

Parágrafos não devem atravessar telas largas inteiras.

---

# 54. Divisores

Utilizar linhas discretas:

```css
border-color: var(--color-border);
```

ou espaço.

Evitar caixas para separar tudo.

---

# 55. Ícones

Usar somente quando:

- ajudam reconhecimento;
- economizam texto;
- representam ação clara.

Evitar ícones decorativos em cada título.

Não usar:

- saco de dinheiro;
- moedas;
- cofrinho;
- foguete financeiro;
- diamante;
- coroa.

---

# 56. Emojis

Na interface final, preferir:

> ícones próprios ou texto.

Emojis podem ser usados durante prototipagem.

Não transformar:

🇧🇷 🌎 💰 🚀

em linguagem visual permanente do produto.

---

# 57. Bandeira Do Brasil

Pode ser utilizada pontualmente.

Entretanto, a identidade brasileira deve vir principalmente de:

- linguagem;
- conteúdo;
- dados;
- verde profundo.

Não criar estética patriótica.

---

# 58. Movimento

Animações devem explicar transição ou mudança de estado.

Permitidas:

- fade;
- slide curto;
- marcador deslocando;
- número contando suavemente;
- expansão de metodologia.

---

# 59. Duração De Animação

Referência:

```css
--motion-fast: 120ms;
--motion-normal: 220ms;
--motion-slow: 400ms;
```

Resultados podem usar até:

```text
500–700ms
```

quando a animação representar a posição.

Evitar animações longas.

---

# 60. Easing

Preferir movimento natural:

```css
ease-out
```

ou curvas suaves equivalentes.

Evitar bounce.

---

# 61. Respeitar Redução De Movimento

Quando:

```css
prefers-reduced-motion: reduce
```

reduzir ou remover animações não essenciais.

---

# 62. Animações Proibidas

Não usar:

- confete;
- fogos;
- moedas caindo;
- cassino;
- slot machine;
- números girando por vários segundos;
- som automático;
- vibração decorativa.

---

# 63. Loading

Se o cálculo for instantâneo:

> não criar loading artificial.

Se necessário:

```text
Calculando sua posição…
```

com feedback simples.

Evitar skeleton complexo para operação de milissegundos.

---

# 64. Erros

Erros devem aparecer próximos do campo relevante.

Exemplo:

> **Informe um valor válido.**

Cor:

```css
--color-error
```

Também usar:

- texto;
- ícone opcional;
- `aria-describedby`.

Não depender apenas da borda vermelha.

---

# 65. Estado Desabilitado

Botões desabilitados devem continuar legíveis.

Não reduzir opacidade a ponto de impossibilitar leitura.

---

# 66. Foco

Todos os elementos interativos devem possuir:

> **focus visible**

claramente perceptível.

Exemplo:

```css
outline: 3px solid rgba(…);
outline-offset: 2px;
```

---

# 67. Contraste

Buscar no mínimo conformidade com:

> **WCAG AA**

para textos e controles relevantes.

Cor nunca deve ser a única forma de transmitir estado.

---

# 68. Tamanho De Texto

Não utilizar corpo principal inferior a:

```text
16px
```

em celular.

Preferência:

```text
17px
```

---

# 69. Leitura Em Celular

Evitar:

- linhas excessivamente longas;
- blocos densos;
- tabelas horizontais;
- texto pequeno;
- tooltip indispensável.

Informação essencial deve funcionar sem hover.

---

# 70. Hover

Hover é aprimoramento de desktop.

Nunca deve ser necessário para compreender ou utilizar uma função.

---

# 71. Navegação

A V1 deve possuir navegação mínima.

Possíveis itens:

```text
Como funciona
Metodologia
Sobre
```

A calculadora é o centro.

Não criar mega menu.

---

# 72. Header

Header deve ser discreto.

Desktop:

```text
RENDA COMPARADA       Como funciona  Metodologia
```

Mobile:

- marca;
- menu simples, se necessário.

Não usar header muito alto.

---

# 73. Footer

Pode conter:

- metodologia;
- fontes;
- privacidade;
- sobre;
- atualização dos dados;
- contato futuro.

Visualmente discreto.

---

# 74. Metadados De Fonte

Exemplo:

```text
Fonte: IBGE — PNAD Contínua 2025
Atualização: agosto de 2026
```

Usar:

- corpo pequeno;
- cinza secundário;
- links acessíveis.

---

# 75. Conteúdo De Confiança

Informações como:

> Como calculamos isso?

> De onde vêm os dados?

devem ser fáceis de encontrar.

Mas não precisam ser visualmente dominantes.

---

# 76. Responsividade Do Resultado

## Mobile

```text
Brasil
[resultado]

Mundo
[resultado]

Compartilhar
```

## Desktop

```text
Brasil             Mundo
[resultado]        [resultado]

      Compartilhar
```

---

# 77. Layout De Leitura Após Resultado

Abaixo do compartilhamento:

```text
Sua posição é apenas parte da história
↓
continuação opcional
↓
conteúdo educativo
↓
metodologia / FAQ
```

---

# 78. Não Transformar a home Em Dashboard

A home não deve abrir com:

- seis cards;
- menu lateral;
- tabelas;
- widgets;
- indicadores;
- gráficos simultâneos.

A sensação deve ser:

> **uma pergunta importante por vez.**

---

# 79. Futuras Ferramentas Financeiras

Quando simuladores forem adicionados, devem reutilizar:

- tipografia;
- campos;
- botões;
- cards;
- feedback;
- gráficos;
- espaçamento.

Não criar identidade própria para cada calculadora.

---

# 80. Custo Real Do Carro

Quando futuramente implementado, deve seguir a mesma lógica visual:

```text
Seu carro custa aproximadamente

R$ 2.150 / mês

21,5% da sua renda familiar
```

O significado financeiro é mais importante que a quantidade de inputs.

---

# 81. Moradia

Mesmo princípio:

```text
Sua moradia consome

32%

da renda familiar
```

Não apresentar dezenas de números sem hierarquia.

---

# 82. Saúde Financeira

Quando existir check-up, não usar semáforo simplista:

```text
verde = ótimo
amarelo = atenção
vermelho = ruim
```

sem contexto.

Cada dimensão deve possuir:

- estado;
- explicação;
- prioridade;
- próximo passo.

---

# 83. Score Financeiro

Não criar medidor circular tipo:

```text
72 / 100
```

na V1.

Caso algum score seja proposto futuramente, precisará de justificativa metodológica própria.

---

# 84. Linguagem Visual Para Orientação

Preferir:

> informação;

> comparação;

> contexto;

> próximo passo.

Evitar:

> julgamento;

> prêmio;

> punição;

> medo.

---

# 85. Performance Visual

Não carregar:

- vídeos;
- imagens grandes;
- bibliotecas pesadas;
- animações complexas;

sem necessidade.

A velocidade da primeira interação é parte da experiência.

---

# 86. Font Loading

Prioridades:

1. evitar bloqueio de renderização;
2. usar fallback adequado;
3. limitar pesos das famílias;
4. carregar apenas estilos necessários.

Inicialmente:

### Source Serif 4

- regular;
- semibold.

### Inter

- regular;
- medium;
- semibold;
- bold se necessário.

---

# 87. Tokens CSS Recomendados

Estrutura inicial:

```css
:root {
  --color-bg: #F7F5F0;
  --color-surface: #FFFFFF;

  --color-text-primary: #181A18;
  --color-text-secondary: #62665F;
  --color-border: #DDDCD6;

  --color-brazil: #1F5A46;
  --color-brazil-soft: #E7F0EB;

  --color-world: #28536B;
  --color-world-soft: #E8EFF3;

  --color-success: #2E6A4E;
  --color-warning: #9A6B20;
  --color-error: #A13C36;

  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-7: 48px;
  --space-8: 64px;
  --space-9: 96px;
  --space-10: 128px;

  --motion-fast: 120ms;
  --motion-normal: 220ms;
  --motion-slow: 400ms;
}
```

Esses valores são o ponto de partida.

Não devem ser replicados manualmente em dezenas de componentes.

---

# 88. Componentes Mínimos Da V1

O sistema deve possuir componentes reutilizáveis para:

- `Button`;
- `InputCurrency`;
- `HouseholdSizeInput`;
- `ResultCard`;
- `PercentileBar`;
- `SourceMeta`;
- `ShareActions`;
- `InfoDisclosure`;
- `ErrorMessage`;
- `Section`;
- `Container`.

Não criar abstrações prematuras para componentes utilizados uma única vez.

---

# 89. ResultCard

Propriedades conceituais:

```text
context
percentile
topPercent
description
source
accent
```

`accent` deve receber tokens semânticos:

```text
brazil
world
```

Não hardcode de hex dentro do componente.

---

# 90. PercentileBar

Deve receber:

```text
value
label
accent
```

e produzir:

- representação visual;
- representação textual acessível.

Não depender do gráfico para comunicar o resultado.

---

# 91. Estados Vazios

Não preencher cards com números fictícios antes do cálculo.

Antes do resultado:

> formulário.

Depois:

> resultado real.

Evitar placeholder como:

```text
TOP 10%
```

que possa ser confundido com resultado.

---

# 92. Skeleton

Usar somente se houver carregamento perceptível.

Não usar skeleton por padrão apenas porque é tendência de interface.

---

# 93. Design E Metodologia

O design não pode modificar o significado estatístico.

Exemplo:

Se a metodologia determinar:

> aproximadamente Top 32%,

a interface não pode arredondar para:

> Top 30%

apenas porque “fica mais bonito”.

---

# 94. Design E Privacidade

A interface deve deixar evidente antes de compartilhar:

> **Sua renda não será mostrada.**

Privacidade deve ser percebida na experiência, não escondida apenas na política jurídica.

---

# 95. Testes Visuais Obrigatórios

Antes da V1:

- 320px;
- 360px;
- 390px;
- 430px;
- tablet;
- notebook;
- desktop largo;
- zoom 200%;
- texto ampliado;
- teclado;
- prefers-reduced-motion;
- modo de alto contraste quando pertinente.

---

# 96. Conteúdo Extremo

Testar:

### Renda

```text
R$ 0
R$ 1.000
R$ 10.000
R$ 1.000.000
```

### Percentis

```text
0,1%
50%
99%
99,9%
```

A interface não pode quebrar com valores longos.

---

# 97. Textos Longos

Considerar que:

- metodologia;
- fontes;
- mensagens de erro;

podem crescer.

Não construir cards com altura rigidamente fixa.

---

# 98. Internacionalização Futura

A V1 é:

```text
pt-BR
```

Mas componentes não devem depender de textos embutidos na lógica quando separação simples for possível.

Moeda inicial:

```text
BRL
```

---

# 99. Critérios De Aceite Visual

A V1 estará visualmente adequada quando:

- a pergunta principal for compreendida imediatamente;
- o formulário parecer simples;
- o resultado for o elemento dominante;
- Brasil e Mundo forem distinguíveis;
- percentil e TOP forem compreensíveis;
- o compartilhamento estiver evidente;
- privacidade estiver perceptível;
- a página funcionar muito bem em celular;
- textos forem confortáveis para leitura;
- gráficos tiverem função informativa;
- a interface não parecer uma fintech;
- a interface não parecer um portal genérico de calculadoras;
- animações forem discretas;
- contraste e navegação por teclado estiverem adequados.

---

# 100. O Que Nunca Fazer

Evitar:

- gradientes chamativos;
- glassmorphism;
- neon;
- sombras pesadas;
- excesso de cards;
- excesso de pills;
- fotos genéricas de família;
- fotos de pessoas com dinheiro;
- cofrinhos;
- cifrões decorativos;
- moedas voando;
- foguetes;
- gráficos decorativos;
- confete;
- medalhas;
- troféus;
- rankings competitivos;
- gamificação excessiva;
- aparência de cassino;
- vermelho para renda baixa;
- verde para renda alta;
- dark patterns;
- pop-ups antes do resultado;
- captura de e-mail antes do cálculo;
- publicidade interrompendo a experiência principal.

---

# 101. Regra Para O Codex

Ao implementar uma tela:

1. preservar hierarquia;
2. utilizar tokens;
3. reutilizar componentes existentes;
4. verificar mobile primeiro;
5. verificar acessibilidade;
6. verificar estados extremos;
7. evitar dependências visuais desnecessárias.

Se uma decisão visual não estiver especificada:

> escolher a solução mais simples, clara e consistente com este documento.

Não introduzir nova linguagem visual sem necessidade.

---

# 102. Norte Visual

O usuário deve sentir:

> **“Isso parece sério.”**

Depois:

> **“Isso é muito simples de usar.”**

Depois:

> **“Entendi imediatamente meu resultado.”**

E finalmente:

> **“Eu compartilharia isso.”**

O design não deve chamar mais atenção que a informação.

> **A estética existe para tornar o dado compreensível, confiável e memorável.**