import time

from loguru import logger
from prometheus_client import Counter, Histogram

from ..config import metric_config

prefix = metric_config.METRICS_PREFIX

ANALYTICS_REPORTS = Counter(
    f"{prefix}_analytics_reports_total",
    "Total number of analytics reports processed",
    ["status", "report_type"],  # добавлен label report_type
)

ANALYTICS_LATENCY = Histogram(
    f"{prefix}_analytics_report_duration_seconds",
    "Time spent generating analytics report in seconds",
    ["report_type"],  # label для типа отчёта
    buckets=[0.5, 1, 2, 5, 10, 30, 60],
)


def metric_analytics_async(func):
    async def wrapper(*args, **kwargs):
        report_type = func.__name__  # имя функции как тип отчёта
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            ANALYTICS_REPORTS.labels(status="success", report_type=report_type).inc()
            return result
        except Exception as e:
            ANALYTICS_REPORTS.labels(status="failure", report_type=report_type).inc()
            logger.error(f"Analytics error in {report_type}: {e}")
            raise e
        finally:
            duration = time.time() - start_time
            ANALYTICS_LATENCY.labels(report_type=report_type).observe(duration)
            logger.info(f"Analytics {report_type} duration: {duration:.3f}s")

    return wrapper
