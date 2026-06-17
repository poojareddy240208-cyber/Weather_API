from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from redis.asyncio import Redis

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from weather_api import get_weather
from schemas import WeatherResponse
from redis_client import r
from logger_config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):

    redis = Redis(
        host="localhost",
        port=6379,
        db=0
    )

    await FastAPILimiter.init(redis)

    yield

    await redis.close()


app = FastAPI(
    title="Weather API",
    description="Weather API with Redis caching and rate limiting",
    version="1.0.0",
    lifespan=lifespan
)


@app.get(
    "/weather",
    response_model=WeatherResponse,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))]
)
def weather(city: str):
    return get_weather(city)


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/cache")
def view_cache_keys():

    keys = r.keys("weather:*")

    return {
        "keys": [
            key.decode() if isinstance(key, bytes) else key
            for key in keys
        ]
    }


@app.delete("/cache/{city}")
def clear_city_cache(city: str):

    cache_key = f"weather:{city.lower()}"

    deleted = r.delete(cache_key)

    logger.info(f"Cache deleted for city={city}")

    return {
        "city": city,
        "deleted": bool(deleted)
    }


@app.delete("/cache")
def clear_all_cache():

    r.flushdb()

    logger.warning("Entire Redis cache flushed")

    return {
        "message": "All cache cleared successfully"
    }