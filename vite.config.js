import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
    // Para dominio propio: '/'
    base: '/',
    plugins: [vue()],
    
    // Configuración del alias @ para resolver rutas
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    
    css: {
        preprocessorOptions: {
            scss: {
                silenceDeprecations: ["color-functions", "global-builtin", "import"],
            },
        },
    },
})
