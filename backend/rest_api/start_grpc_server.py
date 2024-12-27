from loguru import logger

from infra.grpc_server.server import serve


if __name__ == "__main__":
    logger.info("before start GRPC server")
    serve()
    logger.info("after stop GRPC server")
