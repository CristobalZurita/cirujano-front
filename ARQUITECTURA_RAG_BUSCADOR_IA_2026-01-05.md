ARQUITECTURA RAG — BUSCADOR INTELIGENTE

ARQUITECTURA RAG

Buscador Inteligente Asistido por IA

Sistema de Diagnóstico para Sintetizadores

Cirujano de Sintetizadores — Enero 2026

1. RESUMEN EJECUTIVO

Este documento describe la arquitectura técnica para implementar un buscador inteligente basado en RAG (Retrieval-Augmented Generation) para el sistema de diagnóstico de sintetizadores. El sistema permitirá a los clientes describir fallas en lenguaje natural y recibir diagnósticos preliminares, cotizaciones estimadas y recomendaciones basadas en una base de conocimiento especializada.

1.1 Objetivos del Sistema

Diagnóstico asistido por IA: El cliente describe la falla y el sistema sugiere posibles causas

Cotización inteligente: Estimaciones automáticas basadas en el historial de reparaciones

Base de conocimiento: Información técnica de sintetizadores indexada semánticamente

Búsqueda semántica: Encontrar información por significado, no solo por palabras clave

Trazabilidad: Citar fuentes y documentación técnica en las respuestas

2. ARQUITECTURA GENERAL RAG

RAG (Retrieval-Augmented Generation) combina búsqueda semántica con generación de texto mediante LLM. En lugar de depender solo del conocimiento del modelo, el sistema recupera información relevante de una base de datos vectorial y la usa como contexto para generar respuestas precisas y verificables.

2.1 Flujo de Datos

| PASO | COMPONENTE                | DESCRIPCIÓN                                                         |
| ---- | ------------------------- | -------------------------------------------------------------------- |
| 1    | Ingesta de Documentos     | Service manuals, guías de reparación, historial → chunks de texto |
| 2    | Generación de Embeddings | Cada chunk se convierte en vector numérico (1536 dimensiones)       |
| 3    | Almacenamiento Vectorial  | Vectores guardados en PostgreSQL + pgvector                          |
| 4    | Query del Usuario         | "Mi Prophet-5 no enciende" → embedding de consulta                  |
| 5    | Búsqueda por Similitud   | Encontrar los K documentos más similares (cosine similarity)        |
| 6    | Generación con Contexto  | LLM genera respuesta usando documentos recuperados                   |
| 7    | Respuesta con Citas       | Diagnóstico + fuentes + cotización estimada                        |

2.2 Diagrama de Componentes

┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Vue.js)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ DiagnosticWiz│  │  ChatWidget  │  │   ResultsDisplay     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │ API REST / WebSocket
┌───────────────────────────▼─────────────────────────────────────┐
│                     BACKEND (FastAPI)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ /api/search  │  │ /api/diagnose│  │   /api/quote         │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │               │
│  ┌──────▼─────────────────▼──────────────────────▼───────────┐  │
│  │               RAG Service Layer                            │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐   │  │
│  │  │ Embedder   │  │ Retriever  │  │   LLM Generator    │   │  │
│  │  │(Voyage/OAI)│  │ (pgvector) │  │   (Claude/GPT)     │   │  │
│  │  └────────────┘  └────────────┘  └────────────────────┘   │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    PostgreSQL + pgvector                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ knowledge_   │  │ repair_      │  │   instruments        │  │
│  │ embeddings   │  │ history      │  │                      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

3. STACK TECNOLÓGICO RECOMENDADO

3.1 Modelos de Embeddings

Los embeddings convierten texto en vectores numéricos que capturan significado semántico. Textos similares tendrán vectores cercanos en el espacio vectorial.

| PROVEEDOR      | MODELO                 | DIMENSIONES | PRECIO/1M | RECOMENDADO   |
| -------------- | ---------------------- | ----------- | --------- | ------------- |
| OpenAI         | text-embedding-3-small | 1536        | $0.02     | ✓ Balance    |
| OpenAI         | text-embedding-3-large | 3072        | $0.13     | Máx. calidad |
| Voyage AI      | voyage-3.5             | 1024        | $0.06     | ✓ Con Claude |
| Voyage AI      | voyage-3-large         | 1024        | $0.18     | Enterprise    |
| Local (Ollama) | nomic-embed-text       | 768         | $0.00     | Sin costo     |
| HuggingFace    | all-mpnet-base-v2      | 768         | $0.00     | Open source   |

3.2 Modelos LLM para Generación

