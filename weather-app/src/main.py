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


def compare_multiple_cities(cities):
    """Muestra el clima actual comparativo para varias ciudades."""
    rows = []

    for city in cities:
        city = city.strip()
        if not city:
            continue

        coords = OpenMeteoAPI.get_coordinates(city)
        if coords is None:
            rows.append({
                "city": city,
                "status": "Not found",
                "temp": "-",
                "humidity": "-",
                "wind": "-",
                "condition": "-"
            })
            continue

        if coords.get("ambiguous"):
            # prefer first autocasiado para ejecución batch
            candidate = coords.get("choices", [None])[0]
            if not candidate:
                rows.append({
                    "city": city,
                    "status": "Ambiguous, no choice",
                    "temp": "-",
                    "humidity": "-",
                    "wind": "-",
                    "condition": "-"
                })
                continue
            coords = candidate

        weather = OpenMeteoAPI.get_weather(coords["latitude"], coords["longitude"], coords["name"])
        if weather is None:
            rows.append({
                "city": coords.get("name", city),
                "status": "API error",
                "temp": "-",
                "humidity": "-",
                "wind": "-",
                "condition": "-"
            })
            continue

        rows.append({
            "city": weather.city,
            "status": "OK",
            "temp": f"{weather.temperature}°C",
            "humidity": f"{weather.humidity}%",
            "wind": f"{weather.wind_speed} km/h",
            "condition": weather.condition
        })

    print("\n" + "="*90)
    print(f"{'City':20} | {'Status':12} | {'Temp':8} | {'Humidity':10} | {'Wind':10} | Condition")
    print("-"*90)
    for r in rows:
        print(f"{r['city']:20} | {r['status']:12} | {r['temp']:8} | {r['humidity']:10} | {r['wind']:10} | {r['condition']}")
    print("="*90)


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

            # Optional: 5-day forecast
            forecast_answer = input("\nWould you like a 5-day forecast? (y/n): ").strip().lower()
            if forecast_answer == 'y':
                try:
                    from src.api.openmeteo import fetch_5day_forecast, print_5day_forecast
                    forecast_data = fetch_5day_forecast(coords['latitude'], coords['longitude'])
                    print_5day_forecast(forecast_data, coords['name'])
                except Exception as e:
                    print(f"Error fetching 5-day forecast: {e}")

            multi_answer = input("\nWould you like to compare multiple cities? (y/n): ").strip().lower()
            if multi_answer == 'y':
                cities_input = input("Enter city names separated by commas: ")
                cities = [c.strip() for c in cities_input.split(",") if c.strip()]
                if cities:
                    compare_multiple_cities(cities)

        else:
            print("Error: Unable to fetch weather data")
    
    except KeyboardInterrupt:
        print("\n\nApplication cancelled by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
