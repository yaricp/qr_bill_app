import time

from fastapi import Request

from ..metrics.http import (HTTP_4XX_ERRORS, HTTP_5XX_ERRORS, REQUEST_COUNT,
                            REQUEST_LATENCY)


async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        request.method, request.url.path, str(response.status_code)
    ).inc()
    REQUEST_LATENCY.labels(request.method, request.url.path).observe(duration)

    if 400 <= response.status_code < 500:
        HTTP_4XX_ERRORS.labels(request.method, request.url.path).inc()
    elif 500 <= response.status_code < 600:
        HTTP_5XX_ERRORS.labels(request.method, request.url.path).inc()

    return response
