"""Open-Meteo API integration"""
import json
import logging
import re
import time
import requests
from datetime import datetime
from src.models.weather import WeatherData
from config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    filename=settings.LOG_FILE,
    filemode="a"
)


def is_valid_city_name(city_name: str) -> bool:
    """Validate city name input."""
    if not city_name or not city_name.strip():
        return False
    normalized = city_name.strip()
    pattern = r"^[A-Za-zÀ-ÿ\u00f1\u00d1 .'-]+$"
    return bool(re.match(pattern, normalized))


class TimedCache:
    """Simple in-memory cache with TTL (time-to-live)."""

    def __init__(self):
        self._data = {}

    def set(self, key: str, value, ttl_seconds: int):
        expires_at = time.time() + ttl_seconds
        self._data[key] = (value, expires_at)

    def get(self, key: str):
        record = self._data.get(key)
        if not record:
            return None

        value, expires_at = record
        if time.time() > expires_at:
            self._data.pop(key, None)
            return None

        return value

    def invalidate(self, key: str):
        self._data.pop(key, None)

    def clear(self):
        self._data.clear()


class WeatherCache:
    """Cross-platform cache for weather data con caducidad (default 1 hora)."""

    DEFAULT_TTL = 3600  # 1 hora

    def __init__(self):
        self._cache = TimedCache()

    def get(self, key: str):
        return self._cache.get(key)

    def set(self, key: str, value):
        self._cache.set(key, value, ttl_seconds=self.DEFAULT_TTL)

    def invalidate(self, key: str):
        self._cache.invalidate(key)

    def clear(self):
        self._cache.clear()


weather_cache = WeatherCache()


def get_weather_with_cache(key: str, fetch_fn):
    """Devuelve datos cacheados si son válidos, o obtiene los datos con fetch_fn y los guarda."""
    cached = weather_cache.get(key)
    if cached is not None:
        return cached

    data = fetch_fn()
    if data is not None:
        weather_cache.set(key, data)
    return data


