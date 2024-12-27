from datetime import datetime
from concurrent import futures
from loguru import logger

import grpc

import grpc_pb2_grpc
from grpc_pb2 import BillInfo, TotalSumm

from config import grpc_server_config


class RestApiGRPC(grpc_pb2_grpc.RestApiGRPCServicer):

    def __init__(self):
        self.address = f"{grpc_server_config.GRPC_SERVER_HOST}"\
                        f":{grpc_server_config.GRPC_SERVER_PORT}"

    def SendBillUrl(self, request, context):
        logger.info(f"request.name: {request.url}")
        return BillInfo(
            date=str(datetime.now()),
            seller="SEller1",
            summ=1700.0
        )

    def GetTotalSumm(self, request, context):
        return TotalSumm(
            summ=1500.0
        )


def serve():
    rest_api_grpc = RestApiGRPC()
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )
    grpc_pb2_grpc.add_RestApiGRPCServicer_to_server(
        rest_api_grpc, server
    )
    server.add_insecure_port(rest_api_grpc.address)
    server.start()
    logger.info(f"Server started, listening on {rest_api_grpc.address}")
    server.wait_for_termination()


if __name__ == "__main__":
    logger.info("before start GRPC server")
    serve()
    logger.info("after stop GRPC server")
