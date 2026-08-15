import { useRef, useState, type FormEvent } from 'react'
import {
  ArrowDown,
  ArrowUpRight,
  Check,
  CircleHelp,
  Globe2,
  Minus,
  Plus,
  ShieldCheck,
  Sparkles,
} from 'lucide-react'
import {
  calculateBrazilIncomePosition,
  formatBrazilPosition,
  parseBrazilianCurrency,
  parseHouseholdSize,
  type BrazilIncomePosition,
} from './brazil/domain.ts'
import { brazilEngineLoader } from './brazil/loader.ts'

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

type CalculationState =
  | { status: 'idle' | 'loading' | 'unavailable'; result: null }
  | { status: 'success'; result: BrazilIncomePosition }

type FieldErrors = {
  income?: string
  household?: string
}

function BrazilResultCard({ result }: { result: BrazilIncomePosition }) {
  const display = formatBrazilPosition(result)

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
      {display.markerPercent !== null && (
        <div className="result-ruler" aria-label={display.percentileLabel}>
          <span style={{ width: `${Math.min(99.7, Math.max(0, display.markerPercent))}%` }} />
          <i style={{ left: `${Math.min(99.7, Math.max(0, display.markerPercent))}%` }} />
        </div>
      )}
      {display.topLabel && <p className="position-label">{display.percentileLabel}</p>}
      <p className="rank-note">{display.interpretation}</p>
    </article>
  )
}

function WorldUnavailableCard() {
  return (
    <article className="result-card mundo unavailable">
      <div className="result-head">
        <span className="result-icon"><Globe2 size={20} strokeWidth={1.8} /></span>
        <span>No mundo</span>
      </div>
      <p className="eyebrow">Comparação mundial</p>
      <p className="limit-headline">Indisponível nesta versão</p>
      <p className="position-label">A base mundial ainda está em validação.</p>
      <p className="rank-note">Nenhum número provisório ou curva antiga é exibido.</p>
    </article>
  )
}

