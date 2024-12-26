from utils import get_logger


logger = get_logger(__name__)


def get_or_create_user(tg_user_id: int, name: str) -> str:
    logger.info("get_or_create_user")
    return f"{name} - {tg_user_id}"


def get_user_lang(tg_user_id: int):
    logger.info("get_user_lang")
    return "ru"
