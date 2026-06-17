import os
import json
from redis_client import r

import requests
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    cache_key = f"weather:{city.lower()}"

    cached_data = r.get(cache_key)

    if cached_data:
        print("CACHE HIT")
        return json.loads(cached_data)

    print("CACHE MISS")

    params={
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response=requests.get(BASE_URL, params=params, timeout=7)
        if response.status_code == 200:

            weather_data = response.json()

            r.setex(
                cache_key,
                300,
                json.dumps(weather_data)
            )

            return weather_data

        elif response.status_code == 404:
            return {"error": "City not found"}

        elif response.status_code == 401:
            return {"error": "Invalid API key"}

    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            return {"error": "City not found"}
        return {"error": f"HTTP error: {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
