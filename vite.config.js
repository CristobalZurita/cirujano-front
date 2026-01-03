import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
    // Para dominio propio: '/'
    // Para GitHub Pages: '/cirujano-front/'
    base: '/',
    plugins: [vue()],
    css: {
        preprocessorOptions: {
            scss: {
                silenceDeprecations: ["color-functions", "global-builtin", "import"],
            },
        },
    },
})