| PROVEEDOR      | MODELO            | CONTEXTO    | USO RECOMENDADO        |
| -------------- | ----------------- | ----------- | ---------------------- |
| Anthropic      | Claude 3.5 Sonnet | 200K tokens | ✓ Principal (calidad) |
| Anthropic      | Claude 3.5 Haiku  | 200K tokens | ✓ Alto volumen        |
| OpenAI         | GPT-4o            | 128K tokens | Alternativa            |
| OpenAI         | GPT-4o-mini       | 128K tokens | Económico             |
| Local (Ollama) | Llama 3.1 70B     | 128K tokens | Sin costo / privacidad |

3.3 Base de Datos Vectorial

PostgreSQL con la extensión pgvector es la opción recomendada porque ya está en el stack propuesto (VOLCADO10) y evita agregar infraestructura adicional.

| OPCIÓN               | VENTAJAS                                       | DESVENTAJAS                           |
| --------------------- | ---------------------------------------------- | ------------------------------------- |
| PostgreSQL + pgvector | Ya en stack, SQL familiar, ACID, índices HNSW | Requiere tuning para >1M vectores     |
| Qdrant                | Optimizado para vectores, filtros avanzados    | Servicio adicional, curva aprendizaje |
| Pinecone              | Managed, escala automática, rápido           | Costo mensual, vendor lock-in         |
| ChromaDB              | Simple, Python nativo, desarrollo rápido      | No ideal para producción             |

Página  de

ARQUITECTURA RAG — BUSCADOR INTELIGENTE

4. MODELO DE DATOS VECTORIAL

4.1 Esquema de Tablas

Extensión pgvector y tabla principal:

-- Habilitar extensión pgvector

CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla de documentos de conocimiento

CREATE TABLE knowledge_documents (

    id SERIAL PRIMARY KEY,

    title VARCHAR(255) NOT NULL,

    content TEXT NOT NULL,

    source_type VARCHAR(50),  -- 'manual', 'repair_log', 'faq'

    instrument_brand VARCHAR(100),

    instrument_model VARCHAR(100),

    metadata JSONB,

    created_at TIMESTAMP DEFAULT NOW()

);

Tabla de embeddings:

-- Tabla de embeddings (chunks)

CREATE TABLE knowledge_embeddings (

    id SERIAL PRIMARY KEY,

    document_id INTEGER REFERENCES knowledge_documents(id),

    chunk_index INTEGER NOT NULL,

    chunk_text TEXT NOT NULL,

    embedding VECTOR(1536),  -- OpenAI text-embedding-3-small

    token_count INTEGER,

    created_at TIMESTAMP DEFAULT NOW()

);

Índice HNSW para búsqueda rápida:

-- Índice HNSW para búsqueda por similitud coseno

CREATE INDEX ON knowledge_embeddings

USING hnsw (embedding vector_cosine_ops)

WITH (m = 16, ef_construction = 64);

4.2 Query de Búsqueda Semántica

-- Buscar los 5 chunks más similares a un query

SELECT

    ke.chunk_text,

    kd.title,

    kd.instrument_brand,

    1 - (ke.embedding <=> $1::vector) AS similarity

FROM knowledge_embeddings ke

JOIN knowledge_documents kd ON ke.document_id = kd.id

WHERE kd.instrument_brand = $2  -- Filtro opcional

ORDER BY ke.embedding <=> $1::vector

LIMIT 5;

5. IMPLEMENTACIÓN BACKEND

5.1 Estructura de Directorios

backend/app/
├── core/
│   ├── config.py          # Settings incluyendo API keys
│   └── deps.py            # Database session
├── rag/                   # ← NUEVO MÓDULO RAG
│   ├── __init__.py
│   ├── embeddings.py      # Generación de embeddings
│   ├── retriever.py       # Búsqueda en pgvector
│   ├── generator.py       # Llamadas a LLM
│   ├── chunker.py         # División de documentos
│   └── service.py         # Orquestador RAG
├── api/v1/
│   ├── router.py
│   └── endpoints/
│       ├── diagnostic.py   # ← Endpoint de diagnóstico IA
│       └── knowledge.py    # ← CRUD de conocimiento
├── models/
│   ├── knowledge.py       # ← Modelos SQLAlchemy
│   └── embedding.py
└── schemas/
    ├── diagnostic.py      # ← Pydantic schemas
    └── knowledge.py

5.2 Dependencias Adicionales (pyproject.toml)

