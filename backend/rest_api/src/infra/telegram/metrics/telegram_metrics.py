import time
from loguru import logger
from prometheus_client import Counter, Histogram


TELEGRAM_SENT = Counter(
    "qracun_telegram_messages_total",
    "Total number of telegram messages sent",
    ["status"]  # success | failure
)

TELEGRAM_LATENCY = Histogram(
    "qracun_telegram_send_duration_seconds",
    "Time spent sending telegram messages in seconds"
)


def metric_telegram_send(func):
    """Decorator to measure telegram send metrics"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            TELEGRAM_SENT.labels(status="success").inc()
            logger.info("Added metrics success")
            return result
        except Exception as e:
            TELEGRAM_SENT.labels(status="failure").inc()
            logger.info("Added metrics failure")
            raise e
        finally:
            duration = time.time() - start_time
            TELEGRAM_LATENCY.observe(duration)
            logger.info("Added metrics duration: {}", duration)

    return wrapper