function App() {
  const [incomeInput, setIncomeInput] = useState('12.000')
  const [householdInput, setHouseholdInput] = useState('3')
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const [calculation, setCalculation] = useState<CalculationState>({ status: 'idle', result: null })
  const [showMethod, setShowMethod] = useState(false)
  const calculationRequest = useRef(0)

  const parsedIncome = parseBrazilianCurrency(incomeInput)
  const parsedHousehold = parseHouseholdSize(householdInput)
  const nominalPerPerson =
    parsedIncome.ok && parsedHousehold.ok ? parsedIncome.value / parsedHousehold.value : null

  function invalidateResult() {
    calculationRequest.current += 1
    setCalculation({ status: 'idle', result: null })
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
      setCalculation({ status: 'idle', result: null })
      return
    }

    const cachedRuntime = brazilEngineLoader.getCached()
    if (cachedRuntime) {
      setCalculation({
        status: 'success',
        result: calculateBrazilIncomePosition(cachedRuntime, income.value, household.value),
      })
      return
    }

    setCalculation({ status: 'loading', result: null })
    try {
      const runtime = await brazilEngineLoader.load()
      if (request !== calculationRequest.current) return
      setCalculation({
        status: 'success',
        result: calculateBrazilIncomePosition(runtime, income.value, household.value),
      })
    } catch {
      if (request !== calculationRequest.current) return
      setCalculation({ status: 'unavailable', result: null })
    }
  }

  return (
    <div className="site-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Renda em Duas Escalas — início">
          <span className="brand-mark"><i /><i /></span>
          <span>RENDA<br />EM DUAS ESCALAS</span>
        </a>
        <a className="method-link" href="#metodologia">Como calculamos <ArrowDown size={15} /></a>
      </header>

      <main id="top">
        <section className="hero">
          <div className="hero-copy">
            <div className="kicker"><span /> Brasil disponível</div>
            <h1><span>Ranking de renda familiar</span><br /><em>no Brasil.</em></h1>
            <p>Informe a renda da sua casa e veja sua posição. A comparação mundial continua em validação.</p>
          </div>
          <aside className="hero-note">
            <span>01</span>
            <p>Não mede riqueza.<br />Considera a renda total da família<br />e quantas pessoas vivem dela.</p>
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
            <p className="field-help" id="income-help">Some salários e outras rendas regulares de quem mora com você.</p>
            {fieldErrors.income && <p className="field-error" id="income-error">{fieldErrors.income}</p>}

            <div className="household-row">
              <div>
                <label className="field-label" htmlFor="household">Pessoas sustentadas por essa renda</label>
                <p className="field-help">Inclua adultos e crianças.</p>
                {fieldErrors.household && <p className="field-error" id="household-error">{fieldErrors.household}</p>}
              </div>
              <div className={`stepper ${fieldErrors.household ? 'invalid' : ''}`}>
                <button type="button" onClick={() => changeHousehold(-1)} aria-label="Diminuir número de pessoas">
                  <Minus size={18} />
                </button>
                <input
                  id="household"
                  type="text"
                  inputMode="numeric"
                  value={householdInput}
                  onChange={(event) => updateHousehold(event.target.value)}
                  aria-label="Número de pessoas"
                  aria-describedby={fieldErrors.household ? 'household-error' : undefined}
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
            <button className="calculate-button" type="submit" disabled={calculation.status === 'loading'}>
              {calculation.status === 'loading' ? 'Calculando sua posição…' : 'Descobrir minha posição'}
            </button>
            <div className="privacy-note"><ShieldCheck size={15} /><span>O cálculo acontece no seu navegador. Renda, moradores e resultado não são enviados.</span></div>
          </form>

          <div className="results-panel" aria-live="polite" aria-busy={calculation.status === 'loading'}>
            <div className="panel-heading light">
              <span>SUA POSIÇÃO ESTIMADA</span>
              <small>Brasil: preços médios de 2025</small>
            </div>
            {calculation.status === 'idle' && (
              <div className="results-state">
                <Sparkles size={28} />
                <p>Preencha os dados e selecione “Descobrir minha posição”.</p>
              </div>
            )}
            {calculation.status === 'loading' && (
              <div className="results-state loading-state">
                <span className="loading-dot" />
                <p>Calculando sua posição…</p>
                <small>A base brasileira é carregada somente no primeiro cálculo.</small>
              </div>
            )}
            {calculation.status === 'unavailable' && (
              <div className="results-state error-state" role="alert">
                <CircleHelp size={28} />
                <p>Não foi possível carregar a base brasileira.</p>
                <small>Seus dados foram preservados. Tente novamente pelo mesmo botão.</small>
              </div>
            )}
            {calculation.status === 'success' && (
              <>
                <div className="results-grid">
                  <BrazilResultCard result={calculation.result} />
                  <WorldUnavailableCard />
                </div>
                <div className="interpretation">
                  <CircleHelp size={18} />
                  <p><strong>Como ler:</strong> o percentil usa a parcela com renda estritamente menor; o TOP é seu complemento. Empates permanecem no mesmo degrau da distribuição.</p>
                </div>
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
              <strong>PNAD 2025</strong>
              <small>pessoas elegíveis, ponderadas por V1032</small>
            </article>
            <article className="accent">
              <span>R$</span>
              <p>Referência monetária da comparação</p>
              <strong>2025</strong>
              <small>preços médios do ano</small>
            </article>
            <article>
              <span>MUNDO</span>
              <p>Resultado global</p>
              <strong>Em validação</strong>
              <small>sem número provisório nesta versão</small>
            </article>
          </div>
        </section>

        <section className="methodology" id="metodologia">
          <div className="method-title">
            <div className="section-label">METODOLOGIA</div>
            <h2>Sem falsa precisão.</h2>
            <button type="button" onClick={() => setShowMethod((value) => !value)} aria-expanded={showMethod}>
              {showMethod ? 'Ocultar detalhes' : 'Ver os detalhes'} <Plus size={18} />
            </button>
          </div>
          <div className="method-summary">
            <div><Check size={17} /><p><strong>Primeiro</strong> alinhamos a renda nominal atual aos preços médios de 2025 pelo IPCA.</p></div>
            <div><Check size={17} /><p><strong>Depois</strong> dividimos a renda comparável pelo número inteiro de moradores.</p></div>
            <div><Check size={17} /><p><strong>Por fim</strong> consultamos a CDF empírica brasileira, sem interpolação.</p></div>
          </div>
          {showMethod && (
            <div className="method-details">
              <p>A distribuição usa a PNAD Contínua 2025. O RDPC é construído pela soma domiciliar de VD4019 × CO1 e VD4048 × CO1e, dividida por VD2003, com peso V1032 e unidade final de pessoas elegíveis.</p>
              <p>A renda informada é convertida de julho de 2026 para preços médios de 2025 antes da consulta. A CDF é observada em degraus: não há interpolação nem extrapolação acima do máximo. A comparação mundial permanece bloqueada até a validação de fonte, conversão e caudas.</p>
            </div>
          )}
        </section>

        <section className="sources">
          <div>
            <div className="section-label">FONTES CONSULTADAS</div>
            <h2>Dados públicos.<br />Limites visíveis.</h2>
          </div>
          <div className="source-list">
            <a href="https://www.ibge.gov.br/estatisticas/sociais/populacao/17270-pnad-continua.html" target="_blank" rel="noreferrer">
              <span><strong>IBGE — PNAD Contínua</strong><small>Microdados anuais de 2025</small></span>
              <ArrowUpRight size={19} />
            </a>
            <a href="https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2266/p/202501-202607?formato=json" target="_blank" rel="noreferrer">
              <span><strong>IBGE — SIDRA</strong><small>IPCA, números-índice mensais usados no alinhamento</small></span>
              <ArrowUpRight size={19} />
            </a>
            <a href="https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf" target="_blank" rel="noreferrer">
              <span><strong>IBGE — Rendimento de todas as fontes</strong><small>Informativo da PNAD Contínua 2025</small></span>
              <ArrowUpRight size={19} />
            </a>
          </div>
        </section>
      </main>

      <footer>
        <div className="brand footer-brand">
          <span className="brand-mark"><i /><i /></span>
          <span>RENDA<br />EM DUAS ESCALAS</span>
        </div>
        <p>Ferramenta educativa. Não é aconselhamento financeiro, econômico ou tributário.</p>
        <a href="#top">Voltar ao topo <ArrowUpRight size={15} /></a>
      </footer>
    </div>
  )
}

export default App
