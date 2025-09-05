from utils import get_logger
from grpc_client import GPRCClient


logger = get_logger(__name__)


async def send_bill_url(url: str, user_id: int):
    gprc_client = GPRCClient(user_id=user_id)
    result = await gprc_client.send_bill_url(url)
    return result
