import { createHash } from 'node:crypto'
import { copyFile, mkdir, readFile } from 'node:fs/promises'
import { basename, dirname, resolve, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const runtimeConfigPath = resolve(root, 'config/brazil-frontend-runtime.json')
const runtimeConfig = JSON.parse(await readFile(runtimeConfigPath, 'utf8'))

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
  const observedHash = sha256(bytes)
  if (observedHash !== expectedHash) {
    throw new Error(`SHA-256 divergente para ${relativePath}: ${observedHash}`)
  }
  if (expectedSize !== undefined && bytes.byteLength !== expectedSize) {
    throw new Error(`Tamanho divergente para ${relativePath}: ${bytes.byteLength}`)
  }
  return bytes
}

const engineBytes = await verifiedBytes(
  runtimeConfig.engineManifest.sourcePath,
  runtimeConfig.engineManifest.sha256,
)
const engine = JSON.parse(engineBytes.toString('utf8'))

if (
  engine.status !== 'CANONICAL_APPROVED_FOR_INTEGRATION'
  || engine.integration?.brazilFrontendIntegrationAllowed !== true
  || engine.integration?.worldFrontendIntegrationAllowed !== false
) {
  throw new Error('Manifesto do motor Brasil não autoriza esta integração')
}

const artifacts = [
  {
    sourcePath: runtimeConfig.engineManifest.sourcePath,
    expectedHash: runtimeConfig.engineManifest.sha256,
    bytes: engineBytes,
  },
  {
    sourcePath: engine.artifacts.priceAlignment.path,
    expectedHash: engine.artifacts.priceAlignment.sha256,
    expectedSize: engine.artifacts.priceAlignment.sizeBytes,
  },
  {
    sourcePath: engine.artifacts.cdf.path,
    expectedHash: engine.artifacts.cdf.sha256,
    expectedSize: engine.artifacts.cdf.sizeBytes,
  },
]

const publicDirectory = repositoryPath(`public${runtimeConfig.publicBasePath}`)
await mkdir(publicDirectory, { recursive: true })

const copied = []
for (const artifact of artifacts) {
  const bytes = artifact.bytes ?? await verifiedBytes(
    artifact.sourcePath,
    artifact.expectedHash,
    artifact.expectedSize,
  )
  const destination = resolve(publicDirectory, basename(artifact.sourcePath))
  await copyFile(repositoryPath(artifact.sourcePath), destination)
  const copiedBytes = await readFile(destination)
  if (sha256(copiedBytes) !== artifact.expectedHash || !copiedBytes.equals(bytes)) {
    throw new Error(`Cópia pública divergente: ${destination}`)
  }
  copied.push({
    source: artifact.sourcePath,
    publicPath: `${runtimeConfig.publicBasePath}/${basename(artifact.sourcePath)}`,
    sha256: artifact.expectedHash,
    sizeBytes: copiedBytes.byteLength,
  })
}

process.stdout.write(`${JSON.stringify({ status: 'PASS', copied }, null, 2)}\n`)
