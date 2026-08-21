import { useRef, useState, type FormEvent } from 'react'
import {
  ArrowDown,
  ArrowUpRight,
  Check,
  CircleHelp,
  Globe2,
  Link2,
  MessageCircle,
  Minus,
  Plus,
  Share2,
  ShieldCheck,
  Sparkles,
} from 'lucide-react'
import {
  calculateBrazilIncomePosition,
  clampVisualMarkerPercent,
  formatBrazilPosition,
  parseBrazilianCurrency,
  parseHouseholdSize,
  type BrazilIncomePosition,
} from './brazil/domain.ts'
import { brazilEngineLoader } from './brazil/loader.ts'
import { calculateWorldIncomePosition, type WorldIncomePosition, type WorldIncomeRuntime } from './world/domain.ts'
import { worldEngineLoader } from './world/loader.ts'
import {
  datasetYearFromVersion,
  formatReferenceMonth,
  shouldShowSharing,
} from './presentation.ts'
import {
  buildPositionShareMessage,
  buildSharePayload,
  buildShareUrl,
  buildWhatsAppUrl,
} from './share.ts'

function money(value: number, maximumFractionDigits = 2) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 2,
    maximumFractionDigits,
  }).format(value)
}

function formatCurrencyInput(value: number) {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(value)
}

type BrazilCalculationState =
  | { status: 'idle' | 'loading' | 'unavailable'; result: null }
  | { status: 'success'; result: BrazilIncomePosition }

type WorldCalculationState =
  | { status: 'idle' | 'loading' | 'unavailable'; result: null }
  | { status: 'success'; result: WorldIncomePosition }

type FieldErrors = {
  income?: string
  household?: string
}

function BrazilResultCard({ result }: { result: BrazilIncomePosition }) {
  const display = formatBrazilPosition(result)
  const markerPercent = display.markerPercent === null
    ? null
    : clampVisualMarkerPercent(display.markerPercent)

  return (
    <article className="result-card brasil">
      <div className="result-head">
        <span className="result-icon"><Sparkles size={20} strokeWidth={1.8} /></span>
        <span>No Brasil</span>
      </div>
      <p className="eyebrow">Posição estimada na distribuição</p>
      {display.topLabel ? (
        <div className="position-number"><strong>{display.topLabel}</strong></div>
      ) : (
        <p className="limit-headline">{display.percentileLabel}</p>
      )}
      {markerPercent !== null && (
        <div className="result-ruler" aria-label={display.percentileLabel}>
          <span style={{ width: `${markerPercent}%` }} />
          <i style={{ left: `clamp(6.5px, ${markerPercent}%, calc(100% - 6.5px))` }} />
        </div>
      )}
      {display.topLabel && <p className="position-label">{display.percentileLabel}</p>}
      <p className="rank-note">{display.interpretation}</p>
    </article>
  )
}

function WorldResultCard({ result, runtime }: { result: WorldIncomePosition; runtime: WorldIncomeRuntime | null }) {
  const presentation = result.presentation
  const topLabel = presentation.kind === 'main' || presentation.kind === 'upper-tail'
    ? `TOP ${presentation.topDisplayPp.toLocaleString('pt-BR')}%`
    : null
  const positionLabel = presentation.kind === 'main'
    ? `Percentil ${presentation.percentileDisplay}`
    : presentation.kind === 'upper-tail'
      ? 'Cauda superior da distribuição observada'
      : null
  const headline = 'headline' in presentation ? presentation.headline : null

  return (
    <article className="result-card mundo">
      <div className="result-head">
        <span className="result-icon"><Globe2 size={20} strokeWidth={1.8} /></span>
        <span>No mundo</span>
      </div>
      <p className="eyebrow">Posição monetária global estimada</p>
      {topLabel ? (
        <div className="position-number"><strong>{topLabel}</strong></div>
      ) : (
        <p className="limit-headline">{headline}</p>
      )}
      {positionLabel && <p className="position-label">{positionLabel}</p>}
      <p className="rank-note">
        {runtime
          ? `Referência global ${runtime.referenceYear}, PPP ${runtime.pppBase}. `
          : 'Referência global validada pelo runtime. '}
        Resultado estimado com base na distribuição observada pelo World Bank — Poverty and Inequality Platform.
      </p>
    </article>
  )
}

