# Cirujano de Sintetizadores - Guía de Implementación

## Estructura de Archivos Generada

### Frontend (Vue 3 + Vite)

```
src/
├── assets/
│   └── data/
│       ├── brands.json          # Catálogo de 42+ marcas
│       ├── instruments.json     # Catálogo de 10+ instrumentos
│       └── faults.json          # 25+ tipos de fallas clasificadas
├── composables/
│   └── useDiagnostic.js         # Lógica central del diagnóstico
├── scss/
│   └── _variables.scss          # Variables SCSS actualizadas (CORREGIDAS)
└── vue/
    ├── components/
    │   ├── articles/
    │   │   └── DiagnosticWizard.vue     # Wizard de diagnóstico (5 pasos)
    │   └── widgets/
    │       └── FloatingQuoteButton.vue  # Botón flotante con animación
    └── sections/
        └── DiagnosticSection.vue         # Sección que envuelve el wizard
```

### Backend (FastAPI + Python)

```
backend/
├── main.py                      # Aplicación FastAPI principal
├── config.py                    # Configuración y settings
├── schemas.py                   # Modelos Pydantic para validación
├── routers/
│   └── diagnostic.py            # Endpoints de diagnóstico y cotización
├── requirements.txt             # Dependencias Python
├── .env.example                 # Variables de entorno (ejemplo)
└── .env                         # Variables de entorno (no incluir en git)
```

## Cambios Realizados

### ✅ FASE 1: Correcciones Inmediatas

#### 1. **Tipografía Corregida** (`_variables.scss`)
- Text-1 a Text-5: Aumentadas en +14-17% para monitores grandes
- Nuevas escalas base más legibles
- Breakpoints invertidos ahora correctos

**Antes:**
```scss
$texts-breakpoint-multipliers: (
    xxxl: 1,        // Incorrecto, debería escalar arriba
    xxl: 0.95,
    md: 0.875,
    sm: 0.85
);
```

**Después:**
```scss
$texts-breakpoint-multipliers: (
    xxxxl: 1.15,    // NUEVO para 4K
    xxxl: 1.1,      // Antes: 1.0
    xxl: 1.0,       // Antes: 0.95
    xxl: 1.0,
    md: 0.9,        // Antes: 0.875
    sm: 0.85
);
```

