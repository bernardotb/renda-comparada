---
title: 06-privacidade-seguranca
created: 2026-08-12T17:28:31.000-03:00
modified: 2026-08-14T16:31:00.000-03:00
---

# 06-privacidade-seguranca

# Privacidade E Segurança — Renda Comparada

**Produto:** Renda Comparada  
**Documento:** `06-privacidade-seguranca.md`  
**Status:** Canônico para privacidade e segurança  
**Versão:** 1.1
**Última revisão:** 14/08/2026

Documentos relacionados:

- `01-visao-produto.md`
- `02-prd-v1.md`
- `03-jornada-ux-v1.md`
- `04-metodologia-dados.md`
- `05-design-system.md`
- `07-seo-analytics-crescimento.md`
- `09-fontes-referencias.md`
- `10-testes-validacao.md`

---

# 1. Função Deste Documento

Este documento define os princípios e requisitos internos para:

- privacidade;
- proteção de dados;
- segurança da aplicação;
- analytics;
- logs;
- compartilhamento;
- integrações;
- serviços de terceiros;
- retenção;
- incidentes de segurança;
- desenvolvimento seguro.

Ele não substitui:

- Política de Privacidade pública;
- Política de Cookies;
- termos jurídicos;
- análise jurídica especializada.

Antes do lançamento público definitivo, os documentos jurídicos externos deverão ser revisados de acordo com:

- operação real do produto;
- controlador efetivo;
- fornecedores efetivamente contratados;
- tecnologias efetivamente utilizadas.

---

# 2. Princípio Central

O princípio de privacidade do Renda Comparada é:

> # Se não precisamos guardar, não guardamos.

A V1 deve operar segundo:

**coleta mínima**

↓

**processamento mínimo**

↓

**retenção mínima**

↓

**compartilhamento mínimo**

↓

**transparência**

---

# 3. Privacy by Design

Privacidade e segurança devem ser consideradas durante a concepção da funcionalidade, e não adicionadas apenas depois da implementação.

A LGPD determina a adoção de medidas técnicas e administrativas aptas a proteger dados pessoais contra acessos não autorizados, perda, alteração, comunicação ou tratamento inadequado, e determina que essas medidas sejam consideradas desde a fase de concepção do produto ou serviço.

Portanto:

> funcionalidades novas devem ser avaliadas quanto à privacidade antes de serem implementadas.

---

# 4. Regra De Minimização

Toda coleta deve responder:

> **Por que precisamos desse dado?**

Se não existir finalidade clara e necessária:

> **não coletar.**

Antes de adicionar qualquer novo campo:

1. identificar finalidade;
2. verificar necessidade;
3. verificar se existe alternativa menos invasiva;
4. definir retenção;
5. definir quem terá acesso;
6. registrar no inventário de tratamentos.

---

# 5. Dados Da Calculadora V1

A calculadora principal utiliza:

### Renda Mensal Da Casa

Exemplo:

`R$ 6.500`

### Número De Moradores

Exemplo:

`3`

A aplicação calcula temporariamente:

### Renda Por Pessoa

Exemplo:

`R$ 2.166,67`

### Posição Brasil

Resultado individual derivado da distribuição brasileira.

### Posição Mundo

Resultado individual estimado derivado da metodologia mundial vigente, quando esta estiver aprovada.

Esses valores devem ser tratados como **informações financeiras confidenciais do usuário**, ainda que nem todos constituam, isoladamente, dado pessoal identificável.

---

# 6. Renda Não Deve Ser Tratada Como Dado Público

Nunca assumir que o usuário considera sua renda uma informação pública.

A experiência deve partir da hipótese:

> **o usuário deseja preservar o valor exato da sua renda.**

Isso deve orientar:

- compartilhamento;
- analytics;
- logs;
- cache;
- URLs;
- suporte;
- telemetria.

---

# 7. Processamento Preferencial

Quando tecnicamente adequado, o cálculo individual deve ocorrer:

> **no dispositivo/navegador do usuário**

utilizando os datasets preparados pelo projeto.

Fluxo preferencial:

```text
usuário informa renda
↓
browser calcula
↓
resultado exibido
↓
valor descartado quando deixa de ser necessário
```

