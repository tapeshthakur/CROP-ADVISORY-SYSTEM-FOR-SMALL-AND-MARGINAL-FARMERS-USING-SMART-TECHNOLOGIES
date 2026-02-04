import os
import random
import requests


DEFAULT_WEATHER = {
    "temperature": 28.0,
    "rainfall": 110.0,
    "humidity": 72.0,
}


def get_weather(location: str):
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return _mock_weather()

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": location, "appid": api_key, "units": "metric"},
            timeout=8,
        )
        response.raise_for_status()
        data = response.json()
        rainfall = data.get("rain", {}).get("1h", random.uniform(0, 200))
        return {
            "temperature": data["main"]["temp"],
            "rainfall": rainfall,
            "humidity": data["main"]["humidity"],
        }
    except (requests.RequestException, KeyError, ValueError):
        return _mock_weather()


def _mock_weather():
    return {
        "temperature": round(random.uniform(22, 34), 1),
        "rainfall": round(random.uniform(40, 200), 1),
        "humidity": round(random.uniform(55, 90), 1),
    }
