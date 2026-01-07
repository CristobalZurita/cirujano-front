# 🔧 AUDITORÍA TÉCNICA COMPLETA - ACTUALIZACIÓN
## Cirujano de Sintetizadores
### Sistema de Gestión para Taller de Reparación de Instrumentos Electrónicos

**Fecha:** 6 Enero 2026  
**Versión:** 2.1 (Cruce Auditoría Original + Volcado Real)  
**Dominio:** www.cirujanodesintetizadores.cl  

---

# ÍNDICE

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Matriz de Requisitos: Auditoría vs Realidad](#2-matriz-de-requisitos)
3. [Análisis Detallado por Módulo](#3-análisis-detallado)
4. [Archivos Existentes vs Faltantes](#4-archivos-existentes-vs-faltantes)
5. [Seguridad: Estado Actual](#5-seguridad-estado-actual)
6. [Plan de Acción Priorizado](#6-plan-de-acción)
7. [Estimaciones de Tiempo](#7-estimaciones)

---

# 1. RESUMEN EJECUTIVO

## Hallazgo Principal

**El proyecto está más avanzado de lo que la auditoría original indicaba.**

| Métrica | Auditoría Original | Realidad (Volcado) | Diferencia |
|---------|-------------------|-------------------|------------|
| Backend completado | 60% | **75%** | +15% |
| Frontend completado | 55% | **70%** | +15% |
| Autenticación | 80% | **90%** | +10% |
| Sistema cotización | 30% | **50%** | +20% |
| Drag & Drop imágenes | 0% | **80%** | +80% |
| Rate limiting | 0% | **100%** | +100% |
| Sistema auditoría | 0% | **100%** | +100% |
| Tests unitarios | ??? | **8 archivos** | N/A |

## Veredicto

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   ✅ BASE SÓLIDA - El proyecto NO está mal                         │
│                                                                     │
│   Lo que FALTA es principalmente:                                   │
│   1. CONECTAR las piezas existentes                                │
│   2. Crear el endpoint de cotización que une todo                  │
│   3. Hardening de seguridad para producción                        │
│   4. Contenido legal (disclaimers, políticas)                      │
│                                                                     │
│   Tiempo estimado para MVP: 1-2 semanas de trabajo enfocado        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

# 2. MATRIZ DE REQUISITOS: AUDITORÍA vs REALIDAD

## 2.1 Las 25 Funcionalidades Originales

| # | Funcionalidad | Auditoría | Volcado Real | Estado |
|---|--------------|-----------|--------------|--------|
| 1 | Cliente sin cuenta cotiza online | 30% | **50%** | ⚠️ Falta endpoint |
| 2 | Diagnóstico visual interactivo | 0% | **40%** | ⚠️ Componentes existen |
| 3 | Cuestionario "aguas abajo" | 0% | **80%** | ✅ `useDiagnostic.js` |
| 4 | Cotización aproximada + disclaimer | 0% | **30%** | ⚠️ Falta disclaimer |
| 5 | Creación cuenta para agendar | 80% | **90%** | ✅ Auth completo |
| 6 | Panel técnico gestión fichas | 50% | **70%** | ✅ `RepairManager.vue` |
| 7 | Panel cliente ver avance | 0% | **60%** | ✅ `DashboardPage.vue` |
| 8 | Carrito repuestos interno | 0% | 0% | ❌ No existe |
| 9 | Tracking tipo DHL | 0% | **20%** | ⚠️ `RepairTimeline.vue` |
| 10 | APIs tracking (AliExpress, etc) | 0% | 0% | ❌ No existe |
| 11 | Sistema tickets + SLA | 0% | 0% | ❌ No existe |
| 12 | Respuestas automáticas IA | 0% | 0% | ❌ No existe |
| 13 | Web autónoma 24/7 | 0% | **30%** | ⚠️ Parcial |
| 14 | Detección instrumento IA | 0% | **60%** | ✅ `ai_detector.py` |
| 15 | Drag & Drop imágenes | 0% | **90%** | ✅ `ImageUploader.vue` |
| 16 | Todo en base de datos | 50% | **80%** | ✅ SQLAlchemy completo |
| 17 | Notificaciones automáticas | 0% | **40%** | ⚠️ `email_service.py` |
| 18 | Políticas claras | 0% | **10%** | ❌ Solo placeholder |
| 19 | Google Calendar | 0% | 0% | ❌ No existe |
| 20 | 🎬 Streaming en vivo | 0% | 0% | ❌ Hardware listo, SW no |
| 21 | YouTube auto-publicación | 0% | 0% | ❌ No existe |
| 22 | Portfolio automático | 0% | 0% | ❌ No existe |
| 23 | Flujo trabajo técnico | 0% | **60%** | ✅ Dashboard admin |
| 24 | Cotización JUSTA (50% max) | 0% | **30%** | ⚠️ Lógica parcial |
| 25 | SSL/Seguridad producción | 0% | **50%** | ⚠️ Rate limit sí, CORS no |

### Leyenda
- ✅ **Implementado** (>70%)
- ⚠️ **Parcial** (30-70%)
- ❌ **No existe** (<30%)

---

## 2.2 Descubrimientos Positivos (No en Auditoría Original)

Cosas que **EXISTEN** en el volcado pero la auditoría original NO mencionaba:

| Componente | Descripción | Ubicación |
|------------|-------------|-----------|
| **Sistema de Auditoría** | Logging de eventos con `create_audit()` | `logging_service.py` |
| **Rate Limiting** | slowapi configurado, 20/min en uploads | `ratelimit.py`, `uploads.py` |
| **Tests Unitarios** | 8 archivos de tests | `backend/tests/` |
| **Validación Imágenes** | `validate_image()` completo | `utils/uploads.py` |
| **Modelo Payment** | CRUD + idempotencia | `payments.py` |
| **Stock Movements** | Control de inventario | `stock_movement.py` |
| **PDF Generator** | Generación de documentos | `pdf_generator.py` |
| **Quote Calculator** | Base del calculador | `quote_calculator.py` |
| **Schemas Pydantic** | DTOs completos | `schemas/__init__.py` |
| **Composables Vue** | 15+ composables funcionales | `src/composables/` |
| **Stores Pinia** | 8 stores configurados | `src/stores/` |

---

# 3. ANÁLISIS DETALLADO POR MÓDULO

## 3.1 Sistema de Cotización Inteligente

### Lo que la Auditoría Pedía:
```
1. Selección: Marca → Modelo → Foto
2. Diagnóstico visual interactivo (áreas clickeables)
3. Cuestionario aguas abajo (POWER bloquea resto)
4. Cotización con disclaimer
5. Separación Cliente vs Técnico (cliente NO ve valor mercado)
```

### Lo que EXISTE en el Volcado:

**Frontend:**
```
✅ src/composables/useDiagnostic.js
   - getBrands(), getModelsByBrand(), getInstrument()
   - getApplicableComponents() - detecta componentes por instrumento
   - getAvailableFaults() - fallas aplicables
   - addFault(), removeFault(), clearFaults()
   - ✅ LÓGICA DOWNSTREAM: fault.isPrecedence bloquea resto
   
✅ src/composables/useInstrumentsCatalog.js
   - Acceso unificado a brands.json e instruments.json
   - getBrandById(), getAllBrands()
   - getInstrumentsByBrand()
   
✅ src/vue/components/ai/
   - ImageUploader.vue - Drag & drop funcional
   - FaultDetector.vue - Detección de fallas
   - FaultMarker.vue - Marcador visual
   - QuoteGenerator.vue - Generador cotización
   - AIAnalysisResult.vue - Resultados IA

✅ src/vue/components/articles/DiagnosticWizard.vue
   - Wizard de diagnóstico
```

**Backend:**
```
✅ backend/app/api/v1/endpoints/brands.py
   - GET /brands - Lista marcas ordenadas A-Z
   - GET /brands/{id}/models - Instrumentos de una marca

✅ backend/app/api/v1/endpoints/instruments.py
   - GET /instruments/{id} - Detalle instrumento
   - GET /instruments/{id}/image - Imagen

✅ backend/app/services/quote_calculator.py
   - Existe pero contenido parcial
   - Tiene lógica de tier y complexity_factor

⚠️ backend/app/routers/diagnostic.py
   - Existe pero parcialmente implementado
```

**Datos JSON (El Corazón):**
```json
// src/assets/data/brands.json
{
  "brands": [
    {
      "id": "moog",
      "name": "Moog",
      "tier": "legendary",  // ← TIERS IMPLEMENTADOS
      "founded": 1953,
      "country": "USA"
    }
  ]
}

// src/assets/data/instruments.json
{
  "instruments": [
    {
      "id": "moog-minimoog",
      "brand": "moog",
      "model": "Minimoog Model D",
      "components": {
        "faders": 0,
        "encoders_rotativos": 0,
        "botones": 10,
        "lcd": false,
        "rueda_pitch": true
      },
      "valor_min": 3500000,  // ← VALORES EN CLP
      "valor_max": 8000000,
      "imagen_url": "/images/instrumentos/moog-minimoog.jpg"
    }
  ]
}

// src/assets/data/faults.json
{
  "faults": {
    "POWER": {
      "id": "POWER",
      "name": "No enciende",
      "basePrice": 35000,
      "isPrecedence": true  // ← DOWNSTREAM LÓGICA
    }
  }
}
```

### ❌ LO QUE FALTA:

```python
# NO EXISTE: backend/app/routers/quotation.py

@router.post("/api/v1/quotations/estimate")
async def estimate_quotation(request: QuotationRequest):
    """
    ENDPOINT CRÍTICO FALTANTE
    
    Input:
    - brand_id: str
    - instrument_id: str  
    - faults: List[str]
    - client_info: Optional[ClientInfo]
    
    Output:
    - min_price: int
    - max_price: int
    - breakdown: List[FaultCost]
    - disclaimer: str
    - tier: str
    - max_recommended: int (50% del valor)
    """
    pass
```

```vue
<!-- NO EXISTE: DisclaimerModal.vue -->
<template>
  <div class="disclaimer">
    ⚠️ IMPORTANTE - LEA ANTES DE CONTINUAR
    Esta cotización es INDICATIVA y NO VINCULANTE.
    [checkbox] Acepto las condiciones
    [Continuar]
  </div>
</template>
```

---

## 3.2 Sistema de Autenticación

### Lo que EXISTE (Más completo de lo esperado):

**Backend:**
```
✅ backend/app/api/v1/endpoints/auth.py
   - POST /auth/login - Login con JWT
   - POST /auth/register - Registro
   - GET /auth/me - Usuario actual
   - POST /auth/refresh - Refresh token

✅ backend/app/core/security.py
   - JWT completo
   - Bcrypt para passwords
   - Token expiration configurado

✅ backend/app/core/dependencies.py
   - get_current_user()
   - Middleware de autenticación

✅ backend/app/schemas/auth.py
   - Token, TokenData
   - LoginRequest, RegisterRequest
   - PasswordResetRequest, PasswordResetConfirm
   - RefreshTokenRequest
```

**Frontend:**
```
✅ src/composables/useAuth.js
   - register(), login(), logout()
   - checkAuth(), fetchUserInfo()
   - refreshAccessToken()
   - isAuthenticated, isAdmin (computed)

✅ src/stores/auth.js
   - Estado global de autenticación

✅ src/vue/components/auth/
   - LoginForm.vue
   - RegisterForm.vue
   - PasswordReset.vue
   - AccountDelete.vue
```

### Estado: ✅ 90% Completo

Solo falta:
- Verificación de email (opcional)
- OAuth social (opcional)

---

## 3.3 Sistema de Reparaciones

### Lo que EXISTE:

**Backend:**
```
✅ backend/app/models/repair.py
   - Modelo completo con estados

✅ backend/app/routers/repair.py
   - GET /repairs - Lista
   - POST /repairs - Crear
   - PUT /repairs/{id} - Actualizar
   - DELETE /repairs/{id} - Eliminar
   - ✅ Auditoría integrada (create_audit)

✅ backend/app/crud/repair.py
   - Operaciones CRUD

✅ backend/app/schemas/repair.py (en __init__.py)
   - RepairCreate, RepairRead, RepairDetailRead
```

**Frontend:**
```
✅ src/vue/components/admin/
   - RepairManager.vue
   - RepairForm.vue
   - RepairStatusEditor.vue
   - RepairsList.vue

✅ src/vue/components/dashboard/
   - RepairCard.vue
   - RepairTimeline.vue
   - RepairsList.vue
   - StatusBadge.vue

✅ src/stores/repairs.js
   - CRUD en store

✅ src/composables/useRepairs.js
   - Wrapper del store
```

### ❌ Lo que FALTA:

```
- Numeración automática CDS-XXX
- Upload de fotos por etapa (modelo RepairEventPhoto)
- Notificaciones automáticas por cambio de estado
- Firma digital del cliente
- Timeline visual con fotos
```

---

## 3.4 Sistema de Pagos

### Lo que EXISTE (Sorpresa positiva):

```
✅ backend/app/models/payment.py
   - Modelo Payment completo
   - Enum PaymentStatus (PENDING, SUCCESS, etc.)

✅ backend/app/routers/payments.py
   - POST /payments - Crear con idempotencia
   - GET /payments - Lista con filtros
   - GET /payments/{id} - Detalle
   - ✅ Manejo de duplicados (transaction_id)
   - ✅ Auditoría integrada

✅ backend/app/schemas/__init__.py
   - PaymentCreate (con validación payment_method)
   - PaymentRead
```

### ❌ Lo que FALTA:

```
- Integración Flow.cl (API)
- Checkout frontend
- Webhooks de confirmación
- Comprobantes descargables
```

---

## 3.5 Sistema de Imágenes

### Lo que EXISTE (Mejor de lo esperado):

```
✅ backend/app/routers/uploads.py
   - POST /uploads/images
   - Rate limiting: 20/minute
   - Auditoría de uploads

✅ backend/app/utils/uploads.py
   - validate_image() - Validación completa
   - save_upload() - Guardar archivo

✅ backend/app/services/image_analysis.py
   - Análisis de imágenes

✅ backend/app/services/ai_detector.py
   - Detección de instrumentos

✅ src/vue/components/ai/ImageUploader.vue
   - Drag & drop funcional
   - Preview de imagen
   - Estados: uploading, analyzing, result
```

### ❌ Lo que FALTA:

```
- Integración Cloudinary (producción)
- Thumbnails automáticos
- Compresión de imágenes
```

---

## 3.6 Sistema de Inventario

### Lo que EXISTE:

```
✅ backend/app/models/inventory.py
✅ backend/app/models/stock_movement.py
✅ backend/app/routers/stock_movement.py
✅ backend/app/crud/inventory.py

✅ src/vue/components/admin/
   - InventoryTable.vue
   - InventoryForm.vue
   - InventoryAlerts.vue
   - StockMovements.vue
   - StockMovementsList.vue

✅ src/stores/inventory.js
✅ src/stores/stockMovements.js
✅ src/composables/useInventory.js
✅ src/composables/useStockMovements.js
```

### Estado: ✅ 80% Completo

---

# 4. ARCHIVOS EXISTENTES vs FALTANTES

## 4.1 Backend - Archivos que EXISTEN

```
backend/
├── app/
│   ├── api/v1/endpoints/
│   │   ├── auth.py          ✅ Completo
│   │   ├── brands.py        ✅ Completo
│   │   ├── instruments.py   ✅ Completo
│   │   ├── ai.py            ✅ Existe
│   │   ├── categories.py    ⚠️ Vacío
│   │   ├── diagnostics.py   ⚠️ Vacío
│   │   ├── inventory.py     ⚠️ Vacío
│   │   ├── repairs.py       ⚠️ Vacío
│   │   ├── stats.py         ⚠️ Vacío
│   │   └── users.py         ⚠️ Vacío
│   │
│   ├── routers/
│   │   ├── repair.py        ✅ CRUD + audit
│   │   ├── payments.py      ✅ CRUD + idempotencia
│   │   ├── uploads.py       ✅ Rate limit + audit
│   │   ├── user.py          ✅ CRUD
│   │   ├── category.py      ✅ CRUD
│   │   ├── instrument.py    ✅ CRUD
│   │   ├── stock_movement.py ✅ CRUD
│   │   ├── contact.py       ✅ Formulario
│   │   └── diagnostic.py    ⚠️ Parcial
│   │
│   ├── models/
│   │   ├── user.py          ✅
│   │   ├── repair.py        ✅
│   │   ├── payment.py       ✅
│   │   ├── instrument.py    ✅
│   │   ├── brand.py         ✅
│   │   ├── category.py      ✅
│   │   ├── diagnostic.py    ✅
│   │   ├── inventory.py     ✅
│   │   ├── stock_movement.py ✅
│   │   └── audit.py         ✅
│   │
│   ├── services/
│   │   ├── quote_calculator.py  ⚠️ Parcial
│   │   ├── email_service.py     ⚠️ Existe
│   │   ├── ai_detector.py       ✅
│   │   ├── image_analysis.py    ✅
│   │   ├── logging_service.py   ✅ create_audit()
│   │   └── pdf_generator.py     ✅
│   │
│   ├── core/
│   │   ├── security.py      ✅ JWT completo
│   │   ├── database.py      ✅ SQLAlchemy
│   │   ├── config.py        ⚠️ Secrets hardcoded
│   │   ├── ratelimit.py     ✅ slowapi
│   │   ├── dependencies.py  ✅
│   │   └── logging_config.py ✅
│   │
│   ├── schemas/
│   │   ├── __init__.py      ✅ DTOs completos
│   │   ├── auth.py          ✅
│   │   ├── user.py          ✅
│   │   └── otros...         ⚠️ Vacíos
│   │
│   ├── crud/
│   │   ├── base.py          ✅
│   │   ├── user.py          ✅
│   │   ├── repair.py        ✅
│   │   ├── category.py      ✅
│   │   └── inventory.py     ✅
│   │
│   └── utils/
│       └── uploads.py       ✅ validate_image
│
├── tests/
│   ├── conftest.py          ✅
│   ├── test_audit_hooks.py  ✅
│   ├── test_audit_logging.py ✅
│   ├── test_config.py       ✅
│   ├── test_payments_concurrency.py ✅
│   ├── test_payments_endpoints.py ✅
│   ├── test_ratelimit.py    ✅
│   └── test_uploads.py      ✅
│
└── cirujano.db              ✅ SQLite funcionando
```

## 4.2 Backend - Archivos FALTANTES (Críticos)

```
❌ backend/app/routers/quotation.py
   - POST /quotations/estimate
   - Cálculo de precio con reglas de negocio
   - Validación 50% máximo

❌ backend/app/services/rule_engine.py
   - Lógica downstream completa
   - Validación de combinaciones

❌ backend/app/services/calendar_service.py
   - Integración Google Calendar

❌ backend/app/services/flow_service.py
   - Integración Flow.cl

❌ backend/app/services/tracking_service.py
   - APIs de tracking (17track, etc.)

❌ .env.example
   - Template de variables de entorno

❌ passenger_wsgi.py
   - Deploy en cPanel
```

## 4.3 Frontend - Archivos que EXISTEN

```
src/
├── composables/           (15 archivos)
│   ├── useApi.js          ✅ Axios + interceptors
│   ├── useAuth.js         ✅ Completo
│   ├── useDiagnostic.js   ✅ Lógica downstream
│   ├── useDiagnostics.js  ✅ Store wrapper
│   ├── useInstruments.js  ✅
│   ├── useInstrumentsCatalog.js ✅
│   ├── useInventory.js    ✅
│   ├── useRepairs.js      ✅
│   ├── useUsers.js        ✅
│   ├── useCategories.js   ✅
│   ├── useStockMovements.js ✅
│   ├── emails.js          ✅
│   ├── layout.js          ✅
│   ├── scheduler.js       ✅
│   ├── settings.js        ✅
│   ├── strings.js         ✅
│   └── utils.js           ✅
│
├── stores/                (8 archivos)
│   ├── auth.js            ✅
│   ├── repairs.js         ✅
│   ├── instruments.js     ✅
│   ├── diagnostics.js     ✅
│   ├── inventory.js       ✅
│   ├── users.js           ✅
│   ├── categories.js      ✅
│   └── stockMovements.js  ✅
│
├── vue/components/
│   ├── ai/                (5 componentes)
│   │   ├── ImageUploader.vue    ✅ Drag & drop
│   │   ├── FaultDetector.vue    ✅
│   │   ├── FaultMarker.vue      ✅
│   │   ├── QuoteGenerator.vue   ✅
│   │   └── AIAnalysisResult.vue ✅
│   │
│   ├── admin/             (22 componentes)
│   │   ├── RepairManager.vue    ✅
│   │   ├── RepairForm.vue       ✅
│   │   ├── RepairsList.vue      ✅
│   │   ├── RepairStatusEditor.vue ✅
│   │   ├── InventoryTable.vue   ✅
│   │   ├── InventoryForm.vue    ✅
│   │   ├── InventoryAlerts.vue  ✅
│   │   ├── ClientList.vue       ✅
│   │   ├── ClientDetail.vue     ✅
│   │   ├── DiagnosticsList.vue  ✅
│   │   ├── UserList.vue         ✅
│   │   ├── UserForm.vue         ✅
│   │   ├── CategoryManager.vue  ✅
│   │   ├── CategoryList.vue     ✅
│   │   ├── CategoryForm.vue     ✅
│   │   ├── InstrumentList.vue   ✅
│   │   ├── InstrumentForm.vue   ✅
│   │   ├── StatsCards.vue       ✅
│   │   ├── StockMovements.vue   ✅
│   │   └── StockMovementsList.vue ✅
│   │
│   ├── dashboard/         (7 componentes)
│   │   ├── DashboardPanel.vue   ✅
│   │   ├── RepairCard.vue       ✅
│   │   ├── RepairTimeline.vue   ✅
│   │   ├── RepairsList.vue      ✅
│   │   ├── StatusBadge.vue      ✅
│   │   ├── QuickStats.vue       ✅
│   │   └── UserProfile.vue      ✅
│   │
│   ├── auth/              (4 componentes)
│   │   ├── LoginForm.vue        ✅
│   │   ├── RegisterForm.vue     ✅
│   │   ├── PasswordReset.vue    ✅
│   │   └── AccountDelete.vue    ✅
│   │
│   ├── articles/          (11 componentes)
│   │   ├── DiagnosticWizard.vue ✅
│   │   └── ... (10 más)
│   │
│   ├── widgets/           (12 componentes)
│   │   ├── FloatingQuoteButton.vue ✅
│   │   ├── ProgressBar.vue      ✅
│   │   ├── Alert.vue            ✅
│   │   └── ... (9 más)
│   │
│   └── ... (footer, nav, forms, etc.)
│
├── vue/content/pages/
│   ├── CotizadorIAPage.vue      ✅
│   ├── DashboardPage.vue        ✅
│   ├── HomePage.vue             ✅
│   ├── LoginPage.vue            ✅
│   ├── RegisterPage.vue         ✅
│   ├── ProfilePage.vue          ✅
│   ├── RepairsPage.vue          ✅
│   ├── PolicyPage.vue           ⚠️ Existe pero vacío
│   ├── LicensePage.vue          ✅
│   └── admin/
│       ├── AdminDashboard.vue   ✅
│       ├── RepairsAdminPage.vue ✅
│       ├── ClientsPage.vue      ✅
│       ├── InventoryPage.vue    ✅
│       ├── CategoriesPage.vue   ✅
│       └── StatsPage.vue        ✅
│
└── assets/data/
    ├── brands.json              ✅ Con tiers
    ├── instruments.json         ✅ Con componentes y valores
    └── faults.json              ✅ Con isPrecedence
```

## 4.4 Frontend - Archivos FALTANTES (Críticos)

```
❌ src/vue/components/quotation/
   ├── DisclaimerModal.vue       - Aceptación legal
   ├── QuotationResult.vue       - Mostrar resultado
   └── InstrumentSelector.vue    - Selector marca→modelo

❌ src/vue/components/payment/
   ├── PaymentCheckout.vue       - Checkout Flow.cl
   └── PaymentHistory.vue        - Historial pagos

❌ src/vue/components/calendar/
   └── AppointmentPicker.vue     - Selector de citas

❌ src/vue/content/pages/
   ├── TermsPage.vue             - Términos y condiciones
   └── PrivacyPage.vue           - Política privacidad
```

---

# 5. SEGURIDAD: ESTADO ACTUAL

## 5.1 Lo que YA está implementado ✅

| Control | Estado | Ubicación |
|---------|--------|-----------|
| JWT Authentication | ✅ | `security.py` |
| Password Hashing (bcrypt) | ✅ | `security.py` |
| Token Expiration | ✅ | Configurado |
| Refresh Tokens | ✅ | `auth.py` |
| Rate Limiting | ✅ | `ratelimit.py`, 20/min uploads |
| Image Validation | ✅ | `uploads.py` |
| SQL Injection Protection | ✅ | SQLAlchemy ORM |
| Audit Logging | ✅ | `logging_service.py` |

## 5.2 Lo que FALTA ❌

| Control | Estado | Prioridad |
|---------|--------|-----------|
| Secrets en .env | ❌ Hardcoded | 🔴 CRÍTICA |
| CORS producción | ❌ Solo localhost | 🔴 CRÍTICA |
| HTTPS forzado | ❌ No configurado | 🔴 CRÍTICA |
| CSRF Protection | ❌ No existe | 🟡 MEDIA |
| Security Headers | ❌ No configurado | 🟡 MEDIA |
| Input Sanitization | ⚠️ Parcial | 🟡 MEDIA |

## 5.3 Código Problemático Actual

```python
# ❌ backend/app/core/config.py - ACTUAL
secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
jwt_secret: str = os.getenv("JWT_SECRET", "your-jwt-secret-change-in-production")

# ❌ CORS - ACTUAL
allowed_origins: list = [
    "http://localhost:3000",
    "http://localhost:5173",
]
```

## 5.4 Código Requerido

```python
# ✅ backend/app/core/config.py - CORREGIDO
secret_key: str = os.getenv("SECRET_KEY")
jwt_secret: str = os.getenv("JWT_SECRET")

if not secret_key or not jwt_secret:
    raise ValueError("SECRET_KEY y JWT_SECRET son OBLIGATORIOS")

# ✅ CORS - CORREGIDO
allowed_origins: list = os.getenv("ALLOWED_ORIGINS", "").split(",")
# En .env: ALLOWED_ORIGINS=https://cirujanodesintetizadores.cl
```

---

# 6. PLAN DE ACCIÓN PRIORIZADO

## Fase 0: Seguridad (1-2 días) 🔴 URGENTE

```bash
# 1. Crear .env
cat > backend/.env << EOF
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)
DATABASE_URL=sqlite:///./cirujano.db
ALLOWED_ORIGINS=http://localhost:5173
EOF

# 2. Agregar a .gitignore
echo ".env" >> .gitignore

# 3. Modificar config.py para NO tener defaults peligrosos
```

**Archivos a modificar:**
- `backend/app/core/config.py`
- `backend/.gitignore`
- Crear `backend/.env`
- Crear `backend/.env.example`

---

## Fase 1: Endpoint de Cotización (3-5 días) 🔴 CRÍTICO

Este es EL endpoint que falta para conectar todo.

### 1.1 Crear `backend/app/routers/quotation.py`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
from pathlib import Path

router = APIRouter(prefix="/quotations", tags=["Cotizaciones"])

DATA_PATH = Path(__file__).resolve().parents[4] / "src" / "assets" / "data"

# Cargar datos
with open(DATA_PATH / "brands.json") as f:
    BRANDS = {b["id"]: b for b in json.load(f)["brands"]}
with open(DATA_PATH / "instruments.json") as f:
    INSTRUMENTS = {i["id"]: i for i in json.load(f)["instruments"]}
with open(DATA_PATH / "faults.json") as f:
    FAULTS = json.load(f)["faults"]

# Configuración de tiers
TIER_CONFIG = {
    'legendary': {'multiplier': 1.5, 'min_charge_percent': 10},
    'professional': {'multiplier': 1.3, 'min_charge_percent': 10},
    'historic': {'multiplier': 1.4, 'min_charge_percent': 10},
    'boutique': {'multiplier': 1.2, 'min_charge_percent': 10},
    'specialized': {'multiplier': 1.1, 'min_charge_percent': 10},
    'standard': {'multiplier': 1.0, 'min_charge_percent': 10},
}

class QuotationRequest(BaseModel):
    instrument_id: str
    faults: List[str]
    
class FaultBreakdown(BaseModel):
    fault_id: str
    name: str
    base_price: int
    
class QuotationResponse(BaseModel):
    instrument_id: str
    instrument_name: str
    brand_name: str
    tier: str
    
    # Precios
    base_total: int
    multiplier: float
    min_price: int
    max_price: int
    
    # Desglose
    breakdown: List[FaultBreakdown]
    
    # Validaciones
    instrument_value_avg: int
    max_recommended: int  # 50% del valor
    exceeds_recommendation: bool
    
    # Legal
    disclaimer: str
    budget_cost: int = 20000

@router.post("/estimate", response_model=QuotationResponse)
async def estimate_quotation(request: QuotationRequest):
    """
    Genera cotización estimada basada en instrumento y fallas.
    
    REGLAS DE NEGOCIO:
    1. Si "POWER" está en fallas, solo cuenta POWER (precedencia)
    2. Precio base × multiplicador de tier
    3. Rango: -20% a +30% del calculado
    4. Máximo recomendado: 50% del valor del instrumento
    """
    
    # Validar instrumento
    instrument = INSTRUMENTS.get(request.instrument_id)
    if not instrument:
        raise HTTPException(404, "Instrumento no encontrado")
    
    brand = BRANDS.get(instrument["brand"])
    if not brand:
        raise HTTPException(404, "Marca no encontrada")
    
    tier = brand.get("tier", "standard")
    tier_config = TIER_CONFIG.get(tier, TIER_CONFIG["standard"])
    
    # Aplicar lógica de precedencia
    effective_faults = request.faults
    has_power_fault = "POWER" in request.faults
    if has_power_fault:
        effective_faults = ["POWER"]  # Solo POWER si está presente
    
    # Calcular precio base
    breakdown = []
    base_total = 0
    
    for fault_id in effective_faults:
        fault = FAULTS.get(fault_id)
        if fault:
            base_total += fault.get("basePrice", 0)
            breakdown.append(FaultBreakdown(
                fault_id=fault_id,
                name=fault.get("name", fault_id),
                base_price=fault.get("basePrice", 0)
            ))
    
    # Aplicar multiplicador de tier
    multiplier = tier_config["multiplier"]
    adjusted_total = int(base_total * multiplier)
    
    # Calcular rango
    min_price = int(adjusted_total * 0.8)  # -20%
    max_price = int(adjusted_total * 1.3)  # +30%
    
    # Calcular valor del instrumento y máximo recomendado
    valor_min = instrument.get("valor_min", 0)
    valor_max = instrument.get("valor_max", 0)
    valor_avg = (valor_min + valor_max) // 2 if valor_min and valor_max else 0
    
    # Regla del 50%
    max_recommended = int(valor_avg * 0.5) if valor_avg else 999999999
    exceeds = max_price > max_recommended
    
    return QuotationResponse(
        instrument_id=request.instrument_id,
        instrument_name=f"{brand['name']} {instrument['model']}",
        brand_name=brand["name"],
        tier=tier,
        
        base_total=base_total,
        multiplier=multiplier,
        min_price=min_price,
        max_price=max_price,
        
        breakdown=breakdown,
        
        instrument_value_avg=valor_avg,
        max_recommended=max_recommended,
        exceeds_recommendation=exceeds,
        
        disclaimer="""⚠️ IMPORTANTE: Esta cotización es INDICATIVA y NO VINCULANTE.
        
• El precio final se confirma tras revisión presencial del equipo.
• El diagnóstico completo puede revelar fallas adicionales.
• Presupuesto formal: $20.000 CLP (abonable si procede con reparación).""",
        
        budget_cost=20000
    )
```

### 1.2 Registrar router en `router.py`

```python
# En backend/app/api/v1/router.py
from backend.app.routers import quotation as quotation_router

# Agregar:
api_router.include_router(quotation_router.router)
```

### 1.3 Crear componente `DisclaimerModal.vue`

```vue
<template>
  <div v-if="show" class="disclaimer-overlay">
    <div class="disclaimer-modal">
      <div class="disclaimer-header">
        <span class="warning-icon">⚠️</span>
        <h2>IMPORTANTE - LEA ANTES DE CONTINUAR</h2>
      </div>
      
      <div class="disclaimer-content">
        <p class="highlight">Esta cotización es <strong>INDICATIVA</strong> y <strong>NO VINCULANTE</strong>.</p>
        
        <ul>
          <li>El precio final se confirma tras revisión presencial del equipo en el taller.</li>
          <li>El diagnóstico completo requiere abrir el instrumento, lo que puede revelar fallas adicionales no detectables externamente.</li>
          <li>El presupuesto formal tiene un costo de <strong>$20.000 CLP</strong>, que es:
            <ul>
              <li><strong>ABONABLE:</strong> Se descuenta del total si decide reparar</li>
              <li><strong>NO REEMBOLSABLE:</strong> Queda como pago por diagnóstico si no repara</li>
            </ul>
          </li>
        </ul>
        
        <div class="acceptance">
          <label>
            <input type="checkbox" v-model="accepted" />
            <span>He leído y acepto las condiciones</span>
          </label>
        </div>
      </div>
      
      <div class="disclaimer-actions">
        <button @click="$emit('cancel')" class="btn-cancel">Cancelar</button>
        <button 
          @click="$emit('accept')" 
          :disabled="!accepted"
          class="btn-accept"
        >
          Continuar y Ver Cotización
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  show: Boolean
})

defineEmits(['accept', 'cancel'])

const accepted = ref(false)
</script>

<style scoped>
.disclaimer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.disclaimer-modal {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  padding: 2rem;
}

.disclaimer-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.warning-icon {
  font-size: 2rem;
}

.disclaimer-header h2 {
  margin: 0;
  color: #c53030;
}

.highlight {
  background: #fff5f5;
  border-left: 4px solid #c53030;
  padding: 1rem;
  margin-bottom: 1rem;
}

.acceptance {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f7fafc;
  border-radius: 8px;
}

.acceptance label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.disclaimer-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
}

.btn-accept {
  padding: 0.75rem 1.5rem;
  background: #2f855a;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-accept:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}
</style>
```

---

## Fase 2: Conectar Frontend con Endpoint (2-3 días)

### 2.1 Crear `src/composables/useQuotation.js`

```javascript
import { ref, computed } from 'vue'
import { useApi } from './useApi'

export function useQuotation() {
  const { api } = useApi()
  
  const loading = ref(false)
  const error = ref(null)
  const quotation = ref(null)
  
  const estimate = async (instrumentId, faults) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/quotations/estimate', {
        instrument_id: instrumentId,
        faults: faults
      })
      quotation.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Error al generar cotización'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const reset = () => {
    quotation.value = null
    error.value = null
  }
  
  const exceedsRecommendation = computed(() => 
    quotation.value?.exceeds_recommendation ?? false
  )
  
  return {
    loading,
    error,
    quotation,
    estimate,
    reset,
    exceedsRecommendation
  }
}
```

### 2.2 Actualizar `CotizadorIAPage.vue`

```vue
<template>
  <div class="cotizador-page">
    <!-- Paso 1: Selección de instrumento -->
    <InstrumentSelector 
      v-if="step === 1"
      @selected="onInstrumentSelected"
    />
    
    <!-- Paso 2: Diagnóstico de fallas -->
    <DiagnosticWizard
      v-if="step === 2"
      :instrument="selectedInstrument"
      @complete="onDiagnosticComplete"
      @back="step = 1"
    />
    
    <!-- Paso 3: Disclaimer -->
    <DisclaimerModal
      :show="step === 3"
      @accept="onDisclaimerAccepted"
      @cancel="step = 2"
    />
    
    <!-- Paso 4: Resultado -->
    <QuotationResult
      v-if="step === 4"
      :quotation="quotation"
      :loading="loading"
      @new-quote="resetAll"
      @schedule="goToSchedule"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useQuotation } from '@/composables/useQuotation'
