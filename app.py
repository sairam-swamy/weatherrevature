from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
CORS(app)  # Enable CORS

API_KEY = "8928040ad74083e2c6a73017101a89b3"

# Prometheus Metrics
temperature_gauge = Gauge("weather_temperature", "Temperature in Celsius", ["city"])
humidity_gauge = Gauge("weather_humidity", "Humidity percentage", ["city"])
wind_speed_gauge = Gauge("weather_wind_speed", "Wind speed in m/s", ["city"])
pressure_gauge = Gauge("weather_pressure", "Atmospheric pressure in hPa", ["city"])

def get_weather_data(city):
    """Fetch weather data from OpenWeather API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to fetch weather for {city}: {response.status_code}")
        return None

@app.route("/weather", methods=["POST"])
def fetch_weather():
    """Handle weather data request from frontend."""
    data = request.json
    cities = data.get("cities", [])

    weather_data = []
    for city in cities:
        weather_info = get_weather_data(city)
        if weather_info:
            temperature = weather_info["main"]["temp"]
            humidity = weather_info["main"]["humidity"]
            wind_speed = weather_info["wind"]["speed"]
            pressure = weather_info["main"]["pressure"]
            condition = weather_info["weather"][0]["description"]

            weather_details = {
                "city": city,
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "pressure": pressure,
                "condition": condition,
            }
            weather_data.append(weather_details)

            # ✅ Ensure Prometheus metrics are updated correctly
            temperature_gauge.labels(city=city).set(temperature)
            humidity_gauge.labels(city=city).set(humidity)
            wind_speed_gauge.labels(city=city).set(wind_speed)
            pressure_gauge.labels(city=city).set(pressure)

    return jsonify(weather_data)

@app.route("/metrics")
def metrics():
    """Expose Prometheus metrics."""
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)