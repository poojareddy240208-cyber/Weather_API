# Weather API

A production-ready Weather API built with FastAPI, Redis caching, rate limiting, Docker, and Render deployment.

## Live Demo

API Base URL:

https://weather-api-eiee.onrender.com

https://weather-api-eiee.onrender.com/docs

Interactive API Documentation:

https://weather-api-eiee.onrender.com/docs

---

## Features

* Fetch real-time weather data using OpenWeather API
* Redis caching for improved performance
* Rate limiting (5 requests per minute per IP)
* Async FastAPI architecture
* Dockerized application
* Structured logging
* Health check endpoint
* Cache management endpoints
* Render cloud deployment

---

## Tech Stack

* FastAPI
* Redis / Render Key Value
* FastAPI Limiter
* Docker
* OpenWeather API
* Render
* Python 3.12

---

## Project Architecture

Client
│
▼
FastAPI
│
├── Redis Cache
│
└── OpenWeather API

---

## API Endpoints

### Health Check
https://weather-api-eiee.onrender.com/health

GET /health

Response:

{
"status": "healthy"
}

---

### Get Weather
https://weather-api-eiee.onrender.com/weather?city=hyderabad

GET /weather?city=hyderabad

Example Response:

{
"city": "Hyderabad",
"temperature": 31.2,
"condition": "clear sky"
}

---

### View Cached Keys
https://weather-api-eiee.onrender.com/cache

GET /cache

---

### Delete Cache For One City
https://weather-api-eiee.onrender.com/cache/hyderabad

DELETE 

DELETE /cache/{city}

Example:

DELETE /cache/hyderabad

---

### Clear Entire Cache
https://weather-api-eiee.onrender.com/cache

DELETE 

DELETE /cache

---

## Rate Limiting

The weather endpoint is limited to:

5 requests per minute per IP address

Exceeding the limit returns HTTP 429.

---

## Environment Variables

Create a .env file:

OPENWEATHER_API_KEY=your_api_key
REDIS_URL=redis://localhost:6379

---

## Local Setup

Clone the repository:

git clone https://github.com/poojareddy240208-cyber/Weather_API.git

cd Weather_API

Create a virtual environment:

python -m venv .venv

Activate it:

Windows:
.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run Redis:

redis-server

Start FastAPI:

uvicorn main:app --reload

---

## Docker

Build image:

docker build -t weather-api .

Run container:

docker run -p 8000:8000 weather-api

---

## Deployment

The application is deployed on Render using:

* Docker Web Service
* Render Key Value (Redis-compatible)
* GitHub Auto Deploy

---

## Future Improvements

* JWT Authentication
* PostgreSQL Integration
* User Accounts
* Weather Forecast Endpoint
* API Analytics Dashboard
* CI/CD Pipeline with GitHub Actions

---

## Author

Pooja Reddy
