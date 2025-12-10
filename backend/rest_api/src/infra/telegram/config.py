from pydantic_settings import BaseSettings


class TelegramConfig(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_CHAT_ID: str


class MetricsConfig(BaseSettings):
    METRICS_PREFIX: str = "my_app"


telegram_config: TelegramConfig = TelegramConfig()
metric_config: MetricsConfig = MetricsConfig()