Isso reduz a necessidade de transmitir informações financeiras para servidores.

---

# 8. Processamento no Servidor

Se alguma funcionalidade exigir cálculo no servidor:

- utilizar conexão criptografada;
- não persistir os inputs por padrão;
- não incluir os inputs em logs;
- não incluir os inputs em traces;
- não incluir os inputs em mensagens de erro;
- não reutilizar os inputs para outras finalidades;
- descartar os valores assim que o processamento terminar.

Qualquer mudança dessa política exige revisão deste documento.

---

# 9. Persistência Padrão

Na V1:

> **a renda não deve ser persistida por padrão.**

Não salvar automaticamente em:

- banco de dados;
- arquivo;
- backend;
- histórico de usuário;
- CRM;
- analytics;
- data warehouse.

---

# 10. LocalStorage

Não armazenar renda em:

```text
localStorage
```

por padrão.

Isso poderia deixar informações financeiras persistidas no navegador após o encerramento da sessão.

---

# 11. SessionStorage

Também evitar:

```text
sessionStorage
```

para renda, salvo necessidade técnica claramente documentada.

Se a interface puder manter o valor somente em memória:

> preferir memória.

---

# 12. Estado Da Aplicação

Durante a interação, os valores podem existir temporariamente no estado da aplicação.

Exemplo:

```text
React state
```

ou estrutura equivalente.

Ao recarregar ou encerrar a experiência, não há obrigação de preservar o valor.

---


# 12A. Cache De Datasets Públicos

As proibições de `localStorage` e `sessionStorage` acima se referem a **dados financeiros do usuário**.

Elas não impedem cache HTTP normal de artefatos estatísticos públicos e idênticos para todos, como:

```text
brazil-income-cdf-2025.json
```

ou manifestos públicos do motor.

Seguir D072:

- a CDF pode ser mantida em memória após o primeiro cálculo;
- o navegador/CDN pode usar cache HTTP de conteúdo estático;
- a requisição do dataset nunca deve carregar renda, moradores, percentil ou resultado em URL, query string, header customizado ou body;
- o cache do dataset não deve ser confundido com persistência do cálculo individual.

Manifestos que mudam após atualização aprovada, como o alinhamento mensal de preços, devem ser revalidados conforme sua política de atualização e não tratados como imutáveis sem versionamento adequado.

---

# 13. URLs

É proibido colocar renda em:

```text
?renda=6500
```

ou:

```text
/resultado/6500/3
```

Também não incluir em:

- hash da URL;
- pathname;
- canonical;
- referrer;
- Open Graph;
- metadata;
- parâmetros UTM.

---

# 14. Número De Moradores

O número de moradores também não precisa constar na URL.

Embora menos sensível isoladamente, combinado com outras informações pode aumentar a capacidade de inferência sobre o usuário.

Princípio:

> **não transmitir aquilo que não é necessário transmitir.**

---

# 15. Renda per Capita

Não inserir renda per capita em:

- URL;
- analytics;
- logs;
- pixels;
- ferramentas de marketing.

Ela é derivada diretamente da renda familiar informada.

---

# 16. Percentil

Na V1, evitar enviar o percentil individual exato para ferramentas de analytics de terceiros.

O analytics precisa saber:

> **que houve um cálculo**

e não necessariamente:

> **qual foi o resultado financeiro daquela pessoa.**

---

# 17. Analytics Permitido

Eventos permitidos incluem:

```text
calculator_view
calculation_started
calculation_completed
result_viewed
share_clicked
share_whatsapp
share_native
copy_link
methodology_opened
recalculate_clicked
financial_checkup_interest
```

Parâmetros categóricos estritamente necessários podem incluir:

```text
share_channel
share_mode
app_version
```

onde `share_mode` admite apenas categorias como `generic` ou `position`, sem carregar o valor da posição.

---

# 18. Analytics Proibido

Não enviar como parâmetros:

```text
income = 6500
household_size = 3
per_capita_income = 2166
percentile_brazil = 67.9
percentile_world = 76.6
```

Também evitar transformar esses valores em:

- nomes de eventos;
- IDs;
- labels;
- dimensões customizadas.

---

# 19. Dados Agregados

