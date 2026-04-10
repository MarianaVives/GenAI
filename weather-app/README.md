# Weather Application 🌤️

## Descripción del Proyecto

La Weather Application es una solución integral desarrollada en Python que permite consultar datos meteorológicos precisos y actualizados utilizando la API gratuita Open-Meteo. Diseñada para satisfacer las necesidades tanto de usuarios finales como de desarrolladores, esta aplicación ofrece una experiencia dual: una interfaz de línea de comandos (CLI) robusta y una interfaz web moderna y responsiva construida con Flask.

### Funcionalidades Clave

La aplicación destaca por su capacidad para buscar ciudades mediante geocodificación automática, proporcionando información detallada sobre temperatura actual, humedad, velocidad del viento y condiciones climáticas. Una característica innovadora es el manejo inteligente de ciudades ambiguas, como "Springfield", donde el sistema presenta opciones de selección para garantizar la precisión de los resultados.

Los usuarios pueden acceder a pronósticos extendidos de 5 días, facilitando la planificación de actividades, y comparar el clima entre múltiples ciudades simultáneamente. El sistema implementa un caché con tiempo de vida (TTL) que optimiza las consultas a la API, reduciendo tiempos de respuesta y preservando recursos.

La interfaz web, desarrollada con HTML5, CSS3 y JavaScript vanilla, ofrece un diseño responsivo que se adapta perfectamente a dispositivos móviles y de escritorio. Incluye interacciones dinámicas como dropdowns para selección de ciudades y manejo asíncrono de errores.

### Arquitectura Técnica

La arquitectura modular separa claramente las responsabilidades: el backend utiliza Python puro con bibliotecas como Requests para comunicaciones HTTP y Pytest para testing unitario con mocking. Flask sirve como framework para el servidor web, exponiendo endpoints REST para integración con otros sistemas.

La gestión de configuraciones se realiza mediante variables de entorno, asegurando seguridad y flexibilidad. El archivo .env permite configuraciones específicas por entorno (desarrollo/producción), mientras que .env.example sirve como plantilla segura para colaboradores.

### Seguridad y Testing

La seguridad es prioritaria, con claves de API y configuraciones sensibles protegidas por .gitignore. La aplicación incluye una suite completa de tests unitarios (18 tests) que cubren validación de entrada, manejo de errores, funcionamiento del caché y resolución de ambigüedades.

### Casos de Uso

Esta aplicación es perfecta para viajeros que requieren información meteorológica confiable, desarrolladores que buscan integrar servicios climáticos, o equipos que necesitan ejemplos de buenas prácticas en Python. Su naturaleza de código abierto y documentación completa la convierten en un recurso valioso para el aprendizaje y desarrollo.

En conclusión, la Weather Application combina simplicidad de uso con robustez técnica, ofreciendo una experiencia meteorológica completa y segura que se adapta a diversos contextos de uso.

**Palabras: 412** (Aproximadamente 300 palabras efectivas)

## Características

- ✅ Búsqueda de ciudades por nombre con geocodificación
- ✅ Temperatura actual, humedad, velocidad del viento y condiciones climáticas
- ✅ Pronóstico del tiempo de 5 días 📅
- ✅ Comparación de clima entre múltiples ciudades 🔄
- ✅ Manejo de ciudades ambiguas (ej. Springfield) con selección interactiva
- ✅ Caché con tiempo de vida (TTL) para optimizar consultas API
- ✅ Interfaz web responsiva con HTML/CSS/JS y backend Flask
- ✅ Manejo robusto de errores y validación de entrada
- ✅ Tests unitarios con pytest y mocking
- ✅ Salida formateada amigable en CLI

## Estructura del Proyecto

```
weather-app/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada CLI
│   ├── server.py               # Servidor Flask para UI web
│   ├── api/
│   │   ├── __init__.py
│   │   └── openmeteo.py        # Integración API Open-Meteo con caché y pronóstico
│   ├── utils/
│   │   ├── __init__.py
│   │   └── formatter.py        # Formateadores de salida
│   └── models/
│       ├── __init__.py
│       └── weather.py          # Modelo de datos WeatherData
├── web/
│   ├── index.html              # Interfaz web principal
│   ├── styles.css              # Estilos responsivos
│   └── app.js                  # Lógica frontend con fetch y manejo de errores
├── config/
│   └── settings.py             # Configuraciones (timeout, caché, etc.)
├── tests/
│   ├── __init__.py
│   └── test_api.py             # Tests unitarios
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

## Instalación

1. Clone o descargue el proyecto
2. Instale las dependencias:
```bash
pip install -r requirements.txt
```

3. Configure las variables de entorno:
```bash
# Copie el archivo de ejemplo
cp .env.example .env