function EngineLoadingCard({ engine }: { engine: 'Brasil' | 'Mundo' }) {
  return (
    <article className={`result-card ${engine === 'Brasil' ? 'brasil' : 'mundo'} unavailable`}>
      <div className="result-head">
        <span className="result-icon">{engine === 'Brasil' ? <Sparkles size={20} /> : <Globe2 size={20} />}</span>
        <span>No {engine === 'Brasil' ? 'Brasil' : 'mundo'}</span>
      </div>
      <p className="eyebrow">Carregando base</p>
      <p className="limit-headline">Calculando…</p>
      <p className="rank-note">O artefato estático é validado antes do cálculo.</p>
    </article>
  )
}

function EngineUnavailableCard({ engine }: { engine: 'Brasil' | 'Mundo' }) {
  return (
    <article className={`result-card ${engine === 'Brasil' ? 'brasil' : 'mundo'} unavailable`} role="alert">
      <div className="result-head">
        <span className="result-icon"><CircleHelp size={20} /></span>
        <span>No {engine === 'Brasil' ? 'Brasil' : 'mundo'}</span>
      </div>
      <p className="eyebrow">Base indisponível</p>
      <p className="limit-headline">Não foi possível calcular</p>
      <p className="rank-note">Nenhum número provisório ou fallback legado é exibido. Tente novamente.</p>
    </article>
  )
}

