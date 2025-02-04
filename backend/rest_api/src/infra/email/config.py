from pydantic_settings import BaseSettings


class SMTPServerConfig(BaseSettings):
    MASTER_EMAIL: str
    SMTP_SERVER: str
    SMTP_SERVER_PORT: int = 537
    SMTP_SERVER_PASSWORD: str
    EMAIL_REPLY_TO: str


smtp_server_config: SMTPServerConfig = SMTPServerConfig()
