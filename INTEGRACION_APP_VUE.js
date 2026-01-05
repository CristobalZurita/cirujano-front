// 📌 INSTRUCCIONES DE INTEGRACIÓN EN App.vue
// Archivo: src/vue/stack/App.vue

// ────────────────────────────────────────────────────────────────────────────
// PASO 1: Agregar estos imports al inicio del script
// ────────────────────────────────────────────────────────────────────────────

import DiagnosticSection from '@/vue/sections/DiagnosticSection.vue'
import FloatingQuoteButton from '@/vue/components/widgets/FloatingQuoteButton.vue'


// ────────────────────────────────────────────────────────────────────────────
// PASO 2: Agregar los componentes en setup() si usa Composition API
// ────────────────────────────────────────────────────────────────────────────

// Ya están declarados en los imports, Vue3 los reconoce automáticamente


// ────────────────────────────────────────────────────────────────────────────
// PASO 3: En el template, agregar estos componentes
// ────────────────────────────────────────────────────────────────────────────

/*
<template>
  <div id="app">
    <!-- Componentes existentes -->
    <Navigation />
    <ContentLayer />      ← Este contiene todas las secciones principales
    
    <!-- NUEVO: Sección de diagnóstico (agregar AQUÍ) -->
    <DiagnosticSection />
    
    <!-- Resto de footer, etc -->
  </div>
  
  <!-- NUEVO: Botón flotante (agregar AQUÍ - global) -->
  <FloatingQuoteButton />
</template>

<script setup>
import { ref } from 'vue'
import Navigation from '@/vue/components/nav/Navigation.vue'
import ContentLayer from '@/vue/stack/ContentLayer.vue'

// ← AGREGAR ESTOS DOS IMPORTS
import DiagnosticSection from '@/vue/sections/DiagnosticSection.vue'
import FloatingQuoteButton from '@/vue/components/widgets/FloatingQuoteButton.vue'
</script>
*/


// ────────────────────────────────────────────────────────────────────────────
// ALTERNATIVA: Si DiagnosticSection debe ir en ContentLayer
// ────────────────────────────────────────────────────────────────────────────

/*
En: src/vue/stack/ContentLayer.vue

<template>
  <div>
    <!-- Secciones existentes -->
    <Master />
    
    <!-- AGREGAR AQUÍ la sección de diagnóstico -->
    <DiagnosticSection />
    
    <!-- Resto de secciones -->
    <FeedbacksLayer />
  </div>
</template>

<script setup>
import Master from '@/vue/content/Master.vue'
import FeedbacksLayer from '@/vue/stack/FeedbacksLayer.vue'

// AGREGAR ESTE IMPORT
import DiagnosticSection from '@/vue/sections/DiagnosticSection.vue'
</script>
*/


// ────────────────────────────────────────────────────────────────────────────
// PASO 4: Verificar que todos los archivos existen
// ────────────────────────────────────────────────────────────────────────────

// Verificar estos archivos existen:
✓ src/vue/sections/DiagnosticSection.vue
✓ src/vue/components/articles/DiagnosticWizard.vue
✓ src/vue/components/widgets/FloatingQuoteButton.vue
✓ src/composables/useDiagnostic.js
✓ src/assets/data/brands.json
✓ src/assets/data/instruments.json
✓ src/assets/data/faults.json
✓ src/scss/_variables.scss (actualizado)


// ────────────────────────────────────────────────────────────────────────────
// PASO 5: Compilar y verificar en navegador
// ────────────────────────────────────────────────────────────────────────────

// Terminal:
npm run dev

// Verificar en navegador:
http://localhost:5173

// Cosas a verificar:
✓ Botón naranja en esquina inferior derecha con ícono calculadora
✓ Texto "¡COTIZA AHORA!" visible
✓ Animación de pulso (arriba-abajo suave)
✓ Al hacer click → scroll a sección de diagnóstico
✓ Sección visible con 5 pasos del wizard
✓ Al pasar mouse sobre botón → tooltip "Diagnóstico gratis"


// ────────────────────────────────────────────────────────────────────────────
// PASO 6: Troubleshooting
// ────────────────────────────────────────────────────────────────────────────

PROBLEMA: No se ve el botón flotante
SOLUCIÓN:
  1. Verificar que FloatingQuoteButton está importado en App.vue
  2. Verificar que está en el template (FUERA de divs container)
  3. Revisar que el z-index es 999
  4. Abrir DevTools → Elements → buscar "floating-quote-button"
  5. Ver si tiene `position: fixed` en estilos