function App() {
  const [incomeInput, setIncomeInput] = useState('')
  const [householdInput, setHouseholdInput] = useState('')
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const [brazilCalculation, setBrazilCalculation] = useState<BrazilCalculationState>({ status: 'idle', result: null })
  const [worldCalculation, setWorldCalculation] = useState<WorldCalculationState>({ status: 'idle', result: null })
  const [showMethod, setShowMethod] = useState(false)
  const [includePosition, setIncludePosition] = useState(false)
  const [shareFeedback, setShareFeedback] = useState('')
  const calculationRequest = useRef(0)
  const incomeInputRef = useRef<HTMLInputElement>(null)
  const householdInputRef = useRef<HTMLInputElement>(null)

  const parsedIncome = parseBrazilianCurrency(incomeInput)
  const parsedHousehold = parseHouseholdSize(householdInput)
  const nominalPerPerson =
    parsedIncome.ok && parsedHousehold.ok ? parsedIncome.value / parsedHousehold.value : null

  function invalidateResult() {
    calculationRequest.current += 1
    setBrazilCalculation({ status: 'idle', result: null })
    setWorldCalculation({ status: 'idle', result: null })
    setIncludePosition(false)
    setShareFeedback('')
  }

  function updateIncome(value: string) {
    setIncomeInput(value)
    setFieldErrors((errors) => ({ ...errors, income: undefined }))
    invalidateResult()
  }

  function updateHousehold(value: string) {
    setHouseholdInput(value)
    setFieldErrors((errors) => ({ ...errors, household: undefined }))
    invalidateResult()
  }

  function changeHousehold(delta: number) {
    const current = parseHouseholdSize(householdInput)
    updateHousehold(String(Math.max(1, (current.ok ? current.value : 1) + delta)))
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const request = ++calculationRequest.current
    const income = parseBrazilianCurrency(incomeInput)
    const household = parseHouseholdSize(householdInput)
    const errors: FieldErrors = {}
    setIncludePosition(false)
    setShareFeedback('')

    if (!income.ok) {
      errors.income = income.reason === 'negative'
        ? 'A renda não pode ser negativa.'
        : 'Informe uma renda válida, usando no máximo duas casas decimais.'
    }
    if (!household.ok) {
      errors.household = 'Informe um número inteiro de moradores, a partir de 1.'
    }
    setFieldErrors(errors)
    if (!income.ok || !household.ok) {
      setBrazilCalculation({ status: 'idle', result: null })
      setWorldCalculation({ status: 'idle', result: null })
      if (!income.ok) incomeInputRef.current?.focus()
      else householdInputRef.current?.focus()
      return
    }

    const cachedBrazilRuntime = brazilEngineLoader.getCached()
    if (cachedBrazilRuntime) {
      setBrazilCalculation({
        status: 'success',
        result: calculateBrazilIncomePosition(cachedBrazilRuntime, income.value, household.value),
      })
    } else {
      setBrazilCalculation({ status: 'loading', result: null })
      void brazilEngineLoader.load().then((runtime) => {
        if (request !== calculationRequest.current) return
        setBrazilCalculation({
          status: 'success',
          result: calculateBrazilIncomePosition(runtime, income.value, household.value),
        })
      }).catch(() => {
        if (request !== calculationRequest.current) return
        setBrazilCalculation({ status: 'unavailable', result: null })
      })
    }

    const cachedWorldRuntime = worldEngineLoader.getCached()
    if (cachedWorldRuntime) {
      setWorldCalculation({
        status: 'success',
        result: calculateWorldIncomePosition(cachedWorldRuntime, income.value, household.value),
      })
    } else {
      setWorldCalculation({ status: 'loading', result: null })
      void worldEngineLoader.load().then((runtime) => {
        if (request !== calculationRequest.current) return
        setWorldCalculation({
          status: 'success',
          result: calculateWorldIncomePosition(runtime, income.value, household.value),
        })
      }).catch(() => {
        if (request !== calculationRequest.current) return
        setWorldCalculation({ status: 'unavailable', result: null })
      })
    }
  }

  const brazilDisplay = brazilCalculation.status === 'success'
    ? formatBrazilPosition(brazilCalculation.result)
    : null
  const positionShareMessage = buildPositionShareMessage(brazilDisplay)
  const shareUrl = buildShareUrl(window.location.origin)
  const sharePayload = buildSharePayload(shareUrl, includePosition, positionShareMessage)
  const showSharing = shouldShowSharing(brazilCalculation.status, worldCalculation.status)
  const brazilRuntime = brazilEngineLoader.getCached()
  const worldRuntime = worldEngineLoader.getCached()
  const brazilDatasetYear = brazilRuntime
    ? datasetYearFromVersion(brazilRuntime.datasetVersion)
    : null
  const brazilReferenceMonth = brazilRuntime
    ? formatReferenceMonth(brazilRuntime.referenceMonth)
    : null

  async function copyShareLink(fallbackMessage = 'Link copiado') {
    if (!navigator.clipboard?.writeText) {
      setShareFeedback('Não foi possível copiar automaticamente. Use o endereço desta página.')
      return
    }
    try {
      await navigator.clipboard.writeText(shareUrl)
      setShareFeedback(fallbackMessage)
    } catch {
      setShareFeedback('Não foi possível copiar automaticamente. Use o endereço desta página.')
    }
  }

  async function handleNativeShare() {
    if (typeof navigator.share !== 'function') {
      await copyShareLink('Compartilhamento nativo indisponível. Link copiado.')
      return
    }
    try {
      await navigator.share(sharePayload)
      setShareFeedback('Compartilhamento aberto')
    } catch (error) {
      if (error instanceof DOMException && error.name === 'AbortError') return
      setShareFeedback('Não foi possível abrir o compartilhamento.')
    }
  }

  return (
    <div className="site-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Renda Comparada — início">
          <span className="brand-mark"><i /><i /></span>
          <span>RENDA<br />COMPARADA</span>
        </a>
        <a className="method-link" href="#metodologia">Como calculamos <ArrowDown size={15} /></a>
      </header>

      <main id="top">
        <section className="hero">
          <div className="hero-copy">
            <div className="kicker"><span /> Brasil e mundo disponíveis</div>
            <h1><span>Você é mais rico do que</span><br /><em>quantos brasileiros?</em></h1>
            <p>Descubra onde a renda da sua família está no Brasil — e onde ela estaria no mundo.</p>
          </div>
          <aside className="hero-note">
            <span>01</span>
            <p>A comparação é de renda,<br />não de patrimônio.<br />O cálculo considera todo o domicílio.</p>
          </aside>
        </section>

        <section className="calculator" aria-label="Calculadora de posição de renda">
          <form className="form-panel" onSubmit={handleSubmit} noValidate>
            <div className="panel-heading">
              <span>SEUS DADOS</span>
              <small>Renda mensal atual</small>
            </div>

            <label className="field-label income-label" htmlFor="income">Renda mensal da casa</label>
            <div className={`money-input-wrap ${fieldErrors.income ? 'invalid' : ''}`}>
              <span>R$</span>
              <input
                ref={incomeInputRef}
                id="income"
                inputMode="decimal"
                value={incomeInput}
                onChange={(event) => updateIncome(event.target.value)}
                onBlur={() => {
                  const income = parseBrazilianCurrency(incomeInput)
                  if (income.ok) setIncomeInput(formatCurrencyInput(income.value))
                }}
                aria-describedby={fieldErrors.income ? 'income-help income-error' : 'income-help'}
                aria-invalid={Boolean(fieldErrors.income)}
              />
            </div>
            <p className="field-help" id="income-help">Use a renda bruta mensal, antes de impostos e despesas.</p>
            {fieldErrors.income && <p className="field-error" id="income-error" role="alert">{fieldErrors.income}</p>}

            <div className="household-row">
              <div>
                <label className="field-label" htmlFor="household">Quantas pessoas fazem parte deste domicílio?</label>
                <p className="field-help" id="household-help">Inclua adultos e crianças, mesmo que não tenham renda.</p>
                <details className="household-technical-help" id="household-technical-help">
                  <summary>Quem não entra no indicador brasileiro?</summary>
                  <p>Há exclusões técnicas do IBGE para empregado doméstico residente, parente de empregado doméstico e “pensionista” na classificação da condição no domicílio. Aqui, “pensionista” é uma categoria técnica e não significa automaticamente alguém que recebe pensão.</p>
                </details>
                {fieldErrors.household && <p className="field-error" id="household-error" role="alert">{fieldErrors.household}</p>}
              </div>
              <div className={`stepper ${fieldErrors.household ? 'invalid' : ''}`}>
                <button type="button" onClick={() => changeHousehold(-1)} aria-label="Diminuir número de pessoas">
                  <Minus size={18} />
                </button>
                <input
                  ref={householdInputRef}
                  id="household"
                  type="text"
                  inputMode="numeric"
                  value={householdInput}
                  onChange={(event) => updateHousehold(event.target.value)}
                  aria-describedby={fieldErrors.household ? 'household-help household-technical-help household-error' : 'household-help household-technical-help'}
                  aria-invalid={Boolean(fieldErrors.household)}
                />
                <button type="button" onClick={() => changeHousehold(1)} aria-label="Aumentar número de pessoas">
                  <Plus size={18} />
                </button>
              </div>
            </div>

            <div className="per-capita-strip">
              <span>Renda nominal por pessoa</span>
              <strong>{nominalPerPerson === null ? '—' : money(nominalPerPerson)}</strong>
            </div>
            <button className="calculate-button" type="submit" disabled={brazilCalculation.status === 'loading' || worldCalculation.status === 'loading'}>
              {brazilCalculation.status === 'loading' || worldCalculation.status === 'loading' ? 'Calculando sua posição…' : 'Descobrir minha posição'}
            </button>
            <div className="privacy-note"><ShieldCheck size={15} /><span>O cálculo acontece no seu navegador. Renda, moradores e resultado não são enviados.</span></div>
          </form>

          <div className="results-panel" aria-live="polite" aria-busy={brazilCalculation.status === 'loading' || worldCalculation.status === 'loading'}>
            <div className="panel-heading light">
              <span>SUA POSIÇÃO ESTIMADA</span>
              <small>{brazilRuntime ? `Brasil: ${brazilRuntime.priceReference}` : 'Brasil: referência validada no cálculo'}</small>
            </div>
            {brazilCalculation.status === 'idle' && worldCalculation.status === 'idle' && (
              <div className="results-state">
                <Sparkles size={28} />
                <p>Preencha os dados e selecione “Descobrir minha posição”.</p>
              </div>
            )}
            {(brazilCalculation.status !== 'idle' || worldCalculation.status !== 'idle') && (
              <>
                <div className="results-grid">
                  {brazilCalculation.status === 'success' && <BrazilResultCard result={brazilCalculation.result} />}
                  {brazilCalculation.status === 'loading' && <EngineLoadingCard engine="Brasil" />}
                  {brazilCalculation.status === 'unavailable' && <EngineUnavailableCard engine="Brasil" />}
                  {worldCalculation.status === 'success' && <WorldResultCard result={worldCalculation.result} runtime={worldRuntime} />}
                  {worldCalculation.status === 'loading' && <EngineLoadingCard engine="Mundo" />}
                  {worldCalculation.status === 'unavailable' && <EngineUnavailableCard engine="Mundo" />}
                </div>
                <div className="interpretation">
                  <CircleHelp size={18} />
                  <p><strong>Como ler:</strong> o percentil usa a parcela com renda estritamente menor; o TOP é seu complemento. Empates permanecem no mesmo degrau da distribuição.</p>
                </div>
                {showSharing && (
                  <section className="sharing" aria-labelledby="sharing-title">
                    <div className="sharing-heading">
                      <div>
                        <p className="eyebrow">PRIVADO POR PADRÃO</p>
                        <h2 id="sharing-title">Compartilhar</h2>
                      </div>
                      <ShieldCheck size={24} aria-hidden="true" />
                    </div>
                    <p>Sua renda e o número de moradores não serão mostrados.</p>
                    <label className={`share-position-toggle ${positionShareMessage ? '' : 'disabled'}`}>
                      <input
                        type="checkbox"
                        checked={includePosition}
                        disabled={!positionShareMessage}
                        onChange={(event) => {
                          setIncludePosition(event.target.checked)
                          setShareFeedback('')
                        }}
                      />
                      <span>Incluir minha posição — sem mostrar minha renda</span>
                    </label>
                    {!positionShareMessage && brazilCalculation.status === 'success' && (
                      <p className="share-limit-note">Esta posição está em um limite da pesquisa e será compartilhada sem número.</p>
                    )}
                    <div className="share-actions">
                      <button type="button" onClick={handleNativeShare}>
                        <Share2 size={18} aria-hidden="true" /> Compartilhar
                      </button>
                      <a href={buildWhatsAppUrl(sharePayload)} target="_blank" rel="noopener noreferrer">
                        <MessageCircle size={18} aria-hidden="true" /> WhatsApp
                      </a>
                      <button type="button" onClick={() => void copyShareLink()}>
                        <Link2 size={18} aria-hidden="true" /> Copiar link
                      </button>
                    </div>
                    <p className="share-feedback" role="status" aria-live="polite">{shareFeedback}</p>
                  </section>
                )}
              </>
            )}
          </div>
        </section>

        <section className="benchmarks" aria-labelledby="benchmarks-title">
          <div className="section-label">PARA DAR CONTEXTO</div>
          <div className="benchmark-intro">
            <h2 id="benchmarks-title">Números sozinhos<br />não contam a história.</h2>
            <p>A mesma renda sustenta vidas diferentes conforme cidade, moradia, saúde, dívidas e patrimônio. O resultado mostra somente uma posição estatística de renda.</p>
          </div>
          <div className="benchmark-grid">
            <article>
              <span>BASE</span>
              <p>Distribuição brasileira</p>
              <strong>{brazilDatasetYear ? `PNAD ${brazilDatasetYear}` : 'PNAD Contínua'}</strong>
              <small>pessoas elegíveis, ponderadas por V1032</small>
            </article>
            <article className="accent">
              <span>R$</span>
              <p>Referência monetária da comparação</p>
              <strong>{brazilRuntime?.priceReference ?? 'Referência validada'}</strong>
              <small>base monetária do runtime Brasil</small>
            </article>
            <article>
              <span>MUNDO</span>
              <p>Resultado global</p>
              <strong>{worldRuntime ? `PIP ${worldRuntime.referenceYear}` : 'PIP'}</strong>
              <small>posição monetária global estimada{worldRuntime ? `, PPP ${worldRuntime.pppBase}` : ''}</small>
            </article>
          </div>
        </section>

        <section className="methodology" id="metodologia">
          <div className="method-title">
            <div className="section-label">METODOLOGIA</div>
            <h2>Sem falsa precisão.</h2>
            <button type="button" onClick={() => setShowMethod((value) => !value)} aria-expanded={showMethod} aria-controls="method-details">
              {showMethod ? 'Ocultar detalhes' : 'Ver os detalhes'} <Plus size={18} />
            </button>
          </div>
          <div className="method-summary">
            <div><Check size={17} /><p><strong>Primeiro</strong> alinhamos a renda nominal atual à referência monetária validada pelo IPCA{brazilRuntime ? `: ${brazilRuntime.priceReference}` : ''}.</p></div>
            <div><Check size={17} /><p><strong>Depois</strong> dividimos a renda comparável pelo número inteiro de moradores.</p></div>
            <div><Check size={17} /><p><strong>Por fim</strong> consultamos a CDF empírica brasileira, sem interpolação.</p></div>
          </div>
          <div className="method-details" id="method-details" hidden={!showMethod}>
              <p>A distribuição usa a PNAD Contínua{brazilDatasetYear ? ` ${brazilDatasetYear}` : ''}. O RDPC é construído pela soma domiciliar de VD4019 × CO1 e VD4048 × CO1e, dividida por VD2003, com peso V1032 e unidade final de pessoas elegíveis.</p>
              <p>{brazilReferenceMonth && brazilRuntime
                ? `A renda informada é convertida de ${brazilReferenceMonth} para ${brazilRuntime.priceReference} antes da consulta brasileira. `
                : 'A renda informada é alinhada à referência monetária validada pelo runtime Brasil antes da consulta. '}
                A CDF é observada em degraus: não há interpolação nem extrapolação acima do máximo.</p>
              <p>No mundo, a renda mensal por pessoa é alinhada à referência de preços{worldRuntime ? ` de ${worldRuntime.referenceYear}` : ''} e convertida para dólares internacionais diários{worldRuntime ? ` em PPP ${worldRuntime.pppBase}` : ' pela PPP aprovada'}. A consulta preserva empates e limites do suporte observado, sem extrapolação.</p>
              <p>Brasil e Mundo não medem patrimônio e não são comparações idênticas: o Brasil usa renda domiciliar per capita de pessoas elegíveis na PNAD; o resultado mundial é uma estimativa monetária baseada em pesquisas harmonizadas de renda ou consumo entre países, não um ranking exato de salário.</p>
              <p>Como a V1 não coleta UF, o alinhamento brasileiro usa o IPCA nacional como aproximação oficial; diferenças regionais de preços não são modeladas.</p>
          </div>
        </section>

        <section className="sources">
          <div>
            <div className="section-label">FONTES CONSULTADAS</div>
            <h2>Dados públicos.<br />Limites visíveis.</h2>
          </div>
          <div className="source-list">
            <a href="https://www.ibge.gov.br/estatisticas/sociais/populacao/17270-pnad-continua.html" target="_blank" rel="noreferrer">
              <span><strong>IBGE — PNAD Contínua</strong><small>Microdados anuais{brazilDatasetYear ? ` de ${brazilDatasetYear}` : ''}</small></span>
              <ArrowUpRight size={19} />
            </a>
            <a href="https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2266/p/202501-202607?formato=json" target="_blank" rel="noreferrer">
              <span><strong>IBGE — SIDRA</strong><small>IPCA, números-índice mensais usados no alinhamento</small></span>
              <ArrowUpRight size={19} />
            </a>
            <a href="https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf" target="_blank" rel="noreferrer">
              <span><strong>IBGE — Rendimento de todas as fontes</strong><small>Informativo da PNAD Contínua{brazilDatasetYear ? ` ${brazilDatasetYear}` : ''}</small></span>
              <ArrowUpRight size={19} />
            </a>
            <a href="https://pip.worldbank.org/" target="_blank" rel="noreferrer">
              <span><strong>World Bank — Poverty and Inequality Platform</strong><small>Distribuição global{worldRuntime ? `, referência ${worldRuntime.referenceYear} e PPP ${worldRuntime.pppBase}` : ''}</small></span>
              <ArrowUpRight size={19} />
            </a>
          </div>
        </section>
      </main>

      <footer>
        <div className="brand footer-brand">
          <span className="brand-mark"><i /><i /></span>
          <span>RENDA<br />COMPARADA</span>
        </div>
        <p>Ferramenta educativa. Não é aconselhamento financeiro, econômico ou tributário.</p>
        <a href="#top">Voltar ao topo <ArrowUpRight size={15} /></a>
      </footer>
    </div>
  )
}

export default App
