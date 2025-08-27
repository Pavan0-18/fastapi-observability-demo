🚀 FastAPI Observability Demo – Metrics, Logs & Traces

This repository demonstrates a complete observability stack for a FastAPI application using Prometheus, Grafana, Loki, Promtail, and Jaeger.

The project shows how to instrument a FastAPI service for metrics, logs, and traces, and visualize them in Grafana with pre-configured dashboards.

📂 Project Structure
observability-demo/
├── main.py                     # FastAPI service with observability instrumentation
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Service container configuration
├── docker-compose.yml          # Full observability stack orchestration
├── prometheus.yml              # Prometheus scrape configuration
├── loki-config.yml             # Loki configuration for log aggregation
├── promtail-config.yml         # Promtail configuration for log shipping
├── traffic_simulator.py        # Script to generate traffic/load on FastAPI service
└── grafana/
    ├── provisioning/
    │   └── datasources.yml     # Grafana datasources configuration
    └── dashboards/
        └── dashboard.json      # Pre-built Grafana dashboard

⚙️ Prerequisites

Docker
 & Docker Compose

Python 3.11+ (for local development & traffic simulation)

Git

🚦 Quick Start
1️⃣ Clone Repo and Setup
git clone https://github.com/<your-username>/fastapi-observability-demo.git
cd fastapi-observability-demo

2️⃣ Start the Stack
docker-compose up --build


(or run in detached mode)

docker-compose up --build -d

3️⃣ Verify Services

Once services are up (wait 30–60s):

FastAPI Service → http://localhost:8000

FastAPI Docs → http://localhost:8000/docs

Prometheus → http://localhost:9090

Grafana → http://localhost:3000
 (default login: admin/admin)

Jaeger UI → http://localhost:16686

4️⃣ Generate Traffic
pip install requests
python traffic_simulator.py


Or hit endpoints manually:

curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/simulate-work
curl http://localhost:8000/metrics

🔎 How It Works (Code + Stack Explanation)
FastAPI Service (main.py)

Metrics (Prometheus)

Instrumented with custom counters & histograms (e.g., request counts, durations).

/metrics endpoint exposes Prometheus metrics.

Tracing (OpenTelemetry + Jaeger)

Each request is traced as a span with metadata.

Traces flow through the OpenTelemetry exporter into Jaeger for visualization.

Logging (Structured JSON logs)

All logs are structured in JSON format with correlation IDs.

Promtail collects logs and sends them to Loki.

Grafana queries and visualizes logs.

Simulated Endpoints

/ → Basic request

/health → Health check

/simulate-work → Simulates variable response times & errors

Observability Stack

Prometheus – Scrapes FastAPI metrics and stores them.

Grafana – Pre-configured dashboard for request rate, latency, error rate, and logs.

Loki + Promtail – Collects logs from FastAPI container and makes them queryable in Grafana.

Jaeger – Stores and visualizes distributed traces.

📊 Grafana Dashboard Features

Request Rate – Requests per second

Latency Percentiles – P50, P95, P99 response times

Error Rate – Percentage of failed requests

Logs Panel – Live service logs with filtering

Trace Correlation – Jump from logs to Jaeger traces

🎥 Suggested Demo Flow (Screen Recording)

Start stack → docker-compose up --build

Open FastAPI docs & test endpoints

Run traffic_simulator.py to generate traffic

Open Grafana dashboard → show metrics updating live

Show logs in Grafana (filter by errors)

Open Jaeger → inspect traces and spans

Wrap up by explaining observability pillars (metrics, logs, traces)

🛠️ Cleanup
docker-compose down       # stop stack
docker-compose down -v    # stop & remove volumes

🔧 Troubleshooting

Port conflicts – Update docker-compose.yml ports.

Startup delay – Wait 60s for services to initialize.

Memory issues – Allocate at least 4GB to Docker.

Logs – View logs with:

docker-compose logs demo-service
docker-compose logs prometheus
docker-compose logs grafana
