export type EngineStatus = 'idle' | 'loading' | 'success' | 'unavailable'

export function isEngineSettled(status: EngineStatus): boolean {
  return status === 'success' || status === 'unavailable'
}

export function shouldShowSharing(
  brazilStatus: EngineStatus,
  worldStatus: EngineStatus,
): boolean {
  return (
    isEngineSettled(brazilStatus)
    && isEngineSettled(worldStatus)
    && (brazilStatus === 'success' || worldStatus === 'success')
  )
}

export function formatReferenceMonth(referenceMonth: string): string | null {
  const match = /^(\d{4})-(0[1-9]|1[0-2])$/.exec(referenceMonth)
  if (!match) return null

  const year = Number(match[1])
  const month = Number(match[2])
  return new Intl.DateTimeFormat('pt-BR', {
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(new Date(Date.UTC(year, month - 1, 1)))
}

export function datasetYearFromVersion(datasetVersion: string): number | null {
  const match = /^(\d{4})(?:-|$)/.exec(datasetVersion)
  return match ? Number(match[1]) : null
}
