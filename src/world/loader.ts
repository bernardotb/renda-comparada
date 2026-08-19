import runtimeConfig from '../../config/world-frontend-runtime.json' with { type: 'json' };
import type { WorldIncomeRuntime } from './domain.ts';

interface ArtifactContract {
  path: string;
  schema: string;
  sha256: string;
  sizeBytes: number;
  version: string;
}

interface EngineManifest {
  schemaVersion: string;
  dataset: string;
  version: string;
  status: string;
  decisionIds: string[];
  artifacts: { cdf: ArtifactContract; priceAlignment: ArtifactContract; goldenCases: ArtifactContract };
  methodology: {
    version: string;
    pipVersion: string;
    productionBuild: string;
    referenceYear: number;
    pppBase: number;
    unit: string;
    lookup: { interpolation: string; extrapolation: string };
  };
  maxAbsoluteErrorPp: string;
  delivery: { legacyFallback: string; persistence: string };
  integration: { worldFrontendIntegrationAllowed: boolean };
}

interface PriceAlignment {
  schemaVersion: string;
  dataset: string;
  version: string;
  status: string;
  baseIndex: string;
  currentIndex: string;
  priceIndexReferenceMonth: string;
  pipVersion: string;
  productionBuild: string;
  referenceYear: number;
  pppBase: number;
  brazilPipPpp2021: string;
  brazilPipCpi2024Base2021: string;
  brlPerIntl2024Derived: string;
  combinedFactorState: string;
  integration: { worldFrontendIntegrationAllowed: boolean };
}

interface WorldCdfDocument {
  schemaVersion: string;
  dataset: string;
  version: string;
  status: string;
  methodology: {
    version: string;
    pipVersion: string;
    productionBuild: string;
    referenceYear: number;
    pppBase: number;
    interpolation: string;
    extrapolation: string;
  };
  statistics: { pointCount: number; totalPopulationMillions: string; minWelfare: string; maxWelfare: string };
  points: [string, string][];
  integration: { worldFrontendIntegrationAllowed: boolean };
}

export interface WorldRuntimeBootstrap {
  publicBasePath: string;
  engineManifest: { publicPath: string; sha256: string; sizeBytes?: number };
}

type Fetcher = (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>;

const defaultBootstrap = runtimeConfig as WorldRuntimeBootstrap;

function artifactPublicPath(basePath: string, repositoryPath: string): string {
  const filename = repositoryPath.replaceAll('\\', '/').split('/').at(-1);
  if (!filename) throw new Error('Caminho inválido de artefato Mundo.');
  return `${basePath.replace(/\/$/, '')}/${filename}`;
}

async function sha256Hex(bytes: ArrayBuffer): Promise<string> {
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('').toUpperCase();
}

async function fetchVerifiedJson<T>(
  fetcher: Fetcher,
  publicPath: string,
  expectedSha256: string,
  expectedBytes?: number,
): Promise<T> {
  const response = await fetcher(publicPath, { method: 'GET', credentials: 'same-origin', cache: 'default' });
  if (!response.ok) throw new Error(`Artefato Mundo indisponível: ${publicPath}`);
  const bytes = await response.arrayBuffer();
  if (expectedBytes !== undefined && bytes.byteLength !== expectedBytes) throw new Error(`Tamanho incompatível para ${publicPath}.`);
  if ((await sha256Hex(bytes)) !== expectedSha256.toUpperCase()) throw new Error(`SHA-256 incompatível para ${publicPath}.`);
  try {
    return JSON.parse(new TextDecoder().decode(bytes)) as T;
  } catch {
    throw new Error(`JSON inválido em ${publicPath}.`);
  }
}

function finitePositive(value: string): number {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed <= 0) throw new Error('Decimal Mundo inválido.');
  return parsed;
}

function assertManifest(value: EngineManifest): void {
  if (
    value.schemaVersion !== '1.0.0'
    || value.dataset !== 'world-income-engine'
    || value.version !== '1.0.0'
    || value.status !== 'CANONICAL_APPROVED_FOR_INTEGRATION'
    || value.integration?.worldFrontendIntegrationAllowed !== true
    || value.methodology?.version !== 'D066-D070-v1'
    || value.methodology?.pipVersion !== '20260324_2021'
    || value.methodology?.productionBuild !== '20260324_2021_01_02_PROD'
    || value.methodology?.referenceYear !== 2024
    || value.methodology?.pppBase !== 2021
    || value.methodology?.lookup?.interpolation !== 'none'
    || value.methodology?.lookup?.extrapolation !== 'none'
    || value.delivery?.legacyFallback !== 'forbidden'
    || value.delivery?.persistence !== 'none'
    || value.decisionIds?.join(',') !== 'D066,D067,D068,D069,D070'
  ) throw new Error('Manifesto Mundo incompatível ou indevidamente autorizado.');
  for (const artifact of Object.values(value.artifacts ?? {})) {
    if (!artifact?.path || !/^[A-F0-9]{64}$/i.test(artifact.sha256) || !Number.isSafeInteger(artifact.sizeBytes) || artifact.sizeBytes <= 0) {
      throw new Error('Referência de artefato Mundo inválida.');
    }
  }
}

