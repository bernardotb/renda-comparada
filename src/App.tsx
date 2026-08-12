import { useMemo, useState } from 'react'
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

const BRAZIL_THRESHOLDS = [
  1.8079, 2.4714, 2.9975, 3.3899, 3.7577, 4.1338, 4.4897, 4.8073, 5.0882, 5.3792,
  5.6662, 6.0001, 6.2859, 6.5716, 6.8089, 7.066, 7.3261, 7.5896, 7.8379, 8.0757,
  8.4068, 8.6917, 8.9526, 9.2059, 9.4631, 9.7109, 9.9535, 10.1922, 10.4252, 10.6553,
  10.927, 11.193, 11.4389, 11.7423, 12.0468, 12.3373, 12.6227, 12.8975, 13.174, 13.4509,
  13.787, 14.1229, 14.4461, 14.8083, 15.1427, 15.4935, 15.8272, 16.1043, 16.5034, 16.9121,
  17.2854, 17.6767, 18.0757, 18.4447, 18.8328, 19.1838, 19.5563, 19.9203, 20.2813, 20.6397,
  21.0539, 21.4833, 21.9421, 22.385, 22.8038, 23.275, 23.83, 24.4328, 25.0793, 25.7432,
  26.4562, 27.1912, 27.8797, 28.6073, 29.5044, 30.432, 31.2852, 32.2751, 33.2885, 34.3595,
  35.8186, 37.1506, 38.7378, 40.275, 41.9058, 43.8106, 45.6599, 47.9562, 50.6956, 54.1986,
  57.8693, 62.394, 67.4786, 73.406, 80.8134, 90.3982, 103.957, 126.2317, 173.5652,
]

const WORLD_CURVE: Array<[number, number]> = [
  [0.5, 0.25], [0.75, 0.62], [1, 1.16], [1.5, 2.74], [2, 4.85], [3, 10.4],
  [4, 17.41], [5, 25.27], [6, 32.92], [8, 44.67], [10, 52.69], [12, 58.57],
  [15, 65.03], [20, 72.32], [25, 77.18], [30, 80.64], [40, 85.49], [50, 88.89],
  [70, 93.31], [100, 96.68], [150, 98.76], [200, 99.43], [500, 99.96],
  [800, 99.99], [1200, 100],
]

const PPP_2021_BRL = 2.4499
const BRAZIL_CPI_2024 = 1.1929
const BRL_PER_INTL_2024 = PPP_2021_BRL * BRAZIL_CPI_2024
const DAYS_PER_MONTH = 365 / 12
const BRAZIL_POPULATION = 211_998_573
const WORLD_POPULATION = 8_141_808_945

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value))
}

function interpolateLog(x: number, x1: number, y1: number, x2: number, y2: number) {
  if (x1 <= 0 || x2 <= 0 || x <= 0 || x1 === x2) return y1
  const t = (Math.log(x) - Math.log(x1)) / (Math.log(x2) - Math.log(x1))
  return y1 + clamp(t, 0, 1) * (y2 - y1)
}

function brazilPercentile(dailyIntl: number) {
  if (dailyIntl <= BRAZIL_THRESHOLDS[0]) {
    return clamp((dailyIntl / BRAZIL_THRESHOLDS[0]) * 1, 0.1, 1)
  }

  for (let i = 1; i < BRAZIL_THRESHOLDS.length; i += 1) {
    if (dailyIntl <= BRAZIL_THRESHOLDS[i]) {
      return interpolateLog(
        dailyIntl,
        BRAZIL_THRESHOLDS[i - 1],
        i,
        BRAZIL_THRESHOLDS[i],
        i + 1,
      )
    }
  }

  return clamp(99 + Math.log(dailyIntl / BRAZIL_THRESHOLDS.at(-1)!) / Math.log(8), 99, 99.9)
}

function worldPercentile(dailyIntl: number) {
  if (dailyIntl <= WORLD_CURVE[0][0]) {
    return clamp((dailyIntl / WORLD_CURVE[0][0]) * WORLD_CURVE[0][1], 0.1, WORLD_CURVE[0][1])
  }

  for (let i = 1; i < WORLD_CURVE.length; i += 1) {
    if (dailyIntl <= WORLD_CURVE[i][0]) {
      return interpolateLog(
        dailyIntl,
        WORLD_CURVE[i - 1][0],
        WORLD_CURVE[i - 1][1],
        WORLD_CURVE[i][0],
        WORLD_CURVE[i][1],
      )
    }
  }
  return 99.99
}

function money(value: number) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 0,
  }).format(value)
}

