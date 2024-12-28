import asyncio
from loguru import logger

from src.infra.grpc_server.server import serve


if __name__ == "__main__":
    logger.info("before start GRPC server")
    asyncio.run(serve())
    logger.info("after stop GRPC server")
