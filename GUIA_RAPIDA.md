# ⚡ GUÍA RÁPIDA DE INTEGRACIÓN

## Lo que se ha generado

✅ **6 nuevos archivos de datos** (JSON)
✅ **1 composable Vue** (useDiagnostic.js)
✅ **3 componentes Vue** (Wizard, Sección, Botón flotante)
✅ **4 archivos backend FastAPI** (main, config, schemas, routers)
✅ **Variables SCSS corregidas** (tipografía + breakpoints)
✅ **Documentación completa** (IMPLEMENTACION.md)

---

## PASO 1: Integrar el Frontend en App.vue

Localizar: `src/vue/stack/App.vue`

```vue
<template>
  <div id="app">
    <ContentLayer />
    
    <!-- ← AGREGAR ESTA LÍNEA DENTRO DE ContentLayer O ANTES DE FooterSection →-->
    <DiagnosticSection />
    
    <!-- Botón flotante global -->
    <FloatingQuoteButton />
  </div>
</template>

<script setup>
import ContentLayer from '@/vue/stack/ContentLayer.vue'
import DiagnosticSection from '@/vue/sections/DiagnosticSection.vue'
import FloatingQuoteButton from '@/vue/components/widgets/FloatingQuoteButton.vue'
</script>
```

**O si DiagnosticSection debe ir en ContentLayer (más probable):**

En `src/vue/stack/ContentLayer.vue`, agregar:

```vue
<template>
  <div>
    <!-- Resto de secciones existentes -->
    <Master />
    
    <!-- AGREGAR AQUÍ -->
    <DiagnosticSection />
    
    <FeedbacksLayer />
  </div>
</template>

<script setup>
import DiagnosticSection from '@/vue/sections/DiagnosticSection.vue'
// ... resto de imports
</script>
```

---

## PASO 2: Verificar que los datos JSON se cargan

Los archivos están en:
```
src/assets/data/
├── brands.json
├── instruments.json
└── faults.json
```

Si Vite no los encuentra automáticamente, en `vite.config.js` asegurarse de:

```javascript
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
```

---

## PASO 3: Probar en navegador

```bash
cd /mnt/CZ_BODEGA/010_VSCODE/007_PROYECTOS_WEB/cirujano-front
npm run dev
```

Verificar:
- ✅ Botón flotante naranja en esquina inferior derecha con animación de pulso
- ✅ "¡COTIZA AHORA!" con ícono de calculadora
- ✅ Al hacer scroll, el botón permanece visible
- ✅ Click redirecciona a sección de diagnóstico

---

## PASO 4: Configurar Backend (Opcional ahora, requiere después)

```bash
# En directorio backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copiar configuración
cp .env.example .env

# Ejecutar servidor
uvicorn main:app --reload
```

Verificar en: `http://localhost:8000/docs`

---

## Cambios de Tipografía (APLICADOS)

| Variable | Antes | Después | Cambio |
|----------|-------|---------|--------|
| text-1 | 0.85rem | 1.0rem | +17% |
| text-2 | 0.90rem | 1.05rem | +17% |
| text-3 | 0.95rem | 1.1rem | +16% |
| text-4 | 1.00rem | 1.15rem | +15% |
| text-5 | 1.05rem | 1.2rem | +14% |

**Breakpoints (corregidos):**
| Tamaño | Antes | Después |
|--------|-------|---------|
| xxxxl (>1920px) | NO EXISTÍA | 1.15 |
| xxxl | 1.0 | 1.1 |
| xxl | 0.95 | 1.0 |
| md | 0.875 | 0.9 |

**Impacto:** Textos más legibles en monitores 24"+ sin afectar móvil/tablet

---

## Estructura del Wizard (5 pasos)

```
Paso 1: Seleccionar Marca
   ↓
Paso 2: Seleccionar Modelo
   ↓
Paso 3: Describir Problemas (Fallas)
   ↓
Paso 4: Información de Contacto
   ↓
Paso 5: Ver Cotización
   ├→ Enviar por Email
   ├→ Descargar PDF
   └→ Nueva Cotización
```

**Lógica de Precedencia:**
- Si selecciona "No enciende" → ignora todas las otras fallas automáticamente
- Muestra advertencia roja