def fetch_5day_forecast(latitude: float, longitude: float, timezone: str = "auto") -> dict:
    """Obtiene el pronóstico 5 días desde Open-Meteo."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
        "timezone": timezone,
        "forecast_days": 5
    }

    response = requests.get(url, params=params, timeout=settings.API_TIMEOUT)
    response.raise_for_status()
    return response.json()


def print_5day_forecast(forecast_data: dict, city_name: str = "Unknown") -> None:
    """Imprime en pantalla el pronóstico de 5 días en formato legible."""
    daily = forecast_data.get("daily", {})
    dates = daily.get("time", [])
    tmax = daily.get("temperature_2m_max", [])
    tmin = daily.get("temperature_2m_min", [])
    rain = daily.get("precipitation_sum", [])
    codes = daily.get("weathercode", [])

    print("\n" + "="*50)
    print(f"5-day forecast for {city_name}")
    print("="*50)

    for i, day in enumerate(dates):
        d = datetime.fromisoformat(day).strftime("%a %d %b %Y")
        maxv = tmax[i] if i < len(tmax) else "N/A"
        minv = tmin[i] if i < len(tmin) else "N/A"
        prcp = rain[i] if i < len(rain) else "N/A"
        code = codes[i] if i < len(codes) else None
        cond = OpenMeteoAPI._get_condition(code) if code is not None else "Unknown"

        print(f"{d:20} | Max {maxv:5}°C | Min {minv:5}°C | Rain {prcp:5}mm | {cond}")

    print("="*50)


class OpenMeteoAPI:
    """Handle requests to Open-Meteo API"""
    
    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
    _coords_cache = TimedCache()
    _weather_cache = TimedCache()
    COORDS_CACHE_TTL = 60 * 15  # 15 minutes
    WEATHER_CACHE_TTL = 60 * 60  # 1 hour
    
    @staticmethod
    def get_coordinates(city_name: str) -> dict:
        """Get latitude and longitude from city name"""
        if not is_valid_city_name(city_name):
            print("Error: invalid city name provided")
            return None

        cache_key = f"coords:{city_name.strip().lower()}"
        cached_coords = OpenMeteoAPI._coords_cache.get(cache_key)
        if cached_coords is not None:
            return cached_coords

        try:
            params = {
                "name": city_name.strip(),
                "count": 10,
                "language": "en",
                "format": "json"
            }
            response = requests.get(OpenMeteoAPI.BASE_URL, params=params, timeout=settings.API_TIMEOUT)
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            if not results:
                return None

            choices = []
            for result in results:
                choices.append({
                    "latitude": result["latitude"],
                    "longitude": result["longitude"],
                    "name": result["name"],
                    "country": result.get("country", "Unknown")
                })

            if len(choices) == 1:
                OpenMeteoAPI._coords_cache.set(cache_key, choices[0], OpenMeteoAPI.COORDS_CACHE_TTL)
                return choices[0]

            ambiguous_result = {
                "ambiguous": True,
                "choices": choices
            }
            OpenMeteoAPI._coords_cache.set(cache_key, ambiguous_result, OpenMeteoAPI.COORDS_CACHE_TTL)
            return ambiguous_result
        except Exception as e:
            logger.exception(f"Error fetching coordinates: {e}")
            return None
    
    @staticmethod
    def _weather_params(latitude: float, longitude: float) -> dict:
        return {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto"
        }

    @staticmethod
    def _to_weather_data(current: dict, latitude: float, longitude: float, city_name: str) -> WeatherData:
        temperature = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        wind_speed = current.get("wind_speed_10m")
        weather_code = current.get("weather_code")

        if temperature is None or humidity is None or wind_speed is None or weather_code is None:
            logger.warning("Incomplete weather data received from API")
            return None

        return WeatherData(
            city=city_name,
            latitude=latitude,
            longitude=longitude,
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
            condition=OpenMeteoAPI._get_condition(weather_code),
            timestamp=datetime.now()
        )

    @staticmethod
    def get_weather(latitude: float, longitude: float, city_name: str):
        """Fetch weather data for given coordinates.

        Parameters
        ----------
        latitude : float
            Latitude of the desired location (e.g. 40.4168).
        longitude : float
            Longitude of the desired location (e.g. -3.7038).
        city_name : str
            User-friendly city name to include in response model.

        Returns
        -------
        WeatherData | None
            WeatherData instance when successful, otherwise None on error.

        Notes
        -----
        - Se comunica con Open-Meteo a través de `OpenMeteoAPI.WEATHER_URL`.
        - Usa `settings.API_TIMEOUT` para timeout.
        - Verifica que exista el campo "current" y que contenga valores clave.
        - Maneja los errores: timeout, connection error, HTTP 4xx/5xx, JSON inválido.

        Example
        -------
        >>> weather = OpenMeteoAPI.get_weather(40.4168, -3.7038, "Madrid")
        >>> if weather:
        ...     print(weather.temperature, weather.condition)
        ... else:
        ...     print("No weather data available")
        """
        params = OpenMeteoAPI._weather_params(latitude, longitude)

        try:
            response = requests.get(OpenMeteoAPI.WEATHER_URL, params=params, timeout=settings.API_TIMEOUT)
            response.raise_for_status()
            payload = response.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.warning(f"Weather request failed: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"Weather HTTP error: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Weather response invalid JSON: {e}")
            return None
        except Exception as e:
            logger.exception(f"Unexpected error getting weather: {e}")
            return None

        cache_key = f"weather:{latitude}:{longitude}:{city_name.strip().lower()}"
        cached_weather = OpenMeteoAPI._weather_cache.get(cache_key)
        if cached_weather is not None:
            return cached_weather

        current = payload.get("current")
        if not isinstance(current, dict):
            logger.error("Weather response missing current field")
            return None

        weather_data = OpenMeteoAPI._to_weather_data(current, latitude, longitude, city_name)
        if weather_data is None:
            logger.warning("Weather data conversion returned None")
            return None

        OpenMeteoAPI._weather_cache.set(cache_key, weather_data, OpenMeteoAPI.WEATHER_CACHE_TTL)
        return weather_data
    
    @staticmethod
    def _get_condition(weather_code: int) -> str:
        """Convert WMO weather code to readable description"""
        conditions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with hail"
        }
        return conditions.get(weather_code, "Unknown")
