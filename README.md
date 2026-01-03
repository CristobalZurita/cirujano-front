# 📁 ARCHIVOS CORREGIDOS V2 - CIRUJANO DE SINTETIZADORES
## Con tipografías más grandes + responsividad mejorada

---

## 🗂️ DÓNDE VA CADA ARCHIVO

| Archivo | Destino en tu proyecto |
|---------|------------------------|
| `index.html` | `./index.html` (raíz) |
| `_variables.scss` | `./src/scss/_variables.scss` |
| `_typography.scss` | `./src/scss/_typography.scss` |
| `HeroSection.vue` | `./src/vue/content/sections/HeroSection.vue` |
| `Master.vue` | `./src/vue/content/Master.vue` |
| `ReviewsSection.vue` | `./src/vue/content/sections/ReviewsSection.vue` |
| `FaqSection.vue` | `./src/vue/content/sections/FaqSection.vue` |
| `HomePage.vue` | `./src/vue/content/pages/HomePage.vue` |
| `vite.config.js` | `./vite.config.js` (raíz) |
| `client-instagram.svg` | `./public/images/clients/client-instagram.svg` |

---

## ⚠️ PROBLEMA DEL HERO QUE NO SE VE

**El Hero SÍ existe**, pero si entras con `#about` en la URL, salta directo a esa sección.

### Solución:
- Entra a `http://localhost:5173/` (sin hash)
- O entra a `http://localhost:5173/#hero`

El Hero con el logo y "Descubre más" aparecerá correctamente.

---

## 📏 CAMBIOS EN TAMAÑOS DE FUENTE

### Textos (body, párrafos)
| Clase | ANTES | AHORA |
|-------|-------|-------|
| text-1 | 0.85rem | **1.0rem** |
| text-2 | 0.9rem | **1.1rem** |
| text-3 | 0.95rem | **1.15rem** |
| text-4 | 1.0rem | **1.2rem** |
| text-5 | 1.05rem | **1.25rem** |

### Títulos (headings)
| Elemento | ANTES | AHORA |
|----------|-------|-------|
| h1 | 3rem | **3.5rem** |
| h2 | 2.5rem | **2.8rem** |
| h3 | 2rem | **2.2rem** |
| h4 | 1.5rem | **1.7rem** |
| h5 | 1.3rem | **1.4rem** |
| h6 | 1.1rem | **1.2rem** |

---

## 📺 RESPONSIVIDAD PARA PANTALLAS GRANDES

Agregado soporte para TV 4K, 8K y ultra-wide en `_typography.scss`

---

**Fecha:** 2 de enero de 2026
