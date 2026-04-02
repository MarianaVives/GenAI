import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, request, jsonify, send_from_directory
from src.api.openmeteo import OpenMeteoAPI

app = Flask(__name__, static_folder="../web", static_url_path="/static")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/styles.css")
def styles():
    return send_from_directory(app.static_folder, "styles.css")

@app.route("/app.js")
def appjs():
    return send_from_directory(app.static_folder, "app.js")

@app.route("/static/<path:filename>")
def static_asset(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/api/weather")
def api_weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "city parameter is required"}), 400

    coords = OpenMeteoAPI.get_coordinates(city)
    if not coords:
        return jsonify({"error": "city not found"}), 404

    if coords.get("ambiguous"):
        return jsonify({
            "status": "ambiguous",
            "choices": coords.get("choices", []),
        })

    weather = OpenMeteoAPI.get_weather(coords["latitude"], coords["longitude"], coords["name"])
    if weather is None:
        return jsonify({"error": "no weather data"}), 500

    return jsonify({
        "city": weather.city,
        "temperature": weather.temperature,
        "humidity": weather.humidity,
        "wind_speed": weather.wind_speed,
        "condition": weather.condition,
    })

@app.route("/api/weather-by-coords")
def api_weather_by_coords():
    lat = request.args.get("latitude")
    lon = request.args.get("longitude")
    city = request.args.get("city", "Unknown")

    if not lat or not lon:
        return jsonify({"error": "latitude and longitude are required"}), 400

    try:
        latitude = float(lat)
        longitude = float(lon)
    except ValueError:
        return jsonify({"error": "invalid latitude/longitude"}), 400

    weather = OpenMeteoAPI.get_weather(latitude, longitude, city)
    if weather is None:
        return jsonify({"error": "no weather data"}), 500

    return jsonify({
        "status": "ok",
        "city": weather.city,
        "temperature": weather.temperature,
        "humidity": weather.humidity,
        "wind_speed": weather.wind_speed,
        "condition": weather.condition,
    })


@app.route("/api/compare", methods=["POST"])
def api_compare():
    payload = request.get_json(force=True, silent=True) or {}
    cities = payload.get("cities", [])

    if not isinstance(cities, list) or not cities:
        return jsonify({"error": "cities field is required"}), 400

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
                "condition": "-",
            })
            continue

        if coords.get("ambiguous"):
            coords = coords.get("choices", [None])[0]
            if coords is None:
                rows.append({
                    "city": city,
                    "status": "Ambiguous",
                    "temp": "-",
                    "humidity": "-",
                    "wind": "-",
                    "condition": "-",
                })
                continue

        weather = OpenMeteoAPI.get_weather(coords["latitude"], coords["longitude"], coords["name"])
        if weather is None:
            rows.append({
                "city": coords.get("name", city),
                "status": "API error",
                "temp": "-",
                "humidity": "-",
                "wind": "-",
                "condition": "-",
            })
            continue

        rows.append({
            "city": weather.city,
            "status": "OK",
            "temp": f"{weather.temperature}°C",
            "humidity": f"{weather.humidity}%",
            "wind": f"{weather.wind_speed} km/h",
            "condition": weather.condition,
        })

    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
