from prometheus_client import Counter, Histogram

# Define Prometheus metrics
HTTP_4XX_ERRORS = Counter(
    "qracun_api_4xx_total",
    "Total 4xx HTTP responses",
    ["method", "endpoint"]
)

HTTP_5XX_ERRORS = Counter(
    "qracun_api_5xx_total",
    "Total 5xx HTTP responses",
    ["method", "endpoint"]
)

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
