AUDITORÍA DE BUGS - Cirujano de Sintetizadores

AUDITORÍA DE BUGS

Sistema de Diagnóstico y Cotización

Cirujano de Sintetizadores

Fecha: 5 de Enero de 2026

Versión: 1.0

1. RESUMEN EJECUTIVO

Esta auditoría identifica bugs críticos en el sistema de diagnóstico/cotización que causan los problemas observados en la interfaz: validaciones que no funcionan, cotización que retorna $0, campos vacíos, y factores indefinidos.

| CATEGORÍA                 | BUGS    | SEVERIDAD   |
| -------------------------- | ------- | ----------- |
| Validación de Formularios | 4       | CRÍTICA    |
| Lógica de Cotización     | 3       | CRÍTICA    |
| Datos Incompletos (JSON)   | 5       | ALTA        |
| UX / Estados Visuales      | 3       | MEDIA       |
| TOTAL                      | 15 bugs | 7 críticos |

2. BUGS DE VALIDACIÓN DE FORMULARIOS

Problema observado: El formulario acepta "123" como nombre, "asdf" como teléfono, y "a@a.d" como email.

2.1 BUG: Sin validación de nombre

Archivo: DiagnosticWizard.vue (línea ~12454)

Código actual:

<input v-model="diagnostic.clientName.value" type="text" required />

Problema: Solo usa 'required', no valida contenido. Acepta números, símbolos, espacios.

Fix requerido:

pattern="[A-Za-zÀ-ÿ\s]{2,50}" + validación JS

2.2 BUG: Sin validación de teléfono

Archivo: DiagnosticWizard.vue (línea ~12480)

Código actual:

<input v-model="diagnostic.clientPhone.value" type="tel" />

Problema: type='tel' NO valida formato, solo sugiere teclado numérico en móvil.

Fix requerido:

pattern="^\+?[0-9]{8,15}$" + validación JS

2.3 BUG: Validación de email insuficiente

Archivo: useDiagnostic.js (línea ~8004)

Código actual:

clientEmail.value && clientEmail.value.includes('@')

Problema: 'a@a.d' pasa la validación. No verifica dominio válido.

Fix requerido:

/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)

2.4 BUG: Falta validación en nextStep()

Archivo: DiagnosticWizard.vue (línea ~12640)

Código actual:

const nextStep = () => { if (currentStep.value < 5) currentStep.value++ }

Problema: No valida datos del paso actual antes de avanzar. Permite llegar al paso 5 con datos inválidos.

3. BUGS DE LÓGICA DE COTIZACIÓN

Problema observado: Cotización retorna $0, factores muestran '×' (undefined), lista de problemas vacía.

3.1 BUG CRÍTICO: calculateQuote() retorna null

Archivo: useDiagnostic.js (líneas 7937-7998)

Código actual:

if (!selectedModel.value || selectedFaults.value.length === 0) return null

Problema: Si el modelo no tiene fallas seleccionadas O selectedModel es null, retorna null. El template NO maneja este caso.

Impacto en template (líneas 12521-12533):

quoteData?.baseCost → undefined

quoteData?.complexityFactor.toFixed(2) → ERROR (undefined.toFixed)

quoteData?.valueFactor.toFixed(2) → ERROR (undefined.toFixed)

3.2 BUG: Instrumento sin valor_estimado

Archivo: useDiagnostic.js (líneas 7973-7984)

Código actual:

const estValue = instrument.valor_estimado

if (estValue) { const minValue = estValue.min ... }

Problema: 96% de instrumentos tienen valor_estimado.min = null. El código NO falla pero valueFactor queda en 1.0 siempre, haciendo el cálculo incorrecto.

3.3 BUG: faults.value[faultId] puede ser undefined

Archivo: DiagnosticWizard.vue (líneas 12509-12514)

Código actual:

{{ diagnostic.faults.value[faultId]?.name }}

Problema: Si faultId no existe en faults.json, muestra undefined. El optional chaining (?.) evita crash pero muestra vacío.

4. DATOS INCOMPLETOS EN JSON

4.1 instruments_updated.json - Análisis

| MÉTRICA                            | VALOR      |
| ----------------------------------- | ---------- |
| Total instrumentos                  | 305        |
| Sin valor_estimado (min/max = null) | 295 (96%)  |
| Con components = null               | ~290 (95%) |
| Sin description                     | ~290 (95%) |
| Sin year                            | ~290 (95%) |
| Marcas huérfanas                   | 0 ✓       |
| Fallas inválidas referenciadas     | 0 ✓       |

