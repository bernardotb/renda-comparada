import { SHARE_CHANNELS } from './share.ts'

export const ANALYTICS_EVENTS = [
  'calculation_started',
  'calculation_completed',
  'result_viewed',
  'share_clicked',
  'recalculate_clicked',
] as const

export type AnalyticsEventName = typeof ANALYTICS_EVENTS[number]

type PlausibleInitOptions = {
  transformRequest: (payload: Record<string, unknown>) => Record<string, unknown>
}

type PlausibleFunction = ((eventName: AnalyticsEventName) => void) & {
  init?: (options?: PlausibleInitOptions) => void
  o?: PlausibleInitOptions
  q?: unknown[][]
}

declare global {
  interface Window {
    plausible?: PlausibleFunction
  }
}

const ALLOWED_EVENT_NAMES = new Set<string>(ANALYTICS_EVENTS)
const ALLOWED_SHARE_CHANNELS = new Set<string>(SHARE_CHANNELS)
const PLAUSIBLE_SCRIPT_PATTERN = /^https:\/\/plausible\.io\/js\/pa-[a-z0-9_-]+\.js$/i

export function sanitizeAnalyticsUrl(value: string): string {
  const source = new URL(value)
  const sanitized = new URL(source.pathname, source.origin)
  const shareSource = source.searchParams.get('utm_source')
  const shareMedium = source.searchParams.get('utm_medium')
  const shareCampaign = source.searchParams.get('utm_campaign')

  if (
    shareSource === 'share'
    && shareMedium !== null
    && ALLOWED_SHARE_CHANNELS.has(shareMedium)
    && shareCampaign === 'organic_share'
  ) {
    sanitized.searchParams.set('utm_source', 'share')
    sanitized.searchParams.set('utm_medium', shareMedium)
    sanitized.searchParams.set('utm_campaign', 'organic_share')
  }

  return sanitized.toString()
}

export function buildPlausibleInitOptions(getCurrentUrl = () => window.location.href): PlausibleInitOptions {
  return {
    transformRequest(payload) {
      return {
        ...payload,
        u: sanitizeAnalyticsUrl(getCurrentUrl()),
      }
    },
  }
}

function ensurePlausibleFunction(): PlausibleFunction {
  if (window.plausible) return window.plausible

  const plausible = ((...args: unknown[]) => {
    plausible.q = plausible.q ?? []
    plausible.q.push(args)
  }) as PlausibleFunction
  plausible.init = (options) => {
    plausible.o = options
  }
  window.plausible = plausible
  return plausible
}

function configuredScriptSource(): string | undefined {
  const env = (import.meta as ImportMeta & {
    env?: { VITE_PLAUSIBLE_SCRIPT_SRC?: string }
  }).env
  return env?.VITE_PLAUSIBLE_SCRIPT_SRC?.trim()
}

export function initializePlausible(scriptSource = configuredScriptSource()): boolean {
  if (typeof window === 'undefined' || typeof document === 'undefined') return false
  if (!scriptSource || !PLAUSIBLE_SCRIPT_PATTERN.test(scriptSource)) return false
  if (document.querySelector('script[data-renda-comparada-plausible]')) return true

  try {
    const plausible = ensurePlausibleFunction()
    plausible.init?.(buildPlausibleInitOptions())

    const script = document.createElement('script')
    script.async = true
    script.src = scriptSource
    script.dataset.rendaComparadaPlausible = 'true'
    document.head.append(script)
    return true
  } catch {
    return false
  }
}

export function trackAnalyticsEvent(eventName: AnalyticsEventName): void {
  if (!ALLOWED_EVENT_NAMES.has(eventName)) return

  try {
    const plausible = typeof window !== 'undefined' ? window.plausible : undefined
    if (!plausible) return

    plausible(eventName)
  } catch {
    // Analytics nunca é dependência funcional do produto.
  }
}
