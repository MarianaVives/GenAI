"""Unit tests for weather application"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.api.openmeteo import OpenMeteoAPI
from src.models.weather import WeatherData
from src.utils.formatter import WeatherFormatter
from datetime import datetime


class TestOpenMeteoAPI:
    """Tests for OpenMeteoAPI"""
    
    def test_get_coordinates_valid_city(self):
        """Test getting coordinates for a valid city"""
        coords = OpenMeteoAPI.get_coordinates("Paris")
        assert coords is not None
        assert 'latitude' in coords
        assert 'longitude' in coords
        assert 'name' in coords
    
    def test_get_coordinates_invalid_city(self):
        """Test getting coordinates for an invalid city"""
        coords = OpenMeteoAPI.get_coordinates("xyzabc12345invalid")
        assert coords is None
    
    def test_weather_code_conversion(self):
        """Test weather code to description conversion"""
        assert OpenMeteoAPI._get_condition(0) == "Clear sky"
        assert OpenMeteoAPI._get_condition(3) == "Overcast"
        assert OpenMeteoAPI._get_condition(61) == "Slight rain"


class TestWeatherFormatter:
    """Tests for WeatherFormatter"""
    
    @staticmethod
    def create_test_weather():
        """Helper to create test weather data"""
        return WeatherData(
            city="Test City",
            latitude=0.0,
            longitude=0.0,
            temperature=20.5,
            humidity=65,
            wind_speed=10.5,
            condition="Partly cloudy",
            timestamp=datetime.now()
        )
    
    def test_format_weather(self):
        """Test weather formatting"""
        weather = self.create_test_weather()
        formatted = WeatherFormatter.format_weather(weather)
        assert "Test City" in formatted
        assert "20.5" in formatted
        assert "65" in formatted
    
    def test_format_simple(self):
        """Test simple weather formatting"""
        weather = self.create_test_weather()
        formatted = WeatherFormatter.format_simple(weather)
        assert "Test City" in formatted
        assert "20.5°C" in formatted


class TestWeatherData:
    """Tests for WeatherData model"""
    
    def test_weather_data_creation(self):
        """Test creating WeatherData instance"""
        weather = WeatherData(
            city="Madrid",
            latitude=40.4168,
            longitude=-3.7038,
            temperature=25.0,
            humidity=60,
            wind_speed=15.0,
            condition="Clear sky",
            timestamp=datetime.now()
        )
        assert weather.city == "Madrid"
        assert weather.temperature == 25.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
