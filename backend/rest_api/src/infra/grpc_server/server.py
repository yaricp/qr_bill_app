import asyncio
from datetime import datetime
from concurrent import futures
from loguru import logger

import grpc

from . import grpc_pb2_grpc
from .grpc_pb2 import (
    BillInfo, TotalSumm, TgUserID, UserLangEditForm,
    UserLang, LoginURL
)

from ...app.bill import BillCommands
from ...app.user import UserCommands, UserQueries
from ...app.entities.user import UserUpdate

from .config import grpc_server_config


class RestApiGRPC(grpc_pb2_grpc.RestApiGRPCServicer):

    def __init__(self):
        self.address = f"{grpc_server_config.GRPC_SERVER_HOST}"\
                        f":{grpc_server_config.GRPC_SERVER_PORT}"
        self.bill_commands = BillCommands()

        self.user_commands = UserCommands()
        self.user_queries = UserQueries()

    async def SendBillUrl(
        self, request, context: grpc.aio.ServicerContext
    ) -> BillInfo:
        logger.info(f"request.name: {request.url}")
        # result_bill = BillInfo(
        #     date="user not found",
        #     seller="user not found",
        #     address="user not found",
        #     summ=0.0
        # )
        user = await self.user_commands.register_user_by_tg_id(
            tg_id=request.tg_user_id
        )
        if user:
            result_bill = await self.bill_commands.parse_link_save_bill(
                request.url, user_id=user.id
            )
            logger.info(f"result_bill: {result_bill}")
        return BillInfo(
            date=str(result_bill.created),
            seller=result_bill.seller.official_name,
            address=result_bill.seller.address,
            summ=result_bill.value
        )

    async def GetTotalSumm(
        self, request, context: grpc.aio.ServicerContext
    ) -> TotalSumm:
        total_summ = await self.bill_commands.get_total_summ(
            user_id=request.tg_user_id
        )
        return TotalSumm(
            summ=total_summ
        )

    async def GetOrCreateUser(
        self, request, context: grpc.aio.ServicerContext
    ) -> UserLang:
        user = await self.user_commands.register_user_by_tg_id(
            tg_id=request.tg_user_id
        )
        return UserLang(lang=user.lang)

    async def GetUserLang(
        self, request, context: grpc.aio.ServicerContext
    ) -> UserLang:
        user = self.user_queries.get_user_by_tg_id(
            tg_id=request.tg_user_id
        )
        return UserLang(lang=user.lang)

    async def SetUserLang(
        self, request, context: grpc.aio.ServicerContext
    ) -> UserLang:
        user_db = await self.user_queries.get_by_tg_id(
            request.tg_user_id
        )
        user_income = UserUpdate(
            id=user_db.id,
            lang=request.lang
        )
        user = await self.user_commands.edit_user(
            user_income
        )
        return UserLang(lang=user.lang)

    async def GetLoginURL(
        self, request, context: grpc.aio.ServicerContext
    ) -> LoginURL:
        url = await self.user_commands.create_temp_login_link_by_tg_id(
            tg_id=request.tg_user_id
        )
        logger.info(f"url: {url} in method of GRPC SErver")
        return LoginURL(url=url)


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
