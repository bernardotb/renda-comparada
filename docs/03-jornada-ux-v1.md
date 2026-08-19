---
title: 03-jornada-ux-v1
created: 2026-08-12T17:09:52.000-03:00
modified: 2026-08-14T16:31:00.000-03:00
---

# 03-jornada-ux-v1

**Produto:** Renda Comparada  
**Versão:** V1  
**Status:** Canônico para a jornada da V1; Brasil e Mundo integrados com estados assíncronos independentes
**Versão do documento:** 1.1
**Última revisão:** 14/08/2026
**Visão:** `01-visao-produto.md`  
**PRD:** `02-prd-v1.md`  
**Metodologia:** `04-metodologia-dados.md`  
**Design:** `05-design-system.md`

---

# 1. Objetivo Deste Documento

Este documento define **como o usuário percorre a V1 do produto**, desde a entrada na página até o resultado, compartilhamento e eventual continuação opcional.

Ele não define:

- fórmulas estatísticas;
- datasets;
- regras de cálculo;
- identidade visual detalhada;
- regras completas de privacidade;
- funcionalidades futuras.

Esses assuntos pertencem aos documentos específicos do projeto.

O objetivo aqui é garantir que a experiência preserve:

- simplicidade;
- curiosidade;
- clareza;
- confiança;
- baixo atrito;
- compartilhamento;
- progressão opcional.

---

# 2. Princípio Central Da Jornada

A experiência principal deve seguir esta lógica:

**Perguntar pouco**

↓

**entregar rapidamente**

↓

**explicar com clareza**

↓

**permitir compartilhar**

↓

**só então oferecer aprofundamento**

A V1 não deve transformar uma curiosidade simples em um questionário financeiro antes que o usuário receba aquilo que veio buscar.

---

# 3. Jornada Principal

Fluxo canônico:

```text
ENTRA NO SITE
      ↓
ENTENDE A PERGUNTA
      ↓
INFORMA RENDA
      ↓
INFORMA MORADORES
      ↓
CALCULA
      ↓
RESULTADO BRASIL + MUNDO
      ↓
INTERPRETAÇÃO
      ↓
COMPARTILHAMENTO
      ↓
────────────────────────────
EXPERIÊNCIA PRINCIPAL COMPLETA
────────────────────────────
      ↓
CONVITE OPCIONAL
      ↓
“Quer entender melhor sua vida financeira?”
      ↓
CONTINUA OU ENCERRA
```

A ordem acima é obrigatória na V1.

---

# 4. O Que Não Pode Acontecer Antes Do Resultado

Antes do resultado principal, não pedir:

- nome;
- e-mail;
- telefone;
- CPF;
- cidade;
- profissão;
- patrimônio;
- dívidas;
- gastos;
- reserva;
- investimentos;
- objetivo financeiro;
- cadastro;
- login.

A experiência inicial deve depender somente das informações estritamente necessárias ao cálculo.

---

# 5. Etapa 1 — Entrada Na Página

## Objetivo Do Usuário

Entender imediatamente:

> “O que esse site faz?”

A primeira dobra deve responder isso em poucos segundos.

---

# 6. Conteúdo Da Primeira Dobra

Estrutura conceitual:

### Identidade

**RENDA COMPARADA**

### Pergunta Principal

# Você É Mais Rico Do Que Quantos Brasileiros?

### Subtítulo

> **Descubra onde a renda da sua família está no Brasil — e onde ela estaria no mundo.**

### Explicação Discreta

> **A comparação é baseada em renda, não em patrimônio.**

A explicação não deve competir visualmente com a pergunta principal.

---

# 7. Prioridade Visual Da Primeira Dobra

A hierarquia deve ser:

1. pergunta principal;
2. breve explicação;
3. campos;
4. botão de cálculo;
5. metodologia/privacidade como apoio.

Evitar colocar antes do formulário:

- grandes blocos de metodologia;
- gráficos complexos;
- estatísticas;
- matérias;
- artigos;
- cursos;
- simuladores;
- ferramentas do Banco Central.

O usuário deve chegar ao cálculo sem distrações.

---

# 8. Etapa 2 — Renda Familiar

Pergunta:

> **Qual é a renda mensal total da sua casa?**

Campo:

`R$ _________`

Texto de apoio:

> **Use a renda bruta mensal, antes de impostos e despesas.**

