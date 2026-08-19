export type WorldInputValidation =
  | { ok: true; householdIncome: number; residents: number }
  | { ok: false; reason: 'income-not-finite' | 'income-negative' | 'residents-not-integer' | 'residents-nonpositive' };

export type WorldSupportStatus =
  | 'below-minimum'
  | 'at-minimum'
  | 'inside'
  | 'at-maximum'
  | 'above-maximum';

export interface WorldIncomeRuntime {
  engineVersion: string;
  methodologyVersion: string;
  pipVersion: string;
  productionBuild: string;
  referenceYear: 2024;
  pppBase: 2021;
  priceReferenceMonth: string;
  baseIndex: number;
  currentIndex: number;
  brazilPipPpp2021: number;
  brazilPipCpi2024Base2021: number;
  brlPerIntl2024Derived: number;
  maxAbsoluteErrorPp: number;
  cdf: {
    welfare: Float64Array;
    cumulativePopulationAtOrBelow: Float64Array;
    totalPopulationMillions: number;
    minWelfare: number;
    maxWelfare: number;
  };
}

export interface WorldIncomeLookup {
  internationalPppDaily: number;
  shareBelow: number;
  shareAtOrBelow: number;
  topShare: number;
  supportStatus: WorldSupportStatus;
}

export type WorldPresentation =
  | { kind: 'outside-lower-support' | 'outside-upper-support'; headline: string; extrapolated: false }
  | { kind: 'at-minimum'; headline: string; extrapolated: false }
  | { kind: 'main'; percentileDisplay: number; topDisplayPp: number; extrapolated: false }
  | { kind: 'upper-tail'; topDisplayPp: number; extrapolated: false }
  | { kind: 'upper-extreme'; headline: 'menos de 0,1%' | 'aproximadamente 0,1%'; extrapolated: false }
  | { kind: 'upper-support-limit'; headline: string; extrapolated: false };

export interface WorldIncomePosition extends WorldIncomeLookup {
  nominalHouseholdIncome: number;
  residents: number;
  nominalIncomePerPersonMonthly: number;
  comparableIncomePerPersonMonthly2024: number;
  presentation: WorldPresentation;
  language: 'posição monetária global estimada';
}

export function validateWorldInputs(householdIncome: number, residents: number): WorldInputValidation {
  if (!Number.isFinite(householdIncome)) return { ok: false, reason: 'income-not-finite' };
  if (householdIncome < 0) return { ok: false, reason: 'income-negative' };
  if (!Number.isSafeInteger(residents)) return { ok: false, reason: 'residents-not-integer' };
  if (residents <= 0) return { ok: false, reason: 'residents-nonpositive' };
  return { ok: true, householdIncome, residents };
}

export function nominalHouseholdIncomeToInternationalPppDaily(
  runtime: WorldIncomeRuntime,
  householdIncome: number,
  residents: number,
): number {
  const validation = validateWorldInputs(householdIncome, residents);
  if (!validation.ok) throw new RangeError(`Entrada Mundo inválida: ${validation.reason}`);
  return (
    (householdIncome / residents)
    * (runtime.baseIndex / runtime.currentIndex)
    / runtime.brlPerIntl2024Derived
    * 12
    / 365
  );
}

