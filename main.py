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
        db=0,
        decode_responses=True
    )

    await FastAPILimiter.init(redis)

    logger.info("FastAPI Limiter initialized")

    yield

    await redis.aclose()

    logger.info("Redis connection closed")


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
async def weather(city: str):
    """
    Get weather data for a city.
    Limited to 5 requests per minute per IP.
    """
    return await get_weather(city)


@app.get("/health")
async def health():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy"
    }


@app.get("/cache")
async def view_cache_keys():
    """
    View all cached weather keys.
    """

    keys = await r.keys("weather:*")

    return {
        "keys": keys
    }


@app.delete("/cache/{city}")
async def clear_city_cache(city: str):
    """
    Delete cache for a specific city.
    """

    cache_key = f"weather:{city.lower()}"

    deleted = await r.delete(cache_key)

    logger.info(f"Cache deleted for city={city}")

    return {
        "city": city,
        "deleted": bool(deleted)
    }


@app.delete("/cache")
async def clear_all_cache():
    """
    Flush entire Redis database.
    """

    await r.flushdb()

    logger.warning("Entire Redis cache flushed")

    return {
        "message": "All cache cleared successfully"
    }