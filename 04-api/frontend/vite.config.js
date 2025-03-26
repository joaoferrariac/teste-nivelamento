import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0', // Permite acesso por IP local
    port: 5173,
    strictPort: true,
    open: true // Abre o navegador automaticamente
  },
  build: {
    outDir: '../dist', // Pasta de saída diferente
    emptyOutDir: true
  }
})