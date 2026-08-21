import assert from 'node:assert/strict'
import test from 'node:test'
import {
  calculateBrazilIncomePosition,
  clampVisualMarkerPercent,
  formatBrazilPosition,
  parseBrazilianCurrency,
  parseHouseholdSize,
  type BrazilIncomeRuntime,
} from '../../src/brazil/domain.ts'

const runtime: BrazilIncomeRuntime = {
  engineVersion: 'test',
  priceReference: 'preços médios de 2025',
  referenceMonth: '2026-07',
  multiplierCurrentToBase: 0.5,
  cdf: {
    rdpc: Float64Array.from([0, 10, 20]),
    cumulativeWeightAtOrBelow: Float64Array.from([2, 5, 10]),
    totalWeight: 10,
    maxRdpc: 20,
  },
}

test('interpreta moeda brasileira e evita o bug 6500.50 → 650050', () => {
  const cases: Array<[string, number]> = [
    ['6500.50', 6500.5],
    ['6.500', 6500],
    ['6.500,50', 6500.5],
    ['R$ 6.500,50', 6500.5],
    ['1,25', 1.25],
    ['0', 0],
  ]

  for (const [input, expected] of cases) {
    const parsed = parseBrazilianCurrency(input)
    assert.equal(parsed.ok, true, input)
    if (parsed.ok) assert.equal(parsed.value, expected, input)
  }

  for (const input of ['', '-1', '6x500', '1,234', '6500.500', '1.2.3,45']) {
    assert.equal(parseBrazilianCurrency(input).ok, false, input)
  }
})

test('aceita somente moradores inteiros positivos', () => {
  for (const [input, expected] of [['1', 1], ['3', 3], ['100', 100]] as const) {
    assert.deepEqual(parseHouseholdSize(input), { ok: true, value: expected })
  }

  for (const input of ['', '0', '-1', '2.5', '2,5', 'abc']) {
    assert.equal(parseHouseholdSize(input).ok, false, input)
  }
})

test('aplica alinhamento D065 antes do RDPC e consulta a CDF em degraus', () => {
  const result = calculateBrazilIncomePosition(runtime, 40, 2)

  assert.equal(result.nominalRdpc, 20)
  assert.equal(result.comparableHouseholdIncome, 20)
  assert.equal(result.comparableRdpc, 10)
  assert.equal(result.shareBelow, 0.2)
  assert.equal(result.shareAtOrBelow, 0.5)
  assert.equal(result.topShare, 0.8)
})

test('preserva empate, renda zero, máximo e acima do máximo', () => {
  const zero = calculateBrazilIncomePosition(runtime, 0, 1)
  assert.equal(zero.shareBelow, 0)
  assert.equal(zero.shareAtOrBelow, 0.2)
  const zeroDisplay = formatBrazilPosition(zero)
  assert.equal(zeroDisplay.kind, 'zero')
  assert.equal(
    zeroDisplay.interpretation,
    'R$ 0 é o menor nível de renda por pessoa observado na distribuição utilizada e há outras pessoas empatadas nesse valor.',
  )

  const maximum = calculateBrazilIncomePosition(runtime, 40, 1)
  assert.equal(maximum.comparableRdpc, 20)
  assert.equal(maximum.shareBelow, 0.5)
  assert.equal(maximum.shareAtOrBelow, 1)
  assert.equal(maximum.isAboveMaximum, false)

  const above = calculateBrazilIncomePosition(runtime, 42, 1)
  assert.equal(above.shareBelow, 1)
  assert.equal(above.shareAtOrBelow, 1)
  assert.equal(above.isAboveMaximum, true)
  const aboveDisplay = formatBrazilPosition(above)
  assert.equal(aboveDisplay.kind, 'above-maximum')
  assert.equal(aboveDisplay.topLabel, null)
  assert.equal(
    aboveDisplay.interpretation,
    'Sua renda por pessoa está acima do maior valor observado na distribuição da PNAD 2025 utilizada. A pesquisa não permite estimar com segurança uma posição mais fina nessa cauda.',
  )
})

test('aplica as fronteiras visuais da D071 sem arredondar a estatística interna', () => {
  const base = calculateBrazilIncomePosition(runtime, 40, 2)
  const cases = [
    { topShare: 0.02, topLabel: 'TOP 2%', percentileLabel: 'Percentil 98' },
    { topShare: 0.01, topLabel: 'TOP 1%', percentileLabel: 'Percentil 99' },
    { topShare: 0.009999, topLabel: 'TOP 1,0%', percentileLabel: 'Percentil 99,0' },
    { topShare: 0.006, topLabel: 'TOP 0,6%', percentileLabel: 'Percentil 99,4' },
    { topShare: 0.001, topLabel: 'TOP 0,1%', percentileLabel: 'Percentil 99,9' },
    {
      topShare: 0.000999,
      topLabel: 'TOP < 0,1%',
      percentileLabel: 'Acima do percentil 99,9',
      interpretation: 'Entre menos de 0,1% de maior renda na distribuição observada.',
    },
    {
      topShare: 0.0005,
      topLabel: 'TOP < 0,1%',
      percentileLabel: 'Acima do percentil 99,9',
      interpretation: 'Entre menos de 0,1% de maior renda na distribuição observada.',
    },
  ] as const

  for (const expected of cases) {
    const display = formatBrazilPosition({
      ...base,
      shareBelow: 1 - expected.topShare,
      topShare: expected.topShare,
    })
    assert.equal(display.topLabel, expected.topLabel, String(expected.topShare))
    assert.equal(display.percentileLabel, expected.percentileLabel, String(expected.topShare))
    if ('interpretation' in expected) {
      assert.equal(display.interpretation, expected.interpretation, String(expected.topShare))
    }
    assert.doesNotMatch(display.topLabel ?? '', /TOP 0%/, String(expected.topShare))
  }
})

test('a geometria preserva posições legítimas acima de 99,7% e limita somente a barra física', () => {
  const base = calculateBrazilIncomePosition(runtime, 40, 2)
  const position = { ...base, shareBelow: 0.9998, topShare: 0.0002 }
  const display = formatBrazilPosition(position)

  assert.equal(position.shareBelow, 0.9998)
  assert.equal(position.topShare, 0.0002)
  assert.equal(display.markerPercent, 99.98)
  assert.equal(clampVisualMarkerPercent(display.markerPercent), 99.98)
  assert.notEqual(clampVisualMarkerPercent(display.markerPercent), 99.7)
  assert.equal(clampVisualMarkerPercent(-0.01), 0)
  assert.equal(clampVisualMarkerPercent(100.01), 100)
})
