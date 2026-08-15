import runtimeConfig from '../../config/brazil-frontend-runtime.json' with { type: 'json' };
import type { BrazilIncomeRuntime } from './domain.ts';

export interface BrazilRuntimeBootstrap {
  publicBasePath: string;
  engineManifest: {
    publicPath: string;
    sha256: string;
  };
}

interface ArtifactContract {
  path: string;
  sizeBytes: number;
  sha256: string;
  version: string;
}

interface EngineManifest {
  schemaVersion: string;
  version: string;
  status: string;
  integration: {
    brazilFrontendIntegrationAllowed: boolean;
    worldFrontendIntegrationAllowed: boolean;
  };
  methodology: {
    priceReference: string;
    populationUnit: string;
  };
  artifacts: {
    cdf: ArtifactContract;
    priceAlignment: ArtifactContract;
  };
}

interface PriceAlignment {
  schemaVersion: string;
  version: string;
  status: string;
  basePriceReference: string;
  priceIndexReferenceMonth: string;
  multiplierCurrentToBase: string;
  cdfSha256: string;
  integration: {
    frontendIntegrationAllowed: boolean;
  };
}

interface IncomeCdf {
  schemaVersion: string;
  brazilDatasetVersion: string;
  priceReference: string;
  populationUnit: string;
  frontendIntegrationAllowed: boolean;
  uniqueIncomeValues: number;
  totalWeight: number;
  rdpc: number[];
  cumAtOrBelow: number[];
}

