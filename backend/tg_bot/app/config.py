from pydantic_settings import BaseSettings
from typing import List

from utils import get_logger


logger = get_logger(__name__)


class TelegramBotConfig(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_DEFAULT_LANG: str
    TELEGRAM_WEBAPP_ADDRESS: str
    TELEGRAM_LANGUAGES: List[str]
    TELEGRAM_QR_PIC_DIR: str


tg_bot_config: TelegramBotConfig = TelegramBotConfig()

logger.info(f"tg_bot_config: {tg_bot_config}")
logger.info(
    f"tg_bot_config.TELEGRAM_LANGUAGES: {tg_bot_config.TELEGRAM_LANGUAGES}"
)
