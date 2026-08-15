import assert from 'node:assert/strict'
import test from 'node:test'
import {
  calculateBrazilIncomePosition,
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
  assert.equal(formatBrazilPosition(zero).kind, 'zero')

  const maximum = calculateBrazilIncomePosition(runtime, 40, 1)
  assert.equal(maximum.comparableRdpc, 20)
  assert.equal(maximum.shareBelow, 0.5)
  assert.equal(maximum.shareAtOrBelow, 1)
  assert.equal(maximum.isAboveMaximum, false)

  const above = calculateBrazilIncomePosition(runtime, 42, 1)
  assert.equal(above.shareBelow, 1)
  assert.equal(above.shareAtOrBelow, 1)
  assert.equal(above.isAboveMaximum, true)
  assert.equal(formatBrazilPosition(above).kind, 'above-maximum')
  assert.equal(formatBrazilPosition(above).topLabel, null)
})

test('aplica as faixas visuais da D071 sem exibir TOP 0%', () => {
  const base = calculateBrazilIncomePosition(runtime, 40, 2)
  assert.equal(formatBrazilPosition(base).topLabel, 'TOP 80%')

  const upperTail = formatBrazilPosition({ ...base, shareBelow: 0.994, topShare: 0.006 })
  assert.equal(upperTail.topLabel, 'TOP 0,6%')

  const extremeTail = formatBrazilPosition({ ...base, shareBelow: 0.9995, topShare: 0.0005 })
  assert.equal(extremeTail.topLabel, 'TOP < 0,1%')
  assert.doesNotMatch(extremeTail.topLabel ?? '', /TOP 0%/)
})
