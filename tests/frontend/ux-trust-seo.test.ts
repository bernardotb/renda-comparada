import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import test from 'node:test'

const root = new URL('../../', import.meta.url)

async function source(path: string) {
  return readFile(new URL(path, root), 'utf8')
}

test('campo de renda oferece definição progressiva e microcopy de privacidade limitada ao cálculo', async () => {
  const app = await source('src/App.tsx')

  assert.match(app, /Qual é a renda mensal total da sua casa\?/)
  assert.match(app, /Use a renda bruta mensal, antes de impostos e despesas\./)
  assert.match(app, /<summary>O que devo incluir\?<\/summary>/)
  assert.match(app, /Some os rendimentos mensais da casa antes de impostos e despesas, como salários e trabalho por conta própria, aposentadorias, pensões, aluguéis recebidos e outras rendas abrangidas pela metodologia\./)
  assert.match(app, /Não desconte aluguel, financiamento, cartão, plano de saúde ou gastos do mês\./)
  assert.match(app, /id="income-inclusion-help"/)
  assert.match(app, /aria-describedby=\{fieldErrors\.income \? 'income-help income-inclusion-help income-error' : 'income-help income-inclusion-help'\}/)
  assert.match(app, /Sua renda e o número de moradores são usados temporariamente no navegador para calcular o resultado\. Esses valores não são enviados aos servidores nem armazenados de forma persistente pelo produto\./)
  assert.equal(app.includes('Renda, moradores e resultado não são enviados.'), false)
})

test('jornada H3 prioriza entrada, descoberta Brasil, mudança de perspectiva e Mundo', async () => {
  const app = await source('src/App.tsx')
  const privacy = app.indexOf('Seu cálculo acontece no navegador. Sua renda não é armazenada.')
  const income = app.indexOf('Qual é a renda mensal total da sua casa?')
  const results = app.indexOf('className="results-panel"')
  const brazil = app.lastIndexOf('<BrazilResultCard')
  const perspective = app.indexOf('Agora mude a perspectiva.')
  const world = app.lastIndexOf('<WorldResultCard')

  assert.equal(privacy >= 0 && privacy < income, true)
  assert.match(app, /hasCalculationStarted && <div ref=\{resultPanelRef\} className="results-panel"/)
  assert.equal(brazil > results && perspective > brazil && world > perspective, true)
  assert.equal(app.includes('className="per-capita-strip"'), false)
  assert.match(app, /<strong>Em cada 100 pessoas,<\/strong> aproximadamente \{percentileForPeople\} estão abaixo da sua posição de renda\./)
})