Se futuramente houver necessidade de estudar distribuição de resultados dos usuários, isso deverá passar por análise específica.

Não criar automaticamente algo como:

> “quantos usuários ganham de R$ 10 mil a R$ 20 mil”

apenas porque seria interessante para produto ou marketing.

Antes disso será necessário avaliar:

- necessidade;
- finalidade;
- base legal aplicável;
- anonimização;
- risco de reidentificação;
- transparência;
- retenção.

---

# 20. Logs De Aplicação

Logs não devem conter:

- renda;
- renda per capita;
- número de moradores;
- respostas financeiras do check-up;
- conteúdos digitados em formulários financeiros.

---

# 21. Logs Permitidos

Exemplos:

```text
request_id
timestamp
endpoint
status_code
duration
application_version
dataset_version
```

Sempre que possível, minimizar também:

- IP;
- user-agent completo;
- identificadores persistentes.

---

# 22. IP

Endereço IP pode constituir dado pessoal em determinados contextos.

Não armazenar além do necessário para:

- segurança;
- prevenção de abuso;
- funcionamento técnico.

Se a infraestrutura de terceiros registrar IP automaticamente, isso deve ser:

- identificado;
- documentado;
- considerado na Política de Privacidade.

---

# 23. Error Tracking

Se forem utilizados serviços como:

- Sentry;
- Datadog;
- LogRocket;
- Bugsnag;
- ferramentas equivalentes;

configurar sanitização antes do envio.

Nunca capturar automaticamente:

- conteúdo de campos financeiros;
- estado completo da aplicação;
- query strings contendo dados;
- DOM contendo renda;
- screenshots contendo informações financeiras.

---

# 24. Session Replay

Na V1, preferencialmente:

> **não utilizar gravação de sessão.**

Se futuramente adotada:

- mascarar campos;
- excluir telas financeiras;
- revisar necessidade;
- atualizar política de privacidade.

---

# 25. Console

Não deixar em produção:

```javascript
console.log(income)
console.log(result)
console.log(userFinancialData)
```

Dados financeiros não devem aparecer em logs do navegador por conveniência de debugging.

---

# 26. Compartilhamento Padrão

O compartilhamento padrão deve preservar privacidade.

Mensagem possível:

> **Descobri onde minha renda está na distribuição brasileira. E você?**

Não incluir:

- renda;
- moradores;
- renda per capita.

---

# 27. Compartilhamento Da Posição

O usuário poderá optar conscientemente por compartilhar algo como:

> **Minha renda está aproximadamente entre os 12% mais altos da distribuição brasileira.**

Nesse caso:

> o usuário realizou uma ação explícita para divulgar a posição.

Mesmo assim:

- não divulgar renda;
- não divulgar moradores;
- não divulgar outras informações financeiras.

---

# 28. Card Social Padrão

O Open Graph padrão deve ser genérico.

Exemplo:

```text
RENDA COMPARADA

Você é mais rico do que
quantos brasileiros?

Descubra sua posição.
```

Não gerar automaticamente Open Graph individual contendo renda.

---

# 29. Card Personalizado

Se futuramente quisermos gerar uma imagem personalizada com:

> **TOP 12%**

preferir geração local no dispositivo quando tecnicamente viável.

Isso evita enviar o resultado financeiro individual ao servidor apenas para produzir uma imagem.

---

# 30. Links Compartilhados

O link compartilhado deve preferencialmente apontar para:

```text
/
```

ou URL pública da calculadora.

Não criar URLs personalizadas contendo o resultado do usuário.

---

# 31. Web Share API

O uso da Web Share API deve enviar somente:

- título;
- texto;
- URL;

necessários ao compartilhamento escolhido.

Nenhuma informação oculta deve ser anexada.

---

# 32. WhatsApp

O link de compartilhamento para WhatsApp deve conter somente o texto que o usuário vê antes de compartilhar.

Não inserir dados adicionais invisíveis para tracking.

UTMs genéricos podem ser utilizados desde que:

- não identifiquem o usuário;
- não revelem renda;
- não revelem resultado financeiro.

---

# 33. Gov.br

O Renda Comparada nunca deve solicitar:

