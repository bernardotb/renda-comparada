import type { BrazilPositionDisplay } from './brazil/domain.ts'

export const GENERIC_SHARE_MESSAGE = 'Descobri onde minha renda está na distribuição brasileira. E você?'
export const SHARE_TITLE = 'Renda Comparada'
export const SHARE_CHANNELS = ['native', 'whatsapp', 'copy'] as const

export type ShareChannel = typeof SHARE_CHANNELS[number]

export type SharePayload = {
  title: string
  text: string
  url: string
}

export function buildShareUrl(origin: string, channel: ShareChannel): string {
  const url = new URL('/', origin)
  url.searchParams.set('utm_source', 'share')
  url.searchParams.set('utm_medium', channel)
  url.searchParams.set('utm_campaign', 'organic_share')
  url.hash = ''
  return url.toString()
}

export function buildPositionShareMessage(display: BrazilPositionDisplay | null): string | null {
  if (!display?.topLabel) return null
  if (/^TOP (?:0(?:[,.]0+)?|100)%$/i.test(display.topLabel)) return null
  return `${display.topLabel} — minha posição aproximada na distribuição de renda brasileira. E você?`
}

export function buildSharePayload(
  url: string,
  includePosition: boolean,
  positionMessage: string | null,
): SharePayload {
  return {
    title: SHARE_TITLE,
    text: includePosition && positionMessage ? positionMessage : GENERIC_SHARE_MESSAGE,
    url,
  }
}

export function buildWhatsAppUrl(payload: SharePayload): string {
  return `https://wa.me/?text=${encodeURIComponent(`${payload.text}\n${payload.url}`)}`
}
