export type CurrencyParseResult =
  | { ok: true; value: number }
  | { ok: false; reason: 'empty' | 'invalid' | 'negative' };

export type HouseholdSizeParseResult =
  | { ok: true; value: number }
  | { ok: false; reason: 'empty' | 'invalid' };

export interface BrazilIncomeRuntime {
  engineVersion: string;
  priceReference: string;
  referenceMonth: string;
  multiplierCurrentToBase: number;
  cdf: {
    rdpc: Float64Array;
    cumulativeWeightAtOrBelow: Float64Array;
    totalWeight: number;
    maxRdpc: number;
  };
}

export interface BrazilIncomePosition {
  nominalHouseholdIncome: number;
  householdSize: number;
  nominalRdpc: number;
  comparableHouseholdIncome: number;
  comparableRdpc: number;
  shareBelow: number;
  shareAtOrBelow: number;
  topShare: number;
  isAboveMaximum: boolean;
}

export type BrazilPositionDisplay =
  | {
      kind: 'standard' | 'upper-tail';
      topLabel: string;
      percentileLabel: string;
      interpretation: string;
      markerPercent: number;
    }
  | {
      kind: 'zero';
      topLabel: null;
      percentileLabel: string;
      interpretation: string;
      markerPercent: 0;
    }
  | {
      kind: 'above-maximum';
      topLabel: null;
      percentileLabel: string;
      interpretation: string;
      markerPercent: null;
    };

function parseSeparatedNumber(value: string): number | null {
  const commaCount = (value.match(/,/g) ?? []).length;
  const dotCount = (value.match(/\./g) ?? []).length;

  if (commaCount > 0 && dotCount > 0) {
    const decimalSeparator = value.lastIndexOf(',') > value.lastIndexOf('.') ? ',' : '.';
    const thousandsSeparator = decimalSeparator === ',' ? '.' : ',';
    const parts = value.split(decimalSeparator);

    if (parts.length !== 2 || !/^\d{1,2}$/.test(parts[1])) return null;

    const integerGroups = parts[0].split(thousandsSeparator);
    if (
      integerGroups.length < 2 ||
      !/^\d{1,3}$/.test(integerGroups[0]) ||
      integerGroups.slice(1).some((group) => !/^\d{3}$/.test(group))
    ) {
      return null;
    }

    return Number(`${integerGroups.join('')}.${parts[1]}`);
  }

  if (commaCount > 0) {
    if (commaCount !== 1) return null;
    const parts = value.split(',');
    if (!/^\d+$/.test(parts[0]) || !/^\d{1,2}$/.test(parts[1])) return null;
    return Number(`${parts[0]}.${parts[1]}`);
  }

  if (dotCount > 0) {
    const parts = value.split('.');

    if (dotCount === 1 && /^\d+$/.test(parts[0]) && /^\d{1,2}$/.test(parts[1])) {
      return Number(`${parts[0]}.${parts[1]}`);
    }

    if (
      /^\d{1,3}$/.test(parts[0]) &&
      parts.length >= 2 &&
      parts.slice(1).every((group) => /^\d{3}$/.test(group))
    ) {
      return Number(parts.join(''));
    }

    return null;
  }

  return /^\d+$/.test(value) ? Number(value) : null;
}

export function parseBrazilianCurrency(input: string): CurrencyParseResult {
  const normalized = input
    .trim()
    .replace(/^R\$\s*/i, '')
    .replace(/\s+/g, '');

  if (!normalized) return { ok: false, reason: 'empty' };
  if (normalized.startsWith('-')) return { ok: false, reason: 'negative' };
  if (!/^[0-9.,]+$/.test(normalized)) return { ok: false, reason: 'invalid' };

  const parsed = parseSeparatedNumber(normalized);
  if (parsed === null || !Number.isFinite(parsed) || parsed < 0) {
    return { ok: false, reason: 'invalid' };
  }

  return { ok: true, value: parsed };
}

export function parseHouseholdSize(input: string): HouseholdSizeParseResult {
  const normalized = input.trim();
  if (!normalized) return { ok: false, reason: 'empty' };
  if (!/^\d+$/.test(normalized)) return { ok: false, reason: 'invalid' };

  const value = Number(normalized);
  if (!Number.isSafeInteger(value) || value < 1) {
    return { ok: false, reason: 'invalid' };
  }

  return { ok: true, value };
}

