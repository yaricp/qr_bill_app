from __future__ import print_function

import grpc
from google.protobuf.json_format import MessageToDict

from .grpc_pb2_grpc import RestApiGRPCStub
from .grpc_pb2 import BillInfo, TotalSumm, BillUrl

# from bot.utils import get_logger
from config import tg_bot_config
from loguru import logger

# logger = get_logger(__name__)


class GPRCClient:

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.api_address =  f"{tg_bot_config.GRPC_HOST}"\
                            f":{tg_bot_config.GRPC_PORT}"

    def send_bill_url(self, url: str) -> dict:
        with grpc.insecure_channel(self.api_address) as channel:
            stub = RestApiGRPCStub(channel)
            response = stub.SendBillUrl(
                BillUrl(url=url)
            )
        logger.info(f"response: {response}")
        return MessageToDict(response)