| PAQUETE   | VERSIÓN | PROPÓSITO                          |
| --------- | -------- | ----------------------------------- |
| openai    | ^1.50.0  | Embeddings y GPT (opcional)         |
| anthropic | ^0.40.0  | Claude API para generación         |
| voyageai  | ^0.3.0   | Embeddings (recomendado con Claude) |
| pgvector  | ^0.3.0   | Soporte vectores en SQLAlchemy      |
| langchain | ^0.3.0   | Opcional: framework RAG             |
| tiktoken  | ^0.8.0   | Conteo de tokens                    |
| numpy     | ^1.26.0  | Operaciones vectoriales             |

Página  de

ARQUITECTURA RAG — BUSCADOR INTELIGENTE

6. BASE DE CONOCIMIENTO PARA SINTETIZADORES

6.1 Fuentes de Datos a Indexar

| TIPO                   | CONTENIDO                                    | FORMATO                |
| ---------------------- | -------------------------------------------- | ---------------------- |
| Service Manuals        | Manuales técnicos oficiales de fabricantes  | PDF → texto extraído |
| Repair Logs            | Historial de reparaciones propias            | Base de datos / JSON   |
| FAQ Técnico           | Preguntas frecuentes por instrumento         | Markdown / JSON        |
| Troubleshooting Guides | Guías de diagnóstico paso a paso           | Markdown estructurado  |
| Parts Catalogs         | Catálogos de repuestos y compatibilidad     | CSV / JSON             |
| Forum Knowledge        | Soluciones de foros especializados (curadas) | Texto estructurado     |

6.2 Estrategia de Chunking

El chunking divide documentos grandes en fragmentos manejables para embeddings. La estrategia correcta es crucial para la calidad de la búsqueda.

| ESTRATEGIA   | TAMAÑO CHUNK       | CASO DE USO                              |
| ------------ | ------------------- | ---------------------------------------- |
| Fixed Size   | 500-1000 tokens     | Documentos uniformes, manuales técnicos |
| Semantic     | Variable            | Contenido con secciones claras, FAQs     |
| Recursive    | 500 + overlap 100   | ✓ Recomendado: balance calidad/costo    |
| Parent-Child | Pequeño + contexto | Troubleshooting con pasos dependientes   |

6.3 Ejemplo de Documento Indexado

{
  "title": "Prophet-5 Rev 3.3 - Power Supply Troubleshooting",
  "source_type": "service_manual",
  "instrument_brand": "Sequential",
  "instrument_model": "Prophet-5",
  "metadata": {
    "section": "Power Supply",
    "revision": "3.3",
    "page": 42,
    "tags": ["power", "no-boot", "voltage"]
  },
  "content": "Si el Prophet-5 no enciende, verificar primero el fusible F1
               (250mA slow-blow). Medir voltajes en el conector J5: +15V,
               -15V, +5V. Si +5V está ausente, revisar regulador 7805..."
}

7. API ENDPOINTS

7.1 Endpoints RAG

| MÉTODO | ENDPOINT                 | DESCRIPCIÓN                           |
| ------- | ------------------------ | -------------------------------------- |
| POST    | /api/v1/diagnose         | Diagnóstico asistido por IA           |
| POST    | /api/v1/search           | Búsqueda semántica en knowledge base |
| POST    | /api/v1/chat             | Chat conversacional con contexto RAG   |
| POST    | /api/v1/knowledge/ingest | Ingestar nuevo documento               |
| GET     | /api/v1/knowledge/{id}   | Obtener documento por ID               |
| DELETE  | /api/v1/knowledge/{id}   | Eliminar documento y embeddings        |

7.2 Ejemplo Request/Response

POST /api/v1/diagnose

// Request
{
  "instrument_brand": "Sequential",
  "instrument_model": "Prophet-5",
  "symptoms": "No enciende, sin luces, sin sonido",
  "additional_info": "Estuvo guardado 2 años"
}

// Response
{
  "diagnosis": {
    "probable_causes": [
      {
        "cause": "Fusible F1 quemado",
        "probability": 0.75,
        "explanation": "Causa más común después de almacenamiento prolongado"
      },
      {
        "cause": "Capacitores de fuente secos",
        "probability": 0.60,
        "explanation": "Los electrolíticos se degradan sin uso"
      }
    ],
    "recommended_actions": [
      "Verificar fusible F1 (250mA slow-blow)",
      "Medir voltajes en J5: +15V, -15V, +5V",
      "Inspección visual de capacitores"
    ]
  },
  "quote_estimate": {
    "min_clp": 45000,
    "max_clp": 180000,
    "note": "Rango según complejidad de fuente"
  },
  "sources": [
    {
      "title": "Prophet-5 Service Manual",
      "section": "Power Supply Troubleshooting",
      "page": 42
    }
  ],
  "confidence": 0.85
}

