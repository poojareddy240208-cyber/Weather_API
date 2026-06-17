import os
import json
import requests

from dotenv import load_dotenv
from redis_client import r
from logger_config import logger

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str):

    cache_key = f"weather:{city.lower()}"

    cached_data = r.get(cache_key)

    if cached_data:
        logger.info(f"CACHE HIT for city={city}")
        return json.loads(cached_data)

    logger.info(f"CACHE MISS for city={city}")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    logger.info(f"Fetching weather from OpenWeather for city={city}")

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=7
        )

        if response.status_code == 200:

            weather_data = response.json()

            result = {
                "city": weather_data["name"],
                "temperature": weather_data["main"]["temp"],
                "condition": weather_data["weather"][0]["description"]
            }

            r.setex(
                cache_key,
                300,
                json.dumps(result)
            )
            logger.info(f"Cached weather data for city={city}")

            return result

        elif response.status_code == 404:
            return {
                "city": city,
                "temperature": 0,
                "condition": "City not found"
            }

        elif response.status_code == 401:
            return {
                "city": city,
                "temperature": 0,
                "condition": "Invalid API key"
            }

        return {
            "city": city,
            "temperature": 0,
            "condition": f"Error {response.status_code}"
        }

    except requests.exceptions.Timeout:
        return {
            "city": city,
            "temperature": 0,
            "condition": "Request timed out"
        }

    except requests.exceptions.RequestException as e:
        return {
            "city": city,
            "temperature": 0,
            "condition": f"Request failed: {e}"
        }