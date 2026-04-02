"""Unit tests for weather application"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import requests
from src.api.openmeteo import OpenMeteoAPI
from src.models.weather import WeatherData
from src.utils.formatter import WeatherFormatter
from datetime import datetime


class TestOpenMeteoAPI:
    """Tests for OpenMeteoAPI"""
    
    class MockResponse:
        def __init__(self, data, status=200):
            self._data = data
            self.status_code = status

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.exceptions.HTTPError(f"{self.status_code} Error")

        def json(self):
            return self._data

    def test_get_coordinates_valid_city(self, monkeypatch):
        """Test getting coordinates for a valid city"""
        def fake_get(url, params=None, timeout=None):
            if url == OpenMeteoAPI.BASE_URL:
                return TestOpenMeteoAPI.MockResponse({
                    "results": [{
                        "latitude": 48.8566,
                        "longitude": 2.3522,
                        "name": "Paris",
                        "country": "France"
                    }]
                })
            raise AssertionError("Unexpected URL")

        monkeypatch.setattr("src.api.openmeteo.requests.get", fake_get)

        coords = OpenMeteoAPI.get_coordinates("Paris")
        assert coords is not None
        assert coords["name"] == "Paris"
        assert coords["country"] == "France"

    def test_get_weather_valid_city(self, monkeypatch):
        """Test the full coordinates + weather flow for a valid city"""
        def fake_get(url, params=None, timeout=None):
            if url == OpenMeteoAPI.BASE_URL:
                return TestOpenMeteoAPI.MockResponse({
                    "results": [{
                        "latitude": 48.8566,
                        "longitude": 2.3522,
                        "name": "Paris",
                        "country": "France"
                    }]
                })
            if url == OpenMeteoAPI.WEATHER_URL:
                return TestOpenMeteoAPI.MockResponse({
                    "current": {
                        "temperature_2m": 18.3,
                        "relative_humidity_2m": 73,
                        "weather_code": 1,
                        "wind_speed_10m": 3.4
                    }
                })
            raise AssertionError("Unexpected URL")

        monkeypatch.setattr("src.api.openmeteo.requests.get", fake_get)

        coords = OpenMeteoAPI.get_coordinates("Paris")
        weather = OpenMeteoAPI.get_weather(coords["latitude"], coords["longitude"], coords["name"])

        assert weather is not None
        assert weather.city == "Paris"
        assert weather.temperature == 18.3
        assert weather.condition == "Mainly clear"

    def test_get_coordinates_invalid_city(self, monkeypatch):
        """Test getting coordinates for an invalid city"""
        def fake_get(url, params=None, timeout=None):
            return TestOpenMeteoAPI.MockResponse({"results": []})

        monkeypatch.setattr("src.api.openmeteo.requests.get", fake_get)

        coords = OpenMeteoAPI.get_coordinates("xyzabc12345invalid")
        assert coords is None

    def test_get_coordinates_reject_invalid_string(self):
        """Invalid city name should be rejected before API call"""
        coords = OpenMeteoAPI.get_coordinates("<script>")
        assert coords is None

    def test_get_coordinates_timeout(self, monkeypatch):
        """Test timeout handling in coordinate lookup"""
        def fake_get(url, params=None, timeout=None):
            raise requests.exceptions.Timeout("Connection timed out")

        monkeypatch.setattr("src.api.openmeteo.requests.get", fake_get)
        coords = OpenMeteoAPI.get_coordinates("Paris")
        assert coords is None

    def test_get_weather_server_error(self, monkeypatch):
        """Test server error handling in weather fetch"""
        def fake_get(url, params=None, timeout=None):
            if url == OpenMeteoAPI.BASE_URL:
                return TestOpenMeteoAPI.MockResponse({
                    "results": [{
                        "latitude": 48.8566,
                        "longitude": 2.3522,
                        "name": "Paris",
                        "country": "France"
                    }]
                })
            if url == OpenMeteoAPI.WEATHER_URL:
                return TestOpenMeteoAPI.MockResponse({"detail": "Server error"}, status=500)
            raise AssertionError("Unexpected URL")

        monkeypatch.setattr("src.api.openmeteo.requests.get", fake_get)

        coords = OpenMeteoAPI.get_coordinates("Paris")
        assert coords is not None
        weather = OpenMeteoAPI.get_weather(coords["latitude"], coords["longitude"], coords["name"])
        assert weather is None


from src.main import main as app_main


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
        assert "TEST CITY" in formatted
        assert "20.5" in formatted
        assert "65" in formatted
    
    def test_format_simple(self):
        """Test simple weather formatting"""
        weather = self.create_test_weather()
        formatted = WeatherFormatter.format_simple(weather)
        assert "Test City" in formatted
        assert "20.5°C" in formatted

    def test_main_empty_city(self, monkeypatch, capsys):
        """Test main() with empty city input"""
        monkeypatch.setattr("builtins.input", lambda prompt="": "   ")
        app_main()
        captured = capsys.readouterr()
        assert "Error: City name cannot be empty" in captured.out


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
