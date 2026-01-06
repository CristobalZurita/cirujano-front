import { ref, computed } from 'vue'
import brandsData from '@/assets/data/brands.json'
import instrumentsData from '@/assets/data/instruments.json'

/**
 * useInstrumentsCatalog - Central data catalog for brands and instruments
 * 
 * This composable provides:
 * - Unified access to brands and instruments
 * - Brand → Instruments mapping
 * - Image path generation based on instrument ID
 * - No database needed; all data derived from JSON
 */
export function useInstrumentsCatalog() {
  // Raw data
  const brands = ref(brandsData.brands || [])
  const instruments = ref(instrumentsData.instruments || [])

  /**
   * Get a brand by ID
   */
  const getBrandById = (brandId) => {
    return brands.value.find(b => b.id === brandId)
  }

  /**
   * Get all brands, optionally sorted A→Z
   */
  const getAllBrands = (sorted = true) => {
    const list = [...brands.value]
    if (sorted) {
      return list.sort((a, b) => a.name.localeCompare(b.name))
    }
    return list
  }

  /**
   * Get instruments for a specific brand
   * Returns array of instrument objects with image path included
   */
  const getInstrumentsByBrand = (brandId) => {
    return instruments.value
      .filter(inst => inst.brand === brandId)
      .map(inst => enrichInstrument(inst))
      .sort((a, b) => a.model.localeCompare(b.model))
  }

  /**
   * Get a specific instrument by ID
   */
  const getInstrumentById = (instrumentId) => {
    const inst = instruments.value.find(i => i.id === instrumentId)
    return inst ? enrichInstrument(inst) : null
  }

  /**
   * Generate image path for an instrument
   * Convention: /images/instruments/{instrument.id}.jpg
   * Falls back to placeholder if not found
   */
  const getInstrumentImage = (instrument) => {
    // Priority 1: Use existing imagen_url if valid
    if (instrument?.imagen_url) {
      return instrument.imagen_url
    }

    // Priority 2: Generate from convention (use Spanish 'instrumentos' directory)
    if (instrument?.id) {
      return `/images/instrumentos/${instrument.id}.jpg`
    }

    // Priority 3: Placeholder
    return '/images/placeholder.svg'
  }

  /**
   * Enrich instrument object with computed fields
   * (adds image path, formatted price, etc.)
   */
  const enrichInstrument = (inst) => {
    if (!inst) return null

    return {
      ...inst,
      imagePath: getInstrumentImage(inst),
      // Do not include any price/valor fields for frontend rendering
      // Prices are not rendered in the frontend by design
      displayName: `${inst.model} (${inst.year || '?'})`,
      brandLabel: getBrandById(inst.brand)?.name || inst.brand
    }
  }

  /**
   * Search instruments by text
   */
  const searchInstruments = (query) => {
    if (!query || query.trim() === '') return []

    const lower = query.toLowerCase()
    return instruments.value
      .filter(
        inst =>
          inst.model.toLowerCase().includes(lower) ||
          inst.brand.toLowerCase().includes(lower) ||
          inst.description?.toLowerCase().includes(lower)
      )
      .map(inst => enrichInstrument(inst))
  }

  /**
   * Get a summary of the catalog
   */
  const getCatalogStats = computed(() => {
    const brandsCount = brands.value.length
    const instrumentsCount = instruments.value.length
    const instrumentsWithImage = instruments.value.filter(
      i => i.imagen_url || i.image?.url
    ).length

    return {
      totalBrands: brandsCount,
      totalInstruments: instrumentsCount,
      instrumentsWithImage,
      coverage: instrumentsCount > 0
        ? Math.round((instrumentsWithImage / instrumentsCount) * 100)
        : 0
    }
  })

  return {
    // Data refs
    brands,
    instruments,

    // Query methods
    getBrandById,
    getAllBrands,
    getInstrumentsByBrand,
    getInstrumentById,
    getInstrumentImage,
    searchInstruments,

    // Stats
    getCatalogStats
  }
}
