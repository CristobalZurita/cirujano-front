# IMPLEMENTACION_CDS_MASTER.md
## Documento Técnico Maestro de Implementación
### Proyecto: CIRUJANO DE SINTETIZADORES (CDS)

---

## Payments (Operational notes)

- Payments are created via POST `/api/v1/payments/` and are idempotent when a `transaction_id` is provided: subsequent requests with the same `transaction_id` will return the existing payment instead of creating a duplicate.

### Production migration / dedupe process

1. Use the provided script `scripts/dedupe_payments_transaction_ids.py` to detect duplicates:

	- Dry run: `python scripts/dedupe_payments_transaction_ids.py --dry-run`
	- Apply: `python scripts/dedupe_payments_transaction_ids.py --apply`

For a detailed step-by-step runbook and verification steps, see `docs/PRODUCTION_MIGRATIONS.md`.

2. After deduplication, run `alembic upgrade head` in production to allow the Alembic migration to add the UNIQUE constraint.

Notes:
- The test environment uses SQLite and the migration is tolerant for SQLite; in production (Postgres) run the dedupe script first to avoid failure when adding uniqueness constraints.
- The system enforces idempotency both at application level (check by transaction_id on create) and via the DB constraint when applied.


## 0. OBJETIVO DEL DOCUMENTO

Este documento constituye la **guía técnica definitiva de implementación** del sistema
**Cirujano de Sintetizadores**, derivada **exclusivamente** de:

- El documento AUDITORIA_CDS.md (visión, reglas, restricciones)
- El TREE real del proyecto (`src/`, `backend/`, `public/`)
- El estado actual del repositorio GitHub
- El flujo de negocio descrito por el dueño del taller

Este documento **NO**:
- Resume la visión
- Propone ideas nuevas
- Agrega features no solicitadas

Este documento **SÍ**:
- Cruza visión vs código existente
- Identifica faltantes reales
- Enumera archivos concretos
- Define responsabilidades técnicas
- Establece el alcance legal y técnico del sistema

---

## 1. ESTADO ACTUAL DEL PROYECTO (BASE OBJETIVA)

### 1.1 Stack detectado

- Frontend: Vue 3 + Vite
- Backend: FastAPI (Python)
- Persistencia actual: JSON plano
- Media: carpeta `public/`
- Autenticación: inexistente
- Motor de reglas: inexistente
- Capa legal: inexistente
- Capa media validada: inexistente

---

## 2. CHECKLIST COMPARATIVO GLOBAL
### (AUDITORIA_CDS.md vs CÓDIGO REAL)

---

## 2.1 Capa Frontend

### 2.1.1 EXISTE

| Requisito AUDITORIA | Archivo | Estado |
|---|---|---|
| Wizard de diagnóstico | DiagnosticWizard.vue | UI-only |
| Sección diagnóstico | DiagnosticSection.vue | Render |
| Estado diagnóstico | useDiagnostic.js | Plano |
| Selección marca | brands.json | Estático |
| Selección modelo | instruments.json | Estático |
| Selección fallas | faults.json | Sin pesos |
| Imagen instrumento | ImageView.vue | Visual |

### 2.1.2 NO EXISTE

| Requisito AUDITORIA | Falta | Archivo requerido |
|---|---|---|
| Flujo aguas abajo | Motor de reglas | src/constants/diagnosticFlow.js |
| Estados formales | Enum | src/constants/diagnosticStates.js |
| Resultado tipado | Modelo | src/models/DiagnosticResult.js |
| Sesión diagnóstica | Modelo | src/models/DiagnosticSession.js |
| Disclaimer obligatorio | UI | DiagnosticDisclaimer.vue |
| Bloqueo sin aceptación | Guard | Router / Wizard |
| Gestión errores | UI | DiagnosticError.vue |
| Tipografía responsiva | Sistema | SCSS / tokens |

---

## 2.2 Capa Backend

### 2.2.1 EXISTE

