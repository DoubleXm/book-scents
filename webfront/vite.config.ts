import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    vueDevTools(),
    AutoImport({
      dts: 'src/dts/auto-imports.d.ts',
      imports: [
        'vue',
        'vue-router'
        // '@vueuse/core'
      ],
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [
        ElementPlusResolver({
          importStyle: 'sass'
        }),
      ],
      dts: 'src/dts/components.d.ts',
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      '/api/v1': {
        // target: 'http://127.0.0.1:4523/m1/7163149-6887265-default',
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        secure: false,
        // rewrite: (path) => path.replace(/^\/api\/v1/, ''),
      }
    }
  }
})