- senha gov.br;
- código de autenticação;
- token;
- QR Code de login;
- credenciais bancárias.

---

# 34. Registrato

Quando orientar o usuário a utilizar o Registrato:

> direcionar para o serviço oficial.

O Renda Comparada deve explicar:

- o que é;
- para que serve;
- qual caminho seguir.

Não deve:

- imitar a tela do gov.br;
- receber credenciais;
- atuar como intermediário de autenticação;
- solicitar relatório privado sem necessidade.

---

# 35. Valores a Receber

Mesma regra:

> direcionar o usuário ao serviço oficial do Banco Central.

Não criar páginas que possam ser confundidas com o próprio serviço oficial.

---

# 36. Links Oficiais

Links externos de:

- Banco Central;
- gov.br;
- IBGE;
- CVM;
- Senacon;
- Enap;

devem apontar para domínios oficiais previamente validados.

---

# 37. Check-up Financeiro Futuro

O check-up poderá envolver informações mais delicadas, como:

- dívidas;
- valor de parcelas;
- despesas;
- reserva financeira;
- patrimônio;
- capacidade de poupança.

Essas funcionalidades exigirão revisão deste documento **antes da implementação**.

---

# 38. Regra Para O Check-up

Preferência inicial:

> **processar respostas localmente e não persistir.**

O usuário deve conseguir receber orientação sem necessariamente criar uma conta.

---

# 39. Cadastro Futuro

Se futuramente houver benefício real em salvar histórico:

> cadastro deve ser uma funcionalidade separada e opcional.

A calculadora principal não deve exigir cadastro.

---

# 40. Histórico Financeiro

Não criar histórico persistente simplesmente porque tecnicamente é possível.

Antes de armazenar histórico será necessário definir:

- finalidade;
- base jurídica;
- período de retenção;
- exclusão;
- exportação;
- segurança;
- controle de acesso;
- direito do titular.

---

# 41. Crianças

A calculadora solicita quantidade total de moradores e orienta que crianças sejam incluídas.

Isso **não significa que o site precise coletar dados pessoais das crianças**.

Na V1, não solicitar:

- nome da criança;
- idade exata;
- CPF;
- escola;
- saúde;
- localização;
- qualquer identificador individual.

---

# 42. Dados De Crianças Em Versões Futuras

Qualquer funcionalidade que passe a coletar dados identificáveis de crianças ou adolescentes exige análise específica antes de implementação.

Não inferir autorização a partir do simples campo:

> “número de moradores”.

---

# 43. Cookies

Preferência da V1:

> **utilizar o menor número possível de cookies.**

Se for possível operar analytics sem cookies não necessários:

> preferir essa arquitetura.

---

# 44. Cookies Necessários

Cookies estritamente necessários ao funcionamento podem ser utilizados quando houver justificativa técnica.

Devem possuir:

- finalidade definida;
- duração mínima adequada;
- segurança compatível.

---

# 45. Cookies Não Necessários

Cookies não necessários, incluindo determinadas tecnologias analíticas, publicitárias ou de perfilização, exigem avaliação específica e tratamento transparente.

A ANPD mantém guia orientativo específico sobre cookies e diferencia cookies necessários, analíticos, publicitários, de terceiros e outras categorias.

Na dúvida:

> **não adicionar o cookie.**

---

# 46. Publicidade E Pixels

Na V1, evitar pixels publicitários que permitam construir perfis financeiros a partir do uso da calculadora.

Exemplos que exigem revisão específica antes de implantação:

- Meta Pixel;
- Google Ads remarketing;
- TikTok Pixel;
- ferramentas equivalentes.

---

# 47. Retargeting

Não criar públicos como:

> “usuários Top 5%”

> “usuários com renda alta”

> “usuários endividados”

para publicidade.

Essa prática conflitaria com o posicionamento de confiança do produto e aumentaria significativamente o risco de privacidade.

---

# 48. Monetização Futura

Qualquer modelo de monetização deve respeitar:

> **o dado financeiro do usuário não é o produto.**

Não vender:

- renda;
- perfil financeiro;
- respostas do check-up;
- segmentos financeiros individuais.

---

# 49. Política De Não Venda

A visão inicial do Renda Comparada deve adotar:

