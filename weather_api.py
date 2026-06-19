import os
import json
import httpx

from dotenv import load_dotenv

from redis_client import r
from logger_config import logger

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_weather(city: str):

    cache_key = f"weather:{city.lower()}"

    # Check cache first
    cached_data = await r.get(cache_key)

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
        async with httpx.AsyncClient(timeout=7.0) as client:
            response = await client.get(
                BASE_URL,
                params=params
            )

        if response.status_code == 200:

            weather_data = response.json()

            result = {
                "city": weather_data["name"],
                "temperature": weather_data["main"]["temp"],
                "condition": weather_data["weather"][0]["description"]
            }

            # Cache for 5 minutes
            await r.setex(
                cache_key,
                300,
                json.dumps(result)
            )

            logger.info(f"Cached weather data for city={city}")

            return result

        if response.status_code == 404:

            logger.warning(f"City not found: {city}")

            return {
                "city": city,
                "temperature": 0,
                "condition": "City not found"
            }

        if response.status_code == 401:

            logger.error("Invalid OpenWeather API key")

            return {
                "city": city,
                "temperature": 0,
                "condition": "Invalid API key"
            }

        logger.error(
            f"OpenWeather returned status code {response.status_code}"
        )

        return {
            "city": city,
            "temperature": 0,
            "condition": f"Error {response.status_code}"
        }

    except httpx.TimeoutException:

        logger.error(f"Timeout while fetching weather for city={city}")

        return {
            "city": city,
            "temperature": 0,
            "condition": "Request timed out"
        }

    except httpx.RequestError as e:

        logger.error(f"Request failed: {e}")

        return {
            "city": city,
            "temperature": 0,
            "condition": f"Request failed: {str(e)}"
        }