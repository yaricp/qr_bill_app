from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from ... import app


@app.get("/metrics")
def metrics():
    """
    Endpoint, which is used by Prometheus to scrape the metrics."""
    return Response(
        generate_latest(), media_type=CONTENT_TYPE_LATEST
    )
