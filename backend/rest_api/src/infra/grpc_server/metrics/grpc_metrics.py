import time
import grpc
from prometheus_client import Counter, Histogram

from ..config import metric_config

prefix = metric_config.METRICS_PREFIX


GRPC_SERVER_STARTED = Counter(
    "grpc_server_started_total",
    "Total number of RPCs started on the server",
    ["grpc_service", "grpc_method"]
)

GRPC_SERVER_HANDLED = Counter(
    "grpc_server_handled_total",
    "Total number of RPCs completed on the server, regardless of success or failure",
    ["grpc_service", "grpc_method", "grpc_code"]
)

GRPC_SERVER_HANDLING_SECONDS = Histogram(
    "grpc_server_handling_seconds",
    "Histogram of response latency (seconds) of gRPC that had been application-level handled by the server",
    ["grpc_service", "grpc_method"]
)


class PrometheusInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        service, method = handler_call_details.method.split("/")[-2:]
        GRPC_SERVER_STARTED.labels(service, method).inc()

        handler = await continuation(handler_call_details)

        async def wrapper(request, context):
            start = time.time()
            try:
                response = await handler(request, context)
                GRPC_SERVER_HANDLED.labels(service, method, "OK").inc()
                return response
            except Exception:
                GRPC_SERVER_HANDLED.labels(service, method, "ERROR").inc()
                raise
            finally:
                duration = time.time() - start
                GRPC_SERVER_HANDLING_SECONDS.labels(service, method).observe(duration)

        return wrapper
