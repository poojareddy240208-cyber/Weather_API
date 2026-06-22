# Weather API 🚀

A production-style Weather API built with FastAPI that fetches real-time weather data from OpenWeatherMap, caches responses using Redis, and protects endpoints with rate limiting.

## Features

- FastAPI-based REST API
- Real-time weather data from OpenWeatherMap
- Redis caching for improved performance
- Redis-backed rate limiting
- Dockerized deployment
- Docker Compose setup
- Health check endpoint
- Logging support
- Interactive Swagger API documentation

---

## Tech Stack

- Python 3.12
- FastAPI
- Redis
- FastAPI Limiter
- HTTPX
- Docker
- Docker Compose
- OpenWeatherMap API

---

## Project Structure

```text
Weather_API/
│
├── main.py                 # FastAPI application
├── weather_api.py          # Weather service logic
├── redis_client.py         # Redis connection
├── schemas.py              # Response schemas
├── logger_config.py        # Logging configuration
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
│
└── README.md
```

---

## API Endpoints

### Get Weather

```http
GET /weather?city={city_name}
```

Example:

```http
GET /weather?city=Hyderabad
```

Response:

```json
{
  "city": "Hyderabad",
  "temperature": 31.2,
  "condition": "clear sky"
}
```

---

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

---

### View Cached Keys

```http
GET /cache
```

---

### Delete Cache For City

```http
DELETE /cache/{city}
```

Example:

```http
DELETE /cache/Hyderabad
```

---

### Clear Entire Cache

```http
DELETE /cache
```

---

## Redis Caching

The application caches weather responses for 5 minutes.

### Cache Flow

```text
Client Request
      │
      ▼
Check Redis Cache
      │
 ┌────┴────┐
 │         │
Hit       Miss
 │         │
 ▼         ▼
Return   OpenWeather API
Cached      │
Data        ▼
         Store in Redis
              │
              ▼
         Return Response
```

Benefits:

- Faster responses
- Reduced API calls
- Better scalability

---

## Rate Limiting

The weather endpoint is protected using Redis-backed rate limiting.

Current configuration:

```text
5 requests per minute per IP
```

Exceeding the limit returns:

```http
429 Too Many Requests
```

---

## Local Setup

### Clone Repository

```bash
git clone <your-repository-url>
cd Weather_API
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create .env

```env
OPENWEATHER_API_KEY=your_api_key_here
```

### Run Application

```bash
uvicorn main:app --reload
```

Visit:

```text
http://localhost:8000/docs
```

---

## Docker Setup

### Build Containers

```bash
docker compose build
```

### Start Services

```bash
docker compose up
```

### Stop Services

```bash
docker compose down
```

---

## Swagger Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

## Logging

The application logs:

- Cache hits
- Cache misses
- API requests
- Errors
- Redis events

Example:

```text
INFO - CACHE MISS for city=Hyderabad
INFO - Cached weather data for city=Hyderabad
INFO - CACHE HIT for city=Hyderabad
```

---

## Future Improvements

- JWT Authentication
- Role-Based Authorization
- User Accounts
- Request Analytics
- Automated Testing (Pytest)
- CI/CD Pipeline
- Cloud Deployment
- Monitoring & Metrics

---

## Learning Outcomes

This project demonstrates:

- REST API development
- FastAPI fundamentals
- Asynchronous programming
- Redis caching
- Rate limiting
- Docker containerization
- API integration
- Environment variable management
- Backend system design

---

## Author

**Pooja Reddy**

Backend Development Project built using FastAPI, Redis, and Docker.
