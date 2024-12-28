import asyncio
from datetime import datetime
from concurrent import futures
from loguru import logger

import grpc

from . import grpc_pb2_grpc
from .grpc_pb2 import BillInfo, TotalSumm

from ...app.bill import BillCommands

from .config import grpc_server_config


class RestApiGRPC(grpc_pb2_grpc.RestApiGRPCServicer):

    def __init__(self):
        self.address = f"{grpc_server_config.GRPC_SERVER_HOST}"\
                        f":{grpc_server_config.GRPC_SERVER_PORT}"
        self.bill_commands = BillCommands()

    async def SendBillUrl(self, request, context: grpc.aio.ServicerContext):
        logger.info(f"request.name: {request.url}")
        result_bill = await self.bill_commands.parse_link_save_bill(request.url)
        logger.info(f"result_bill: {result_bill}")
        return BillInfo(
            date=str(result_bill.created),
            seller=result_bill.seller.official_name,
            address=result_bill.seller.address,
            summ=result_bill.value
        )

    async def GetTotalSumm(self, request, context: grpc.aio.ServicerContext):
        total_summ = await self.bill_commands.get_total_summ()
        return TotalSumm(
            summ=total_summ
        )


async def serve():
    rest_api_grpc = RestApiGRPC()
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )
    grpc_pb2_grpc.add_RestApiGRPCServicer_to_server(
        rest_api_grpc, server
    )
    server.add_insecure_port(rest_api_grpc.address)
    await server.start()
    logger.info(f"Server started, listening on {rest_api_grpc.address}")
    await server.wait_for_termination()


if __name__ == "__main__":
    logger.info("before start GRPC server")
    asyncio.run(serve())
    logger.info("after stop GRPC server")
