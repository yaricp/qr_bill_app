from prometheus_client import Counter, Histogram

from ..config import metric_config


prefix = metric_config.METRICS_PREFIX

# Define Prometheus metrics
HTTP_4XX_ERRORS = Counter(
    f"{prefix}_api_4xx_total",
    "Total 4xx HTTP responses",
    ["method", "endpoint"]
)

HTTP_5XX_ERRORS = Counter(
    f"{prefix}_api_5xx_total",
    "Total 5xx HTTP responses",
    ["method", "endpoint"]
)

REQUEST_COUNT = Counter(
    f"{prefix}_api_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    f"{prefix}_api_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)
