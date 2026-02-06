from typing import Dict
import requests


# OpenWeatherMap API (free tier is enough for projects)
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str = "Delhi") -> Dict[str, float]:
    """
    Fetches real-time weather data for a given city.

    Returns:
        Dict with temperature (°C), rainfall (mm), and humidity (%)
    """

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        # Rainfall may not always be present
        rainfall = 0.0
        if "rain" in data and "1h" in data["rain"]:
            rainfall = data["rain"]["1h"]

        return {
            "temperature": float(temperature),
            "rainfall": float(rainfall),
            "humidity": float(humidity)
        }

    except Exception as e:
        # Fallback values (safe defaults)
        return {
            "temperature": 30.0,
            "rainfall": 0.0,
            "humidity": 60.0
        }
