from fastapi import FastAPI
from weather_api import get_weather

app = FastAPI()

@app.get("/weather")
def weather(city: str):

    data = get_weather(city)

    return data