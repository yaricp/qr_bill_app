from pydantic_settings import BaseSettings


class SMTPServerConfig(BaseSettings):
    MASTER_EMAIL: str
    SMTP_SERVER: str
    SMTP_SERVER_PORT: int = 537
    SMTP_SERVER_PASSWORD: str
    EMAIL_REPLY_TO: str


class MetricsConfig(BaseSettings):
    METRICS_PREFIX: str = "my_app"


class AppConfig(BaseSettings):
    APP_NAME: str = "My Application"


smtp_server_config: SMTPServerConfig = SMTPServerConfig()
metrics_config: MetricsConfig = MetricsConfig()
app_config: AppConfig = AppConfig()