#### 2. **Botón Flotante de Cotización** (`FloatingQuoteButton.vue`)
- ✅ Posicionado en esquina inferior derecha (fixed)
- ✅ Animación de pulso sutil (2s loop)
- ✅ Color naranja primario (#EC6B00)
- ✅ Tooltip "Diagnóstico gratis"
- ✅ Responsive: Oculta texto en móvil
- ✅ Scroll suave a sección de diagnóstico

#### 3. **Referencias a Thaddeus Cahill**
- ❌ Actualmente: No hay referencias en el código analizado
- ✅ Verificado en VOLCADO07.txt - ninguna mención
- ℹ️ Consultar si hay referencias en otros archivos

### ✅ FASE 2: Sistema de Cotización (En Construcción)

#### 1. **Datos Base (JSON)**

**brands.json** (42 marcas + tiers):
```json
{
  "brands": [
    { "id": "moog", "name": "Moog", "tier": "legendary", "founded": 1954 },
    { "id": "waldorf", "name": "Waldorf", "tier": "professional", "founded": 1992 },
    // ... 40+ marcas más
  ]
}
```

**instruments.json** (10+ instrumentos base):
```json
{
  "instruments": [
    {
      "id": "waldorf-blofeld",
      "brand": "waldorf",
      "model": "Blofeld",
      "type": "Digital Synthesizer",
      "components": {
        "encoders_rotativos": 4,
        "botones": 23,
        "lcd": true,
        "usb": true,
        "midi_din": true
      },
      "valor_estimado": { "min": 400000, "max": 600000 },
      "fallas_comunes": [...]
    },
    // ... 9+ instrumentos más
  ]
}
```

**faults.json** (25+ fallas con precedencia):
```json
{
  "faults": {
    "POWER": {
      "name": "No enciende / Quemado",
      "category": "critical",
      "precedence": 1,
      "isPrecedence": true,
      "basePrice": 150000
    },
    "ENCODER_INTERMITTENT": {
      "name": "Encoder/Potenciómetro intermitente",
      "category": "controls",
      "basePrice": 18000
    },
    // ... 23+ fallas más
  }
}
```

#### 2. **Composable Vue: `useDiagnostic.js`**

Estado reactivo centralizado:
```javascript
const diagnostic = useDiagnostic()

// State
diagnostic.selectedBrand     // String (id)
diagnostic.selectedModel     // String (id instrumento)
diagnostic.selectedFaults    // Array[String] (ids de fallas)
diagnostic.clientName        // String
diagnostic.clientEmail       // String (validado)
diagnostic.clientPhone       // String

// Methods
diagnostic.getModelsByBrand(brandId)         // Array[Instrument]
diagnostic.getAvailableFaults()              // Array[Fault]
diagnostic.getEffectiveFaults()              // Array (con reglas de precedencia)
diagnostic.calculateQuote()                  // { finalCost, baseCost, ... }
diagnostic.addFault(faultId)                 // Agregar con validación
diagnostic.removeFault(faultId)              // Remover
diagnostic.getQuoteData()                    // Objeto para enviar a API
```

**Lógica de Precedencia (CRÍTICO):**
```javascript
// Si se selecciona "No enciende", se ignora todo lo demás
if (fault.isPrecedence) {
    selectedFaults.value = [faultId]  // Reemplaza todo
}
```

#### 3. **Componente: `DiagnosticWizard.vue`** (5 pasos)

**Paso 1:** Seleccionar marca
- Grid de marcas ordenadas por tier
- Visual diferenciador (color badge)
- Filtro: Tier Legendario, Profesional, etc.

**Paso 2:** Seleccionar modelo
- Dropdown dinámico según marca seleccionada
- Muestra: Tipo, año, valor estimado, descripción
- Solo modelos registrados en la BD

**Paso 3:** Descripción de problemas
- Checkboxes de fallas (solo las aplicables al modelo)
- Categorización por color
- Advertencia roja si se selecciona "POWER"
- Precio base visible por falla

**Paso 4:** Información de contacto
- Campos: Nombre, Email, Teléfono
- Validación básica en frontend
- Email requerido

**Paso 5:** Resultado de cotización
- Resumen de equipo
- Desglose de precios:
  - Subtotal de fallas
  - Multiplicador de complejidad (tier)
  - Multiplicador de valor equipo
  - **TOTAL FINAL**
- Botones:
  - Enviar cotización (email)
  - Descargar PDF
  - Nueva cotización

#### 4. **Fórmula de Precio (Implementada)**

```
PRECIO_FINAL = Σ(precio_base_falla) × factor_complejidad × factor_valor

Factor Complejidad (por tier de marca):
  Legendary     → 1.8
  Professional → 1.5
  Standard     → 1.2
  Specialized  → 1.3
  Boutique     → 1.4
  Historic     → 1.3

Factor Valor Equipo (por valor estimado):
  < $500k CLP          → 1.0
  $500k - $2M CLP      → 1.3
  $2M - $5M CLP        → 1.6
  > $5M CLP (ej: J-8)  → 2.0
```

#### 5. **Componente: `DiagnosticSection.vue`**
- Envuelve el Wizard en `PageSection`
- ID: "diagnostic-section" (para scroll desde botón flotante)
- Fondo gradiente (naranja + beige de identidad)

### Backend FastAPI

#### 1. **Estructura `main.py`**
```python
# CORS habilitado para desarrollo
# Health check endpoint
# Auto-documentación OpenAPI en /docs
```

#### 2. **Modelos Pydantic (`schemas.py`)**
- ClientCreate, InstrumentResponse, QuoteResponse, etc.
- Enums: RepairStatus, InstrumentTier, FaultCategory
- Validación automática de email, rangos, etc.

#### 3. **Endpoints (`routers/diagnostic.py`)**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/instruments/brands` | Todas las marcas |
| GET | `/api/instruments/models/{brand_id}` | Modelos de una marca |
| GET | `/api/instruments/{instrument_id}` | Detalles de instrumento |
| GET | `/api/faults` | Todas las fallas |
| GET | `/api/faults/applicable/{instrument_id}` | Fallas aplicables |
| POST | `/api/diagnostic/calculate` | Calcular cotización |
| POST | `/api/quotes` | Crear cotización (TODO) |
| GET | `/api/quotes/{quote_id}` | Obtener cotización (TODO) |

#### 4. **Configuración (`config.py`)**
```python
Settings:
  - DATABASE_URL: SQLite (default) o PostgreSQL
  - SECRET_KEY: JWT
  - SMTP: Configuración de email
  - service_multipliers: Factores de complejidad
  - value_multipliers: Factores de valor equipo
```

## Instalación y Setup

### Frontend (Vue)

1. **Los archivos ya están creados**, solo falta integrar en App.vue:

```vue
<template>
  <div id="app">
    <!-- Componentes existentes -->
    <HeroSection />
    <AboutSection />
    
    <!-- NUEVO: Sección de diagnóstico -->
    <DiagnosticSection />
    
    <!-- Resto de secciones -->
    <ContactSection />
    <FooterSection />
    
    <!-- NUEVO: Botón flotante -->
    <FloatingQuoteButton />
  </div>
</template>

<script setup>
import DiagnosticSection from '@/vue/sections/DiagnosticSection.vue'
import FloatingQuoteButton from '@/vue/components/widgets/FloatingQuoteButton.vue'
</script>
```

2. **Verificar que los archivos JSON se cargan correctamente:**

```bash
# Verificar rutas en composable
src/assets/data/brands.json
src/assets/data/instruments.json
src/assets/data/faults.json
```

3. **Compilar y probar:**

```bash
npm run dev
# Acceder a http://localhost:5173
# Botón flotante debe estar visible en esquina inferior derecha
```

### Backend (FastAPI)

1. **Crear ambiente virtual:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows
```

2. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno:**

```bash
cp .env.example .env
# Editar .env con valores reales (SECRET_KEY, DATABASE_URL, etc.)
```

4. **Ejecutar servidor:**

```bash
# Desarrollo con auto-reload
uvicorn main:app --reload

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000
```

5. **Verificar endpoints:**

```
http://localhost:8000/docs         # Swagger UI
http://localhost:8000/redoc        # ReDoc
http://localhost:8000/health       # Health check
```

## Próximos Pasos Inmediatos

### Para Poner en Producción:

1. **Base de Datos:**
   - [ ] Migrar de SQLite a PostgreSQL
   - [ ] Crear modelos SQLAlchemy (models.py)
   - [ ] Configurar Alembic para migrations
   - [ ] Poblar BD con 20+ instrumentos (expandir JSON)

2. **Integración Frontend-Backend:**
   - [ ] Conectar composable `useDiagnostic.js` con endpoints `/api`
   - [ ] Implementar llamadas fetch/axios
   - [ ] Manejo de errores y loading states

3. **Email y Cotizaciones:**
   - [ ] Implementar envío de email (EmailJS o SMTP)
   - [ ] Template HTML para cotización
   - [ ] Descarga PDF (usar jsPDF o similar)

4. **Autenticación:**
   - [ ] Sistema de login para panel admin
   - [ ] JWT tokens
   - [ ] Proteger endpoints admin

5. **Portal de Clientes:**
   - [ ] Dashboard con estado de reparación
   - [ ] Historial de cotizaciones
   - [ ] Sistema de notificaciones

### Datos Faltantes para Expandir:

1. **Instrumentos (expandir `instruments.json`):**
   ```
   Waldorf: Staccato, Pulse, Strobe, M-Scaler
   Roland: TR-909, Juno-106, Juno-60, CR-78
   Korg: Monologue, Monotron, Monotron Delay, Volca FM
   Sequential: Prophet-5 Rev4, Prophet X, OB-6
   Moog: Moog One, Moogerfoogler, Sub Phatty
   Access: Virus B, Virus KC, Virus Snow
   Elektron: Syntakt, Rytm MkII, Analog Four MkII
   Nord: Nord Modular G2, Nord A1, Nord Lead A1
   ```

2. **Precios Base de Fallas (refinar `faults.json`):**
   - Diagnóstico gratis (ya implementado)
   - Por tecla: $12,000
   - Por botón: $15,000
   - Por encoder: $18,000
   - Por fader: $20,000
   - LCD nuevo: $35,000
   - etc.

3. **Referencias a Thaddeus Cahill:**
   - Buscar en archivos Vue
   - Buscar en strings.js
   - Eliminar completamente

## Troubleshooting

### "No se ve el botón flotante"
- Verificar que `FloatingQuoteButton.vue` está importado en App.vue
- Verificar z-index: 999 en CSS
- Revisar position: fixed en viewport

### "Fallas no se muestran según el instrumento"
- Verificar que instrument.json y faults.json están en rutas correctas
- Revisar lógica en `getAvailableFaults()` en composable
- Console.log para debugging

### "API retorna 404 en /api/instruments/brands"
- Verificar que `main.py` importa el router
- Asegurarse que rutas JSON se cargan desde path correcto
- Verificar CORS configuration

### "Cotización no calcula bien"
- Debuggear `calculateQuote()` en composable
- Verificar multiplicadores en config.py
- Console.log para ver valores intermedios

## Notas Técnicas

### Por qué esta arquitectura:

1. **Datos en JSON (no BD aún):**
   - Permite iterar rápido sin configurar DB
   - Datos son versionables en git
   - Fácil de expandir manualmente
   - Migración a PostgreSQL es simple después

2. **Composable en Vue (lógica centralizada):**
   - Reutilizable en múltiples componentes
   - Testing más fácil
   - Separa lógica de UI

3. **FastAPI (no Django/Flask):**
   - Async/await nativo (más rápido)
   - Auto-documentación OpenAPI
   - Validación automática Pydantic
   - Mejor para APIs modernas

4. **Precedencia de fallas:**
   - Si "No enciende" → ignorar todo lo demás
   - Reduce falsos diagnósticos
   - Costo diferenciado apropiadamente

## Referencias

- Vue 3 Composition API: https://vuejs.org/guide/extras/composition-api-faq.html
- FastAPI Docs: https://fastapi.tiangolo.com/
- Manual de Identidad: Colores, tipografía ya implementados
- VOLCADO07.txt: Estructura actual del frontend

---

**Versión:** 1.0.0  
**Fecha:** Enero 2026  
**Autor:** Sistema de Generación Automatizada
