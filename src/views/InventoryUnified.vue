<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Inventario Unificado (POC)</h1>
    <div class="mb-4">
      <input v-model="filter" @keyup.enter="load" placeholder="Filtrar por categoría" class="input" />
      <button @click="load" class="btn btn-primary ml-2">Buscar</button>
    </div>

    <div v-if="store.loading">Cargando...</div>
    <div v-else class="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      <InventoryCard v-for="it in store.items" :key="it.id" :item="it" />
    </div>
  </div>
</template>

<script>
import { useInventoryStore } from '@/stores/inventory'
import InventoryCard from '@/components/prototypes/InventoryCard.vue'
import { ref, onMounted } from 'vue'

export default {
  name: 'InventoryUnified',
  components: { InventoryCard },
  setup() {
    const filter = ref('')
    const store = useInventoryStore()
    const load = () => store.fetchItems(1, 20, filter.value || null)
    onMounted(() => load())
    return { filter, store, load }
  }
}
</script>

<style scoped>
.input { padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px }
.btn { padding: 0.5rem 0.75rem }
</style>