4.2 Impacto de datos incompletos

valueFactor siempre = 1.0: Sin valor_estimado, el multiplicador por valor de equipo no se aplica

Fallas incorrectas: getApplicableComponents() falla con components null

UI vacía: Modelos sin descripción/año muestran campos vacíos

"Valor est." muestra NaN: (null + null) / 2 = NaN en template

5. BUGS DE UX / ESTADOS VISUALES

5.1 BUG: Botones no funcionales

Archivo: DiagnosticWizard.vue (líneas 12657-12667)

const submitQuote = () => { console.log('Quote submitted:', data) // TODO }

const downloadQuote = () => { console.log('Download PDF') // TODO }

Problema: Botones 'Enviar Cotización' y 'Descargar PDF' solo hacen console.log. Usuario no recibe feedback.

5.2 BUG: formatPrice() con null

Archivo: DiagnosticWizard.vue (líneas 12608-12615)

const formatPrice = (price) => {

  if (!price) return '0'  // ← Retorna '0' para null/undefined

  return new Intl.NumberFormat(...).format(price)

}

Problema: Cuando quoteData es null, formatPrice(null) retorna '0'. Usuario ve '$0' en vez de mensaje informativo.

5.3 BUG: .toFixed() en undefined

Archivo: DiagnosticWizard.vue (líneas 12525-12529)

× {{ quoteData?.complexityFactor.toFixed(2) }}

Problema: Si quoteData es null, quoteData?.complexityFactor es undefined, y undefined.toFixed() causa error silencioso. Muestra solo '×'.

6. FIXES RECOMENDADOS

6.1 Fix de Validaciones (useDiagnostic.js)

// Agregar funciones de validación

const validateName = (name) => /^[A-Za-zÀ-ÿ\s]{2,50}$/.test(name?.trim())

const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)

const validatePhone = (phone) => !phone || /^\+?[0-9]{8,15}$/.test(phone)

// Modificar isValid()

const isValid = () => {

  return selectedBrand.value && selectedModel.value &&

    selectedFaults.value.length > 0 &&

    validateName(clientName.value) &&

    validateEmail(clientEmail.value) &&

    validatePhone(clientPhone.value)

}

6.2 Fix de Cotización (DiagnosticWizard.vue)

// En template, manejar quoteData null

<div v-if="quoteData" class="pricing-breakdown">

<!-- contenido actual -->

</div>

<div v-else class="quote-error">

<p>No se pudo calcular la cotización.</p>

</div>

// Fix para .toFixed() en undefined

× {{ quoteData?.complexityFactor?.toFixed(2) ?? 'N/A' }}

6.3 Fix de Datos (instruments_updated.json)

Opciones para resolver el 96% de instrumentos sin datos:

Valor por defecto: En calculateQuote(), usar valor_estimado de la marca si instrumento no tiene

Completar datos: Script para llenar valor_estimado basado en tier de marca

UI adaptativa: Si no hay valor, mostrar 'Valor a determinar' en vez de $0

7. PRIORIZACIÓN DE FIXES

| # | FIX                                   | ESFUERZO  | IMPACTO |
| - | ------------------------------------- | --------- | ------- |
| 1 | Validaciones de formulario            | 30 min    | ALTO    |
| 2 | Manejo de quoteData null en template  | 15 min    | ALTO    |
| 3 | Valores por defecto para instrumentos | 1 hora    | ALTO    |
| 4 | Feedback visual en botones            | 30 min    | MEDIO   |
| 5 | Completar datos de 295 instrumentos   | 4-8 horas | MEDIO   |

Tiempo total estimado para fixes críticos: ~2 horas

Tiempo total para completar datos: ~4-8 horas (puede automatizarse con script)

8. CONCLUSIÓN

Los bugs identificados explican completamente los síntomas observados:

"123" como nombre: Sin validación de contenido (solo required)

"asdf" como teléfono: type=tel no valida formato

"a@a.d" como email: Validación solo verifica presencia de @

Cotización $0: calculateQuote() retorna null, formatPrice(null) = '0'

Factores "×": undefined.toFixed() falla silenciosamente

Lista vacía: faults.value[faultId] undefined cuando no hay selección

La mayoría de fixes son rápidos (< 2 horas). El trabajo más extenso es completar los datos de los 295 instrumentos con valor_estimado null.

Página  de

* 
* [•••]()
