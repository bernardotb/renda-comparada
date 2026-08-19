import { createHash } from 'node:crypto'
import { copyFile, mkdir, readFile, readdir, rm } from 'node:fs/promises'
import { basename, dirname, resolve, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const runtimeConfig = JSON.parse(await readFile(resolve(root, 'config/world-frontend-runtime.json'), 'utf8'))

function repositoryPath(relativePath) {
  const resolved = resolve(root, relativePath)
  if (resolved !== root && !resolved.startsWith(`${root}${sep}`)) {
    throw new Error(`Caminho fora da raiz canônica: ${relativePath}`)
  }
  return resolved
}

function sha256(buffer) {
  return createHash('sha256').update(buffer).digest('hex').toUpperCase()
}

async function verifiedBytes(relativePath, expectedHash, expectedSize) {
  const bytes = await readFile(repositoryPath(relativePath))
  if (sha256(bytes) !== expectedHash) throw new Error(`SHA-256 divergente para ${relativePath}`)
  if (expectedSize !== undefined && bytes.byteLength !== expectedSize) {
    throw new Error(`Tamanho divergente para ${relativePath}: ${bytes.byteLength}`)
  }
  return bytes
}

function assertArtifact(value, name) {
  if (
    !value
    || typeof value.path !== 'string'
    || !/^[A-F0-9]{64}$/.test(value.sha256)
    || !Number.isSafeInteger(value.sizeBytes)
    || value.sizeBytes <= 0
    || typeof value.version !== 'string'
    || typeof value.schema !== 'string'
  ) throw new Error(`Contrato inválido do artefato Mundo ${name}`)
}

const engineBytes = await verifiedBytes(runtimeConfig.engineManifest.sourcePath, runtimeConfig.engineManifest.sha256)
const engine = JSON.parse(engineBytes.toString('utf8'))
if (
  engine.schemaVersion !== '1.0.0'
  || engine.dataset !== 'world-income-engine'
  || engine.status !== 'CANONICAL_APPROVED_FOR_INTEGRATION'
  || engine.integration?.worldFrontendIntegrationAllowed !== true
  || engine.methodology?.pipVersion !== '20260324_2021'
  || engine.methodology?.productionBuild !== '20260324_2021_01_02_PROD'
  || engine.methodology?.referenceYear !== 2024
  || engine.methodology?.pppBase !== 2021
) throw new Error('Manifesto Mundo não autoriza esta integração')

assertArtifact(engine.artifacts?.cdf, 'CDF')
assertArtifact(engine.artifacts?.priceAlignment, 'alinhamento de preços')
assertArtifact(engine.artifacts?.goldenCases, 'golden cases')

const engineSchemaBytes = await readFile(repositoryPath(engine.schema))
if (sha256(engineSchemaBytes) !== engine.schemaSha256) throw new Error('Schema do manifesto Mundo divergente')

const priceBytes = await verifiedBytes(
  engine.artifacts.priceAlignment.path,
  engine.artifacts.priceAlignment.sha256,
  engine.artifacts.priceAlignment.sizeBytes,
)
const price = JSON.parse(priceBytes.toString('utf8'))
if (
  price.status !== 'CANONICAL_PRODUCTION_FRONTEND_BLOCKED'
  || price.integration?.worldFrontendIntegrationAllowed !== false
  || price.version !== engine.artifacts.priceAlignment.version
  || price.pipVersion !== engine.methodology.pipVersion
  || price.productionBuild !== engine.methodology.productionBuild
  || price.referenceYear !== engine.methodology.referenceYear
  || price.pppBase !== engine.methodology.pppBase
) throw new Error('Alinhamento Mundo incompatível com o manifesto autorizado')

const cdfBytes = await verifiedBytes(
  engine.artifacts.cdf.path,
  engine.artifacts.cdf.sha256,
  engine.artifacts.cdf.sizeBytes,
)
const cdf = JSON.parse(cdfBytes.toString('utf8'))
if (
  cdf.status !== 'CANONICAL_PRODUCTION_FRONTEND_BLOCKED'
  || cdf.integration?.worldFrontendIntegrationAllowed !== false
  || cdf.version !== engine.artifacts.cdf.version
  || cdf.methodology?.pipVersion !== engine.methodology.pipVersion
  || cdf.methodology?.productionBuild !== engine.methodology.productionBuild
  || cdf.methodology?.referenceYear !== engine.methodology.referenceYear
  || cdf.methodology?.pppBase !== engine.methodology.pppBase
  || cdf.statistics?.pointCount !== 216790
  || cdf.points?.length !== 216790
) throw new Error('CDF Mundo incompatível com o manifesto autorizado')

const artifacts = [
  { sourcePath: runtimeConfig.engineManifest.sourcePath, expectedHash: runtimeConfig.engineManifest.sha256, bytes: engineBytes },
  { sourcePath: engine.artifacts.priceAlignment.path, expectedHash: engine.artifacts.priceAlignment.sha256, bytes: priceBytes },
  { sourcePath: engine.artifacts.cdf.path, expectedHash: engine.artifacts.cdf.sha256, bytes: cdfBytes },
]

const publicDirectory = repositoryPath(`public${runtimeConfig.publicBasePath}`)
await rm(publicDirectory, { recursive: true, force: true })
await mkdir(publicDirectory, { recursive: true })

const copied = []
for (const artifact of artifacts) {
  const destination = resolve(publicDirectory, basename(artifact.sourcePath))
  await copyFile(repositoryPath(artifact.sourcePath), destination)
  const copiedBytes = await readFile(destination)
  if (sha256(copiedBytes) !== artifact.expectedHash || !copiedBytes.equals(artifact.bytes)) {
    throw new Error(`Cópia pública Mundo divergente: ${destination}`)
  }
  copied.push({
    source: artifact.sourcePath,
    publicPath: `${runtimeConfig.publicBasePath}/${basename(artifact.sourcePath)}`,
    sha256: artifact.expectedHash,
    sizeBytes: copiedBytes.byteLength,
  })
}

const publicNames = (await readdir(publicDirectory)).sort()
const expectedNames = artifacts.map(({ sourcePath }) => basename(sourcePath)).sort()
if (JSON.stringify(publicNames) !== JSON.stringify(expectedNames)) {
  throw new Error(`Publicação Mundo contém arquivos inesperados: ${publicNames.join(', ')}`)
}

process.stdout.write(`${JSON.stringify({ status: 'PASS', copied }, null, 2)}\n`)
