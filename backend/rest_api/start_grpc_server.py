import asyncio

from loguru import logger
from prometheus_client import start_http_server
from src.infra.grpc_server.server import serve

if __name__ == "__main__":
    logger.info("before start GRPC server")
    start_http_server(90)
    logger.info("started Prometheus GRPC metrics server at port 90")
    asyncio.run(serve())
    logger.info("after stop GRPC server")
