from utils import get_logger
from grpc_client import GPRCClient

from .config import login_link_conf

logger = get_logger(__name__)


def get_or_create_user(user_id: int) -> str:
    logger.info("get_or_create_user")
    gprc_client = GPRCClient(user_id=user_id)
    result = gprc_client.get_or_create_user()
    return result


def get_user_lang(user_id: int) -> str:
    gprc_client = GPRCClient(user_id=user_id)
    result = gprc_client.get_user_lang()
    return result


def set_user_lang(user_id: int, lang: str) -> str:
    gprc_client = GPRCClient(user_id=user_id)
    result = gprc_client.set_user_lang(lang=lang)
    return result


def get_login_url(user_id: int) -> str:
    gprc_client = GPRCClient(user_id=user_id)
    result = gprc_client.get_login_url()
    return result


def get_time_expiry_login_url() -> int:
    return login_link_conf.TIME_LIFE_TEMP_LOGIN_LINK_MIN