A entrada representa a renda mensal nominal vigente no momento do cálculo. O alinhamento para a referência monetária da PNAD 2025 é feito automaticamente conforme D065.

Não tentar explicar toda a metodologia neste momento.

Pode existir link discreto:

> **O que devo incluir?**

---

# 9. Comportamento Do Campo De Renda

O campo deve:

- aceitar entrada numérica;
- formatar em reais;
- funcionar bem em celular;
- abrir teclado numérico quando possível;
- tolerar colagem de valores;
- tratar vírgula e ponto;
- impedir valores negativos;
- preservar o valor caso ocorra erro posterior.

Exemplo:

Usuário digita:

`6500`

Interface apresenta:

`R$ 6.500`

ou outra formatação definida pelo design system.

---

# 10. Ajuda Contextual Sobre Renda

Caso o usuário toque em:

> **O que devo incluir?**

abrir uma explicação curta.

Texto recomendado:

> **Some os rendimentos mensais da casa antes de impostos e despesas, como salários e trabalho por conta própria, aposentadorias, pensões, aluguéis recebidos e outras rendas abrangidas pela metodologia. Não desconte aluguel, financiamento, cartão, plano de saúde ou gastos do mês.**

A definição completa e as limitações ficam em “Como calculamos”.

Não colocar explicação estatística extensa dentro do fluxo principal.

---

# 11. Etapa 3 — Moradores

Pergunta:

> **Quantas pessoas fazem parte deste domicílio?**

Texto de apoio:

> **Inclua adultos e crianças, mesmo que não tenham renda.**

Ajuda contextual deve informar que, para compatibilidade com o indicador do IBGE, existem exclusões técnicas para empregado doméstico residente, parente de empregado doméstico e “pensionista” na classificação da condição no domicílio. A palavra “pensionista” deve ser apresentada como categoria técnica do IBGE, sem ser confundida automaticamente com beneficiário de pensão.

Controle pode ser:

`− 3 +`

ou campo numérico, conforme testes de UX.

---

# 12. Comportamento Do Campo De Moradores

O campo deve:

- aceitar somente inteiros;
- mínimo de 1;
- não aceitar zero;
- não aceitar valores negativos;
- não aceitar frações;
- ser fácil de operar com uma mão no celular.

---

# 13. Etapa 4 — CTA Principal

Botão:

> # Descobrir minha posição

O CTA deve ser o elemento de ação mais evidente da primeira etapa.

Evitar múltiplos botões concorrentes.

Não usar CTA como:

- continuar;
- enviar;
- próximo;
- começar diagnóstico.

A intenção deve estar explícita.

---

# 14. Estado Do CTA

Antes de entradas válidas:

- pode permanecer desabilitado;
- ou aceitar clique e indicar claramente o campo pendente.

Depois de entradas válidas:

- estado ativo;
- boa área de toque;
- feedback imediato ao clique.

---

# 15. Etapa 5 — Processamento

Seguir D072 para Brasil.

No primeiro cálculo, a aplicação pode precisar carregar a CDF brasileira estática e validar os manifestos aprovados. Nesse caso, existe trabalho real e o feedback de carregamento é necessário.

Mensagem recomendada:

> **Calculando sua posição…**

Regras:

- manter o usuário na mesma página;
- preservar os campos preenchidos;
- usar feedback simples e acessível;
- não enviar renda ou moradores na requisição do dataset;
- não usar barra longa, suspense ou animação decorativa;
- depois da CDF estar em memória, novas simulações não devem criar espera artificial.

Se os artefatos já estiverem disponíveis e o cálculo for imediato:

> **não criar loading artificial.**

---

# 16. Transição Para O Resultado

Ao concluir o cálculo:

- deslocar a atenção imediatamente para o resultado;
- em celular, rolar suavemente se necessário;
- manter contexto suficiente para o usuário saber que aquele resultado deriva dos dados informados.

Evitar abrir modal que desconecte o resultado da página.

---

# 17. Etapa 6 — Resultado Principal

O resultado deve responder imediatamente:

> **Onde estou?**

A primeira leitura deve ser visual e intuitiva.

Estrutura:

## No Brasil

resultado principal

## No Mundo

resultado principal

A interpretação detalhada vem depois.

---

# 18. Resultado Brasil

Estrutura conceitual:

### 🇧🇷 Brasil

# Percentil 68

ou representação visual equivalente.

