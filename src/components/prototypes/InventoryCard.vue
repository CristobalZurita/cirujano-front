<template>
  <div class="inventory-card p-4 border rounded-md shadow-sm bg-white">
    <div class="flex items-center">
      <div class="flex-1">
        <h3 class="text-lg font-semibold">{{ item.name }}</h3>
        <p class="text-sm text-gray-600">{{ item.category }}</p>
      </div>
      <div class="text-right">
        <div class="text-sm">Stock</div>
        <div class="text-xl font-bold">{{ item.stock }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InventoryCard',
  props: {
    item: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.inventory-card { max-width: 420px }
</style>
