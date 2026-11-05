# Weather API

A production-ready Weather API built with FastAPI, Redis caching, rate limiting, Docker, Kubernetes (Minikube), and Render cloud deployment.

## Live Production Demo

- **API Base URL:** https://weather-api-eiee.onrender.com
- **Interactive API Documentation (Swagger):** https://weather-api-eiee.onrender.com/docs
- **Health Check Endpoint:** https://weather-api-eiee.onrender.com/health

---

## Features

- **Real-time Weather Data:** Integrated with OpenWeatherMap API.
- **Redis Caching:** Accelerates response times and minimizes external API calls.
- **Rate Limiting:** IP-based rate limiting (5 requests per minute) to prevent abuse.
- **Async Architecture:** High-throughput backend powered by FastAPI and Uvicorn.
- **Containerization & Orchestration:** Fully dockerized with multi-replica local Kubernetes deployment.
- **Self-Healing Infrastructure:** Kubernetes deployments configure liveness/readiness management, desired-state reconciliation, and secret management.
- **Structured Logging:** Centralized application logging for monitoring and debugging.

---

## Tech Stack

- **Backend:** Python 3.12, FastAPI, Uvicorn, Pydantic
- **Caching & Storage:** Redis (Render Key-Value in cloud, Redis 7 Alpine in local k8s)
- **Rate Limiting:** FastAPI Limiter
- **Containerization & Orchestration:** Docker, Docker Compose, Kubernetes (Minikube), `kubectl`
- **Cloud & Deployment:** Render (PaaS Web Service)
- **External Services:** OpenWeatherMap API

---

## Architecture Overview

The system supports two independent deployment strategies:

### 1. Cloud Production Architecture (Render)
```
Client  ──►  Render Web Service (FastAPI Docker Container)  ──►  Render Key-Value (Redis)
                                        │
                                        ▼
                               OpenWeatherMap API
```

### 2. Local Kubernetes Architecture (Minikube)
```
                                ┌────────────────────────────────────────────────────────┐
                                │ Kubernetes Cluster (weather-local namespace)           │
                                │                                                        │
Client ──► ClusterIP Service ──►│   ├── FastAPI Pod 1 ──┐                                │
          (Port 8000/8001)      │   ├── FastAPI Pod 2   ├──► Redis Service ──► Redis Pod │
                                │   └── FastAPI Pod N ──┘     (Port 6379)                │
                                └────────────────────────────────────────────────────────┘
```

---

## API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Application health check endpoint |
| `GET` | `/weather?city={name}` | Retrieves live weather data for a city (cached & rate-limited) |
| `GET` | `/cache` | Lists all active Redis cached keys |
| `DELETE` | `/cache/{city}` | Purges cache entry for a specific city |
| `DELETE` | `/cache` | Clears all cached weather data |

---

## Local Development & Docker Setup

### Prerequisites
- Python 3.12+
- Docker Engine & Docker Desktop

### 1. Standard Python Virtual Environment
```bash
# Clone the repository
git clone https://github.com/poojareddy240208-cyber/Weather_API.git
cd Weather_API

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application locally
uvicorn main:app --reload
```

### 2. Docker Compose Setup
```bash
# Start both FastAPI and Redis containers locally
docker compose up --build
```

---

## Local Kubernetes (Minikube) Deployment

The project includes declarative Kubernetes manifests in the `k8s/` directory for local container orchestration.

### 1. Start Cluster & Create Namespace
```bash
minikube start --driver=docker
kubectl create namespace weather-local
kubectl config set-context --current --namespace=weather-local
```

### 2. Configure Secrets & Build Image
```bash
# Pass your OpenWeatherMap API key into Kubernetes Secret
kubectl create secret generic weather-secrets --from-literal=OPENWEATHER_API_KEY="YOUR_ACTUAL_API_KEY"

# Build image directly inside Minikube's Docker daemon
minikube image build -t weather-api:1.0 .
```

### 3. Deploy Resources to Kubernetes
```bash
# Apply all Kubernetes manifests (ConfigMap, Deployments, Services)
kubectl apply -f k8s/
```

### 4. Access Local Cluster & Scale
```bash
# Check pod status
kubectl get pods

# Forward service port to host machine
kubectl port-forward service/weather-api 8001:8000

# Open Swagger Docs in browser: http://localhost:8001/docs

# Experiment with horizontal pod scaling
kubectl scale deployment weather-api --replicas=4
```

---

## Kubernetes Manifests Structure

```
k8s/
├── configmap.yaml       # Non-sensitive runtime environment variables (REDIS_URL, REDIS_HOST)
├── api-deployment.yaml  # FastAPI workload deployment (2+ replicas, resource limits, health probes)
├── api-service.yaml     # Internal ClusterIP load balancing for FastAPI Pods
├── redis.yaml           # Single-instance Redis deployment and ClusterIP service
└── hpa.yaml             # Horizontal Pod Autoscaler configuration (CPU-based auto-scaling)
```

---

## Deployment Strategy

- **Production:** Continuous deployment on **Render** triggered by commits to `fastapi-migration` branch.
- **Local Sandbox:** Development, orchestration, auto-healing, and scaling tests managed independently via **Minikube**.

---

## Future Roadmap

- [ ] Horizontal Pod Autoscaling (HPA) fine-tuning under load test scenarios.
- [ ] Ingress Controller implementation for local domain routing.
- [ ] Helm Chart packaging for dynamic multi-environment values.
- [ ] CI/CD Pipeline automation using GitHub Actions.
- [ ] JWT Authentication & PostgreSQL database integration.

---

## Author

**Pooja Reddy**  
- **GitHub:** [@poojareddy240208-cyber](https://github.com/poojareddy240208-cyber)