from dataclasses import dataclass
from enum import Enum

from pydantic_settings import BaseSettings
from typing import List, Tuple


class TelegramBotConfig(BaseSettings):
    TELEGRAM_BOT_TOKEN: str


tg_bot_config: TelegramBotConfig = TelegramBotConfig()