Página  de

ARQUITECTURA RAG — BUSCADOR INTELIGENTE

8. INTEGRACIÓN FRONTEND

8.1 Componentes Vue.js Requeridos

| COMPONENTE            | DESCRIPCIÓN                                           |
| --------------------- | ------------------------------------------------------ |
| DiagnosticWizard.vue  | Ya existe: agregar integración con endpoint /diagnose |
| AIChatWidget.vue      | NUEVO: Widget de chat flotante con streaming           |
| DiagnosticResults.vue | NUEVO: Mostrar diagnóstico, causas, acciones          |
| QuoteEstimate.vue     | NUEVO: Mostrar rango de cotización estimada           |
| SourceCitations.vue   | NUEVO: Mostrar fuentes con links a documentación      |

8.2 Composable para RAG

src/composables/useAIDiagnostic.js

import { ref, computed } from 'vue'

export function useAIDiagnostic() {
  const isLoading = ref(false)
  const diagnosis = ref(null)
  const error = ref(null)

  async function diagnose(instrumentData) {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch('/api/v1/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(instrumentData)
      })

    if (!response.ok) throw new Error('Error en diagnóstico')

    diagnosis.value = await response.json()
    } catch (e) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  const topCause = computed(() =>
    diagnosis.value?.diagnosis?.probable_causes?.[0] || null
  )

  return { isLoading, diagnosis, error, diagnose, topCause }
}

9. CONSIDERACIONES DE PRODUCCIÓN

9.1 Seguridad

API Keys en variables de entorno (nunca en código)

Rate limiting en endpoints de IA (costosos)

Validación de inputs para prevenir prompt injection

Logging de queries para auditoría

9.2 Optimización de Costos

Cache de embeddings para queries repetidos

Batch processing para ingesta de documentos

Usar modelo más económico para queries simples

Streaming responses para mejor UX y timeout handling

9.3 Monitoreo

Métricas de latencia por endpoint

Tracking de tokens consumidos (costos)

Feedback de usuarios sobre calidad de respuestas

Alertas de errores en llamadas a APIs externas

10. ESTIMACIÓN DE COSTOS MENSUALES

| COMPONENTE                  | USO ESTIMADO      | COSTO USD            | COSTO CLP |
| --------------------------- | ----------------- | -------------------- | --------- |
| OpenAI Embeddings           | 500K tokens/mes   | $0.01     | $10      |           |
| Claude Sonnet (generación) | 200 consultas/mes | $6.00     | $6,000   |           |
| PostgreSQL (Render/Railway) | Starter plan      | $7.00     | $7,000   |           |
| TOTAL ESTIMADO              |                   | ~$13/mes  | ~$13,000 |           |

Nota: Costos escalables según uso. La opción local con Ollama elimina costos de API pero requiere GPU.

11. ROADMAP DE IMPLEMENTACIÓN

| FASE | SEMANAS     | ENTREGABLES                                            |
| ---- | ----------- | ------------------------------------------------------ |
| 1    | Semana 1-2  | pgvector configurado, modelo de datos, ingesta básica |
| 2    | Semana 3-4  | Servicio RAG, embeddings, búsqueda semántica         |
| 3    | Semana 5-6  | Integración LLM, endpoint /diagnose, generación      |
| 4    | Semana 7-8  | Frontend integrado, widget chat, testing               |
| 5    | Semana 9-10 | Optimización, caché, monitoreo, documentación       |

12. CONCLUSIÓN

La implementación de un buscador inteligente RAG para Cirujano de Sintetizadores representa una ventaja competitiva significativa. El sistema permitirá ofrecer diagnósticos preliminares automatizados, reducir tiempo de cotización, y escalar el conocimiento técnico acumulado en 12+ años de experiencia. La arquitectura propuesta se integra con el stack existente (PostgreSQL + FastAPI + Vue.js) minimizando la complejidad adicional, con costos operativos controlados (~$13 USD/mes) y un roadmap de 10 semanas para implementación completa.

— Fin del documento —

Página  de

* 
* [•••]()