Em seguida:

> **Você está aproximadamente entre os 32% de maior renda na distribuição utilizada.**

Depois:

> Sua renda por pessoa está acima da observada para aproximadamente 68 em cada 100 pessoas na distribuição brasileira considerada.

A redação exata depende de `04-metodologia-dados.md`.

---

# 19. Percentil E TOP Percentual

Sempre que metodologicamente válido, mostrar as duas leituras:

### Estatística

**Percentil 68**

### Intuitiva

**TOP 32%**

Isso ajuda usuários que não conhecem percentis.

As duas medidas devem ser coerentes entre si.

---

# 20. Resultado Mundo

Depois do resultado brasileiro:

### 🌎 Mundo

# Percentil X

### TOP Y%

Explicação curta:

> Sua renda está aproximadamente nesta posição quando comparada à distribuição global utilizada.

A interface deve deixar claro que a comparação mundial possui metodologia e limitações diferentes.

---

# 21. Relação Visual Brasil × Mundo

Brasil e Mundo devem parecer partes da mesma experiência.

Não criar duas calculadoras separadas.

Em desktop:

- podem aparecer lado a lado.

Em celular:

- preferencialmente em sequência vertical.

A ordem padrão deve ser:

**Brasil primeiro**

↓

**Mundo depois**

porque o produto é inicialmente orientado ao usuário brasileiro.

---

# 22. Visualização Da Posição

A V1 pode usar uma visualização simples como:

```text
MENOR RENDA                           MAIOR RENDA
|──────────────────────────●──────────────|
                           você
```

ou uma distribuição equivalente.

O objetivo do gráfico é responder:

> “Onde eu estou?”

Não apresentar um gráfico apenas como decoração.

---

# 23. Animações Do Resultado

Permitidas:

- marcador deslizando até a posição;
- número aparecendo suavemente;
- transição discreta Brasil → Mundo.

Evitar:

- confete;
- explosões;
- moedas;
- fogos;
- sons;
- comportamento semelhante a jogo de azar.

A informação é econômica e deve manter sobriedade.

---

# 24. Renda Por Pessoa

Abaixo do resultado, pode aparecer:

> **Sua renda mensal atual por pessoa: R$ X**

Com explicação:

> renda mensal atual da casa ÷ número de moradores considerados.

Isso ajuda o usuário a compreender de onde veio a comparação.

Para o Brasil, a comparação estatística utiliza uma versão desse valor alinhada automaticamente a preços médios de 2025 conforme D065. O valor ajustado pertence à explicação metodológica e não deve ser apresentado como se fosse uma nova renda nominal do usuário.

Não dar mais destaque a esse número do que à posição.

---

# 25. Etapa 7 — Interpretação

Depois da leitura visual, responder:

> **O que isso significa?**

Conteúdo curto.

Exemplo conceitual:

> Isso não significa que X% das pessoas tenham exatamente a mesma renda. Significa que sua renda foi posicionada aproximadamente neste ponto da distribuição utilizada.

O objetivo é impedir interpretações erradas sem transformar a tela em uma aula de estatística.

---

# 26. Fontes Visíveis

Perto do resultado:

> **Brasil: IBGE — PNAD Contínua 2025**

> **Mundo: World Bank — PIP**

> **Dados atualizados em: XX/XX/XXXX**

Para o Brasil, a explicação de fonte deve informar que a renda corrente é alinhada a preços médios de 2025 pelo IPCA oficial e mostrar o mês de referência efetivamente usado.

E:

> **Como calculamos isso?**

Ano, versão, referência monetária e mês do índice de preços devem vir dos manifestos/datasets utilizados, nunca de texto hardcoded.

---

# 27. Etapa 8 — Compartilhamento

O compartilhamento aparece **imediatamente depois do resultado e da interpretação essencial**.

Título:

> ## Compartilhar minha posição

Texto:

> **Sua renda não será mostrada.**

Essa frase deve aparecer de forma explícita.

---

# 28. Motivo Da Posição Do Compartilhamento

O usuário acabou de obter o momento de maior interesse emocional e cognitivo da experiência.

Não inserir antes do compartilhamento:

- check-up;
- cursos;
- Registrato;
- artigos;
- newsletter;
- cadastro;
- outras calculadoras.

O fluxo é:

**resultado → compartilhar**

e não:

**resultado → formulário → compartilhar**

---