function firstIndexGreaterThan(values: Float64Array, target: number): number {
  let low = 0;
  let high = values.length;

  while (low < high) {
    const middle = low + Math.floor((high - low) / 2);
    if (values[middle] <= target) low = middle + 1;
    else high = middle;
  }

  return low;
}

function firstIndexAtLeast(values: Float64Array, target: number): number {
  let low = 0;
  let high = values.length;

  while (low < high) {
    const middle = low + Math.floor((high - low) / 2);
    if (values[middle] < target) low = middle + 1;
    else high = middle;
  }

  return low;
}

export function calculateBrazilIncomePosition(
  runtime: BrazilIncomeRuntime,
  nominalHouseholdIncome: number,
  householdSize: number,
): BrazilIncomePosition {
  if (!Number.isFinite(nominalHouseholdIncome) || nominalHouseholdIncome < 0) {
    throw new RangeError('A renda domiciliar deve ser um número finito não negativo.');
  }
  if (!Number.isSafeInteger(householdSize) || householdSize < 1) {
    throw new RangeError('O número de moradores deve ser um inteiro positivo.');
  }

  const comparableHouseholdIncome = nominalHouseholdIncome * runtime.multiplierCurrentToBase;
  const comparableRdpc = comparableHouseholdIncome / householdSize;
  const insertionIndex = firstIndexGreaterThan(runtime.cdf.rdpc, comparableRdpc);
  const lastAtOrBelow = insertionIndex - 1;
  const firstEqual = firstIndexAtLeast(runtime.cdf.rdpc, comparableRdpc);

  const cumulativeBelow = firstEqual > 0 ? runtime.cdf.cumulativeWeightAtOrBelow[firstEqual - 1] : 0;
  const cumulativeAtOrBelow =
    lastAtOrBelow >= 0 ? runtime.cdf.cumulativeWeightAtOrBelow[lastAtOrBelow] : 0;
  const shareBelow = cumulativeBelow / runtime.cdf.totalWeight;
  const shareAtOrBelow = cumulativeAtOrBelow / runtime.cdf.totalWeight;

  return {
    nominalHouseholdIncome,
    householdSize,
    nominalRdpc: nominalHouseholdIncome / householdSize,
    comparableHouseholdIncome,
    comparableRdpc,
    shareBelow,
    shareAtOrBelow,
    topShare: 1 - shareBelow,
    isAboveMaximum: comparableRdpc > runtime.cdf.maxRdpc,
  };
}

function formatPt(value: number, maximumFractionDigits: number): string {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: maximumFractionDigits,
    maximumFractionDigits,
  }).format(value);
}

export function formatBrazilPosition(position: BrazilIncomePosition): BrazilPositionDisplay {
  if (position.isAboveMaximum) {
    return {
      kind: 'above-maximum',
      topLabel: null,
      percentileLabel: 'Acima do maior valor observado na amostra',
      interpretation: 'A base não permite extrapolar uma posição numérica além desse ponto.',
      markerPercent: null,
    };
  }

  if (position.comparableRdpc === 0) {
    return {
      kind: 'zero',
      topLabel: null,
      percentileLabel: 'Renda per capita igual a zero',
      interpretation: 'A posição é apresentada sem o rótulo “TOP 100%”, que seria enganoso.',
      markerPercent: 0,
    };
  }

  const percentile = position.shareBelow * 100;
  const top = position.topShare * 100;

  if (top < 0.1) {
    return {
      kind: 'upper-tail',
      topLabel: 'TOP < 0,1%',
      percentileLabel: 'Acima do percentil 99,9',
      interpretation: 'Sua renda está na cauda superior observada, sem sugerir precisão além da base.',
      markerPercent: Math.min(100, percentile),
    };
  }

  if (top < 1) {
    return {
      kind: 'upper-tail',
      topLabel: `TOP ${formatPt(top, 1)}%`,
      percentileLabel: `Percentil ${formatPt(percentile, 1)}`,
      interpretation: `Sua renda é maior que a de aproximadamente ${formatPt(percentile, 1)}% das pessoas elegíveis.`,
      markerPercent: Math.min(100, percentile),
    };
  }

  const roundedPercentile = Math.round(percentile);
  const roundedTop = 100 - roundedPercentile;
  return {
    kind: 'standard',
    topLabel: `TOP ${roundedTop}%`,
    percentileLabel: `Percentil ${roundedPercentile}`,
    interpretation: `Sua renda é maior que a de aproximadamente ${roundedPercentile}% das pessoas elegíveis.`,
    markerPercent: Math.min(100, percentile),
  };
}