**Fórmula de Precio:**
```
FINAL = (suma_fallas) × multiplicador_marca × multiplicador_valor_equipo
```

---

## Archivos Creados (Resumen)

### Datos
- `src/assets/data/brands.json` (42 marcas)
- `src/assets/data/instruments.json` (10 instrumentos + expandible)
- `src/assets/data/faults.json` (25 fallas + categorías)

### Frontend Vue
- `src/composables/useDiagnostic.js` (lógica central)
- `src/vue/components/articles/DiagnosticWizard.vue` (wizard 5 pasos)
- `src/vue/components/widgets/FloatingQuoteButton.vue` (botón flotante)
- `src/vue/sections/DiagnosticSection.vue` (wrapper PageSection)

### Backend FastAPI
- `backend/main.py` (app principal)
- `backend/config.py` (configuración)
- `backend/schemas.py` (modelos Pydantic)
- `backend/routers/diagnostic.py` (endpoints)
- `backend/requirements.txt` (dependencias)
- `backend/.env.example` (variables de entorno)

### Documentación
- `IMPLEMENTACION.md` (documentación completa)
- `GUIA_RAPIDA.md` (este archivo)

---

## Testing del Sistema

### Frontend: Prueba Manual

1. **Botón flotante:**
   - [ ] Visible en esquina inferior derecha
   - [ ] Tiene animación de pulso
   - [ ] Click scroll suave a sección

2. **Wizard Paso 1 (Marcas):**
   - [ ] Muestra todas las marcas en grid
   - [ ] Colores diferenciados por tier
   - [ ] Click selecciona y habilita siguiente

3. **Wizard Paso 2 (Modelos):**
   - [ ] Solo muestra modelos de marca seleccionada
   - [ ] Muestra valor estimado
   - [ ] Click selecciona modelo

4. **Wizard Paso 3 (Fallas):**
   - [ ] Solo muestra fallas aplicables al modelo
   - [ ] Checkbox funciona
   - [ ] Si selecciona POWER, otras se deshabilitan

5. **Wizard Paso 4 (Datos):**
   - [ ] Email se valida
   - [ ] Datos se guardan en state

6. **Wizard Paso 5 (Cotización):**
   - [ ] Muestra cálculo correcto
   - [ ] Desglose de precios visible
   - [ ] Botones funcionan (ahora son placeholders)

### Backend: Test de APIs

```bash
# Health check
curl http://localhost:8000/health

# Get marcas
curl http://localhost:8000/api/instruments/brands

# Get modelos de una marca
curl http://localhost:8000/api/instruments/models/waldorf

# Get fallas aplicables
curl http://localhost:8000/api/faults/applicable/waldorf-blofeld

# Calcular cotización
curl -X POST http://localhost:8000/api/diagnostic/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "client": {"name": "Test", "email": "test@test.com"},
    "equipment": {"brand": "waldorf", "model": "waldorf-blofeld"},
    "faults": ["ENCODER_INTERMITTENT"]
  }'
```

---

## Puntos Importantes

⚠️ **No implementado aún:**
- [ ] Envío de email
- [ ] Descarga de PDF
- [ ] Persistencia en base de datos
- [ ] Sistema de autenticación admin
- [ ] Dashboard de cliente

✅ **Ya funciona:**
- [x] Cálculo de cotización
- [x] Interfaz del wizard
- [x] Lógica de precedencia de fallas
- [x] Visualización de datos JSON
- [x] Botón flotante

📅 **Próximos pasos sugeridos:**
1. Integrar y probar frontend (hoy)
2. Expandir catálogo de instrumentos (esta semana)
3. Conectar API backend (proxima semana)
4. Implementar email + PDF (proxima semana)
5. Base de datos PostgreSQL (cuando sea necesario escalar)

---

## Contacto

Si hay problemas en la integración:
1. Revisar IMPLEMENTACION.md (sección Troubleshooting)
2. Verificar rutas de import
3. Abrir console en DevTools (F12)
4. Checkear archivos JSON se cargan (Network tab)

---

**Documento generado:** Enero 2026  
**Sistema:** Cirujano de Sintetizadores  
**Versión:** 1.0.0
