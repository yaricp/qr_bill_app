import time

from loguru import logger
from prometheus_client import Counter, Histogram

from ..config import metrics_config

prefix = metrics_config.METRICS_PREFIX

EMAIL_SENT = Counter(
    f"{prefix}_email_sent_total",
    "Total number of emails sent",
    ["status"],  # success | failure
)

EMAIL_LATENCY = Histogram(
    f"{prefix}_email_send_duration_seconds", "Time spent sending emails in seconds"
)


def metric_email_client(func):
    def wrapper(*args, **kwargs):
        logger.info("start Email Client metrics")
        logger.info(f"args: {args}, kwargs: {kwargs}")
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            EMAIL_SENT.labels(status="success").inc()
            logger.info("Added Email Client metrics success")
            return result
        except Exception as e:
            EMAIL_SENT.labels(status="failure").inc()
            logger.error("Added Email Client metrics failure")
            raise e
        finally:
            duration = time.time() - start_time
            EMAIL_LATENCY.observe(duration)
            logger.info("Added Email Client metrics duration")

    return wrapper