test('resultado Mundo explica percentil, maior aproximação e relação com o Brasil sem novo cálculo', async () => {
  const app = await source('src/App.tsx')

  assert.match(app, /presentation\.kind === 'main'/)
  assert.match(app, /Sua posição estimada está aproximadamente no percentil \{presentation\.percentileDisplay\} da distribuição monetária mundial utilizada\./)
  assert.match(app, /A comparação global combina dados de renda ou consumo por pessoa de diferentes países, ajustados por poder de compra\. Por isso, é mais aproximada que a comparação brasileira\./)
  assert.match(app, /Brasil e Mundo podem mostrar posições diferentes porque usam distribuições, referências de preços e metodologias diferentes\./)
  assert.equal(app.includes('calculateWorldIncomePosition('), true)
  assert.equal((app.match(/calculateWorldIncomePosition\(/g) ?? []).length, 2)
})

test('fontes e versões do runtime ficam junto aos resultados com acesso à metodologia pública', async () => {
  const app = await source('src/App.tsx')

  for (const field of [
    'brazilDatasetYear',
    'brazilRuntime?.priceReference',
    'brazilReferenceMonth',
    'worldRuntime.referenceYear',
    'worldRuntime.pppBase',
    'worldRuntime.pipVersion',
  ]) assert.match(app, new RegExp(field.replace(/[?.]/g, '\\$&')))

  assert.match(app, /href="\/metodologia"/)
  assert.match(app, /Como calculamos isso\?/)
})

test('home contém o núcleo editorial depois do compartilhamento', async () => {
  const app = await source('src/App.tsx')
  const sharing = app.indexOf('className="sharing"')
  const editorial = app.indexOf('id="como-funciona"')

  assert.equal(sharing >= 0 && editorial > sharing, true)
  for (const heading of [
    'Como funciona?',
    'O que é percentil?',
    'Por que crianças entram no cálculo?',
    'Renda é a mesma coisa que patrimônio?',
    'Por que Brasil e Mundo podem apresentar posições diferentes?',
    'O resultado é exato?',
  ]) assert.match(app, new RegExp(heading.replace(/[?]/g, '\\?')))
  assert.match(app, /<strong>Exemplo:<\/strong> percentil 68 significa/)
  assert.match(app, /href="\/metodologia#moradores"/)
})

test('configuração MPA e fontes HTML declaram as rotas públicas sem router', async () => {
  const config = await source('vite.config.ts')
  const vercel = await source('vercel.json')
  const methodology = await source('metodologia/index.html')
  const privacy = await source('privacidade/index.html')

  assert.match(config, /metodologia\/index\.html/)
  assert.match(config, /privacidade\/index\.html/)
  assert.match(config, /appType: 'mpa'/)
  assert.match(vercel, /"source": "\/metodologia"/)
  assert.match(vercel, /"destination": "\/metodologia\/index\.html"/)
  assert.match(vercel, /"source": "\/privacidade"/)
  assert.match(vercel, /"destination": "\/privacidade\/index\.html"/)

  assert.match(methodology, /rel="canonical" href="https:\/\/rendacomparada\.com\.br\/metodologia"/)
  assert.match(methodology, /property="og:url" content="https:\/\/rendacomparada\.com\.br\/metodologia"/)
  assert.match(methodology, /id="moradores"/)
  for (const concept of ['PNAD Contínua 2025', 'IPCA', 'Poverty and Inequality Platform', 'PPP 2021', 'percentil', 'TOP', 'patrimônio']) {
    assert.match(methodology, new RegExp(concept, 'i'))
  }

  assert.match(privacy, /rel="canonical" href="https:\/\/rendacomparada\.com\.br\/privacidade"/)
  assert.match(privacy, /property="og:url" content="https:\/\/rendacomparada\.com\.br\/privacidade"/)
  for (const fact of ['Frederico Wiermann Barroso', 'privacidade@rendacomparada.com.br', 'temporariamente no seu navegador', 'genérico por padrão', 'Plausible Analytics']) {
    assert.match(privacy, new RegExp(fact, 'i'))
  }
  assert.match(privacy, /O cálculo não envia esses valores aos servidores, não os persiste nos sistemas do produto e não os inclui na URL\./)
  assert.match(privacy, /Os fornecedores de infraestrutura podem tratar dados técnicos necessários à operação e à entrega pública da aplicação\./)
  for (const unsupported of ['servidores localizados no Brasil', 'retenção de 30 dias', 'Google Analytics', 'Vercel Analytics']) {
    assert.equal(privacy.includes(unsupported), false, unsupported)
  }
})

test('SEO técnico usa D076 sem criar imagem OG fictícia', async () => {
  const [home, methodology, privacy, robots, sitemap] = await Promise.all([
    source('index.html'),
    source('metodologia/index.html'),
    source('privacidade/index.html'),
    source('public/robots.txt'),
    source('public/sitemap.xml'),
  ])

  assert.match(home, /rel="canonical" href="https:\/\/rendacomparada\.com\.br\/"/)
  assert.match(home, /property="og:url" content="https:\/\/rendacomparada\.com\.br\/"/)
  assert.match(robots, /Sitemap: https:\/\/rendacomparada\.com\.br\/sitemap\.xml/)
  for (const url of [
    'https://rendacomparada.com.br/',
    'https://rendacomparada.com.br/metodologia',
    'https://rendacomparada.com.br/privacidade',
  ]) assert.match(sitemap, new RegExp(`<loc>${url.replace(/[/.]/g, '\\$&')}</loc>`))

  const publicHtml = `${home}\n${methodology}\n${privacy}`
  assert.equal(/property="og:image"/i.test(publicHtml), false)
  assert.equal(publicHtml.includes('DEFAULT_OG_IMAGE'), false)
})

test('integração Plausible não adiciona persistência, pixels ou novas dependências', async () => {
  const [app, main, share, packageJson] = await Promise.all([
    source('src/App.tsx'),
    source('src/main.tsx'),
    source('src/share.ts'),
    source('package.json'),
  ])
  const active = `${app}\n${main}\n${share}`

  for (const forbidden of ['localStorage', 'sessionStorage', 'indexedDB', 'document.cookie', 'sendBeacon', 'gtag', 'dataLayer']) {
    assert.equal(active.includes(forbidden), false, forbidden)
  }
  assert.deepEqual(Object.keys(JSON.parse(packageJson).dependencies).sort(), [
    '@vitejs/plugin-react',
    'lucide-react',
    'react',
    'react-dom',
    'vite',
  ])
})

test('CSS declara override de smooth scroll para reduced motion', async () => {
  const styles = await source('src/styles.css')

  assert.match(styles, /html \{ scroll-behavior: smooth; \}/)
  assert.match(styles, /@media \(prefers-reduced-motion: reduce\) \{\s+html \{ scroll-behavior: auto; \}/)
})

test('fontes declaram nova simulação, foco de duas cores e alvos mínimos de 48px', async () => {
  const [app, styles] = await Promise.all([
    source('src/App.tsx'),
    source('src/styles.css'),
  ])

  assert.match(app, /function handleRecalculate\(\) \{\s+trackAnalyticsEvent\('recalculate_clicked'\)\s+incomeInputRef\.current\?\.focus\(\)/)
  assert.match(app, /className="recalculate-button"[^>]*onClick=\{handleRecalculate\}[\s\S]*?Simular outra renda/)
  assert.match(styles, /\.money-input-wrap:focus-within,[\s\S]*?outline: 2px solid var\(--lime\);[\s\S]*?outline-offset: 0;[\s\S]*?box-shadow: 0 0 0 4px var\(--ink\);/)
  assert.match(styles, /\.stepper:focus-within \{[\s\S]*?outline: 2px solid var\(--lime\);/)
  assert.match(styles, /\.stepper\.invalid:focus-within \{ box-shadow: 0 0 0 4px var\(--ink\); \}/)
  assert.match(styles, /\.stepper button:focus-visible, \.stepper input:focus-visible \{ outline: 0; box-shadow: none; \}/)
  assert.match(styles, /\.stepper button \{ width: 48px; height: 48px;/)
  assert.match(styles, /\.share-actions button, \.share-actions a \{ min-height: 48px;/)
})

test('inventário canônico registra o Google Fonts conforme a implementação atual', async () => {
  const [styles, privacy] = await Promise.all([
    source('src/styles.css'),
    source('docs/06-privacidade-seguranca.md'),
  ])

  assert.match(styles, /https:\/\/fonts\.googleapis\.com/)
  assert.match(privacy, /\|Google Fonts\|carregamento das fontes públicas utilizadas pela interface\|/)
  assert.match(privacy, /renda, moradores e resultado individual não são enviados explicitamente pela aplicação/)
  assert.match(privacy, /localização física.*retenção.*não foram verificados/i)
})
