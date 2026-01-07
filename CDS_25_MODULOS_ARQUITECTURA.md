# 🔧 ARQUITECTURA TÉCNICA - 25 MÓDULOS
## Cirujano de Sintetizadores

**Fecha:** 6 Enero 2026  
**Stack:** FastAPI + Vue 3 + MySQL + Redis + Celery

---

# VISIÓN GENERAL

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLOUDFLARE (CDN + SSL)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
        ┌────────────────────────────┴────────────────────────────┐
        ▼                                                         ▼
┌──────────────────────┐                              ┌──────────────────────┐
│   FRONTEND (Vue 3)   │                              │  BACKEND (FastAPI)   │
│   ────────────────   │                              │  ─────────────────   │
│   • SPA Vite         │◀────── REST API ────────────▶│  • JWT Auth          │
│   • Pinia stores     │                              │  • Rate Limiting     │
│   • TailwindCSS      │◀────── WebSocket ───────────▶│  • Async Workers     │
└──────────────────────┘                              └──────────────────────┘
                                                                │
                    ┌───────────────────────────────────────────┼───────────────┐
                    ▼                       ▼                   ▼               ▼
            ┌─────────────┐         ┌─────────────┐     ┌─────────────┐  ┌─────────────┐
            │    MySQL    │         │    Redis    │     │   Celery    │  │ Cloudinary  │
            │   (datos)   │         │   (cache)   │     │   (jobs)    │  │  (imágenes) │
            └─────────────┘         └─────────────┘     └─────────────┘  └─────────────┘
```

---

# LOS 25 MÓDULOS

## 1. AUTH (Autenticación)
```
Qué hace: Login, registro, JWT, roles, refresh tokens
Endpoints: POST /auth/login, /register, /refresh, /logout, GET /me
Modelos: User, RefreshToken
Estado: ✅ 90% implementado
```

## 2. CATÁLOGO (Instrumentos + Marcas)
```
Qué hace: BD de marcas, modelos, tiers, componentes, valores
Endpoints: GET /catalog/brands, /instruments, /faults
Modelos: Brand, Instrument, Fault, InstrumentComponent
Datos: brands.json, instruments.json, faults.json
Estado: ✅ 85% implementado

IMPORTANTE - Separación Cliente/Técnico:
├── Cliente ve: nombre, marca, foto, componentes
└── Técnico ve: + valor mercado, tier, cobro mínimo, precios fuentes
```

## 3. COTIZADOR INTELIGENTE
```
Qué hace: Marca → Modelo → Fallas → Precio aproximado con reglas
Endpoints: POST /quotations/estimate, GET /quotations/{id}
Modelos: Quotation, QuotationFault

Reglas de negocio:
├── Lógica downstream: POWER bloquea resto de fallas
├── Multiplicador por tier: legendary ×1.5, standard ×1.0
├── Rango de precio: -20% a +30%
├── Regla del 50%: NUNCA cobrar más del 50% del valor
└── Disclaimer obligatorio antes de mostrar precio

Estado: ⚠️ 50% - FALTA ENDPOINT /estimate
```

## 4. DIAGNÓSTICO VISUAL
```
Qué hace: UI interactiva donde cliente marca componentes malos en imagen
Endpoints: GET /diagnostics/instrument/{id}/diagram, POST /analyze
Componentes Vue: VisualDiagnostic.vue, ClickableArea.vue
Estado: ⚠️ 40% - Lógica existe, falta UI interactiva
```

## 5. DETECCIÓN IA
```
Qué hace: Sube foto → detecta marca/modelo automático
Endpoints: POST /ai/detect, POST /ai/confirm
Servicios: AIDetectionService (CLIP local + OpenAI Vision fallback)

Estrategia:
├── 1. Modelo local (CLIP) - gratis, rápido
├── 2. Si confianza < 85% → OpenAI Vision API
└── 3. Match contra BD local

Estado: ⚠️ 60% - Servicio existe, falta fine-tuning
```

## 6. REPARACIONES
```
Qué hace: Gestión completa del ciclo de reparación
Endpoints: POST/GET/PUT /repairs, POST /repairs/{id}/status, /photos, /notes
Modelos: Repair, RepairEvent, RepairPhoto

