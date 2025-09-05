from prometheus_client import Counter, Histogram

from ..config import metric_config


prefix = metric_config.METRICS_PREFIX


BILLS_PROCESSED = Counter(
    f"{prefix}_bills_processed_total",
    "Total number of checks processed",
    ["status"]   # success | failure
)

BILLS_VALIDATED = Counter(
    f"{prefix}_bills_validated_total",
    "Total number of checks processed",
    ["status"]   # success | failure
)

BILLS_CREATED = Counter(
    f"{prefix}_bills_created_total",
    "Total number of checks processed",
    ["status"]   # success | failure
)


EXTERNAL_API_CALLS = Counter(
    f"{prefix}_external_api_requests_total",
    "Total number of external API requests",
    ["api_name", "status"]  # status: success | failure | timeout
)


EXTERNAL_API_LATENCY = Histogram(
    f"{prefix}_external_api_request_duration_seconds",
    "Latency of external API requests in seconds",
    ["api_name"]
)

BILL_PROCESSING_TIME = Histogram(
    f"{prefix}_bill_processing_duration_seconds",
    "End-to-end time of bill processing",
    ["status"],  # success | failure
    buckets=[1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 10, 30]
)


def metric_bill_processing_time(status: str, duration: float) -> None:
    BILL_PROCESSING_TIME.labels(status=status).observe(duration)


def metric_processed_bill(status: str) -> None:
    BILLS_PROCESSED.labels(status=status).inc()


def metric_validated_bill(status: str) -> None:
    BILLS_VALIDATED.labels(status=status).inc()


def metric_call_external_api(
    api_name: str, status: str, delay: float
) -> None:
    EXTERNAL_API_CALLS.labels(
        api_name=api_name, status=status
    ).inc()
    EXTERNAL_API_LATENCY.labels(api_name=api_name).observe(delay)


def metric_created_bill(status: str) -> None:
    BILLS_CREATED.labels(status=status).inc()


def metric_processed_analitics_total() -> None:
    pass