function compact(value: number) {
  return new Intl.NumberFormat('pt-BR', {
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(value)
}

function decimal(value: number, digits = 1) {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  }).format(value)
}

function readCurrency(value: string) {
  const numeric = Number(value.replace(/\D/g, ''))
  return Number.isFinite(numeric) ? numeric : 0
}

function positionLabel(percentile: number) {
  const top = 100 - percentile
  if (top < 0.1) return 'entre o 0,1% de maior renda'
  if (top < 1) return `entre o ${decimal(top, 1)}% de maior renda`
  return `entre os ${decimal(top, top < 10 ? 1 : 0)}% de maior renda`
}

type ResultCardProps = {
  kind: 'brasil' | 'mundo'
  percentile: number
  population: number
}

function ResultCard({ kind, percentile, population }: ResultCardProps) {
  const isBrazil = kind === 'brasil'
  const Icon = isBrazil ? Sparkles : Globe2
  const top = Math.max(0.01, 100 - percentile)
  const peopleAhead = Math.max(1, Math.round((top / 100) * population))

  return (
    <article className={`result-card ${kind}`}>
      <div className="result-head">
        <span className="result-icon"><Icon size={20} strokeWidth={1.8} /></span>
        <span>{isBrazil ? 'No Brasil' : 'No mundo'}</span>
      </div>
      <p className="eyebrow">Sua renda por pessoa é maior que a de</p>
      <div className="percentile-number">
        <strong>{decimal(percentile, 1)}</strong><span>%</span>
      </div>
      <div className="result-ruler" aria-label={`Percentil ${decimal(percentile, 1)}`}>
        <span style={{ width: `${clamp(percentile, 1, 99.7)}%` }} />
        <i style={{ left: `${clamp(percentile, 1, 99.7)}%` }} />
      </div>
      <p className="position-label">Você está {positionLabel(percentile)}.</p>
      <p className="rank-note">Cerca de {compact(peopleAhead)} pessoas estão acima nesta régua.</p>
    </article>
  )
}

