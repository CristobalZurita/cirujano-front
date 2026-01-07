<template>
  <div class="quote-generator">
    <h3>Generador de Cotización (IA)</h3>
    <p class="muted">Prueba rápida: selecciona marca y modelo para generar una estimación de ejemplo.</p>

    <div class="controls">
      <select v-model="brand" @change="onChange">
        <option value="">-- Selecciona marca --</option>
        <option v-for="b in brands" :key="b.id" :value="b.id">{{ b.name }}</option>
      </select>

      <select v-model="model" @change="onChange">
        <option value="">-- Selecciona modelo --</option>
        <option v-for="m in models" :key="m.id" :value="m.id">{{ m.model }}</option>
      </select>

      <button class="btn btn-primary" @click="generate" :disabled="!model">Generar</button>
    </div>

    <div v-if="result" class="result">
      <h4>Resultado de ejemplo</h4>
      <p class="muted">{{ result }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useInstrumentsCatalog } from '@/composables/useInstrumentsCatalog'

const brand = ref('')
const model = ref('')
const result = ref(null)

const { brands, getInstrumentsByBrand } = useInstrumentsCatalog()

const models = computed(() => {
  if (!brand.value) return []
  return getInstrumentsByBrand(brand.value)
})

function onChange() {
  result.value = null
}

function generate() {
  // Simple client-side mock: return a short string using selected model/brand
  const m = models.value.find(x => x.id === model.value)
  result.value = `Estimación de ejemplo para ${m?.displayName || model.value}: diagnóstico y presupuesto en taller.`
}
</script>

<style scoped>
.quote-generator { padding: 1rem; }
.controls { display:flex; gap: 0.75rem; align-items:center; }
.result { margin-top: 1rem; padding: 0.75rem; border-radius:6px; background: rgba(0,0,0,0.03) }
</style>
