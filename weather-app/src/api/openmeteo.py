"""Open-Meteo API integration"""
import requests
from datetime import datetime
from src.models.weather import WeatherData


class OpenMeteoAPI:
    """Handle requests to Open-Meteo API"""
    
    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
    
    @staticmethod
    def get_coordinates(city_name: str) -> dict:
        """Get latitude and longitude from city name"""
        try:
            params = {
                "name": city_name,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            response = requests.get(OpenMeteoAPI.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            if data.get("results"):
                result = data["results"][0]
                return {
                    "latitude": result["latitude"],
                    "longitude": result["longitude"],
                    "name": result["name"],
                    "country": result.get("country", "Unknown")
                }
            else:
                return None
        except Exception as e:
            print(f"Error fetching coordinates: {e}")
            return None
    
    @staticmethod
    def get_weather(latitude: float, longitude: float, city_name: str) -> WeatherData:
        """Fetch weather data for given coordinates"""
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                "timezone": "auto"
            }
            response = requests.get(OpenMeteoAPI.WEATHER_URL, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            current = data.get("current", {})
            
            weather_data = WeatherData(
                city=city_name,
                latitude=latitude,
                longitude=longitude,
                temperature=current.get("temperature_2m", 0),
                humidity=current.get("relative_humidity_2m", 0),
                wind_speed=current.get("wind_speed_10m", 0),
                condition=OpenMeteoAPI._get_condition(current.get("weather_code", 0)),
                timestamp=datetime.now()
            )
            
            return weather_data
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
    
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
