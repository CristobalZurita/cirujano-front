import { defineStore } from 'pinia'

export const useInventoryStore = defineStore('inventory', {
  state: () => ({
    items: [],
    loading: false,
    page: 1,
    limit: 20
  }),
  actions: {
    async fetchItems(page = 1, limit = 20, category = null) {
      this.loading = true
      this.page = page
      this.limit = limit
      const q = new URLSearchParams({ limit: String(limit), page: String(page) })
      if (category) q.set('category', category)
      const res = await fetch(`/api/v1/items?${q.toString()}`)
      if (!res.ok) {
        this.items = []
        this.loading = false
        return
      }
      this.items = await res.json()
      this.loading = false
    }
  }
})