import { useDiagnostic } from '@/composables/useDiagnostic'

import InstrumentSelector from '@/vue/components/quotation/InstrumentSelector.vue'
import DiagnosticWizard from '@/vue/components/articles/DiagnosticWizard.vue'
import DisclaimerModal from '@/vue/components/quotation/DisclaimerModal.vue'
import QuotationResult from '@/vue/components/quotation/QuotationResult.vue'

const step = ref(1)
const selectedInstrument = ref(null)
const selectedFaults = ref([])

const { quotation, loading, estimate, reset } = useQuotation()

const onInstrumentSelected = (instrument) => {
  selectedInstrument.value = instrument
  step.value = 2
}

const onDiagnosticComplete = (faults) => {
  selectedFaults.value = faults
  step.value = 3
}

const onDisclaimerAccepted = async () => {
  step.value = 4
  await estimate(selectedInstrument.value.id, selectedFaults.value)
}

const resetAll = () => {
  selectedInstrument.value = null
  selectedFaults.value = []
  reset()
  step.value = 1
}

const goToSchedule = () => {
  // Navegar a agendamiento
}
</script>
```

---

## Fase 3: Deploy Básico (1-2 días)

### 3.1 Crear `passenger_wsgi.py`

```python
import sys
import os

# Agregar path de la aplicación
sys.path.insert(0, os.path.dirname(__file__))

