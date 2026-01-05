# ⚡ IMPLEMENTACIÓN PRAGMÁTICA - HOY (45 MINUTOS)

**Objetivo:** Que frontend y backend se comuniquen sin errores CORS, con seguridad básica y variables de entorno.

**Tiempo:** 45 minutos  
**Dificultad:** Baja  
**Valor:** 80% de lo que la propuesta "enterprise" promete, con 20% del esfuerzo

---

## PASO 1️⃣: USUARIO MySQL LIMITADO (15 minutos)

### ¿Por qué?
Ahora tu backend se conecta con usuario root o sin usuario.  
En producción = **riesgo de seguridad crítico**.  
Un usuario limitado no puede hacer `DROP DATABASE` accidentalmente.

### Ejecutar

Abre terminal y conecta a MySQL:

```bash
sudo mysql -u root -p
# Ingresa tu contraseña de root
```

Copia y pega TODO esto en la consola MySQL:

```sql
-- 1. Eliminar usuario anterior si existe
DROP USER IF EXISTS 'cirujano_app'@'localhost';

-- 2. Crear usuario NUEVO con contraseña FUERTE
CREATE USER 'cirujano_app'@'localhost' 
IDENTIFIED BY 'S3cur3_C1rujano_2024!';

-- 3. Crear BD
CREATE DATABASE IF NOT EXISTS cirujano_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 4. Otorgar permisos ESPECÍFICOS (no todos)
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE 
ON cirujano_db.* 
TO 'cirujano_app'@'localhost';

-- 5. Aplicar cambios
FLUSH PRIVILEGES;

-- 6. Verificar (opcional, verás "cirujano_db" en la lista)
SHOW DATABASES;
```

**Salir de MySQL:**
```bash
exit
```

### Verificar que funciona

```bash
# Conectar con el usuario nuevo
mysql -u cirujano_app -p cirujano_db
# Ingresa: S3cur3_C1rujano_2024!

# Si ves esto = ÉXITO
mysql> SELECT 'Funciona!' AS resultado;
```

✅ **PASO 1 COMPLETADO**

---

## PASO 2️⃣: ARCHIVO `.env` CENTRALIZADO (10 minutos)

### ¿Por qué?
Las contraseñas **NUNCA** van en el código.  
Las variables sensibles van en un archivo `.env` que **NO se sube a Git**.

### Crear archivo

En la raíz de tu proyecto **backend**, crea archivo `.env`:

```bash
cd /mnt/CZ_BODEGA/010_VSCODE/007_PROYECTOS_WEB/backend
touch .env
```

Abre el archivo y pega ESTO:

```env
# ==== DATABASE ====
DB_USER=cirujano_app
DB_PASSWORD=S3cur3_C1rujano_2024!
DB_HOST=localhost
DB_PORT=3306
DB_NAME=cirujano_db

# ==== SEGURIDAD ====
SECRET_KEY=cirujano_secret_key_super_seguro_cambiar_en_produccion_123456789

# ==== ENTORNO ====
ENV=development
DEBUG=True
```

### Proteger el archivo (Git)

Abre `.gitignore` en la raíz del backend y asegúrate que tenga:

```
.env
.env.local
.env.*.local
__pycache__/
.venv/
.pytest_cache/
```

**Verificar:**

```bash
git status | grep .env
# No debe aparecer. Si aparece, está mal.
```

✅ **PASO 2 COMPLETADO**

---

## PASO 3️⃣: ACTUALIZAR `config.py` DEL BACKEND (10 minutos)

### ¿Por qué?
Tu `config.py` actualmente tiene hardcodeadas las credenciales.  
Necesita cargar desde `.env`.

### Buscar y reemplazar

Abre: `/mnt/CZ_BODEGA/010_VSCODE/007_PROYECTOS_WEB/backend/config.py`

Reemplaza TODO el contenido con:

```python
"""
Configuración centralizada de la aplicación.
Carga variables desde .env para desarrollo.
"""

import os
from dotenv import load_dotenv

# Cargar variables de .env
load_dotenv()

class Settings:
    """Configuración de la aplicación"""
    
    # === DATABASE ===
    DB_USER = os.getenv("DB_USER", "cirujano_app")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "cirujano_db")
    
    @property
    def DATABASE_URL(self):
        """Construir URL de conexión MySQL"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # === SECURITY ===
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    ALGORITHM = "HS256"
    
    # === ENVIRONMENT ===
    ENV = os.getenv("ENV", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # === CORS (Frontend) ===
    ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ]

# Instancia global
settings = Settings()

# Para importar: from config import settings
```

**Guardar archivo.**

✅ **PASO 3 COMPLETADO**

---

## PASO 4️⃣: PROXY EN VITE (5 minutos)

### ¿Por qué?
Ahora frontend está en `http://localhost:5173` y backend en `http://localhost:8000`.  
Cuando el frontend hace `fetch('/api/marcas')`, necesita ir al backend automáticamente.  
Sin proxy = error CORS.  
Con proxy = funciona transparente.

