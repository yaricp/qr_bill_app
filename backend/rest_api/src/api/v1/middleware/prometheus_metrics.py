import time
from fastapi import Request
from prometheus_client import Counter, Histogram


# Define Prometheus metrics
REQUEST_COUNT = Counter(
    "qracun_api_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "qracun_api_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)


async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        request.method,
        request.url.path,
        str(response.status_code)
    ).inc()
    REQUEST_LATENCY.labels(
        request.method, request.url.path
    ).observe(duration)

    return response
