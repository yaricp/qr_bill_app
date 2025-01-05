from pydantic_settings import BaseSettings


class TelegramBotConfig(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_DEFAULT_LANG: str
    QR_PIC_DIR: str
    GRPC_HOST: str
    GRPC_PORT: int


tg_bot_config: TelegramBotConfig = TelegramBotConfig()
