import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'

const cleanPublicRoutes = {
  name: 'clean-public-routes',
  configureServer(server) {
    server.middlewares.use((request, _response, next) => {
      const pathnameRequest = request as typeof request & { url?: string }
      pathnameRequest.url = pathnameRequest.url
        ?.replace(/^\/metodologia(?=\?|$)/, '/metodologia/')
        .replace(/^\/privacidade(?=\?|$)/, '/privacidade/')
      next()
    })
  },
  configurePreviewServer(server) {
    server.middlewares.use((request, _response, next) => {
      const pathnameRequest = request as typeof request & { url?: string }
      pathnameRequest.url = pathnameRequest.url
        ?.replace(/^\/metodologia(?=\?|$)/, '/metodologia/')
        .replace(/^\/privacidade(?=\?|$)/, '/privacidade/')
      next()
    })
  },
} satisfies Plugin

export default defineConfig({
  appType: 'mpa',
  plugins: [cleanPublicRoutes, react()],
  build: {
    rollupOptions: {
      input: {
        main: 'index.html',
        metodologia: 'metodologia/index.html',
        privacidade: 'privacidade/index.html',
      },
    },
  },
})