> **não vender dados pessoais dos usuários.**

Mudança desse princípio exigiria revisão estratégica, jurídica e documental explícita.

---

# 50. Fornecedores

Antes de adicionar fornecedor externo que receba dados ou telemetria, registrar:

- fornecedor;
- finalidade;
- dados recebidos;
- localização do processamento;
- retenção;
- medidas de segurança;
- mecanismo de exclusão;
- contrato aplicável.

---

# 51. Inventário De Terceiros

Manter documento ou tabela contendo, por exemplo:

|Serviço|Finalidade|Dados tratados|Necessário?|Produção|
|---|---|---|---|---|
|Vercel|hospedagem|técnico|sim|sim|
|Analytics|métricas|eventos mínimos|avaliar|definir|
|Error tracking|erros|metadados sanitizados|avaliar|definir|

Não adicionar serviço sem atualizar o inventário.

---

# 52. Transferência Internacional

Serviços em nuvem podem envolver tratamento ou armazenamento fora do Brasil.

Isso deve ser identificado e documentado antes da produção, observando a regulamentação vigente aplicável a transferências internacionais.

Não presumir localização física de dados sem verificar o fornecedor contratado.

---

# 53. Controlador

Antes do lançamento definitivo, definir:

```text
CONTROLADOR = [DEFINIR]
```

O controlador é quem tomará as decisões sobre o tratamento dos dados pessoais no contexto do produto.

Não publicar Política de Privacidade definitiva enquanto essa informação não estiver clara.

---

# 54. Operadores

Fornecedores que tratem dados pessoais em nome do controlador devem ser identificados conforme sua função real.

A ANPD mantém orientação específica sobre controlador, operador e encarregado.

---

# 55. Canal De Privacidade

Antes do lançamento, definir:

```text
PRIVACY_CONTACT = [DEFINIR]
```

O usuário deve possuir forma clara de:

- tirar dúvidas;
- exercer direitos;
- reportar problema relacionado a dados.

---

# 56. Direitos Dos Titulares

Quando houver tratamento de dados pessoais, o projeto deve oferecer mecanismo adequado para exercício dos direitos previstos na LGPD, conforme aplicáveis ao tratamento efetivamente realizado.

Entre eles estão:

- confirmação do tratamento;
- acesso;
- correção;
- anonimização, bloqueio ou eliminação em situações previstas;
- informações sobre compartilhamentos;
- revogação de consentimento quando esse for utilizado;
- outros direitos previstos na legislação.

---

# 57. Ausência De Armazenamento

Se o usuário solicitar:

> “apague a renda que digitei”

e a V1 efetivamente nunca tiver armazenado essa renda:

o atendimento deve explicar claramente que o valor foi utilizado apenas temporariamente e não foi mantido nos sistemas do produto.

Não fingir possuir dados que não existem.

---

# 58. Política De Privacidade Pública

Antes do lançamento definitivo, publicar aviso compreensível contendo, conforme aplicável:

- quem é o controlador;
- quais dados são tratados;
- para quais finalidades;
- tecnologias utilizadas;
- fornecedores;
- retenção;
- compartilhamentos;
- direitos;
- canal de contato;
- segurança;
- cookies.

O documento público deve refletir **o sistema real**, não um template genérico.

---

# 59. Segurança De Transporte

Todo tráfego público deve utilizar:

```text
HTTPS
```

Não permitir envio de informações através de HTTP inseguro.

---

# 60. HSTS

Quando compatível com a infraestrutura, configurar:

```text
Strict-Transport-Security
```

para reduzir risco de downgrade de conexão.

---

# 61. Security Headers

Avaliar e configurar adequadamente:

```text
Content-Security-Policy
X-Content-Type-Options
Referrer-Policy
Permissions-Policy
```

e demais headers pertinentes.

Não copiar políticas genéricas sem testar o funcionamento da aplicação.

---

# 62. Content Security Policy

A CSP deve, progressivamente:

- limitar origens de scripts;
- limitar conexões externas;
- reduzir risco de XSS;
- evitar `unsafe-eval` quando possível;
- reduzir `unsafe-inline` quando tecnicamente viável.

Toda exceção deve possuir justificativa.

---