# 29. Opção De Compartilhamento Privado

Modo padrão:

> **Descobri onde minha renda está na distribuição brasileira. E você?**

O card/link não mostra:

- renda;
- renda por pessoa;
- número de moradores.

---

# 30. Opção De Compartilhar Posição

Pode existir opção secundária:

> **Compartilhar minha posição**

Exemplo:

> **Minha renda está aproximadamente entre os 12% mais altos da distribuição brasileira.**

Não mostrar o valor financeiro.

---

# 31. Canais De Compartilhamento

Prioridade:

### Mobile

- compartilhamento nativo;
- WhatsApp;
- copiar link.

### Desktop

- WhatsApp;
- copiar link;
- compartilhamento nativo quando disponível.

Não sobrecarregar a interface com dez redes sociais.

---

# 32. Feedback De Compartilhamento

Após copiar:

> **Link copiado**

Após ação de share:

- não assumir que o compartilhamento foi concluído se a API não confirmar isso;
- registrar somente eventos tecnicamente válidos.

---

# 33. Card Social

Estrutura conceitual:

**RENDA COMPARADA**

# TOP X%

> Minha posição na distribuição de renda brasileira.

> **E você?**

O card deve ser compreensível sem contexto adicional.

---

# 34. Experiência Principal Termina Aqui

Depois de:

- cálculo;
- resultado;
- interpretação;
- compartilhamento;

a experiência principal está completa.

O usuário já recebeu integralmente o valor prometido na entrada.

Qualquer etapa posterior é complementar.

---

# 35. Etapa 9 — Ponte Opcional

Depois do bloco de compartilhamento, introduzir:

> ## Sua posição de renda conta apenas uma parte da história.

Texto:

> Estar acima de grande parte da população não significa necessariamente ter uma vida financeira saudável.

Depois:

> # Quer entender melhor sua vida financeira?

CTA:

> **Quero continuar**

ou:

> **Fazer meu check-up financeiro**

A escolha final do CTA depende do estágio de implementação.

---

# 36. A Ponte Não Deve Invalidar O Resultado

Evitar mensagens como:

> “Seu resultado é bom, mas…”

> “Parabéns, porém…”

> “Apesar de estar no Top X%…”

O site não deve julgar se o percentil é bom ou ruim.

A mensagem deve apenas explicar:

> **posição de renda ≠ saúde financeira.**

---

# 37. Usuário Que Não Quer Continuar

Deve conseguir simplesmente:

- encerrar a navegação;
- compartilhar;
- simular outra renda;
- abrir metodologia;
- voltar posteriormente.

Não usar técnicas de retenção agressiva.

---

# 38. Simular Novamente

Perto do resultado:

> **Simular outra renda**

Ao tocar:

- retornar aos campos;
- preservar os valores anteriores;
- permitir alteração;
- recalcular sem reload completo quando possível.

O usuário pode explorar livremente diferentes cenários.

---

# 39. Navegação Principal Da V1

A navegação deve ser mínima.

Itens possíveis:

- Calculadora;
- Como funciona;
- Metodologia;
- Sobre.

Evitar colocar na V1 uma mega navegação com dezenas de categorias futuras.

---

# 40. Conteúdo Abaixo Da Experiência

Depois da jornada principal, a página pode conter:

## Como Funciona

## O Que É Renda Por Pessoa

## O Que É Percentil

## Brasil × Mundo

## Renda × Patrimônio

## Fontes Dos Dados

## Perguntas Frequentes

Esses conteúdos não devem interromper o caminho até o resultado.

---

# 41. Estado Inicial

Características:

- nenhum resultado;
- formulário visível;
- CTA claro;
- explicações mínimas;
- nada de dados fictícios apresentados como resultado real.

Pode haver exemplo didático claramente identificado como exemplo.

---

# 42. Estado Preenchendo

Enquanto o usuário digita:

- formatação deve acontecer sem atrapalhar;
- erros devem aparecer no momento adequado;
- não apagar campos;
- evitar alertas invasivos.

---

# 43. Estado Inválido — Renda

Exemplos:

### Campo Vazio

> **Informe a renda mensal da casa.**

### Valor Inválido

> **Digite um valor válido.**

### Valor Negativo

> **A renda não pode ser negativa.**

A redação deve ser simples.

---

# 44. Estado Inválido — Moradores

Exemplos:

### Campo Vazio

