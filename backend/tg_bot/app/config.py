from pydantic_settings import BaseSettings


class TelegramBotConfig(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_DEFAULT_LANG: str
    TELEGRAM_WEBAPP_ADDRESS: str
    TELEGRAM_LANGUAGES: list


tg_bot_config: TelegramBotConfig = TelegramBotConfig()
