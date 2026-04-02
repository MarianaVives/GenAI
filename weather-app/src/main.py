"""Main application entry point"""
import re
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.openmeteo import OpenMeteoAPI
from src.utils.formatter import WeatherFormatter
from config.settings import OUTPUT_FORMAT


def is_valid_city_name(city_name: str) -> bool:
    if not city_name or not city_name.strip():
        return False
    pattern = r"^[A-Za-zÀ-ÿ\u00f1\u00d1 .'-]+$"
    return bool(re.match(pattern, city_name.strip()))


def main():
    """Main application function"""
    print("\n" + "="*40)
    print("   WEATHER APPLICATION")
    print("="*40)
    
    try:
        # Get city input from user
        city_input = input("\nEnter city name: ")
        city = city_input.strip()

        if not is_valid_city_name(city):
            print("Error: City name cannot be empty or contener caracteres inválidos")
            return
        
        print(f"\nFetching weather data for {city}...")
        
        # Get coordinates
        coords = OpenMeteoAPI.get_coordinates(city)
        
        if coords is None:
            print(f"Error: City '{city}' not found")
            return

        if coords.get("ambiguous"):
            print("Multiple results found for city. Please select one:")
            for idx, c in enumerate(coords["choices"], start=1):
                print(f"  {idx}. {c['name']}, {c['country']} ({c['latitude']}, {c['longitude']})")

            choice = input("Select option number: ").strip()
            if not choice.isdigit() or not (1 <= int(choice) <= len(coords["choices"])):
                print("Error: option inválida")
                return

            coords = coords["choices"][int(choice) - 1]

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
