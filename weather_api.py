import os

import requests
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params={
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response=requests.get(BASE_URL, params=params, timeout=7)
        if response.status_code == 200:
            return response.json()

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
