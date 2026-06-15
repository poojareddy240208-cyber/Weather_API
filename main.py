import json
import time
from weather_api import get_weather

CACHE_DURATION = 7

try:
    with open("cache.json", "r") as file:
        cache = json.load(file)
except FileNotFoundError:
    cache = {}

city = input("Enter city name: ")

city_key = city.lower()

if city_key in cache:

    cached_data = cache[city_key]

    if time.time() - cached_data["timestamp"] < CACHE_DURATION:
        print("Using cached data...")
        weather = cached_data["data"]

    else:
        print("Cache expired. Fetching new data...")
        weather = get_weather(city)

        cache[city_key] = {
            "data": weather,
            "timestamp": time.time()
        }

        with open("cache.json", "w") as file:
            json.dump(cache, file)

else:
    print("Fetching from API...")

    weather = get_weather(city)

    cache[city_key] = {
        "data": weather,
        "timestamp": time.time()
    }

    with open("cache.json", "w") as file:
        json.dump(cache, file)

if "error" in weather:
    print(weather["error"])
else:
    print("\nWeather Information")
    print("City:", weather["name"])
    print("Temperature:", weather["main"]["temp"], "°C")
    print("Feels Like:", weather["main"]["feels_like"], "°C")
    print("Humidity:", weather["main"]["humidity"], "%")
    print("Pressure:", weather["main"]["pressure"], "hPa")
    print("Condition:", weather["weather"][0]["description"])
    print("Wind Speed:", weather["wind"]["speed"], "m/s")