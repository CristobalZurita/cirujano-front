<template>
  <div>
    <h2>Panel</h2>
    <div class="grid">
      <div class="card">Quick stats</div>
      <div class="card">Reparaciones recientes</div>
      <div class="card">Alertas de inventario</div>
    </div>
  </div>
</template>
<script setup>
// Component placeholder - integrar datos reales desde stores
</script>
<style scoped>
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.card { padding: 12px; border: 1px solid #ddd; border-radius: 6px; }
</style>