Estados:
RECEIVED → DIAGNOSING → QUOTED → APPROVED → REPAIRING → 
WAITING_PARTS → COMPLETED → READY_PICKUP → DELIVERED

Numeración: CDS-2026-0001, CDS-2026-0002...

Estado: ✅ 75% implementado
```

## 7. TRACKING (tipo DHL)
```
Qué hace: Timeline visual con fechas, estados y fotos
Endpoints: GET /tracking/{repair_number}, /events, /photos
Componentes Vue: RepairTimeline.vue, TimelineEvent.vue

Vista:
✅ 05/01 - Equipo recibido [📷 fotos]
✅ 06/01 - Diagnóstico completado [💰 cotización]
🔄 06/01 - En reparación (45%) [📷 avance]
○  --/-- - Listo para retiro

Estado: ⚠️ 60% - Componentes existen, falta conectar
```

## 8. CARRITO DE REPUESTOS
```
Qué hace: Gestionar compra de repuestos por reparación
Endpoints: GET/POST /cart/{repair_id}, PUT/DELETE /cart/items/{id}
Modelos: RepairPart

Flujo:
├── Técnico o cliente agrega repuesto
├── Cliente aprueba y paga (Flow.cl)
├── Técnico compra + ingresa tracking
└── Sistema rastrea envío

Estado: ❌ 0% - No implementado
```

## 9. TRACKING DE ENVÍOS
```
Qué hace: Seguimiento de repuestos con APIs externas
Endpoints: GET /shipments/{part_id}, /events

APIs integradas:
├── 17track.net (universal, 900+ carriers)
├── AliExpress
├── DHL, FedEx
├── Correos Chile, Chilexpress

Cron: Sync cada 4 horas

Estado: ❌ 0% - No implementado
```

## 10. PAGOS (Flow.cl)
```
Qué hace: Procesar pagos online
Endpoints: POST /payments/create, GET /status, POST /webhook

Tipos de pago:
├── BUDGET - Presupuesto $20.000
├── REPAIR - Costo reparación
├── PARTS - Repuestos
└── STORAGE - Bodegaje

Flujo:
1. Cliente click Pagar → 2. Backend crea orden Flow →
3. Redirect a Flow → 4. Cliente paga →
5. Webhook confirma → 6. Actualiza estado

Estado: ⚠️ 40% - Modelo existe, falta integración Flow
```

## 11. CALENDARIO (Google Calendar)
```
Qué hace: Agendar citas sincronizado con Google Calendar
Endpoints: GET /appointments/slots, POST/PUT/DELETE /appointments
Modelos: Appointment, BlockedSlot, Holiday

Tipos de cita:
├── RECEPTION - Entrega equipo (30 min)
├── PICKUP - Retiro equipo (15 min)
└── STREAMING - Reparación en vivo

Horarios: Lun-Vie 10-18, Sáb 10-14

Estado: ❌ 0% - No implementado
```

## 12. TICKETS + SLA
```
Qué hace: Sistema de soporte con tiempos de respuesta
Endpoints: POST/GET /tickets, POST /reply, PUT /status
Modelos: Ticket, TicketReply

Categorías y SLA:
├── quote_question - 4 hrs
├── repair_status - 2 hrs
├── payment_issue - 2 hrs (alta)
├── complaint - 2 hrs (alta)
├── warranty - 4 hrs
└── general_inquiry - 24 hrs

Escalado:
├── 50% SLA → Recordatorio técnico
├── 80% SLA → SMS urgente
├── 100% SLA → Marca INCUMPLIDO
└── 150% SLA → Compensación

Estado: ❌ 0% - No implementado
```

## 13. RESPUESTAS AUTOMÁTICAS
```
Qué hace: Clasifica mensajes y responde automáticamente
Servicios: AutoResponseEngine

Flujo:
1. Ticket nuevo → 2. Clasificar por keywords →
3. Asignar SLA → 4. Generar respuesta auto →
5. Notificar si urgente

