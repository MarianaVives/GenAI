# Weather Application 🌤️

Una aplicación Python simple para consultar datos meteorológicos usando la API Open-Meteo.

## Características

- ✅ Búsqueda de ciudades por nombre
- ✅ Temperatura actual, humedad y velocidad del viento
- ✅ Descripción de las condiciones climáticas
- ✅ Salida formateada amigable
- ✅ Manejo de errores robusto

## Estructura del Proyecto

```
weather-app/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── api/
│   │   ├── __init__.py
│   │   └── openmeteo.py        # Integración con API Open-Meteo
│   ├── utils/
│   │   ├── __init__.py
│   │   └── formatter.py        # Formateadores de salida
│   └── models/
│       ├── __init__.py
│       └── weather.py          # Modelo de datos WeatherData
├── config/
│   └── settings.py             # Configuraciones de la aplicación
├── tests/
│   └── __init__.py             # Tests unitarios
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

## Instalación

1. Clone o descargue el proyecto
2. Instale las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecute la aplicación:
```bash
python src/main.py
```

Ingrese el nombre de una ciudad cuando se le solicite:
```
Enter city name: Madrid
```

La aplicación mostrará los datos meteorológicos en un formato amigable:
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

## Configuración

Edite `config/settings.py` para personalizar:
- Formato de salida (detallado o simple)
- Timeout de API
- Nivel de registros

## API Utilizada

- **Open-Meteo**: https://open-meteo.com/
  - Geocodificación: https://geocoding-api.open-meteo.com/
  - Datos climáticos: https://api.open-meteo.com/

## Dependencias

- `requests`: Para consultas HTTP
- `pytest`: Para testing (opcional)

## Ejemplo de Código

```python
from src.api.openmeteo import OpenMeteoAPI
from src.utils.formatter import WeatherFormatter

# Obtener coordenadas
coords = OpenMeteoAPI.get_coordinates("Barcelona")

# Obtener datos meteorológicos
weather = OpenMeteoAPI.get_weather(
    coords['latitude'],
    coords['longitude'],
    coords['name']
)

# Mostrar datos formateados
print(WeatherFormatter.format_weather(weather))
```

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autor

Creado con ❤️ usando Python y la API Open-Meteo