# Edite .env con sus configuraciones
# (Incluye API keys, puertos, niveles de logging, etc.)
```

⚠️ **Nota importante**: El archivo `.env` contiene información sensible y no debe ser commiteado. Está protegido automáticamente por `.gitignore`.

## Uso

### Interfaz de Línea de Comandos (CLI)

Ejecute la aplicación en modo CLI:
```bash
python src/main.py
```

Ingrese el nombre de una ciudad cuando se le solicite:
```
Enter city name: Madrid
```

La aplicación mostrará los datos meteorológicos en un formato amigable. También puede:
- Comparar múltiples ciudades
- Ver pronóstico de 5 días
- Manejar ciudades ambiguas con selección

Ejemplo de salida:
```
╔════════════════════════════════════════╗
║  WEATHER REPORT FOR MADRID             ║
╠════════════════════════════════════════╣
║  Temperature:         25°C              ║
║  Humidity:            65%               ║
║  Wind Speed:           12 km/h          ║
║  Condition:        Partly cloudy       ║
║  Updated:         14:30:45             ║
╠════════════════════════════════════════╣
║  Location: (40.4168, -3.7038)          ║
╚════════════════════════════════════════╝
```

### Interfaz Web (UI)

Para acceder a la interfaz web interactiva:

1. Inicie el servidor Flask:
```bash
python src/server.py
```

2. Abra su navegador y vaya a: **http://localhost:5000**

La interfaz web permite:
- Buscar clima por ciudad
- Comparar clima entre ciudades
- Ver pronóstico de 5 días
- Seleccionar entre ciudades ambiguas mediante dropdown
- Diseño responsivo para escritorio y móvil

#### Cómo usar la UI web:
- **Búsqueda simple**: Ingrese una ciudad en el campo "City" y haga clic en "Get Weather".
- **Comparación**: Ingrese múltiples ciudades separadas por comas en "Compare Cities" y haga clic en "Compare".
- **Ciudades ambiguas**: Si hay múltiples resultados, aparecerá un dropdown para seleccionar la ciudad correcta.
- **Pronóstico**: Use el botón "Get 5-Day Forecast" para ver el pronóstico extendido.

La UI maneja errores automáticamente y muestra mensajes claros si hay problemas con la API o entradas inválidas.

## API Endpoints (para desarrollo)

El servidor Flask expone los siguientes endpoints REST:

- `GET /`: Sirve la página principal de la UI web
- `GET /api/weather?city=<city>`: Obtiene clima actual para una ciudad
- `POST /api/weather`: Obtiene clima con datos JSON (maneja ciudades ambiguas)
- `GET /api/compare?cities=<city1,city2>`: Compara clima entre ciudades
- `GET /api/forecast?city=<city>&days=5`: Obtiene pronóstico de 5 días

Ejemplo de uso con curl:
```bash
curl "http://localhost:5000/api/weather?city=Madrid"
```

## Testing

Ejecute los tests unitarios:
```bash
python -m pytest
```

Los tests cubren:
- Consultas válidas e inválidas
- Manejo de errores de API
- Caché y TTL
- Validación de entrada
- Ciudades ambiguas

## Configuración

Las configuraciones se cargan desde el archivo `.env`. Edite este archivo para personalizar:

### Variables de Entorno Disponibles:
- `API_TIMEOUT`: Timeout para consultas API (default: 5 segundos)
- `API_RETRIES`: Número de reintentos para solicitudes fallidas (default: 3)
- `CACHE_ENABLED`: Habilitar caché (default: True)
- `CACHE_DURATION`: Duración del caché en segundos (default: 600)
- `LOG_LEVEL`: Nivel de logging: DEBUG, INFO, WARNING, ERROR (default: INFO)
- `FLASK_PORT`: Puerto para el servidor Flask (default: 5000)
- `FLASK_ENV`: Entorno: development o production (default: development)
- `OUTPUT_FORMAT`: Formato de salida: detailed o simple (default: detailed)
- `API_KEY`: Clave de API para servicio externo (si se integran otros servicios)
- `FLASK_SECRET_KEY`: Clave secreta para Flask (cambiar en producción)

Ver [SECURITY.md](SECURITY.md) para más información sobre protección de claves de API.

## 🔐 Seguridad

Para información detallada sobre cómo almacenar de forma segura las claves de API, credenciales y variables sensibles, consulta la [Guía de Seguridad](SECURITY.md).

### Puntos clave:
- ✅ Las claves se almacenan en `.env` (nunca en código)
- ✅ Usa `.env.example` como plantilla para nuevos desarrolladores
- ✅ El archivo `.env` está protegido por `.gitignore`
- ✅ Crea claves seguras para producción con `secrets.token_hex(32)`
- ✅ Usa variables diferentes para desarrollo y producción

## API Utilizada

- **Open-Meteo**: https://open-meteo.com/
  - Geocodificación: https://geocoding-api.open-meteo.com/
  - Datos climáticos: https://api.open-meteo.com/

## Dependencias

- `requests`: Consultas HTTP
- `flask`: Servidor web y API REST
- `pytest`: Framework de testing
- `pytest-mock`: Mocking para tests
- `python-dotenv`: Cargador de variables de entorno

## Ejemplo de Código

```python
from src.api.openmeteo import OpenMeteoAPI

# Obtener coordenadas
coords = OpenMeteoAPI.get_coordinates("Barcelona")
print(f"Coordenadas: {coords}")

# Obtener clima actual
weather = OpenMeteoAPI.get_weather(coords['latitude'], coords['longitude'], coords['name'])
print(weather)

# Obtener pronóstico de 5 días
forecast = OpenMeteoAPI.fetch_5day_forecast(coords['latitude'], coords['longitude'])
OpenMeteoAPI.print_5day_forecast(forecast, coords['name'])
```

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autor

Creado con ❤️ usando Python, Flask y la API Open-Meteo
