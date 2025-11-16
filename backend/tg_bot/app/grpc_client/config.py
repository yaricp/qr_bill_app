from pydantic_settings import BaseSettings


class GRPCConfig(BaseSettings):
    TELEGRAM_GRPC_HOST: str
    TELEGRAM_GRPC_PORT: int


grpc_config: GRPCConfig = GRPCConfig()
