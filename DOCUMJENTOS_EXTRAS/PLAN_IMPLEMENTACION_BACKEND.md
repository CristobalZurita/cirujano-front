# 🏗️ PLAN DE IMPLEMENTACIÓN - BACKEND CIRUJANO

**Estado:** Frontend ✅ Funcionando | Backend ⏳ Listo para implementar  
**Fecha:** Enero 2026  
**Responsable:** Cristóbal

---

## 📋 RESUMEN EJECUTIVO

El **frontend está 100% funcional**. Ahora necesitamos el backend que procese las cotizaciones.

### Estado Actual
- ✅ Landing page completa (Hero, About, Services, History, FAQ, Reviews, Contact)
- ✅ Botón "COTIZA YA" que aparece tras primer scroll
- ✅ Formulario de 5 pasos (Marca → Modelo → Problemas → Contacto → Confirmación)
- ⏳ **Falta:** Backend que calcule cotizaciones y guarde diagnósticos

---

## 🎯 PROPUESTA TÉCNICA

### Stack Recomendado
| Capa | Tecnología | Razón |
|------|-----------|-------|
| **Frontend** | Vue 3 + Vite | ✅ Ya implementado |
| **Backend** | PHP 8.x | Nativo en cPanel (minimalmarimba.cl) |
| **BD** | MySQL 8.x | Incluido en hosting |
| **IA** | Claude (Anthropic) | Análisis de texto del usuario |
| **Hosting** | Tu cPanel | Sin costos adicionales |

### Opción Alternativa (Recomendada)
| Capa | Tecnología | Razón |
|------|-----------|-------|
| **Backend** | Python FastAPI | Más moderno, mejor para IA |
| **Hosting** | PythonAnywhere.com | Hosting gratuito para pequeños proyectos |
| **BD** | MySQL/SQLite | En PythonAnywhere |

**VENTAJAS de FastAPI sobre PHP:**
- ✅ Integración más limpia con APIs de IA
- ✅ Tipado estático (menos bugs)
- ✅ Mejor rendimiento
- ✅ Hosting gratuito en PythonAnywhere
- ✅ Reutilizas código Python ya escrito

---

## 🗄️ BASE DE DATOS (MySQL)

### Tablas Necesarias

```sql
-- 1. MARCAS
CREATE TABLE marcas (
  id VARCHAR(50) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  tier ENUM('legendary','professional','standard','boutique','historic'),
  pais VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. INSTRUMENTOS
CREATE TABLE instrumentos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  marca_id VARCHAR(50) NOT NULL,
  modelo VARCHAR(100) NOT NULL,
  tipo ENUM('sintetizador','piano','organo','controlador','modular','sampler'),
  año_inicio INT,
  imagen_url VARCHAR(255),
  componentes JSON NOT NULL,
  valor_estimado_min INT,
  valor_estimado_max INT,
  factor_complejidad DECIMAL(3,2) DEFAULT 1.00,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (marca_id) REFERENCES marcas(id),
  UNIQUE KEY (marca_id, modelo)
);

-- 3. DIAGNOSTICOS
CREATE TABLE diagnosticos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(20) UNIQUE NOT NULL,  -- CDS-001, CDS-002...
  instrumento_id INT,
  cliente_nombre VARCHAR(200) NOT NULL,
  cliente_email VARCHAR(200) NOT NULL,
  cliente_telefono VARCHAR(50),
  descripcion_usuario TEXT NOT NULL,  -- Lo que escribió el usuario
  analisis_ia JSON,  -- Respuesta de Claude
  problemas_confirmados JSON,  -- Lo que confirmó el usuario
  cotizacion_min INT,
  cotizacion_max INT,
  estado ENUM('pendiente','cotizado','aprobado','en_taller','finalizado','entregado','cancelado'),
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (instrumento_id) REFERENCES instrumentos(id)
);

-- 4. PRECIOS_COMPONENTES
CREATE TABLE precios_componentes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  componente VARCHAR(50) NOT NULL,
  tipo_falla VARCHAR(50) NOT NULL,
  precio_base INT NOT NULL,  -- En CLP
  precio_por_unidad INT DEFAULT 0,
  UNIQUE KEY (componente, tipo_falla)
);
```

---

## 🔌 ENDPOINTS API

### POST `/api/diagnostic/submit`
**Envía:** Datos del diagnóstico del usuario  
**Retorna:** Cotización, código de diagnóstico, resumen

```json
// REQUEST
{
  "marca_id": "roland",
  "modelo_id": "juno-106",
  "problemas": [
    {
      "componente": "botones",
      "tipo_falla": "intermitente",
      "cantidad": 3
    },
    {
      "componente": "slider",
      "tipo_falla": "ruido",
      "cantidad": 1
    }
  ],
  "cliente": {
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "+56 9 1234 5678"
  }
}

// RESPONSE
{
  "codigo_diagnostico": "CDS-20260105-001",
  "cotizacion_minima": 450000,
  "cotizacion_maxima": 650000,
  "desglose": [
    {
      "componente": "botones",
      "cantidad": 3,
      "precio_unitario": 25000,
      "subtotal": 75000
    },
    {
      "componente": "slider",
      "cantidad": 1,
      "precio_unitario": 35000,
      "subtotal": 35000
    }
  ],
  "factor_complejidad": 1.15,
  "url_pdf": "/descargas/CDS-20260105-001.pdf",
  "mensaje": "Cotización lista. Válida por 30 días."
}
```

### GET `/api/diagnosticos/:codigo`
**Obtiene:** Detalles de un diagnóstico previo

### GET `/api/marcas`
**Obtiene:** Lista de todas las marcas disponibles

