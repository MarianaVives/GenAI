"""Weather data model"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherData:
    """Data class for weather information"""
    city: str
    latitude: float
    longitude: float
    temperature: float
    humidity: int
    wind_speed: float
    condition: str
    timestamp: datetime

    def __repr__(self):
        return (
            f"WeatherData(city={self.city}, temp={self.temperature}°C, "
            f"humidity={self.humidity}%, wind={self.wind_speed} km/h)"
        )
