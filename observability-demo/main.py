from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random
import logging
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])

app = FastAPI(title="Demo Service", description="A simple service with observability")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Update Prometheus metrics
    REQUEST_COUNT.labels(
        method=request.method, 
        endpoint=request.url.path, 
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method, 
        endpoint=request.url.path
    ).observe(process_time)
    
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log response
    logger.info(f"Response: {response.status_code} - Duration: {process_time:.4f}s")
    
    return response

@app.get("/")
async def root():
    """Root endpoint that returns a simple message"""
    logger.info("Root endpoint accessed")
    return {"message": "Hello World", "service": "demo-service"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/simulate-work")
async def simulate_work():
    """Endpoint that simulates some work with random delays"""
    # Simulate some work
    work_time = random.uniform(0.1, 2.0)
    logger.info(f"Simulating work for {work_time:.2f} seconds")
    
    time.sleep(work_time)
    
    # Sometimes simulate an error
    if random.random() < 0.1:  # 10% chance of error
        logger.error("Simulated error occurred")
        return {"status": "error", "message": "Simulated error"}, 500
    
    logger.info("Work completed successfully")
    return {
        "status": "completed", 
        "work_duration": work_time,
        "message": "Work simulation completed"
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)