> **Informe quantas pessoas moram na casa.**

### Zero

> **Informe pelo menos 1 morador.**

### Fração

> **Use um número inteiro de pessoas.**

---

# 45. Renda Zero

O tratamento depende da metodologia.

Se permitido:

- calcular conforme regras definidas.

Se não permitido:

- informar de forma clara.

Não assumir comportamento estatístico sem consultar `04-metodologia-dados.md`.

---

# 46. Rendas Muito Altas

Se o RDPC comparável ultrapassar o maior valor observado da CDF brasileira, seguir D071:

- não extrapolar silenciosamente;
- não mostrar `TOP 0%`;
- informar que o valor está acima do maior RDPC observado na distribuição utilizada;
- esclarecer que a pesquisa não permite estimar posição mais fina nessa cauda.

Mensagem conceitual:

> **Sua renda por pessoa está acima do maior valor observado na distribuição utilizada. A pesquisa não permite estimar com segurança uma posição mais fina nessa cauda.**

---

# 47. Erro De Dados

Se o dataset não carregar ou estiver inconsistente:

Não mostrar percentil inventado.

Mensagem:

> **Não conseguimos calcular sua posição agora. Tente novamente em instantes.**

Se útil:

> **Seus dados preenchidos foram mantidos.**

---

# 48. Estado Offline

Quando possível, oferecer mensagem clara:

> **Parece que você está sem conexão.**

Não usar erros técnicos como:

`Failed to fetch`

ou:

`500 Internal Server Error`

na interface para usuário comum.

---

# 49. Mobile First

A jornada deve ser desenhada primeiro para celular.

Prioridades:

- formulário em uma coluna;
- campos grandes;
- teclado numérico;
- botão em largura adequada;
- resultado sem necessidade de zoom;
- compartilhamento fácil;
- boa leitura com uma mão;
- nenhuma tabela larga obrigatória.

---

# 50. Hipótese De Uso Principal

Uma jornada importante é:

```text
RECEBE LINK NO WHATSAPP
        ↓
ABRE NO CELULAR
        ↓
CALCULA
        ↓
SE SURPREENDE
        ↓
COMPARTILHA NO WHATSAPP
        ↓
OUTRA PESSOA ABRE
```

A V1 deve funcionar especialmente bem neste fluxo.

---

# 51. Desktop

No desktop, pode haver:

- maior largura de conteúdo;
- cards Brasil × Mundo lado a lado;
- visualização mais ampla.

Mas a hierarquia de jornada não muda.

---

# 52. Acessibilidade

A experiência deve:

- permitir navegação por teclado;
- usar labels reais;
- indicar erros por texto;
- não depender exclusivamente de cor;
- manter contraste adequado;
- permitir leitores de tela;
- ter foco visível;
- possuir áreas de toque adequadas.

Percentis e gráficos devem ter representação textual equivalente.

---

# 53. Linguagem

Usar português brasileiro simples.

Preferir:

> **Sua renda por pessoa**

em contexto introdutório.

Explicar depois:

> **renda domiciliar per capita**

quando necessário.

Não iniciar a experiência exigindo vocabulário estatístico.

---

# 54. Tom

O produto deve soar:

- claro;
- confiável;
- curioso;
- respeitoso;
- sóbrio.

Evitar:

- paternalismo;
- julgamento;
- ostentação;
- sensacionalismo;
- vergonha financeira.

---

# 55. Não Celebrar Renda Alta

Evitar mensagens como:

> “Parabéns! Você é rico!”

> “Você venceu!”

> “Incrível!”

O resultado deve ser informativo.

A surpresa vem do dado.

---

# 56. Não Dramatizar Renda Baixa

Evitar:

> “Sua situação é preocupante.”

> “Você está entre os mais pobres.”

> “Isso é ruim.”

A calculadora mede posição relativa, não valor pessoal nem saúde financeira.

---

# 57. Resposta Emocional Neutra

Se o usuário estiver em percentil baixo:

> **Sua renda está aproximadamente nesta posição da distribuição.**

Se estiver alto:

> **Sua renda está aproximadamente nesta posição da distribuição.**

A estrutura deve permanecer consistente.

---

# 58. Conteúdo Progressivo

Regra:

> **Mostrar primeiro o que o usuário precisa saber agora.**

Detalhes metodológicos ficam disponíveis sob demanda.

Exemplo:

### Resultado

