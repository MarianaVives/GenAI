"""Output formatting utilities"""
from src.models.weather import WeatherData


class WeatherFormatter:
    """Format weather data for display"""
    
    @staticmethod
    def format_weather(weather_data: WeatherData) -> str:
        """Format weather data into a readable string"""
        if weather_data is None:
            return "Unable to fetch weather data"
        
        output = f"""
╔════════════════════════════════════════╗
║  WEATHER REPORT FOR {weather_data.city.upper():^30} ║
╠════════════════════════════════════════╣
║  Temperature:      {weather_data.temperature:>5}°C             ║
║  Humidity:         {weather_data.humidity:>5}%              ║
║  Wind Speed:       {weather_data.wind_speed:>5} km/h           ║
║  Condition:        {weather_data.condition:<22} ║
║  Updated:         {weather_data.timestamp.strftime('%H:%M:%S'):<15} ║
╠════════════════════════════════════════╣
║  Location: ({weather_data.latitude}, {weather_data.longitude}) ║
╚════════════════════════════════════════╝
"""
        return output
    
    @staticmethod
    def format_simple(weather_data: WeatherData) -> str:
        """Format weather data in a simple format"""
        if weather_data is None:
            return "Unable to fetch weather data"
        
        return (
            f"{weather_data.city}: {weather_data.temperature}°C, "
            f"{weather_data.condition}, Humidity: {weather_data.humidity}%"
        )