function assertPrice(value: PriceAlignment, engine: EngineManifest): Omit<WorldIncomeRuntime, 'cdf'> {
  const ppp = finitePositive(value.brazilPipPpp2021);
  const cpi = finitePositive(value.brazilPipCpi2024Base2021);
  const derived = finitePositive(value.brlPerIntl2024Derived);
  if (
    value.schemaVersion !== '1.0.0'
    || value.dataset !== 'world-price-alignment'
    || value.version !== engine.artifacts.priceAlignment.version
    || value.status !== 'CANONICAL_PRODUCTION_FRONTEND_BLOCKED'
    || value.integration?.worldFrontendIntegrationAllowed !== false
    || value.pipVersion !== engine.methodology.pipVersion
    || value.productionBuild !== engine.methodology.productionBuild
    || value.referenceYear !== engine.methodology.referenceYear
    || value.pppBase !== engine.methodology.pppBase
    || value.combinedFactorState !== 'DERIVED'
    || Math.abs(ppp * cpi - derived) > Number.EPSILON * Math.max(1, derived) * 4
  ) throw new Error('Alinhamento Mundo incompatível com o manifesto.');
  return {
    engineVersion: engine.version,
    methodologyVersion: engine.methodology.version,
    pipVersion: engine.methodology.pipVersion,
    productionBuild: engine.methodology.productionBuild,
    referenceYear: 2024,
    pppBase: 2021,
    priceReferenceMonth: value.priceIndexReferenceMonth,
    baseIndex: finitePositive(value.baseIndex),
    currentIndex: finitePositive(value.currentIndex),
    brazilPipPpp2021: ppp,
    brazilPipCpi2024Base2021: cpi,
    brlPerIntl2024Derived: derived,
    maxAbsoluteErrorPp: finitePositive(engine.maxAbsoluteErrorPp),
  };
}

function compileCdf(value: WorldCdfDocument, engine: EngineManifest): WorldIncomeRuntime['cdf'] {
  if (
    value.schemaVersion !== '1.0.0'
    || value.dataset !== 'world-income-cdf'
    || value.version !== engine.artifacts.cdf.version
    || value.status !== 'CANONICAL_PRODUCTION_FRONTEND_BLOCKED'
    || value.integration?.worldFrontendIntegrationAllowed !== false
    || value.methodology?.version !== engine.methodology.version
    || value.methodology?.pipVersion !== engine.methodology.pipVersion
    || value.methodology?.productionBuild !== engine.methodology.productionBuild
    || value.methodology?.referenceYear !== engine.methodology.referenceYear
    || value.methodology?.pppBase !== engine.methodology.pppBase
    || value.methodology?.interpolation !== 'none'
    || value.methodology?.extrapolation !== 'none'
    || !Array.isArray(value.points)
    || value.points.length !== 216790
    || value.statistics?.pointCount !== value.points.length
  ) throw new Error('CDF Mundo incompatível com o manifesto.');
  const welfare = new Float64Array(value.points.length);
  const cumulativePopulationAtOrBelow = new Float64Array(value.points.length);
  let previousWelfare = Number.NEGATIVE_INFINITY;
  let previousCumulative = 0;
  for (let index = 0; index < value.points.length; index += 1) {
    const point = value.points[index];
    const currentWelfare = Number(point?.[0]);
    const currentCumulative = Number(point?.[1]);
    if (!Number.isFinite(currentWelfare) || currentWelfare < 0 || currentWelfare <= previousWelfare || !Number.isFinite(currentCumulative) || currentCumulative <= previousCumulative) {
      throw new Error(`CDF Mundo não monotônica no ponto ${index}.`);
    }
    welfare[index] = currentWelfare;
    cumulativePopulationAtOrBelow[index] = currentCumulative;
    previousWelfare = currentWelfare;
    previousCumulative = currentCumulative;
  }
  const totalPopulationMillions = finitePositive(value.statistics.totalPopulationMillions);
  const minWelfare = Number(value.statistics.minWelfare);
  const maxWelfare = finitePositive(value.statistics.maxWelfare);
  if (previousCumulative !== totalPopulationMillions || welfare[0] !== minWelfare || previousWelfare !== maxWelfare) {
    throw new Error('CDF Mundo não reconcilia suporte e população.');
  }
  return { welfare, cumulativePopulationAtOrBelow, totalPopulationMillions, minWelfare, maxWelfare };
}

export function createWorldEngineLoader(
  fetcher: Fetcher = globalThis.fetch.bind(globalThis),
  bootstrap: WorldRuntimeBootstrap = defaultBootstrap,
) {
  let cachedRuntime: WorldIncomeRuntime | null = null;
  let inFlight: Promise<WorldIncomeRuntime> | null = null;

  async function loadUncached(): Promise<WorldIncomeRuntime> {
    const engine = await fetchVerifiedJson<EngineManifest>(fetcher, bootstrap.engineManifest.publicPath, bootstrap.engineManifest.sha256, bootstrap.engineManifest.sizeBytes);
    assertManifest(engine);
    const price = await fetchVerifiedJson<PriceAlignment>(fetcher, artifactPublicPath(bootstrap.publicBasePath, engine.artifacts.priceAlignment.path), engine.artifacts.priceAlignment.sha256, engine.artifacts.priceAlignment.sizeBytes);
    const runtimeBase = assertPrice(price, engine);
    const cdfDocument = await fetchVerifiedJson<WorldCdfDocument>(fetcher, artifactPublicPath(bootstrap.publicBasePath, engine.artifacts.cdf.path), engine.artifacts.cdf.sha256, engine.artifacts.cdf.sizeBytes);
    const cdf = compileCdf(cdfDocument, engine);
    return { ...runtimeBase, cdf };
  }

  return {
    getCached(): WorldIncomeRuntime | null { return cachedRuntime; },
    load(): Promise<WorldIncomeRuntime> {
      if (cachedRuntime) return Promise.resolve(cachedRuntime);
      if (!inFlight) {
        inFlight = loadUncached().then((runtime) => {
          cachedRuntime = runtime;
          return runtime;
        }).finally(() => { inFlight = null; });
      }
      return inFlight;
    },
  };
}

export const worldEngineLoader = createWorldEngineLoader();