TOP 20%

### Explicação Curta

Sua renda está acima de aproximadamente 80% da distribuição.

### Quer Entender O Cálculo?

Como calculamos →

---

# 59. Analytics Na Jornada

Eventos possíveis:

### Entrada

`calculator_view`

### Primeira Interação

`calculation_started`

### Resultado

`calculation_completed`

`result_viewed`

### Explicação

`methodology_opened`

### Compartilhamento

`share_clicked`

`share_native`

`share_whatsapp`

`copy_link`

### Nova Simulação

`recalculate_clicked`

### Continuação

`financial_checkup_interest`

Eventos não devem conter dados financeiros informados pelo usuário.

---

# 60. Pontos De Abandono Que Devem Ser Monitorados

Medir:

### Antes De Digitar

Usuário vê a página mas não inicia.

### Entre Renda E Moradores

Usuário abandona formulário.

### Após Cálculo

Erro impede resultado.

### Após Resultado

Usuário não interage com nada.

### Compartilhamento

Usuário vê CTA mas não compartilha.

### Continuação

Usuário ignora o check-up.

Esses dados devem informar futuras melhorias de UX.

---

# 61. Critério De Sucesso Da Jornada Inicial

Um novo usuário deve conseguir compreender a tarefa sem tutorial.

Idealmente:

1. entende a pergunta;
2. sabe o que preencher;
3. preenche;
4. calcula;
5. entende o resultado;
6. consegue compartilhar.

Sem precisar abrir FAQ.

---

# 62. Critério De Clareza Do Resultado

Após ver o resultado, o usuário deve conseguir responder:

> **Estou acima de aproximadamente quantas pessoas?**

e:

> **Estou aproximadamente entre os X% de maior renda?**

Se isso não estiver claro, a interface falhou mesmo que o cálculo esteja correto.

---

# 63. Critério De Confiança

O usuário deve conseguir encontrar facilmente:

- quem fornece os dados;
- de qual ano são;
- como o cálculo funciona;
- quais são as limitações.

Mas essas informações não devem dominar a primeira tela.

---

# 64. Critério De Privacidade Percebida

Antes de compartilhar, deve estar claro:

> **Sua renda não será mostrada.**

O usuário não deve precisar ler a política de privacidade para descobrir isso.

---

# 65. Critério De Compartilhamento

O usuário deve conseguir compartilhar com:

- no máximo poucos toques;
- sem editar manualmente o link;
- sem revelar renda;
- com mensagem compreensível para quem recebe.

---

# 66. Critério De Continuidade

A jornada para saúde financeira deve parecer:

> **uma opção natural de aprofundamento**

e não:

> **uma obrigação escondida atrás da calculadora.**

---

# 67. Experiência Futura — Não Implementar Automaticamente

A seguinte jornada pertence a versões posteriores:

```text
RESULTADO DE RENDA
      ↓
CHECK-UP
      ↓
DÍVIDAS
      ↓
RESERVA
      ↓
ORÇAMENTO
      ↓
CAPACIDADE DE POUPANÇA
      ↓
PRIORIDADES
      ↓
FERRAMENTAS OFICIAIS
      ↓
CURSOS
      ↓
SIMULADORES
```

Na V1, apenas a ponte pode existir.

---

# 68. O Que Não Deve Entrar Na Jornada Principal Da V1

Não colocar entre entrada e compartilhamento:

- cursos;
- Registrato;
- Valores a Receber;
- carro;
- imóvel;
- energia;
- cartão;
- cheque especial;
- investimentos;
- notícias;
- artigos extensos;
- simuladores paralelos;
- publicidade invasiva.

Esses itens pertencem a experiências posteriores ou conteúdos secundários.

---

# 69. Princípio De Uma Pergunta Por Vez

Sempre que possível, a interface deve reduzir carga cognitiva.

Mesmo que renda e moradores apareçam na mesma área, cada pergunta deve ser visualmente inequívoca.

Evitar formulários densos.

---

# 70. Princípio De Uma Ação Principal Por Etapa

Na entrada:

> **Descobrir minha posição**

No resultado:

> **Compartilhar minha posição**

Depois:

> **Quero entender melhor minha vida financeira**

Cada momento possui uma ação dominante diferente.

---

# 71. Princípio De Não Esconder Contexto

O site não deve revelar simplesmente:

> **68%**

sem explicar o que significa.