Clasificación:
├── "cotiz", "precio" → quote_question
├── "estado", "avance" → repair_status
├── "pago" → payment_issue
├── "reclamo", "queja" → complaint
└── default → general_inquiry

Estado: ❌ 0% - No implementado
```

## 14. NOTIFICACIONES
```
Qué hace: Enviar emails y SMS automáticos
Servicios: NotificationService
Integraciones: SendGrid (email), Twilio (SMS)

Eventos:
├── Cotización guardada → Email
├── Reparación creada → Email + SMS
├── Estado cambiado → Email
├── Repuesto llegó → Email + SMS
├── Listo para retiro → Email + SMS
├── Recordatorio cita → Email + SMS
├── SLA por vencer → SMS (técnico)
└── Pago confirmado → Email

Estado: ⚠️ 40% - email_service.py existe, falta completar
```

## 15. 🎬 STREAMING EN VIVO
```
Qué hace: Cliente paga y ve su equipo siendo reparado
Endpoints: POST /streaming/start, /marker, /end
Integraciones: OBS WebSocket, YouTube Live API

Modelo de negocio:
├── Estándar: Precio base
├── Premium VIVO: +$30.000-50.000
└── Público: -$15.000-25.000 (descuento)

Hardware: 6-9 cámaras + OBS configurado

Estado: ❌ 0% - Hardware listo, software no
```

## 16. YOUTUBE AUTO-PUBLISH
```
Qué hace: Publica video automático al terminar stream
Servicios: YouTubeService
Integraciones: YouTube Data API v3

Flujo:
Stream termina → Procesa video → Genera capítulos → Publica

Metadata auto:
├── Título: "Reparación {Instrumento} - {Fallas}"
├── Descripción: De la ficha
├── Tags: marca, modelo, fallas
└── Capítulos: De los markers

Estado: ❌ 0% - No implementado
```

## 17. PORTFOLIO AUTOMÁTICO
```
Qué hace: "Últimos Trabajos" se actualiza solo al entregar
Endpoints: GET /portfolio, GET /portfolio/latest
Modelos: PortfolioItem, PortfolioPhoto

Trigger: Repair.status = "delivered"

Auto-genera:
├── Selecciona mejores fotos
├── Crea entrada portfolio
├── Publica en web
└── (Opcional) Comparte en redes

Estado: ❌ 0% - No implementado
```

## 18. SCRAPER PRECIOS
```
Qué hace: Consulta precios de mercado (SOLO TÉCNICO)
Servicios: ScraperService
Modelos: PriceHistory, InstrumentValuation

Fuentes:
├── Reverb.com (prioritario)
├── eBay
├── Thomann
├── MercadoLibre CL
└── Yapo.cl

Output por instrumento:
├── valor_min, valor_max, valor_avg
├── disponibilidad Chile
├── costo importación estimado
└── cobro_minimo (10% del avg)

Cron: Semanal (domingo 03:00)

Estado: ❌ 0% - No implementado
```

## 19. COTIZACIÓN JUSTA
```
Qué hace: Valida regla del 50% automáticamente
Ubicación: Integrado en QuotationService

Regla:
├── Si cotización > 50% valor instrumento → WARNING
├── Cliente debe aceptar explícitamente
├── Se registra en auditoría
└── Sugiere "considerar otras opciones"

Estado: ⚠️ 30% - Lógica parcial en quote_calculator.py
```

## 20. POLÍTICAS/LEGAL
```
Qué hace: Gestión de documentos legales versionados
Endpoints: GET /policies, GET /policies/{type}
Modelos: Policy

Documentos:
├── Términos y Condiciones
├── Política de Presupuesto ($20.000 abonable)
├── Política de Bodega (30 días, luego $5.000/mes, 90 días = abandonado)
├── Política de Garantía
├── Política de Privacidad
└── Exención de Responsabilidad

Estado: ❌ 10% - PolicyPage.vue vacía
```

## 21. PANEL TÉCNICO
```
Qué hace: Dashboard admin completo
Componentes: AdminDashboard.vue, RepairManager.vue, etc.