# 63. Referrer Policy

Evitar vazamento desnecessário de informações para domínios externos.

Como URLs não devem possuir renda, o risco já deve ser reduzido pela arquitetura.

Ainda assim, configurar política de referrer adequada.

---

# 64. Validação De Inputs

Não confiar em entradas do usuário.

Validar:

- tipo;
- tamanho;
- limites;
- formato;
- valores permitidos.

A validação de UI não substitui validação do lado responsável pelo processamento quando houver servidor envolvido.

---

# 65. XSS

Qualquer texto ou dado inserido pelo usuário deve ser tratado como não confiável.

Não injetar entrada diretamente como HTML.

---

# 66. Dependências

Manter dependências:

- atualizadas;
- minimizadas;
- auditáveis.

Evitar adicionar biblioteca pesada apenas para função simples.

---

# 67. Vulnerabilidades

Incluir no fluxo de desenvolvimento:

- atualização periódica;
- verificação de vulnerabilidades;
- revisão de alertas de dependências;
- correção prioritária de vulnerabilidades relevantes.

---

# 68. Secrets

Nunca colocar no repositório:

- tokens;
- chaves privadas;
- senhas;
- segredos de API;
- credenciais de produção.

Utilizar mecanismo seguro de variáveis/segredos da infraestrutura.

---

# 68A. Achado Operacional — Google Drive Público Com Escrita

Verificação realizada em 14/08/2026 identificou na pasta raiz `Calculadora de renda` e no arquivo `.env.local` a permissão:

```text
type = anyone
role = writer
allowFileDiscovery = false
```

Isto significa que qualquer pessoa com o link pode editar o conteúdo compartilhado. Como `.env.local` está dentro da mesma pasta e herda essa permissão, o cenário deve ser tratado como **P0 operacional de segurança**.

### Ações exigidas antes de produção

1. restringir o compartilhamento público de escrita;
2. confirmar que os conectores autorizados continuam funcionando sem acesso público;
3. remover do espaço compartilhado cópias de arquivos de segredos que não precisem estar no Drive;
4. considerar rotação de tokens, chaves ou credenciais que possam ter ficado acessíveis;
5. revisar `.git`, `.vercel`, builds e outros artefatos locais que não precisem ser sincronizados publicamente.

### Limite de automação

Um agente não deve alterar permissões de compartilhamento ou rotacionar credenciais sem decisão explícita do responsável, pois isso pode interromper integrações e acesso legítimo.

---

# 69. Client-side Secrets

Qualquer valor enviado ao JavaScript público deve ser considerado:

> **público.**

Não colocar segredo real em:

```text
NEXT_PUBLIC_*
VITE_*
```

ou equivalentes expostos ao browser.

---

# 70. GitHub

Contas com acesso de escrita ao repositório devem utilizar, sempre que possível:

- autenticação forte;
- MFA;
- menor privilégio necessário.

Branches de produção devem possuir proteção adequada.

---

# 71. Vercel / Infraestrutura

Contas com capacidade de:

- alterar DNS;
- mudar produção;
- ler secrets;
- publicar deploy;

devem ser limitadas a pessoas autorizadas e protegidas por autenticação forte.

---

# 72. Ambientes

Separar quando pertinente:

```text
development
preview
production
```

Dados ou segredos de produção não devem ser usados desnecessariamente no desenvolvimento.

---

# 73. Deploy

Alterações relevantes devem passar por:

1. revisão;
2. testes;
3. preview;
4. validação;
5. produção.

Evitar mudanças estatísticas ou de segurança diretamente em produção sem revisão.

---

# 74. Dados Oficiais

Datasets de:

- IBGE;
- Banco Mundial;

não são dados pessoais dos usuários do site.

Ainda assim:

- verificar integridade;
- versionar;
- validar checksum;
- proteger pipeline contra alteração acidental ou maliciosa;
- não anexar dados do usuário às requisições desses artefatos públicos.

---

# 75. Integridade Estatística

Segurança também significa impedir que alguém altere os dados para produzir resultados falsos.

Portanto:

- datasets devem ser versionados;
- alterações devem ser rastreáveis;
- checksums devem ser mantidos;
- produção deve utilizar apenas datasets aprovados.

