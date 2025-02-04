from pydantic_settings import BaseSettings


class TelegramConfig(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_CHAT_ID: str


telegram_config: TelegramConfig = TelegramConfig()