type Fetcher = (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>;

const defaultBootstrap = runtimeConfig as BrazilRuntimeBootstrap;

function artifactPublicPath(basePath: string, repositoryPath: string): string {
  const filename = repositoryPath.replaceAll('\\', '/').split('/').at(-1);
  if (!filename) throw new Error('O manifesto contém um caminho de artefato inválido.');
  return `${basePath.replace(/\/$/, '')}/${filename}`;
}

async function sha256Hex(bytes: ArrayBuffer): Promise<string> {
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0'))
    .join('')
    .toUpperCase();
}

async function fetchVerifiedJson<T>(
  fetcher: Fetcher,
  publicPath: string,
  expectedSha256: string,
  expectedBytes?: number,
): Promise<T> {
  const response = await fetcher(publicPath, {
    method: 'GET',
    credentials: 'same-origin',
    cache: 'default',
  });

  if (!response.ok) throw new Error(`Artefato indisponível: ${publicPath}`);
  const bytes = await response.arrayBuffer();
  if (expectedBytes !== undefined && bytes.byteLength !== expectedBytes) {
    throw new Error(`Tamanho incompatível para ${publicPath}.`);
  }
  if ((await sha256Hex(bytes)) !== expectedSha256.toUpperCase()) {
    throw new Error(`SHA-256 incompatível para ${publicPath}.`);
  }

  try {
    return JSON.parse(new TextDecoder().decode(bytes)) as T;
  } catch {
    throw new Error(`JSON inválido em ${publicPath}.`);
  }
}

function assertArtifactContract(value: unknown, name: string): asserts value is ArtifactContract {
  if (
    typeof value !== 'object' ||
    value === null ||
    typeof (value as ArtifactContract).path !== 'string' ||
    !Number.isSafeInteger((value as ArtifactContract).sizeBytes) ||
    (value as ArtifactContract).sizeBytes <= 0 ||
    !/^[A-F0-9]{64}$/i.test((value as ArtifactContract).sha256) ||
    typeof (value as ArtifactContract).version !== 'string'
  ) {
    throw new Error(`Contrato inválido do artefato ${name}.`);
  }
}

function assertEngineManifest(value: EngineManifest): void {
  if (
    value.schemaVersion !== '1.0.0' ||
    value.version !== '1.0.0' ||
    value.status !== 'CANONICAL_APPROVED_FOR_INTEGRATION' ||
    value.integration?.brazilFrontendIntegrationAllowed !== true ||
    value.integration?.worldFrontendIntegrationAllowed !== false ||
    value.methodology?.priceReference !== 'preços médios de 2025' ||
    value.methodology?.populationUnit !== 'pessoas elegíveis'
  ) {
    throw new Error('Manifesto do motor Brasil não está aprovado para esta integração.');
  }
  assertArtifactContract(value.artifacts?.cdf, 'CDF');
  assertArtifactContract(value.artifacts?.priceAlignment, 'alinhamento de preços');
}

function assertPriceAlignment(value: PriceAlignment, engine: EngineManifest): number {
  const multiplier = Number(value.multiplierCurrentToBase);
  if (
    value.schemaVersion !== '1.0.0' ||
    value.version !== engine.artifacts.priceAlignment.version ||
    value.status !== 'CANONICAL_APPROVED' ||
    value.basePriceReference !== engine.methodology.priceReference ||
    !/^\d{4}-\d{2}$/.test(value.priceIndexReferenceMonth) ||
    typeof value.cdfSha256 !== 'string' ||
    value.cdfSha256.toUpperCase() !== engine.artifacts.cdf.sha256.toUpperCase() ||
    value.integration?.frontendIntegrationAllowed !== false ||
    !Number.isFinite(multiplier) ||
    multiplier <= 0
  ) {
    throw new Error('Manifesto de alinhamento de preços incompatível com o motor Brasil.');
  }
  return multiplier;
}

function assertAndCompileCdf(value: IncomeCdf, engine: EngineManifest): BrazilIncomeRuntime['cdf'] {
  const rdpc = value.rdpc;
  const cumulative = value.cumAtOrBelow;
  if (
    value.brazilDatasetVersion !== engine.artifacts.cdf.version ||
    value.priceReference !== engine.methodology.priceReference ||
    typeof value.populationUnit !== 'string' ||
    !value.populationUnit.startsWith(engine.methodology.populationUnit) ||
    value.frontendIntegrationAllowed !== false ||
    !Array.isArray(rdpc) ||
    !Array.isArray(cumulative) ||
    rdpc.length === 0 ||
    rdpc.length !== cumulative.length ||
    value.uniqueIncomeValues !== rdpc.length ||
    !Number.isFinite(value.totalWeight) ||
    value.totalWeight <= 0
  ) {
    throw new Error('CDF Brasil incompatível com o contrato do motor.');
  }

  if (rdpc[0] < 0) throw new Error('CDF Brasil contém renda negativa.');

  let previousRdpc = Number.NEGATIVE_INFINITY;
  let previousCumulative = 0;
  for (let index = 0; index < rdpc.length; index += 1) {
    if (
      !Number.isFinite(rdpc[index]) ||
      rdpc[index] <= previousRdpc ||
      !Number.isFinite(cumulative[index]) ||
      cumulative[index] <= previousCumulative
    ) {
      throw new Error('CDF Brasil não é estritamente crescente.');
    }
    previousRdpc = rdpc[index];
    previousCumulative = cumulative[index];
  }

  const tolerance = Math.max(1e-6, value.totalWeight * 1e-12);
  if (
    Math.abs(previousCumulative - value.totalWeight) > tolerance
  ) {
    throw new Error('Métricas da CDF Brasil não reconciliam com seus vetores.');
  }

  return {
    rdpc: Float64Array.from(rdpc),
    cumulativeWeightAtOrBelow: Float64Array.from(cumulative),
    totalWeight: value.totalWeight,
    maxRdpc: previousRdpc,
  };
}

export function createBrazilEngineLoader(
  fetcher: Fetcher = globalThis.fetch.bind(globalThis),
  bootstrap: BrazilRuntimeBootstrap = defaultBootstrap,
) {
  let cachedRuntime: BrazilIncomeRuntime | null = null;
  let inFlight: Promise<BrazilIncomeRuntime> | null = null;

  async function loadUncached(): Promise<BrazilIncomeRuntime> {
    const engine = await fetchVerifiedJson<EngineManifest>(
      fetcher,
      bootstrap.engineManifest.publicPath,
      bootstrap.engineManifest.sha256,
    );
    assertEngineManifest(engine);

    const price = await fetchVerifiedJson<PriceAlignment>(
      fetcher,
      artifactPublicPath(bootstrap.publicBasePath, engine.artifacts.priceAlignment.path),
      engine.artifacts.priceAlignment.sha256,
      engine.artifacts.priceAlignment.sizeBytes,
    );
    const multiplierCurrentToBase = assertPriceAlignment(price, engine);

    const cdfArtifact = await fetchVerifiedJson<IncomeCdf>(
      fetcher,
      artifactPublicPath(bootstrap.publicBasePath, engine.artifacts.cdf.path),
      engine.artifacts.cdf.sha256,
      engine.artifacts.cdf.sizeBytes,
    );
    const cdf = assertAndCompileCdf(cdfArtifact, engine);

    return {
      engineVersion: engine.version,
      priceReference: engine.methodology.priceReference,
      referenceMonth: price.priceIndexReferenceMonth,
      multiplierCurrentToBase,
      cdf,
    };
  }

  return {
    getCached(): BrazilIncomeRuntime | null {
      return cachedRuntime;
    },
    load(): Promise<BrazilIncomeRuntime> {
      if (cachedRuntime) return Promise.resolve(cachedRuntime);
      if (!inFlight) {
        inFlight = loadUncached()
          .then((runtime) => {
            cachedRuntime = runtime;
            return runtime;
          })
          .finally(() => {
            inFlight = null;
          });
      }
      return inFlight;
    },
  };
}

export const brazilEngineLoader = createBrazilEngineLoader();