# Importar app FastAPI
from app.main import app as application
```

### 3.2 Crear `.htaccess` para backend

```apache
PassengerEnabled On
PassengerAppRoot /home/usuario/backend
PassengerBaseURI /api
PassengerPython /home/usuario/backend/.venv/bin/python

RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

### 3.3 Build Frontend

```bash
cd frontend
npm run build
# Copiar dist/ a public_html/
```

---

# 7. ESTIMACIONES DE TIEMPO

## Resumen por Fase

| Fase | Descripción | Tiempo | Prioridad |
|------|-------------|--------|-----------|
| 0 | Seguridad (.env, CORS) | 1-2 días | 🔴 CRÍTICA |
| 1 | Endpoint cotización | 3-5 días | 🔴 CRÍTICA |
| 2 | Conectar frontend | 2-3 días | 🔴 CRÍTICA |
| 3 | Deploy básico | 1-2 días | 🟠 ALTA |
| 4 | Políticas legales | 1-2 días | 🟠 ALTA |
| 5 | Email notifications | 2-3 días | 🟡 MEDIA |
| 6 | Pagos Flow.cl | 3-5 días | 🟡 MEDIA |
| 7 | Google Calendar | 2-3 días | 🟢 BAJA |

## Timeline MVP

```
Semana 1:
├── Día 1-2: Fase 0 (Seguridad)
├── Día 3-5: Fase 1 (Endpoint cotización)
└── Día 6-7: Fase 2 inicio (Frontend)

Semana 2:
├── Día 1-2: Fase 2 completar
├── Día 3-4: Fase 3 (Deploy)
├── Día 5: Testing y ajustes
└── Día 6-7: Buffer / Políticas legales

🎯 MVP ONLINE: Fin de semana 2
```