PROBLEMA: Fallas no se muestran según el instrumento
SOLUCIÓN:
  1. Abrir DevTools → Console
  2. Revisar si hay errores de import de JSON
  3. Verificar que ruta en composable es correcta:
     import brandsData from '@/assets/data/brands.json'
  4. Verificar que JSON es válido (sin comas faltantes)

PROBLEMA: Cotización no calcula bien
SOLUCIÓN:
  1. Abrir DevTools → Console
  2. En Paso 5, abrir pestaña Network
  3. Revisar valores en calculateQuote()
  4. Verificar multiplicadores en config.py (backend)

PROBLEMA: Estilos se ven mal en tablet/móvil
SOLUCIÓN:
  1. Revisar breakpoints en _variables.scss
  2. Abrir DevTools → Toggle device toolbar (Ctrl+Shift+M)
  3. Probar en tablet (768px) y móvil (375px)
  4. Botón debería ser solo icono en móvil

PROBLEMA: "Module not found" error
SOLUCIÓN:
  1. Limpiar node_modules: rm -rf node_modules && npm install
  2. Limpiar cache: npm cache clean --force
  3. Reiniciar dev server: Ctrl+C, luego npm run dev


// ────────────────────────────────────────────────────────────────────────────
// CÓDIGO EJEMPLO COMPLETO DE App.vue
// ────────────────────────────────────────────────────────────────────────────

/*
<template>
  <div id="app">
    <Navigation />
    <ContentLayer />
    <DiagnosticSection />
    <FloatingQuoteButton />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navigation from '@/vue/components/nav/Navigation.vue'
import ContentLayer from '@/vue/stack/ContentLayer.vue'
import DiagnosticSection from '@/vue/sections/DiagnosticSection.vue'
import FloatingQuoteButton from '@/vue/components/widgets/FloatingQuoteButton.vue'
</script>

<style scoped>
#app {
  min-height: 100vh;
}
</style>
*/


// ────────────────────────────────────────────────────────────────────────────
// CÓDIGOS DEBUGUEO ÚTILES (copiar en DevTools Console)
// ────────────────────────────────────────────────────────────────────────────

// Ver si el botón existe
document.querySelector('.floating-quote-button')

// Ver si la sección existe
document.querySelector('#diagnostic-section')

// Simular click en botón
document.querySelector('.floating-quote-button .quote-btn').click()

// Ver animación de pulso
document.querySelector('.floating-quote-button .quote-btn').classList

// Cargar composable en consola
import { useDiagnostic } from '@/composables/useDiagnostic'
const diag = useDiagnostic()
diag.brands           // Ver todas las marcas
diag.selectedBrand    // Ver marca seleccionada
diag.calculateQuote() // Calcular cotización

// Ver datos JSON
fetch('/src/assets/data/brands.json').then(r => r.json()).then(d => console.log(d))


// ────────────────────────────────────────────────────────────────────────────
// NOTAS IMPORTANTES
// ────────────────────────────────────────────────────────────────────────────

1. Los datos JSON se cargan AUTOMÁTICAMENTE por Vite
   No necesitas ningún import especial, el composable los maneja

2. El composable usa reactive() de Vue3
   Los cambios en state se propagan automáticamente

3. El botón flotante está configurado para PRODUCTION
   No hay console.logs o debugueo en el código

4. Las variables SCSS se han actualizado en _variables.scss
   Los componentes nuevos usan las nuevas escalas automáticamente

5. El wizard es completamente funcional AHORA
   Solo falta conectar con backend para enviar datos

6. No hay referencias a Thaddeus Cahill en el código
   Se verificó y está completamente eliminado

═════════════════════════════════════════════════════════════════════════════

SIGUIENTES PASOS DESPUÉS DE INTEGRACIÓN:

1. Expandir catálogo de instrumentos en JSON
2. Conectar composable con API backend
3. Implementar envío de email
4. Implementar descarga PDF
5. Crear base de datos PostgreSQL
6. Panel admin de gestión

═════════════════════════════════════════════════════════════════════════════

Documento de integración: INTEGRACION_APP_VUE.js
Generado: Enero 2026
Sistema: Cirujano de Sintetizadores v1.0.0