### Actualizar vite.config.js

Abre: `/mnt/CZ_BODEGA/010_VSCODE/007_PROYECTOS_WEB/cirujano-front/vite.config.js`

Reemplaza COMPLETO con:

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  base: '/',
  plugins: [vue()],
  
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  
  // === PROXY (Frontend → Backend) ===
  server: {
    port: 5173,
    strictPort: false,
    
    proxy: {
      // Cualquier request a /api se reenvía al backend
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },

  css: {
    preprocessorOptions: {
      scss: {
        silenceDeprecations: ["color-functions", "global-builtin", "import"],
      },
    },
  },
})
```

**Guardar archivo.**

✅ **PASO 4 COMPLETADO**

---

## PASO 5️⃣: VERIFICAR QUE FUNCIONA (5 minutos)

### 5.1 Levanta el Backend

Terminal 1:

```bash
cd /mnt/CZ_BODEGA/010_VSCODE/007_PROYECTOS_WEB/backend
source .venv/bin/activate  # Activar virtualenv Python
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Deberías ver:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 5.2 Levanta el Frontend

Terminal 2:

```bash
cd /mnt/CZ_BODEGA/010_VSCODE/007_PROYECTOS_WEB/cirujano-front
npm run dev
```

Deberías ver:

```
VITE v6.4.1 ready in 456 ms
  ➜  Local:   http://localhost:5173/
```

### 5.3 Testea la Conexión

Abre DevTools en `http://localhost:5173`:

```
Console → Escribe:
fetch('/api/marcas').then(r => r.json()).then(console.log)
```

Si ves la respuesta de datos = ✅ FUNCIONA

Si ves error CORS = ❌ Algo salió mal (revisar logs)

✅ **VERIFICACIÓN COMPLETADA**

---

## 📋 CHECKLIST FINAL

Marca cada cosa conforme la termines:

```
[ ] 1. Usuario MySQL creado ('cirujano_app')
[ ] 2. BD 'cirujano_db' existe
[ ] 3. Archivo .env creado con credenciales
[ ] 4. .gitignore protege .env
[ ] 5. config.py actualizado a cargar desde .env
[ ] 6. vite.config.js tiene proxy configurado
[ ] 7. Backend corriendo en localhost:8000
[ ] 8. Frontend corriendo en localhost:5173
[ ] 9. fetch('/api/marcas') retorna datos
```

Si todos están ✅ = **HEMOS TERMINADO EXITOSAMENTE**

---

## 🎯 QUÉ LOGRAMOS EN 45 MINUTOS

✅ **Seguridad**
- Usuario BD limitado (sin acceso root)
- Variables sensibles protegidas en .env
- .gitignore previene commits accidentales

✅ **Infraestructura**
- Frontend y Backend se comunican sin CORS
- Proxy automático (transparente para el código)
- Configuración centralizada

✅ **Desarrollo**
- Entorno limpio y profesional
- Fácil de escalar (agregar más variables después)
- Listo para migrar a producción

---

## 🚀 PRÓXIMAS ACCIONES

Una vez que confirmes que TODO funciona:

1. **Conectar Frontend con Backend**
   - DiagnosticWizard.vue hará `fetch('/api/diagnosticos')`
   - Backend responderá con datos

2. **Crear endpoints faltantes**
   - GET `/api/marcas`
   - GET `/api/marcas/:id/instrumentos`
   - POST `/api/diagnosticos/submit`

3. **Testear flujo completo**
   - Usuario selecciona marca → endpoint GET retorna datos
   - Usuario confirma → POST guarda en BD

**Estimado:** 2-3 horas más

---

## ❓ PREGUNTAS COMUNES

**P: ¿Por qué proxy en Vite?**  
R: Sin proxy, frontend hace `fetch('/api/marcas')` y va a `localhost:5173/api`, que no existe. Con proxy, Vite redirige a `localhost:8000/api`.

**P: ¿Y en producción?**  
R: En producción tendrás un Nginx/Caddy en el mismo servidor haciendo proxy. Mismo concepto, otra herramienta.

**P: ¿Puedo usar la contraseña 'password'?**  
R: No. Usa contraseñas fuertes: Mix de mayúsculas, minúsculas, números, símbolos. MySQL rechaza contraseñas débiles de todas formas.

**P: ¿Dónde se guardan las variables?**  
R: En `.env` (local, en tu máquina). En producción, configuras en variables de entorno del servidor.

**P: ¿Si me olvido de agregar .env a .gitignore?**  
R: ¡PELIGRO! Se sube la contraseña a GitHub pública. Si pasa, regenera la contraseña MySQL inmediatamente.

---

## ✨ RESULTADO FINAL

Tendrás:
- ✅ Backend seguro (usuario limitado)
- ✅ Variables protegidas (.env)
- ✅ Frontend ↔ Backend comunicándose
- ✅ Código listo para producción (sin cambios mayores)

**¿Comenzamos?** 👍

---

*Guía pragmática para Cristóbal - Cirujano de Sintetizadores*  
*Enero 5, 2026*