export function internationalPppDailyToNominalHouseholdIncome(
  runtime: WorldIncomeRuntime,
  internationalPppDaily: number,
  residents: number,
): number {
  if (!Number.isFinite(internationalPppDaily) || internationalPppDaily < 0) {
    throw new RangeError('Valor PPP Mundo inválido.');
  }
  if (!Number.isSafeInteger(residents) || residents <= 0) {
    throw new RangeError('Moradores Mundo inválidos.');
  }
  return (
    internationalPppDaily
    * 365
    / 12
    * runtime.brlPerIntl2024Derived
    / (runtime.baseIndex / runtime.currentIndex)
    * residents
  );
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

export function lookupWorldIncome(runtime: WorldIncomeRuntime, internationalPppDaily: number): WorldIncomeLookup {
  if (!Number.isFinite(internationalPppDaily) || internationalPppDaily < 0) {
    throw new RangeError('Valor PPP Mundo inválido para lookup.');
  }
  const { welfare, cumulativePopulationAtOrBelow, totalPopulationMillions, minWelfare, maxWelfare } = runtime.cdf;
  const left = firstIndexAtLeast(welfare, internationalPppDaily);
  const right = firstIndexGreaterThan(welfare, internationalPppDaily);
  const belowPopulation = left === 0 ? 0 : cumulativePopulationAtOrBelow[left - 1];
  const atOrBelowPopulation = right === 0 ? 0 : cumulativePopulationAtOrBelow[right - 1];
  const shareBelow = belowPopulation / totalPopulationMillions;
  const shareAtOrBelow = atOrBelowPopulation / totalPopulationMillions;
  let supportStatus: WorldSupportStatus = 'inside';
  if (internationalPppDaily < minWelfare) supportStatus = 'below-minimum';
  else if (internationalPppDaily === minWelfare) supportStatus = 'at-minimum';
  else if (internationalPppDaily === maxWelfare) supportStatus = 'at-maximum';
  else if (internationalPppDaily > maxWelfare) supportStatus = 'above-maximum';
  return {
    internationalPppDaily,
    shareBelow,
    shareAtOrBelow,
    topShare: 1 - shareBelow,
    supportStatus,
  };
}

export function presentWorldPosition(
  topShare: number,
  maxAbsoluteErrorPp: number,
  supportStatus: WorldSupportStatus,
): WorldPresentation {
  if (!Number.isFinite(topShare) || topShare < 0 || topShare > 1) throw new RangeError('topShare Mundo inválido.');
  if (!Number.isFinite(maxAbsoluteErrorPp) || maxAbsoluteErrorPp < 0) throw new RangeError('Erro D068 inválido.');
  if (supportStatus === 'below-minimum') {
    return { kind: 'outside-lower-support', headline: 'fora do suporte inferior observado', extrapolated: false };
  }
  if (supportStatus === 'above-maximum') {
    return { kind: 'outside-upper-support', headline: 'fora do suporte superior observado', extrapolated: false };
  }
  if (supportStatus === 'at-minimum') {
    return { kind: 'at-minimum', headline: 'menor degrau observado; empates preservados', extrapolated: false };
  }
  const topPercent = topShare * 100;
  if (topPercent === 0) {
    return { kind: 'upper-support-limit', headline: 'limite superior observado; posição mais fina indisponível', extrapolated: false };
  }
  if (topPercent >= 1) {
    const percentileDisplay = Math.round(100 - topPercent);
    return { kind: 'main', percentileDisplay, topDisplayPp: 100 - percentileDisplay, extrapolated: false };
  }
  if (topPercent >= 0.1) {
    return { kind: 'upper-tail', topDisplayPp: Math.round(topPercent * 10) / 10, extrapolated: false };
  }
  return {
    kind: 'upper-extreme',
    headline: topPercent + maxAbsoluteErrorPp < 0.1 ? 'menos de 0,1%' : 'aproximadamente 0,1%',
    extrapolated: false,
  };
}

export function calculateWorldIncomePosition(
  runtime: WorldIncomeRuntime,
  householdIncome: number,
  residents: number,
): WorldIncomePosition {
  const internationalPppDaily = nominalHouseholdIncomeToInternationalPppDaily(runtime, householdIncome, residents);
  const lookup = lookupWorldIncome(runtime, internationalPppDaily);
  const nominalIncomePerPersonMonthly = householdIncome / residents;
  return {
    ...lookup,
    nominalHouseholdIncome: householdIncome,
    residents,
    nominalIncomePerPersonMonthly,
    comparableIncomePerPersonMonthly2024: nominalIncomePerPersonMonthly * (runtime.baseIndex / runtime.currentIndex),
    presentation: presentWorldPosition(lookup.topShare, runtime.maxAbsoluteErrorPp, lookup.supportStatus),
    language: 'posição monetária global estimada',
  };
}