| Requisito | Archivo | Nivel |
|---|---|---|
| API base | main.py | Infra |
| Catálogo marcas | brands.py | Read |
| Catálogo instrumentos | instruments.py | Read |
| Router diagnóstico | diagnostic.py | Vacío |
| Config DB | database.py | Infra |

### 2.2.2 NO EXISTE

| Requisito AUDITORIA | Falta | Archivo requerido |
|---|---|---|
| Motor reglas diagnóstico | Lógica | services/rule_engine.py |
| Evaluador síntomas | Lógica | services/symptom_evaluator.py |
| Motor estimativo | Precios | services/estimator.py |
| Sesión persistente | Modelo | models/diagnosis_session.py |
| Estados del caso | Enum | models/diagnosis_state.py |
| Aceptación legal | Modelo | models/legal_acceptance.py |
| Auditoría | Logger | services/audit_logger.py |
| Workflow estados | Servicio | services/workflow.py |

---

## 2.3 Capa Media (CRÍTICA)

### 2.3.1 EXISTE

| Elemento | Estado |
|---|---|
| Imágenes públicas | Parcial |
| Logos marcas | OK |

### 2.3.2 NO EXISTE

| Requisito AUDITORIA | Falta | Consecuencia |
|---|---|---|
| Subida controlada | Pipeline | No validación |
| Validación formato | Seguridad | Malware |
| Rechazo watermark | Legal | Uso indebido |
| Cuarentena | Control | Riesgo |
| Revisión manual | Autoridad | Caos |
| Asociación modelo | Mapping | No indexable |
| Versionado | Histórico | Sin trazabilidad |

---

## 3. LISTA EXHAUSTIVA DE ARCHIVOS FALTANTES

### 3.1 Frontend

```

src/constants/diagnosticStates.js
src/constants/diagnosticFlow.js
src/models/DiagnosticSession.js
src/models/DiagnosticResult.js
src/vue/components/diagnostic/DiagnosticDisclaimer.vue
src/vue/components/diagnostic/DiagnosticResult.vue
src/vue/components/diagnostic/DiagnosticError.vue

```

### 3.2 Backend

```

backend/app/services/rule_engine.py
backend/app/services/symptom_evaluator.py
backend/app/services/estimator.py
backend/app/services/workflow.py
backend/app/services/image_pipeline.py
backend/app/services/image_validator.py
backend/app/services/audit_logger.py
backend/app/models/diagnosis_session.py
backend/app/models/diagnosis_state.py
backend/app/models/legal_acceptance.py
backend/app/routers/media.py
backend/app/routers/legal.py
backend/app/routers/session.py

```

### 3.3 Filesystem Media

```

backend/media/official/
backend/media/user_pending/
backend/media/quarantine/
backend/media/rejected/
backend/media/approved/

```

---

## 4. MATRIZ DE RESPONSABILIDAD (NO NEGOCIABLE)

| Capa | Informa | Estima | Decide | Diagnostica |
|---|---|---|---|---|
| Web | ✔ | ✔ | ✖ | ✖ |
| Backend | ✔ | ✔ | ✖ | ✖ |
| Usuario | ✖ | ✖ | ✖ | ✖ |
| Taller físico | ✔ | ✔ | ✔ | ✔ |

---

## 5. ALCANCE LEGAL DEL SISTEMA

- La web **NO diagnostica**
- La web **NO compromete precio**
- El diagnóstico real ocurre **solo en taller**
- El presupuesto online es **orientativo**
- El presupuesto pagado en taller **manda siempre**
- Todo flujo requiere **aceptación explícita**

---

## 6. CONCLUSIÓN TÉCNICA FINAL

El proyecto actual:
- NO está mal diseñado
- NO está conceptualmente errado
- Está **estructuralmente incompleto**

La ausencia es:
- Capa de dominio
- Capa legal
- Capa media
- Motor de reglas
- Persistencia de sesión

Este documento define la **línea base real de implementación**.

Fin del documento.