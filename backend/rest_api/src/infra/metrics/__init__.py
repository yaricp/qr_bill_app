# импортируем все метрики из модулей приложения
from api.metrics.http import *
from app.metrics.operations import *
from infra.database.metrics.db_metrics import *
from infra.grpc_server.metrics.grpc_metrics import *
from infra.telegram.metrics.telegram_metrics import *
from infra.email.metrics.email_metrics import *

from prometheus_client import make_asgi_app


# создаём единый ASGI endpoint для Prometheus
metrics_app = make_asgi_app()
