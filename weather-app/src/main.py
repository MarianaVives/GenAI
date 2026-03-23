"""Main application entry point"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.openmeteo import OpenMeteoAPI
from src.utils.formatter import WeatherFormatter
from config.settings import OUTPUT_FORMAT


def main():
    """Main application function"""
    print("\n" + "="*40)
    print("   WEATHER APPLICATION")
    print("="*40)
    
    try:
        # Get city input from user
        city = input("\nEnter city name: ").strip()
        
        if not city:
            print("Error: City name cannot be empty")
            return
        
        print(f"\nFetching weather data for {city}...")
        
        # Get coordinates
        coords = OpenMeteoAPI.get_coordinates(city)
        
        if coords is None:
            print(f"Error: City '{city}' not found")
            return
        
        print(f"Found: {coords['name']}, {coords['country']}")
        
        # Get weather data
        weather = OpenMeteoAPI.get_weather(
            coords['latitude'],
            coords['longitude'],
            coords['name']
        )
        
        # Display formatted weather
        if weather:
            if OUTPUT_FORMAT == 'simple':
                print(WeatherFormatter.format_simple(weather))
            else:
                print(WeatherFormatter.format_weather(weather))
        else:
            print("Error: Unable to fetch weather data")
    
    except KeyboardInterrupt:
        print("\n\nApplication cancelled by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