Todo resultado numérico relevante deve possuir interpretação textual.

---

# 72. Princípio De Não Exagerar Precisão

Se o resultado for uma estimativa:

mostrar:

> **aproximadamente**

quando necessário.

Não usar casas decimais apenas porque o algoritmo consegue calculá-las.

A quantidade de precisão visual deve refletir a precisão real da metodologia.

---

# 73. Decisão — Precisão Visual Do Resultado Brasil

A precisão visual brasileira é regida por **D071**.

Na faixa comum, `TOP` e percentil são exibidos como inteiros complementares. Na cauda entre `0,1%` e `1%`, pode-se usar uma casa decimal; abaixo de `0,1%`, usar linguagem de limite (`TOP < 0,1%`) em vez de falsa precisão.

Não exibir mais casas apenas porque o cálculo interno as possui. O Mundo permanece subordinado a D070.

---

# 74. Decisão — Posição Visual Da Renda per Capita

A renda por pessoa deve aparecer **dentro do resultado como informação secundária**.

Mostrar o valor nominal atual derivado da entrada:

> **Sua renda mensal atual por pessoa: R$ X**

O valor alinhado a preços médios de 2025 pode aparecer em “Como calculamos”, para auditabilidade, sem competir com a posição principal.

Não mostrar a renda por pessoa antes do cálculo.

---

# 75. Regra Responsiva — Brasil E Mundo

No mobile, a sequência é obrigatoriamente vertical, com **Brasil antes de Mundo**.

No desktop, os cards podem ficar lado a lado quando houver largura suficiente, desde que Brasil permaneça primeiro na ordem semântica e a composição não sugira equivalência de precisão entre as duas metodologias.

A implementação visual final deve ser validada no protótipo/responsividade; essa validação não reabre a ordem conceitual da jornada.

---

# 76. Decisão — CTA Pós-resultado

Conforme D019, a transição deve ser formulada como pergunta de compreensão, não como avaliação emocional do percentil:

> **Quer entender melhor sua vida financeira?**

CTA:

> **Quero entender melhor**

O check-up completo continua fora do escopo obrigatório da V1.

---

# 77. Decisão — Modo De Compartilhar

Conforme D017, o modo padrão deve ser **genérico e sem posição**.

A interface pode usar um único botão:

> **Compartilhar**

Ao abrir a ação, a inclusão da posição deve exigir escolha explícita, inicialmente desativada:

> **Incluir minha posição — sem mostrar minha renda**

Em ambos os modos é proibido compartilhar automaticamente:

- renda;
- moradores;
- renda por pessoa.

A URL compartilhada não deve codificar o resultado individual.

---

# 78. Fluxo Resumido Para Implementação

```text
[HOME]
  |
  |-- headline
  |-- renda
  |-- moradores
  |-- CTA
  |
  v
[VALIDAÇÃO]
  |
  v
[CÁLCULO]
  |
  v
[RESULTADO]
  |
  |-- Brasil
  |-- Mundo
  |-- interpretação
  |-- fontes
  |
  v
[COMPARTILHAR]
  |
  |-- native share
  |-- WhatsApp
  |-- copiar
  |
  v
[FIM DA EXPERIÊNCIA PRINCIPAL]
  |
  v
[CONTINUAR?]
  |
  |-- não → encerra/explora conteúdo
  |
  |-- sim → futura experiência financeira
```

---

# 79. Definition of Done Da Jornada UX

A jornada V1 estará adequada quando um usuário novo conseguir:

- entender o propósito sem explicação externa;
- preencher renda corretamente;
- entender que crianças entram nos moradores;
- calcular sem cadastro;
- visualizar Brasil e Mundo;
- entender percentil e TOP percentual;
- identificar a fonte dos dados;
- compartilhar sem revelar renda;
- recalcular facilmente;
- perceber que o check-up é opcional;
- usar a experiência completa no celular;
- navegar sem obstáculos artificiais.

---

# 80. Norte Da Jornada

A experiência deve preservar esta sensação:

> **“Entendi a pergunta em segundos.”**

↓

> **“Foi fácil calcular.”**

↓

> **“Agora entendi onde estou.”**

↓

> **“Quero mostrar isso para alguém.”**

E somente depois:

> **“Talvez eu queira entender melhor minha vida financeira.”**

Se alguma decisão de UX prejudicar essa sequência, ela deve ser questionada.