Secciones:
├── Reparaciones activas
├── Cotizaciones pendientes
├── Tickets sin responder
├── Calendario del día
├── Métricas y KPIs
├── Inventario bajo stock
├── Pagos pendientes
├── Control streaming
└── Scraper precios (solo tú)

Estado: ✅ 70% - Estructura existe
```

## 22. PANEL CLIENTE
```
Qué hace: Dashboard para clientes
Componentes: DashboardPage.vue, RepairCard.vue, etc.

Secciones:
├── Mis reparaciones (con tracking)
├── Mis cotizaciones
├── Mis pagos / Historial
├── Mis citas
├── Mis tickets
└── Mi perfil

Estado: ⚠️ 60% - Componentes existen
```

## 23. INVENTARIO
```
Qué hace: Control de stock de repuestos
Endpoints: CRUD /inventory, /stock-movements
Modelos: InventoryItem, StockMovement

Funcionalidades:
├── CRUD items
├── Movimientos de stock
├── Alertas stock bajo
├── Asociar a reparaciones
├── Costos y valorización
└── Proveedores

Estado: ✅ 80% implementado
```

## 24. AUDITORÍA
```
Qué hace: Registro de todas las acciones
Servicios: logging_service.py → create_audit()
Modelos: AuditLog

Registra:
├── Quién (user_id)
├── Qué (action)
├── Cuándo (timestamp)
├── Desde dónde (IP)
├── Valores antes/después
└── Exportable

Estado: ✅ 90% implementado
```

## 25. ANALYTICS/SEO
```
Qué hace: Medición y posicionamiento
Integraciones: GA4, Search Console

Implementar:
├── Google Analytics 4
├── Google Search Console
├── Schema.org LocalBusiness
├── Open Graph (redes)
└── Sitemap automático

