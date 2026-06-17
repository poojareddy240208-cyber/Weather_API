from fastapi import FastAPI
from weather_api import get_weather
from schemas import WeatherResponse

app = FastAPI()

@app.get("/weather",response_model=WeatherResponse)
def weather(city: str):

    data = get_weather(city)

    return data