### GET `/api/marcas/:marca_id/instrumentos`
**Obtiene:** Instrumentos de una marca específica

---

## 🤖 INTEGRACIÓN CON CLAUDE (IA)

### Flujo de Análisis Inteligente

```
Usuario escribe:
"Mi Juno-106 tiene 3 botones que no responden bien"
         ↓
Backend envía a Claude API:
{
  "modelo": "Juno-106",
  "componentes_disponibles": ["botones", "sliders", "teclas", "display", "fuente"],
  "texto_usuario": "Mi Juno-106 tiene 3 botones que no responden bien"
}
         ↓
Claude responde:
{
  "problemas_detectados": [
    {
      "componente": "botones",
      "tipo_falla": "intermitente",
      "cantidad": 3,
      "confianza": 0.95
    }
  ],
  "preguntas_sugeridas": [
    "¿El problema es intermitente o constante?",
    "¿Afecta a todo el teclado o solo a ciertos botones?"
  ]
}
         ↓
Backend retorna al Frontend para confirmación del usuario
```

### Costo de la API Claude
- ~$0.01 - $0.03 USD por diagnóstico
- 100 diagnósticos/mes ≈ $1-3 USD
- **Muy económico**

---

## 📅 PLAN DE IMPLEMENTACIÓN (4 FASES)

### ✅ FASE 0 - COMPLETADA
- [x] Frontend Vue 3 funcional
- [x] Botón flotante "COTIZA YA"
- [x] Formulario de 5 pasos
- [x] Sistema de loader y navegación

### ⏳ FASE 1 - BASE DE DATOS (1-2 días)
- [ ] Crear base de datos MySQL
- [ ] Crear tablas (marcas, instrumentos, diagnósticos, precios)
- [ ] Poblar datos iniciales (50 marcas, 100+ instrumentos)
- [ ] Configurar credenciales en `.env`

### ⏳ FASE 2 - API BÁSICA (2-3 días)
- [ ] Crear endpoints GET (marcas, instrumentos)
- [ ] Crear endpoint POST (submit diagnóstico)
- [ ] Conectar BD con endpoints
- [ ] Testear con Postman

### ⏳ FASE 3 - INTELIGENCIA ARTIFICIAL (1-2 días)
- [ ] Configurar API de Anthropic (Claude)
- [ ] Implementar análisis de texto
- [ ] Integrar análisis en flujo de diagnóstico
- [ ] Testear con ejemplos reales

### ⏳ FASE 4 - OPTIMIZACIÓN (1 día)
- [ ] Generación de PDFs descargables
- [ ] Envío de emails automáticos
- [ ] Almacenamiento en BD
- [ ] Dashboard admin (opcional para Fase 2)

---

## 💾 TECNOLOGÍAS ESPECÍFICAS

### Opción A: PHP (En tu cPanel)
```php
// composer.json
{
  "require": {
    "anthropic/anthropic-sdk": "^1.0",
    "doctrine/orm": "^2.15"
  }
}
```

**Ventajas:**
- ✅ Sin cambiar hosting
- ✅ Configuración mínima

**Desventajas:**
- ❌ Menos moderno
- ❌ Más verboso

### Opción B: Python FastAPI (Recomendado)
```python
# requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
mysql-connector-python==8.2.0
anthropic==0.7.1
python-dotenv==1.0.0
```

**Ventajas:**
- ✅ Más limpio y moderno
- ✅ Mejor para IA
- ✅ Hosting gratuito en PythonAnywhere

**Desventajas:**
- ❌ Cambiar hosting
- ❌ Aprendizaje curva pequeña

---

## 🚀 MIS RECOMENDACIONES

### Para Implementar RÁPIDO (Próximos 7 días)

1. **Usa FastAPI en PythonAnywhere** (gratis y moderno)
2. **Comienza con 50 marcas/instrumentos reales** (no 100+)
3. **Implementa cálculo de precios SIN IA primero**
4. **Integra Claude después** (Fase 3)

### Razones:
- ✅ Más rápido de implementar
- ✅ Menos bugs
- ✅ Escalable
- ✅ Gratis hasta producción

---

## 📊 TIMELINE ESTIMADO

```
Semana 1 (Días 1-2):    BD + Datos iniciales
Semana 1 (Días 3-4):    API básica (GET/POST)
Semana 2 (Día 5-6):     Claude IA
Semana 2 (Día 7):       Testing + Deploy
```

---

## ❓ PREGUNTAS ANTES DE COMENZAR

1. **¿Cuántos instrumentos tienes para empezar?**
   - Opción A: 50 (los más reparados) ← RECOMENDADO
   - Opción B: 100+
   - Opción C: Pocas, y agregar conforme surja demanda

2. **¿Hosting PHP en cPanel o Python en PythonAnywhere?**
   - PHP: Más rápido, pero menos flexible
   - Python: Más flexible, mejor para IA

3. **¿Con o sin IA en Fase 1?**
   - Con IA: Más inteligente, +costo
   - Sin IA: Más simple, igual de funcional

4. **¿Generar PDFs y enviar emails?**
   - Sí: Más profesional, más código
   - No: MVP simple primero

---

## 📞 PRÓXIMOS PASOS

**Mi propuesta:**
```
1. Confirmas decisiones (hosting, cantidad instrumentos, con/sin IA)
2. Creamos estructura de BD en MySQL
3. Poblamos datos iniciales
4. Implementamos API GET/POST
5. Testeamos con frontend
6. Iteramos hasta perfeccionar
```

**¿Aprobado?** 👍

---

*Documento técnico preparado para el taller Cirujano de Sintetizadores*