---

# 76. Backup

Backups devem priorizar:

- código;
- configurações;
- datasets processados;
- documentação.

Como a V1 não deve armazenar renda dos usuários:

> não deverá existir backup de históricos de renda que nunca precisaram ser criados.

---

# 77. Retenção

Cada categoria de dado deve possuir prazo ou critério de retenção.

Exemplo:

### Renda Do Cálculo

```text
retenção = nenhuma persistência
```

### Logs Técnicos

```text
retenção = mínima necessária para segurança/operação
```

### Dados De Contato Futuros

```text
retenção = definir conforme finalidade
```

---

# 78. Não Guardar “Para tAlvez uSar dEpois”

É proibido justificar retenção com:

> “Pode ser útil futuramente.”

Toda retenção exige finalidade atual e documentada.

---

# 79. Incidente De Segurança

Considerar incidente qualquer evento confirmado que comprometa, conforme aplicável:

- confidencialidade;
- integridade;
- disponibilidade;

de dados pessoais ou sistemas que os tratam.

---

# 80. Exemplos De Incidentes

- acesso indevido a logs;
- vazamento de dados financeiros;
- credencial comprometida;
- banco exposto;
- malware;
- alteração maliciosa dos resultados;
- coleta involuntária por analytics;
- envio de renda para terceiro não previsto.

---

# 81. Plano De Resposta

Manter processo para:

```text
detectar
↓
conter
↓
preservar evidências
↓
avaliar impacto
↓
corrigir
↓
avaliar obrigação de comunicação
↓
documentar
↓
evitar recorrência
```

---

# 82. Comunicação De Incidente

A regulamentação vigente da ANPD determina comunicação à ANPD e aos titulares, em até **3 dias úteis**, quando o incidente puder acarretar risco ou dano relevante, ressalvadas hipóteses legais específicas.

A decisão de comunicação deve ser feita de acordo com:

- natureza do incidente;
- dados envolvidos;
- riscos;
- regulamentação vigente.

---

# 83. Registro De Incidentes

A regulamentação atual exige manutenção do registro de incidentes de segurança envolvendo dados pessoais por **pelo menos cinco anos**, mesmo no contexto das regras específicas de comunicação.

O projeto deve manter processo adequado para esse registro quando aplicável.

---

# 84. Renda E Incidentes

Embora renda não seja automaticamente uma categoria legal de dado pessoal sensível, a ANPD considera **dados financeiros** relevantes na avaliação de risco ou dano de incidentes.

Por isso, o Renda Comparada deve tratar informações financeiras com nível interno elevado de confidencialidade.

---

# 85. Reporte Interno

Definir antes da produção:

```text
SECURITY_CONTACT = [DEFINIR]
```

Toda pessoa com acesso ao projeto deve saber:

> onde reportar incidente ou vulnerabilidade.

---

# 86. Vulnerability Disclosure

Futuramente considerar canal público simples:

> **Reportar vulnerabilidade**

especialmente se o produto ganhar escala.

---

# 87. Dados Do Check-up

Antes de implementar o check-up financeiro completo, revisar especificamente:

- persistência;
- analytics;
- profiling;
- recomendações;
- dados sobre dívidas;
- patrimônio;
- reserva;
- despesas;
- objetivos.

Não assumir automaticamente as regras da calculadora simples.

---

# 88. Perfil Financeiro

O sistema não deve criar um perfil persistente do usuário sem necessidade clara.

Especialmente evitar perfis como:

```text
alta renda
endividado
investidor
sem reserva
cliente potencial
```

para finalidades comerciais não informadas.

---

# 89. Decisões Automatizadas

Orientações financeiras futuras devem ser apresentadas como:

> educação e priorização geral.

Não utilizar o sistema para tomar decisões relevantes sobre:

- concessão de crédito;
- seguro;
- emprego;
- preços individualizados;
- acesso a serviços.

Qualquer evolução nessa direção exige análise jurídica e técnica específica.

---

# 90. Dados Para IA

Não utilizar respostas financeiras dos usuários para:

- treinamento de modelos;
- fine-tuning;
- criação de datasets;
- avaliação humana;

sem avaliação e transparência específicas.