function App() {
  const [income, setIncome] = useState(12000)
  const [household, setHousehold] = useState(3)
  const [showMethod, setShowMethod] = useState(false)

  const result = useMemo(() => {
    const perPerson = income / Math.max(1, household)
    const dailyIntl = perPerson / BRL_PER_INTL_2024 / DAYS_PER_MONTH
    return {
      perPerson,
      dailyIntl,
      brazil: brazilPercentile(dailyIntl),
      world: worldPercentile(dailyIntl),
    }
  }, [income, household])

  const handleIncome = (value: string) => setIncome(clamp(readCurrency(value), 0, 100_000_000))
  const inputDisplay = new Intl.NumberFormat('pt-BR').format(income)
  const worldMedianBrl = 277.4407 * BRL_PER_INTL_2024
  const brazilMedianBrl = 16.9121 * DAYS_PER_MONTH * BRL_PER_INTL_2024

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
            <div className="kicker"><span /> Brasil + mundo</div>
            <h1><span>Ranking de renda familiar</span><br /><em>no Brasil e no mundo.</em></h1>
            <p>Informe a renda da sua casa e veja sua posição.</p>
          </div>
          <aside className="hero-note">
            <span>01</span>
            <p>Não mede riqueza.<br />Considera a renda total da família<br />e quantas pessoas vivem dela.</p>
          </aside>
        </section>

        <section className="calculator" aria-label="Calculadora de posição de renda">
          <div className="form-panel">
            <div className="panel-heading">
              <span>SEUS DADOS</span>
              <small>Valores de 2024</small>
            </div>

            <label className="field-label income-label" htmlFor="income">Renda mensal da casa</label>
            <div className="money-input-wrap">
              <span>R$</span>
              <input
                id="income"
                inputMode="numeric"
                value={inputDisplay}
                onChange={(event) => handleIncome(event.target.value)}
                aria-describedby="income-help"
              />
            </div>
            <p className="field-help" id="income-help">Some salários e outras rendas regulares de quem mora com você.</p>

            <div className="household-row">
              <div>
                <label className="field-label" htmlFor="household">Pessoas sustentadas por essa renda</label>
                <p className="field-help">Inclua adultos e crianças.</p>
              </div>
              <div className="stepper">
                <button type="button" onClick={() => setHousehold((value) => Math.max(1, value - 1))} aria-label="Diminuir número de pessoas">
                  <Minus size={18} />
                </button>
                <input
                  id="household"
                  type="number"
                  min="1"
                  max="30"
                  value={household}
                  onChange={(event) => setHousehold(clamp(Number(event.target.value) || 1, 1, 30))}
                  aria-label="Número de pessoas"
                />
                <button type="button" onClick={() => setHousehold((value) => Math.min(30, value + 1))} aria-label="Aumentar número de pessoas">
                  <Plus size={18} />
                </button>
              </div>
            </div>

            <div className="per-capita-strip">
              <span>Renda mensal por pessoa</span>
              <strong>{money(result.perPerson)}</strong>
            </div>
            <div className="privacy-note"><ShieldCheck size={15} /><span>O cálculo acontece no seu navegador. Nenhum dado é enviado.</span></div>
          </div>

          <div className="results-panel" aria-live="polite">
            <div className="panel-heading light">
              <span>SUA POSIÇÃO ESTIMADA</span>
              <small>Base 2024</small>
            </div>
            <div className="results-grid">
              <ResultCard kind="brasil" percentile={result.brazil} population={BRAZIL_POPULATION} />
              <ResultCard kind="mundo" percentile={result.world} population={WORLD_POPULATION} />
            </div>
            <div className="interpretation">
              <CircleHelp size={18} />
              <p><strong>Como ler:</strong> percentil 80 significa que a renda por pessoa supera a de aproximadamente 80 em cada 100 pessoas daquela população.</p>
            </div>
          </div>
        </section>

        <section className="benchmarks" aria-labelledby="benchmarks-title">
          <div className="section-label">PARA DAR CONTEXTO</div>
          <div className="benchmark-intro">
            <h2 id="benchmarks-title">Números sozinhos<br />não contam a história.</h2>
            <p>A mesma renda sustenta vidas diferentes conforme cidade, moradia, saúde, dívidas e patrimônio. Estas referências mostram apenas a distribuição estatística.</p>
          </div>
          <div className="benchmark-grid">
            <article>
              <span>50º</span>
              <p>Mediana brasileira do modelo</p>
              <strong>{money(brazilMedianBrl)}</strong>
              <small>por pessoa/mês</small>
            </article>
            <article className="accent">
              <span>R$</span>
              <p>Média brasileira segundo o IBGE</p>
              <strong>R$ 2.069</strong>
              <small>por pessoa/mês em 2024</small>
            </article>
            <article>
              <span>50º</span>
              <p>Mediana mundial em poder de compra brasileiro</p>
              <strong>{money(worldMedianBrl)}</strong>
              <small>por pessoa/mês</small>
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
            <div><Check size={17} /><p><strong>Primeiro</strong> dividimos a renda pelo número de pessoas da casa.</p></div>
            <div><Check size={17} /><p><strong>Depois</strong> convertemos reais para dólares internacionais de 2021 por PPC.</p></div>
            <div><Check size={17} /><p><strong>Por fim</strong> interpolamos sua posição nas distribuições de Brasil e mundo.</p></div>
          </div>
          {showMethod && (
            <div className="method-details">
              <p>A base brasileira usa os 100 percentis da distribuição nacional de renda da PNAD Contínua 2024, harmonizados pela plataforma PIP do Banco Mundial. A base mundial usa a distribuição global alinhada para 2024. Os valores internacionais são ajustados por paridade de poder de compra (PPC 2021).</p>
              <p>O resultado é uma estimativa: pesquisas domiciliares podem sub-representar rendas muito altas, diferentes países medem renda ou consumo, e uma única PPC nacional não capta diferenças regionais de custo de vida. O número de pessoas “acima” é apenas uma tradução aproximada do percentil.</p>
            </div>
          )}
        </section>

        <section className="sources">
          <div>
            <div className="section-label">FONTES CONSULTADAS</div>
            <h2>Dados públicos.<br />Limites visíveis.</h2>
          </div>
          <div className="source-list">
            <a href="https://pip.worldbank.org/" target="_blank" rel="noreferrer">
              <span><strong>Banco Mundial — PIP</strong><small>Distribuições de renda, versão 24/03/2026</small></span>
              <ArrowUpRight size={19} />
            </a>
            <a href="https://ourworldindata.org/grapher/incomes-across-distribution-wb" target="_blank" rel="noreferrer">
              <span><strong>Our World in Data</strong><small>Limiares da distribuição mundial, ano 2024</small></span>
              <ArrowUpRight size={19} />
            </a>
            <a href="https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/42761-ibge-divulga-rendimento-domiciliar-per-capita-2024-para-brasil-e-unidades-da-federacao" target="_blank" rel="noreferrer">
              <span><strong>IBGE — PNAD Contínua</strong><small>Rendimento domiciliar per capita, ano 2024</small></span>
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
