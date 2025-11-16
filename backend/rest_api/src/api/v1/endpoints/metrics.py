from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from ... import app


@app.get("/metrics", tags=["Bills"])
def metrics():
    """
    Endpoint, which is used by Prometheus to scrape the metrics.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