O fato de um dado ter sido digitado no site não implica autorização para reutilização ilimitada.

---

# 91. Ferramentas De IA Futuras

Se IA for utilizada no check-up:

- não enviar automaticamente toda a situação financeira para fornecedor externo;
- minimizar contexto;
- avaliar política do fornecedor;
- documentar tratamento;
- evitar retenção desnecessária;
- informar o usuário quando relevante.

---

# 92. Princípio De Segurança Do Codex

O Codex não deve:

- adicionar analytics sem solicitação;
- adicionar tracking “para ajudar”;
- criar banco para persistir renda;
- incluir inputs em logs;
- colocar dados em URLs;
- instalar session replay;
- adicionar pixels de marketing;
- alterar política de cookies;

sem requisito explícito.

---

# 93. Revisão De Pull Request

Mudanças envolvendo:

- dados do usuário;
- analytics;
- banco;
- logs;
- autenticação;
- cookies;
- terceiros;
- compartilhamento;

devem receber revisão de privacidade e segurança antes de merge.

---

# 94. Checklist Para Nova Funcionalidade

Antes de aprovar nova feature:

- Que dados ela precisa?
- Todos são necessários?
- Pode funcionar sem armazená-los?
- Onde são processados?
- Quem recebe?
- Quanto tempo ficam armazenados?
- Aparecem em logs?
- Aparecem em analytics?
- Aparecem em URLs?
- São compartilhados?
- Existe fornecedor externo?
- Precisamos atualizar Política de Privacidade?
- Precisamos atualizar Política de Cookies?
- Precisamos de nova revisão jurídica?
- Existe risco específico para crianças?
- Existe risco financeiro relevante?

---

# 95. Checklist De Produção V1

Antes do lançamento:

- controlador definido;
- canal de privacidade definido;
- contato de segurança definido;
- Política de Privacidade publicada;
- cookies inventariados;
- fornecedores inventariados;
- analytics auditado;
- renda ausente do analytics;
- renda ausente de logs;
- renda ausente das URLs;
- session replay desativado ou inexistente;
- compartilhamento auditado;
- HTTPS obrigatório;
- security headers revisados;
- secrets protegidos;
- dependências auditadas;
- MFA habilitado nas contas críticas;
- acessos revisados;
- plano de incidente definido;
- backups testados quando aplicáveis.

---

# 96. Teste De Vazamento

Executar antes da produção um cálculo contendo valor facilmente identificável.

Exemplo:

```text
R$ 12.345.678
7 moradores
```

Depois pesquisar esse valor em:

- Network DevTools;
- logs;
- analytics;
- error tracking;
- URL;
- console;
- localStorage;
- sessionStorage;
- cookies;
- ferramentas de terceiros.

Resultado esperado:

> **o valor não aparece fora do processamento estritamente necessário.**

---

# 97. Teste De Compartilhamento

Realizar cálculo e compartilhar através de:

- WhatsApp;
- Web Share;
- copiar link.

Verificar que o destinatário não recebe:

- renda;
- moradores;
- renda per capita;

quando o modo privado for usado.

---

# 98. Teste De Reload

Após digitar renda e recarregar a página:

> verificar se o valor permanece armazenado.

Com a política inicial da V1, o comportamento preferido é:

> **não permanecer**, salvo decisão UX explícita e revisada.

---

# 99. Teste De Terceiros

Utilizar DevTools para identificar todas as requisições externas.

Cada domínio externo deve possuir uma razão conhecida.

Se aparecer domínio desconhecido:

> investigar antes da produção.

---

# 100. Norte De Privacidade

O usuário deve sentir que pode utilizar o Renda Comparada sem medo de que sua curiosidade financeira vire um perfil comercial.

A arquitetura deve permitir afirmar com verdade:

> **Você pode descobrir sua posição sem nos dizer quem você é.**

E, sempre que tecnicamente possível:

> **Seu cálculo acontece sem que precisemos guardar sua renda.**

---

# 101. Norte De Segurança

O projeto deve seguir três prioridades:

> **coletar menos**

> **expor menos**

> **guardar menos**

A melhor proteção para um dado financeiro que não precisamos manter é:

> # nunca armazená-lo.