---

# CONCLUSIÓN FINAL

## Lo que tienes es BUENO

```
✅ Arquitectura sólida (FastAPI + Vue 3 + SQLAlchemy)
✅ Autenticación completa con JWT
✅ Sistema de auditoría funcionando
✅ Rate limiting implementado
✅ Validación de imágenes
✅ Tests unitarios
✅ Lógica de fallas con precedencia
✅ Datos de instrumentos con tiers y valores
✅ Componentes de UI listos
✅ Stores y composables configurados
```

## Lo que falta es CONECTAR

```
❌ Endpoint /quotations/estimate (LA PIEZA CLAVE)
❌ Disclaimer legal antes de mostrar precio
❌ Hardening de seguridad para producción
❌ Conectar DiagnosticWizard → API → QuotationResult
```

## Recomendación

**NO necesitas reescribir nada.** Solo necesitas:

1. Crear 1 endpoint nuevo (`quotation.py`)
2. Crear 2-3 componentes Vue (`DisclaimerModal`, `QuotationResult`)
3. Conectar las piezas existentes
4. Configurar `.env` y CORS
5. Deploy

**El proyecto está a 1-2 semanas de ser un MVP funcional.**

---

*Auditoría actualizada - 6 Enero 2026*
*Cruce: AUDITORIA_CDS.md (2837 líneas) + VOLCADO_UNIFICADO_01.txt (4868 líneas)*