Estado: ❌ 0% - No implementado
```

---

# RESUMEN DE ESTADOS

| # | Módulo | Estado | % |
|---|--------|--------|---|
| 1 | Auth | ✅ Implementado | 90% |
| 2 | Catálogo | ✅ Implementado | 85% |
| 3 | Cotizador | ⚠️ Falta endpoint | 50% |
| 4 | Diagnóstico Visual | ⚠️ Parcial | 40% |
| 5 | Detección IA | ⚠️ Parcial | 60% |
| 6 | Reparaciones | ✅ Implementado | 75% |
| 7 | Tracking | ⚠️ Parcial | 60% |
| 8 | Carrito Repuestos | ❌ No existe | 0% |
| 9 | Tracking Envíos | ❌ No existe | 0% |
| 10 | Pagos Flow.cl | ⚠️ Parcial | 40% |
| 11 | Calendario | ❌ No existe | 0% |
| 12 | Tickets + SLA | ❌ No existe | 0% |
| 13 | Auto-responder | ❌ No existe | 0% |
| 14 | Notificaciones | ⚠️ Parcial | 40% |
| 15 | 🎬 Streaming | ❌ No existe | 0% |
| 16 | YouTube Auto | ❌ No existe | 0% |
| 17 | Portfolio Auto | ❌ No existe | 0% |
| 18 | Scraper Precios | ❌ No existe | 0% |
| 19 | Cotización Justa | ⚠️ Parcial | 30% |
| 20 | Políticas | ❌ Solo placeholder | 10% |
| 21 | Panel Técnico | ✅ Implementado | 70% |
| 22 | Panel Cliente | ⚠️ Parcial | 60% |
| 23 | Inventario | ✅ Implementado | 80% |
| 24 | Auditoría | ✅ Implementado | 90% |
| 25 | Analytics | ❌ No existe | 0% |

**Promedio general: ~38%**

---

# PRIORIDAD DE IMPLEMENTACIÓN

## FASE 1: MVP (Semanas 1-2) 🔴 CRÍTICO
```
├── [3] Cotizador - Crear endpoint /estimate
├── [4] Diagnóstico - Conectar UI
├── [19] Cotización Justa - Completar validación
├── [20] Políticas - Crear contenido legal
└── [Seguridad] - .env, CORS, HTTPS
```

## FASE 2: Core Business (Semanas 3-4)
```
├── [6] Reparaciones - Completar flujo
├── [7] Tracking - Timeline visual
├── [14] Notificaciones - Email básico
├── [21] Panel Técnico - Dashboard
└── [22] Panel Cliente - Dashboard
```

## FASE 3: Pagos (Semanas 5-6)
```
├── [10] Pagos - Integrar Flow.cl
├── [8] Carrito - Sistema de repuestos
└── [11] Calendario - Google Calendar
```

## FASE 4: Automatización (Semanas 7-8)
```
├── [12] Tickets - Sistema + SLA
├── [13] Auto-responder - IA
├── [9] Tracking Envíos - APIs
└── [14] Notificaciones - SMS
```

## FASE 5: Premium (Semanas 9-10)
```
├── [15] 🎬 Streaming
├── [16] YouTube Auto
├── [17] Portfolio Auto
└── [18] Scraper Precios
```

## FASE 6: Optimización (Continuo)
```
├── [5] Detección IA - Fine-tuning
├── [25] Analytics - GA4, SEO
└── Mejoras continuas
```

---

# JOBS ASÍNCRONOS (Celery)

```python
SCHEDULED_JOBS = {
    # Cada 15 minutos
    "check_sla_breaches": "*/15 * * * *",
    
    # Cada 4 horas
    "sync_shipment_tracking": "0 */4 * * *",
    
    # Diario 08:00
    "send_daily_summary": "0 8 * * *",
    
    # Diario 10:00  
    "send_pickup_reminders": "0 10 * * *",
    
    # Diario 18:00
    "send_appointment_reminders": "0 18 * * *",
    
    # Diario 03:00
    "database_backup": "0 3 * * *",
    
    # Semanal domingo 03:00
    "scrape_market_prices": "0 3 * * 0",
    
    # Mensual día 1
    "generate_storage_fees": "0 0 1 * *",
}
```

---

# INTEGRACIONES EXTERNAS

| Servicio | Uso | Costo |
|----------|-----|-------|
| **Flow.cl** | Pagos | 2.9% por transacción |
| **SendGrid** | Email | Free tier 100/día |
| **Twilio** | SMS | ~$0.05/SMS |
| **Google Calendar** | Citas | Gratis |
| **YouTube API** | Streaming | Gratis |
| **17track** | Tracking | Free tier + paid |
| **OpenAI Vision** | IA detección | $0.01/imagen |
| **Cloudinary** | Imágenes | Free tier 25GB |
| **Cloudflare** | CDN/SSL | Gratis |

---

# MODELO DE DATOS RESUMIDO

```sql
-- Core
users, roles, refresh_tokens, audit_logs

-- Catálogo  
brands, instruments, instrument_components, faults, 
instrument_valuations, price_history

-- Cotización
quotations, quotation_faults, diagnostics

-- Reparaciones
repairs, repair_events, repair_photos

-- Comercio
repair_parts, shipments, shipment_events,
payments, carts, cart_items

-- Soporte
tickets, ticket_replies

-- Scheduling
appointments, blocked_slots, holidays

-- Streaming
streams, stream_markers, youtube_videos

-- Portfolio
portfolio_items, portfolio_photos

-- Inventario
inventory_items, stock_movements, suppliers

-- Legal
policies
```

---

# ENDPOINTS TOTALES

| Categoría | Cantidad |
|-----------|----------|
| Auth | 8 |
| Catálogo | 10 |
| Cotizaciones | 5 |
| Diagnósticos | 4 |
| IA | 3 |
| Reparaciones | 8 |
| Tracking | 6 |
| Carrito | 6 |
| Pagos | 5 |
| Calendario | 5 |
| Tickets | 6 |
| Streaming | 4 |
| Portfolio | 3 |
| Inventario | 8 |
| Usuarios | 5 |
| Admin | 10 |
| Webhooks | 3 |
| **TOTAL** | **~100** |

---

*Arquitectura CDS v1.0 - Enero 2026*
