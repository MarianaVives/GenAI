# 🔐 Guía de Seguridad: Almacenamiento de Claves de API

## 📋 Tabla de Contenidos
1. [Introducción](#introducción)
2. [¿Por qué es importante?](#por-qué-es-importante)
3. [Mejores prácticas](#mejores-prácticas)
4. [Implementación en esta aplicación](#implementación-en-esta-aplicación)
5. [Configuración de desarrollo vs. producción](#configuración-de-desarrollo-vs-producción)
6. [Auditoría de seguridad](#auditoría-de-seguridad)

---

## Introducción

Las claves de API son credenciales sensibles que otorgan acceso a servicios externos. Una clave comprometida puede resultar en:
- 🚨 Acceso no autorizado a tus servicios
- 💰 Cargos inesperados por uso malicioso
- 📊 Filtración de datos sensibles
- 🔓 Vulnerabilidades en tu aplicación

---

## ¿Por qué es importante?

### ❌ NUNCA Hagas Esto:
```python
# MAL: Hardcodear claves en el código
API_KEY = "sk-1234567890abcdef"  # ¡NUNCA!
DB_PASSWORD = "admin123"          # ¡NUNCA!
JWT_SECRET = "mi-secreto"         # ¡NUNCA!

# MAL: Guardar en control de versiones
git add config.py  # Ahora la clave está en GitHub para siempre
```

### ✅ SIEMPRE Haz Esto:
```python
# BIEN: Usar variables de entorno
import os
from dotenv import load_dotenv

load_dotenv()  # Carga desde .env
API_KEY = os.getenv('API_KEY')
DB_PASSWORD = os.getenv('DB_PASSWORD')
```

---

## Mejores prácticas

### 1. **Usa Variables de Entorno**
Las variables de entorno son valores que el sistema operativo proporciona a la aplicación sin incluirlos en el código fuente.

```bash
# En Linux/Mac:
export API_KEY="tu-clave-aqui"
export FLASK_SECRET_KEY="tu-secreto-aqui"

# En Windows:
set API_KEY=tu-clave-aqui
set FLASK_SECRET_KEY=tu-secreto-aqui
```

### 2. **Usa Archivos .env para Desarrollo**
El archivo `.env` almacena variables de entorno localmente sin comprometer el control de versiones.

```bash
# .env (NO COMITEAR)
API_KEY=sk-dev-1234567890abcdef
DATABASE_URL=postgresql://user:password@localhost/db
FLASK_SECRET_KEY=desarrollo-clave-secreta
```

### 3. **Exluye .env del Control de Versiones**
Ya está hecho en tu `.gitignore`:
```gitignore
# Nunca versionaremos estos archivos:
.env
.env.local
.env.*.local
```

### 4. **Crea un Archivo .env.example**
Sirve como plantilla para nuevos desarrolladores:

```bash
# .env.example (COMITEAR ESTE ARCHIVO)
API_KEY=        # Tu clave API aquí
DATABASE_URL=   # URL de conexión BD
FLASK_SECRET_KEY=   # Genera una clave segura
```

Los nuevos miembros del equipo copian este archivo:
```bash
cp .env.example .env
# Y luego llenan los valores correctos
```

### 5. **Genera Claves Seguras para Producción**
```bash
# Generar SECRET_KEY seguro (32 caracteres hexadecimales)
python -c "import secrets; print(secrets.token_hex(32))"

# Resultado: a3f8c2e9b1d4f6a7c9e2b1d4f6a7c9e2
```

### 6. **Valida las Variables de Entorno**
```python
# En tu aplicación, valida que existan
import os
from dotenv import load_dotenv

load_dotenv()

# Validar variables obligatorias
required_vars = ['API_KEY', 'FLASK_SECRET_KEY']
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"⚠️ Variable de entorno '{var}' no está definida en .env")

print("✅ Todas las variables obligatorias están configuradas")
```

### 7. **Usa Secretos Diferentes para Cada Entorno**
```bash
# .env.development
FLASK_ENV=development
FLASK_DEBUG=True
API_TIMEOUT=10

# .env.production
FLASK_ENV=production
FLASK_DEBUG=False
API_TIMEOUT=5
```

### 8. **Protege el Archivo .env**
```bash
# Restringir permisos de lectura (Linux/Mac)
chmod 600 .env

# En Windows, usa las propiedades de seguridad del archivo
# - Click derecho > Propiedades > Seguridad
# - Solo tu usuario debe tener acceso de lectura
```

---

## Implementación en esta aplicación

### 📁 Estructura de archivos actualizada:
```
weather-app/
├── .env                    # Variables locales (NO COMITEAR)
├── .env.example            # Plantilla de variables (COMITEAR)
├── .gitignore              # Excluye .env
├── config/
│   └── settings.py         # Carga desde variables de entorno
└── requirements.txt        # Incluye python-dotenv
```

### 🔧 Cómo configurar tu aplicación:

#### 1. **Instala las dependencias actualizadas:**
```bash
pip install -r requirements.txt
```

#### 2. **Crea tu archivo .env local:**
```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Abre .env y personaliza los valores:
nano .env  # o tu editor favorito
```

#### 3. **Usa las variables en tu código:**
```python
from config import settings

# Las variables se cargan automáticamente
print(settings.API_KEY)
print(settings.FLASK_SECRET_KEY)
print(settings.LOG_LEVEL)
```

#### 4. **Para ejecutar en producción:**
Define variables en el servidor:
```bash
# En tu servidor de producción (Heroku, AWS, etc.):
export FLASK_ENV=production
export API_KEY=tu-clave-produccion
export FLASK_SECRET_KEY=clave-segura-produccion

# Luego ejecuta:
python src/server.py
```

---

## Configuración de desarrollo vs. producción

### 🛠️ Desarrollo Local:
```bash
# .env.local
FLASK_ENV=development
FLASK_DEBUG=True
API_TIMEOUT=10
LOG_LEVEL=DEBUG

# Las claves pueden ser de desarrollo/testing
API_KEY=sk-dev-testing-key
```

### 🚀 Producción:
```bash
# Variables del servidor (NO guardes en archivo)
FLASK_ENV=production
FLASK_DEBUG=False  # NUNCA True en producción
API_TIMEOUT=5
LOG_LEVEL=WARNING

# Claves REALES y seguras
API_KEY=sk-prod-real-key-xxxxx
FLASK_SECRET_KEY=super-secreto-generado-aleatoriamente
```

---

## Auditoría de seguridad

### ✅ Checklist de seguridad:

- [ ] No hay claves de API en archivos `.py`
- [ ] `.env` está en `.gitignore`
- [ ] `.env.example` existe como plantilla
- [ ] Se usa `python-dotenv` para cargar variables
- [ ] Variables obligatorias se validan al inicio
- [ ] Diferentes secretos para desarrollo y producción
- [ ] Claves de producción NO están en repositorio
- [ ] Archivo `.env` tiene permisos restrictivos (chmod 600)
- [ ] Se usa `FLASK_SECRET_KEY` en Flask en producción
- [ ] Se registran accesos fallidos a API (logging)

### 🔍 Verifica que tu código es seguro:
```bash
# Buscar posibles claves hardcodeadas
grep -r "api_key\|apikey\|secret\|password" src/ --ignore-case

# Buscar referencias directas en el código
grep -r "sk-" src/  # Patrón común de claves OpenAI, etc.
```

---

## Integraciones con Servicios en la Nube

### Heroku:
```bash
# Configura variables en Heroku:
heroku config:set API_KEY=tu-clave-produccion
heroku config:set FLASK_SECRET_KEY=tu-secreto-produccion

# Verifica que estén configuradas:
heroku config
```

### AWS / EC2:
```bash
# Guarda en SSM Parameter Store o Secrets Manager
# Tu aplicación lee desde allí, nunca desde archivos

# O usa IAM roles para dar permisos automáticamente
```

### Docker:
```dockerfile
# Dockerfile - NO incluyas claves
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Las claves se pasan en tiempo de ejecución:
# docker run -e API_KEY=xxxx -e FLASK_SECRET_KEY=yyyy weather-app
```

---

## 🎯 Resumen Rápido

| Aspecto | ❌ Malo | ✅ Bueno |
|--------|--------|---------|
| **Almacenamiento** | Hardcodear en código | Variables de entorno |
| **Desarrollo** | Archivo `.env` versionado | `.env` en .gitignore, `.env.example` versionado |
| **Producción** | Claves en código | Claves en variables del servidor/CI-CD |
| **Secretos compartidos** | Email, chat, git | Gestor de secretos (Vault, 1Password, etc.) |
| **Control de acceso** | Todo el equipo | Solo quien lo necesita |
| **Rotación** | Nunca | Regularmente (cada 90 días) |

---

## 📚 Recursos Adicionales

- [12-factor app - Config](https://12factor.net/config)
- [OWASP - Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [python-dotenv Documentation](https://python-dotenv.readthedocs.io/)
- [NaCl - Crypto library](https://pynacl.readthedocs.io/)

---

**Última actualización:** Abril 2026  
**Versión:** 1.0
